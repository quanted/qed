import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import sys
sys.path.append("../utils")
sys.path.append('../CAS')
from CAS.CASGql import CASGql
import logging

class Use_metadata(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    created = db.DateTimeProperty(auto_now_add=True)
