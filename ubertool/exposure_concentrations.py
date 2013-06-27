import logging
import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

logger = logging.getLogger('ExposureConcentrationsService')
        
class ExposureConcentrations(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    ar_lb = db.FloatProperty()
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
    frac_pest_surface = db.FloatProperty()
    created = db.DateTimeProperty(auto_now_add=True)
