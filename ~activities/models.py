from django.db import models

from users.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'categories'


class Activity(models.Model):
    created_by = models.ForeignKey(User, related_name='activities', null=True, blank=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    kid_friendly = models.BooleanField(default=True)
    handicap_friendly = models.BooleanField(default=True)
    over_18 = models.BooleanField(default=True)
    over_21 = models.BooleanField(default=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        verbose_name_plural = 'activities'
