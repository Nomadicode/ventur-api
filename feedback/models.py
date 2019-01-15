from django.db import models

from users.models import User


# Create your models here.
class FeedbackCategory(models.Model):
    name = models.CharField(max_length=64)


class Feedback(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.DO_NOTHING, null=True, blank=True)
    subject = models.CharField(max_length=128)
    category = models.ForeignKey(FeedbackCategory, related_name='category', on_delete=models.DO_NOTHING)
    details = models.TextField()
