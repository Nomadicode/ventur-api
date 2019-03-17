import random
import string

from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from feedback.models import Feedback, FeedbackCategory


class FeedbackTest(TestCase):
    client_class = APIClient

    def setUp(self):
        pass

    def test_get_feedback_categories(self):
        pass

    def test_add_feedback(self):
        pass

    def test_get_feedback(self):
        pass

    def test_get_feedback_by_category(self):
        pass
