import graphene

from graphene_django.types import DjangoObjectType
from api.helpers import get_user_from_info

from .models import Category, Activity, Location, Schedule, Report, RepeatOptions, ReportOptions


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


class RepeatOptionsType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = RepeatOptions


class ReportOptionsType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = ReportOptions


class ScheduleType(DjangoObjectType):
    pk = graphene.Int()
    repeat = graphene.String()

    class Meta:
        model = Schedule

    def resolve_repeat(self, info, **kwargs):
        return self.repeat.name


class ReportType(DjangoObjectType):
    pk = graphene.Int()
    reason = graphene.String()

    class Meta:
        model = Report

    def resolve(self, info, **kwargs):
        return self.reason.name


class ActivityQuery(object):
    activities = graphene.List(ActivityType)
    categories = graphene.List(CategoryType)
    random_activity = graphene.Field(ActivityType, latitude=graphene.Float(), longitude=graphene.Float())

    report_reasons = graphene.List(ReportOptionsType)
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

        return Activity.objects.order_by('?')[0]

    def resolve_repeat_intervals(self, info, **kwargs):
        return RepeatOptions.objects.all()

    def resolve_report_reasons(self, info, **kwargs):
        return ReportOptions.objects.all().order_by('name')

