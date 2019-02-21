import graphene

from graphene_django.types import DjangoObjectType
from api.helpers import get_user_from_info

from .models import FriendRequest, Friendship, Group


class FriendshipType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Friendship


class FriendRequestType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = FriendRequest


class GroupType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Group


class FriendQuery(object):
    friends = graphene.List(FriendshipType)
    sent_friend_requests = graphene.List(FriendRequestType)
    incoming_friend_requests = graphene.List(FriendRequestType)
    friend_groups = graphene.List(GroupType)

    def resolve_friends(self, info, **kwargs):
        user = get_user_from_info(info)

        if user.is_authenticated:
            return Friendship.objects.filter(user=user)

        return None

    def resolve_sent_friend_requests(self, info, **kwargs):
        user = get_user_from_info(info)

        if user.is_authenticated:
            return FriendRequest.objects.filter(initiator=user)

        return None

    def resolve_incoming_friend_requests(self, info, **kwargs):
        user = get_user_from_info(info)

        if user.is_authenticated:
            return FriendRequest.objects.filter(recipient=user)

        return None

    def resolve_friend_groups(self, info, **kwargs):
        user = get_user_from_info(info)

        if user.is_authenticated:
            return Group.objects.filter(creator=user)

        return None
