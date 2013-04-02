import google.appengine.ext.db as db
from google.appengine.api import users
import datetime
import time
import sys
sys.path.append("ubertool")
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
from utils import json_utils

logger = logging.getLogger("Ubertool")

class UbertoolService(webapp.RequestHandler):
    
    def get(self, ubertool_config_name):
        user = users.get_current_user()
        q = db.Query(Ubertool)
        q.filter('user =',user)
        q.filter('config_name =',ubertool_config_name)
        ubertool = q.get()
        ubertool_dict = {}
        if ubertool != None:
            ubertool_dict['use'] = ubertool.use.config_name
            ubertool_dict['pest'] = ubertool.pest.config_name 
            ubertool_dict['aqua'] = ubertool.aqua.config_name 
            ubertool_dict['eco'] = ubertool.eco.config_name
            ubertool_dict['expo'] = ubertool.expo.config_name 
            ubertool_dict['terra'] = ubertool.terra.config_name 
            ubertool_json = simplejson.dumps(ubertool_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(ubertool_json)

class UbertoolConfigStats(webapp.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        #data = json.loads(self.request.body)
        #data = json_utils.convert(data)
        q = db.Query(Ubertool)
        q.filter('user =',user)
        #include filters for all ubertool config types
        ubertool_stats = {}
        ubertool_stats['use'] = {}
        ubertool_stats['use']['total-nodes'] = 0;
        ubertool_stats['use']['total-links'] = 0;
        ubertool_stats['aquatic'] = {}
        ubertool_stats['aquatic']['total-nodes'] = 0;
        ubertool_stats['aquatic']['total-links'] = 0;
        ubertool_stats['eco'] = {}
        ubertool_stats['eco']['total-nodes'] = 0;
        ubertool_stats['eco']['total-links'] = 0;
        ubertool_stats['expo'] = {}
        ubertool_stats['expo']['total-nodes'] = 0;
        ubertool_stats['expo']['total-links'] = 0;
        ubertool_stats['pest'] = {}
        ubertool_stats['pest']['total-nodes'] = 0;
        ubertool_stats['pest']['total-links'] = 0;
        ubertool_stats['terre'] = {}
        ubertool_stats['terre']['total-nodes'] = 0;
        ubertool_stats['terre']['total-links'] = 0;
        logger.info(q)
        for ubertool in q:
            logger.info(ubertool_stats)
            temp_use_config = ubertool.use.config_name
            temp_pest_config = ubertool.pest.config_name
            temp_aqua_config = ubertool.aqua.config_name
            temp_eco_config = ubertool.eco.config_name
            temp_expo_config = ubertool.expo.config_name
            temp_terra_config = ubertool.terra.config_name
            #Create stats of nodes/links between use and pest
            if temp_use_config in ubertool_stats['use']:
                if temp_pest_config in ubertool_stats['use'][temp_use_config]:
                    ubertool_stats['use'][temp_use_config][temp_pest_config] = ubertool_stats['use'][temp_use_config][temp_pest_config] + 1
                    ubertool_stats['use']['total-links'] = ubertool_stats['use']['total-links'] + 1
                else:
                    ubertool_stats['use'][temp_use_config][temp_pest_config] = 1
                    ubertool_stats['use']['total-links'] = ubertool_stats['use']['total-links'] + 1
            else:
                ubertool_stats['use'][temp_use_config] = {}
                ubertool_stats['use'][temp_use_config][temp_pest_config] = 1
                ubertool_stats['use']['total-nodes'] = ubertool_stats['use']['total-nodes'] + 1
                ubertool_stats['use']['total-links'] = ubertool_stats['use']['total-links'] + 1
            #Create stats of nodes/links between pest and expo
            if temp_pest_config in ubertool_stats['pest']:
                if temp_expo_config in ubertool_stats['pest'][temp_pest_config]:
                    ubertool_stats['pest'][temp_pest_config][temp_expo_config] = ubertool_stats['pest'][temp_pest_config][temp_expo_config] + 1
                    ubertool_stats['pest']['total-links'] = ubertool_stats['pest']['total-links'] + 1
                else:
                    ubertool_stats['pest'][temp_pest_config][temp_expo_config] = 1
                    ubertool_stats['pest']['total-links'] = ubertool_stats['pest']['total-links'] + 1
            else:
                ubertool_stats['pest'][temp_pest_config] = {}
                ubertool_stats['pest'][temp_pest_config][temp_expo_config] = 1
                ubertool_stats['pest']['total-nodes'] = ubertool_stats['pest']['total-nodes'] + 1
                ubertool_stats['pest']['total-links'] = ubertool_stats['pest']['total-links'] + 1
            #Create stats of nodes/links between expo and aqua
            if temp_expo_config in ubertool_stats['expo']:
                if temp_aqua_config in ubertool_stats['expo'][temp_expo_config]:
                    ubertool_stats['expo'][temp_expo_config][temp_aqua_config] = ubertool_stats['expo'][temp_expo_config][temp_aqua_config] + 1
                    ubertool_stats['expo']['total-links'] = ubertool_stats['expo']['total-links'] + 1
                else:
                    ubertool_stats['expo'][temp_expo_config][temp_aqua_config] = 1
                    ubertool_stats['expo']['total-links'] = ubertool_stats['expo']['total-links'] + 1
            else:
                ubertool_stats['expo'][temp_expo_config] = {}
                ubertool_stats['expo'][temp_expo_config][temp_aqua_config] = 1
                ubertool_stats['expo']['total-nodes'] = ubertool_stats['expo']['total-nodes'] + 1
                ubertool_stats['expo']['total-links'] = ubertool_stats['expo']['total-links'] + 1
            #Create stats of nodes/links between aqua and terre
            if temp_aqua_config in ubertool_stats['aquatic']:
                if temp_terra_config in ubertool_stats['aquatic'][temp_aqua_config]:
                    ubertool_stats['aquatic'][temp_aqua_config][temp_terra_config] = ubertool_stats['aquatic'][temp_aqua_config][temp_terra_config] + 1
                    ubertool_stats['aquatic']['total-links'] = ubertool_stats['aquatic']['total-links'] + 1
                else:
                    ubertool_stats['aquatic'][temp_aqua_config][temp_terra_config] = 1
                    ubertool_stats['aquatic']['total-links'] = ubertool_stats['aquatic']['total-links'] + 1
            else:
                ubertool_stats['aquatic'][temp_aqua_config] = {}
                ubertool_stats['aquatic'][temp_aqua_config][temp_terra_config] = 1
                ubertool_stats['aquatic']['total-nodes'] = ubertool_stats['aquatic']['total-nodes'] + 1
                ubertool_stats['aquatic']['total-links'] = ubertool_stats['aquatic']['total-links'] + 1
            #Create stats of nodes/links between terre and eco
            if temp_terra_config in ubertool_stats['terre']:
                if temp_eco_config in ubertool_stats['terre'][temp_terra_config]:
                    ubertool_stats['terre'][temp_terra_config][temp_eco_config] = ubertool_stats['terre'][temp_terra_config][temp_eco_config] + 1
                    ubertool_stats['terre']['total-links'] = ubertool_stats['terre']['total-links'] + 1
                else:
                    ubertool_stats['terre'][temp_terra_config][temp_eco_config] = 1
                    ubertool_stats['terre']['total-links'] = ubertool_stats['terre']['total-links'] + 1
            else:
                ubertool_stats['terre'][temp_terra_config] = {}
                ubertool_stats['terre'][temp_terra_config][temp_eco_config] = 1
                ubertool_stats['terre']['total-nodes'] = ubertool_stats['terre']['total-nodes'] + 1 
                ubertool_stats['terre']['total-links'] = ubertool_stats['terre']['total-links'] + 1              
            #Create stats of nodes in eco
            if temp_eco_config in ubertool_stats['eco']:
                ubertool_stats['eco'][temp_eco_config] = ubertool_stats['eco'][temp_eco_config] + 1
            else:
                ubertool_stats['eco'][temp_eco_config] = {}
                ubertool_stats['eco'][temp_eco_config] = 1
                ubertool_stats['eco']['total-nodes'] = ubertool_stats['eco']['total-nodes'] + 1  
        ubertool_stats_json = simplejson.dumps(ubertool_stats)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(ubertool_stats_json) 
               
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
    
application = webapp.WSGIApplication([('/ubertool/(.*)', UbertoolService),
                                      ('/ubertool-stats', UbertoolConfigStats)],debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()