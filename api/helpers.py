import base64
import random
import string
import googlemaps

from mimetypes import guess_extension, guess_all_extensions, guess_type

from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.models import AnonymousUser
from geopy.geocoders import GoogleV3

from users.models import User


def get_user_from_info(info):
    jwt = info.context.META.get('HTTP_AUTHORIZATION', None)
    if jwt:
        jwt = jwt.split(' ')[-1]
        return User.decode_jwt(jwt)
    return AnonymousUser()

def base64_to_file(encoded_str):
    format, imgstr = encoded_str.split(';base64,')
    ext = format.split('/')[-1]

    file_name = 'media_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '.' + ext
    file_contents = base64.b64decode(imgstr)
    return ContentFile(file_contents, name=file_name)

def get_address_from_latlng(latitude, longitude):
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    gmaps.
    geolocator = GoogleV3(api_key=settings.GOOGLE_API_KEY, timeout=10)
    if latitude and longitude:
        location = geolocator.reverse(str(latitude) + ", " + str(longitude), sensor=True, exactly_one=True)
        return location.name, location.address

    return None

def get_latlng_from_address(address=None, city=None, state=None, location_str=None):
    geolocator = GoogleV3(api_key=settings.GOOGLE_API_KEY, timeout=10)
    if address and city and state:
        location = geolocator.geocode(address + " " + city + ", " + state.abbreviation)
        return location.latitude, location.longitude

    if location_str:
        location = geolocator.geocode(location_str)
        return location.latitude, location.longitude

    return None, None

def get_distance(origin=None, destination=None, unit='imperial'):
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    distance = gmaps.distance_matrix(origin, destination, units=unit)

    if distance['status'] != 'OK':
        return None

    return distance['rows'][0]['elements'][0]['distance']['text']

def sanitize_category(name):
    name = name.lower().strip()
    return name
