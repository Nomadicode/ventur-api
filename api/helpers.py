import base64
import random
import string

from django.core.files.base import ContentFile
from django.contrib.auth.models import AnonymousUser
from geopy.geocoders import Nominatim

from users.models import User


def get_user_from_info(info):
    jwt = info.context.META.get('HTTP_AUTHORIZATION', None)
    if jwt:
        jwt = jwt.split(' ')[-1]
        return User.decode_jwt(jwt)
    return AnonymousUser()


def base64_to_file(encoded_str):
    file_name = 'media_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '.png'
    file_path = '/tmp/' + file_name
    file_content = base64.b64decode(encoded_str)
    
    return ContentFile(file_content, name=file_name)


def get_address_from_latlng(latitude, longitude):
    geolocator = Nominatim(user_agent="driftr-app")
    if latitude and longitude:
        location = geolocator.reverse(str(latitude) + ", " + str(longitude))
        return location.address

    return None


def get_latlng_from_address(address=None, city=None, state=None, location_str=None):
    geolocator = Nominatim(user_agent="driftr-app")
    if address and city and state:
        location = geolocator.geocode(address + " " + city + ", " + state.abbreviation)

        return location.latitude, location.longitude

    if location_str:
        location = geolocator.geocode(location_str)

        return location.latitude, location.longitude

    return None, None
