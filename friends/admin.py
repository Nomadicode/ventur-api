from django.contrib import admin
from friends.models import Group


# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator', 'num_members')

admin.site.register(Group, GroupAdmin)