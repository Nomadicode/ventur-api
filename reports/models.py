from django.db import models

from activities.models import Activity
from users.models import User


# Create your models here.
class ReportCategory(models.Model):
    name = models.CharField(max_length=64)
    detail = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name


class Report(models.Model):
    activity = models.ForeignKey(Activity, related_name='reports', on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, related_name='reported_activities', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(ReportCategory, related_name='reason', on_delete=models.DO_NOTHING)
    detail = models.CharField(max_length=128, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {}:{}'.format(self.reporter.id, self.activity.id, self.activity.name)