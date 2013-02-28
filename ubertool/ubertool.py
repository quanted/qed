import google.appengine.ext.db as db
from google.appengine.api import users
import datetime
import time
from use import Use
from pesticide_properties import PesticideProperties
from aquatic_toxicity import AquaticToxicity
from ecosystem_inputs import EcosystemInputs
from exposure_concentrations import ExposureConcentrations
from terrestrial_toxicity import TerrestrialToxicity
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import logging

logger = logging.getLogger("Ubertool")

class UbertoolService(webapp.RequestHandler):
    
    def get(self, ubertool_config_name):
        user = users.get_current_user()
        q = db.Query(Ubertool)
        q.filter('user =',user)
        q.filter('config_name =',ubertool_config_name)
        ubertool = q.get()
        ubertool_dict = {}
        ubertool_dict['use'] = ubertool.use.config_name
        ubertool_dict['pest'] = ubertool.pest.config_name 
        ubertool_dict['aqua'] = ubertool.aqua.config_name 
        ubertool_dict['eco'] = ubertool.eco.config_name
        ubertool_dict['expo'] = ubertool.expo.config_name 
        ubertool_dict['terra'] = ubertool.terra.config_name 
        ubertool_json = simplejson.dumps(ubertool_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(ubertool_json)

class Ubertool(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    use = db.ReferenceProperty(Use)
    pest = db.ReferenceProperty(PesticideProperties)
    aqua = db.ReferenceProperty(AquaticToxicity)
    eco = db.ReferenceProperty(EcosystemInputs)
    expo = db.ReferenceProperty(ExposureConcentrations)
    terra = db.ReferenceProperty(TerrestrialToxicity)
    created = db.DateTimeProperty(auto_now_add=True)
    
application = webapp.WSGIApplication([('/ubertool/(.*)', UbertoolService)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()