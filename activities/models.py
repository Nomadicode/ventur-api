from django.db import models
from recurrence.fields import RecurrenceField

from users.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'categories'


class AgeRange(models.Model):
    label = models.CharField(max_length=32)
    min_age = models.IntegerField()
    max_age = models.IntegerField()


class Activity(models.Model):
    created_by = models.ForeignKey(User, related_name='activities', null=True, blank=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    media = models.FileField(upload_to='activity', null=True, blank=True)
    age_ranges = models.ManyToManyField(AgeRange)
    recurrences = RecurrenceField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'activities'
