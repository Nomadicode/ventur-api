import random
import string

from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from users.models import User


class UserAuthTest(TestCase):
    client_class = APIClient

    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'testpass'
        self.user = User.objects.create_user(name='Test User', email=self.email, password=self.password, is_active=True)

    def test_user_registration(self):
        first_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        last_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        email = first_name + '@example.com'
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))

        url = '/auth/register/'
        response = self.client.post(url, {
            'name': first_name + ' ' + last_name,
            'email': email,
            'password': password
        }, format='json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['email'], email.lower())

    def test_user_login(self):
        url = reverse('rest_login')
        response = self.client.post(url, {
            'email': self.email,
            'password': self.password
        })
        
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_password_recovery(self):
        pass
