from datetime import date, datetime, timedelta
import pytz
import json
import graphene

from api.helpers import get_user_from_info, base64_to_file

from .models import Activity, Category
from .serializers import ActivitySerializer
from .schema import ActivityType


class ActivityAddMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=False)
        duration = graphene.Int(required=False)
        price = graphene.Float(required=False)
        categories = graphene.String(required=False)
        age_ranges = graphene.String(required=False)
        latitude = graphene.String(required=False)
        longitude = graphene.String(required=False)
        media = graphene.String(required=False)

    success = graphene.Boolean()
    error = graphene.String()
    activity = graphene.Field(ActivityType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return ActivityAddMutation(success=False, error="You must be logged in to add an activity.",
                                        activity=None)

        kwargs['created_by'] = user.id
        
        if 'media' in kwargs:
            kwargs['media'] = base64_to_file(kwargs['media'])

        if 'categories' in kwargs:
            categories = kwargs['categories'].split(',')

            category_arr = []
            for category_name in categories:
                category, created = Category.objects.get_or_create(name=category_name)
                category_arr.append(category.id) 

            kwargs['categories'] = category_arr

        if 'age_ranges' in kwargs:
            age_ranges = kwargs['age_ranges'].split(',')

            age_arr = []
            age = age_ranges[0]
            while age < age_ranges[-1]:
                age_arr.append(age + 1)

            kwargs['age_ranges'] = age_arr

        if 'latitude' in kwargs and 'longitude' in kwargs:
            pass

        # if 'schedule' in kwargs:
        #     schedule = json.loads(kwargs['schedule'])

        
        serializer = ActivitySerializer(data=kwargs)

        if not serializer.is_valid():
            return ActivityAddMutation(success=False, error=str(serializer.errors), activity=None)

        instance = serializer.save()
        return ActivityAddMutation(success=True, error=None, activity=instance)