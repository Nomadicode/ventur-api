import graphene

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
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

    class Meta:
        model = Activity

    def resolve_media(self, info, **kwargs):
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
        exclude_fields = ('point', )


class ActivityQuery(object):
    activities = graphene.List(ActivityType, latitude=graphene.Float(), longitude=graphene.Float())
    categories = graphene.List(CategoryType)
    random_activity = graphene.Field(ActivityType, latitude=graphene.Float(), longitude=graphene.Float())

    def resolve_activities(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return None

        location = GEOSGeometry('POINT(%s %s)' % (kwargs['longitude'], kwargs['latitude']), srid=4326)

        return Activity.objects.filter(location__point__distance_lte=(location, D(mi=10)))

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_random_activity(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return None

        if 'longitude' not in kwargs or 'latitude' not in kwargs:
            return None

        location = GEOSGeometry('POINT(%s %s)' % (kwargs['longitude'], kwargs['latitude']), srid=4326)

        activity = Activity.objects.filter(location__point__distance_lte=(location, D(mi=10))).order_by('?').first()

        return activity
