import uuid
from django.db import models

from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import Point
from graphene_django.converter import convert_django_field
# from recurrence.fields import RecurrenceField
from eventtools.models import BaseEvent, BaseOccurrence


from users.models import User
from friends.models import Group

REPEAT_CHOICES = [
    'Yearly',
    'Monthly',
    'Weekly',
    'Daily'
]

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()
    point = geomodels.PointField(null=True, blank=True)

    def __str__(self):
        return self.address

class Activity(BaseEvent):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=64)
    media = models.FileField(upload_to='activities', blank=True, null=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='categories', blank=True)
    location = models.ForeignKey(Location, related_name='location', on_delete=models.DO_NOTHING)
    duration = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    minimum_age = models.IntegerField(default=0)
    maximum_age = models.IntegerField(default=65)
    handicap_friendly = models.BooleanField(default=False)
    is_nsfw = models.BooleanField(default=False)
    alcohol_present = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='allowed_groups', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return '{} -> {}'.format(self.id, self.name)

class Schedule(BaseOccurrence):
    event = models.ForeignKey(Activity, related_name="schedule", on_delete=models.CASCADE)

#
# @convert_django_field.register(RecurrenceField)
# def convert_field_to_object(field, registry=None):
#     return None