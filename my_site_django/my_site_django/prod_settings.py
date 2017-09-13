from .settings import *

# Override base dev settings for production
DEBUG = False
ALLOWED_HOSTS += ['.amazonaws.com','randalmoore.me']

if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Self defined settings
PRODUCTION = True
