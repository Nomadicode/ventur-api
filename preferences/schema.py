import graphene

from graphene_django.types import DjangoObjectType
from api.helpers import get_user_from_info

from .models import AcceptedActivity, RejectedActivity, SavedActivity


class AcceptedActivityType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = AcceptedActivity


class RejectedActivityType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = RejectedActivity


class SavedActivityType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = SavedActivity


class PreferenceQuery(graphene.AbstractType):
    accepted_activities = graphene.List(AcceptedActivityType)
    rejected_activities = graphene.List(RejectedActivityType)
    saved_activities = graphene.List(SavedActivityType)

    def resolve_accepted_activities(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return None

        return AcceptedActivity.objects.filter(user_id=user.id)

    def resolve_rejected_activities(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return None

        return RejectedActivity.objects.filter(user_id=user.id)

    def resolve_saved_activities(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return None

        return SavedActivity.objects.filter(user_id=user.id)
