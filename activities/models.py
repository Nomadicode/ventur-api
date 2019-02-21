from django.db import models
from graphene_django.converter import convert_django_field
from recurrence.fields import RecurrenceField

from users.models import User


# Create your models here.
class RepeatOptions(models.Model):
    name = models.CharField(max_length=64)


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Categories'


class Schedule(models.Model):
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    repeat = models.ForeignKey(RepeatOptions, related_name='repeat', on_delete=models.DO_NOTHING, default=1)


class Location(models.Model):
    address = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Activity(models.Model):
    name = models.CharField(max_length=64)
    media = models.FileField(upload_to='activities', blank=True, null=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='categories')
    location = models.ForeignKey(Location, related_name='location', on_delete=models.DO_NOTHING)
    duration = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    kid_friendly = models.BooleanField(default=False)
    handicap_friendly = models.BooleanField(default=False)
    over_18 = models.BooleanField(default=False)
    over_21 = models.BooleanField(default=False)
    recurrence = RecurrenceField(blank=True, null=True)
    schedule = models.ForeignKey(Schedule, related_name='schedule', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE, null=True, blank=True)


@convert_django_field.register(RecurrenceField)
def convert_field_to_object(field, registry=None):
    return None
