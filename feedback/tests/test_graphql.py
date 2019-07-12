import uuid

from api.test_helper import GraphQLTestCase
from api.generators import Generator

from feedback.models import Feedback, FeedbackCategory


class FeedbackGraphQLTest(GraphQLTestCase):
    def setUp(self):
        self.generator = Generator()
        self.user = self.generator.create_test_user()
        super(FeedbackGraphQLTest, self).setUp()

    def test_get_feedback_categories(self):
        resp = self.query('''
                    { 
                        feedbackCategories {
                            id
                            name
                        } 
                    }
                ''')

        data = resp['data']
        self.assertEqual(len(data['feedbackCategories']), 4)

    def test_add_feedback(self):
        query = '''
                    mutation SubmitFeedback ($subject: String!, $category: Int!, $details: String!) {
                      submitFeedback (subject: $subject, category: $category, details: $details) {
                        success
                        error
                        feedback {
                          subject
                          details
                          category {
                            name
                          }
                        }
                      }
                    }
                '''

        category = FeedbackCategory.objects.all().order_by('?')[0]

        data = {
            "subject": str(uuid.uuid4())[:30],
            "category": category.id,
            "details": str(uuid.uuid4())
        }

        resp = self.query(query,
                          op_name='submitFeedback',
                          input=data,
                          headers={
                              'HTTP_AUTHORIZATION': 'JWT ' + self.user.get_jwt()
                          })

        self.assertResponseNoErrors(resp,
                                    {
                                        'submitFeedback': {
                                            'error': None,
                                            'success': True,
                                            'feedback': {
                                                'subject': data['subject'],
                                                'category': {
                                                    'name': category.name,
                                                },
                                                'details': data['details']
                                            }
                                        }
                                    }
                                   )

    def test_get_feedback(self):
        feedback = self.generator.create_feedback()
        resp = self.query('''
                    { 
                        feedback {
                            subject
                            details
                            category {
                                name
                            }
                        } 
                    }
                ''')

        data = resp['data']
        self.assertEqual(len(data['feedback']), 1)
        self.assertEqual(data['feedback'][0]['subject'], feedback.subject)

    def test_get_feedback_by_category(self):
        category_1 = FeedbackCategory.objects.first()
        category_2 = FeedbackCategory.objects.all()[3]

        feedback_1 = self.generator.create_feedback(category=category_1)
        feedback_2 = self.generator.create_feedback(category=category_2)
        resp = self.query('''
                    {
                        feedback (categoryId: ''' + str(category_2.id) + '''){
                            subject
                            details
                            category {
                                name
                            }
                        }
                    }
                ''')

        data = resp['data']
        self.assertEqual(len(data['feedback']), 1)
        self.assertEqual(data['feedback'][0]['subject'], feedback_2.subject)
