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
from use import Use
import logging

logger = logging.getLogger("UseBatchLoader")

class UseBatchLoader:
    
    def batchLoadUseConfigs(self,params_matrix):
        params_matrix["Use"]=[]
        for use_config_index in range(len(params_matrix.get('cas_number'))):
            use_config_name = None
            if "use_config_name" in params_matrix:
                use_config_name = params_matrix.get("use_config_name")[use_config_index]
            logger.info(use_config_name)
            cas_number = None
            if "cas_number" in params_matrix:
                cas_number = params_matrix.get("cas_number")[use_config_index]            
            formulated_product_name = None
            if "formulated_product_name" in params_matrix:
                formulated_product_name = params_matrix.get("formulated_product_name")[use_config_index]            
            percent_ai = None
            if "percent_ai" in params_matrix:
                percent_ai = params_matrix.get("percent_ai")[use_config_index]            
            met_file = None
            if "met_file" in params_matrix:
                met_file = params_matrix.get("met_file")[use_config_index]  
            przm_scenario = None
            if "przm_scenario" in params_matrix:
                przm_scenario = params_matrix.get("przm_scenario")[use_config_index]  
            exams_environment_file = None
            if "exams_environment_file" in params_matrix:
                exams_environment_file = params_matrix.get("exams_environment_file")[use_config_index]              
            application_method = None
            if "application_method" in params_matrix:
                application_method = params_matrix.get("application_method")[use_config_index]
            application_type = None
            if "application_type" in params_matrix:
                application_type = params_matrix.get("application_type")[use_config_index]            
            app_type = None
            if "app_type" in params_matrix:
                app_type = params_matrix.get("app_type")[use_config_index]
            weight_of_one_granule = None
            if "weight_of_one_granule" in params_matrix:
                weight_of_one_granule = params_matrix.get("weight_of_one_granule")[use_config_index]               
            wetted_in = None
            if "wetted_in" in params_matrix:
                wetted_in = params_matrix.get("wetted_in")[use_config_index]            
            incorporation_depth = None
            if "incorporation_depth" in params_matrix:
                incorporation_depth = params_matrix.get("incorporation_depth")[use_config_index]  
            percent_incorporated = None
            if "percent_incorporated" in params_matrix:
                percent_incorporated = params_matrix.get("percent_incorporated")[use_config_index]  
            application_kg_rate = None
            if "application_kg_rate" in params_matrix:
                application_kg_rate = params_matrix.get("application_kg_rate")[use_config_index]              
            application_lbs_rate = None
            if "application_lbs_rate" in params_matrix:
                application_lbs_rate = params_matrix.get("application_lbs_rate")[use_config_index]
            seed_treatment_formulation_name = None
            if "seed_treatment_formulation_name" in params_matrix:
                seed_treatment_formulation_name = params_matrix.get("seed_treatment_formulation_name")[use_config_index]            
            density_of_product = None
            if "density_of_product" in params_matrix:
                density_of_product = params_matrix.get("density_of_product")[use_config_index]            
            maximum_seedling_rate_per_use = None
            if "maximum_seedling_rate_per_use" in params_matrix:
                maximum_seedling_rate_per_use = params_matrix.get("maximum_seedling_rate_per_use")[use_config_index]            
            application_rate_per_use = None
            if "application_rate_per_use" in params_matrix:
                application_rate_per_use = params_matrix.get("application_rate_per_use")[use_config_index]  
            application_date = None
            if "application_date" in params_matrix:
                application_date = params_matrix.get("application_date")[use_config_index]  
            number_of_applications = None
            if "number_of_applications" in params_matrix:
                number_of_applications = params_matrix.get("number_of_applications")[use_config_index]              
            interval_between_applications = None
            if "interval_between_applications" in params_matrix:
                interval_between_applications = params_matrix.get("interval_between_applications")[use_config_index]
            application_efficiency = None
            if "application_efficiency" in params_matrix:
                application_efficiency = params_matrix.get("application_efficiency")[use_config_index]            
            spray_drift = None
            if "spray_drift" in params_matrix:
                spray_drift = params_matrix.get("spray_drift")[use_config_index]            
            runoff = None
            if "runoff" in params_matrix:
                runoff = params_matrix.get("runoff")[use_config_index]
            user = users.get_current_user()
            q = db.Query(Use)
            if user:
                q.filter('user =',user)
            if use_config_name:
                q.filter("config_name =", use_config_name)
            use = q.get()
            if use is None:
                use = Use()
            if user:
                use.user = user
            use.config_name = use_config_name
            use.cas_number = cas_number
            use.formulated_product_name = formulated_product_name
            use.percent_ai = percent_ai
            use.met_file = met_file   
            use.przm_scenario = przm_scenario
            use.exams_environment_file = exams_environment_file
            use.application_method = application_method
            use.application_type = application_type
            use.app_type = app_type
            use.weight_of_one_granule = weight_of_one_granule   
            use.wetted_in = wetted_in
            use.incorporation_depth = incorporation_depth
            use.percent_incorporated = percent_incorporated
            use.application_kg_rate = application_kg_rate
            use.application_lbs_rate = application_lbs_rate
            use.seed_treatment_formulation_name = seed_treatment_formulation_name   
            use.density_of_product = density_of_product
            use.maximum_seedling_rate_per_use = maximum_seedling_rate_per_use            
            use.application_rate_per_use = application_rate_per_use
            use.application_date = application_date
            use.number_of_applications = number_of_applications
            use.interval_between_applications = interval_between_applications   
            use.application_date = application_date
            use.application_efficiency = application_efficiency
            use.spray_drift = spray_drift   
            use.runoff = runoff   
            use.put()
            params_matrix["Use"].append(use)
        return params_matrix
                
                      