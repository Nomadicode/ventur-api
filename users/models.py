from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from rest_framework_jwt.settings import APISettings


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
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=512, unique=True)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_jwt(self):
        jwt_payload_handler = APISettings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = APISettings.JWT_ENCODE_HANDLER
        try:
            payload = jwt_payload_handler(self)
            token = jwt_encode_handler(payload)
        except:
            token = ''
        return token

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super(User, self).save(*args, **kwargs)