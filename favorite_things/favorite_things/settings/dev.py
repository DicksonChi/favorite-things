from favorite_things.settings.base import *  # NOQA (ignore all errors on this line)
DEBUG = True

PAGE_CACHE_SECONDS = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fav_db',
        'USER': 'admin',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

ALLOWED_HOSTS += ['*']  # NOQA

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {'level': 'DEBUG', 'handlers': ['django_rest_logger_handler']},
    'formatters': {'verbose': {'format': '%(levelname)s %(asctime)s %(module)s ' '%(process)d %(thread)d %(message)s'}},
    'handlers': {
        'django_rest_logger_handler': {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'verbose'}
    },
    'loggers': {
        'django.db.backends': {'level': 'ERROR', 'handlers': ['django_rest_logger_handler'], 'propagate': False},
        'django_rest_logger': {'level': 'DEBUG', 'handlers': ['django_rest_logger_handler'], 'propagate': False},
    },
}

CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}

DEFAULT_LOGGER = 'django_rest_logger'

LOGGER_EXCEPTION = DEFAULT_LOGGER
LOGGER_ERROR = DEFAULT_LOGGER
LOGGER_WARNING = DEFAULT_LOGGER

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
