"""Production settings and globals."""

from os import environ
import os

from base import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

########## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['beta.brandclub.mobi', '162.243.106.173', 'srv1.brandclub.mobi', 'brandclub.mobi', '198.74.61.6']
########## END HOST CONFIGURATION

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION

########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'brandclubdb',
        'USER': 'brandclub',
        'PASSWORD': 'bclub',
        'HOST': '192.168.188.122',
        'PORT': '5432',
    }

}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
########## END CACHE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('SECRET_KEY')
########## END SECRET CONFIGURATION

DEFAULT_CLUSTER_ID = "1"
DEFAULT_DEVICE_ID = "5678"

MEDIA_ROOT = "/var/www/brandclub/media"

RAVEN_CONFIG = {
    'dsn': 'http://b1b3a58559e94dcaae82898beeb049e9:28f2df373fdf4d1e985909dff51a2ad4@monitor.brandclub.mobi/3',
}

INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)

CONTENT_CACHE_DIRECTORY = '/opt/bclub/content'

MEDIA_ROOT = '/opt/bclub/media'

CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'ckeditor')

CACHE_TIME_OUT = 1 * 60

AWS_ACCESS_KEY = 'AKIAIOHZ3UXUTZ6EETWA'

AWS_SECRET_KEY = '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'

BRANDCLUB_HOST = "srv1.brandclub.mobi"

REPORT_DOWNLOAD_PATH = os.path.join(MEDIA_ROOT, 'reports')

AWS_BUCKET_NAME = 'tib.bcng.content'

TIME_ZONE = 'Asia/Calcutta'
API_URL_DOMAIN='http://beta.brandclub.mobi/'