"""
WSGI config for favorite_things project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "favorite_things.settings")

application = get_wsgi_application()
