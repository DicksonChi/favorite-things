from favorite_things.settings.base import *  # NOQA (ignore all errors on this line)

SECRET_KEY = 'SECRETKEY'  # nosec

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PAGE_CACHE_SECONDS = 60

# TODO: n a real production server this should have a proper url
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


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {'level': 'WARNING', 'handlers': ['sentry']},
    'formatters': {'verbose': {'format': '%(levelname)s %(asctime)s %(module)s ' '%(process)d %(thread)d %(message)s'}},
    'handlers': {
        'sentry': {'level': 'ERROR', 'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler'},
        'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'verbose'},
    },
    'loggers': {
        'django.db.backends': {'level': 'ERROR', 'handlers': ['console'], 'propagate': False},
        'raven': {'level': 'DEBUG', 'handlers': ['sentry'], 'propagate': False},
        'sentry.errors': {'level': 'DEBUG', 'handlers': ['sentry'], 'propagate': False},
    },
}

DEFAULT_LOGGER = 'raven'

LOGGER_EXCEPTION = DEFAULT_LOGGER
LOGGER_ERROR = DEFAULT_LOGGER
LOGGER_WARNING = DEFAULT_LOGGER


# main accounts
EMF_COLLECTION_ACCOUNT_NAME = 'EMFCOLLECTIONACCOUNTNAME'
EMF_COLLECTION_ACCOUNT_NUMBER = 'EMFCOLLECTIONACCOUNTNUMBER'
EMF_COLLECTION_BANK = 'EMFCOLLECTIONBANK'
DF_COLLECTION_ACCOUNT_NAME = 'DFCOLLECTIONACCOUNTNAME'
DF_COLLECTION_ACCOUNT_NUMBER = 'DFCOLLECTIONACCOUNTNUMBER'
DF_COLLECTION_BANK = 'DFCOLLECTIONBANK'

SPARKPOST_API_KEY = 'SPARKPOSTKEY'  # nosec

# AWS
AWS_ACCESS_KEY_ID = 'AWSACCESSKEYID'  # nosec
AWS_SECRET_ACCESS_KEY = 'AWSSECRETACCESSKEY'  # nosec
AWS_STORAGE_BUCKET_NAME = 'invoizpaid-prod'  # nosec
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)


# TEAM
DEV_TEAM = ['pedro@invoizpaid.com', 'goncalo@invoizpaid.com']
BUSINESS_TEAM = ['seun@invoizpaid.com']
FINANCE_TEAM = ['vivian@invoizpaid.com', 'stephanie@invoizpaid.com']
CEO_EMAIL = ['robert@invoizpaid.com']
COLLECTION_EMAIL = 'collection@invoizpaid.com'
TRANSACTION_EMAIL = 'transactions@invoizpaid.com'

JUMIA_CC = ['vendorfinance.mall.ng@jumia.com']
KONGA_CC = ['sellerservices@konga.com']
TRUST_PILOT_INVITE_EMAIL = ['754848e66d@invite.trustpilot.com']

# ######### CELERY ###########

REDIS_ADDRESS = 'REDISADDRESS'
REDIS_URL = 'redis://{}:6379/0'.format(REDIS_ADDRESS)
CELERY_BROKER_URL = REDIS_URL
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600, 'fanout_prefix': True, 'fanout_patterns': True}  # 1 hour

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
    }
}
