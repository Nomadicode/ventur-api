from django.db import models


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
    title = models.CharField(max_length=128)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    media = models.FileField(upload_to='activity', null=True, blank=True)
    age_ranges = models.ManyToManyField(AgeRange)

    class Meta:
        verbose_name_plural = 'activities'


class Schedule(models.Model):
    activity = models.ForeignKey(Activity, related_name='activity', on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    