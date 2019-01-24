import graphene
from django.db import IntegrityError
from api.helpers import get_user_from_info

from .models import AcceptedActivity, RejectedActivity, SavedActivity
from .serializers import AcceptedActivitySerializer, RejectedActivitySerializer, SavedActivitySerializer
from .schema import AcceptedActivityType, RejectedActivityType, SavedActivityType


class AcceptActivityMutation(graphene.Mutation):
    class Arguments:
        activity = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    activity = graphene.Field(AcceptedActivityType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return AcceptActivityMutation(success=False, error="You must be signed in to modify preferences.",
                                          activity=None)

        kwargs['user'] = user.id

        RejectedActivity.objects.filter(activity_id=kwargs['activity'], user_id=user.id).delete()

        if AcceptedActivity.objects.filter(activity_id=kwargs['activity'], user_id=user.id).exists():
            return AcceptActivityMutation(success=False, error="You have already accepted this activity.", activity=None)

        serializer = AcceptedActivitySerializer(data=kwargs)

        if not serializer.is_valid():
            return AcceptActivityMutation(success=False, error=str(serializer.errors), activity=None)

        instance = serializer.save()

        return AcceptActivityMutation(success=True, error=None, activity=instance)


class RejectActivityMutation(graphene.Mutation):
    class Arguments:
        activity = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    activity = graphene.Field(RejectedActivityType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return RejectActivityMutation(success=False, error="You must be signed in to modify preferences.",
                                          activity=None)

        kwargs['user'] = user.id

        AcceptedActivity.objects.filter(activity_id=kwargs['activity'], user_id=user.id).delete()

        if RejectedActivity.objects.filter(activity_id=kwargs['activity'], user_id=user.id).exists():
            return RejectActivityMutation(success=False, error="You have already rejected this activity.", activity=None)

        serializer = RejectedActivitySerializer(data=kwargs)

        if not serializer.is_valid():
            return RejectActivityMutation(success=False, error=str(serializer.errors), activity=None)

        instance = serializer.save()

        return RejectActivityMutation(success=True, error=None, activity=instance)


class SaveActivityMutation(graphene.Mutation):
    class Arguments:
        activity = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    activity = graphene.Field(SavedActivityType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return SaveActivityMutation(success=False, error="You must be signed in to save activities.",
                                        activity=None)

        kwargs['user'] = user.id

        saved_filter = SavedActivity.objects.filter(activity_id=kwargs['activity'], user_id=user.id)

        if saved_filter.exists():
            return SaveActivityMutation(success=True, error="You have already saved this activity.",
                                        activity=saved_filter.first())

        serializer = SavedActivitySerializer(data=kwargs)

        if not serializer.is_valid():
            return SaveActivityMutation(success=False, error=str(serializer.errors), activity=None)

        instance = serializer.save()

        return SaveActivityMutation(success=True, error=None, activity=instance)


class UnsaveActivityMutation(graphene.Mutation):
    class Arguments:
        activity = graphene.Int(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return UnsaveActivityMutation(success=False, error="You must be signed in to modify saved activities.")

        kwargs['user'] = user.id

        try:
            saved_activity = SavedActivity.objects.get(activity_id=kwargs['activity'], user_id=user.id)
        except SavedActivity.DoesNotExist:
            return UnsaveActivityMutation(success=False, error="An error occurred fetching specified activity")

        try:
            saved_activity.delete()
        except IntegrityError:
            return UnsaveActivityMutation(success=False, error="An error occurred trying to remove saved activity")

        return UnsaveActivityMutation(success=True, error=None)
