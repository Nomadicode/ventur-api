import graphene

from users.schema import UserQuery
from activities.schema import ActivityQuery

from users import mutations as user_mutations
from activities import mutations as activity_mutations


class RootQuery(graphene.ObjectType, UserQuery, ActivityQuery):
    pass


class Mutations(graphene.ObjectType):
    update_user = user_mutations.UserUpdateMutation.Field()

    # Activity Mutations
    add_activity = activity_mutations.ActivityAddMutation.Field()
    delete_activity = activity_mutations.ActivityDeleteMutation.Field()
    update_activity = activity_mutations.ActivityUpdateMutation.Field()
    save_activity = activity_mutations.ActivitySaveMutation.Field()
    unsave_activity = activity_mutations.ActivityUnsaveMutation.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutations)
