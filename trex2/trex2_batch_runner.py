import numpy as np
import logging
import sys
sys.path.append("utils")
import json_utils
sys.path.append("./trex2")
import trex2_model
logger = logging.getLogger("TREX2BatchRunner")

class TREX2BatchRunner():

    def runTREX2Model(self,config_properties,results_dict):
        if not results_dict:
            results_dict = {}
        #this is where properties are searched, converted as needed, and any available methods are called
        logger.info(config_properties)
        chemical_name = None
        if 'chemical_name' in config_properties:
            chemical_name = config_properties['chemical_name']
        use = None
        if 'use' in config_properties:
            use = config_properties['use']
        formu_name = None
        if 'Formulated_product_name' in config_properties:
            formu_name = config_properties['Formulated_product_name']
        a_i = None
        if 'percent_ai' in config_properties:
            a_i = config_properties['percent_ai']
        Application_type = None
        if 'application_type' in config_properties:
            Application_type = config_properties['application_type']
        seed_treatment_formulation_name = None
        if 'seed_treatment_formulation_name' in config_properties:
            seed_treatment_formulation_name = config_properties['seed_treatment_formulation_name']
        seed_crop = None
        if 'seed_crop' in config_properties:
            seed_crop = config_properties['seed_crop']
        seed_crop = None
        if 'seed_crop' in config_properties:
            seed_crop = config_properties['seed_crop']
        den = None ## Presumption that this is density of product
        if 'density_of_product' in config_properties:
            den = config_properties['density_of_product']
        h_l = None
        if 'foliar_dissipation_half_life' in config_properties:
            h_l = config_properties['foliar_dissipation_half_life']
        n_a = None
        if 'n_a' in config_properties:
            n_a = config_properties['n_a']
        ar_lb = None ##called rate_out in crosswalk
        if 'ar_lb' in config_properties:
            ar_lb = config_properties['ar_lb']
        day_out = None
        if 'day_out' in config_properties:
            day_out = config_properties['day_out']
        ld50_bird = None 
        if 'avian_ld50' in config_properties:
            ld50_bird = config_properties['avian_ld50']
        ld50_bird = None 
        if 'avian_lc50' in config_properties:
            ld50_bird = config_properties['avian_lc50']
        NOAEC_bird = None  
        if 'avian_NOAEC' in config_properties:
            NOAEC_bird = config_properties['avian_NOAEC']
        NOAEL_bird = None    
        if 'avian_NOAEL' in config_properties:
            NOAEL_bird = config_properties['avian_NOAEC']
        ## Assessed Weight Bird small, medium, large
        aw_bird_sm = None    
        if 'body_weight_of_the_assessed_bird_small' in config_properties:
            aw_bird_sm = config_properties['body_weight_of_the_assessed_bird_small']
        aw_bird_md = None    
        if 'body_weight_of_the_assessed_bird_medium' in config_properties:
            aw_bird_md = config_properties['body_weight_of_the_assessed_bird_medium']
        aw_bird_lg = None    
        if 'body_weight_of_the_assessed_bird_large' in config_properties:
            aw_bird_lg = config_properties['body_weight_of_the_assessed_bird_large']
        Species_of_the_tested_bird_avian_ld50 = None    
        if 'Species_of_the_tested_bird_avian_ld50' in config_properties:
            Species_of_the_tested_bird_avian_ld50 = config_properties['Species_of_the_tested_bird_avian_ld50']
        Species_of_the_tested_bird_avian_lc50 = None    
        if 'Species_of_the_tested_bird_avian_lc50' in config_properties:
            Species_of_the_tested_bird_avian_lc50 = config_properties['Species_of_the_tested_bird_avian_lc50']
        Species_of_the_tested_bird_avian_NOAEC = None    
        if 'Species_of_the_tested_bird_avian_NOAEC' in config_properties:
            Species_of_the_tested_bird_avian_NOAEC = config_properties['Species_of_the_tested_bird_avian_NOAEC']
        Species_of_the_tested_bird_avian_NOAEL = None    
        if 'Species_of_the_tested_bird_avian_NOAEL' in config_properties:
            Species_of_the_tested_bird_avian_NOAEL = config_properties['Species_of_the_tested_bird_avian_NOAEL']
        tw_bird_ld50 = None    
        if 'bw_avian_ld50' in config_properties:
            tw_bird_ld50 = config_properties['bw_avian_ld50']
        tw_bird_lc50 = None    
        if 'bw_avian_lc50' in config_properties:
            tw_bird_lc50 = config_properties['bw_avian_lc50']
        tw_bird_NOAEC = None    
        if 'bw_avian_NOAEC' in config_properties:
            tw_bird_NOAEC = config_properties['bw_avian_NOAEC']
        tw_bird_NOAEL = None    
        if 'bw_avian_NOAEL' in config_properties:
            tw_bird_NOAEL = config_properties['bw_avian_NOAEL']
        ld50_mamm = None    
        if 'mammalian_ld50' in config_properties:
            ld50_mamm = config_properties['mammalian_ld50']
        lc50_mamm = None    
        if 'mammalian_lc50' in config_properties:
            lc50_mamm = config_properties['mammalian_lc50']
        NOAEC_mamm = None    
        if 'mammalian_NOAEC' in config_properties:
            NOAEC_mamm = config_properties['mammalian_NOAEC']
        NOAEL_mamm = None    
        if 'mammalian_NOAEL' in config_properties:
            NOAEL_mamm = config_properties['mammalian_NOAEL']
        ## Assessed Weight Mammal small, medium, large
        aw_mamm_sm = None    
        if 'body_weight_of_the_assessed_mammal_small' in config_properties:
            aw_mamm_sm = config_properties['body_weight_of_the_assessed_mammal_small']
        aw_mamm_md = None    
        if 'body_weight_of_the_assessed_mammal_medium' in config_properties:
            aw_mamm_md = config_properties['body_weight_of_the_assessed_mammal_medium']
        aw_mamm_lg = None    
        if 'body_weight_of_the_assessed_mammal_large' in config_properties:
            aw_mamm_lg = config_properties['body_weight_of_the_assessed_mammal_large']
        tw_mamm = None    
        if 'tested_mamm_body_weight' in config_properties:
            tw_mamm = config_properties['tested_mamm_body_weight']
        ## These properties don't exist yet
        seed_crop_v = None
        if 'seed_crop' in config_properties:
            seed_crop_v = config_properties['seed_crop']
        r_s = None
        if 'row_sp' in config_properties:
            r_s = config_properties['row_sp']
        b_w = None
        if 'bandwidth' in config_properties:
            b_w = config_properties['bandwidth']*12
        p_i = None
        if 'percent_incorporated' in config_properties:
            p_i = config_properties['percent_incorporated']
        x = None
        if 'mineau_scaling_factor' in config_properties:
            x = config_properties['mineau_scaling_factor']
        m_s_r_p = None
        if 'maximum_seedling_rate_per_use' in config_properties:
            m_s_r_p = config_properties['maximum_seedling_rate_per_use']

        trex2_obj = trex2_model.trex2(True,True, chemical_name, use, formu_name, a_i, Application_type, 
                seed_treatment_formulation_name, seed_crop, seed_crop_v, r_s, b_w, p_i, den, h_l, n_a, ar_lb, day_out,
                ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, aw_bird_sm, aw_bird_md, aw_bird_lg, 
                Species_of_the_tested_bird_avian_ld50, Species_of_the_tested_bird_avian_lc50, 
                Species_of_the_tested_bird_avian_NOAEC, Species_of_the_tested_bird_avian_NOAEL, 
                tw_bird_ld50, tw_bird_lc50, tw_bird_NOAEC, tw_bird_NOAEL, x, ld50_mamm, lc50_mamm, 
                NOAEC_mamm, NOAEL_mamm, aw_mamm_sm, aw_mamm_md, aw_mamm_lg, tw_mamm,
                m_s_r_p)
        results_dict['trex2'] = vars(trex2_obj)
        return results_dict