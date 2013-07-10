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
    if "EEC_diet_SG" in params_matrix:
        config_params['EEC_diet_SG'] = params_matrix.get("EEC_diet_SG")[config_index]            
    if "EEC_diet_TG" in params_matrix:
        config_params['EEC_diet_TG'] = params_matrix.get("EEC_diet_TG")[config_index]  
    if "EEC_diet_BP" in params_matrix:
        config_params['EEC_diet_BP'] = params_matrix.get("EEC_diet_BP")[config_index] 
    if "EEC_diet_FR" in params_matrix:
        config_params['EEC_diet_FR'] = params_matrix.get("EEC_diet_FR")[config_index]  
    if "EEC_diet_AR" in params_matrix:
        config_params['EEC_diet_AR'] = params_matrix.get("EEC_diet_AR")[config_index] 
    if "EEC_dose_bird_SG_sm" in params_matrix:
        config_params['EEC_dose_bird_SG_sm'] = params_matrix.get("EEC_dose_bird_SG_sm")[config_index]  
    if "EEC_dose_bird_SG_md" in params_matrix:
        config_params['EEC_dose_bird_SG_md'] = params_matrix.get("EEC_dose_bird_SG_md")[config_index]  
    if "EEC_dose_bird_SG_lg" in params_matrix:
        config_params['EEC_dose_bird_SG_lg'] = params_matrix.get("EEC_dose_bird_SG_lg")[config_index] 
    if "EEC_dose_bird_TG_sm" in params_matrix:
        config_params['EEC_dose_bird_TG_sm'] = params_matrix.get("EEC_dose_bird_TG_sm")[config_index] 
    if "EEC_dose_bird_TG_md" in params_matrix:
        config_params['EEC_dose_bird_TG_md'] = params_matrix.get("EEC_dose_bird_TG_md")[config_index]  
    if "EEC_dose_bird_TG_lg" in params_matrix:
        config_params['EEC_dose_bird_TG_lg'] = params_matrix.get("EEC_dose_bird_TG_lg")[config_index]  
    if "EEC_dose_bird_BP_sm" in params_matrix:
        config_params['EEC_dose_bird_BP_sm'] = params_matrix.get("EEC_dose_bird_BP_sm")[config_index]
    if "EEC_dose_bird_BP_md" in params_matrix:
        config_params['EEC_dose_bird_BP_md'] = params_matrix.get("EEC_dose_bird_BP_md")[config_index]
    if "EEC_dose_bird_BP_lg" in params_matrix:
        config_params['EEC_dose_bird_BP_lg'] = params_matrix.get("EEC_dose_bird_BP_lg")[config_index] 
    if "EEC_dose_bird_FP_sm" in params_matrix:
        config_params['EEC_dose_bird_FP_sm'] = params_matrix.get("EEC_dose_bird_FP_sm")[config_index] 
    if "EEC_dose_bird_FP_md" in params_matrix:
        config_params['EEC_dose_bird_FP_md'] = params_matrix.get("EEC_dose_bird_FP_md")[config_index]
    if "EEC_dose_bird_FP_lg" in params_matrix:
        config_params['EEC_dose_bird_FP_lg'] = params_matrix.get("EEC_dose_bird_FP_lg")[config_index]   
    if "EEC_dose_bird_AR_sm" in params_matrix:
        config_params['EEC_dose_bird_AR_sm'] = params_matrix.get("EEC_dose_bird_AR_sm")[config_index]
    if "EEC_dose_bird_AR_md" in params_matrix:
        config_params['EEC_dose_bird_AR_md'] = params_matrix.get("EEC_dose_bird_AR_md")[config_index]
    if "EEC_dose_bird_AR_lg" in params_matrix:
        config_params['EEC_dose_bird_AR_lg'] = params_matrix.get("EEC_dose_bird_AR_lg")[config_index]   
    if "EEC_dose_bird_SE_sm" in params_matrix:
        config_params['EEC_dose_bird_SE_sm'] = params_matrix.get("EEC_dose_bird_SE_sm")[config_index] 
    if "EEC_dose_bird_SE_md" in params_matrix:
        config_params['EEC_dose_bird_SE_md'] = params_matrix.get("EEC_dose_bird_SE_md")[config_index]  
    if "EEC_dose_bird_SE_lg" in params_matrix:
        config_params['EEC_dose_bird_SE_lg'] = params_matrix.get("EEC_dose_bird_SE_lg")[config_index]
    if "ARQ_diet_bird_SG_A" in params_matrix:
        config_params['ARQ_diet_bird_SG_A'] = params_matrix.get("ARQ_diet_bird_SG_A")[config_index] 
    if "ARQ_diet_bird_SG_C" in params_matrix:
        config_params['ARQ_diet_bird_SG_C'] = params_matrix.get("ARQ_diet_bird_SG_C")[config_index]  
    if "ARQ_diet_bird_TG_A" in params_matrix:
        config_params['ARQ_diet_bird_TG_A'] = params_matrix.get("ARQ_diet_bird_TG_A")[config_index] 
    if "ARQ_diet_bird_TG_C" in params_matrix:
        config_params['ARQ_diet_bird_TG_C'] = params_matrix.get("ARQ_diet_bird_TG_C")[config_index]
    if "ARQ_diet_bird_BP_A" in params_matrix:
        config_params['ARQ_diet_bird_BP_A'] = params_matrix.get("ARQ_diet_bird_BP_A")[config_index] 
    if "ARQ_diet_bird_BP_C" in params_matrix:
        config_params['ARQ_diet_bird_BP_C'] = params_matrix.get("ARQ_diet_bird_BP_C")[config_index]  
    if "ARQ_diet_bird_FP_A" in params_matrix:
        config_params['ARQ_diet_bird_FP_A'] = params_matrix.get("ARQ_diet_bird_FP_A")[config_index]  
    if "ARQ_diet_bird_FP_C" in params_matrix:
        config_params['ARQ_diet_bird_FP_C'] = params_matrix.get("ARQ_diet_bird_FP_C")[config_index]  
    if "ARQ_diet_bird_AR_A" in params_matrix:
        config_params['ARQ_diet_bird_AR_A'] = params_matrix.get("ARQ_diet_bird_AR_A")[config_index]   
    if "ARQ_diet_bird_AR_C" in params_matrix:
        config_params['ARQ_diet_bird_AR_C'] = params_matrix.get("ARQ_diet_bird_AR_C")[config_index]  
    if "EEC_dose_mamm_SG_sm" in params_matrix:
        config_params['EEC_dose_mamm_SG_sm'] = params_matrix.get("EEC_dose_mamm_SG_sm")[config_index]  
    if "EEC_dose_mamm_SG_md" in params_matrix:
        config_params['EEC_dose_mamm_SG_md'] = params_matrix.get("EEC_dose_mamm_SG_md")[config_index]  
    if "EEC_dose_mamm_SG_lg" in params_matrix:
        config_params['EEC_dose_mamm_SG_lg'] = params_matrix.get("EEC_dose_mamm_SG_lg")[config_index] 
    if "EEC_dose_mamm_TG_sm" in params_matrix:
        config_params['EEC_dose_mamm_TG_sm'] = params_matrix.get("EEC_dose_mamm_TG_sm")[config_index] 
    if "EEC_dose_mamm_TG_md" in params_matrix:
        config_params['EEC_dose_mamm_TG_md'] = params_matrix.get("EEC_dose_mamm_TG_md")[config_index]  
    if "EEC_dose_mamm_TG_lg" in params_matrix:
        config_params['EEC_dose_mamm_TG_lg'] = params_matrix.get("EEC_dose_mamm_TG_lg")[config_index]  
    if "EEC_dose_mamm_BP_sm" in params_matrix:
        config_params['EEC_dose_mamm_BP_sm'] = params_matrix.get("EEC_dose_mamm_BP_sm")[config_index]
    if "EEC_dose_mamm_BP_md" in params_matrix:
        config_params['EEC_dose_mamm_BP_md'] = params_matrix.get("EEC_dose_mamm_BP_md")[config_index]
    if "EEC_dose_mamm_BP_lg" in params_matrix:
        config_params['EEC_dose_mamm_BP_lg'] = params_matrix.get("EEC_dose_mamm_BP_lg")[config_index] 
    if "EEC_dose_mamm_FP_sm" in params_matrix:
        config_params['EEC_dose_mamm_FP_sm'] = params_matrix.get("EEC_dose_mamm_FP_sm")[config_index] 
    if "EEC_dose_mamm_FP_md" in params_matrix:
        config_params['EEC_dose_mamm_FP_md'] = params_matrix.get("EEC_dose_mamm_FP_md")[config_index]
    if "EEC_dose_mamm_FP_lg" in params_matrix:
        config_params['EEC_dose_mamm_FP_lg'] = params_matrix.get("EEC_dose_mamm_FP_lg")[config_index]   
    if "EEC_dose_mamm_AR_sm" in params_matrix:
        config_params['EEC_dose_mamm_AR_sm'] = params_matrix.get("EEC_dose_mamm_AR_sm")[config_index]
    if "EEC_dose_mamm_AR_md" in params_matrix:
        config_params['EEC_dose_mamm_AR_md'] = params_matrix.get("EEC_dose_mamm_AR_md")[config_index]
    if "EEC_dose_mamm_AR_lg" in params_matrix:
        config_params['EEC_dose_mamm_AR_lg'] = params_matrix.get("EEC_dose_mamm_AR_lg")[config_index]   
    if "EEC_dose_mamm_SE_sm" in params_matrix:
        config_params['EEC_dose_mamm_SE_sm'] = params_matrix.get("EEC_dose_mamm_SE_sm")[config_index] 
    if "EEC_dose_mamm_SE_md" in params_matrix:
        config_params['EEC_dose_mamm_SE_md'] = params_matrix.get("EEC_dose_mamm_SE_md")[config_index]  
    if "EEC_dose_mamm_SE_lg" in params_matrix:
        config_params['EEC_dose_mamm_SE_lg'] = params_matrix.get("EEC_dose_mamm_SE_lg")[config_index] 
    if "ARQ_dose_mamm_SG_sm" in params_matrix:
        config_params['ARQ_dose_mamm_SG_sm'] = params_matrix.get("ARQ_dose_mamm_SG_sm")[config_index]
    if "CRQ_dose_mamm_SG_sm" in params_matrix:
        config_params['CRQ_dose_mamm_SG_sm'] = params_matrix.get("CRQ_dose_mamm_SG_sm")[config_index]
    if "ARQ_dose_mamm_SG_md" in params_matrix:
        config_params['ARQ_dose_mamm_SG_md'] = params_matrix.get("ARQ_dose_mamm_SG_md")[config_index]
    if "CRQ_dose_mamm_SG_md" in params_matrix:
        config_params['CRQ_dose_mamm_SG_md'] = params_matrix.get("CRQ_dose_mamm_SG_md")[config_index]
    if "ARQ_dose_mamm_SG_lg" in params_matrix:
        config_params['ARQ_dose_mamm_SG_lg'] = params_matrix.get("ARQ_dose_mamm_SG_lg")[config_index]
    if "CRQ_dose_mamm_SG_lg" in params_matrix:
        config_params['CRQ_dose_mamm_SG_lg'] = params_matrix.get("CRQ_dose_mamm_SG_lg")[config_index] 
    if "ARQ_dose_mamm_TG_sm" in params_matrix:
        config_params['ARQ_dose_mamm_TG_sm'] = params_matrix.get("ARQ_dose_mamm_TG_sm")[config_index]
    if "CRQ_dose_mamm_TG_sm" in params_matrix:
        config_params['CRQ_dose_mamm_TG_sm'] = params_matrix.get("CRQ_dose_mamm_TG_sm")[config_index]
    if "ARQ_dose_mamm_TG_md" in params_matrix:
        config_params['ARQ_dose_mamm_TG_md'] = params_matrix.get("ARQ_dose_mamm_TG_md")[config_index]
    if "CRQ_dose_mamm_TG_md" in params_matrix:
        config_params['CRQ_dose_mamm_TG_md'] = params_matrix.get("CRQ_dose_mamm_TG_md")[config_index]
    if "ARQ_dose_mamm_TG_lg" in params_matrix:
        config_params['ARQ_dose_mamm_TG_lg'] = params_matrix.get("ARQ_dose_mamm_TG_lg")[config_index]
    if "CRQ_dose_mamm_TG_lg" in params_matrix:
        config_params['CRQ_dose_mamm_TG_lg'] = params_matrix.get("CRQ_dose_mamm_TG_lg")[config_index] 
    if "ARQ_dose_mamm_BP_sm" in params_matrix:
        config_params['ARQ_dose_mamm_BP_sm'] = params_matrix.get("ARQ_dose_mamm_BP_sm")[config_index]
    if "CRQ_dose_mamm_BP_sm" in params_matrix:
        config_params['CRQ_dose_mamm_BP_sm'] = params_matrix.get("CRQ_dose_mamm_BP_sm")[config_index]
    if "ARQ_dose_mamm_BP_md" in params_matrix:
        config_params['ARQ_dose_mamm_BP_md'] = params_matrix.get("ARQ_dose_mamm_BP_md")[config_index]
    if "CRQ_dose_mamm_BP_md" in params_matrix:
        config_params['CRQ_dose_mamm_BP_md'] = params_matrix.get("CRQ_dose_mamm_BP_md")[config_index]
    if "ARQ_dose_mamm_BP_lg" in params_matrix:
        config_params['ARQ_dose_mamm_BP_lg'] = params_matrix.get("ARQ_dose_mamm_BP_lg")[config_index]
    if "CRQ_dose_mamm_BP_lg" in params_matrix:
        config_params['CRQ_dose_mamm_BP_lg'] = params_matrix.get("CRQ_dose_mamm_BP_lg")[config_index] 
    if "ARQ_dose_mamm_FP_sm" in params_matrix:
        config_params['ARQ_dose_mamm_FP_sm'] = params_matrix.get("ARQ_dose_mamm_FP_sm")[config_index]
    if "CRQ_dose_mamm_FP_sm" in params_matrix:
        config_params['CRQ_dose_mamm_FP_sm'] = params_matrix.get("CRQ_dose_mamm_FP_sm")[config_index]
    if "ARQ_dose_mamm_FP_md" in params_matrix:
        config_params['ARQ_dose_mamm_FP_md'] = params_matrix.get("ARQ_dose_mamm_FP_md")[config_index]
    if "CRQ_dose_mamm_FP_md" in params_matrix:
        config_params['CRQ_dose_mamm_FP_md'] = params_matrix.get("CRQ_dose_mamm_FP_md")[config_index]
    if "ARQ_dose_mamm_FP_lg" in params_matrix:
        config_params['ARQ_dose_mamm_FP_lg'] = params_matrix.get("ARQ_dose_mamm_FP_lg")[config_index]
    if "CRQ_dose_mamm_FP_lg" in params_matrix:
        config_params['CRQ_dose_mamm_FP_lg'] = params_matrix.get("CRQ_dose_mamm_FP_lg")[config_index] 
    if "ARQ_dose_mamm_AR_sm" in params_matrix:
        config_params['ARQ_dose_mamm_AR_sm'] = params_matrix.get("ARQ_dose_mamm_AR_sm")[config_index]
    if "CRQ_dose_mamm_AR_sm" in params_matrix:
        config_params['CRQ_dose_mamm_AR_sm'] = params_matrix.get("CRQ_dose_mamm_AR_sm")[config_index]
    if "ARQ_dose_mamm_AR_md" in params_matrix:
        config_params['ARQ_dose_mamm_AR_md'] = params_matrix.get("ARQ_dose_mamm_AR_md")[config_index]
    if "CRQ_dose_mamm_AR_md" in params_matrix:
        config_params['CRQ_dose_mamm_AR_md'] = params_matrix.get("CRQ_dose_mamm_AR_md")[config_index]
    if "ARQ_dose_mamm_AR_lg" in params_matrix:
        config_params['ARQ_dose_mamm_AR_lg'] = params_matrix.get("ARQ_dose_mamm_AR_lg")[config_index]
    if "CRQ_dose_mamm_AR_lg" in params_matrix:
        config_params['CRQ_dose_mamm_AR_lg'] = params_matrix.get("CRQ_dose_mamm_AR_lg")[config_index]  
     if "ARQ_dose_mamm_SE_sm" in params_matrix:
        config_params['ARQ_dose_mamm_SE_sm'] = params_matrix.get("ARQ_dose_mamm_SE_sm")[config_index]
    if "CRQ_dose_mamm_SE_sm" in params_matrix:
        config_params['CRQ_dose_mamm_SE_sm'] = params_matrix.get("CRQ_dose_mamm_SE_sm")[config_index]
    if "ARQ_dose_mamm_SE_md" in params_matrix:
        config_params['ARQ_dose_mamm_SE_md'] = params_matrix.get("ARQ_dose_mamm_SE_md")[config_index]
    if "CRQ_dose_mamm_SE_md" in params_matrix:
        config_params['CRQ_dose_mamm_SE_md'] = params_matrix.get("CRQ_dose_mamm_SE_md")[config_index]
    if "ARQ_dose_mamm_SE_lg" in params_matrix:
        config_params['ARQ_dose_mamm_SE_lg'] = params_matrix.get("ARQ_dose_mamm_SE_lg")[config_index]
    if "CRQ_dose_mamm_SE_lg" in params_matrix:
        config_params['CRQ_dose_mamm_SE_lg'] = params_matrix.get("CRQ_dose_mamm_SE_lg")[config_index]  
    if "ARQ_diet_bird_SG_A" in params_matrix:
        config_params['ARQ_diet_bird_SG_A'] = params_matrix.get("ARQ_diet_bird_SG_A")[config_index] 
    if "ARQ_diet_bird_SG_C" in params_matrix:
        config_params['ARQ_diet_bird_SG_C'] = params_matrix.get("ARQ_diet_bird_SG_C")[config_index]  
    if "ARQ_diet_mamm_TG" in params_matrix:
        config_params['ARQ_diet_mamm_TG'] = params_matrix.get("ARQ_diet_mamm_TG")[config_index] 
    if "CRQ_diet_mamm_TG" in params_matrix:
        config_params['CRQ_diet_mamm_TG'] = params_matrix.get("CRQ_diet_mamm_TG")[config_index]
    if "ARQ_diet_mamm_BP" in params_matrix:
        config_params['ARQ_diet_mamm_BP'] = params_matrix.get("ARQ_diet_mamm_BP")[config_index] 
    if "CRQ_diet_mamm_BP" in params_matrix:
        config_params['CRQ_diet_mamm_BP'] = params_matrix.get("CRQ_diet_mamm_BP")[config_index]  
    if "ARQ_diet_mamm_FP" in params_matrix:
        config_params['ARQ_diet_mamm_FP'] = params_matrix.get("ARQ_diet_mamm_FP")[config_index]  
    if "CRQ_diet_mamm_FP" in params_matrix:
        config_params['CRQ_diet_mamm_FP'] = params_matrix.get("CRQ_diet_mamm_FP")[config_index]  
    if "ARQ_diet_mamm_AR" in params_matrix:
        config_params['ARQ_diet_mamm_AR'] = params_matrix.get("ARQ_diet_mamm_AR")[config_index]   
    if "CRQ_diet_mamm_AR" in params_matrix:
        config_params['CRQ_diet_mamm_AR'] = params_matrix.get("CRQ_diet_mamm_AR")[config_index] 
    if "LD50_rg_bird_sm" in params_matrix:
        config_params['LD50_rg_bird_sm'] = params_matrix.get("LD50_rg_bird_sm")[config_index]
    if "LD50_rg_bird_md" in params_matrix:
        config_params['LD50_rg_bird_md'] = params_matrix.get("LD50_rg_bird_md")[config_index] 
    if "LD50_rg_bird_lg" in params_matrix:
        config_params['LD50_rg_bird_lg'] = params_matrix.get("LD50_rg_bird_lg")[config_index] 
    if "LD50_rg_mamm_sm" in params_matrix:
        config_params['LD50_rg_mamm_sm'] = params_matrix.get("LD50_rg_mamm_sm")[config_index] 
    if "LD50_rg_mamm_md" in params_matrix:
        config_params['LD50_rg_mamm_md'] = params_matrix.get("LD50_rg_mamm_md")[config_index] 
    if "LD50_rg_mamm_lg" in params_matrix:
        config_params['LD50_rg_mamm_lg'] = params_matrix.get("LD50_rg_mamm_lg")[config_index] 
    if "LD50_rl_bird_sm" in params_matrix:
        config_params['LD50_rl_bird_sm'] = params_matrix.get("LD50_rl_bird_sm")[config_index]
    if "LD50_rl_bird_md" in params_matrix:
        config_params['LD50_rl_bird_md'] = params_matrix.get("LD50_rl_bird_md")[config_index] 
    if "LD50_rl_bird_lg" in params_matrix:
        config_params['LD50_rl_bird_lg'] = params_matrix.get("LD50_rl_bird_lg")[config_index] 
    if "LD50_rl_mamm_sm" in params_matrix:
        config_params['LD50_rl_mamm_sm'] = params_matrix.get("LD50_rl_mamm_sm")[config_index] 
    if "LD50_rl_mamm_md" in params_matrix:
        config_params['LD50_rl_mamm_md'] = params_matrix.get("LD50_rl_mamm_md")[config_index] 
    if "LD50_rl_mamm_lg" in params_matrix:
        config_params['LD50_rl_mamm_lg'] = params_matrix.get("LD50_rl_mamm_lg")[config_index] 
    if "LD50_bg_bird_sm" in params_matrix:
        config_params['LD50_bg_bird_sm'] = params_matrix.get("LD50_bg_bird_sm")[config_index]
    if "LD50_bg_bird_md" in params_matrix:
        config_params['LD50_bg_bird_md'] = params_matrix.get("LD50_bg_bird_md")[config_index] 
    if "LD50_bg_bird_lg" in params_matrix:
        config_params['LD50_bg_bird_lg'] = params_matrix.get("LD50_bg_bird_lg")[config_index] 
    if "LD50_bg_mamm_sm" in params_matrix:
        config_params['LD50_bg_mamm_sm'] = params_matrix.get("LD50_bg_mamm_sm")[config_index] 
    if "LD50_bg_mamm_md" in params_matrix:
        config_params['LD50_bg_mamm_md'] = params_matrix.get("LD50_bg_mamm_md")[config_index] 
    if "LD50_bg_mamm_lg" in params_matrix:
        config_params['LD50_bg_mamm_lg'] = params_matrix.get("LD50_bg_mamm_lg")[config_index]
    if "LD50_bl_bird_sm" in params_matrix:
        config_params['LD50_bl_bird_sm'] = params_matrix.get("LD50_bl_bird_sm")[config_index]
    if "LD50_bl_bird_md" in params_matrix:
        config_params['LD50_bl_bird_md'] = params_matrix.get("LD50_bl_bird_md")[config_index] 
    if "LD50_bl_bird_lg" in params_matrix:
        config_params['LD50_bl_bird_lg'] = params_matrix.get("LD50_bl_bird_lg")[config_index] 
    if "LD50_bl_mamm_sm" in params_matrix:
        config_params['LD50_bl_mamm_sm'] = params_matrix.get("LD50_bl_mamm_sm")[config_index] 
    if "LD50_bl_mamm_md" in params_matrix:
        config_params['LD50_bl_mamm_md'] = params_matrix.get("LD50_bl_mamm_md")[config_index] 
    if "LD50_bl_mamm_lg" in params_matrix:
        config_params['LD50_bl_mamm_lg'] = params_matrix.get("LD50_bl_mamm_lg")[config_index]                                                                                                                                                                                 
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