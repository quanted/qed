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
    if "chemical_name" in params_matrix:
        config_params['chemical_name'] = params_matrix.get("chemical_name")[config_index] 
    if "Formulated_product_name" in params_matrix:
        config_params['Formulated_product_name'] = params_matrix.get("Formulated_product_name")[config_index]
    if "seed_treatment_formulation_name" in params_matrix:
        config_params['seed_treatment_formulation_name'] = params_matrix.get("seed_treatment_formulation_name")[config_index]     
    if "label_epa_reg_no" in params_matrix:
        config_params['label_epa_reg_no'] = params_matrix.get("label_epa_reg_no")[config_index]  
    if "molecular_weight" in params_matrix:
        config_params['molecular_weight'] = params_matrix.get("molecular_weight")[config_index]   
    if "percent_ai" in params_matrix:
        config_params['percent_ai'] = params_matrix.get("percent_ai")[config_index]                         
    if "henrys_law_constant" in params_matrix:
        config_params['henrys_law_constant'] = params_matrix.get("henrys_law_constant")[config_index]            
    if "vapor_pressure" in params_matrix:
        config_params['vapor_pressure'] = params_matrix.get("vapor_pressure")[config_index]            
    if "solubility" in params_matrix:
        config_params['solubility'] = params_matrix.get("solubility")[config_index]  
    if "Kd" in params_matrix:
        config_params['Kd'] = params_matrix.get("Kd")[config_index]  
    if "Koc" in params_matrix:
        config_params['Koc'] = params_matrix.get("Koc")[config_index]  
    if "photolysis" in params_matrix:
        config_params['photolysis'] = params_matrix.get("photolysis")[config_index]
    if "aerobic_aquatic_metabolism" in params_matrix:
        config_params['aerobic_aquatic_metabolism'] = params_matrix.get("aerobic_aquatic_metabolism")[config_index]            
    if "anaerobic_aquatic_metabolism" in params_matrix:
        config_params['anaerobic_aquatic_metabolism'] = params_matrix.get("anaerobic_aquatic_metabolism")[config_index]            
    if "aerobic_soil_metabolism" in params_matrix:
        config_params['aerobic_soil_metabolism'] = params_matrix.get("aerobic_soil_metabolism")[config_index]
    if "hydrolysis_ph5" in params_matrix:
        config_params['hydrolysis_ph5'] = params_matrix.get("hydrolysis_ph5")[config_index]            
    if "hydrolysis_ph7" in params_matrix:
        config_params['hydrolysis_ph7'] = params_matrix.get("hydrolysis_ph7")[config_index]            
    if "hydrolysis_ph9" in params_matrix:
        config_params['hydrolysis_ph9'] = params_matrix.get("hydrolysis_ph9")[config_index]
    if "foliar_extraction" in params_matrix:
        config_params['foliar_extraction'] = params_matrix.get("foliar_extraction")[config_index]            
    if "foliar_decay_rate" in params_matrix:
        config_params['foliar_decay_rate'] = params_matrix.get("foliar_decay_rate")[config_index]            
    if "foliar_dissipation_half_life" in params_matrix:
        config_params['foliar_dissipation_half_life'] = params_matrix.get("foliar_dissipation_half_life")[config_index]
    if "density_of_product" in params_matrix:
        config_params['density_of_product'] = params_matrix.get("density_of_product")[config_index]            
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