from django.db import models

from users.models import User


# Create your models here.
class Relationship(models.Model):
    STATUS_CHOICES = (
        (1, 'Requested'),
        (2, 'Accepted'),
        (3, 'Rejected')
    )
    initiator = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='relationship', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created = models.DateTimeField(auto_now_add=True)


# class FriendRequest(models.Model):
#     initiator = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
#     recipient = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    creator = models.ForeignKey(User, related_name='friend_groups', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    friends = models.ManyToManyField(User, blank=True)
    created = models.DateTimeField(auto_now_add=True)
#
#
# class BlockedUser(models.Model):
#     creator = models.ForeignKey(User, related_name='blocked_users', on_delete=models.CASCADE)
#     blocked_user = models.ForeignKey(User, related_name='blocked_users', on_delete=models.CASCADE)
#     blocked = models.DateTimeField(auto_now_add=True)
