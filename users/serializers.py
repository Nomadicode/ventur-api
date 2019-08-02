import datetime
from dateutil import parser

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from rest_framework import serializers, exceptions

from .models import User, UserSettings


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)

            if not user.is_staff:
                msg = _('User is not authorized')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = User
        exclude = ('password', )
        read_only_fields = ('pk', )


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = "__all__"


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password = serializers.CharField(required=True, write_only=True)
    date_of_birth = serializers.DateField(required=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address.")
                )
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate_name(self, name):
        return name

    def validate_date_of_birth(self, date_of_birth):
        return date_of_birth

    def create(self, validated_data):
        User = get_user_model()
        password = validated_data.pop('password', None)
        name = validated_data.pop('name', None)

        user = User(
            name=name,
            email=validated_data.get('email', ''),
            date_of_birth=validated_data.get('date_of_birth', None)
        )
        user.set_password(password)
        user.save()

        user_settings = UserSettings.objects.create(user=user)
        return user

    def save(self, request=None):
        return super(RegisterSerializer, self).save()
