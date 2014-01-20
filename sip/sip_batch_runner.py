import numpy as np
import logging
import sys
sys.path.append("utils")
import json_utils
sys.path.append("./sip")
import sip_model

logger = logging.getLogger("SIPBatchRunner")

class SIPBatchRunner():
    
    def runSIPModel(self,config_properties,results_dict):
        if not results_dict:
            results_dict = {}
        #this is where properties are searched, converted as needed, and any available methods are called
        logger.info(config_properties)
        chemical_name = None
        if 'chemical_name' in config_properties:
            chemical_name = config_properties['chemical_name']
        sol = None
        if 'solubility' in config_properties:
            sol = config_properties['solubility']
        ld50_a = None
        if 'avian_ld50_water' in config_properties:
            ld50_a = config_properties['avian_ld50_water']
        noaec = None
        if 'avian_NOAEC' in config_properties:
            noaec = config_properties['avian_NOAEC']
        aw_bird = None
        if 'body_weight_of_the_assessed_bird' in config_properties:
            aw_bird = config_properties['body_weight_of_the_assessed_bird']
        bw_quail = None
        if 'bw_quail' in config_properties:
            bw_quail = config_properties['bw_quail']
        bw_duck = None
        if 'bw_duck' in config_properties:
            bw_duck = config_properties['bw_duck']
        bwb_other = None
        if 'bwb_other' in config_properties:
            bwb_other = config_properties['bwb_other']
        mineau = None
        if 'mineau' in config_properties:
            mineau = config_properties['mineau']
        ld50_m = None
        if 'ld50_m' in config_properties:
            ld50_m = config_properties['ld50_m']
        noael = None
        if 'noael' in config_properties:
            noael = config_properties['noael']
        aw_mamm = None
        if 'aw_mamm' in config_properties:
            aw_mamm = config_properties['aw_mamm']
        bw_rat = None
        if 'bw_rat' in config_properties:
            bw_rat = config_properties['bw_rat']
        bwm_other = None
        if 'bwm_other' in config_properties:
            bw_rat = config_properties['bwm_other']
        m_species = None
        if 'm_species' in config_properties:
            m_species = config_properties['m_species']
        b_species = None
        if 'b_species' in config_properties:
            b_species = config_properties['id_Species_of_the_tested_bird']
        noaec_d = None
        if 'noaec_d' in config_properties:
            noaec_d = config_properties['noaec_d']
        noaec_q = None
        if 'noaec_q' in config_properties:
            noaec_q = config_properties['noaec_q']
        noaec_o = None
        if 'noaec_o' in config_properties:
            noaec_o = config_properties['noaec_o']
        sip_obj = sip_model.sip(True,True,chemical_name, b_species, m_species, bw_quail, bw_duck, bwb_other, bw_rat, bwm_other, sol, ld50_a, ld50_m, aw_bird, mineau, aw_mamm, noaec_d, noaec_q, noaec_o, Species_of_the_bird_NOAEC_CHOICES, noael)
        results_dict['sip'] = vars(sip_obj)
        return results_dict
