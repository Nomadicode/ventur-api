from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from rest_framework import serializers

from .models import User


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = User
        exclude = ('password', )
        read_only_fields = ('pk', )


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password = serializers.CharField(required=True, write_only=True)

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

    def create(self, validated_data):
        User = get_user_model()
        password = validated_data.pop('password', None)
        user = User(
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', '')
        )
        user.set_password(password)
        user.save()
        return user

    def save(self, request=None):
        return super(RegisterSerializer, self).save()