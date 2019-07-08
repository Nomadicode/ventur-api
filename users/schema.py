import graphene

from django.conf import settings
from api.helpers import get_user_from_info

from graphene_django.types import DjangoObjectType
from graphene_django import DjangoConnectionField

from .models import User, UserSettings

class UserSettingsType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = UserSettings


class UserType(DjangoObjectType):
    pk = graphene.Int()
    profile_picture = graphene.String()
    settings = graphene.Field(UserSettingsType)

    class Meta:
        model = User
        exclude_fields = ('password',)

    def resolve_profile_picture(self, info, **kwargs):
        if self.profile_picture:
            return settings.SITE_DOMAIN + self.profile_picture.url
        return None

    def resolve_settings(self, info, **kwargs):
        user = get_user_from_info(info)
        if not user.is_authenticated:
            return None

        if user.id != self.id:
            return None

        return self.settings.first()


class UserQuery(graphene.AbstractType):
    users = graphene.List(UserType, query=graphene.String())
    user = graphene.Field(UserType, jwt=graphene.String(), pk=graphene.Int())

    def resolve_users(self, info, **kwargs):
        users = User.objects.filter(is_active=True, is_system=False)

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
