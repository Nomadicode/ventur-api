import graphene

from core.schema import CoreQuery
from geo.schema import GeoQuery
from users.schema import UserQuery
from activities.schema import ActivityQuery

from users import mutations as user_mutations
from activities import mutations as activity_mutations


class RootQuery(graphene.ObjectType, UserQuery, CoreQuery, GeoQuery, ActivityQuery):
    pass


class Mutations(graphene.ObjectType):
    update_user = user_mutations.UserUpdateMutation.Field()
    add_activity = activity_mutations.ActivityAddMutation.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutations)