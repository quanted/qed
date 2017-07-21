"""
WSGI config for UberDjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import django.core.handlers.wsgi
import os
from django.core.wsgi import get_wsgi_application

print('wsgi_local.py')
# Settings.py declaration
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

if os.environ.get('DJANGO_SETTINGS_FILE'):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get('DJANGO_SETTINGS_FILE'))
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_local")


# entry point
app = django.core.handlers.wsgi.WSGIHandler()
application = get_wsgi_application()