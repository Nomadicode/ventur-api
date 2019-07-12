import uuid
from api.test_helper import GraphQLTestCase
from api.generators import Generator


class FriendGraphQLTest(GraphQLTestCase):
    def setUp(self):
        self.generator = Generator()
        self.user = self.generator.create_test_user()
        super(FriendGraphQLTest, self).setUp()

    def test_get_friend_groups(self):
        group_1 = self.generator.create_friend_group(user=self.user)
        group_2 = self.generator.create_friend_group()
        group_3 = self.generator.create_friend_group(user=self.user)

        query = '''
                query FriendGroups ($query: String) {
                  friendGroups (query: $query) {
                    pk
                    id
                    name
                  }
                }
                '''

        variables = {
            'query': group_1.name[:3]
        }

        resp = self.query(query,
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        data = resp['data']
        self.assertEqual(len(data['friendGroups']), 1)

    def test_create_group(self):
        query = '''
                mutation CreateFriendGroup($name: String!){
                  createFriendGroup(name: $name) {
                    success
                    error
                    group {
                      name
                    }
                  }
                } 
                '''

        variables = {
            'name': str(uuid.uuid4())[:15]
        }

        resp = self.query(query,
                          input=variables,
                          op_name='createFriendGroup',
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'createFriendGroup': {
                'success': True,
                'error': None,
                'group': {
                    'name': variables['name']
                }
            }
        })

    def test_update_group(self):
        group = self.generator.create_friend_group(self.user)
        query = '''
                mutation UpdateFriendGroup($pk: Int!, $name: String!){
                  updateFriendGroup(pk: $pk, name: $name) {
                    success
                    error
                    group {
                      name
                    }
                  }
                } 
                '''

        variables = {
            'pk': group.id,
            'name': str(uuid.uuid4())[:15]
        }

        resp = self.query(query,
                          input=variables,
                          op_name='updateFriendGroup',
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'updateFriendGroup': {
                'success': True,
                'error': None,
                'group': {
                    'name': variables['name']
                }
            }
        })

    def test_delete_group(self):
        group = self.generator.create_friend_group(self.user)
        query = '''
                mutation RemoveFriendGroup($pk: Int!){
                  removeFriendGroup(pk: $pk) {
                    success
                    error
                  }
                } 
                '''

        variables = {
            'pk': group.id
        }

        resp = self.query(query,
                          input=variables,
                          op_name='removeFriendGroup',
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'removeFriendGroup': {
                'success': True,
                'error': None
            }
        })

    def test_add_friend_to_group(self):
        friend = self.generator.create_test_user()

        request = self.generator.create_friend(self.user, friend)
        group = self.generator.create_friend_group(user=self.user)

        query = '''
                mutation AddFriendToGroup ($groupId: Int!, $memberId: String!) {
                  addFriendToGroup (groupId: $groupId, memberId: $memberId) {
                    success
                    error,
                    group {
                      pk
                      friends {
                        id
                      }
                    }
                  }
                }
                '''

        variables = {
            'groupId': group.id,
            'memberId': str(friend.id)
        }

        resp = self.query(query,
                          input=variables,
                          op_name='addFriendToGroup',
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'addFriendToGroup': {
                'success': True,
                'error': None,
                'group': {
                    'pk': group.id,
                    'friends': [{
                        'id': str(friend.id)
                    }]
                }
            }
        })

    def test_remove_friend_from_group(self):
        friend = self.generator.create_test_user()
        group = self.generator.create_friend_group(self.user, friend=friend, friends=3)

        query = '''
                mutation RemoveFriendFromGroup($groupId: Int!, $memberId:ID!){
                  removeFriendFromGroup(groupId: $groupId, memberId: $memberId) {
                    success
                    error
                    group {
                      pk
                      name
                      friends {
                        id
                      }
                    }
                  }
                }
                '''

        variables = {
            'groupId': group.id,
            'memberId': str(friend.id)
        }

        resp = self.query(query,
                          input=variables,
                          op_name='addFriendToGroup',
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertEqual(len(resp['data']['removeFriendFromGroup']['group']['friends']), 3)

    def test_send_friend_request(self):
        friend = self.generator.create_test_user()

        query = '''
                mutation CreateFriendRequest ($handle: String!, $message: String) {
                  createFriendRequest (handle: $handle, message: $message) {
                    success
                    error
                    friendshipRequest {
                        toUser {
                            id
                        }
                    }
                  }
                } 
                '''

        variables = {
            'handle': friend.handle
        }

        resp = self.query(query,
                          input=variables,
                          op_name='createFriendRequest',
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'createFriendRequest': {
                'success': True,
                'error': None,
                'friendshipRequest': {
                    'toUser': {
                        'id': str(friend.id)
                    }
                }
            }
        })

    def test_accept_friend_request(self):
        friend = self.generator.create_test_user()
        friend_request = self.generator.create_friend_request(self.user, friend)

        query = '''
                mutation AcceptFriendRequest ($handle: String!) {
                  acceptFriendRequest (handle: $handle) {
                    success
                    error
                  }
                }
                '''

        variables = {
            'handle': self.user.handle
        }

        resp = self.query(query,
                          input=variables,
                          op_name='acceptFriendRequest',
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + friend.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'acceptFriendRequest': {
                'success': True,
                'error': None
            }
        })

    def test_reject_friend_request(self):
        friend = self.generator.create_test_user()
        friend_request = self.generator.create_friend_request(self.user, friend)

        query = '''
                mutation RejectFriendRequest ($handle: String!) {
                  rejectFriendRequest (handle: $handle) {
                    success
                    error
                  }
                }
                '''

        variables = {
            'handle': self.user.handle
        }

        resp = self.query(query,
                          input=variables,
                          op_name='rejectFriendRequest',
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + friend.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'rejectFriendRequest': {
                'success': True,
                'error': None
            }
        })

    def test_cancel_friend_request(self):
        friend = self.generator.create_test_user()
        friend_request = self.generator.create_friend_request(self.user, friend)

        query = '''
                mutation CancelFriendRequest ($handle: String!) {
                  cancelFriendRequest (handle: $handle) {
                    success
                    error
                  }
                }
                '''

        variables = {
            'handle': friend.handle
        }

        resp = self.query(query,
                          input=variables,
                          op_name='cancelFriendRequest',
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'cancelFriendRequest': {
                'success': True,
                'error': None
            }
        })

    def test_get_friends(self):
        self.generator.create_friend(self.user)
        self.generator.create_friend(self.user)
        self.generator.create_friend()

        query = '''
                query friendships { 
                  friendships {
                    id
                  }
                }
                '''

        resp = self.query(query,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        data = resp['data']
        self.assertEqual(len(data['friendships']), 2)

    def test_get_pending_requests(self):
        self.generator.create_friend_request(friend=self.user)
        self.generator.create_friend_request(friend=self.user)
        self.generator.create_friend_request()

        query = '''
                query pendingFriendRequests { 
                  pendingFriendRequests {
                    id
                    fromUser {
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
        self.assertEqual(len(data['pendingFriendRequests']), 2)

    def test_get_sent_requests(self):
        self.generator.create_friend_request(self.user)
        self.generator.create_friend_request(self.user)
        self.generator.create_friend_request()

        query = '''
                query {
                  sentFriendRequests {
                    id
                    toUser {
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
        self.assertEqual(len(data['sentFriendRequests']), 2)

    def test_get_friend_suggestions(self):
        self.generator.create_test_user()
        self.generator.create_test_user()
        self.generator.create_test_user()
        self.generator.create_test_user()
        self.generator.create_test_user()

        query = '''
                query {
                  friendSuggestions {
                    id
                    handle
                  }
                }
                '''

        resp = self.query(query,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        data = resp['data']
        self.assertEqual(len(data['friendSuggestions']), 5)