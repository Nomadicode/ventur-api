from django.contrib import admin

from .models import Continent, Country, Region


class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name', 'alpha_2_code', )


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'alpha_3_code', 'alpha_2_code', 'continent', )


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'alpha_2_code', 'country', )


admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
