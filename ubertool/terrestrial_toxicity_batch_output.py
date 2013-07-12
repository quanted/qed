import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import urllib
from google.appengine.api import urlfetch
import logging
from django.utils import simplejson

logger = logging.getLogger("PesticidePropertiesBatchOutput")

ubertool_config_service_base_url = os.environ['UBERTOOL_MONGO_SERVER']
    
def batchLoadTerrestrialToxicityConfigs(params_matrix,config_index,ubertool_configuration_properties):
    config_params = {}
    config_name = None
    if "terrestrial_toxicity_config_name" in params_matrix:
        config_name = params_matrix.get("terrestrial_toxicity_config_name")[config_index]
    if "low_bird_acute_oral_ld50" in params_matrix:
        config_params['low_bird_acute_oral_ld50'] = params_matrix.get("low_bird_acute_oral_ld50")[config_index]
    if "bird_study_add_comm" in params_matrix:
        config_params['bird_study_add_comm'] = params_matrix.get("bird_study_add_comm")[config_index]    
    if "mamm_study_add_comm" in params_matrix:
        config_params['mamm_study_add_comm'] = params_matrix.get("mamm_study_add_comm")[config_index]    
    if "avian_ld50" in params_matrix:
        config_params['avian_ld50'] = params_matrix.get("avian_ld50")[config_index]  
    if "Species_of_the_tested_bird" in params_matrix:
        config_params['Species_of_the_tested_bird'] = params_matrix.get("Species_of_the_tested_bird")[config_index]    
    if "Species_of_the_tested_bird_avian_LD50" in params_matrix:
        config_params['Species_of_the_tested_bird_avian_LD50'] = params_matrix.get("Species_of_the_tested_bird_avian_LD50")[config_index]      
    if "Species_of_the_tested_bird_avian_LC50" in params_matrix:
        config_params['Species_of_the_tested_bird_avian_LC50'] = params_matrix.get("Species_of_the_tested_bird_avian_LC50")[config_index]      
    if "Species_of_the_tested_bird_avian_NOAEC" in params_matrix:
        config_params['Species_of_the_tested_bird_avian_NOAEC'] = params_matrix.get("Species_of_the_tested_bird_avian_NOAEC")[config_index]      
    if "Species_of_the_tested_bird_avian_NOAEL" in params_matrix:
        config_params['Species_of_the_tested_bird_avian_NOAEL'] = params_matrix.get("Species_of_the_tested_bird_avian_NOAEL")[config_index]            
    if "mamm_acute_derm_ld50" in params_matrix:
        config_params['mamm_acute_derm_ld50'] = params_matrix.get("mamm_acute_derm_ld50")[config_index] 
    if "mamm_acute_derm_study" in params_matrix:
        config_params['mamm_acute_derm_study'] = params_matrix.get("mamm_acute_derm_study")[config_index] 
    if "bird_acute_oral_study" in params_matrix:
        config_params['bird_acute_oral_study'] = params_matrix.get("bird_acute_oral_study")[config_index]             
    if "avian_lc50" in params_matrix:
        config_params['avian_lc50'] = params_matrix.get("avian_lc50")[config_index]            
    if "avian_NOAEC" in params_matrix:
        config_params['avian_ld50'] = params_matrix.get("avian_NOAEC")[config_index]            
    if "avian_NOAEL" in params_matrix:
        config_params['avian_NOAEC'] = params_matrix.get("avian_NOAEL")[config_index]  
    if "tested_bird_body_weight" in params_matrix:
        config_params['tested_bird_body_weight'] = params_matrix.get("tested_bird_body_weight")[config_index]
    if "tested_mamm_body_weight" in params_matrix:
        config_params['tested_mamm_body_weight'] = params_matrix.get("tested_mamm_body_weight")[config_index]        
    if "bw_avian_ld50" in params_matrix:
        config_params['bw_avian_ld50'] = params_matrix.get("bw_avian_ld50")[config_index]
    if "bw_avian_lc50" in params_matrix:
        config_params['bw_avian_lc50'] = params_matrix.get("bw_avian_lc50")[config_index]
    if "bw_avian_NOAEC" in params_matrix:
        config_params['bw_avian_NOAEC'] = params_matrix.get("bw_avian_NOAEC")[config_index]
    if "bw_avian_NOAEL" in params_matrix:
        config_params['bw_avian_NOAEL'] = params_matrix.get("bw_avian_NOAEL")[config_index]
    if "bw_quail" in params_matrix:
        config_params['bw_quail'] = params_matrix.get("bw_quail")[config_index]
    if "bw_duck" in params_matrix:
        config_params['bw_duck'] = params_matrix.get("bw_duck")[config_index]
    if "bwb_duck" in params_matrix:
        config_params['bwb_duck'] = params_matrix.get("bwb_duck")[config_index]    
    if "body_weight_of_the_assessed_bird" in params_matrix:
        config_params['body_weight_of_the_assessed_bird'] = params_matrix.get("body_weight_of_the_assessed_bird")[config_index]
    if "body_weight_of_the_assessed_bird_sm" in params_matrix:
        config_params['body_weight_of_the_assessed_bird_sm'] = params_matrix.get("body_weight_of_the_assessed_bird_sm")[config_index]
    if "body_weight_of_the_assessed_bird_md" in params_matrix:
        config_params['body_weight_of_the_assessed_bird_md'] = params_matrix.get("body_weight_of_the_assessed_bird_md")[config_index]
    if "body_weight_of_the_assessed_bird_lg" in params_matrix:
        config_params['body_weight_of_the_assessed_bird_lg'] = params_matrix.get("body_weight_of_the_assessed_bird_lg")[config_index] 
    if "body_weight_of_the_assessed_mammal_sm" in params_matrix:
        config_params['body_weight_of_the_assessed_mammal_sm'] = params_matrix.get("body_weight_of_the_assessed_mammal_sm")[config_index]
    if "body_weight_of_the_assessed_mammal_md" in params_matrix:
        config_params['body_weight_of_the_assessed_mammal_md'] = params_matrix.get("body_weight_of_the_assessed_mammal_md")[config_index]
    if "body_weight_of_the_assessed_mammal_lg" in params_matrix:
        config_params['body_weight_of_the_assessed_mammal_lg'] = params_matrix.get("body_weight_of_the_assessed_mammal_lg")[config_index]       
    if "mineau_scaling_factor" in params_matrix:
        config_params['mineau_scaling_factor'] = params_matrix.get("mineau_scaling_factor")[config_index]              
    if "mammalian_ld50" in params_matrix:
        config_params['mammalian_ld50'] = params_matrix.get("mammalian_ld50")[config_index]
    if "mammalian_lc50" in params_matrix:
        config_params['mammalian_lc50'] = params_matrix.get("mammalian_lc50")[config_index]            
    if "mammalian_inhalation_lc50" in params_matrix:
        config_params['mammalian_inhalation_lc50'] = params_matrix.get("mammalian_inhalation_lc50")[config_index]            
    if "duration_of_rat_study" in params_matrix:
        config_params['duration_of_rat_study'] = params_matrix.get("duration_of_rat_study")[config_index]            
    if "mammalian_NOAEC" in params_matrix:
        config_params['mammalian_NOAEC'] = params_matrix.get("mammalian_NOAEC")[config_index]  
    if "mammalian_NOAEL" in params_matrix:
        config_params['mammalian_NOAEL'] = params_matrix.get("mammalian_NOAEL")[config_index]  
    if "amphibian_bw" in params_matrix:
        config_params['amphibian_bw'] = params_matrix.get("amphibian_bw")[config_index]              
    if "terrestrial_phase_amphibian_ld50" in params_matrix:
        config_params['terrestrial_phase_amphibian_ld50'] = params_matrix.get("terrestrial_phase_amphibian_ld50")[config_index]
    if "terrestrial_phase_amphibian_lc50" in params_matrix:
        config_params['terrestrial_phase_amphibian_lc50'] = params_matrix.get("terrestrial_phase_amphibian_lc50")[config_index]            
    if "terrestrial_phase_amphibian_NOAEC" in params_matrix:
        config_params['terrestrial_phase_amphibian_NOAEC'] = params_matrix.get("terrestrial_phase_amphibian_NOAEC")[config_index]            
    if "terrestrial_phase_amphibian_NOAEL" in params_matrix:
        config_params['terrestrial_phase_amphibian_NOAEL'] = params_matrix.get("terrestrial_phase_amphibian_NOAEL")[config_index]            
    if "reptile_bw" in params_matrix:
        config_params['reptile_bw'] = params_matrix.get("reptile_bw")[config_index]  
    if "terrestrial_phase_reptile_ld50" in params_matrix:
        config_params['terrestrial_phase_reptile_ld50'] = params_matrix.get("terrestrial_phase_reptile_ld50")[config_index]  
    if "terrestrial_phase_reptile_lc50" in params_matrix:
        config_params['terrestrial_phase_reptile_lc50'] = params_matrix.get("terrestrial_phase_reptile_lc50")[config_index]              
    if "terrestrial_phase_reptile_NOAEC" in params_matrix:
        config_params['terrestrial_phase_reptile_NOAEC'] = params_matrix.get("terrestrial_phase_reptile_NOAEC")[config_index]
    if "terrestrial_phase_reptile_NOAEL" in params_matrix:
        config_params['terrestrial_phase_reptile_NOAEL'] = params_matrix.get("terrestrial_phase_reptile_NOAEL")[config_index]            
    if "EC25_for_nonlisted_seedling_emergence_monocot" in params_matrix:
        config_params['EC25_for_nonlisted_seedling_emergence_monocot'] = params_matrix.get("EC25_for_nonlisted_seedling_emergence_monocot")[config_index]            
    if "EC25_for_nonlisted_seedling_emergence_dicot" in params_matrix:
        config_params['EC25_for_nonlisted_seedling_emergence_dicot'] = params_matrix.get("EC25_for_nonlisted_seedling_emergence_dicot")[config_index]            
    if "NOAEC_for_listed_seedling_emergence_monocot" in params_matrix:
        config_params['NOAEC_for_listed_seedling_emergence_monocot'] = params_matrix.get("NOAEC_for_listed_seedling_emergence_monocot")[config_index]  
    if "NOAEC_for_listed_seedling_emergence_dicot" in params_matrix:
        config_params['NOAEC_for_listed_seedling_emergence_dicot'] = params_matrix.get("NOAEC_for_listed_seedling_emergence_dicot")[config_index]  
    if "EC25_for_nonlisted_vegetative_vigor_monocot" in params_matrix:
        config_params['EC25_for_nonlisted_vegetative_vigor_monocot'] = params_matrix.get("EC25_for_nonlisted_vegetative_vigor_monocot")[config_index]              
    if "EC25_for_nonlisted_vegetative_vigor_dicot" in params_matrix:
        config_params['EC25_for_nonlisted_vegetative_vigor_dicot'] = params_matrix.get("EC25_for_nonlisted_vegetative_vigor_dicot")[config_index]
    if "NOAEC_for_listed_vegetative_vigor_monocot" in params_matrix:
        config_params['NOAEC_for_listed_vegetative_vigor_monocot'] = params_matrix.get("NOAEC_for_listed_vegetative_vigor_monocot")[config_index]            
    if "NOAEC_for_listed_vegetative_vigor_dicot" in params_matrix:
        config_params['NOAEC_for_listed_vegetative_vigor_dicot'] = params_matrix.get("NOAEC_for_listed_vegetative_vigor_dicot")[config_index]            
    if "Small_medium_and_large_BW_of_assessed_herptile_listed_species" in params_matrix:
        config_params['Small_medium_and_large_BW_of_assessed_herptile_listed_species'] = params_matrix.get("Small_medium_and_large_BW_of_assessed_herptile_listed_species")[config_index]            
    if "percent_water_content_of_small_med_large_herptile_species_diet" in params_matrix:
        config_params['percent_water_content_of_small_med_large_herptile_species_diet'] = params_matrix.get("percent_water_content_of_small_med_large_herptile_species_diet")[config_index]  
    if "slope_of_dose_response" in params_matrix:
        config_params['slope_of_dose_response'] = params_matrix.get("slope_of_dose_response")[config_index]
    if "desired_threshold" in params_matrix:
        config_params['desired_threshold'] = params_matrix.get("desired_threshold")[config_index]
    if "taxonomic_group" in params_matrix:
        config_params['taxonomic_group'] = params_matrix.get("taxonomic_group")[config_index]  
    if "eat_mammals" in params_matrix:
        config_params['eat_mammals'] = params_matrix.get("eat_mammals")[config_index]              
    if "eat_amphibians_reptiles" in params_matrix:
        config_params['eat_amphibians_reptiles'] = params_matrix.get("eat_amphibians_reptiles")[config_index]
                                                          
    config_params['terrestrial_configuration'] = config_name
    ubertool_configuration_properties.update(config_params)
    config_params['config_name'] = config_name
    form_data = simplejson.dumps(config_params)
    url = ubertool_config_service_base_url+"/ubertool/terre/"+config_name
    result = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
    return ubertool_configuration_properties