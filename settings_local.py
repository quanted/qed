"""
Django settings for QED project when developing.

NOTE: Make sure PyCharm django config is pointing to settings_local.py
instead of settings.py

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from settings import *
import os
import socket
import logging

print('settings_local.py')

# Get machine IP address
MACHINE_ID = "developer"


# Get local machine IP
def get_machine_ip():
    try:
        _MACHINE_ID = socket.gethostname()
        _MACHINE_INFO = socket.gethostbyname_ex(_MACHINE_ID)
        print("Development machine INFO: {}".format(_MACHINE_INFO))
    except:
        print("Unable to get machine IP")
        return None
    _MACHINE_IP = ""
    for ip in _MACHINE_INFO[2]:
        if '192' in ip:
            _MACHINE_IP = ip
    return _MACHINE_IP


MACHINE_IP = get_machine_ip()

# CTS- Boolean for if it's on Nick's local machine or not..
NICK_LOCAL = False

# Define ENVIRONMENTAL VARIABLES
os.environ.update({
    'REST_SERVER_8': 'http://134.67.114.8',  # 'http://localhost:64399'
    'PROJECT_PATH': PROJECT_ROOT,
    'SITE_SKIN': 'EPA',                          # Leave empty ('') for default skin, 'EPA' for EPA skin
    'CONTACT_URL': 'https://www.epa.gov/research/forms/contact-us-about-epa-research',
})

# SECURITY WARNING: don't run with debug turned on in production!
TEMPLATE_DEBUG = False
CSRF_USE_SESSIONS = False

if not os.environ.get('UBERTOOL_REST_SERVER'):
    # Local REST server within epa intranet
    os.environ.update({'UBERTOOL_REST_SERVER': 'http://localhost:7777'})
    print("REST backend = http://localhost:7777")

    # SECURITY WARNING: we keep the secret key in a shared dropbox directory
try:
    with open('secrets/secret_key_django_dropbox.txt') as f:
        SECRET_KEY = f.read().strip()
except IOError as e:
    print("Could not find secret file")
    down_low = 'Shhhhhhhhhhhhhhh'
    SECRET_KEY = down_low

    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        str(MACHINE_IP)
    ]
    print("ALLOWED_HOSTS: {}".format(str(ALLOWED_HOSTS)))

#IS_PUBLIC = True
#IS_PUBLIC = False

WSGI_APPLICATION = 'wsgi_local.application'

DEBUG = True

# Log to console in Debug mode
if DEBUG:
    import logging
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)s %(levelname)s %(message)s',
    )

# Authentication
if os.environ.get('PASSWORD_REQUIRED') == "True":
    logging.warning("Password protection enabled")
    MIDDLEWARE += [
        'login_middleware.RequireLoginMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ]
    AUTH = True

REQUIRE_LOGIN_PATH = '/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
