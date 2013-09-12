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
    if "user_use_configuration" in params_matrix:
        config_name = params_matrix.get("user_use_configuration")[config_index]
    if "percent_ai" in params_matrix:
        config_params['percent_ai'] = params_matrix.get("percent_ai")[config_index]
    if "seed_treatment_formulation_name" in params_matrix:
        config_params['seed_treatment_formulation_name'] = params_matrix.get("seed_treatment_formulation_name")[config_index]
    if "density_of_product" in params_matrix:
        config_params['density_of_product'] = params_matrix.get("density_of_product")[config_index]
    if "maximum_seedling_rate_per_use" in params_matrix:
        config_params['maximum_seedling_rate_per_use'] = params_matrix.get("maximum_seedling_rate_per_use")[config_index]
    if "use" in params_matrix:
        config_params['use'] = params_matrix.get("use")[config_index]
    if "seed_crop" in params_matrix:
        config_params['seed_crop'] = params_matrix.get("seed_crop")[config_index]
    if "application_type" in params_matrix:
        config_params['application_type'] = params_matrix.get("application_type")[config_index]
    if "n_a" in params_matrix:
        config_params['n_a'] = params_matrix.get("n_a")[config_index]
    if "ar_lb" in params_matrix:
        config_params['ar_lb'] = params_matrix.get("ar_lb")[config_index]
    if "row_sp" in params_matrix:
        config_params['row_sp'] = params_matrix.get("row_sp")[config_index]
    if "bandwidth" in params_matrix:
        config_params['bandwidth'] = params_matrix.get("bandwidth")[config_index]
    if "foliar_dissipation_half_life" in params_matrix:
        config_params['foliar_dissipation_half_life'] = params_matrix.get("foliar_dissipation_half_life")[config_index]
    if "frac_pest_surface" in params_matrix:
        config_params['frac_pest_surface'] = params_matrix.get("frac_pest_surface")[config_index]
    if "day_out" in params_matrix:
        config_params['day_out'] = params_matrix.get("day_out")[config_index]
    if "aerobic_aquatic_metabolism" in params_matrix:
        config_params['aerobic_aquatic_metabolism'] = params_matrix.get("aerobic_aquatic_metabolism")[config_index]
    if "anaerobic_aquatic_metabolism" in params_matrix:
        config_params['anaerobic_aquatic_metabolism'] = params_matrix.get("anaerobic_aquatic_metabolism")[config_index]
    if "aerobic_soil_metabolism" in params_matrix:
        config_params['aerobic_soil_metabolism'] = params_matrix.get("aerobic_soil_metabolism")[config_index]
    if "foliar_extraction" in params_matrix:
        config_params['foliar_extraction'] = params_matrix.get("foliar_extraction")[config_index]
    if "foliar_decay_rate" in params_matrix:
        config_params['foliar_decay_rate'] = params_matrix.get("foliar_decay_rate")[config_index]
    if "foliar_dissipation_half_life" in params_matrix:
        config_params['foliar_dissipation_half_life'] = params_matrix.get("foliar_dissipation_half_life")[config_index]
    if "application_method" in params_matrix:
        config_params['application_method'] = params_matrix.get("application_method")[config_index]
    if "application_form" in params_matrix:
        config_params['application_form'] = params_matrix.get("application_form")[config_index]

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