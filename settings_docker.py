"""
Django settings for QED project when running with Docker.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import logging
import os
import socket
from settings import *
from django.conf import settings
# import settings
# from . import settings

print('settings_docker.py')

# Get machine IP address
MACHINE_ID = socket.gethostname()

for key, val in os.environ.items():
    logging.info("QED DJANGO ENV VAR: {}: {}".format(key, val))

# Define ENVIRONMENTAL VARIABLES for project (replaces the app.yaml)
os.environ.update({
    'REST_SERVER_8': 'http://172.20.100.18',
    'PROJECT_PATH': PROJECT_ROOT,
    'SITE_SKIN': 'EPA',  # Leave empty ('') for default skin, 'EPA' for EPA skin
    'CONTACT_URL': 'https://www.epa.gov/research/forms/contact-us-about-epa-research',
    # # # cts_api addition:
    # 'CTS_EPI_SERVER': 'http://172.20.100.18',
    # 'CTS_EFS_SERVER': 'http://172.20.100.12',
    # 'CTS_JCHEM_SERVER': 'http://172.20.100.12',
    # 'CTS_SPARC_SERVER': 'http://204.46.160.69:8080',
    # 'CTS_TEST_SERVER': 'http://172.20.100.16:8080',
    # 'CTS_REST_SERVER': 'http://172.20.100.11', #using qedinternal as proxy for rest server
    # # 'CTS_VERSION': '1.8'  # Now set at settings.py
})

# SECURITY WARNING: don't run with debug turned on in production! (unless you are desperate)
# DEBUG = False
if not os.environ.get('IS_PUBLIC'):
    DEBUG = True
else:
    if os.environ.get('IS_PUBLIC') == "True":
        DEBUG = False
    else:
        DEBUG = True
print("DEBUG: " + str(DEBUG))
TEMPLATE_DEBUG = False

if not os.environ.get('UBERTOOL_REST_SERVER'):
    # Docker network
    os.environ.update({'UBERTOOL_REST_SERVER': 'http://qed_nginx:7777'})
    print("REST backend = http://qed_nginx:7777")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
try:
    #    SECRET_KEY= os.environ.get('DOCKER_SECRET_KEY')
    with open('secrets/secret_key_django_dropbox.txt') as f:
        SECRET_KEY = f.read().strip()
except IOError as e:
    print("Secret file not set as env variable")
    # down_low = 'Shhhhhhhhhhhhhhh'
    # SECRET_KEY = down_low

try:
    HOSTNAME = os.environ.get('DOCKER_HOSTNAME')
    # with open('secret_key_django_dropbox.txt') as f:
    #        SECRET_KEY = f.read().strip()
except IOError as e:
    print("HOSTNAME address not set as env variable")
    HOSTNAME = 'unknown'

# try:
#    with open('my_ip_address.txt') as f:
#	IP_ADDRESS = f.read().strip()
# except IOError as e:
#    print("No IP address given")
#    IP_ADDRESS = '0.0.0.0'



ALLOWED_HOSTS = []
if HOSTNAME == "ord-uber-vm003":
    IS_PUBLIC = True
else:
    IS_PUBLIC = False
if HOSTNAME == "ord-uber-vm001":
    ALLOWED_HOSTS.append('qedinternal.epa.gov')
    ALLOWED_HOSTS.append('134.67.114.1')
    ALLOWED_HOSTS.append('172.20.100.11')
elif HOSTNAME == "ord-uber-vm003":
    ALLOWED_HOSTS.append('134.67.114.3')
    ALLOWED_HOSTS.append('172.20.100.13')
    ALLOWED_HOSTS.append('qed.epa.gov')
elif HOSTNAME == "UberTool-Dev":
    ALLOWED_HOSTS.append('172.16.0.4')
else:
    ALLOWED_HOSTS.append('192.168.99.100')  # Docker Machine IP (generally, when using VirtualBox VM)
    ALLOWED_HOSTS.append('134.67.114.3')  # CGI NAT address (mapped to 'qed.epa.gov')
    ALLOWED_HOSTS.append('134.67.114.1')
    ALLOWED_HOSTS.append('134.67.114.5')
    ALLOWED_HOSTS.append('172.20.100.11')
    ALLOWED_HOSTS.append('172.20.100.13')
    ALLOWED_HOSTS.append('172.20.100.15')
    ALLOWED_HOSTS.append('qedinternal.epa.gov')
    ALLOWED_HOSTS.append('qed.epa.gov')

print("MACHINE_ID = {}".format(MACHINE_ID))
print("HOSTNAME = {}".format(HOSTNAME))
print("IS_PUBLIC = {}".format(IS_PUBLIC))

# Disable this because Django wants to email errors and there is no email server set up
# ADMINS = (
#     ('Ubertool Dev Team', 'ubertool-dev@googlegroups.com')
# )


MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', #rollbar
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', #rollbar
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'login_middleware.RequireLoginMiddleware',
]
# if os.environ.get('IS_PUBLIC') == "True":
#     MIDDLEWARE_CLASSES += ['login_middleware.RequireLoginMiddleware',]


ROOT_URLCONF=__name__, #rollbar

ROLLBAR = {
    'access_token': 'b626ac6c59744e5ba7ddd088a0075893',
    # 'environment': 'development', # if DEBUG else 'production',
    'environment': 'production',
    'branch': 'master',
    'root': '/var/www/qed',
}

ROLLBAR = {
    'access_token': 'POST_SERVER_ITEM_ACCESS_TOKEN',
    'environment': 'production',
    'branch': 'master',
    'root': os.getcwd()
}

## rollbar integration
#settings.configure(
#    DEBUG=True,
#    SECRET_KEY='thisisthesecretkey',
#    ROOT_URLCONF=__name__,
#    ROLLBAR = {
#        'access_token': 'POST_SERVER_ITEM_ACCESS_TOKEN',
#        'environment': 'development',
#        'branch': 'master',
#        'root': os.getcwd()
#    },
#    MIDDLEWARE_CLASSES=(
#        'django.middleware.common.CommonMiddleware',
#        'django.middleware.csrf.CsrfViewMiddleware',
#        'django.middleware.clickjacking.XFrameOptionsMiddleware',###
#
#        # Rollbar middleware
#        'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
#    ),
#)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi_docker.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Authentication
AUTH = False
# Note: env vars in os.environ always strings..
# if os.environ.get('IS_PUBLIC') == "True":
if IS_PUBLIC:
    logging.warning("IS_PUBLIC set to true..")
    MIDDLEWARE += ['login_middleware.RequireLoginMiddleware',]
    AUTH = True
    DEBUG = False

REQUIRE_LOGIN_PATH = '/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = '/src/collected_static/'

# Log to console in Debug mode
if DEBUG:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
    )
