import graphene

from graphene_django.types import DjangoObjectType

from .models import Category, Activity


class CategoryType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Category


class ActivityType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Activity


class ActivityQuery(object):
    activities = graphene.List(ActivityType)
    categories = graphene.List(CategoryType)

    def resolve_activities(self, info, **kwargs):
        return Activity.objects.all()

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()
