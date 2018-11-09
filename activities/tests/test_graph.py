import json
import os
import urllib
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from users.models import User
from activities.models import Activity, Category


class ActivityGraphTest(TestCase):
    client_class = APIClient

    def test_activity_add(self):
        activity = {
            'title': 'Test Activity',
            'description': 'Test activity description',
            'categories': ['Test', 'cool', 'activity'],
            'latitude': 47.22232,
            'longitude': 111.23234
            'duration': 15,
            'price': 10.00,
            'ageRanges': '0,3'
        }

        data = {
            'query': '''
                mutation AddActivity($title: String!, $description: String, $duration: Int, $price: Float, $categories: String, $ageRanges: String, $latitude: String, $longitude: String, $media: String) {
                    addActivity(title: $title, description: $description, duration: $duration, price: $price, categories: $categories, ageRanges: $ageRanges. latitude: $latitude, longitude: $longitude, media: $media) {
                        success
                        error
                        activity {
                            title
                        }
                    }
                }
            ''',
            'variables': activity
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)