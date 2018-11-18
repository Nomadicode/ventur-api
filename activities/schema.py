import graphene
from recurrence.fields import RecurrenceField
from recurrence import Recurrence

from graphene_django.converter import convert_django_field
from graphene_django.types import DjangoObjectType
from graphene_django.fields import DjangoListField
from graphene import Dynamic
from api.helpers import get_user_from_info

from .models import Category, Activity


@convert_django_field.register(RecurrenceField)
def convert_recurrence_field(field, registry=None):
    model = Recurrence

    def dynamic_type():
        # print(field.occurrences)

        return DjangoListField(field)

    return Dynamic(dynamic_type)


class CategoryType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Category


class ActivityType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Activity


class ActivityQuery(object):
    activities = graphene.List(ActivityType)
    categories = graphene.List(CategoryType)

    def resolve_activities(self, info, **kwargs):
        user = get_user_from_info(info)

        if not user.is_authenticated:
            return None

        return Activity.objects.all()

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()
