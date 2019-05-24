from django.urls import reverse
from django.views.generic import RedirectView

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    callback_url = 'localhost:8000'
    client_class = OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
