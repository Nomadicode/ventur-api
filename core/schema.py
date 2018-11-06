import graphene

from graphene_django.types import DjangoObjectType
from graphene_django import DjangoConnectionField

from .models import FeedbackCategory, Feedback


class FeedbackCategoryType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = FeedbackCategory


class FeedbackType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Feedback


class CoreQuery(graphene.AbstractType):
    feedback_categories = graphene.List(FeedbackCategoryType)


    def resolve_feedback_categories(self, info, **kwargs):
        return FeedbackCategory.objects.all()
