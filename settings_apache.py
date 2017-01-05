"""
Django settings for UberDjango project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import socket


# Get machine IP address
MACHINE_ID = socket.gethostname()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Define ENVIRONMENTAL VARIABLES for project (replaces the app.yaml)
os.environ.update({
    'UBERTOOL_BATCH_SERVER': 'http://uberrest-topknotmeadows.rhcloud.com/',
    'UBERTOOL_MONGO_SERVER': 'http://uberrest-topknotmeadows.rhcloud.com',
    'UBERTOOL_SECURE_SERVER': 'http://uberrest-topknotmeadows.rhcloud.com',
    'REST_SERVER_8': 'http://172.20.100.18',
    'PROJECT_PATH': PROJECT_ROOT,
    'SITE_SKIN': 'EPA',                          # Leave empty ('') for default skin, 'EPA' for EPA skin
    'CONTACT_URL': 'https://www.epa.gov/research/forms/contact-us-about-epa-research',
    'CTS_EPI_SERVER': 'http://172.20.100.18',
    'CTS_EFS_SERVER': 'http://172.20.100.12',
    'CTS_JCHEM_SERVER': 'http://172.20.100.12',
    'CTS_SPARC_SERVER': 'http://204.46.160.69:8080',
    'CTS_TEST_SERVER': 'http://172.20.100.16:8080'
})
if not os.environ.get('UBERTOOL_REST_SERVER'):
    os.environ.update({'UBERTOOL_REST_SERVER': 'http://172.20.100.15:7777'})  # CGI Internal
    print("REST backend = {}".format(os.environ.get('UBERTOOL_REST_SERVER')))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!  <-- We do not use this for anything
# try:
#     import secret
#     SECRET_KEY = secret.SECRET_KEY
# except ImportError:
#     SECRET_KEY = "ShhhDontTellAnyone"

# SECURITY WARNING: keep the secret key used in production secret!
with open('splash_app/secret_key_django_dropbox.txt') as f:
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

# Disable this because Django wants to email errors and there is no email server set up
# ADMINS = (
#     ('Ubertool Dev Team', 'ubertool-dev@googlegroups.com')
# )

APPEND_SLASH = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
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
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'mod_wsgi.server',
    'docs',
    'api',
    'models.terrplant',
    'models.sip',
    'models.stir',
    'models.trex',
    'models.therps',
    'models.iec',
    'models.earthworm',
    'models.rice',
    'models.kabam',
    'models.ore',
    'models.hwbi',
    'cts_api'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi_apache.application'


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
TEST_RUNNER = 'testing.DatabaselessTestRunner'

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
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/ubertool/static/'

# print 'BASE_DIR = %s' %BASE_DIR
# print 'PROJECT_ROOT = %s' %PROJECT_ROOT

# Path to Sphinx HTML Docs
# http://django-docs.readthedocs.org/en/latest/

DOCS_ROOT = os.path.join(PROJECT_ROOT, 'docs', '_build', 'html')

DOCS_ACCESS = 'public'


#### APACHE TESTING ####
#print "PROJECT_PATH", os.environ['PROJECT_PATH']
#print "__name__ =", __name__
#print "__file__ =", __file__
#print "os.getpid() =", os.getpid()
#print "os.getcwd() =", os.getcwd()
#print "os.curdir =", os.curdir
#print "sys.path =", repr(sys.path)
#print "sys.modules.keys() =", repr(sys.modules.keys())
#print "sys.modules.has_key('ubertool_eco') =", sys.modules.has_key('ubertool_eco')

#if sys.modules.has_key('ubertool_eco'):
#    print "sys.modules['ubertool_eco'].__name__ =", sys.modules['ubertool_eco'].__name__
#    print "sys.modules['ubertool_eco'].__file__ =", sys.modules['ubertool_eco'].__file__
#    print "os.environ['DJANGO_SETTINGS_MODULE'] =", os.environ.get('DJANGO_SETTINGS_MODULE', None)
