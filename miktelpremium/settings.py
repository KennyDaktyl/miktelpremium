import os
#import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATICFILES_DIRS = (os.path.join(SITE_ROOT, 'static/'), )

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get('SECRET_KEY')

ACCESS_TOKEN_SMS = os.environ.get('ACCESS_TOKEN_SMS')

ALLOWED_HOSTS = [
    'www.naprawatelefonu.krakow.pl',
    'www.pieczatki24.krakow.pl',
    'www.serwisgsm.krakow.pl',
    'www.miktel.krakow.pl',
    'miktel.krakow.pl',
    'www.tabliczki.krakow.pl',
    'www.immobilizer.krakow.pl',
    'vps689102',
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
    #'django_filters',
    'django_cleanup',
'captcha', 'crispy_forms',
# 'debug_toolbar',
]


CRISPY_TEMPLATE_PACK = 'bootstrap3'

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAP_PUBKEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAP_PRIVKEY')

DJANGO_WYSIWYG_FLAVOR = "yui_advanced"
TINYMCE_DEFAULT_CONFIG = {
    # 'mode':
    # "textareas",
    'theme':
    "advanced",
    'plugins':
    '''pagebreak, style, layer, table, save, advhr, advimage, advlink,
               emotions, iespell, inlinepopups, insertdatetime, preview, media, 
               searchreplace, print, contextmenu, paste, directionality, 
               fullscreen, noneditable, visualchars, nonbreaking, xhtmlxtras, 
               template, wordcount, advlist, autosave''',
    'theme_advanced_buttons1':
    '''bold, italic, underline, strikethrough, |,
                               justifyleft, justifycenter, justifyright,
                               justifyfull, fontselect, fontsizeselect,
                               fullscreen, code''',
    'theme_advanced_buttons2':
    '''bullist, numlist, |, outdent, indent,
                               blockquote, |, undo, redo, |, link, unlink, |,
                               forecolor, backcolor''',
    'theme_advanced_buttons3':
    '''tablecontrols, |, hr, sub, sup, |, charmap''',
    'theme_advanced_toolbar_location':
    "top",
    'theme_advanced_toolbar_align':
    "left",
    'theme_advanced_statusbar_location':
    "bottom",
    'theme_advanced_resizing':
    "true",
    'template_external_list_url':
    "lists/template_list.js",
    'external_link_list_url':
    "lists/link_list.js",
    'external_image_list_url':
    "lists/image_list.js",
    'media_external_list_url':
    "lists/media_list.js",
    'style_formats': [{
        'title': 'Bold text',
        'inline': 'strong'
    }, {
        'title': 'Red text',
        'inline': 'span',
        'styles': {
            'color': '#ff0000'
        }
    }, {
        'title': 'Help',
        'inline': 'strong',
        'classes': 'help'
    }, {
        'title': 'Table styles'
    }, {
        'title': 'Table row 1',
        'selector': 'tr',
        'classes': 'tablerow'
    }],
    'width':
    '700',
    'height':
    '400'
}


SITE_ID=1

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS':
    ['django_filters.rest_framework.DjangoFilterBackend']
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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

#SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
#SESSION_COOKIE_AGE = 3600
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.server458609.nazwa.pl'
EMAIL_HOST_USER="miktelgsm@miktelgsm.pl"
EMAIL_HOST_PASSWORD =os.environ.get("GMAIL_PASSWORD")
EMAIL_PORT = 587
SERVER_EMAIL = EMAIL_HOST_USER

#CACHES = {
#    "default": {
#        "BACKEND": "django_redis.cache.RedisCache",
#        "LOCATION": "redis://127.0.0.1:6379/1",
#        "OPTIONS": {
#            "CLIENT_CLASS": "django_redis.client.DefaultClient",
#        }
#    }
#}
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
#SESSION_CACHE_ALIAS = "default"
#CACHE_TTL = 60 * 15

DATETIME_FORMAT = "Y-m-d H:M:S"
USE_L10N = True
USE_TZ = True
TIME_ZONE = "Poland"

CRISPY_TEMPLATE_PACK = 'bootstrap4'

import socket
if socket.gethostname() == "kenny-N551JX" or socket.gethostname(
) == "vps689102":
    print(socket.gethostname())
    DEBUG =False
    SECURE_SSL_REDIRECT = True
    PREPEND_WWW = True
    STATIC_URL = '/static/'
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
    STATICFILES_DIRS = (os.path.join(SITE_ROOT, "static/"), )

    SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT = os.path.join(BASE_DIR, "static/media/")
    # MEDIA_URL = "static/media/"

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

	#STATICFILES_DIRS = (os.path.join(SITE_ROOT, "static/"), '/home/kenny/Pulpit/HerokuPremium/MiktelHeroku/miktelpremium/static/')
        MEDIA_URL = f'http://127.0.0.1:8000/static/media/'
    if socket.gethostname() == "vps689102":
        DATABASES = {
            "default": {
               # "NAME": "miktel_3",
                "NAME":"miktel_db_5",
                "ENGINE": "django.db.backends.postgresql",
                "USER": os.environ.get('DB_USER'),
                "PASSWORD": os.environ.get('DB_PASSWORD'),
                "HOST": "localhost",
            }
        }
        #STATIC_URL = 'static'
        #STATICFILES_DIRS = (os.path.join(SITE_ROOT, "static"), )
        #STATIC_ROOT = "/home/kenny/www/miktelpremium/staticfiles"
        MEDIA_URL = f'https://www.miktel.krakow.pl/static/media/'



