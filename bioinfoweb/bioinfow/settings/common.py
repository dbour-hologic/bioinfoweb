from os.path import abspath, basename, dirname, join, normpath
from os import listdir
from sys import path

# BIOINFORMATICS WEB CONFIGURATION
# ---------------------------------------------------

############# PATH CONFIGURATIONS

# Absolute filesystem path to the config directory
CONFIG_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the project directory
PROJECT_ROOT = dirname(CONFIG_ROOT)

# Absolute filesystem path to the django repo directory
DJANGO_ROOT = dirname(PROJECT_ROOT)

# Project Name
PROJECT_NAME = basename(PROJECT_ROOT).capitalize()

# Project Folder
PROJECT_FOLDER = basename(PROJECT_ROOT)

# Add Project to pythonpath; allows us to not type our
# project name in our dotted import paths:
path.append(CONFIG_ROOT)

############### END PATH CONFIGURATION

DJANGO_APPS = [
	# Default Django Apps
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.humanize',
	'django.contrib.sites',
	'django.contrib.flatpages',
]

LOCAL_APPS = [
	# Custom Django Project Apps (non-third party)
	'portal',
	'services',
	'tech',
	'gparchives',
	'seqconversion',
	'melting',
	'reportbug',
	'feasibility',
	'biomatcher',
	'pqanalysis'
]

THIRD_PARTY_APPS = [
	'markdown_deux',
	'bootstrapform',
	'helpdesk'
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ---------------------------------------------------
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

# GENERAL CONFIGURATION
# ---------------------------------------------------
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# TEMPLATE CONFIGURATION
# ---------------------------------------------------
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			normpath(join(PROJECT_ROOT, 'templates')),
			normpath(join(PROJECT_ROOT, 'extensions')),
		],
		'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',
            ],
            'loaders':[
            	'django.template.loaders.filesystem.Loader',
            	'django.template.loaders.app_directories.Loader',
            ]		
        },
	},
]

# WSGI CONFIGURATION
# ---------------------------------------------------
WSGI_APPLICATION = 'bioinfow.wsgi.application'

# URL CONFIGURATION
# ---------------------------------------------------
ROOT_URLCONF = 'bioinfow.urls'

# MEDIA CONFIGURATION
# ---------------------------------------------------
MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'files', 'media'))
MEDIA_URL = '/media/'

# STATIC FILE CONFIGURATION
# ---------------------------------------------------
STATIC_ROOT = normpath(join(PROJECT_ROOT, 'public'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
	normpath(join(PROJECT_ROOT, 'static')),
)

STATICFILES_FINDERS_IGNORE = [
	'*.scss',
	'*.coffee',
	'*.map',
	'*.html',
	'*.txt',
	'*tests*',
	'*uncompressed*',
]

# The SITE_ID Attribute is used to assign the flat pages
# a main website to attach itself to; you can attach
# multiple websites to a single page ID: i.e.
#
# SITE_ID = 1 - www.site1.com/contact.html
# SITE_ID = 2 - www.site2.com/contact.html
# SITE_ID = 3 - www.site3.com/contact.html
# All use the same /contact.html, but the site ID
# is unique to only ONE of the websites.
# 
# https://docs.djangoproject.com/en/dev/ref/contrib/flatpages/

# Change this to SITE_ID = 1 on the production server
SITE_ID = 3
