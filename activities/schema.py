import graphene

from graphene_django.types import DjangoObjectType
from api.helpers import get_user_from_info

from .models import Category, Activity, Location, Schedule


class CategoryType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Category


class ActivityType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Activity


class LocationType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Location


class ScheduleType(DjangoObjectType):
    pk = graphene.Int()
    repeat = graphene.String()

    class Meta:
        model = Schedule

    def resolve_repeat(self, info, **kwargs):
        return self.get_repeat_display()


class ActivityQuery(object):
    activities = graphene.List(ActivityType)
    categories = graphene.List(CategoryType)
    random_activity = graphene.Field(ActivityType, latitude=graphene.Float(), longitude=graphene.Float())

    def resolve_activities(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return None

        return Activity.objects.all()

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_random_activity(self, info, **kwargs):
        return Activity.objects.first()

