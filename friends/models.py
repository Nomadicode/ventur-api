from django.db import models

from users.models import User


# Create your models here.
class Group(models.Model):
    creator = models.ForeignKey(User, related_name='friend_groups', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    friends = models.ManyToManyField(User, related_name='group_memberships', blank=True)
    created = models.DateTimeField(auto_now_add=True)
