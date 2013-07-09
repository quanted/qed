import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import urllib
from google.appengine.api import urlfetch
import logging
from django.utils import simplejson

logger = logging.getLogger("Use_metadataBatchOutput")

ubertool_config_service_base_url = os.environ['UBERTOOL_MONGO_SERVER']
    
def batchLoadUseConfigs(params_matrix,config_index,ubertool_configuration_properties):
    config_params = {}
    config_name = None
    if "use_metadata_config_name" in params_matrix:
        config_name = params_matrix.get("use_metadata_config_name")[config_index]

          

    config_params['use_metadata_configuration'] = config_name
    ubertool_configuration_properties.update(config_params)
    config_params['config_name'] = config_name
    form_data = simplejson.dumps(config_params)
    url = ubertool_config_service_base_url+"/ubertool/use_metadata/"+config_name
    result = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
    return ubertool_configuration_properties