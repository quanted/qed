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
    concentration_of_particulate_organic_carbon = db.FloatProperty() 
    concentration_of_dissolved_organic_carbon = db.FloatProperty() 
    concentration_of_dissolved_oxygen = db.FloatProperty() 
    water_temperature = db.FloatProperty() 
    concentration_of_suspended_solids = db.FloatProperty() 
    sediment_organic_carbon = db.FloatProperty() 
    created = db.DateTimeProperty(auto_now_add=True)

