import json
import requests
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from activities.models import Category


class Command(BaseCommand):
    help = 'Fetches all categories from Eventbrite'

    def handle(self, *args, **kwargs):
        headers = {
            'Authorization': 'Bearer TYAYIW476KEAOWOKLOW3'
        }

        page = 1

        while True:
            url = 'https://www.eventbriteapi.com/v3/subcategories?page={0}'.format(page)

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                categories = json.loads(response.text)

                for category in categories['subcategories']:
                    category, created = Category.objects.get_or_create(name=category['name'])

                if categories['pagination']['has_more_items']:
                    page += 1
                else:
                    break
