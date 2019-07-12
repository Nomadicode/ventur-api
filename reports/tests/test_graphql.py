import uuid
from datetime import timedelta
from django.utils import timezone

from api.test_helper import GraphQLTestCase
from api.generators import Generator

from reports.models import ReportCategory


class ReportGraphQLTest(GraphQLTestCase):
    def setUp(self):
        self.generator = Generator()
        self.user = self.generator.create_test_user()
        super(ReportGraphQLTest, self).setUp()

    def test_get_report_categories(self):
        query = '''
                { 
                    reportCategories {
                        id
                        name
                        detail
                    }
                }
                '''

        resp = self.query(query,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        data = resp['data']
        self.assertEqual(len(data['reportCategories']), 10)

    def test_get_reports(self):
        report = self.generator.create_report()
        query = '''
                { 
                    reports {
                        id
                        detail
                    }
                }
                '''

        resp = self.query(query,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        data = resp['data']
        self.assertEqual(len(data['reports']), 1)

    def test_submit_report(self):
        category = ReportCategory.objects.all().order_by('?')[0]
        activity = self.generator.create_activity()
        query = '''
                mutation SubmitReport($activity: ID!, $category: Int!, $detail: String){
                  submitReport(activity: $activity, category: $category, detail: $detail) {
                    success
                    error
                    report {
                      activity {
                        name
                      }
                    }
                  }
                }
                '''

        variables = {
            'activity': str(activity.id),
            'category': category.id
        }

        resp = self.query(query,
                          input=variables,
                          op_name='submitReport',
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp, {
            'submitReport': {
                'success': True,
                'error': None,
                'report': {
                    'activity': {
                        'name': activity.name
                    }
                }
            }
        })