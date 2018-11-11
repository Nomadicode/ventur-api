"""
Django settings for driftr_api project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import datetime
from configurations import Configuration


class Base(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '(+bpkvj2$j%k8pm7-*(*l@1tnuc&@ds^pmm!evpv(v2-d6rps&'


    # Application definition

    INSTALLED_APPS = [
        # 'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',

        'recurrence',
        'allauth',
        'allauth.socialaccount',
        'allauth.account',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',

        'rest_framework',
        'rest_framework.authtoken',
        'rest_auth',

        'corsheaders',
        'core',
        'users',
        'geo',
        'activities'
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    CORS_ORIGIN_ALLOW_ALL = True

    ROOT_URLCONF = 'api.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'api.wsgi.application'

    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.Argon2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
        'django.contrib.auth.hashers.BCryptPasswordHasher',
    ]

    # Password validation
    # https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]
    # AUTHENTICATION CONFIGURATION
    # ------------------------------------------------------------------------------
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    ]

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        )
    }

    REST_USE_JWT = True
    JWT_AUTH = {
        'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
        'JWT_ALLOW_REFRESH': True,
        'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
    }

    REST_AUTH_REGISTER_SERIALIZERS = {
        'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer',
    }

    REST_AUTH_SERIALIZERS = {
        'USER_DETAILS_SERIALIZER': ('users.serializers.'
                                    'UserDetailsSerializer'),
        # 'PASSWORD_RESET_CONFIRM_SERIALIZER': ('leadtracker.users.serializers.'
        #                                       'PasswordResetConfirmSerializer'),
        # 'PASSWORD_CHANGE_SERIALIZER': ('leadtracker.users.serializers.'
        #                                'PasswordChangeSerializer'),
    }

    REST_SESSION_LOGIN = False

    GRAPHENE = {
        'SCHEMA': 'api.schema.schema'
    }
    
    # Some really nice defaults
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_EMAIL_VERIFICATION = 'optional'
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None

    ACCOUNT_ALLOW_REGISTRATION = True
    # ACCOUNT_ADAPTER = 'klyp_web.users.adapters.AccountAdapter'
    # SOCIALACCOUNT_ADAPTER = 'klyp_web.users.adapters.SocialAccountAdapter'

    SOCIALACCOUNT_PROVIDERS = {
        'facebook': {
            'METHOD': 'oauth2',
            'SCOPE': ['email', 'public_profile', 'user_friends'],
            'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
            'FIELDS': [
                'id',
                'email',
                'name',
                'first_name',
                'last_name',
                'verified',
                'locale',
                'timezone',
                'link',
                'gender',
                'updated_time'],
            'EXCHANGE_TOKEN': True,
            'LOCALE_FUNC': lambda request: 'kr_KR',
            'VERIFIED_EMAIL': False,
            'VERSION': 'v3.1'
        }
    }
    SITE_ID = 1
    # Custom user app defaults
    # Select the correct user model
    AUTH_USER_MODEL = 'users.User'
    LOGIN_REDIRECT_URL = 'users:redirect'
    LOGIN_URL = 'account_login'

    # Internationalization
    # https://docs.djangoproject.com/en/2.1/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.1/howto/static-files/
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'


class Test(Base):
        # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'driftr',
            'USER': 'driftr',
            'PASSWORD': 'testpass',
            'HOST': '127.0.0.1',
            'PORT': '',
        }
    }

    MIGRATION_MODULES = {
        'geo': None
    }

class Local(Base):
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'driftr',
            'USER': 'driftr',
            'PASSWORD': '93zgKhnRsYgmBLssxu6h',
            'HOST': 'dev-db.getdriftr.com',
            'PORT': '',
        }
    }


class Dev(Base):
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ['api-dev.getdriftr.com', '207.246.103.228']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'driftr',
            'USER': 'driftr',
            'PASSWORD': '93zgKhnRsYgmBLssxu6h',
            'HOST': 'dev-db.getdriftr.com',
            'PORT': '',
        }
    }


class Prod(Base):
    DEBUG = False

    ALLOWED_HOSTS = []

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'myproject',
            'USER': 'myprojectuser',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }