from django.db import models

from users.models import User


# Create your models here.
class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend', on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)


class FriendRequest(models.Model):
    initiator = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    creator = models.ForeignKey(User, related_name='friend_groups', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    friends = models.ManyToManyField(User, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
#
#
# class BlockedUser(models.Model):
#     creator = models.ForeignKey(User, related_name='blocked_users', on_delete=models.CASCADE)
#     blocked_user = models.ForeignKey(User, related_name='blocked_users', on_delete=models.CASCADE)
#     blocked = models.DateTimeField(auto_now_add=True)
