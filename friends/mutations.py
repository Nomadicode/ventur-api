import graphene

from api.helpers import get_user_from_info, base64_to_file

from .serializers import GroupSerializer
from .schema import GroupType


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
