import graphene

from graphene_django.types import DjangoObjectType
from graphene_django import DjangoConnectionField

from .models import User


class UserType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = User
        exclude_fields = ('password', )


class UserQuery(graphene.AbstractType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, jwt=graphene.String(), pk=graphene.Int())

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        if 'pk' in kwargs: 
            return User.objects.get(pk=kwargs['pk'])
        
        jwt = info.context.META.get('HTTP_AUTHORIZATION', None)
        if jwt:
            jwt = jwt.split(' ')[-1]
            return User.decode_jwt(jwt)

        return User.decode_jwt(kwargs.get('jwt', ''))