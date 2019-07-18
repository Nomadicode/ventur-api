import base64
import json
import requests
from dateutil import parser
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.gis.geos import GEOSGeometry
from django.db import IntegrityError

from api.helpers import base64_to_file
from users.models import User
from activities.models import Activity, Schedule, Location


class Command(BaseCommand):
    help = 'Fetches all events found on key sites for the specified cities'

    def add_arguments(self, parser):
        parser.add_argument('city', type=str, help='Specify which city to find events in')
        parser.add_argument('state', type=str, help='Specify which state that city is in')

    def handle(self, *args, **kwargs):
        city = kwargs['city']
        state = kwargs['state']

        system_user = User.objects.get(is_system=True)

        eventbrite = requests.get('https://www.eventbriteapi.com/v3/events/search?expand=venue&token=TYAYIW476KEAOWOKLOW3')

        if eventbrite.status_code == 200:
            events = json.loads(eventbrite.text)

            for event in events['events']:
                location_data = {
                    'address': event['venue']['address']['localized_address_display'],
                    'latitude': float(event['venue']['address']['latitude']),
                    'longitude': float(event['venue']['address']['longitude'])
                }
                location_data['point'] = GEOSGeometry('POINT(%s %s)' % (location_data['longitude'],
                                                      location_data['latitude']),
                                                      srid=4326)

                try:
                    location, created = Location.objects.get_or_create(**location_data)
                except IntegrityError:
                    continue

                schedule = Schedule(start=parser.parse(event['start']['utc']), end=parser.parse(event['end']['utc']))

                logo = None
                try:
                    b64Img = base64.b64encode(requests.get(event['logo']['url']).content)
                    logo = base64_to_file(b64Img)
                except Exception:
                    pass

                activity = {
                    'created_by': system_user,
                    'name': event['name']['text'],
                    'media': logo,
                    'description': event['description']['html'],
                    'location': location
                }

                activity = Activity.objects.create(**activity)

                if schedule:
                    schedule.event = activity
                    schedule.save()