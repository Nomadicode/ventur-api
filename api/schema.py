import graphene

from users.schema import UserQuery
from activities.schema import ActivityQuery
from feedback.schema import FeedbackQuery
from reports.schema import ReportQuery
from preferences.schema import PreferenceQuery
from friends.schema import FriendQuery

from users import mutations as user_mutations
from activities import mutations as activity_mutations
from feedback import mutations as feedback_mutations
from reports import mutations as report_mutations
from preferences import mutations as preference_mutations
from friends import mutations as friend_mutations


class RootQuery(graphene.ObjectType, UserQuery, ActivityQuery, FeedbackQuery, ReportQuery, PreferenceQuery, FriendQuery):
    pass


class Mutations(graphene.ObjectType):
    update_profile = user_mutations.UserUpdateMutation.Field()

    # Activity Mutations
    add_activity = activity_mutations.ActivityAddMutation.Field()
    # schedule_activity = activity_mutations.ActivityScheduleMutation.Field()
    delete_activity = activity_mutations.ActivityDeleteMutation.Field()

    # Feedback Mutations
    submit_feedback = feedback_mutations.FeedbackAddMutation.Field()

    # Report Mutations
    submit_report = report_mutations.ReportActivityMutation.Field()

    # Preference Mutations
    accept_activity = preference_mutations.AcceptActivityMutation.Field()
    reject_activity = preference_mutations.RejectActivityMutation.Field()
    # save_activity = preference_mutations.SaveActivityMutation.Field()
    # unsave_activity = preference_mutations.UnsaveActivityMutation.Field()

    # Friend Mutations
    create_friend_group = friend_mutations.FriendGroupAddMutation.Field()
    create_friend_request = friend_mutations.FriendshipRequestMutation.Field()
    accept_friend_request = friend_mutations.FriendshipRequestAcceptMutation.Field()
    reject_friend_request = friend_mutations.FriendshipRequestRejectMutation.Field()
    remove_friend = friend_mutations.FriendshipRemoveMutation.Field()
    block_user = friend_mutations.BlockUserMutation.Field()
    unblock_user = friend_mutations.UnblockUserMutation.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutations)
