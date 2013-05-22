import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import urllib
from google.appengine.api import urlfetch
import logging
from django.utils import simplejson

logger = logging.getLogger("EcoSystemInputsBatchOutput")

ubertool_config_service_base_url = os.environ['UBERTOOL_MONGO_SERVER']

def batchLoadEcosystemInputsConfigs(params_matrix,config_index,ubertool_configuration_properties):
    config_params = {}
    config_name = None
    if "ecosystem_inputs_config_name" in params_matrix:
        config_name = params_matrix.get("ecosystem_inputs_config_name")[config_index]
    if "concentration_of_particulate_organic_carbon" in params_matrix:
        config_params['concentration_of_particulate_organic_carbon'] = params_matrix.get("concentration_of_particulate_organic_carbon")[config_index]
    if "concentration_of_dissolved_organic_carbon" in params_matrix:
        config_params['concentration_of_dissolved_organic_carbon'] = params_matrix.get("concentration_of_dissolved_organic_carbon")[config_index]          
    if "concentration_of_dissolved_oxygen" in params_matrix:
        config_params['concentration_of_dissolved_oxygen'] = params_matrix.get("concentration_of_dissolved_oxygen")[config_index]            
    if "water_temperature" in params_matrix:
        config_params['water_temperature'] = params_matrix.get("water_temperature")[config_index]
    if "concentration_of_suspended_solids" in params_matrix:
        config_params['concentration_of_suspended_solids'] = params_matrix.get("concentration_of_suspended_solids")[config_index]
    if "sediment_organic_carbon" in params_matrix:
        config_params['sediment_organic_carbon'] = params_matrix.get("sediment_organic_carbon")[config_index]
    config_params['ecosystems_configuration'] = config_name
    ubertool_configuration_properties.update(config_params)
    config_params['config_name'] = config_name
    form_data = simplejson.dumps(config_params)
    url = ubertool_config_service_base_url+"/ubertool/eco/"+config_name
    result = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
    return ubertool_configuration_properties
