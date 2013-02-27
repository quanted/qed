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
from aquatic_toxicity import AquaticToxicity
import logging

logger = logging.getLogger("AquaToxicity")

class AquaticToxicityBatchLoader:
    
    def batchLoadAquaticToxicityConfigs(self,params_matrix):
        params_matrix["AquaticToxicity"]=[]
        for aqua_config_index in range(len(params_matrix.get('acute_toxicity_target_concentration_for_freshwater_fish'))):
            aquatic_toxicity_config_name = None
            if "aquatic_toxicity_config_name" in params_matrix:
                logger.info(params_matrix.get("aquatic_toxicity_config_name")[aqua_config_index])
                aquatic_toxicity_config_name = params_matrix.get("aquatic_toxicity_config_name")[aqua_config_index]
            acute_toxicity_target_concentration_for_freshwater_fish = None
            if "acute_toxicity_target_concentration_for_freshwater_fish" in params_matrix:
                acute_toxicity_target_concentration_for_freshwater_fish = params_matrix.get("acute_toxicity_target_concentration_for_freshwater_fish")[aqua_config_index]            
            chronic_toxicity_target_concentration_for_freshwater_fish = None
            if "chronic_toxicity_target_concentration_for_freshwater_fish" in params_matrix:
                chronic_toxicity_target_concentration_for_freshwater_fish = params_matrix.get("chronic_toxicity_target_concentration_for_freshwater_fish")[aqua_config_index]            
            acute_toxicity_target_concentration_for_freshwater_invertebrates = None
            if "acute_toxicity_target_concentration_for_freshwater_invertebrates" in params_matrix:
                acute_toxicity_target_concentration_for_freshwater_invertebrates = params_matrix.get("acute_toxicity_target_concentration_for_freshwater_invertebrates")[aqua_config_index]            
            chronic_toxicity_target_concentration_for_freshwater_invertebrates = None
            if "chronic_toxicity_target_concentration_for_freshwater_invertebrates" in params_matrix:
                chronic_toxicity_target_concentration_for_freshwater_invertebrates = params_matrix.get("chronic_toxicity_target_concentration_for_freshwater_invertebrates")[aqua_config_index]  
            toxicity_target_concentration_for_nonlisted_vascular_plants = None
            if "toxicity_target_concentration_for_nonlisted_vascular_plants" in params_matrix:
                toxicity_target_concentration_for_nonlisted_vascular_plants = params_matrix.get("toxicity_target_concentration_for_nonlisted_vascular_plants")[aqua_config_index]  
            toxicity_target_concentration_for_nonlisted_vascular_plants = None
            if "toxicity_target_concentration_for_nonlisted_vascular_plants" in params_matrix:
                toxicity_target_concentration_for_nonlisted_vascular_plants = params_matrix.get("toxicity_target_concentration_for_nonlisted_vascular_plants")[aqua_config_index]  
            toxicity_target_concentration_for_listed_vascular_plants = None
            if "toxicity_target_concentration_for_listed_vascular_plants" in params_matrix:
                toxicity_target_concentration_for_listed_vascular_plants = params_matrix.get("toxicity_target_concentration_for_listed_vascular_plants")[aqua_config_index]  
            toxicity_target_concentration_for_duckweed = None
            if "toxicity_target_concentration_for_duckweed" in params_matrix:
                toxicity_target_concentration_for_duckweed = params_matrix.get("toxicity_target_concentration_for_duckweed")[aqua_config_index]  
            user = users.get_current_user()
            q = db.Query(AquaticToxicity)
            if user:
                q.filter('user =',user)
            if aquatic_toxicity_config_name:
                q.filter("config_name =", aquatic_toxicity_config_name)
            aquatic_toxicity = q.get()
            if aquatic_toxicity is None:
                aquatic_toxicity = AquaticToxicity()
            if user:
                aquatic_toxicity.user = user
            aquatic_toxicity.config_name = aquatic_toxicity_config_name
            logger.info(aquatic_toxicity_config_name)
            aquatic_toxicity.acute_toxicity_target_concentration_for_freshwater_fish = acute_toxicity_target_concentration_for_freshwater_fish
            aquatic_toxicity.chronic_toxicity_target_concentration_for_freshwater_fish = chronic_toxicity_target_concentration_for_freshwater_fish
            aquatic_toxicity.acute_toxicity_target_concentration_for_freshwater_invertebrates = acute_toxicity_target_concentration_for_freshwater_invertebrates
            aquatic_toxicity.chronic_toxicity_target_concentration_for_freshwater_invertebrates = chronic_toxicity_target_concentration_for_freshwater_invertebrates   
            aquatic_toxicity.toxicity_target_concentration_for_nonlisted_vascular_plants = toxicity_target_concentration_for_nonlisted_vascular_plants
            aquatic_toxicity.toxicity_target_concentration_for_listed_vascular_plants = toxicity_target_concentration_for_listed_vascular_plants
            aquatic_toxicity.toxicity_target_concentration_for_duckweed = toxicity_target_concentration_for_duckweed
            aquatic_toxicity.put()
            params_matrix["AquaticToxicity"].append(aquatic_toxicity)
        return params_matrix
                
                      