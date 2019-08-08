import graphene

from django.conf import settings
from api.helpers import get_user_from_info

from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django import DjangoConnectionField

from .models import User, UserSettings, UserDevice, AccountDeleteRequest

class AccountDeleteRequestType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = AccountDeleteRequest

class UserSettingsType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = UserSettings


class UserDeviceType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = UserDevice


class UserType(DjangoObjectType):
    pk = graphene.Int()
    settings = graphene.Field(UserSettingsType)

    class Meta:
        model = User
        exclude_fields = ('password',)

    def resolve_settings(self, info, **kwargs):
        user = get_user_from_info(info)
        if not user.is_authenticated:
            return None

        if user.id != self.id:
            return None

        return self.settings.first()


class UserConnection(relay.Connection):
    class Meta:
        node = UserType


class UserQuery(graphene.AbstractType):
    users = relay.ConnectionField(UserConnection, fetch_all=graphene.Boolean(), query=graphene.String())
    user = graphene.Field(UserType, jwt=graphene.String(), pk=graphene.ID())

    def resolve_users(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            raise Exception('Authentication Error')

        users = User.objects.all()

        if 'fetch_all' not in kwargs or not kwargs['fetch_all'] or not user.is_staff:
            users = users.filter(is_active=True, is_system=False)

        if 'query' in kwargs:
            users = users.filter(handle__icontains=kwargs['query'])

        return users

    def resolve_user(self, info, **kwargs):
        if 'pk' in kwargs: 
            return User.objects.get(pk=kwargs['pk'])
        
        jwt = info.context.META.get('HTTP_AUTHORIZATION', None)
        if jwt:
            jwt = jwt.split(' ')[-1]
            return User.decode_jwt(jwt)

        return User.decode_jwt(kwargs.get('jwt', ''))
