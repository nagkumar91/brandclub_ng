"""Common settings and globals."""

from os.path import abspath, basename, dirname, join, normpath
from sys import path


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
from django.core.urlresolvers import reverse_lazy

DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Your Name', 'your_email@example.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'America/Los_Angeles'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r")^35!ziv0f5vn(zj#n^$*p5#*utp&x_fbbnm%%gx8fr9496@9s"
########## END SECRET CONFIGURATION


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
########## END SITE CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'core.proc.brandclub_processor',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'templates')),
    normpath(join(SITE_ROOT, 'core', 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Default Django middleware.
    'core.middleware.XsSharing',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.ClusterDeviceDetectionMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin panel and documentation:

    # 'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    # Database migration helpers:
    'south',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'ckeditor',
    'pipeline',
    'crispy_forms',
    'djcelery',
    'forms_builder.forms',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'core',
    'report',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME
########## END WSGI CONFIGURATION

GRAPPELLI_ADMIN_TITLE = "BrandClub"

GRAPPELLI_INDEX_DASHBOARD = 'brandclub.dashboard.CustomIndexDashboard'

############ BRANDCLUB CONFIGURATION
DEFAULT_DEVICE_ID = '121'
DEFAULT_CLUSTER_ID = '-1'
CREATE_STORE_MAPS = True

CKEDITOR_UPLOAD_PATH = normpath(join(MEDIA_ROOT, 'ckeditor'))
CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'toolbar': 'Basic',
    },
    'default': {
        'toolbar': 'Full',
        'height': 400,
        'width': 750,
    },
}

PIPELINE_JS = {
    'app': {
        'source_filenames': (
          'js/jquery-1.10.2.js',
          'js/bootstrap.js',
          'js/blueimp-gallery.min.js',
          'js/imagesloaded.pkgd.min.js',
          'js/masonry.pkgd.min.js',
          'js/helper.js',
          'js/slideshow.js',
          'js/store.js'
        ),
        'output_filename': 'js/app.min.js',
    }
}

PIPELINE_CSS = {
    'brandclub': {
        'source_filenames': (
            'css/bootstrap.css',
            'css/bootstrap-theme.css',
            'css/blueimp-gallery.css',
            'css/reveal.css',
            'css/project.css',
        ),
        'output_filename': 'css/brandclub.css',
    },
}

STORE_MAPS_DIRECTORY = 'store_maps'

# STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

CACHE_TIME_OUT = 300
CONTENT_CACHE_DIRECTORY = '/tmp/core'
CRISPY_TEMPLATE_PACK = 'bootstrap3'

PIWIK_URL = 'piwik.brandclub.mobi'
PIWIK_SITE_ID = '1'
PIWIK_COOKIE_DOMAIN = "*.beta.brandclub.mobi"
PIWIK_SITE_TOKEN = '663969d8ed74ece3ba288c38b74b0609'
DEFAULT_MAC_ID = "0:0:0:0:0:0:0"

BRANDCLUB_HOST = "localhost"

AWS_ACCESS_KEY = None
AWS_SECRET_KEY = None
REPORT_DOWNLOAD_PATH = "/tmp/reports"
CONTENT_ID_FOR_CLUSTER_HOME = -1
CONTENT_ID_FOR_STORE_HOME = -2
CONTENT_ID_FOR_CLUSTER_INFO = -3
CONTENT_ID_FOR_STORE_INFO = -4
CONTENT_ID_FOR_STORE_FEEDBACK = -5
CONTENT_ID_FOR_OFFERS_PAGE = -6
CONTENT_ID_MAPPING = {-1: "Cluster Home",
                      -2: "Store Home",
                      -3: "Cluster Info",
                      -4: "Store Info",
                      -5: "Store Feedback",
                      -6: "Offers in Cluster"}
CONTENT_ID_ARRAY = [-1, -2, -3, -4, -5, -6]
LOG_SAVE_PATH = "/tmp/bc_logs_csv/"
AWS_BUCKET_NAME = 'tib.bcng.content'
GOOGLE_STATIC_MAP_KEY = 'AIzaSyBOtLGz2PvdRmqZBIVA4fj9VKhk3nyjpk8'
MAILGUN_API_KEY = 'key-1-j3498psszetjazh3-e1o5c6qgn60v4'
MAILGUN_HOST = 'https://api.mailgun.net/v2/sandbox28548.mailgun.org/messages'
MAILING_LIST = 'santosh.s@telibrahma.com, santhosh@telibrahma.com, nagkumar@telibrahma.com, brandclub@telibrahma.com'
FORMS_BUILDER_LABEL_MAX_LENGTH = 100
LOGIN_URL = '/admin/'

API_URL_DOMAIN='http://brandclub.mobi/'
DEFAULT_COUPON_VALUE = 50
DEFAULT_LOYALTY_INCREMENT = 10
SITE_HOST_NAME = "http://brandclub.mobi"
SERVER_NAME_FOR_QR = "brandclub.mobi"
