import numpy as np
import logging
import sys
sys.path.append("utils")
import json_utils
sys.path.append("./stir")
import stir_model

logger = logging.getLogger("STIRBatchRunner")

class SIPBatchRunner():
    
    def runSTIRModel(self,config_properties,results_dict):
        if not results_dict:
            results_dict = {}
        #this is where properties are searched, converted as needed, and any available methods are called
        logger.info(config_properties)
        chemical_name = None
        if 'chemical_name' in config_properties:
            chemical_name = config_properties['chemical_name']
        application_rate = None
        if 'ar_lb' in config_properties:
            application_rate = config_properties['ar_lb']
        column_height = None
        if 'column_height' in config_properties:
            column_height = config_properties['column_height']
        spray_drift = None
        if 'spray_drift' in config_properties:
            spray_drift = config_properties['spray_drift']
        direct_spray_duration = None
        if 'direct_spray_duration' in config_properties:
            direct_spray_duration = config_properties['direct_spray_duration']
        molecular_weight = None
        if 'molecular_weight' in config_properties:
            molecular_weight = config_properties['molecular_weight']
        vapor_pressure = None
        if 'vapor_pressure' in config_properties:
            vapor_pressure = config_properties['vapor_pressure']
        avian_oral_ld50 = None
        if 'avian_ld50' in config_properties:
            avian_oral_ld50 = config_properties['avian_ld50']
        body_weight_assessed_bird = None
        if 'body_weight_of_the_assessed_bird' in config_properties:
            body_weight_assessed_bird = config_properties['body_weight_of_the_assessed_bird']
        mineau_scaling_factor = None
        if 'mineau_scaling_factor' in config_properties:
            mineau_scaling_factor = config_properties['mineau_scaling_factor']
        mammal_inhalation_lc50 = None
        if 'mammal_inhalation_lc50' in config_properties:
            mammal_inhalation_lc50 = config_properties['mammal_inhalation_lc50']
        duration_mammal_inhalation_study = None
        if 'duration_of_rat_study' in config_properties:
            duration_mammal_inhalation_study = config_properties['duration_of_rat_study']
        body_weight_assessed_mammal = None
        if 'bw_mamm' in config_properties:
            body_weight_assessed_mammal = config_properties['bw_mamm']
        mammal_oral_ld50 = None
        if 'mammalian_ld50' in config_properties:
            mammal_oral_ld50 = config_properties['mammalian_ld50']

        stir_obj = stir_model.sip(True,True,chemical_name, application_rate, column_height, spray_drift, 
                                    direct_spray_duration, molecular_weight, vapor_pressure, avian_oral_ld50,
                                    body_weight_assessed_bird, mineau_scaling_factor, mammal_inhalation_lc50,
                                    duration_mammal_inhalation_study, body_weight_assessed_mammal,
                                    body_weight_tested_mammal, mammal_oral_ld50)

        results_dict['stir'] = vars(stir_obj)
        return results_dict
