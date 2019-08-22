import graphene
from django.db.models import Q
from graphene import relay
from graphene_django.types import DjangoObjectType
from api.helpers import get_user_from_info, get_distance

from api.enums import Errors
from users.models import User
from users.schema import UserType, UserConnection
from .models import Group
from friendship.models import Friend, FriendshipRequest, Block


class FriendshipType(DjangoObjectType):
    pk = graphene.ID()

    class Meta:
        model = Friend


class GroupType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Group


class FriendshipConnection(relay.Connection):
    class Meta:
        node = FriendshipType


class GroupConnection(relay.Connection):
    class Meta:
        node = GroupType


class FriendshipRequestType(DjangoObjectType):
    pk = graphene.ID()

    class Meta:
        model = FriendshipRequest


class FriendQuery(object):
    friendships = relay.ConnectionField(UserConnection)
    sent_friend_requests = graphene.List(FriendshipRequestType)
    pending_friend_requests = graphene.List(FriendshipRequestType)
    friend_groups = graphene.List(GroupType)
    friend_groups_paged = relay.ConnectionField(GroupConnection, query=graphene.String())
    blocked_users = graphene.List(UserType)
    search_users = graphene.List(UserType, query=graphene.String())
    friend_suggestions = graphene.List(UserType)

    def resolve_friendships(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            raise Exception(Errors.AUTH)

        friends = Friend.objects.friends(user)

        return friends

    def resolve_sent_friend_requests(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            raise Exception(Errors.AUTH)

        return FriendshipRequest.objects.filter(from_user=user, rejected__isnull=True)

    def resolve_pending_friend_requests(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            raise Exception(Errors.AUTH)

        return FriendshipRequest.objects.filter(to_user=user, rejected__isnull=True)

    def resolve_friend_groups_paged(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            raise Exception(Errors.AUTH)

        groups = Group.objects.filter(creator=user)

        if 'query' in kwargs:
            groups = groups.filter(name__icontains=kwargs['query'])

        return groups

    def resolve_friend_groups(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            raise Exception(Errors.AUTH)

        return Group.objects.filter(creator=user)

    def resolve_blocked_users(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            raise Exception(Errors.AUTH)

        return Block.objects.blocking(user)

    def resolve_search_users(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            raise Exception(Errors.AUTH)

        if not 'query' in kwargs:
            return []

        # Remove self from results
        users = User.objects.all().exclude(id__in=(user.id,))
        users = users.exclude(is_system=True)

        # Remove users that have been sent requests
        # requests = FriendshipRequest.objects.filter(from_user__id=user.id)

        # sent_requests = []
        # for req in requests:
        #     sent_requests.append(req.to_user.id)
        #
        # users = users.exclude(id__in=sent_requests)

        # Remove users that sent user requests
        # requests = FriendshipRequest.objects.filter(to_user__id=user.id)
        # pending_requests = []
        # for req in requests:
        #     pending_requests.append(req.from_user.id)
        #
        # users = users.exclude(id__in=pending_requests)

        # Remove existing friends
        # friends = Friend.objects.filter(from_user__id=user.id)
        #
        # existing_friends = []
        # for friend in friends:
        #     existing_friends.append(friend.to_user.id)
        #
        # users = users.exclude(id__in=existing_friends)

        # Check handle
        users = users.filter(Q(handle__icontains=kwargs['query']) |
                             Q(name__icontains=kwargs['query']) |
                             Q(email__icontains=kwargs['query']))

        return users

    def resolve_friend_suggestions(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            raise Exception('Authentication Error')

        # Remove self from results
        users = User.objects.all().exclude(id__in=(user.id,))
        users = users.exclude(is_system=True)

        # Remove users that have been sent requests
        requests = FriendshipRequest.objects.filter(from_user__id=user.id)

        sent_requests = []
        for req in requests:
            sent_requests.append(req.to_user.id)

        users = users.exclude(id__in=sent_requests)

        # Remove users that sent user requests
        requests = FriendshipRequest.objects.filter(to_user__id=user.id)
        pending_requests = []
        for req in requests:
            pending_requests.append(req.from_user.id)

        users = users.exclude(id__in=pending_requests)

        # Remove existing friends
        friends = Friend.objects.filter(from_user__id=user.id)

        existing_friends = []
        for friend in friends:
            existing_friends.append(friend.to_user.id)

        users = users.exclude(id__in=existing_friends)

        # Refine by location
        discard_distance = []
        for suggest in users:
            if suggest.location and user.location:
                distance = get_distance(user.location, suggest.location).split(' ')[0]
                if float(distance) > 10.0:
                    discard_distance.append(suggest.id)

        users = users.exclude(id__in=discard_distance)

        # Refine by shared interests

        return users