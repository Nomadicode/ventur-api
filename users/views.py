from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_auth.app_settings import (
    TokenSerializer, UserDetailsSerializer, LoginSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    PasswordChangeSerializer, JWTSerializer, create_token
)

from users.serializers import AdminLoginSerializer
from rest_auth.models import TokenModel
from rest_auth.utils import jwt_encode


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


# Create your views here.
class AdminLoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework
    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = AdminLoginSerializer
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(AdminLoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()