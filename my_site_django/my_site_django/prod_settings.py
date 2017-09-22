from .settings import *

# Override base dev settings for production
DEBUG = False
ALLOWED_HOSTS += ['.amazonaws.com','randalmoore.me']

if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

STATIC_ROOT = '/var/run/www/static'
# Media files copied over in setup.sh to /var/run/www/media

# Self defined settings
PRODUCTION = True
MAX_QUERY_LENGTH = 80