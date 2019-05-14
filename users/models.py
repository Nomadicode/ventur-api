import random

from django.db import models
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from rest_framework_jwt.settings import api_settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=256)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=512, unique=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    handle = models.CharField(max_length=128, unique=True, null=True, blank=True)
    profile_picture = models.FileField(upload_to='profile_pictures', null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @staticmethod
    def decode_jwt(jwt):
        if not jwt:
            return AnonymousUser()
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        user_data = jwt_decode_handler(jwt)
        user = User.objects.filter(id=user_data.get('user_id', 0)).first()
        if user:
            return user
        return AnonymousUser()
    
    def get_jwt(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        try:
            payload = jwt_payload_handler(self)
            token = jwt_encode_handler(payload)
        except:
            token = ''
        return token

    def save(self, *args, **kwargs):
        self.email = self.email.lower()

        if 'handle' not in kwargs and not self.handle:
            name_parts = self.name.split(' ')
            self.handle = name_parts[0].lower() + str(random.randint(100, 999))

        return super(User, self).save(*args, **kwargs)
