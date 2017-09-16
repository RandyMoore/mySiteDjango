from .settings import *

# Override base dev settings for production
DEBUG = True
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

# Self defined settings
PRODUCTION = True
