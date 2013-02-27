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
sys.path.append("ubertool")
from CSVTestParamsLoader import CSVTestParamsLoader
from ecosystem_inputs import EcosystemInputs

class EcosystemInputsBatchLoader:
    
    def batchLoadEcosystemInputsConfigs(self,params_matrix):
        params_matrix["EcosystemInputs"]=[]
        for ecosystem_config_index in range(len(params_matrix.get('concentration_of_particulate_organic_carbon'))):
            ecosystem_inputs_config_name = None
            if "ecosystem_inputs_config_name" in params_matrix:
                ecosystem_inputs_config_name = params_matrix.get("ecosystem_inputs_config_name")[ecosystem_config_index]
            concentration_of_particulate_organic_carbon = None
            if "concentration_of_particulate_organic_carbon" in params_matrix:
                concentration_of_particulate_organic_carbon = params_matrix.get("concentration_of_particulate_organic_carbon")[ecosystem_config_index]            
            concentration_of_dissolved_organic_carbon = None
            if "concentration_of_dissolved_organic_carbon" in params_matrix:
                concentration_of_dissolved_organic_carbon = params_matrix.get("concentration_of_dissolved_organic_carbon")[ecosystem_config_index]            
            concentration_of_dissolved_oxygen = None
            if "concentration_of_dissolved_oxygen" in params_matrix:
                concentration_of_dissolved_oxygen = params_matrix.get("concentration_of_dissolved_oxygen")[ecosystem_config_index]            
            water_temperature = None
            if "water_temperature" in params_matrix:
                water_temperature = params_matrix.get("water_temperature")[ecosystem_config_index]  
            concentration_of_suspended_solids = None
            if "concentration_of_suspended_solids" in params_matrix:
                concentration_of_suspended_solids = params_matrix.get("concentration_of_suspended_solids")[ecosystem_config_index]  
            sediment_organic_carbon = None
            if "sediment_organic_carbon" in params_matrix:
                sediment_organic_carbon = params_matrix.get("sediment_organic_carbon")[ecosystem_config_index]  
            user = users.get_current_user()
            q = db.Query(EcosystemInputs)
            if user:
                q.filter('user =',user)
            if ecosystem_inputs_config_name:
                q.filter("config_name =", ecosystem_inputs_config_name)
            ecosystem = q.get()
            if ecosystem is None:
                ecosystem = EcosystemInputs()
            if user:
                ecosystem.user = user
            ecosystem.config_name = ecosystem_inputs_config_name
            ecosystem.concentration_of_particulate_organic_carbon = concentration_of_particulate_organic_carbon
            ecosystem.concentration_of_dissolved_organic_carbon = concentration_of_dissolved_organic_carbon
            ecosystem.concentration_of_dissolved_oxygen = concentration_of_dissolved_oxygen
            ecosystem.water_temperature = water_temperature   
            ecosystem.concentration_of_suspended_solids = concentration_of_suspended_solids
            ecosystem.sediment_organic_carbon = sediment_organic_carbon
            ecosystem.put()
            params_matrix["EcosystemInputs"].append(ecosystem)
        return params_matrix
                
                      