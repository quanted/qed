"""
Django settings for UberDjango project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import socket
import sys


# Get machine IP address
MACHINE_ID = socket.gethostname()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_ROOT = os.path.join(PROJECT_ROOT, 'templates_qed/') #.replace('\\','/'))

# Define ENVIRONMENTAL VARIABLES for project (replaces the app.yaml)
os.environ.update({
    'REST_SERVER_8': 'http://172.20.100.18',
    'PROJECT_PATH': PROJECT_ROOT,
    'SITE_SKIN': 'EPA',                          # Leave empty ('') for default skin, 'EPA' for EPA skin
    'CONTACT_URL': 'https://www.epa.gov/research/forms/contact-us-about-epa-research',

    # cts_api addition:
    'CTS_EPI_SERVER': 'http://172.20.100.18',
    'CTS_EFS_SERVER': 'http://172.20.100.12',
    'CTS_JCHEM_SERVER': 'http://172.20.100.12',
    'CTS_SPARC_SERVER': 'http://204.46.160.69:8080',
    'CTS_TEST_SERVER': 'http://172.20.100.16:8080'
    #'CTS_TEST_SERVER': 'http://134.67.114.6:8080',
    #'CTS_EPI_SERVER': 'http://134.67.114.8',
    #'CTS_JCHEM_SERVER': 'http://134.67.114.2',
    #'CTS_EFS_SERVER': 'http://134.67.114.2',
    #'CTS_SPARC_SERVER': 'http://204.46.160.69:8080',
    'CTS_VERSION': '1.8'
})

# cts_api addition:
NODEJS_HOST = 'nginx'
NODEJS_PORT = 80
# todo: look into ws w/ django 1.10

if not os.environ.get('UBERTOOL_REST_SERVER'):
    os.environ.update({'UBERTOOL_REST_SERVER': 'http://nginx:7777'})  # Docker network
    print("REST backend = http://nginx:7777")

# SECURITY WARNING: keep the secret key used in production secret!
#http://stackoverflow.com/questions/15170637/effects-of-changing-djangos-secret-key
with open('./secret_key_django_dropbox.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []
if MACHINE_ID == "ord-uber-vm001":
    ALLOWED_HOSTS.append('134.67.114.1')
    ALLOWED_HOSTS.append('qedinternal.epa.gov')
elif MACHINE_ID == "ord-uber-vm003":
    ALLOWED_HOSTS.append('134.67.114.3')
    ALLOWED_HOSTS.append('qed.epa.gov')
else:
    ALLOWED_HOSTS.append('192.168.99.100')  # Docker Machine IP (generally, when using VirtualBox VM)
    ALLOWED_HOSTS.append('134.67.114.3')    # CGI NAT address (mapped to 'qed.epa.gov')
    ALLOWED_HOSTS.append('134.67.114.1')

print("MACHINE_ID = {}").format(MACHINE_ID)


# Disable this because Django wants to email errors and there is no email server set up
# ADMINS = (
#     ('Ubertool Dev Team', 'ubertool-dev@googlegroups.com')
# )

APPEND_SLASH = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(TEMPLATE_ROOT, 'splash'),
                 os.path.join(TEMPLATE_ROOT, 'drupal_2017'),
                 os.path.join(TEMPLATE_ROOT, 'cts'),
                 os.path.join(TEMPLATE_ROOT, 'drupal_2014'),
                 os.path.join(TEMPLATE_ROOT, 'uber2017'),
                 os.path.join(TEMPLATE_ROOT, 'uber2011'),
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

# Application definition

INSTALLED_APPS = (
    'splash_app',
    'ubertool_app',
    #'cts_api',
    #'cts_testing',
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    #'mod_wsgi.server',  # Only needed for mod_wsgi express (Python driver for Apache) e.g. on the production server
    #'docs',
    # 'rest_framework_swagger',
    'cts_app',  # cts django app
    'cts_app.filters',  # cts filters for pchem table
)

## This breaks the pattern of a "pluggable" TEST_CTS django app, but it also makes it convenient to describe the server hosting the TEST API.
#TEST_CTS_PROXY_URL = "http://10.0.2.2:7080/"

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi_docker.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    }
}

# Authentication
AUTH = True
LOGIN_URL = '/ubertool/login'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Setups databse-less test runner (Only needed for running test)
#TEST_RUNNER = 'testing.DatabaselessTestRunner'

# CACHE Setup - required to run Django "sessions" without a database

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake'
#     }
# }
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static_qed'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATIC_URL = '/static_qed/'
STATIC_ROOT = '/src/collected_static/'

#print('BASE_DIR = %s' %BASE_DIR)
print('PROJECT_ROOT = %s' %PROJECT_ROOT)
print('TEMPLATE_ROOT = %s' %TEMPLATE_ROOT)
#print('STATIC_ROOT = %s' %STATIC_ROOT)

# Path to Sphinx HTML Docs
# http://django-docs.readthedocs.org/en/latest/

DOCS_ROOT = os.path.join(PROJECT_ROOT, 'docs', '_build', 'html')
DOCS_ACCESS = 'public'

#try:
#    import settings_local
#    print("Importing additional local settings")
#except ImportError:
#    print("No local settings")
#    pass
