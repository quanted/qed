import numpy as np
import logging
import sys
sys.path.append("utils")
import json_utils
sys.path.append("./terrplant")
from terrplant import terrplant_model

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
        results_dict['EEC-dry'] = terr.rundry_result
        results_dict['EEC-semi-aquatic'] = terr.runsemi_result
        results_dict['EEC-spray-drift'] = terr.spray_result
        results_dict['EEC-total-dry'] = terr.totaldry_result
        results_dict['EEC-total-semi-aquatic'] = terr.totalsemi_result
        results_dict['nmsRQdry'] = terr.nmsRQdry_result
        results_dict['nmsRQsemi'] = terr.nmsRQsemi_result
        results_dict['nmsRQspray'] = terr.nmsRQspray_result
        results_dict['lmsRQdry'] = terr.lmsRQdry_result
        results_dict['lmsRQsemi'] = terr.lmsRQsemi_result
        results_dict['lmsRQspray'] = terr.lmsRQspray_result
        results_dict['ndsRQdry'] = terr.ndsRQdry_result
        results_dict['ndsRQsemi'] = terr.ndsRQsemi_result
        results_dict['ndsRQspray'] = terr.ndsRQspray_result
        results_dict['ldsRQdry'] = terr.ldsRQdry_result
        results_dict['ldsRQsemi'] = terr.ldsRQsemi_result
        results_dict['ldsRQspray'] = terr.ldsRQspray_result 
        return results_dict
