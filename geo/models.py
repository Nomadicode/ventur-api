from django.db import models


# Create your models here.
class Continent(models.Model):
    name = models.CharField(max_length=64)
    alpha_2_code = models.CharField(max_length=2)

    def __str__(self):
        return self.alpha_2_code


class Country(models.Model):
    name = models.CharField(max_length=128)
    alpha_2_code = models.CharField(max_length=2)
    alpha_3_code = models.CharField(max_length=3)
    continent = models.ForeignKey('Continent', related_name='countries', on_delete=models.CASCADE)

    def __str__(self):
        return self.alpha_3_code

    class Meta:
        verbose_name_plural = 'countries'


class Region(models.Model):
    name = models.CharField(max_length=128)
    alpha_2_code = models.CharField(max_length=5)
    country = models.ForeignKey('Country', related_name='regions', on_delete=models.CASCADE)

    def __str__(self):
        return self.alpha_2_code


class City(models.Model):
    name = models.CharField(max_length=256)
    region = models.ForeignKey('Region', related_name='cities', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=16, decimal_places=13)
    longitude = models.DecimalField(max_digits=16, decimal_places=13)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
        

class Location(models.Model):
    address_line_1 = models.CharField(max_length=64)
    address_line_2 = models.CharField(max_length=64, blank=True, null=True)
    city = models.ForeignKey(City, related_name='city', on_delete=models.CASCADE, blank=True, null=True)
    region = models.ForeignKey(Region, related_name='state', on_delete=models.CASCADE, blank=True, null=True)
    zipcode = models.CharField(max_length=5, blank=True, null=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=10)
    longitude = models.DecimalField(max_digits=14, decimal_places=10)