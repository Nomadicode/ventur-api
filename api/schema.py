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
    update_user_settings = user_mutations.UserSettingsUpdateMutation.Field()
    request_account_delete = user_mutations.RequestAccountDelete.Field()

    # Activity Mutations
    add_activity = activity_mutations.ActivityAddMutation.Field()
    update_activity = activity_mutations.ActivityUpdateMutation.Field()
    delete_activity = activity_mutations.ActivityDeleteMutation.Field()

    # Feedback Mutations
    submit_feedback = feedback_mutations.FeedbackAddMutation.Field()

    # Report Mutations
    submit_report = report_mutations.ReportActivityMutation.Field()
    resolve_report = report_mutations.ResolveReportMutation.Field()

    # Preference Mutations
    reject_activity = preference_mutations.RejectActivityMutation.Field()
    save_activity = preference_mutations.SaveActivityMutation.Field()
    unsave_activity = preference_mutations.UnsaveActivityMutation.Field()

    # Friend Mutations
    create_friend_group = friend_mutations.FriendGroupAddMutation.Field()
    update_friend_group = friend_mutations.FriendGroupUpdateMutation.Field()
    remove_friend_group = friend_mutations.FriendGroupRemoveMutation.Field()
    add_friend_to_group = friend_mutations.FriendGroupAddMemberMutation.Field()
    remove_friend_from_group = friend_mutations.FriendGroupRemoveMemberMutation.Field()

    create_friend_request = friend_mutations.FriendshipRequestMutation.Field()
    accept_friend_request = friend_mutations.FriendshipRequestAcceptMutation.Field()
    reject_friend_request = friend_mutations.FriendshipRequestRejectMutation.Field()
    cancel_friend_request = friend_mutations.FriendshipRequestCancelMutation.Field()
    remove_friend = friend_mutations.FriendshipRemoveMutation.Field()
    block_user = friend_mutations.BlockUserMutation.Field()
    unblock_user = friend_mutations.UnblockUserMutation.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutations)
