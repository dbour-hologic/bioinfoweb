# settings/production.py
# These settings are for production only.

from .common import *
from django.core.exceptions import ImproperlyConfigured
import json

# DEBUG Messages OFF | Will Keep True Until Media Served Properly
DEBUG = True

# ALLOWED_HOSTS
ALLOWED_HOSTS = ["bioinfo-3", "bioinfo-3:81", "10.200.254.3"]

# JSON-BASED Secret Module
with open(join(PROJECT_ROOT, "secrets.json")) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secret_file=secrets):
    """ Get the secret variable or return explicit exception """
    try:
        return secret_file[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'bioinfow',
    'USER': 'davidb',
    'PASSWORD': '',
    'HOST': '10.200.254.3',
    'PORT': '5432'
  }
}

# MEDIA CONFIGURATION
# ---------------------------------------------------
MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'files', 'media'))
MEDIA_URL = '/media/'
