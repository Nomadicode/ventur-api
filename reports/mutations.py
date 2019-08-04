import graphene

from api.helpers import get_user_from_info

from activities.models import Activity, Schedule

from .models import Report, ReportCategory
from .serializers import ReportSerializer
from .schema import ReportType


class ReportActivityMutation(graphene.Mutation):
    class Arguments:
        activity = graphene.ID(required=True)
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


class ResolveReportMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        uphold = graphene.Boolean(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return ResolveReportMutation(success=False, error="You must be logged in as an admin to resolve activities")

        if not user.is_staff:
            return ResolveReportMutation(success=False, error="Permission Error: User lacks permission to resolve")

        try:
            report = Report.objects.get(id=kwargs['id'])
        except Report.DoesNotExist:
            return ResolveReportMutation(success=False, error="Unable to find requested report")

        if kwargs['uphold']:
            try:
                activity = Activity.objects.get(id=report.activity.id)
            except Activity.DoesNotExist:
                return ResolveReportMutation(success=False, error="Unable to find activity to reject")

            schedule = Schedule.objects.filter(event=activity).delete()
            activity.delete()

            report.upheld = True
            report.resolved = True
            report.save()

            return ResolveReportMutation(success=True, error=None)
        else:
            report.resolved = True
            report.save()

            return ResolveReportMutation(success=True, error=None)