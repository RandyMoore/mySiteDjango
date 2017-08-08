import os
from .settings import *

# Override base dev settings for production
DEBUG = False
ALLOWED_HOSTS += ['.amazonaws.com','randalmoore.me']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/run/www/db.sqlite3',
    }
}

MEDIA_ROOT = '/var/run/www/media'

if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']