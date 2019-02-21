import graphene

from graphene_django.types import DjangoObjectType
from api.helpers import get_user_from_info

from .models import Category, Activity, Location, Schedule, RepeatOptions


class CategoryType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Category


class ActivityType(DjangoObjectType):
    pk = graphene.Int()
    recurrence = graphene.List(graphene.DateTime, start=graphene.DateTime(), end=graphene.DateTime())
    media = graphene.String()

    class Meta:
        model = Activity

    def resolve_profile_picture(self, info, **kwargs):
        if self.media:
            return self.media.url
        return None

    def resolve_recurrence(self, info, **kwargs):
        if hasattr(self, 'recurrence') and self.recurrence:
            return self.recurrence.occurrences()

        return None


class LocationType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Location


class RepeatOptionsType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = RepeatOptions


class ScheduleType(DjangoObjectType):
    pk = graphene.Int()
    repeat = graphene.String()

    class Meta:
        model = Schedule

    def resolve_repeat(self, info, **kwargs):
        return self.repeat.name


class ActivityQuery(object):
    activities = graphene.List(ActivityType)
    categories = graphene.List(CategoryType)
    random_activity = graphene.Field(ActivityType, latitude=graphene.Float(), longitude=graphene.Float())
    repeat_intervals = graphene.List(RepeatOptionsType)

    def resolve_activities(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return None

        return Activity.objects.all()

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_random_activity(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return None

        return Activity.objects.order_by('?').first()

    def resolve_repeat_intervals(self, info, **kwargs):
        return RepeatOptions.objects.all()
