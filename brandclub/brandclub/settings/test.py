from base import *

########## TEST SETTINGS
#TEST_RUNNER = 'discover_runner.DiscoverRunner'
#TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
#TEST_DISCOVER_ROOT = SITE_ROOT
#TEST_DISCOVER_PATTERN = "test_*.py"
########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "brandclub",
        "USER": "sunil",
        "PASSWORD": "root123",
        "HOST": "",
        "PORT": "",
    },
}

CKEDITOR_UPLOAD_PATH = "/home/sunil/brandclub/media/ckeditor/uploads"
DEFAULT_DEVICE_ID = '121'
DEFAULT_CLUSTER_ID = '1'
CREATE_STORE_MAPS = True
CACHE_TIME_OUT = 0
REPORT_DOWNLOAD_PATH = "/home/sunil/brandclub/reporting/downloads"

ALLOWED_HOSTS = ['122.181.186.237', 'test.gobuzz.mobi']
DEBUG = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
CONTENT_CACHE_DIRECTORY = '/home/sunil/content'
LOG_SAVE_PATH = '/home/sunil/brandclub/bc_logs_csv'

AWS_BUCKET_NAME = 'test.bcng.content'
AWS_ACCESS_KEY = 'AKIAIOHZ3UXUTZ6EETWA'
AWS_SECRET_KEY = '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'