from datetime import date, datetime, timedelta
import pytz
import graphene

from api.helpers import get_user_from_info

from .serializers import FeedbackSerializer
from .schema import FeedbackType


class FeedbackAddMutation(graphene.Mutation):
    class Arguments:
        subject = graphene.String(required=True)
        category = graphene.Int(required=True)
        details = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    feedback = graphene.Field(FeedbackType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return FeedbackAddMutation(success=False, error="Please sign in to submit feedback.",
                                       feedback=None)

        kwargs['user'] = user.id

        serializer = FeedbackSerializer(data=kwargs)

        if not serializer.is_valid():
            return FeedbackAddMutation(success=False, error=str(serializer.errors), feedback=None)

        instance = serializer.save()

        return FeedbackAddMutation(success=True, error=None, feedback=instance)
