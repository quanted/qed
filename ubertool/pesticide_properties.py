import google.appengine.ext.db as db
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import sys
import logging

class PestService(webapp.RequestHandler):
    
    def get(self, use_config_name):
        logger = logging.getLogger("PestService")
        user = users.get_current_user()
        q = db.Query(PesticideProperties)
        q.filter('user =',user)
        q.filter('config_name =',use_config_name)
        pest = q.get()
        pest_dict = {}
        pest_dict['molecular_weight'] = pest.molecular_weight
        pest_dict['henrys_law_constant'] = pest.henrys_law_constant
        pest_dict['vapor_pressure'] = pest.vapor_pressure
        pest_dict['solubility'] = pest.solubility
        pest_dict['Kd'] = pest.Kd
        pest_dict['Koc'] = pest.Koc
        pest_dict['photolysis'] = pest.photolysis
        pest_dict['aerobic_aquatic_metabolism'] = pest.aerobic_aquatic_metabolism
        pest_dict['anaerobic_aquatic_metabolism'] = pest.anaerobic_aquatic_metabolism
        pest_dict['aerobic_soil_metabolism'] = pest.aerobic_soil_metabolism
        pest_dict['hydrolysis_ph5'] = pest.hydrolysis_ph5
        pest_dict['hydrolysis_ph7'] = pest.hydrolysis_ph7
        pest_dict['hydrolysis_ph9'] = pest.hydrolysis_ph9
        pest_dict['foliar_extraction'] = pest.foliar_extraction
        pest_dict['foliar_decay_rate'] = pest.foliar_decay_rate
        pest_dict['foliar_dissipation_half_life'] = pest.foliar_dissipation_half_life
        logger.info(pest_dict)
        pest_json = simplejson.dumps(pest_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(pest_json)

class PesticideProperties(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    molecular_weight = db.FloatProperty()
    henrys_law_constant = db.FloatProperty()
    vapor_pressure = db.FloatProperty()
    solubility = db.FloatProperty()
    Kd = db.FloatProperty()
    Koc = db.FloatProperty() 
    photolysis = db.FloatProperty()
    aerobic_aquatic_metabolism = db.FloatProperty()
    anaerobic_aquatic_metabolism = db.FloatProperty()
    aerobic_soil_metabolism = db.FloatProperty() 
    hydrolysis_ph5 = db.FloatProperty()
    hydrolysis_ph7 = db.FloatProperty()
    hydrolysis_ph9 = db.FloatProperty()
    foliar_extraction = db.FloatProperty()
    foliar_decay_rate = db.FloatProperty()
    foliar_dissipation_half_life = db.FloatProperty()
    created = db.DateTimeProperty(auto_now_add=True)

application = webapp.WSGIApplication([('/pest/(.*)', PestService)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()