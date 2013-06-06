import numpy as np
import logging
import sys
sys.path.append("utils")
import json_utils
sys.path.append("./terrplant")
import terrplant_model

class TerrPlantBatchRunner():
    
    def runTerrPlantModel(self,config_properties,results_dict):
        if not results_dict:
            results_dict = {}
        #this is where properties are searched, converted as needed, and any available methods are called
        A = None
        if 'application_lbs_rate' in config_properties:
            A = config_properties['application_lbs_rate']
        I = None
        if 'incorporation_depth' in config_properties:
            I = config_properties['incorporation_depth']
        R = None
        if 'runoff' in config_properties:
            R = config_properties['runoff']
        D = None
        if 'spray_drift' in config_properties:
            D = config_properties['spray_drift']
        nms = None
        if 'EC25_for_nonlisted_seedling_emergence_monocot' in config_properties:
            nms = config_properties['EC25_for_nonlisted_seedling_emergence_monocot']
        lms = None
        if 'NOAEC_for_listed_seedling_emergence_monocot' in config_properties:
            lms = config_properties['NOAEC_for_listed_seedling_emergence_monocot']
        nds = None
        if 'EC25_for_nonlisted_seedling_emergence_dicot' in config_properties:
            nds = config_properties['EC25_for_nonlisted_seedling_emergence_dicot']
        lds = None
        if 'NOAEC_for_listed_vegetative_vigor_dicot' in config_properties:
            lds = config_properties['NOAEC_for_listed_vegetative_vigor_dicot']
        terr = terrplant_model.terrplant(True,True,A,I,R,D,nms,lms,nds,lds)
        results_dict['terrplant'] = vars(terr)
        return results_dict
