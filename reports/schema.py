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
    reports = graphene.List(ReportType)

    def resolve_report_categories(self, info, **kwargs):
        return ReportCategory.objects.all()

    def resolve_reports(self, info, **kwargs):
        return Report.objects.all()
