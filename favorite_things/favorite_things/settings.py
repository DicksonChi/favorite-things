"""Django settings for favorite_things project."""

import os
import environ
# Load operating system environment variables and then prepare to use them
env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


ALLOWED_HOSTS = ['localhost:',
                 '127.0.0.1',
                 'https://qv05nxyeec.execute-api.eu-west-3.amazonaws.com']

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (

    'google.com',
    'hostname.example.com',
    'localhost:8000',
    '127.0.0.1:8000'

)


# Application definition

INSTALLED_APPS = [
    # Dependencies
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_extensions',
    'django.contrib.staticfiles',
    'django_s3_storage',
    'zappa_django_utils',

    # App
    'main',

    # rest-framework
    'rest_framework',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'favorite_things.urls'

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
        },
    },
]

REST_FRAMEWORK = {
    # other settings...

    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}

WSGI_APPLICATION = 'favorite_things.wsgi.application'
AUTH_USER_MODEL = 'main.User'
AUTH_PASSWORD_VALIDATORS = []


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# fixtures
FIXTURE_DIR = os.path.join(BASE_DIR, "fixtures")

PAGE_CACHE_SECONDS = 1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': env.db("DB_URL", "psql://USER:PASS@RDS_ENDPOINT:5432/DB_NAME")

}


STATIC_ROOT = os.path.join(BASE_DIR, "static")


ALLOWED_HOSTS += ['*']  # NOQA

AWS_S3_BUCKET_NAME_STATIC = "YOUR OWN BUCKET"
AWS_S3_BUCKET_AUTH_STATIC = True
AWS_ACCESS_KEY_ID = "YOUR SECRET KEY"
AWS_SECRET_ACCESS_KEY = "YOUR SECRET KEY"
AWS_REGION = "YOUR REGION"
STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
AWS_S3_CUSTOM_DOMAIN = "{}.s3.amazonaws.com".format(AWS_S3_BUCKET_NAME_STATIC)
STATIC_URL = "https://{}/".format(AWS_S3_CUSTOM_DOMAIN)
