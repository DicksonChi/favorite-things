from favorite_things.settings.base import *  # NOQA (ignore all errors on this line)
DEBUG = True

PAGE_CACHE_SECONDS = 1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gxtx=5weofli6n=rt86h=e1p^3kztw@xtu6i@z^t5$k$3e(j(1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
