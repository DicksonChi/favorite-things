from favorite_things.settings.base import *  # NOQA (ignore all errors on this line)

SECRET_KEY = 'SECRETKEY'  # nosec

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PAGE_CACHE_SECONDS = 60

# TODO: in a real production server this should have a proper url
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DBNAMEHERE',
        'USER': 'DBUSERHERE',
        'PASSWORD': 'DBPASSWORDHERE',
        'HOST': 'DBHOSTHERE',
        'PORT': 5432,
    }
}
