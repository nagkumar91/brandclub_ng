"""Development settings and globals."""


from os.path import join, normpath

from base import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'brandclub',
        'USER': 'nagkumar',
        'PASSWORD': 'root123',
        'HOST': '',
        'PORT': '',
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


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}
########## END TOOLBAR CONFIGURATION
CKEDITOR_UPLOAD_PATH = "/data/ckeditor/uploads"
DEFAULT_DEVICE_ID = '121'
DEFAULT_CLUSTER_ID = '1'
CREATE_STORE_MAPS = True
CACHE_TIME_OUT = 0
REPORT_DOWNLOAD_PATH = "/data/ckeditor/reporting/downloads"
LOG_SAVE_PATH = "/data/ckeditor/reporting/logs"
TIME_ZONE = 'Asia/Calcutta'
MEDIA_ROOT = '/bclub/media/'
MEDIA_URL = '/bclub/media/'
MAILING_LIST = 'nagkumar@telibrahma.com, prakash@telibrahma.com'
MAILGUN_API_KEY = 'key-1-j3498psszetjazh3-e1o5c6qgn60v4'
MAILGUN_HOST = 'https://api.mailgun.net/v2/sandbox28548.mailgun.org/messages'