import uuid
from django.db import models
from dateutil import parser

from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import GEOSGeometry
from django.db import IntegrityError
from django.contrib.gis.geos import Point
from graphene_django.converter import convert_django_field
from scheduling.models import BaseEvent, BaseOccurrence

from api.helpers import get_address_from_latlng, get_latlng_from_address

from users.models import User
from friends.models import Group

from scheduling.models import EventManager

REPEAT_CHOICES = [
    'Yearly',
    'Monthly',
    'Weekly',
    'Daily'
]


class ActivityManager(EventManager):
    def create_activity(self, name, latitude, longitude, user=None, start_datetime=None, end_datetime=None,
                        repeat_until=None, frequency=None, categories=None, groups=None, **extra_fields):
        if not user:
            user = User.objects.filter(is_system=True).first()

        activity = self.model(name=name, created_by=user, **extra_fields)

        # region Set Location
        if latitude and longitude:
            location_data = {
                'name': extra_fields['location_name'] if 'location_name' in extra_fields else None,
                'address': extra_fields['location_address'] if 'location_address' in extra_fields else None,
                'latitude': latitude,
                'longitude': longitude,
                'point': None
            }

            if latitude and longitude:
                location_data['name'], location_data['address'] = get_address_from_latlng(latitude, longitude)

            location_data['point'] = GEOSGeometry('POINT(%s %s)' % (location_data['longitude'], location_data['latitude']),
                                                  srid=4326)

            try:
                location, created = Location.objects.get_or_create(**location_data)
            except IntegrityError:
                raise Exception('Activities require location')

            activity.location = location

        else:
            raise Exception('Missing Information: Latitude and Longitude are required')
        # endregion

        activity.save()

        # region Set groups
        if groups:
            group_list = filter(None, groups)
            activity.groups.set(group_list)
        # endregion

        # region Set categories
        if categories:
            category_list = filter(None, categories)
            activity.categories.set(category_list)
        # endregion

        # region Set Schedule
        schedule = None
        if start_datetime and end_datetime:
            schedule = Schedule(
                start=parser.parse(start_datetime),
                end=parser.parse(end_datetime)
            )
            print(frequency)
            if frequency and frequency > -1:
                frequency_txt = REPEAT_CHOICES[frequency] if frequency < 4 else None

                if frequency_txt:
                    schedule.repeat = 'RRULE:FREQ=' + frequency_txt

                if repeat_until:
                    schedule.repeat_until = parser.parse(repeat_until)

        if schedule:
            schedule.event = activity
            schedule.save()
        # endregion

        return activity


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=10)
    decimal_digits = models.IntegerField(default=2)
    decimal_separator = models.CharField(max_length=1)
    thousands_separator = models.CharField(max_length=1)
    space_symbol = models.BooleanField(default=False)
    symbol_left = models.BooleanField(default=True)


class Location(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()
    point = geomodels.PointField(null=True, blank=True)
    currency = models.ForeignKey(Currency, related_name='currency', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.address

class Activity(BaseEvent):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=256)
    media = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='categories', blank=True)
    location = models.ForeignKey(Location, related_name='location', on_delete=models.DO_NOTHING)
    duration = models.IntegerField(null=True, blank=True)
    minimum_price = models.FloatField(null=True, blank=True, default=0)
    maximum_price = models.FloatField(null=True, blank=True)
    minimum_age = models.IntegerField(default=0)
    maximum_age = models.IntegerField(default=65)
    handicap_friendly = models.BooleanField(default=False)
    is_nsfw = models.BooleanField(default=False)
    kid_friendly = models.BooleanField(default=False)
    alcohol_present = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='allowed_groups', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE, null=True, blank=True)

    objects = ActivityManager()

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return '{} -> {}'.format(self.id, self.name)

class Schedule(BaseOccurrence):
    event = models.ForeignKey(Activity, related_name="schedule", on_delete=models.CASCADE)
