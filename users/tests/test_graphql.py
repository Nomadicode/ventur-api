import uuid

from api.test_helper import GraphQLTestCase
from api.generators import Generator


class UserGraphQLTest(GraphQLTestCase):
    def setUp(self):
        self.generator = Generator()
        self.user = self.generator.create_test_user()
        super(UserGraphQLTest, self).setUp()

    def test_get_user(self):
        resp = self.query('''
            { 
                users {
                    id
                } 
            }
        ''')

        self.assertResponseNoErrors(resp, {'users': [{'id': str(self.user.id) }]})

    def test_user_update(self):
        query = '''
            mutation UpdateProfile ($name: String, $email: String, $handle: String, $dateOfBirth: Date, $profilePicture: String, $timezone: String, $latitude: Float, $longitude: Float){
              updateProfile(name: $name, email: $email, handle: $handle, dateOfBirth: $dateOfBirth, profilePicture: $profilePicture, timezone: $timezone, latitude: $latitude, longitude: $longitude) {
                success
                error
                user {
                  name
                  handle
                }
              }
            }
        '''

        data = {
            "name": "Test User",
            "handle": str(uuid.uuid4())[:8]
        }

        resp = self.query(query,
                          op_name='updateProfile',
                          input=data,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp,
                                    {
                                        'updateProfile': {
                                            'error': None,
                                            'success': True,
                                            'user': {
                                                'name': data['name'],
                                                'handle': data['handle']
                                            }
                                        }
                                    }
                                   )

    def test_user_delete(self):
        query = '''
            mutation RequestAccountDelete ($pk: ID!) {
              requestAccountDelete (pk: $pk) {
                success
                error
              }
            }
        '''

        data = {
            "pk": str(self.user.id)
        }

        resp = self.query(query,
                          op_name='requestAccountDelete',
                          input=data,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp,
                                    {
                                        'requestAccountDelete': {
                                            'error': None,
                                            'success': True
                                        }
                                    }
                                    )

    def test_user_settings(self):
        query = '''
               mutation UpdateUserSettings ($showAlcohol: Boolean, $showNsfw: Boolean, $handicapOnly: Boolean, $newFriendEventNotification: Boolean, $upcomingSavedEventNotification: Boolean) {
                  updateUserSettings (showAlcohol: $showAlcohol, showNsfw: $showNsfw, handicapOnly: $handicapOnly, newFriendEventNotification: $newFriendEventNotification, upcomingSavedEventNotification: $upcomingSavedEventNotification) {
                    success
                    error
                    userSettings {
                      showAlcohol
                      showNsfw
                      handicapOnly
                      newFriendEventNotification
                      upcomingSavedEventNotification
                    }
                  }
                }
                '''

        variables = {
            'showAlcohol': True,
            'showNsfw': False,
            'handicapOnly': False,
            'newFriendEventNotification': True,
            'upcomingSavedEventNotification': False
        }

        resp = self.query(query,
                          op_name='updateUserSettings',
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp,
                                    {
                                        'updateUserSettings': {
                                            'error': None,
                                            'success': True,
                                            'userSettings': {
                                                'showAlcohol': True,
                                                'showNsfw': False,
                                                'handicapOnly': False,
                                                'newFriendEventNotification': True,
                                                'upcomingSavedEventNotification': False
                                            }
                                        }
                                    }
                                    )