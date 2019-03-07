import graphene
from django.db.models import Q
from graphene_django.types import DjangoObjectType
from api.helpers import get_user_from_info

from .models import Relationship, Group


class RelationshipType(DjangoObjectType):
    pk = graphene.Int()
    status = graphene.String()

    class Meta:
        model = Relationship

    def resolve(self, info, **kwargs):
        if 'status' in self:
            return self.get_status_display()


class GroupType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Group


class FriendQuery(object):
    relationships = graphene.List(RelationshipType)
    friend_groups = graphene.List(GroupType)

    def resolve_relationships(self, info, **kwargs):
        user = get_user_from_info(info)

        if user.is_authenticated:
            return Relationship.objects.filter(Q(user=user) | Q(initiator=user))

        return None

    def resolve_friend_groups(self, info, **kwargs):
        user = get_user_from_info(info)

        if user.is_authenticated:
            return Group.objects.filter(creator=user)

        return None
