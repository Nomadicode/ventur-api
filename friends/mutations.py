import graphene

from api.helpers import get_user_from_info, base64_to_file

from users.models import User

from friendship.models import Friend, FriendshipRequest, Block
from friends.models import Group

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


class FriendGroupUpdateMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)
        name = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    group = graphene.Field(GroupType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return FriendGroupUpdateMutation(success=False,
                                             error="You must be logged in to rename a group.",
                                             group=None)

        group = None
        try:
            group = Group.objects.get(creator=user, id=kwargs['pk'])
        except Group.DoesNotExist:
            return FriendGroupUpdateMutation(success=False,
                                             error="Only the group's creator can rename a group.",
                                             group=None)

        serializer = GroupSerializer(group, data=kwargs, partial=True)

        if not serializer.is_valid():
            return FriendGroupUpdateMutation(success=False, error=str(serializer.errors), group=None)

        instance = serializer.save()
        return FriendGroupUpdateMutation(success=True, error=None, group=instance)


class FriendGroupRemoveMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return FriendGroupRemoveMutation(success=False,
                                             error="You must be logged in to remove a group.")

        try:
            group = Group.objects.get(creator=user, id=kwargs['pk'])
        except Group.DoesNotExist:
            return FriendGroupRemoveMutation(success=False,
                                             error="Only the group's creator can delete a group.")

        group.delete()

        return FriendGroupRemoveMutation(success=True, error=None)


class FriendGroupAddMemberMutation(graphene.Mutation):
    class Arguments:
        group_id = graphene.Int(required=True)
        member_id = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    group = graphene.Field(GroupType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return FriendGroupAddMemberMutation(success=False,
                                             error="You must be logged in to add a member to a group.")

        try:
            group = Group.objects.get(creator=user, id=kwargs['group_id'])
        except Group.DoesNotExist:
            return FriendGroupAddMemberMutation(success=False,
                                             error="Only the group's creator can add members a group.")

        try:
            member = User.objects.get(id=kwargs['member_id'])
        except User.DoesNotExist:
            return FriendGroupAddMemberMutation(success=False,
                                                error="Unable to find the requested user.")

        group.friends.add(member)

        return FriendGroupAddMemberMutation(success=True, error=None, group=group)


class FriendGroupRemoveMemberMutation(graphene.Mutation):
    class Arguments:
        group_id = graphene.Int(required=True)
        member_id = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    group = graphene.Field(GroupType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return FriendGroupRemoveMemberMutation(success=False,
                                             error="You must be logged in to remove a member from a group.")

        try:
            group = Group.objects.get(creator=user, id=kwargs['group_id'])
        except Group.DoesNotExist:
            return FriendGroupRemoveMemberMutation(success=False,
                                             error="Only the group's creator can remove members from a group.")

        try:
            member = User.objects.get(id=kwargs['member_id'])
        except User.DoesNotExist:
            return FriendGroupRemoveMemberMutation(success=False,
                                                error="Unable to find the requested user.")

        group.friends.remove(member)

        return FriendGroupRemoveMemberMutation(success=True, error=None, group=group)


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
                                                   friend_request=None)
        other_user = None
        try:
            other_user = User.objects.get(handle=kwargs['handle'])
        except User.DoesNotExist:
            return FriendshipRequestAcceptMutation(success=False,
                                                   error="Unable to find user with handle %s".format(kwargs['handle']),
                                                   friend_request=None)

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
                                                   error="You must be logged in to reject a friend request.",
                                                   friend_request=None)
        other_user = None
        try:
            other_user = User.objects.get(handle=kwargs['handle'])
        except User.DoesNotExist:
            return FriendshipRequestRejectMutation(success=False,
                                                   error="Unable to find user with handle %s".format(kwargs['handle']),
                                                   friend_request=None)

        friend_request = FriendshipRequest.objects.get(to_user=user, from_user=other_user)
        friend_request.reject()

        return FriendshipRequestRejectMutation(success=True, error=None, friend_request=friend_request)


class FriendshipRequestCancelMutation(graphene.Mutation):
    class Arguments:
        handle = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return FriendshipRequestCancelMutation(success=False,
                                                   error="You must be logged in to cancel a friend request.")
        other_user = None
        try:
            other_user = User.objects.get(handle=kwargs['handle'])
        except User.DoesNotExist:
            return FriendshipRequestCancelMutation(success=False,
                                                   error="Unable to find user with handle %s".format(kwargs['handle']))

        friend_request = FriendshipRequest.objects.get(to_user=other_user, from_user=user)
        friend_request.cancel()

        return FriendshipRequestCancelMutation(success=True, error=None)


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
