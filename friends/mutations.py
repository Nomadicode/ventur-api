import graphene

from api.helpers import get_user_from_info, base64_to_file

from users.models import User

from .models import Relationship
from .serializers import GroupSerializer, RelationshipSerializer
from .schema import GroupType, RelationshipType


class FriendGroupAddMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    group = graphene.Field(GroupType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return FriendGroupAddMutation(success=False,
                                          error="You must be logged in to create a group.",
                                          group=None)

        kwargs['creator'] = user.id
        serializer = GroupSerializer(data=kwargs)

        if not serializer.is_valid():
            return FriendGroupAddMutation(success=False,
                                          error=str(serializer.errors),
                                          group=None)

        instance = serializer.save()
        return FriendGroupAddMutation(success=True, error=None, group=instance)


class RelationshipAddMutation(graphene.Mutation):
    class Arguments:
        handle = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    relationship = graphene.Field(RelationshipType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return RelationshipAddMutation(success=False,
                                           error="You must be logged in to create a relationship.",
                                           relationship=None)

        kwargs['initiator'] = user.id

        if 'handle' in kwargs:
            try:
                kwargs['user'] = User.objects.get(handle=kwargs['handle']).id
            except User.DoesNotExist:
                return RelationshipAddMutation(success=False,
                                               error="Unable to find user with handle %s".format(kwargs['handle']),
                                               relationship=None)

        serializer = RelationshipSerializer(data=kwargs)

        if not serializer.is_valid():
            return RelationshipAddMutation(success=False,
                                           error=str(serializer.errors),
                                           relationship=None)

        instance = serializer.save()
        return RelationshipAddMutation(success=True, error=None, relationship=instance)


class RelationshipAcceptMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    relationship = graphene.Field(RelationshipType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return RelationshipAcceptMutation(success=False,
                                              error="You must be logged in to update a relationship.",
                                              relationship=None)

        try:
            relationship = Relationship.objects.get(pk=kwargs['pk'], user_id=user.id)
        except Relationship.DoesNotExist:
            return RelationshipAcceptMutation(success=False,
                                              error="An error occurred updating relationship")

        kwargs['status'] = 2
        serializer = RelationshipSerializer(relationship, data=kwargs, partial=True)

        if not serializer.is_valid():
            return RelationshipAcceptMutation(success=False,
                                              error=str(serializer.errors),
                                              relationship=None)

        instance = serializer.save()
        return RelationshipAcceptMutation(success=True, error=None, relationship=instance)


class RelationshipRemoveMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return RelationshipRemoveMutation(success=False,
                                              error="You must be logged in to create a group.",
                                              relationship=None)

        try:
            relationship = Relationship.objects.get(pk=kwargs['pk'], user_id=user.id)
        except Relationship.DoesNotExist:
            return RelationshipAcceptMutation(success=False,
                                              error="An error occurred updating relationship")

        kwargs['initiator'] = user.id
        serializer = RelationshipSerializer(data=kwargs)

        if not serializer.is_valid():
            return RelationshipAcceptMutation(success=False,
                                              error=str(serializer.errors),
                                              relationship=None)

        instance = serializer.save()
        return RelationshipRemoveMutation(success=True, error=None, relationship=instance)
