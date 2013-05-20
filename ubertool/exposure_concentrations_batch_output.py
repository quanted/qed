import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import urllib
from google.appengine.api import urlfetch
import logging
from django.utils import simplejson

logger = logging.getLogger("ExposurConcentrationsBatchOutput")

ubertool_config_service_base_url = os.environ['UBERTOOL_MONGO_SERVER']
    
def batchLoadExposureConcentrationsConfigs(params_matrix,config_index,ubertool_configuration_properties):
    config_params = {}
    config_name = None
    if "exposure_concentrations_config_name" in params_matrix:
        config_name = params_matrix.get("exposure_concentrations_config_name")[config_index]
    if "exposure_concentrations_config_name" in params_matrix:
        config_params['concentration_of_particulate_organic_carbon'] = params_matrix.get("exposure_concentrations_config_name")[config_index]
    if "one_in_ten_peak_exposure_concentration" in params_matrix:
        config_params['one_in_ten_peak_exposure_concentration'] = params_matrix.get("one_in_ten_peak_exposure_concentration")[config_index]            
    if "one_in_ten_four_day_average_exposure_concentration" in params_matrix:
        config_params['one_in_ten_four_day_average_exposure_concentration'] = params_matrix.get("one_in_ten_four_day_average_exposure_concentration")[config_index]            
    if "one_in_ten_twentyone_day_average_exposure_concentration" in params_matrix:
        config_params['one_in_ten_twentyone_day_average_exposure_concentration'] = params_matrix.get("one_in_ten_twentyone_day_average_exposure_concentration")[config_index]            
    if "one_in_ten_sixty_day_average_exposure_concentration" in params_matrix:
        config_params['one_in_ten_sixty_day_average_exposure_concentration'] = params_matrix.get("one_in_ten_sixty_day_average_exposure_concentration")[config_index]  
    if "one_in_ten_ninety_day_average_exposure_concentration" in params_matrix:
        config_params['one_in_ten_ninety_day_average_exposure_concentration'] = params_matrix.get("one_in_ten_ninety_day_average_exposure_concentration")[config_index]  
    if "maximum_peak_exposure_concentration" in params_matrix:
        config_params['maximum_peak_exposure_concentration'] = params_matrix.get("maximum_peak_exposure_concentration")[config_index]  
    if "maximum_four_day_average_exposure_concentration" in params_matrix:
        config_params['maximum_four_day_average_exposure_concentration'] = params_matrix.get("maximum_four_day_average_exposure_concentration")[config_index]
    if "maximum_twentyone_day_average_exposure_concentration" in params_matrix:
        config_params['maximum_twentyone_day_average_exposure_concentration'] = params_matrix.get("maximum_twentyone_day_average_exposure_concentration")[config_index]            
    if "maximum_sixty_day_average_exposure_concentration" in params_matrix:
        config_params['maximum_sixty_day_average_exposure_concentration'] = params_matrix.get("maximum_sixty_day_average_exposure_concentration")[config_index]            
    if "maximum_ninety_day_average_exposure_concentration" in params_matrix:
        config_params['maximum_ninety_day_average_exposure_concentration'] = params_matrix.get("maximum_ninety_day_average_exposure_concentration")[config_index]
    if "pore_water_peak_exposure_concentration" in params_matrix:
        config_params['pore_water_peak_exposure_concentration'] = params_matrix.get("pore_water_peak_exposure_concentration")[config_index]            
    if "pore_water_four_day_average_exposure_concentration" in params_matrix:
        config_params['pore_water_four_day_average_exposure_concentration'] = params_matrix.get("pore_water_four_day_average_exposure_concentration")[config_index]            
    if "pore_water_twentyone_day_average_exposure_concentration" in params_matrix:
        config_params['pore_water_twentyone_day_average_exposure_concentration'] = params_matrix.get("pore_water_twentyone_day_average_exposure_concentration")[config_index]
    if "pore_water_sixty_day_average_exposure_concentration" in params_matrix:
        config_params['pore_water_sixty_day_average_exposure_concentration'] = params_matrix.get("pore_water_sixty_day_average_exposure_concentration")[config_index]            
    if "pore_water_ninety_day_average_exposure_concentration" in params_matrix:
        config_params['pore_water_ninety_day_average_exposure_concentration'] = params_matrix.get("pore_water_ninety_day_average_exposure_concentration")[config_index]            
    
    config_params['exposures_configuration'] = config_name
    ubertool_configuration_properties.update(config_params)
    config_params['config_name'] = config_name
    form_data = simplejson.dumps(config_params)
    url = ubertool_config_service_base_url+"/ubertool/expo/"+config_name
    result = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
    return ubertool_configuration_properties 
                      