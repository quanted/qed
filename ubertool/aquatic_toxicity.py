import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class AquaticToxicityService(webapp.RequestHandler):
    def get(self, aqua_toxicity):
        user = users.get_current_user()
        q = db.Query(AquaticToxicity)
        q.filter('user =',user)
        q.filter('config_name =',aqua_toxicity)
        aqua = q.get()
        use_dict = {}
        use_dict['acute_toxicity_target_concentration_for_freshwater_fish']=aqua.acute_toxicity_target_concentration_for_freshwater_fish
        use_dict['chronic_toxicity_target_concentration_for_freshwater_fish']=aqua.chronic_toxicity_target_concentration_for_freshwater_fish
        use_dict['acute_toxicity_target_concentration_for_freshwater_invertebrates']=aqua.acute_toxicity_target_concentration_for_freshwater_invertebrates
        use_dict['chronic_toxicity_target_concentration_for_freshwater_invertebrates']=aqua.chronic_toxicity_target_concentration_for_freshwater_invertebrates
        use_dict['toxicity_target_concentration_for_nonlisted_vascular_plants']=aqua.toxicity_target_concentration_for_nonlisted_vascular_plants
        use_dict['toxicity_target_concentration_for_listed_vascular_plants']=aqua.toxicity_target_concentration_for_listed_vascular_plants
        use_dict['toxicity_target_concentration_for_duckweed']=aqua.toxicity_target_concentration_for_duckweed
        use_json = simplejson.dumps(use_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(use_json)

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
    
application = webapp.WSGIApplication([('/aqua/(.*)', AquaticToxicityService)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()