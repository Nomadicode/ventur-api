import json
from django.test import TestCase
from django.test import Client

class GraphQLTestCase(TestCase):
    def setUp (self):
        self._client = Client()

    def query (self, query: str, op_name: str = None, input: dict = None, headers: dict = {}):
        body = {
            'query': query
        }

        if op_name:
            body['operation_name'] = op_name

        if input:
            body['variables'] = input

        resp = self._client.post('/graphql',
                                 json.dumps(body),
                                 content_type='application/json',
                                 **headers)

        jresp = json.loads(resp.content.decode())
        return jresp

    def assertResponseNoErrors(self, resp: dict, expected: dict):
        self.assertNotIn('error', resp, 'Response had errors')
        self.assertNotIn('errors', resp, 'Response had errors')
        self.assertEqual(resp['data'], expected, 'Response has correct data')