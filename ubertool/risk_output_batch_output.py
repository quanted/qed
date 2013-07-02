import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import urllib
from google.appengine.api import urlfetch
import logging
from django.utils import simplejson

logger = logging.getLogger("UseBatchOutput")

ubertool_config_service_base_url = os.environ['UBERTOOL_MONGO_SERVER']
    
def batchLoadUseConfigs(params_matrix,config_index,ubertool_configuration_properties):
    config_params = {}
    config_name = None
    if "use_config_name" in params_matrix:
        config_name = params_matrix.get("use_config_name")[config_index]
	if "terrestrial_toxicity_config_name" in params_matrix:
        config_name = params_matrix.get("terrestrial_toxicity_config_name")[config_index]
    if "gran_bird_ex_derm_dose" in params_matrix:
        config_params['gran_bird_ex_derm_dose'] = params_matrix.get("gran_bird_ex_derm_dose")[config_index]
    if "gran_repamp_ex_derm_dose" in params_matrix:
        config_params['gran_repamp_ex_derm_dose'] = params_matrix.get("gran_repamp_ex_derm_dose")[config_index]
    if "gran_mam_ex_derm_dose" in params_matrix:
        config_params['gran_mam_ex_derm_dose'] = params_matrix.get("gran_mam_ex_derm_dose")[config_index]
    if "fol_bird_ex_derm_dose" in params_matrix:
        config_params['fol_bird_ex_derm_dose'] = params_matrix.get("fol_bird_ex_derm_dose")[config_index]    
    if "fol_repamp_ex_derm_dose" in params_matrix:
        config_params['fol_repamp_ex_derm_dose'] = params_matrix.get("fol_repamp_ex_derm_dose")[config_index] 
    if "fol_mam_ex_derm_dose" in params_matrix:
        config_params['fol_mam_ex_derm_dose'] = params_matrix.get("fol_mam_ex_derm_dose")[config_index] 
    if "bgs_bird_ex_derm_dose" in params_matrix:
        config_params['bgs_bird_ex_derm_dose'] = params_matrix.get("bgs_bird_ex_derm_dose")[config_index] 
    if "bgs_repamp_ex_derm_dose" in params_matrix:
        config_params['bgs_repamp_ex_derm_dose'] = params_matrix.get("bgs_repamp_ex_derm_dose")[config_index] 
    if "bgs_mam_ex_derm_dose" in params_matrix:
        config_params['bgs_mam_ex_derm_dose'] = params_matrix.get("bgs_mam_ex_derm_dose")[config_index]   
    if "ratio_gran_bird" in params_matrix:
        config_params['ratio_gran_bird'] = params_matrix.get("ratio_gran_bird")[config_index]   
    if "LOC_gran_bird" in params_matrix:
        config_params['LOC_gran_bird'] = params_matrix.get("LOC_gran_bird")[config_index]  
    if "ratio_gran_rep" in params_matrix:
        config_params['ratio_gran_rep'] = params_matrix.get("ratio_gran_rep")[config_index]   
    if "LOC_gran_rep" in params_matrix:
        config_params['LOC_gran_rep'] = params_matrix.get("LOC_gran_rep")[config_index] 
    if "ratio_gran_amp" in params_matrix:
        config_params['ratio_gran_amp'] = params_matrix.get("ratio_gran_amp")[config_index] 
    if "LOC_gran_amp" in params_matrix:
        config_params['LOC_gran_amp'] = params_matrix.get("LOC_gran_amp")[config_index] 
    if "ratio_gran_mam" in params_matrix:
        config_params['ratio_gran_mam'] = params_matrix.get("ratio_gran_mam")[config_index] 
    if "LOC_gran_mam" in params_matrix:
        config_params['LOC_gran_mam'] = params_matrix.get("LOC_gran_mam")[config_index] 
    if "ratio_fol_bird" in params_matrix:
        config_params['ratio_fol_bird'] = params_matrix.get("ratio_fol_bird")[config_index] 
    if "LOC_fol_bird" in params_matrix:
        config_params['LOC_fol_bird'] = params_matrix.get("LOC_fol_bird")[config_index]    
    if "ratio_fol_rep" in params_matrix:
        config_params['ratio_fol_rep'] = params_matrix.get("ratio_fol_rep")[config_index]
    if "LOC_fol_rep" in params_matrix:
        config_params['LOC_fol_rep'] = params_matrix.get("LOC_fol_rep")[config_index]  
    if "ratio_fol_amp" in params_matrix:
        config_params['ratio_fol_amp'] = params_matrix.get("ratio_fol_amp")[config_index]   
    if "LOC_fol_amp" in params_matrix:
        config_params['LOC_fol_amp'] = params_matrix.get("LOC_fol_amp")[config_index] 
    if "ratio_fol_mam" in params_matrix:
        config_params['ratio_fol_mam'] = params_matrix.get("ratio_fol_mam")[config_index] 
    if "LOC_fol_mam" in params_matrix:
        config_params['LOC_fol_mam'] = params_matrix.get("LOC_fol_mam")[config_index]  
    if "ratio_bgs_bird" in params_matrix:
        config_params['ratio_bgs_bird'] = params_matrix.get("ratio_bgs_bird")[config_index] 
    if "LOC_bgs_bird" in params_matrix:
        config_params['LOC_bgs_bird'] = params_matrix.get("LOC_bgs_bird")[config_index] 
    if "ratio_bgs_rep" in params_matrix:
        config_params['ratio_bgs_rep'] = params_matrix.get("ratio_bgs_rep")[config_index]
    if "LOC_bgs_rep" in params_matrix:
        config_params['LOC_bgs_rep'] = params_matrix.get("LOC_bgs_rep")[config_index]
    if "ratio_bgs_amp" in params_matrix:
        config_params['ratio_bgs_amp'] = params_matrix.get("ratio_bgs_amp")[config_index] 
    if "LOC_bgs_amp" in params_matrix:
        config_params['LOC_bgs_amp'] = params_matrix.get("LOC_bgs_amp")[config_index] 
    if "ratio_bgs_mam" in params_matrix:
        config_params['ratio_bgs_mam'] = params_matrix.get("ratio_bgs_mam")[config_index]
    if "LOC_bgs_mam" in params_matrix:
        config_params['LOC_bgs_mam'] = params_matrix.get("LOC_bgs_mam")[config_index]                                                                                           
	config_params['use_configuration'] = config_name
    	ubertool_configuration_properties.update(config_params)
    	config_params['config_name'] = config_name
    	form_data = simplejson.dumps(config_params)
    	url = ubertool_config_service_base_url+"/ubertool/use/"+config_name
    	result = urlfetch.fetch(url=url,
                        	payload=form_data,
                        	method=urlfetch.POST,
                        	headers={'Content-Type': 'application/json'})
    return ubertool_configuration_properties        