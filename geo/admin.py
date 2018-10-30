from django.contrib import admin

from .models import Continent, Country, City, Region, Location


class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name', 'alpha_2_code', )


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'alpha_3_code', 'alpha_2_code', 'continent', )


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'alpha_2_code', 'country', )


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', )


class LocationAdmin(admin.ModelAdmin):
    list_display = ('address_line_1', 'city', 'region', )


admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Location, LocationAdmin)