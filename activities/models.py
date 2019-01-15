from django.db import models

from users.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Categories'


class Schedule(models.Model):
    NO_REPEAT = 'NONE'
    DAILY = 'DAY'
    WEEKLY = 'WEEK'
    MONTHLY = 'MON'
    WEEKDAY = 'WDAY'
    WEEKEND = 'WEND'
    REPEAT_CHOICES = (
        (NO_REPEAT, 'No Repeat'),
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (WEEKDAY, 'Weekday'),
        (WEEKEND, 'Weekend'),
    )

    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    repeat = models.CharField(max_length=4, choices=REPEAT_CHOICES, default=NO_REPEAT)


class Location(models.Model):
    address = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Activity(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    categories = models.ManyToManyField(Category, related_name='categories')
    location = models.ForeignKey(Location, related_name='location', on_delete=models.DO_NOTHING)
    duration = models.IntegerField()
    price = models.FloatField()
    kid_friendly = models.BooleanField(default=False)
    handicap_friendly = models.BooleanField(default=False)
    over_18 = models.BooleanField(default=False)
    over_21 = models.BooleanField(default=False)
    schedule = models.ForeignKey(Schedule, related_name='schedule', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE, null=True, blank=True)
