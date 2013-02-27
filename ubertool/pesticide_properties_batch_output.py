import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgi
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db
from ubertool import run_ubertool_db
from StringIO import StringIO
import cStringIO
import csv
import sys
sys.path.append("utils")
sys.path.append("./")
from CSVTestParamsLoader import CSVTestParamsLoader
from pesticide_properties import PesticideProperties

class PesticidePropertiesBatchLoader:
    
    def batchLoadPesticidePropertiesConfigs(self,params_matrix):
        params_matrix["PesticideProperties"]=[]
        for pesticide_properties_config_index in range(len(params_matrix.get('molecular_weight'))):
            pesticide_properties_config_name = None
            if "pesticide_properties_config_name" in params_matrix:
                pesticide_properties_config_name = params_matrix.get("pesticide_properties_config_name")[pesticide_properties_config_index]
            molecular_weight = None
            if "molecular_weight" in params_matrix:
                molecular_weight = params_matrix.get("molecular_weight")[pesticide_properties_config_index]            
            henrys_law_constant = None
            if "henrys_law_constant" in params_matrix:
                henrys_law_constant = params_matrix.get("henrys_law_constant")[pesticide_properties_config_index]            
            vapor_pressure = None
            if "vapor_pressure" in params_matrix:
                vapor_pressure = params_matrix.get("vapor_pressure")[pesticide_properties_config_index]            
            solubility = None
            if "solubility" in params_matrix:
                solubility = params_matrix.get("solubility")[pesticide_properties_config_index]  
            Kd = None
            if "Kd" in params_matrix:
                Kd = params_matrix.get("Kd")[pesticide_properties_config_index]  
            Koc = None
            if "Koc" in params_matrix:
                Koc = params_matrix.get("Koc")[pesticide_properties_config_index]  
            photolysis = None
            if "photolysis" in params_matrix:
                photolysis = params_matrix.get("photolysis")[pesticide_properties_config_index]
            aerobic_aquatic_metabolism = None
            if "aerobic_aquatic_metabolism" in params_matrix:
                aerobic_aquatic_metabolism = params_matrix.get("aerobic_aquatic_metabolism")[pesticide_properties_config_index]            
            anaerobic_aquatic_metabolism = None
            if "anaerobic_aquatic_metabolism" in params_matrix:
                anaerobic_aquatic_metabolism = params_matrix.get("anaerobic_aquatic_metabolism")[pesticide_properties_config_index]            
            aerobic_soil_metabolism = None
            if "aerobic_soil_metabolism" in params_matrix:
                aerobic_soil_metabolism = params_matrix.get("aerobic_soil_metabolism")[pesticide_properties_config_index]
            hydrolysis_ph5 = None
            if "hydrolysis_ph5" in params_matrix:
                hydrolysis_ph5 = params_matrix.get("hydrolysis_ph5")[pesticide_properties_config_index]            
            hydrolysis_ph7 = None
            if "hydrolysis_ph7" in params_matrix:
                hydrolysis_ph7 = params_matrix.get("hydrolysis_ph7")[pesticide_properties_config_index]            
            hydrolysis_ph9 = None
            if "hydrolysis_ph9" in params_matrix:
                hydrolysis_ph9 = params_matrix.get("hydrolysis_ph9")[pesticide_properties_config_index]
            foliar_extraction = None
            if "foliar_extraction" in params_matrix:
                foliar_extraction = params_matrix.get("foliar_extraction")[pesticide_properties_config_index]            
            foliar_decay_rate = None
            if "foliar_decay_rate" in params_matrix:
                foliar_decay_rate = params_matrix.get("foliar_decay_rate")[pesticide_properties_config_index]            
            foliar_dissipation_half_life = None
            if "foliar_dissipation_half_life" in params_matrix:
                foliar_dissipation_half_life = params_matrix.get("foliar_dissipation_half_life")[pesticide_properties_config_index]            
            user = users.get_current_user()
            q = db.Query(PesticideProperties)
            if user:
                q.filter('user =',user)
            if pesticide_properties_config_name:
                q.filter("config_name =", pesticide_properties_config_name)
            pests = q.get()
            if pests is None:
                pests = PesticideProperties()
            if user:
                pests.user = user
            pests.config_name = pesticide_properties_config_name
            pests.molecular_weight = molecular_weight
            pests.henrys_law_constant = henrys_law_constant
            pests.vapor_pressure = vapor_pressure
            pests.solubility = solubility   
            pests.Kd = Kd
            pests.Koc = Koc
            pests.photolysis = photolysis
            pests.aerobic_aquatic_metabolism = aerobic_aquatic_metabolism
            pests.anaerobic_aquatic_metabolism = anaerobic_aquatic_metabolism
            pests.aerobic_soil_metabolism = aerobic_soil_metabolism
            pests.hydrolysis_ph5 = hydrolysis_ph5
            pests.hydrolysis_ph7 = hydrolysis_ph7
            pests.hydrolysis_ph9 = hydrolysis_ph9
            pests.foliar_extraction = foliar_extraction
            pests.foliar_decay_rate = foliar_decay_rate
            pests.foliar_dissipation_half_life = foliar_dissipation_half_life
            pests.put()
            params_matrix["PesticideProperties"].append(pests)
        return params_matrix
                
                      