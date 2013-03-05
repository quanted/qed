import google.appengine.ext.db as db
import datetime
import time
import logging
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users

class AquaticToxicity(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    acute_toxicity_target_concentration_for_freshwater_fish = db.FloatProperty()
    chronic_toxicity_target_concentration_for_freshwater_fish = db.FloatProperty()
    acute_toxicity_target_concentration_for_freshwater_invertebrates = db.FloatProperty()
    chronic_toxicity_target_concentration_for_freshwater_invertebrates = db.FloatProperty() 
    toxicity_target_concentration_for_nonlisted_vascular_plants = db.FloatProperty()
    toxicity_target_concentration_for_listed_vascular_plants = db.FloatProperty()
    toxicity_target_concentration_for_duckweed = db.FloatProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    
class AquaticToxicityConfigNamesService(webapp.RequestHandler):
    
    def get(self):
        logger = logging.getLogger("AquaticToxicityConfigNamesService")
        user = users.get_current_user()
        q = db.Query(AquaticToxicity)
        q.filter('user =',user)
        aquas = q.run()
        aqua_config_names = []
        for aqua in aquas:
            aqua_config_names.append(aqua.config_name)
        aqua_dict = {}
        aqua_dict['config_names'] = aqua_config_names
        aqua_json = simplejson.dumps(aqua_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(aqua_json)
    
class AquaticToxicityPropertiesRetrievalService(webapp.RequestHandler):
    
    def get(self, aquatic_toxicity_config_name):
        user = users.get_current_user()
        q = db.Query(AquaticToxicity)
        q.filter('user =',user)
        q.filter('config_name =',aquatic_toxicity_config_name)
        aquatic = q.get()
        aquatic_dict = {}
        aquatic_dict['acute_toxicity_target_concentration_for_freshwater_fish'] = aquatic.acute_toxicity_target_concentration_for_freshwater_fish
        aquatic_dict['chronic_toxicity_target_concentration_for_freshwater_fish'] = aquatic.chronic_toxicity_target_concentration_for_freshwater_fish
        aquatic_dict['acute_toxicity_target_concentration_for_freshwater_invertebrates'] = aquatic.acute_toxicity_target_concentration_for_freshwater_invertebrates
        aquatic_dict['chronic_toxicity_target_concentration_for_freshwater_invertebrates'] = aquatic.chronic_toxicity_target_concentration_for_freshwater_invertebrates
        aquatic_dict['toxicity_target_concentration_for_nonlisted_vascular_plants'] = aquatic.toxicity_target_concentration_for_nonlisted_vascular_plants
        aquatic_dict['toxicity_target_concentration_for_listed_vascular_plants'] = aquatic.toxicity_target_concentration_for_listed_vascular_plants
        aquatic_dict['toxicity_target_concentration_for_duckweed'] = aquatic.toxicity_target_concentration_for_duckweed
        return aquatic_dict
    
application = webapp.WSGIApplication([('/aqua-config-names', AquaticToxicityConfigNamesService)],
                                      debug=True)
def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
