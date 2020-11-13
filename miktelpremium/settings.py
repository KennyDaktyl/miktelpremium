"""
Django settings for miktelpremium project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import django_heroku
import dj_database_url
import psycopg2

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
# STATICFILES_DIRS = (os.path.join(SITE_ROOT, '/static/'), )

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

ACCESS_TOKEN_SMS = os.environ.get('ACCESS_TOKEN_SMS')
# AWS_DEFAULT_ACL = None
# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = [
    # '10.41.169.187',
    'miktelpremium.herokuapp.com',
    'www.naprawatelefonu.krakow.pl',
    'www.pieczatki24.krakow.pl',
    'www.serwisgsm.krakow.pl',
    'www.miktel.krakow.pl',
    'www.tabliczki.krakow.pl',
    'www.immobilizer.krakow.pl',
    'localhost',
    '127.0.0.1:8000',
    '51.75.127.94',
    'vps689102',
    '*',
    'https://miktelpremium.herokuapp.com'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'miktel',
    'storages',
    'store',
    'boto3',
    'rest_framework',
    'django_filters',
]
SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS':
    ['django_filters.rest_framework.DjangoFilterBackend']
    # "DEFAULT_PERMISSION_CLASSES": [
    #     "rest_framework.authentication.TokenAuthentication",
    #     "rest_framework.authentication.SessionAuthentication",
    # ]
}

MIDDLEWARE = [
    # 'whitenoise.runserver_nostatic',
    # 'django.contrib.staticfiles',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'miktelpremium.urls'

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [os.path.join(SETTINGS_PATH, "templates")],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            "miktel.my_context_processor.sklepy",
            'django.template.context_processors.media',
        ]
    },
}]

WSGI_APPLICATION = 'miktelpremium.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pl'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

AUTH_USER_MODEL = "miktel.MyUser"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static")
LOGIN_URL = "/miktel/login/"

SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 3600

DATETIME_FORMAT = "Y-m-d H:M:S"
USE_L10N = True
USE_TZ = True
TIME_ZONE = "Poland"

CRISPY_TEMPLATE_PACK = 'bootstrap4'
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = 60
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
import socket
if socket.gethostname() == "kenny-N551JX" or socket.gethostname(
) == "vps689102":
    print(socket.gethostname())
    DEBUG = True
    # DEBUG = bool(os.environ.get('DEBUG_VALUE') == True)
    SECURE_SSL_REDIRECT = False
    # import dj_database_url
    # PG_URL = os.environ.get("DATABASE_URL_OVH")
    # DATABASES = {"default": dj_database_url.config(default="")}
    # PG_URL_OVH = os.environ.get("DATABASE_URL_OVH")
    # DATABASES = {"default": dj_database_url.config(default=PG_URL_OVH)}
    STATIC_URL = '/static/'
    STATIC_ROOT = "/home/kenny/www/miktelpremium/static"
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
    STATICFILES_DIRS = (os.path.join(SITE_ROOT, "/static/"), )

    SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT = os.path.join(BASE_DIR, "static/media/")

    if socket.gethostname() == "kenny-N551JX":
        DATABASES = {
            "default": {
                "NAME": "premium03",
                "ENGINE": "django.db.backends.postgresql",
                "USER": os.environ.get('DB_USER'),
                "PASSWORD": os.environ.get('DB_PASSWORD'),
                "HOST": "localhost",
            }
        }

        STATICFILES_DIRS = (os.path.join(
            BASE_DIR, "static/"
        ), '/home/kenny/Pulpit/HerokuPremium/MiktelHeroku/miktelpremium/static/'
                            )
        MEDIA_URL = f'http://127.0.0.1:8000/static/media/'

    if socket.gethostname() == "vps689102":
        DATABASES = {
            "default": {
                "NAME": "miktel_3",
                "ENGINE": "django.db.backends.postgresql",
                "USER": os.environ.get('DB_USER'),
                "PASSWORD": os.environ.get('DB_PASSWORD'),
                "HOST": "localhost",
            }
        }
        PREPEND_WWW = bool(os.environ.get('WWW_REDIRECT') == 'True')
        STATIC_ROOT = "/home/kenny/www/miktelpremium/staticfiles"
        MEDIA_URL = f'https://www.miktel.krakow.pl/static/media/'

else:

    import dj_database_url
    # PG_URL = os.environ.get("DATABASE_URL")
    # DATABASES = {"default": dj_database_url.config(default=PG_URL)}
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            },
        },
    }
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
                'debug':
                DEBUG,
            },
        },
    ]
    # CSRF_COOKIE_SECURE = True
    # SESSION_COOKIE_SECURE = True
    # SECURE_CONTENT_TYPE_NOSNIFF = True
    # SECURE_BROWSER_XSS_FILTER = True
    # SECURE_SSL_REDIRECT = True
    # X_FRAME_OPTIONS = 'DENY'
    # SECURE_HSTS_SECONDS = 60
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # PREPEND_WWW = bool(os.environ.get('WWW_REDIRECT'))
    SECURE_SSL_REDIRECT = True
    DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
    TEMPLATE_DEBUG = False

    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_DIRS = (os.path.join(SITE_ROOT, "static/"), )
    SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    # STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # DEFAULT_FILE_STORAGE = 'miktelpremium.storage_backends.MediaStorage'
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # USE_S3 = os.getenv('USE_S3') == 'FALSE'
    AWS_STORAGE_BUCKET_NAME = 'miktelpremium'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    USE_S3 = os.getenv('USE_S3') == 'TRUE'
    # USE_S3 = os.getenv('USE_S3') == 'FALSE'
    EMAIL_HOST = 'smtp.miktelgsm.nazwa.pl'
    EMAIL_HOST_USER = os.environ.get('GMAIL_PASSWORD')
    EMAIL_HOST_PASSWORD = os.environ.get('GMAIL_USER')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    SERVER_EMAIL = EMAIL_HOST_USER
    if USE_S3:
        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
        AWS_DEFAULT_ACL = 'public-read'
        AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
        AWS_LOCATION = 'media'
        # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        # STATICFILES_STORAGE = 'miktelpremium.storage_backends.MediaStorage'
        # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        MEDIA_ROOT = os.path.join(BASE_DIR, "hello/static/media/")
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    else:
        # DEFAULT_FILE_STORAGE = 'miktelpremium.storage_backends.MediaStorage'
        # STATICFILES_STORAGE = 'miktelpremium.storage_backends.MediaStorage'
        # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        STATIC_URL = '/static/'
        # STATIC_ROOT = os.path.join(BASE_DIR, 'static')
        # STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

        # STATICFILES_DIRS = (os.path.join(SITE_ROOT, "static"), )
        STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"), )
        SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
        SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(BASE_DIR, "static/")
        # MEDIA_URL = "static/media/"
        AWS_LOCATION = 'media'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
        # MEDIA_URL = 'static/media/'
    django_heroku.settings(locals())
# if socket.gethostname() == "miktelpremium.herokuapp.com":
#     PREPEND_WWW = False

# django_heroku.settings(locals())