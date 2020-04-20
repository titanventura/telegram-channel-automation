import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rpv)s+fo$wd52*zm#q4_8j&n&*ch=7fde+mu!&5az!*p2dd=h*'
# SECURITY WARNING: don't run with debug turned on in production!
IS_PRODUCTION = False
ALLOWED_HOSTS = ['*']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



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

    # Custom Apps in the Project.
    "base_app"
]

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

TIME_ZONE = 'UTC'

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

AUTHENTICATION_BACKENDS = [
 'django.contrib.auth.backends.ModelBackend'
 ]


# A SETTING from the config file that can differentiate between normal authentication and google OAuth.
OAUTH_ENABLED = False
if(os.getenv('GOOGLE_CLIENT_ID')!= '0' and os.getenv('GOOGLE_CLIENT_SECRET')!= '0'):
    oauth_client_id,oauth_client_secret = os.getenv('GOOGLE_CLIENT_ID'),os.getenv('GOOGLE_CLIENT_SECRET')
    OAUTH_ENABLED = True
    AUTHENTICATION_BACKENDS += ['allauth.account.auth_backends.AuthenticationBackend']
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
    INSTALLED_APPS +=[
    "allauth",   # <--
    "allauth.account",   # <--
    "allauth.socialaccount",   # <--
    "allauth.socialaccount.providers.google",   # <--
    ]



API_HASH = os.getenv('TELEGRAM_API_HASH')
API_ID = os.getenv('TELEGRAM_API_ID')
CHANNEL_HASH = os.getenv('CHANNEL_HASH')