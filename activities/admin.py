from django.contrib import admin
from activities.models import Activity, Category


# Register your models here.
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'location')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Category, CategoryAdmin)