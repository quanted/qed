import google.appengine.ext.db as db
from google.appengine.api import users
import datetime
import time
import sys
sys.path.append("../ubertool")
from ubertool.ubertool import Ubertool
from ubertool.use import Use,UsePropertiesRetrievalService
from ubertool.aquatic_toxicity import AquaticToxicity,AquaticToxicityPropertiesRetrievalService
from ubertool.ecosystem_inputs import EcosystemInputs,EcosystemInputsPropertiesRetrievalService
from ubertool.exposure_concentrations import ExposureConcentrations,ExposureConcentrationsRetrievalService
from ubertool.terrestrial_toxicity import TerrestrialToxicity,TerrestrialPropertiesRetrievalService
from ubertool.pesticide_properties import PesticideProperties,PestPropertiesRetrievalService
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import logging

class UbertoolAllPropertiesService(webapp.RequestHandler):
    
    def get(self, ubertool_config_name):
        user = users.get_current_user()
        q = db.Query(Ubertool)
        q.filter('user =',user)
        q.filter('config_name =',ubertool_config_name)
        ubertool = q.get()
        ubertool_dict = {}
        use_dict = {}
        use_service = UsePropertiesRetrievalService()
        use_config_name = ubertool.use.config_name
        use_dict_results = use_service.get(use_config_name)
        if use_dict_results:
            use_dict = use_dict_results
        ubertool_dict['use'] = use_dict
        terra_config_name = ubertool.terra.config_name 
        terra_dict = {}
        terra_service = TerrestrialPropertiesRetrievalService()
        terra_dict_results = terra_service.get(terra_config_name)
        if terra_dict_results:
            terra_dict = terra_dict_results
        ubertool_dict['terra'] = terra_dict
        aqua_config_name = ubertool.aqua.config_name 
        aqua_dict = {}
        aqua_service = AquaticToxicityPropertiesRetrievalService()
        aqua_dict_results = aqua_service.get(aqua_config_name)
        if aqua_dict_results:
            aqua_dict = aqua_dict_results        
        ubertool_dict['aqua'] = aqua_dict
        eco_config_name = ubertool.eco.config_name
        eco_dict = {}
        eco_service = EcosystemInputsPropertiesRetrievalService()
        eco_dict_results = eco_service.get(eco_config_name)
        if eco_dict_results:
            eco_dict = eco_dict_results
        ubertool_dict['eco'] = eco_dict
        expo_config_name = ubertool.expo.config_name
        expo_dict = {}
        expo_service = ExposureConcentrationsRetrievalService()
        expo_dict_results = expo_service.get(expo_config_name)
        if expo_dict_results:
            expo_dict = expo_dict_results
        ubertool_dict['expo'] = expo_dict
        pest_config_name = ubertool.pest.config_name 
        pest_dict = {}
        pest_service = PestPropertiesRetrievalService()
        pest_dict_results = pest_service.get(pest_config_name)
        if pest_dict_results:
            pest_dict = pest_dict_results
        ubertool_dict['pest'] = pest_dict
        ubertool_json = simplejson.dumps(ubertool_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(ubertool_json)
        

class UbertoolConfigNamesService(webapp.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        q = db.Query(Ubertool)
        q.filter('user =',user)
        ubertools = q.run()
        ubertool_config_names = []
        for ubertool in ubertools:
            ubertool_config_names.append(ubertool.config_name)
        ubertool_dict = {}
        ubertool_dict['config_names'] = ubertool_config_names
        ubertool_json = simplejson.dumps(ubertool_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(ubertool_json)

application = webapp.WSGIApplication([('/ubertool/all_props/(.*)', UbertoolAllPropertiesService),
                                      ('/ubertool',UbertoolConfigNamesService)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()        