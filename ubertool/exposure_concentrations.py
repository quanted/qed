import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class ExposureConcentrations(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    one_in_ten_peak_exposure_concentration = db.FloatProperty() 
    one_in_ten_four_day_average_exposure_concentration = db.FloatProperty() 
    one_in_ten_twentyone_day_average_exposure_concentration = db.FloatProperty() 
    one_in_ten_sixty_day_average_exposure_concentration = db.FloatProperty() 
    one_in_ten_ninety_day_average_exposure_concentration = db.FloatProperty() 
    maximum_peak_exposure_concentration = db.FloatProperty() 
    maximum_four_day_average_exposure_concentration = db.FloatProperty() 
    maximum_twentyone_day_average_exposure_concentration = db.FloatProperty() 
    maximum_sixty_day_average_exposure_concentration = db.FloatProperty() 
    maximum_ninety_day_average_exposure_concentration = db.FloatProperty() 
    pore_water_peak_exposure_concentration = db.FloatProperty() 
    pore_water_four_day_average_exposure_concentration = db.FloatProperty() 
    pore_water_twentyone_day_average_exposure_concentration = db.FloatProperty() 
    pore_water_sixty_day_average_exposure_concentration = db.FloatProperty() 
    pore_water_ninety_day_average_exposure_concentration = db.FloatProperty() 
    created = db.DateTimeProperty(auto_now_add=True)
    
class ExposureConcentrationsRetrievalService(webapp.RequestHandler):
    
    def get(self, exposure_concentrations_config_name):
        user = users.get_current_user()
        q = db.Query(ExposureConcentrations)
        q.filter('user =',user)
        q.filter('config_name =',exposure_concentrations_config_name)
        expo = q.get()
        expo_dict = {}
        expo_dict['one_in_ten_peak_exposure_concentration'] = expo.one_in_ten_peak_exposure_concentration
        expo_dict['one_in_ten_four_day_average_exposure_concentration'] = expo.one_in_ten_four_day_average_exposure_concentration
        expo_dict['one_in_ten_twentyone_day_average_exposure_concentration'] = expo.one_in_ten_twentyone_day_average_exposure_concentration
        expo_dict['one_in_ten_sixty_day_average_exposure_concentration'] = expo.one_in_ten_sixty_day_average_exposure_concentration
        expo_dict['one_in_ten_ninety_day_average_exposure_concentration'] = expo.one_in_ten_ninety_day_average_exposure_concentration
        expo_dict['maximum_peak_exposure_concentration'] = expo.maximum_peak_exposure_concentration
        expo_dict['maximum_four_day_average_exposure_concentration'] = expo.maximum_four_day_average_exposure_concentration
        expo_dict['maximum_twentyone_day_average_exposure_concentration'] = expo.maximum_twentyone_day_average_exposure_concentration
        expo_dict['maximum_sixty_day_average_exposure_concentration'] = expo.maximum_sixty_day_average_exposure_concentration
        expo_dict['maximum_ninety_day_average_exposure_concentration'] = expo.maximum_ninety_day_average_exposure_concentration
        expo_dict['pore_water_peak_exposure_concentration'] = expo.pore_water_peak_exposure_concentration
        expo_dict['pore_water_four_day_average_exposure_concentration'] = expo.pore_water_four_day_average_exposure_concentration
        expo_dict['pore_water_twentyone_day_average_exposure_concentration'] = expo.pore_water_twentyone_day_average_exposure_concentration
        expo_dict['pore_water_sixty_day_average_exposure_concentration'] = expo.pore_water_sixty_day_average_exposure_concentration
        expo_dict['pore_water_ninety_day_average_exposure_concentration'] = expo.pore_water_ninety_day_average_exposure_concentration
        return expo_dict