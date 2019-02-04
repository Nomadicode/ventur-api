import graphene

from users.schema import UserQuery
from activities.schema import ActivityQuery
from feedback.schema import FeedbackQuery
from reports.schema import ReportQuery
from preferences.schema import PreferenceQuery

from users import mutations as user_mutations
from activities import mutations as activity_mutations
from feedback import mutations as feedback_mutations
from reports import mutations as report_mutations
from preferences import mutations as preference_mutations


class RootQuery(graphene.ObjectType, UserQuery, ActivityQuery, FeedbackQuery, ReportQuery, PreferenceQuery):
    pass


class Mutations(graphene.ObjectType):
    update_user = user_mutations.UserUpdateMutation.Field()

    # Activity Mutations
    add_activity = activity_mutations.ActivityAddMutation.Field()
    delete_activity = activity_mutations.ActivityDeleteMutation.Field()

    # Feedback Mutations
    submit_feedback = feedback_mutations.FeedbackAddMutation.Field()

    # Report Mutations
    submit_report = report_mutations.ReportActivityMutation.Field()

    # Preference Mutations
    accept_activity = preference_mutations.AcceptActivityMutation.Field()
    reject_activity = preference_mutations.RejectActivityMutation.Field()
    save_activity = preference_mutations.SaveActivityMutation.Field()
    unsave_activity = preference_mutations.UnsaveActivityMutation.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutations)
