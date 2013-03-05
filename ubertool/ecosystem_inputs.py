import google.appengine.ext.db as db
import datetime
import time
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
    
class EcosystemInputsPropertiesRetrievalService(webapp.RequestHandler):
    
    def get(self, ecosystem_inputs_config_name):
        user = users.get_current_user()
        q = db.Query(EcosystemInputs)
        q.filter('user =',user)
        q.filter('config_name =',ecosystem_inputs_config_name)
        ecosystem = q.get()
        eco_dict = {}
        eco_dict['concentration_of_particulate_organic_carbon'] = ecosystem.concentration_of_particulate_organic_carbon
        eco_dict['concentration_of_dissolved_organic_carbon'] = ecosystem.concentration_of_dissolved_organic_carbon
        eco_dict['concentration_of_dissolved_oxygen'] = ecosystem.concentration_of_dissolved_oxygen
        eco_dict['water_temperature'] = ecosystem.water_temperature
        eco_dict['concentration_of_suspended_solids'] = ecosystem.concentration_of_suspended_solids
        eco_dict['sediment_organic_carbon'] = ecosystem.sediment_organic_carbon
        return eco_dict