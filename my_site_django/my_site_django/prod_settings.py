from .settings import *

# Override base dev settings for production
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/run/www/db.sqlite3',
    }
}

MEDIA_ROOT = '/var/run/www/media'