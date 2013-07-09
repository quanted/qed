import logging
import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

logger = logging.getLogger('ExposureConcentrationsService')
        
class Exposure(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    cas_number = db.StringProperty()
    formulated_product_name = db.StringProperty()
    met_file = db.StringProperty()
    przm_scenario = db.StringProperty()
    exams_environment_file = db.StringProperty()
    application_method = db.StringProperty()
    app_type = db.StringProperty()
    weight_of_one_granule = db.FloatProperty()
    wetted_in = db.BooleanProperty()
    incorporation_depth = db.FloatProperty()
    application_kg_rate = db.FloatProperty()
    application_lbs_rate = db.FloatProperty()
    application_rate_per_use = db.FloatProperty()
    application_date = db.DateProperty()
    interval_between_applications = db.FloatProperty()
    application_efficiency = db.FloatProperty()
    spray_drift = db.FloatProperty()
    runoff = db.FloatProperty()
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
