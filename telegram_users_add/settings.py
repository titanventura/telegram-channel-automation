"""
Django settings for telegram_users_add project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rpv)s+fo$wd52*zm#q4_8j&n&*ch=7fde+mu!&5az!*p2dd=h*'
IS_PRODUCTION = os.environ.get("IS_PRODUCTION", False)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PRODUCTION

ALLOWED_HOSTS = ['*']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SITE_ID = 3

LOGIN_REDIRECT_URL = '/home/'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',    
    
    "social_auth",   # <--
    "base_app",
    "allauth",   # <--
    "allauth.account",   # <--
    "allauth.socialaccount",   # <--
    "allauth.socialaccount.providers.google",   # <--
]

# # ACCOUNT_CONFIRM_EMAIL_ON_GET = False
# ACCOUNT_EMAIL_REQUIRED = True
# # ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# # SOCIALACCOUNT_EMAIL_VERIFICATION = ACCOUNT_EMAIL_VERIFICATION
# ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'telegram_users_add.urls'

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

WSGI_APPLICATION = 'telegram_users_add.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if IS_PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['POSTGRES_USER'],
            'USER': os.environ['POSTGRES_USER'],
            'PASSWORD': os.environ['POSTGRES_PASSWORD'],
            'HOST': 'postgres',
            'PORT': os.environ['POSTGRES_PORT']
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/')
STATICFILES_DIRS = [
    os.path.join('bootstrap'),
    os.path.join('base_app/templates/base_app/bootsnip'),
]

# Media files root and path for file upload

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = (
 'django.contrib.auth.backends.ModelBackend',
 'allauth.account.auth_backends.AuthenticationBackend',
 )

SOCIALACCOUNT_PROVIDERS = {
'google': {
    'SCOPE': [
        'profile',
        'email',
    ],
    'AUTH_PARAMS': {
        'access_type': 'online',
    }
}
}

import sentry_sdk
import logging
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_sdk.init(
    dsn="https://88fa83118b9641b7a4120cf116b61689@o376320.ingest.sentry.io/5196990",
    integrations=[DjangoIntegration(),LoggingIntegration(event_level=logging.ERROR)],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)