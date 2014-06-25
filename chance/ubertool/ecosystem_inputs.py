import google.appengine.ext.db as db
import datetime
import time
import logging
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class EcosystemInputs(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    x_poc = db.FloatProperty()
    x_doc = db.FloatProperty()
    c_ox = db.FloatProperty() 
    w_t = db.FloatProperty() 
    c_ss = db.FloatProperty() 
    oc = db.FloatProperty()
    created = db.DateTimeProperty(auto_now_add=True)

