import logging
import os
import sys
from pathlib import Path
from datetime import datetime

# Connect to Elasticsearch


from decouple import config

from biller.config import Configurations

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Configurations.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = Configurations.debug

ALLOWED_HOSTS = ['*']

URLS_ALLOW_ANONYMOUS = ['/auth/login/', '/auth/token/', '/api/schema/', '/api/schema/redoc/', '/api/schema/swagger-ui/',
                        '/auth/register/', '/auth/forgot_password/', '/auth/email_verify/']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    #'minio_storage',
    'corsheaders',
    'behave_django',
    'biller_apps.organisation',
    'biller_apps.common',
    'biller_apps.employees',
    'biller_apps.shops',
    'biller_apps.dashboard',
    'biller_apps.item',
    'biller_apps.supplier',
    'biller_apps.brand',
    'biller_apps.category',
    'biller_apps.status',
    'biller_apps.billing',
    'biller_apps.places',
    'biller_apps.storage',
    'biller_apps.customer',
    'biller_apps.approvals',
    'biller_apps.taxes',
    'biller_apps.purchase',
    'biller_apps.return_purchase',
    'biller_apps.stock_transfer',
    'biller_apps.return_item',
    'biller_apps.quotations',
    'biller_apps.pos',
    'biller_apps.inventory',
    'biller_apps.general_report',
    'biller_apps.overview_report',
    'biller_apps.admin_report',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'biller_apps.auth.middleware.AuthenticationMiddleware'
]

ROOT_URLCONF = 'biller.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'biller.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DB_HOST = config('DB_HOST', default=None)

if DB_HOST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': DB_HOST,
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }

# Elasticsearch connection. If ELASTIC_SEARCH_URL isn't set (e.g. local dev
# without an ES instance running), this still registers a 'default' alias so
# django-elasticsearch-dsl doesn't KeyError - actual search calls degrade to
# empty results instead of crashing (see biller_apps/common/elastich_query.py).
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': config('ELASTIC_SEARCH_URL', default='http://localhost:9200')
    }
}

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'POST',
    'PUT',
    'PATCH'
]

CORS_ALLOW_HEADERS = [
    'Accept',
    'Authorization',
    'Content-Type'
]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'info.log',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'formatter': 'verbose',
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'warning.log',
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['debug_file', 'info_file', 'error_file', 'warning_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    }
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"

    ],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'InWently API',
    'DESCRIPTION': 'OpenApi documentation for InWently APIs',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",  # Assuming you want to store them in a folder named "static" at the project root
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}