from django.db import models

from users.models import User
from activities.models import Activity


# Create your models here.
class RejectedActivity(models.Model):
    activity = models.ForeignKey(Activity, related_name='rejected_activities', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='rejected_activities', on_delete=models.CASCADE)
    rejected = models.DateTimeField(auto_now_add=True)


class AcceptedActivity(models.Model):
    activity = models.ForeignKey(Activity, related_name='accepted_activities', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='accepted_activities', on_delete=models.CASCADE)
    accepted = models.DateTimeField(auto_now_add=True)


class SavedActivity(models.Model):
    activity = models.ForeignKey(Activity, related_name='saved_activities', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='saved_activities', on_delete=models.CASCADE)
    saved = models.DateTimeField(auto_now_add=True)
