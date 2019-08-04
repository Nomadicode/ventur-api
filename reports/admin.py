from django.contrib import admin

from reports.models import Report, ReportCategory

# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'category', 'created', 'upheld', 'resolved')

class ReportCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'detail')

admin.site.register(Report, ReportAdmin)
admin.site.register(ReportCategory, ReportCategoryAdmin)