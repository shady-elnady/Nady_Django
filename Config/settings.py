"""
Django settings for Config project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from decouple import config
import calendar
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

calendar.setfirstweekday(calendar.SATURDAY)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = config('TEMPLATE_DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "herokuapp.com",
]


AUTH_USER_MODEL = "User.User"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    ## Libraries
    'graphene_django',
    'debug_toolbar',
    'django_filters',
    'polymorphic_tree',
    'polymorphic',
    'mptt',
    'django_spaghetti',
    'import_export',
    'djmoney',

    ## My Apps
    "GraphQL",
    "Entity",
    "Unit",
    "Payment",  # ماليات
    "Language",
    "Utils",
    "Location",
    "Facility",  # منشآت
    "Person",
    "Product",
    "Laboratory",
    "Report",
    "Doctor",
    "User",
    "Article",
    "Tool",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'Config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
        ],
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

WSGI_APPLICATION = 'Config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': "Nady_Django",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LANGUAGES = [
    ("ar", _("Arabic")),
    ("en", _("English")),
    ("fr", _("french")),
]


# True for right-to-left languages like Arabic, and to False otherwise
# LANGUAGE_BIDI = False
# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = [
    "ar",
    # "he", "ar-dz", "fa", "ur"
]

# LOCALE_PATHS = (BASE_DIR / "locale/",)
LOCALE_PATHS = [
    BASE_DIR / "Locales/",
    # '/home/www/project/common_files/locale',
    # '/var/local/translations/locale',
]


INTERNAL_IPS = [
    "127.0.0.1",
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / "static",
        # "/var/www/example.com/static/",
    ]
    STATIC_ROOT = BASE_DIR / 'staticFiles'
else:
    STATIC_ROOT = BASE_DIR / "static"


MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Graphene settings
GRAPHENE = {
    "SCHEMA": "GraphQL.schema.schema",
    "MIDDLEWARE": (
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
        "graphene_django.debug.DjangoDebugMiddleware",
    ),
    "SCHEMA_OUTPUT": "schema.graphql",
    "SCHEMA_INDENT": 2,
}

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_EXPIRATION_DELTA": timedelta(days=1),
}


## Money

DEFAULT_CURRENCY= 'EGP'

CURRENCY_MAX_DIGITS= 10

CURRENCY_DECIMAL_PLACES= 2

BASE_CURRENCY= "USD"

##

SPAGHETTI_SAUCE = {
    'apps': [
        'auth',
        "GraphQL",
        "Entity",
        "Unit",
        "Payment",  # ماليات
        "Language",
        "Utils",
        "Location",
        "Facility",  # منشآت
        "Person",
        "Product",
        "Laboratory",
        "Report",
        "Doctor",
        "User",
        "Article",
        "Tool",
    ],
    'show_fields': True,
    'exclude': {
        'auth': ['user'],
    },
}

###
## add New Currency
import moneyed
BOB= moneyed.add_currency( 
    code='BOB',
    numeric='068',
    name='Pesoboliviano',
    countries=('BOLIVIA',),
)



###
LOGIN_URL = reverse_lazy('login')

LOGIN_REDIRECT_URL = reverse_lazy('home')

LOGOUT_REDIRECT_URL = reverse_lazy('login')
