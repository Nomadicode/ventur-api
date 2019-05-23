import graphene
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.db.models import Count
from graphene_django.types import DjangoObjectType
from api.helpers import get_user_from_info

from .models import Category, Activity, Location


class CategoryType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Category


class ActivityType(DjangoObjectType):
    pk = graphene.Int()
    recurrence = graphene.List(graphene.DateTime, start=graphene.DateTime(), end=graphene.DateTime())
    media = graphene.String()
    saved = graphene.Boolean()

    class Meta:
        model = Activity

    def resolve_media(self, info, **kwargs):
        if self.media:
            return 'http://127.0.0.1:8000' + self.media.url
        return None

    def resolve_recurrence(self, info, **kwargs):
        if hasattr(self, 'recurrence') and self.recurrence:
            return self.recurrence.occurrences()

        return None

    def resolve_saved(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return False

        return user.saved_activities.filter(activity_id=self.id).exists()

    def resolve_reported(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return False

        return user.reported_activities.filter(activity_id=self.id).exists()


class LocationType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Location
        exclude_fields = ('point', )


class ActivityQuery(object):
    activities = graphene.List(ActivityType, latitude=graphene.Float(), longitude=graphene.Float(), saved=graphene.Boolean(),
                               radius=graphene.Int(), start_date=graphene.DateTime(), end_date=graphene.DateTime(),
                               upcoming=graphene.Boolean())
    categories = graphene.List(CategoryType)
    random_activity = graphene.Field(ActivityType, latitude=graphene.Float(), longitude=graphene.Float(),
                                     radius=graphene.Int(), price=graphene.Int())

    def resolve_activities(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return None

        location = GEOSGeometry('POINT(%s %s)' % (kwargs['longitude'], kwargs['latitude']), srid=4326)
        distance = kwargs['radius'] if 'radius' in kwargs else settings.DEFAULT_RADIUS

        if 'saved' in kwargs and kwargs['saved']:
            activities = Activity.objects.filter(saved_activities__user__id=user.id)

            # Refine to upcoming
            if 'start_date' in kwargs:
                start_date = kwargs['start_date']
                excluded_activities = []
                for activity in activities:
                    if getattr(activity, 'recurrence'):
                        recurrences = activity.recurrence.after(start_date, inc=True)

                        if not recurrences:
                            excluded_activities.append(activity.id)

                activities = activities.exclude(id__in=excluded_activities)

            elif 'end_date' in kwargs:
                end_date = kwargs['end_date']
                excluded_activities = []
                for activity in activities:
                    if getattr(activity, 'recurrence'):
                        recurrences = activity.recurrence.before(end_date, inc=True)

                        if not recurrences:
                            excluded_activities.append(activity.id)

                    activities = activities.exclude(id__in=excluded_activities)
        else:
            # Refine to location
            activities = Activity.objects.filter(location__point__distance_lte=(location, D(mi=distance)))

            # Remove reported activities with > 3 reports
            activities = activities.annotate(report_count=Count('reports')).filter(report_count__lt=3)

            # Remove user reported activities
            activities = activities.exclude(reports__reporter__id=user.id)

            # Refine to available activities
            next_week = timedelta(days=7)
            start_date = kwargs['start_date'] if 'start_date' in kwargs else datetime.now()
            end_date = kwargs['end_date'] if 'end_date' in kwargs else start_date + next_week

            excluded_activities = []
            for activity in activities:
                if getattr(activity, 'recurrence'):
                    recurrences = activity.recurrence.between(start_date, end_date, inc=True)

                    if len(recurrences) == 0:
                        excluded_activities.append(activity.id)

            activities = activities.exclude(id__in=excluded_activities)

        return activities

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_random_activity(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return None

        if 'longitude' not in kwargs or 'latitude' not in kwargs:
            return None

        location = GEOSGeometry('POINT(%s %s)' % (kwargs['longitude'], kwargs['latitude']), srid=4326)
        distance = kwargs['radius'] if 'radius' in kwargs else settings.DEFAULT_RADIUS

        # Refine to location
        activity = Activity.objects.filter(location__point__distance_lte=(location, D(mi=distance)))

        # Refine by price if set

        # Remove reported activities with > 3 reports
        activity = activity.annotate(report_count=Count('reports')).filter(report_count__lt=3)

        # Remove user reported activities
        activity = activity.exclude(reports__reporter__id=user.id)

        # Narrow to upcoming today
        start_date = datetime.now()
        end_date = datetime.now().replace(hour=23, minute=59, second=59)
        excluded_activities = []
        for curr_activity in activity:
            if getattr(curr_activity, 'recurrence'):
                recurrences = curr_activity.recurrence.between(start_date, end_date, inc=True)

                if len(recurrences) == 0:
                    excluded_activities.append(curr_activity.id)

        activity = activity.exclude(id__in=excluded_activities)

        activity = activity.order_by('?').first()

        return activity
