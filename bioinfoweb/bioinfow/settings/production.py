#settings/production.py
# These settings are for production only.

from .common import *
from django.core.exceptions import ImproperlyConfigured

# DEBUG Messages OFF
DEBUG = False

# ALLOWED_HOSTS
ALLOWED_HOSTS = ["bioinfo-3","bioinfo-3:81"]

# JSON-BASED Secret Module
with open(join(PROJECT_ROOT, "secrets.json")) as f:
	secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
	""" Get the secret variable or return explicit exception """
	try:
		return secrets[setting]
	except KeyError:
		error_msg = "Set the {0} environment variable".format(setting)
		raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME':'bioinfow',
		'USER':'davidb',
		'PASSWORD':'',
		'HOST':'10.200.254.3',
		'PORT':'5432'
	}
}