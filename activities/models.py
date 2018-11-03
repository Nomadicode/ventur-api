from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'categories'


class Activity(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    media = models.FileField(upload_to='activity', null=True, blank=True)
    # location = models.ForeignKey(Location, related_name='location', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'activities'
    