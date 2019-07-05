from datetime import datetime, timedelta
from dateutil import parser
import graphene
import recurrence

from django.contrib.gis.geos import GEOSGeometry
from django.db import IntegrityError
from api.helpers import get_user_from_info, get_address_from_latlng, get_latlng_from_address, base64_to_file, \
                        sanitize_category

from friends.models import Group

from .models import Activity, Category, Location, Schedule, REPEAT_CHOICES
from .serializers import ActivitySerializer
from .schema import ActivityType


class ActivityAddMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        media = graphene.String(required=False)
        description = graphene.String(required=False)
        categories = graphene.String(required=False)
        duration = graphene.Int(required=False)
        price = graphene.Float(required=False)
        minimum_age = graphene.Int(required=False)
        maximum_age = graphene.Int(required=False)
        handicap_friendly = graphene.Boolean(required=False)
        is_nsfw = graphene.Boolean(required=False)
        alcohol_present = graphene.Boolean(required=False)
        address = graphene.String(required=False)
        latitude = graphene.Float(required=False)
        longitude = graphene.Float(required=False)
        start_datetime = graphene.String(required=False)
        end_datetime = graphene.String(required=False)
        frequency = graphene.Int(required=False)
        groups = graphene.String(required=False)

    success = graphene.Boolean()
    error = graphene.String()
    activity = graphene.Field(ActivityType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return ActivityAddMutation(success=False, error="You must be logged in to add an activity.",
                                       activity=None)

        kwargs['created_by'] = user.id

        if 'categories' in kwargs:
            categories = kwargs['categories'].split(',')

            category_arr = []
            for category_name in categories:
                # validate category name
                category_name = sanitize_category(category_name)
                category, created = Category.objects.get_or_create(name=category_name)
                category_arr.append(category.id)

            kwargs['categories'] = category_arr

        if 'media' in kwargs:
            kwargs['media'] = base64_to_file(kwargs['media'])

        # region Set up schedule
        if ('start_datetime' in kwargs and kwargs['start_datetime']) or ('end_datetime' in kwargs and kwargs['end_datetime']):
            schedule = Schedule(
                start=parser.parse(kwargs['start_datetime']),
                end=parser.parse(kwargs['end_datetime'])
            )

            if 'frequency' in kwargs and kwargs['frequency'] > -1:
                frequency = REPEAT_CHOICES[kwargs['frequency']] if kwargs['frequency'] < 4 else None

                if frequency:
                    schedule.repeat = 'RRULE:FREQ=' + frequency
        # endregion

        # region Set up location
        location_data = {
            'address': kwargs['address'] if 'address' in kwargs else None,
            'latitude': kwargs['latitude'] if 'latitude' in kwargs else None,
            'longitude': kwargs['longitude'] if 'longitude' in kwargs else None,
            'point': None
        }

        if 'latitude' in kwargs and 'longitude' in kwargs:
            location_data['address'] = get_address_from_latlng(kwargs['latitude'], kwargs['longitude'])
        elif 'address' in kwargs:
            location_data['latitude'], location_data['longitude'] = get_latlng_from_address(location_str=kwargs['address'])

        location_data['point'] = GEOSGeometry('POINT(%s %s)' % (location_data['longitude'], location_data['latitude']), srid=4326)

        try:
            location = Location.objects.create(**location_data)
        except IntegrityError:
            return ActivityAddMutation(success=False, error="An error occurred while saving the activity's location", activity=None)

        kwargs['location'] = location.id
        # endregion

        if 'groups' in kwargs:
            groups = kwargs['groups'].split(',')
            kwargs['groups'] = []

            for group_id in groups:
                if group_id.isdigit():
                    kwargs['groups'].append(int(group_id))

        serializer = ActivitySerializer(data=kwargs)

        if not serializer.is_valid():
            return ActivityAddMutation(success=False, error=str(serializer.errors), activity=None)

        instance = serializer.save()
        schedule.event = instance
        schedule.save()
        # instance.recurrence = schedule
        # instance.save()

        return ActivityAddMutation(success=True, error=None, activity=instance)


class ActivityUpdateMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        name = graphene.String(required=True)
        media = graphene.String(required=False)
        description = graphene.String(required=False)
        categories = graphene.String(required=False)
        duration = graphene.Int(required=False)
        price = graphene.Float(required=False)
        kid_friendly = graphene.Boolean(required=False)
        handicap_friendly = graphene.Boolean(required=False)
        over_18 = graphene.Boolean(required=False)
        over_21 = graphene.Boolean(required=False)
        address = graphene.String(required=False)
        latitude = graphene.Float(required=False)
        longitude = graphene.Float(required=False)
        start_datetime = graphene.DateTime(required=False)
        end_datetime = graphene.DateTime(required=False)
        frequency = graphene.Int(required=False)
        interval = graphene.Int(required=False)
        days = graphene.String(required=False)

    success = graphene.Boolean()
    error = graphene.String()
    activity = graphene.Field(ActivityType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return ActivityUpdateMutation(success=False, error="You must be logged in to edit an activity.",
                                          activity=None)

        try:
            activity = Activity.objects.get(pk=kwargs['pk'])
        except Activity.DoesNotExist:
            return ActivityUpdateMutation(success=False, error="Unable to find requested activity", activity=None)

        if activity.created_by.id != user.id:
            return ActivityUpdateMutation(success=False, error="You are not authorized to update this activity.",
                                          activity=None)

        pass


class ActivityDeleteMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return ActivityDeleteMutation(success=False, error="You must be logged in to delete an activity")

        try:
            activity = Activity.objects.get(id=kwargs['pk'], created_by__id=user.id)
        except Activity.DoesNotExist:
            return ActivityDeleteMutation(success=False, error="Unable to delete activity")

        try:
            activity.delete()
        except IntegrityError:
            return ActivityDeleteMutation(success=False, error="An error occurred attempting to delete the activity")

        return ActivityDeleteMutation(success=True, error=None)
