import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import urllib
from google.appengine.api import urlfetch
import logging
from django.utils import simplejson

logger = logging.getLogger("AquaToxicityBatchOutput")

ubertool_config_service_base_url = os.environ['UBERTOOL_MONGO_SERVER']

def batchLoadAquaticToxicityConfigs(params_matrix,config_index,ubertool_configuration_properties):
    config_params = {}
    config_name = None
    logger.info("Config Index: %d Type: %s" %(config_index,type(config_index)))
    logger.info("params_matrix:")
    logger.info(params_matrix)
    config_name = params_matrix.get("aquatic_toxicity_config_name")[config_index]
    config_params['acute_toxicity_target_concentration_for_freshwater_fish'] = params_matrix.get("acute_toxicity_target_concentration_for_freshwater_fish")[config_index]            
    config_params['chronic_toxicity_target_concentration_for_freshwater_fish'] = params_matrix.get("chronic_toxicity_target_concentration_for_freshwater_fish")[config_index]            
    config_params['acute_toxicity_target_concentration_for_freshwater_invertebrates'] = params_matrix.get("acute_toxicity_target_concentration_for_freshwater_invertebrates")[config_index]            
    config_params['chronic_toxicity_target_concentration_for_freshwater_invertebrates'] = params_matrix.get("chronic_toxicity_target_concentration_for_freshwater_invertebrates")[config_index]  
    config_params['toxicity_target_concentration_for_nonlisted_vascular_plants'] = params_matrix.get("toxicity_target_concentration_for_nonlisted_vascular_plants")[config_index]  
    config_params['toxicity_target_concentration_for_listed_vascular_plants'] = params_matrix.get("toxicity_target_concentration_for_listed_vascular_plants")[config_index]  
    config_params['toxicity_target_concentration_for_duckweed'] = params_matrix.get("toxicity_target_concentration_for_duckweed")[config_index]  
    config_params['aquatic_configuration'] = config_name
    ubertool_configuration_properties.update(config_params)
    config_params['config_name'] = config_name
    logger.info("config_params:")
    logger.info(config_params)
    form_data = simplejson.dumps(config_params)
    url = ubertool_config_service_base_url+"/ubertool/aqua/"+config_name
    result = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
    return ubertool_configuration_properties