import graphene

from graphene_django.types import DjangoObjectType

from .models import FeedbackCategory, Feedback


class FeedbackCategoryType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = FeedbackCategory


class FeedbackType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Feedback


class FeedbackQuery(graphene.AbstractType):
    feedback_categories = graphene.List(FeedbackCategoryType)
    feedback = graphene.List(FeedbackType)

    def resolve_feedback_categories(self, info, **kwargs):
        return FeedbackCategory.objects.all()

    def resolve_feedback(self, info, **kwargs):
        return Feedback.objects.all()
