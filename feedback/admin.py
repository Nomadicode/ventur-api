from django.contrib import admin
from feedback.models import Feedback, FeedbackCategory


# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'category', 'details', 'responded')

class FeedbackCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackCategory, FeedbackCategoryAdmin)