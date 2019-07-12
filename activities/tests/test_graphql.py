import uuid
from datetime import timedelta
from django.utils import timezone

from api.test_helper import GraphQLTestCase
from api.generators import Generator

from activities.models import Activity, Location, Schedule


class ActivityGraphQLTest(GraphQLTestCase):
    def setUp(self):
        self.generator = Generator()
        self.user = self.generator.create_test_user()
        super(ActivityGraphQLTest, self).setUp()

    def test_create_activity(self):
        query = '''
                    mutation AddActivity($name: String!, $media: String, $description: String, $categories: String, $duration: Int, $price: Float, $minimumAge: Int, $maximumAge: Int, 
                      $handicapFriendly: Boolean, $isNsfw: Boolean, $alcoholPresent: Boolean, $address: String, $latitude: Float, $longitude: Float, $startDatetime: String, $endDatetime: String, 
                      $frequency: Int, $groups: String) {
                        addActivity(name: $name, media: $media, description: $description, categories: $categories, duration: $duration, price: $price, minimumAge: $minimumAge, maximumAge: $maximumAge, 
                          handicapFriendly: $handicapFriendly, isNsfw: $isNsfw, alcoholPresent: $alcoholPresent, address: $address, latitude: $latitude, longitude: $longitude, startDatetime: $startDatetime,
                          endDatetime: $endDatetime, frequency: $frequency, groups: $groups) {
                        success
                        error
                        activity {
                          name
                        }
                      }
                    }
                '''

        variables = {
            'name': str(uuid.uuid4())[:20],
            'media': None,
            'description': str(uuid.uuid4()),
            'duration': 30,
            'price': None,
            'minimumAge': 0,
            'maximumAge': 65,
            'handicapFriendly': False,
            'isNsfw': True,
            'alcoholPresent': False,
            'latitude': 41.757595,
            'longitude': -111.834331,
            'startDatetime': timezone.now().strftime('%Y-%m-%dT%H:%M%z'),
            'endDatetime': (timezone.now() + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M%z'),
            'frequency': None,
            'groups': None
        }

        resp = self.query(query,
                          op_name='addActivity',
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'addActivity': {
                'success': True,
                'error': None,
                'activity': {
                    'name': variables['name']
                }
            }
        })

    def test_create_activity_no_schedule(self):
        query = '''
                    mutation AddActivity($name: String!, $media: String, $description: String, $categories: String, $duration: Int, $price: Float, $minimumAge: Int, $maximumAge: Int, 
                      $handicapFriendly: Boolean, $isNsfw: Boolean, $alcoholPresent: Boolean, $address: String, $latitude: Float, $longitude: Float, $startDatetime: String, $endDatetime: String, 
                      $frequency: Int, $groups: String) {
                        addActivity(name: $name, media: $media, description: $description, categories: $categories, duration: $duration, price: $price, minimumAge: $minimumAge, maximumAge: $maximumAge, 
                          handicapFriendly: $handicapFriendly, isNsfw: $isNsfw, alcoholPresent: $alcoholPresent, address: $address, latitude: $latitude, longitude: $longitude, startDatetime: $startDatetime,
                          endDatetime: $endDatetime, frequency: $frequency, groups: $groups) {
                        success
                        error
                        activity {
                          name
                        }
                      }
                    }
                '''

        variables = {
            'name': str(uuid.uuid4())[:20],
            'media': None,
            'description': str(uuid.uuid4()),
            'duration': 30,
            'price': None,
            'minimumAge': 0,
            'maximumAge': 65,
            'handicapFriendly': False,
            'isNsfw': True,
            'alcoholPresent': False,
            'latitude': 41.757595,
            'longitude': -111.834331,
            'startDatetime': None,
            'endDatetime': None,
            'frequency': None,
            'groups': None
        }

        resp = self.query(query,
                          op_name='addActivity',
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'addActivity': {
                'success': True,
                'error': None,
                'activity': {
                    'name': variables['name']
                }
            }
        })

    def test_get_activity(self):
        activity = self.generator.create_activity()

        query = '''
                query Activity($pk: ID!) {
                    activity (pk: $pk) {
                        id
                    }
                }
                '''

        variables = {
            'pk': str(activity.id)
        }

        resp = self.query(query,
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'activity': {
                'id': str(activity.id)
            }
        })

    def test_get_random_activity(self):
        activity_1 = self.generator.create_activity()
        activity_2 = self.generator.create_activity()
        activity_3 = self.generator.create_activity()
        activity_4 = self.generator.create_activity()
        activity_5 = self.generator.create_activity()
        activity_6 = self.generator.create_activity()

        query = '''
                query randomActivity($latitude: Float, $longitude: Float){ 
                  randomActivity (latitude: $latitude, longitude: $longitude) {
                    pk
                  }
                }
                '''

        variables = {
            'latitude': 41.741899,
            'longitude': -111.848185
        }

        resp = self.query(query,
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        data = resp['data']

        self.assertEqual(len(data['randomActivity']), 1)

    def test_get_activities_by_creator(self):
        activity_1 = self.generator.create_activity()
        activity_2 = self.generator.create_activity(creator=self.user)
        activity_3 = self.generator.create_activity()
        activity_4 = self.generator.create_activity()

        query = '''
                query Activities($createdBy: ID!) {
                   activities (createdBy: $createdBy) {
                       id
                   }
                }
                '''

        variables = {
            'createdBy': str(self.user.id)
        }

        resp = self.query(query,
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        data = resp['data']

        self.assertEqual(len(data['activities']), 1)

    def test_get_activities_with_filters(self):
        pass

    def test_update_activity_core(self):
        activity = self.generator.create_activity(creator=self.user, nsfw=True, handicap=False, minimum_age=0, maximum_age=65)
        query = '''
                    mutation UpdateActivity($pk: ID!, $name: String, $media: String, $description: String, $categories: String, $duration: Int, $price: Float, $minimumAge: Int, $maximumAge: Int, 
                      $handicapFriendly: Boolean, $isNsfw: Boolean, $alcoholPresent: Boolean, $address: String, $latitude: Float, $longitude: Float, $startDatetime: String, $endDatetime: String, 
                      $frequency: Int, $groups: String) {
                        updateActivity(pk: $pk, name: $name, media: $media, description: $description, categories: $categories, duration: $duration, price: $price, minimumAge: $minimumAge, maximumAge: $maximumAge, 
                          handicapFriendly: $handicapFriendly, isNsfw: $isNsfw, alcoholPresent: $alcoholPresent, address: $address, latitude: $latitude, longitude: $longitude, startDatetime: $startDatetime,
                          endDatetime: $endDatetime, frequency: $frequency, groups: $groups) {
                        success
                        error
                        activity {
                          name
                          duration
                          price
                          minimumAge
                          maximumAge
                          handicapFriendly
                          isNsfw
                        }
                      }
                    }
                '''

        variables = {
            'pk': str(activity.id),
            'name': str(uuid.uuid4())[:20],
            'duration': 60,
            'price': 45.00,
            'minimumAge': 19,
            'maximumAge': 33,
            'handicapFriendly': True,
            'isNsfw': False
        }

        resp = self.query(query,
                          op_name='updateActivity',
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'updateActivity': {
                'success': True,
                'error': None,
                'activity': {
                    'name': variables['name'],
                    'duration': variables['duration'],
                    'price': variables['price'],
                    'minimumAge': variables['minimumAge'],
                    'maximumAge': variables['maximumAge'],
                    'handicapFriendly': variables['handicapFriendly'],
                    'isNsfw': variables['isNsfw']
                }
            }
        })

    def test_update_activity_location(self):
        activity = self.generator.create_activity(creator=self.user, nsfw=True, handicap=False, minimum_age=0,
                                                  maximum_age=65)
        query = '''
                    mutation UpdateActivity($pk: ID!, $name: String, $media: String, $description: String, $categories: String, $duration: Int, $price: Float, $minimumAge: Int, $maximumAge: Int, 
                      $handicapFriendly: Boolean, $isNsfw: Boolean, $alcoholPresent: Boolean, $address: String, $latitude: Float, $longitude: Float, $startDatetime: String, $endDatetime: String, 
                      $frequency: Int, $groups: String) {
                        updateActivity(pk: $pk, name: $name, media: $media, description: $description, categories: $categories, duration: $duration, price: $price, minimumAge: $minimumAge, maximumAge: $maximumAge, 
                          handicapFriendly: $handicapFriendly, isNsfw: $isNsfw, alcoholPresent: $alcoholPresent, address: $address, latitude: $latitude, longitude: $longitude, startDatetime: $startDatetime,
                          endDatetime: $endDatetime, frequency: $frequency, groups: $groups) {
                        success
                        error
                        activity {
                          location {
                            latitude
                            longitude
                          }
                        }
                      }
                    }
                '''

        variables = {
            'pk': str(activity.id),
            'latitude': 41.720667,
            'longitude': -111.830426
        }

        resp = self.query(query,
                          op_name='updateActivity',
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'updateActivity': {
                'success': True,
                'error': None,
                'activity': {
                    'location': {
                        'latitude': variables['latitude'],
                        'longitude': variables['longitude']
                    }
                }
            }
        })

    def test_update_activity_schedule(self):
        pass
        # activity = self.generator.create_activity()
        # query = '''
        #             mutation UpdateActivity($pk: ID!, $name: String, $media: String, $description: String, $categories: String, $duration: Int, $price: Float, $minimumAge: Int, $maximumAge: Int,
        #               $handicapFriendly: Boolean, $isNsfw: Boolean, $alcoholPresent: Boolean, $address: String, $latitude: Float, $longitude: Float, $startDatetime: String, $endDatetime: String,
        #               $frequency: Int, $groups: String) {
        #                 updateActivity(pk: $pk, name: $name, media: $media, description: $description, categories: $categories, duration: $duration, price: $price, minimumAge: $minimumAge, maximumAge: $maximumAge,
        #                   handicapFriendly: $handicapFriendly, isNsfw: $isNsfw, alcoholPresent: $alcoholPresent, address: $address, latitude: $latitude, longitude: $longitude, startDatetime: $startDatetime,
        #                   endDatetime: $endDatetime, frequency: $frequency, groups: $groups) {
        #                 success
        #                 error
        #                 activity {
        #                   name
        #                 }
        #               }
        #             }
        #         '''
        #
        # variables = {
        #     'pk': str(activity.id),
        #     'startDatetime': timezone.now().strftime('%Y-%m-%dT%H:%M%z'),
        #     'endDatetime': (timezone.now() + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M%z'),
        #     'frequency': None
        # }
        #
        # resp = self.query(query,
        #                   op_name='updateActivity',
        #                   input=variables,
        #                   headers={
        #                       'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
        #                   })
        #
        # self.assertResponseNoErrors(resp, {
        #     'updateActivity': {
        #         'success': True,
        #         'error': None,
        #         'activity': {
        #             'name': variables['name']
        #         }
        #     }
        # })

    def test_delete_activity(self):
        activity = self.generator.create_activity(creator=self.user)

        query = '''
                mutation DeleteActivity ($pk: ID!) {
                  deleteActivity (pk: $pk) {
                    success
                    error
                  }
                }
               '''

        variables = {
            'pk': str(activity.id)
        }

        resp = self.query(query,
                          op_name='deleteActivity',
                          input=variables,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'deleteActivity': {
                'success': True,
                'error': None
            }
        })
        # activity = self.generator.create_activity()
        # resp = self.query('''
        #     {
        #         activity (pk: ''' + activity.id + ''') {
        #             id
        #             name
        #             description
        #             price
        #             duration
        #             location {
        #                 latitude
        #                 longitude
        #             }
        #             createdBy
        #             created
        #         }
        #     }
        # ''')
        #
        # print(resp)