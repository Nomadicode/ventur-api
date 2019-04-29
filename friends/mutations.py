import graphene

from api.helpers import get_user_from_info, base64_to_file

from users.models import User

from friendship.models import Friend, FriendshipRequest, Block

from .serializers import GroupSerializer
from .schema import GroupType, FriendshipRequestType


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


class FriendshipRequestMutation(graphene.Mutation):
    class Arguments:
        handle = graphene.String(required=True)
        message = graphene.String(required=False)

    success = graphene.Boolean()
    error = graphene.String()
    friendship_request = graphene.Field(FriendshipRequestType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return FriendshipRequestMutation(success=False,
                                             error="You must be logged in to create a friend request.",
                                             friendship_request=None)

        other_user = None
        try:
            other_user = User.objects.get(handle=kwargs['handle'])
        except User.DoesNotExist:
            return FriendshipRequestMutation(success=False,
                                             error="Unable to find user with handle %s".format(kwargs['handle']),
                                             friendship_request=None)

        friend_request = Friend.objects.add_friend(
            user,
            other_user,
            message= kwargs['message'] if 'message' in kwargs else None
        )

        return FriendshipRequestMutation(success=True,
                                         error=None,
                                         friendship_request=friend_request)


class FriendshipRequestAcceptMutation(graphene.Mutation):
    class Arguments:
        handle = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    friend_request = graphene.Field(FriendshipRequestType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return FriendshipRequestAcceptMutation(success=False,
                                                   error="You must be logged in to accept a friend request.",
                                                   relationship=None)
        other_user = None
        try:
            other_user = User.objects.get(handle=kwargs['handle'])
        except User.DoesNotExist:
            return FriendshipRequestAcceptMutation(success=False,
                                                   error="Unable to find user with handle %s".format(kwargs['handle']),
                                                   friendship_request=None)

        friend_request = FriendshipRequest.objects.get(to_user=user, from_user=other_user)
        friend_request.accept()

        return FriendshipRequestAcceptMutation(success=True, error=None, friend_request=friend_request)


class FriendshipRequestRejectMutation(graphene.Mutation):
    class Arguments:
        handle = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    friend_request = graphene.Field(FriendshipRequestType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return FriendshipRequestRejectMutation(success=False,
                                                   error="You must be logged in to accept a friend request.",
                                                   relationship=None)
        other_user = None
        try:
            other_user = User.objects.get(handle=kwargs['handle'])
        except User.DoesNotExist:
            return FriendshipRequestRejectMutation(success=False,
                                                   error="Unable to find user with handle %s".format(kwargs['handle']),
                                                   friendship_request=None)

        friend_request = FriendshipRequest.objects.get(to_user=user, from_user=other_user)
        friend_request.reject()

        return FriendshipRequestRejectMutation(success=True, error=None, friend_request=friend_request)


class FriendshipRemoveMutation(graphene.Mutation):
    class Arguments:
        handle = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return FriendshipRemoveMutation(success=False,
                                            error="You must be logged in to remove a friend.")

        other_user = None
        try:
            other_user = User.objects.get(handle=kwargs['handle'])
        except User.DoesNotExist:
            return FriendshipRemoveMutation(success=False,
                                            error="Unable to find user with handle %s".format(kwargs['handle']))

        Friend.objects.remove_friend(
            user,
            other_user
        )

        return FriendshipRemoveMutation(success=True, error=None)


class BlockUserMutation(graphene.Mutation):
    class Arguments:
        handle = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return BlockUserMutation(success=False,
                                     error="You must be logged in to block a user.")

        other_user = None
        try:
            other_user = User.objects.get(handle=kwargs['handle'])
        except User.DoesNotExist:
            return BlockUserMutation(success=False,
                                     error="Unable to find user with handle %s".format(kwargs['handle']))

        Block.objects.add_block(
            user,
            other_user
        )

        return BlockUserMutation(success=True, error=None)


class UnblockUserMutation(graphene.Mutation):
    class Arguments:
        handle = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return UnblockUserMutation(success=False,
                                       error="You must be logged in to unblock a user.")

        other_user = None
        try:
            other_user = User.objects.get(handle=kwargs['handle'])
        except User.DoesNotExist:
            return UnblockUserMutation(success=False,
                                            error="Unable to find user with handle %s".format(kwargs['handle']))

        Block.objects.remove_block(
            user,
            other_user
        )

        return UnblockUserMutation(success=True, error=None)
