import graphene
import json
import pytz
from dateutil import parser
from datetime import datetime, timedelta

from django.utils import timezone
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.db.models import Count
from graphene_django.types import DjangoObjectType
from api.helpers import get_user_from_info, get_distance

from .models import Category, Activity, Location, Schedule


class ScheduleType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Schedule

class CategoryType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Category


class ActivityType(DjangoObjectType):
    pk = graphene.ID()
    next_occurrence = graphene.DateTime()
    distance = graphene.String()
    media = graphene.String()
    saved = graphene.Boolean()

    class Meta:
        model = Activity

    def resolve_media(self, info, **kwargs):
        if self.media:
            return settings.SITE_DOMAIN + self.media.url
        return None

    def resolve_next_occurrence(self, info, **kwargs):
        next_occurrence = self.next_occurrence()

        if next_occurrence:
            return next_occurrence[0]

        return None

    def resolve_distance(self, info, **kwargs):
        user = get_user_from_info(info)

        if user.is_authenticated:
            if user.location:
                destination = "{} {}".format(self.location.latitude, self.location.longitude)
                return get_distance(user.location, destination)

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
    activity = graphene.Field(ActivityType, pk=graphene.ID(required=True))
    activities = graphene.List(ActivityType, latitude=graphene.Float(), longitude=graphene.Float(), saved=graphene.Boolean(),
                               filters=graphene.String(), page=graphene.Int(), created_by=graphene.ID())
    categories = graphene.List(CategoryType)
    random_activity = graphene.Field(ActivityType, latitude=graphene.Float(), longitude=graphene.Float(),
                                     radius=graphene.Int(), price=graphene.Int())


    def resolve_activity(self, info, **kwargs):
        activity = Activity.objects.get(id=kwargs['pk'])

        return activity

    def resolve_activities(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            raise Exception('Authentication Error')

        activities = Activity.objects.all()

        if 'created_by' in kwargs and kwargs['created_by']:
            activities = activities.filter(created_by__id=kwargs['created_by'])
        else:
            if 'saved' in kwargs and kwargs['saved']:
                activities = activities.filter(saved_activities__user__id=user.id)

            # Remove if restricted to a group user is not a member of

            # Refine to my location
            location = GEOSGeometry('POINT(%s %s)' % (kwargs['longitude'], kwargs['latitude']), srid=4326)
            distance = settings.DEFAULT_RADIUS
            if 'filters' in kwargs:
                filters = json.loads(kwargs['filters'].replace("\'", "\"").replace('None', 'null'))

                if 'radius' in filters and filters['radius']:
                    distance = filters['radius']

            activities = activities.filter(location__point__distance_lte=(location, D(mi=distance)))

            # Remove activities with > 3 reports
            activities = activities.annotate(report_count=Count('reports')).filter(report_count__lt=3)

            # Remove activities reported by requesting user
            activities = activities.exclude(reports__reporter__id=user.id)

            # Handle User Preferences
            user_settings = user.settings.first()

            if user_settings:
                if user_settings.handicap_only:
                    activities = activities.filter(handicap_friendly=True)

                if not user_settings.show_nsfw:
                    activities = activities.filter(is_nsfw=False)

                if not user_settings.show_alcohol:
                    activities = activities.filter(alcohol_present=False)

            # Handle filters
            if 'filters' in kwargs:
                filters = json.loads(kwargs['filters'].replace("\'","\"").replace('None', 'null'))

                if 'startDate' in filters and 'endDate' in filters:
                    start_date = parser.parse(filters['startDate'])
                    end_date = parser.parse(filters['endDate'])

                    activities = activities.for_period(from_date=start_date, to_date=end_date)

                if 'price' in filters and filters['price']:
                    activities = activities.filter(price__lte=filters['price'])

                if 'duration' in filters and filters['duration']:
                    activities = activities.filter(duration__lte=filters['duration'])
        #
        # activities = activities.sort_by_next()

        page_size = 10
        start = 0
        end = page_size

        if 'page' in kwargs:
            start = (kwargs['page'] - 1) * page_size
            end = start + page_size

        return activities[start:end]

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_random_activity(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            raise Exception('Authentication Error')

        if 'longitude' not in kwargs or 'latitude' not in kwargs:
            raise Exception('Missing Parameters')

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
        # start_date = datetime.now()
        # end_date = datetime.now().replace(hour=23, minute=59, second=59)
        # activity = activity.for_period(from_date=start_date, to_date=end_date, exact=True)

        activity = activity.order_by('?').first()

        return activity
