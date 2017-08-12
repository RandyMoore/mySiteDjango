from .settings import *

# Override base dev settings for production
DEBUG = False
ALLOWED_HOSTS += ['.amazonaws.com','randalmoore.me']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

MEDIA_ROOT = '/var/run/www/media'

if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Self defined settings
PRODUCTION = True
