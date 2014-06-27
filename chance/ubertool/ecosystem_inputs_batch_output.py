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
    if "x_poc" in params_matrix:
        config_params['x_poc'] = params_matrix.get("x_poc")[config_index]
    if "x_doc" in params_matrix:
        config_params['x_doc'] = params_matrix.get("x_doc")[config_index]          
    if "c_ox" in params_matrix:
        config_params['c_ox'] = params_matrix.get("c_ox")[config_index]            
    if "w_t" in params_matrix:
        config_params['w_t'] = params_matrix.get("w_t")[config_index]
    if "c_ss" in params_matrix:
        config_params['c_ss'] = params_matrix.get("c_ss")[config_index]
    if "oc" in params_matrix:
        config_params['oc'] = params_matrix.get("oc")[config_index]
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
