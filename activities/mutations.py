from datetime import date, datetime, timedelta
import pytz
import json
import graphene

from django.db import IntegrityError
from api.helpers import get_user_from_info, base64_to_file, get_address_from_latlng, get_latlng_from_address, sanitize_category

from .models import Activity, Category, Location, Schedule
from .serializers import ActivitySerializer
from .schema import ActivityType


class ActivityAddMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=False)
        categories = graphene.String(required=True)
        duration = graphene.Int(required=False)
        price = graphene.Float(required=False)
        kid_friendly = graphene.Boolean(required=False)
        handicap_friendly = graphene.Boolean(required=False)
        over_18 = graphene.Boolean(required=False)
        over_21 = graphene.Boolean(required=False)
        address = graphene.String(required=False)
        latitude = graphene.Float(required=False)
        longitude = graphene.Float(required=False)
        start_date = graphene.Date(required=False)
        start_time = graphene.Time(required=False)
        end_date = graphene.Date(required=False)
        end_time = graphene.Time(required=False)
        repeat = graphene.Int(required=False)

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

        if ('over_18' in kwargs and kwargs['over_18']) or ('over_21' in kwargs and kwargs['over_21']):
            kwargs['kid_friendly'] = False

        # Set up schedule
        if 'start_date' in kwargs or 'start_time' in kwargs or 'end_date' in kwargs or 'end_time' in kwargs or 'repeat' in kwargs:
            start_dt = kwargs['start_date'] if 'start_date' in kwargs else datetime.now()
            start_tm = kwargs['start_time'] if 'start_time' in kwargs else datetime.now()

            end_dt = kwargs['end_date'] if 'end_date' in kwargs else None
            end_tm = kwargs['end_time'] if 'end_time' in kwargs else None

            repeat = kwargs['repeat'] if 'repeat' in kwargs else 1

            # Check that end date is after start date
            schedule_data = {
                "start_date": datetime.strftime(start_dt, '%Y-%m-%d'),
                "start_time": start_tm,
                "end_date": datetime.strftime(end_dt, '%Y-%m-%d') if end_dt else None,
                "end_time": end_tm,
                "repeat_id": repeat
            }

            # validate that it succeeds
            try:
                schedule = Schedule.objects.create(**schedule_data)
            except IntegrityError:
                return ActivityAddMutation(success=False, errors="An error occurred while saving the schedule,", activity=None)

            kwargs['schedule'] = schedule.id

        # Set up location
        location_data = {
            'address': kwargs['address'] if 'address' in kwargs else None,
            'latitude': kwargs['latitude'] if 'latitude' in kwargs else None,
            'longitude': kwargs['longitude'] if 'longitude' in kwargs else None
        }

        if 'latitude' in kwargs and 'longitude' in kwargs:
            location_data['address'] = get_address_from_latlng(kwargs['latitude'], kwargs['longitude'])
        elif 'address' in kwargs:
            location_data['latitude'], location_data['longitude'] = get_latlng_from_address(location_str=kwargs['address'])

        try:
            location = Location.objects.create(**location_data)
        except IntegrityError:
            return ActivityAddMutation(success=False, error="An error occurred while saving the activity's location", activity=None)

        kwargs['location'] = location.id

        serializer = ActivitySerializer(data=kwargs)

        if not serializer.is_valid():
            return ActivityAddMutation(success=False, error=str(serializer.errors), activity=None)

        instance = serializer.save()
        return ActivityAddMutation(success=True, error=None, activity=instance)


class ActivityUpdateMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)
        name = graphene.String(required=False)
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
        start_date = graphene.Date(required=False)
        start_time = graphene.Time(required=False)
        end_date = graphene.Date(required=False)
        end_time = graphene.Time(required=False)
        repeat = graphene.String(required=False)

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
        pk = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return ActivityDeleteMutation(success=False, error="You must be logged in to delete an activity")

        try:
            activity = Activity.objects.get(id=kwargs['pk'], created_by__id=user.id)
        except Activity.DoesNotExist:
            return ActivityDeleteMutation(success=False, error="Unable to find activity")

        try:
            activity.delete()
        except IntegrityError:
            return ActivityDeleteMutation(success=False, error="An error occurred attempting to delete the activity")

        return ActivityDeleteMutation(success=True, error=None)


class ActivitySaveMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    activity = graphene.Field(ActivityType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return ActivitySaveMutation(success=False, error="You must be logged in to save an activity.",
                                        activity=None)

        pass


class ActivityUnsaveMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    activity = graphene.Field(ActivityType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return ActivityUnsaveMutation(success=False, error="You must be logged in to unsave an activity.",
                                          activity=None)

        pass
