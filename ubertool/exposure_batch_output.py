import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import urllib
from google.appengine.api import urlfetch
import logging
from django.utils import simplejson

logger = logging.getLogger("ExposureBatchOutput")

ubertool_config_service_base_url = os.environ['UBERTOOL_MONGO_SERVER']
    
def batchLoadExposureConcentrationsConfigs(params_matrix,config_index,ubertool_configuration_properties):
    config_params = {}
    config_name = None
    if "exposure_concentrations_config_name" in params_matrix:
        config_name = params_matrix.get("exposure_concentrations_config_name")[config_index]
    if "cas_number" in params_matrix:
        config_params['cas_number'] = params_matrix.get("cas_number")[config_index]            
    if "formulated_product_name" in params_matrix:
        config_params['formulated_product_name'] = params_matrix.get("formulated_product_name")[config_index]            
    if "percent_ai" in params_matrix:
        config_params['percent_ai'] = params_matrix.get("percent_ai")[config_index]            
    if "met_file" in params_matrix:
        config_params['met_file'] = params_matrix.get("met_file")[config_index]  
    if "przm_scenario" in params_matrix:
        config_params['przm_scenario'] = params_matrix.get("przm_scenario")[config_index]  
    if "exams_environment_file" in params_matrix:
        config_params['exams_environment_file'] = params_matrix.get("exams_environment_file")[config_index]              
    if "application_method" in params_matrix:
        config_params['application_method'] = params_matrix.get("application_method")[config_index]
    if "application_type" in params_matrix:
        config_params['application_type'] = params_matrix.get("application_type")[config_index]            
    if "app_type" in params_matrix:
        config_params['app_type'] = params_matrix.get("app_type")[config_index]
    if "weight_of_one_granule" in params_matrix:
        config_params['weight_of_one_granule'] = params_matrix.get("weight_of_one_granule")[config_index]               
    if "wetted_in" in params_matrix:
        config_params['wetted_in'] = params_matrix.get("wetted_in")[config_index]            
    if "incorporation_depth" in params_matrix:
        config_params['incorporation_depth'] = params_matrix.get("incorporation_depth")[config_index]  
    if "percent_incorporated" in params_matrix:
        config_params['percent_incorporated'] = params_matrix.get("percent_incorporated")[config_index]  
    if "application_kg_rate" in params_matrix:
        config_params['application_kg_rate'] = params_matrix.get("application_kg_rate")[config_index]              
    if "application_lbs_rate" in params_matrix:
        config_params['application_lbs_rate'] = params_matrix.get("application_lbs_rate")[config_index]
    if "seed_treatment_formulation_name" in params_matrix:
        config_params['seed_treatment_formulation_name'] = params_matrix.get("seed_treatment_formulation_name")[config_index]            
    if "density_of_product" in params_matrix:
        config_params['density_of_product'] = params_matrix.get("density_of_product")[config_index]            
    if "maximum_seedling_rate_per_use" in params_matrix:
        config_params['maximum_seedling_rate_per_use'] = params_matrix.get("maximum_seedling_rate_per_use")[config_index]            
    if "application_rate_per_use" in params_matrix:
        config_params['application_rate_per_use'] = params_matrix.get("application_rate_per_use")[config_index]  
    if "application_date" in params_matrix:
        config_params['application_date'] = str(params_matrix.get("application_date")[config_index])
    if "number_of_applications" in params_matrix:
        config_params['number_of_applications'] = params_matrix.get("number_of_applications")[config_index]              
    if "interval_between_applications" in params_matrix:
        config_params['interval_between_applications'] = params_matrix.get("interval_between_applications")[config_index]
    if "application_efficiency" in params_matrix:
        config_params['application_efficiency'] = params_matrix.get("application_efficiency")[config_index]            
    if "spray_drift" in params_matrix:
        config_params['spray_drift'] = params_matrix.get("spray_drift")[config_index]            
    if "runoff" in params_matrix:
        config_params['runoff'] = params_matrix.get("runoff")[config_index]     
    if "ar_lb" in params_matrix:
        config_params['ar_lb'] = params_matrix.get("ar_lb")[config_index]
    if "concentration_of_particulate_organic_carbon" in params_matrix:
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
    if "frac_pest_surface" in params_matrix:
        config_params['frac_pest_surface'] = params_matrix.get("frac_pest_surface")[config_index]            
    
    config_params['exposure'] = config_name
    ubertool_configuration_properties.update(config_params)
    config_params['config_name'] = config_name
    form_data = simplejson.dumps(config_params)
    url = ubertool_config_service_base_url+"/ubertool/expo/"+config_name
    result = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
    return ubertool_configuration_properties 
                      