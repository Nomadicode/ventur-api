import graphene

from api.helpers import get_user_from_info, base64_to_file

from django.db import IntegrityError

from allauth.account.models import EmailAddress
from api.enums import Errors
from .models import AccountDeleteRequest, UserSettings, UserDevice
from .serializers import UserDetailsSerializer, UserSettingsSerializer
from .schema import UserType, UserSettingsType, UserDeviceType


class UserUpdateMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=False)
        email = graphene.String(required=False)
        date_of_birth = graphene.Date(required=False)
        profile_picture = graphene.String(required=False)
        handle = graphene.String(required=False)
        timezone = graphene.String(required=False)
        latitude = graphene.Float(required=False)
        longitude = graphene.Float(required=False)

    success = graphene.Boolean()
    error = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return UserUpdateMutation(success=False, error="You must be logged in to edit your account.",
                                      user=None)

        if 'email' in kwargs:
            address = EmailAddress.objects.get_for_user(user, user.email)
            address.email = kwargs['email']
            address.save()
        
        serializer = UserDetailsSerializer(user, data=kwargs, partial=True)

        if not serializer.is_valid():
            return UserUpdateMutation(success=False, error=str(serializer.errors), user=None)

        instance = serializer.save()
        return UserUpdateMutation(success=True, error=None, user=instance)


class UserSettingsUpdateMutation(graphene.Mutation):
    class Arguments:
        show_alcohol = graphene.Boolean(required=False)
        show_nsfw = graphene.Boolean(required=False)
        handicap_only = graphene.Boolean(required=False)
        new_friend_event_notification = graphene.Boolean(required=False)
        upcoming_saved_event_notification = graphene.Boolean(required=False)

    success = graphene.Boolean()
    error = graphene.String()
    user_settings = graphene.Field(UserSettingsType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return UserSettingsUpdateMutation(success=False, error=Errors.AUTH,
                                      user_settings=None)

        settings = user.settings.first()

        if not settings:
            settings = UserSettings.objects.create(user=user)

        serializer = UserSettingsSerializer(settings, data=kwargs, partial=True)

        if not serializer.is_valid():
            return UserSettingsUpdateMutation(success=False, error=str(serializer.errors), user_settings=None)

        instance = serializer.save()
        return UserSettingsUpdateMutation(success=True, error=None, user_settings=instance)


class RequestAccountDelete(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return RequestAccountDelete(success=False, error=Errors.AUTH)

        AccountDeleteRequest.objects.create(user=user)

        return RequestAccountDelete(success=True, error=None)


class UserDeviceAddMutation(graphene.Mutation):
    class Arguments:
        device_id = graphene.String(required=True)
        device_type = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    user_device = graphene.Field(UserDeviceType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return UserDeviceAdd(success=False, error=Errors.AUTH)

        user_device = UserDevice.objects.create(user=user,
                                                device_id=kwargs['device_id'],
                                                device_type=kwargs['device_type'])

        return UserDeviceAdd(success=True, error=None, user_device=user_device)