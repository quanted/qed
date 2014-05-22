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
        select_receptor = None
        if 'chemical_name' in config_properties:
            select_receptor = config_properties['select_receptor']
        bw_bird = None
        if 'body_weight_of_the_assessed_bird' in config_properties:
            bw_bird = config_properties['body_weight_of_the_assessed_bird']
        ''' Below is how it should actually work above is temporary fix
        if 'body_weight_of_bird' in config_properties:
            bw_bird = config_properties['body_weight_of_bird']
        '''
        bw_mamm = None
        if 'body_weight_of_mammal' in config_properties:
            bw_mamm = config_properties['body_weight_of_mammal']
        sol = None
        if 'solubility' in config_properties:
            sol = config_properties['solubility']
        avian_ld50 = None
        if 'avian_ld50' in config_properties:
            avian_ld50 = config_properties['avian_ld50']
        mammalian_ld50 = None
        if 'mammalian_ld50' in config_properties:
            mammalian_ld50 = config_properties['mammalian_ld50']
        aw_bird = None
        if 'body_weight_of_the_assessed_bird' in config_properties:
            aw_bird = config_properties['body_weight_of_the_assessed_bird']
        tw_bird = None
        if 'body_weight_of_the_assessed_bird' in config_properties:
            #tw_bird = config_properties['body_weight_of_the_tested_bird']
            tw_bird = config_properties['body_weight_of_the_assessed_bird']
        aw_mamm = None
        if 'body_weight_of_the_assessed_mammal' in config_properties:
            aw_mamm = config_properties['body_weight_of_the_assessed_mammal']
        tw_mamm = None
        if 'body_weight_of_the_tested_mammal' in config_properties:
            tw_mamm = config_properties['body_weight_of_the_tested_mammal']
        mineau = None
        if 'mineau_scaling_factor' in config_properties:
            mineau = config_properties['mineau_scaling_factor']
        avian_NOAEC = None
        if 'avian_NOAEC' in config_properties:
            avian_NOAEC = config_properties['avian_NOAEC']
        mammalian_NOAEC = None
        if 'mammalian_NOAEC' in config_properties:
            mammalian_NOAEC = config_properties['mammalian_NOAEC']
        avian_NOAEL = None
        if 'avian_NOAEL' in config_properties:
            avian_NOAEL = config_properties['avian_NOAEL']
        mammalian_NOAEL = None
        if 'mammalian_NOAEL' in config_properties:
            mammalian_NOAEL = config_properties['mammalian_NOAEL']
        if bw_mamm:
            results_dict['fw_mamm'] = sip_model.fw_mamm(bw_mamm)
            if 'fw_mamm' in results_dict and sol and bw_mamm:
                results_dict['dose_mamm'] = sip_model.dose_mamm(results_dict['fw_mamm'],sol,bw_mamm)
        if mammalian_ld50 and aw_mamm and tw_mamm:
            results_dict['at_mamm'] = sip_model.at_mamm(mammalian_ld50,aw_mamm,tw_mamm)
        if mammalian_NOAEL and tw_mamm and aw_mamm:
            results_dict['act'] = sip_model.act(mammalian_NOAEL,tw_mamm,aw_mamm)
        if 'dose_mamm' in results_dict and 'at_mamm' in results_dict:
            results_dict['acute_mamm'] = sip_model.acute_mamm(results_dict['dose_mamm'],results_dict['at_mamm'])
        if 'dose_mamm' in results_dict and 'act' in results_dict:
            results_dict['chron_mamm'] = sip_model.chron_mamm(results_dict['dose_mamm'],results_dict['act'])  
        if 'acute_mamm' in results_dict:
            results_dict['acuconm'] = sip_model.acuconm(results_dict['acute_mamm'])
        if 'chron_mamm' in results_dict:
            results_dict['chronconm'] = sip_model.chronconm(results_dict['chron_mamm']) 
        if bw_bird:
            results_dict['fw_bird'] = sip_model.fw_bird(bw_bird)
            results_dict['fi_bird'] = sip_model.fi_bird(bw_bird)
        if 'fw_bird' in results_dict and sol and bw_bird:
            results_dict['dose_bird'] = sip_model.dose_bird(results_dict['fw_bird'],sol,bw_bird)
        if avian_ld50 and aw_bird and tw_bird and mineau:
            results_dict['at_bird'] = sip_model.at_bird(avian_ld50,aw_bird,tw_bird,mineau)
        logger.info(avian_NOAEC)
        if avian_NOAEC and 'fi_bird' in results_dict and bw_bird:
            results_dict['det'] = sip_model.det(avian_NOAEC,results_dict['fi_bird'],bw_bird)
        if 'dose_bird' in results_dict and 'at_bird' in results_dict:
            results_dict['acute_bird'] = sip_model.acute_bird(results_dict['dose_bird'],results_dict['at_bird'])
        if 'dose_bird' in results_dict and 'det' in results_dict:
            results_dict['chron_bird'] = sip_model.chron_bird(results_dict['dose_bird'],results_dict['det'])
        if 'acute_bird' in results_dict:
            results_dict['acuconb'] = sip_model.acuconb(results_dict['acute_bird']) 
        if 'chron_bird' in results_dict:
            results_dict['chronconb'] = sip_model.chronconb(results_dict['chron_bird'])
        logger.info(results_dict)       
        return results_dict
