import graphene

from graphene_django.types import DjangoObjectType
from api.helpers import get_user_from_info

from .models import Report, ReportCategory


class ReportCategoryType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = ReportCategory


class ReportType(DjangoObjectType):
    pk = graphene.Int()
    reason = graphene.String()

    class Meta:
        model = Report

    def resolve_reason(self, info, **kwargs):
        return self.reason.name


class ReportQuery(object):
    report_categories = graphene.List(ReportCategoryType)
    reports = graphene.List(ReportType, resolved=graphene.Boolean(required=False), all=graphene.Boolean(required=False))

    def resolve_report_categories(self, info, **kwargs):
        return ReportCategory.objects.all()

    def resolve_reports(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated or not user.is_staff:
            raise Exception('Permission Error: User lacks sufficient permissions to view reports')

        if 'all' in kwargs and kwargs['all']:
            return Report.objects.all()

        if 'resolved' in kwargs and kwargs['resolved']:
            return Report.objects.filter(resolved=True)

        return Report.objects.filter(resolved=False)
