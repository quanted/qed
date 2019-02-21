"""
Django settings for qed splash page.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from temp_config.set_environment import DeployEnv

# Determine env vars to use:
runtime_env = DeployEnv()
runtime_env.load_deployment_environment()

print('settings.py')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_ROOT = os.path.join(PROJECT_ROOT, 'templates_qed/') #.replace('\\','/'))
#STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_qed')
#os.path.join(PROJECT_ROOT, 'templates_qed')

# cts_api addition:
NODEJS_HOST = 'nginx'  # default nodejs hostname
NODEJS_PORT = 80  # default nodejs port
# todo: look into ws w/ django 1.10

if not os.environ.get('IS_PUBLIC'):
    DEBUG = True
else:
    if os.environ.get('IS_PUBLIC') == "True":
        DEBUG = False
    else:
        DEBUG = True
print("DEBUG: " + str(DEBUG))
IS_PUBLIC = False
IS_DEVELOPMENT = True

ADMINS = (
    ('Dave Lyons', 'lyons.david@epa.gov'),
    ('Tom Purucker', 'purucker.tom@epa.gov'),
    ('Kurt Wolfe', 'wolfe.kurt@epa.gov'),
    ('Nick Pope', 'i.nickpope@gmail.com'),  # non-epa email ok?
)

APPEND_SLASH = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(TEMPLATE_ROOT, 'api'),
            os.path.join(TEMPLATE_ROOT, 'cts'),
            os.path.join(TEMPLATE_ROOT, 'cyan'),
            os.path.join(TEMPLATE_ROOT, 'drupal_2014'),
            os.path.join(TEMPLATE_ROOT, 'drupal_2017'),
            os.path.join(TEMPLATE_ROOT, 'hem'),
            os.path.join(TEMPLATE_ROOT, 'hms'),
            os.path.join(TEMPLATE_ROOT, 'hwbi'),
            os.path.join(TEMPLATE_ROOT, 'misc'),
            os.path.join(TEMPLATE_ROOT, 'pisces'),
            os.path.join(TEMPLATE_ROOT, 'pop'),
            os.path.join(TEMPLATE_ROOT, 'pram_qaqc_reports'),
            os.path.join(TEMPLATE_ROOT, 'sam'),
            os.path.join(TEMPLATE_ROOT, 'splash'),
            os.path.join(TEMPLATE_ROOT, 'uber2017'),
            os.path.join(TEMPLATE_ROOT, 'uber2011'),
            os.path.join(TEMPLATE_ROOT, 'uberqaqc'),
            os.path.join(TEMPLATE_ROOT, 'nta'),
            os.path.join("/src", "collected_static")
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
    #'cts_api',
    #'cts_testing',
    #'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'mod_wsgi.server',  # Only needed for mod_wsgi express (Python driver for Apache) e.g. on the production server
    # 'docs',
    # 'rest_framework_swagger',
    'cts_app',  # cts django app
    'cts_app.filters',  # cts filters for pchem table
    'cts_app.cts_api',
    'cts_app.cts_testing',
    'cyan_app',  # cyan django app
    # 'hem_app',  # hem django app
    'hms_app',  # hms django app
    'hwbi_app',  # hwbi django app
    'pisces_app',  # pisces django app
    'pram_app',  # pram django app
    #'pop_app',  # pop django app
    #'rest_framework',
    #'sam_app',  # sam django app
    'splash_app',  # splash django app
    # 'ubertool_app',  # ubertool django app
    # 'wqt_app',  # ubertool django app
    'nta_app',
    'corsheaders'
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE_CLASSES = [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

ROOT_URLCONF = 'urls'

ROLLBAR = {
    'access_token': 'b626ac6c59744e5ba7ddd088a0075893',
    # 'environment': 'development', # if DEBUG else 'production',
    'environment': 'development',
    'branch': 'master',
    'root': '/var/www/qed',
}

ROLLBAR = {
    'access_token': 'POST_SERVER_ITEM_ACCESS_TOKEN',
    'environment': 'development',
    'branch': 'master',
    'root': os.getcwd()
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
try:
    with open('secrets/secret_key_database.txt') as f:
        DB_PASS = f.read().strip()
except IOError as e:
    print("secrets/secret_key_database.txt not found!")
    DB_PASS = None

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    },
    'hem_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'hem_app/hem_db.sqlite3'),
    },
    'hwbi_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'hwbi_app/hwbi_db_v2.sqlite3'),
    },
    'pisces_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pisces',
        'USER': 'cgifadmin',
        'PASSWORD': DB_PASS,
        'HOST': '172.20.100.15',
        'PORT': '5432',
    },
    'cyan_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'cyan_app/cyan_web_app_db.sqlite3')
    }
}

DATABASE_ROUTERS = {'routers.HemRouter',
                    'routers.HwbiRouter',
                    'routers.PiscesRouter'}

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

CYAN_ANGULAR_APP_DIR = "static_qed/cyan/webapp"

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static_qed'),
    os.path.join(PROJECT_ROOT, CYAN_ANGULAR_APP_DIR)
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATIC_URL = '/static_qed/'
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_qed')
#print('BASE_DIR = %s' %BASE_DIR)
print('PROJECT_ROOT = {0!s}'.format(PROJECT_ROOT))
print('TEMPLATE_ROOT = {0!s}'.format(TEMPLATE_ROOT))
# print('STATIC_ROOT = %s' %STATIC_ROOT)

# Path to Sphinx HTML Docs
# http://django-docs.readthedocs.org/en/latest/

DOCS_ROOT = os.path.join(PROJECT_ROOT, 'docs', '_build', 'html')
DOCS_ACCESS = 'public'

