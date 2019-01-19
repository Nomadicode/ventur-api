from datetime import date, datetime, timedelta
import pytz
import graphene

from api.helpers import get_user_from_info, base64_to_file

from .models import User
from .serializers import UserDetailsSerializer
from .schema import UserType


class UserUpdateMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=False)
        email = graphene.String(required=False)
        date_of_birth = graphene.String(required=False)
        profile_picture = graphene.String(required=False)

    success = graphene.Boolean()
    error = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return UserUpdateMutation(success=False, error="You must be logged in to edit your account.",
                                      user=None)
        
        if 'profile_picture' in kwargs.keys():
            kwargs['profile_picture'] = base64_to_file(kwargs['profile_picture'])
        
        serializer = UserDetailsSerializer(user, data=kwargs, partial=True)

        if not serializer.is_valid():
            return UserUpdateMutation(success=False, error=str(serializer.errors), user=None)

        instance = serializer.save()
        return UserUpdateMutation(success=True, error=None, user=instance)


class UserPhotoMutation(graphene.Mutation):
    class Arguments:
        media = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    profile = graphene.Field(UserType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return UserPhotoMutation(success=False, error="You must be logged in to edit your profile.",
                                     profile=None)

        kwargs['profile_picture'] = base64_to_file(kwargs['media'])

        serializer = UserDetailsSerializer(user, data=kwargs, partial=True)

        if not serializer.is_valid():
            return UserPhotoMutation(success=False, error=str(serializer.errors), profile=None)

        instance = serializer.save()

        return UserPhotoMutation(success=True, error=None, profile=instance)
