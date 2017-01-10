#!/bin/bash

django-admin.py collectstatic --noinput       # "Collect" static files (--noinput executes the command w/o user interaction)
exec uwsgi /etc/uwsgi/uwsgi.ini               # Start uWSGI (HTTP router that binds Python WSGI to a web server, e.g. NGINX)