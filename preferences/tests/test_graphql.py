import uuid
from datetime import timedelta
from django.utils import timezone

from api.test_helper import GraphQLTestCase
from api.generators import Generator

from preferences.models import AcceptedActivity, SavedActivity, RejectedActivity


class PreferenceGraphQLTest(GraphQLTestCase):
    def setUp(self):
        self.generator = Generator()
        self.user = self.generator.create_test_user()
        super(PreferenceGraphQLTest, self).setUp()

    def test_save_activity(self):
        activity = self.generator.create_activity()

        query = '''
                mutation SaveActivity ($activity: ID!) {
                  saveActivity (activity: $activity) {
                    success
                    error
                    activity {
                      activity {
                        pk
                      }
                    }
                  }
                }
                '''

        variables = {
            'activity': str(activity.id)
        }

        resp = self.query(query,
                          op_name='saveActivity',
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'saveActivity': {
                'success': True,
                'error': None,
                'activity': {
                    'activity': {
                        'pk': str(activity.id)
                    }
                }
            }
        })

    def test_unsave_activity(self):
        activity = self.generator.create_activity()
        SavedActivity.objects.create(activity=activity, user=self.user)

        query = '''
                mutation unsaveActivity ($activity: ID!) {
                  unsaveActivity (activity: $activity) {
                    success
                    error
                  }
                }
                '''

        variables = {
            'activity': str(activity.id)
        }

        resp = self.query(query,
                          op_name='unsaveActivity',
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'unsaveActivity': {
                'success': True,
                'error': None
            }
        })

    def test_get_saved_activities(self):
        activity = self.generator.create_activity()
        SavedActivity.objects.create(activity=activity, user=self.user)

        query = '''
                { 
                    savedActivities {
                        id
                        activity {
                            id
                        }
                    }
                }
                '''

        resp = self.query(query,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        data = resp['data']
        self.assertEqual(len(data['savedActivities']), 1)
