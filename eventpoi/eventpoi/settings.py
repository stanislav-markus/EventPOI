"""
Django settings for eventpoi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from photologue import PHOTOLOGUE_APP_DIR

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g#1mdt!7%m_9ic5r3674n(=ieoi+n4r-ok#kkeds^b21nlf2m+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

LOGGING_OUTPUT_ENABLED = DEBUG

ALLOWED_HOSTS = []

ADMINS = (
    ('LikePOI', 'support@likepoi.com'),
)

MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.sites',
    'django.contrib.comments',
    'crispy_forms',
    'registration',
    'tastypie',
    'photologue',
    'sortedm2m',
    'south',
    'core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'eventpoi.urls'

WSGI_APPLICATION = 'eventpoi.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'eventpoi_db',
        'USER': 'eventpoi_user',
        'PASSWORD': '33b5bdfc-a115-4d3f-8416-f4fbb7af9c02',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TASTYPIE_JSON_CACHE = os.path.join(BASE_DIR, 'public', 'cache', 'cache.json')

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '/var/run/redis/redis.sock',
    },
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'eventpoi/static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'eventpoi/templates'),
    PHOTOLOGUE_APP_DIR,
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_REDIRECT_URL = '/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': (
                '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d '
                '%(thread)d %(message)s')
        },
        'simple': {
            'format': (
                '%(name)s %(levelname)s %(filename)s L%(lineno)s: '
                '%(message)s')
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

ACCOUNT_ACTIVATION_DAYS = 2 

EMAIL_PORT = 25
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'likepoi.com'
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-5rnvtc938wlkrx5u0h-x79t4mlcsk3i6'
MAILGUN_SERVER_NAME = 'sandbox8921.mailgun.org'
EMAIL_HOST = 'http://www.likepoi.com'

AUTH_PROFILE_MODULE = "core.UserProfile"

# override this
POSTGIS_VERSION = ( 2, 1, 5 )

HEROKU = False
if HEROKU:
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    ALLOWED_HOSTS = ['*']
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

OPENSHIFT = False
if OPENSHIFT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': os.environ['OPENSHIFT_APP_NAME'],
            'USER': os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
            'PASSWORD':  os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
            'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
            'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
        }
    }

    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'media')
