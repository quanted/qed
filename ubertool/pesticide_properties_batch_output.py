import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import urllib
from google.appengine.api import urlfetch
import logging
from django.utils import simplejson

logger = logging.getLogger("PesticidePropertiesBatchOutput")

ubertool_config_service_base_url = os.environ['UBERTOOL_MONGO_SERVER']
    
def batchLoadPesticidePropertiesConfigs(params_matrix,config_index,ubertool_configuration_properties):
    config_params = {}
    config_name = None
    if "pesticide_properties_config_name" in params_matrix:
        config_name = params_matrix.get("pesticide_properties_config_name")[config_index]
    if "molecular_weight" in params_matrix:
        config_params['molecular_weight'] = params_matrix.get("molecular_weight")[config_index] 
    if "henrys_law_constant" in params_matrix:
        config_params['henrys_law_constant'] = params_matrix.get("henrys_law_constant")[config_index]
    if "vapor_pressure" in params_matrix:
        config_params['vapor_pressure'] = params_matrix.get("vapor_pressure")[config_index]     
    if "solubility" in params_matrix:
        config_params['solubility'] = params_matrix.get("solubility")[config_index]  
    if "solubility_ppm" in params_matrix:
        config_params['solubility_ppm'] = params_matrix.get("solubility_ppm")[config_index]   
    if "Kd" in params_matrix:
        config_params['Kd'] = params_matrix.get("Kd")[config_index]                                   
    if "photolysis" in params_matrix:
        config_params['photolysis'] = params_matrix.get("photolysis")[config_index]            
    if "hydrolysis_ph5" in params_matrix:
        config_params['hydrolysis_ph5'] = params_matrix.get("hydrolysis_ph5")[config_index]            
    if "hydrolysis_ph7" in params_matrix:
        config_params['hydrolysis_ph7'] = params_matrix.get("hydrolysis_ph7")[config_index]            
    if "hydrolysis_ph9" in params_matrix:
        config_params['hydrolysis_ph9'] = params_matrix.get("hydrolysis_ph9")[config_index]
    if "l_kow" in params_matrix:
        config_params['l_kow'] = params_matrix.get("l_kow")[config_index]   
    if "k_oc" in params_matrix:
        config_params['k_oc'] = params_matrix.get("k_oc")[config_index]  
    if "c_wdp" in params_matrix:
        config_params['c_wdp'] = params_matrix.get("c_wdp")[config_index] 
    if "water_column_EEC" in params_matrix:
        config_params['water_column_EEC'] = params_matrix.get("water_column_EEC")[config_index] 
                     
    config_params['pest_configuration'] = config_name
    ubertool_configuration_properties.update(config_params)
    config_params['config_name'] = config_name
    form_data = simplejson.dumps(config_params)
    url = ubertool_config_service_base_url+"/ubertool/pest/"+config_name
    result = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
    return ubertool_configuration_properties 