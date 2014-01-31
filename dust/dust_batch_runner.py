import numpy as np
import logging
import sys
sys.path.append("utils")
import json_utils
sys.path.append("./dust")
import dust_model
logger = logging.getLogger("DustBatchRunner")

class DUSTBatchRunner():

    def runDustModel(self,config_properties,results_dict):
        if not results_dict:
            results_dict = {}
        #this is where properties are searched, converted as needed, and any available methods are called
        logger.info(config_properties)
        chemical_name = None
        if 'chemical_name' in config_properties:
            chemical_name = config_properties['chemical_name']
        label_epa_reg_no = None
        if 'label_epa_reg_no' in config_properties:
            label_epa_reg_no = config_properties['label_epa_reg_no']
        ar_lb = None
        if 'ar_lb' in config_properties:
            ar_lb = config_properties['ar_lb']
        frac_pest_surface = None
        if 'frac_pest_surface' in config_properties:
            frac_pest_surface = config_properties['frac_pest_surface']
        bird_acute_oral_study = None
        if 'bird_acute_oral_study' in config_properties:
            bird_acute_oral_study = config_properties['bird_acute_oral_study']
        bird_study_add_comm = None
        if 'bird_acute_oral_study_comments' in config_properties:
            bird_study_add_comm = config_properties['bird_acute_oral_study_comments']
        bird_study_add_comm = None
        if 'bird_acute_oral_study_comments' in config_properties:
            bird_study_add_comm = config_properties['bird_acute_oral_study_comments']
        #This variable was called tested_bird_body_weight for dust input
        test_bird_bw = None
        if 'tested_bird_body_weight' in config_properties:
            test_bird_bw = config_properties['tested_bird_body_weight'] 
        mineau_scaling_factor = None
        if 'mineau_scaling_factor' in config_properties:
            mineau_scaling_factor = config_properties['mineau_scaling_factor'] 
        mamm_acute_derm_study = None
        if 'mamm_acute_derm_study' in config_properties:
            mamm_acute_derm_study = config_properties['mamm_acute_derm_study'] 
        mamm_study_add_comm = None
        if 'mamm_study_add_comm' in config_properties:
            mamm_study_add_comm = config_properties['mamm_study_add_comm'] 
        mamm_acute_derm_ld50 = None
        if 'mamm_acute_derm_ld50' in config_properties:
            mamm_acute_derm_ld50 = config_properties['mamm_acute_derm_ld50']
        ## I added this myself, not sure if correct
        mam_acute_oral_ld50 = None
        if 'mammalian_ld50' in config_properties:
            mam_acute_oral_ld50 = config_properties['mammalian_ld50']
        ## I added this myself, not sure if correct
        test_mam_bw = None
        if 'bw_mamm' in config_properties:
            test_mam_bw = config_properties['bw_mamm']
        ## Unrepresented parameters dislodge_fol_res
        low_bird_acute_ld50 = None
        if 'low_bird_acute_oral_ld50' in config_properties:
            low_bird_acute_ld50 = config_properties['low_bird_acute_oral_ld50']
        aviandermaltype = None
        if 'aviandermaltype' in config_properties:
            aviandermaltype = config_properties['aviandermaltype']

        dust_obj = dust_model.dust(True,True, chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface,  
        							bird_acute_oral_study, bird_study_add_comm, low_bird_acute_ld50, 
        							test_bird_bw, mineau_scaling_factor, mamm_acute_derm_study, mamm_study_add_comm,
        							 aviandermaltype, mam_acute_derm_ld50, mam_acute_oral_ld50, test_mam_bw)
        results_dict['dust'] = vars(dust_obj)
        return results_dict