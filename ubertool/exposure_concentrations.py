import logging
import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class ExposureConcentrationsService(webapp.RequestHandler):
    def get(self, expo_concentration):
        user = users.get_current_user()
        q = db.Query(ExposureConcentrations)
        q.filter('user =',user)
        q.filter('config_name =',expo_concentration)
        expo = q.get()
        use_dict = {}
        use_dict['one_in_ten_peak_exposure_concentration']=expo.one_in_ten_peak_exposure_concentration
        use_dict['one_in_ten_four_day_average_exposure_concentration']=expo.one_in_ten_four_day_average_exposure_concentration
        use_dict['one_in_ten_twentyone_day_average_exposure_concentration']=expo.one_in_ten_twentyone_day_average_exposure_concentration
        use_dict['one_in_ten_sixty_day_average_exposure_concentration']=expo.one_in_ten_sixty_day_average_exposure_concentration
        use_dict['one_in_ten_ninety_day_average_exposure_concentration']=expo.one_in_ten_ninety_day_average_exposure_concentration
        use_dict['maximum_peak_exposure_concentration']=expo.maximum_peak_exposure_concentration
        use_dict['maximum_four_day_average_exposure_concentration']=expo.maximum_four_day_average_exposure_concentration
        use_dict['maximum_twentyone_day_average_exposure_concentration']=expo.maximum_twentyone_day_average_exposure_concentration
        use_dict['maximum_sixty_day_average_exposure_concentration']=expo.maximum_sixty_day_average_exposure_concentration
        use_dict['maximum_ninety_day_average_exposure_concentration']=expo.maximum_ninety_day_average_exposure_concentration
        use_dict['pore_water_peak_exposure_concentration']=expo.pore_water_peak_exposure_concentration
        use_dict['pore_water_four_day_average_exposure_concentration']=expo.pore_water_four_day_average_exposure_concentration
        use_dict['pore_water_twentyone_day_average_exposure_concentration']=expo.pore_water_twentyone_day_average_exposure_concentration
        use_dict['pore_water_sixty_day_average_exposure_concentration']=expo.pore_water_sixty_day_average_exposure_concentration
        use_dict['pore_water_ninety_day_average_exposure_concentration']=expo.pore_water_ninety_day_average_exposure_concentration
        use_json = simplejson.dumps(use_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(use_json)
        
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
        expo_dict['config_name'] = expo.config_name
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
    
class ExposureConcentrationsConfigNamesService(webapp.RequestHandler):
    
    def get(self):
        logger = logging.getLogger("ExposureConcentrationsConfigNamesService")
        user = users.get_current_user()
        q = db.Query(ExposureConcentrations)
        q.filter('user =',user)
        expos = q.run()
        expo_config_names = []
        for expo in expos:
            expo_config_names.append(expo.config_name)
        expo_dict = {}
        expo_dict['config_names'] = expo_config_names
        expo_json = simplejson.dumps(expo_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(expo_json)

application = webapp.WSGIApplication([('/expo/(.*)', ExposureConcentrationsService),
										('/expo-config-names', ExposureConcentrationsConfigNamesService)],
                                      debug=True)
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
  	main()