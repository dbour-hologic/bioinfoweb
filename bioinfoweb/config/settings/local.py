# settings/local.py
# These settings are for local development only.

from .common import *
from django.core.exceptions import ImproperlyConfigured
import json

# DEBUG Messages On
DEBUG = True

# JSON-based secret module
with open("secrets.json") as f:
	secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
	""" Get the secret variable or return explicit exception """
	try:
		return secrets[setting]
	except KeyError:
		error_msg = "Set the {0} environment variable".format(setting)
		raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")

# Launch the Test Database
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME':'testlaunch',
		'USER':'davidb',
		'PASSWORD':'',
		'HOST':'10.200.254.3',
		'PORT':'5432'
	}
}