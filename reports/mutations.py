import graphene

from api.helpers import get_user_from_info

from activities.models import Activity

from .models import Report, ReportCategory
from .serializers import ReportSerializer
from .schema import ReportType


class ReportActivityMutation(graphene.Mutation):
    class Arguments:
        activity = graphene.Int(required=True)
        category = graphene.Int(required=True)
        detail = graphene.String(required=False)

    success = graphene.Boolean()
    error = graphene.String()
    report = graphene.Field(ReportType)

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return ReportActivityMutation(success=False, error="You must be logged in to report an activity.",
                                          report=None)

        kwargs['reporter'] = user.id

        if Report.objects.filter(activity_id=kwargs['activity'], reporter_id=user.id).exists():
            return ReportActivityMutation(success=False, error="You have already reported this activity.", report=None)

        try:
            activity = Activity.objects.get(id=kwargs['activity'])
        except Activity.DoesNotExist:
            return ReportActivityMutation(success=False, error="An error occurred trying to find the specified activity",
                                          report=None)

        try:
            reason = ReportCategory.objects.get(id=kwargs['category'])
        except ReportCategory.DoesNotExist:
            return ReportActivityMutation(success=False, error="The selected report category could not be found.",
                                          report=None)

        serializer = ReportSerializer(data=kwargs)

        if not serializer.is_valid():
            return ReportActivityMutation(success=False, error=str(serializer.errors), report=None)

        instance = serializer.save()
        return ReportActivityMutation(success=True, error=None, report=instance)
