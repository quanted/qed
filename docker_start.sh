#!/bin/bash

django-admin.py collectstatic --noinput       # "Collect" static files (--noinput executes the command w/o user interaction)
django-admin.py migrate auth --noinput  # used for login
django-admin.py migrate sessions --noinput   # used for login
exec uwsgi /etc/uwsgi/uwsgi.ini               # Start uWSGI (HTTP router that binds Python WSGI to a web server, e.g. NGINX)

ACCESS_TOKEN=b626ac6c59744e5ba7ddd088a0075893
ENVIRONMENT=production
LOCAL_USERNAME=`puruckertom`
REVISION=`git log -n 1 --pretty=format:"%H"`

curl https://api.rollbar.com/api/1/deploy/ \
  -F access_token=$ACCESS_TOKEN \
  -F environment=$ENVIRONMENT \
  -F revision=$REVISION \
  -F local_username=$LOCAL_USERNAME