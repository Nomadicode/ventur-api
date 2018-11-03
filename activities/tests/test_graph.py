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

    