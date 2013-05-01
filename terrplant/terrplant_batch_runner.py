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
        if A and I and R:
            results_dict['EEC-dry'] = terrplant_model.rundry(A,I,R)
            results_dict['EEC-semi-aquatic'] = terrplant_model.runsemi(A, I, R)
            D = None
            if 'spray_drift' in config_properties:
                D = config_properties['spray_drift']
            if D:
                results_dict['EEC-spray-drift'] = terrplant_model.spray(A,D)
        if results_dict['EEC-dry'] and results_dict['EEC-spray-drift']:
            results_dict['EEC-total-dry'] = terrplant_model.totaldry(results_dict['EEC-dry'],results_dict['EEC-spray-drift'])
        if results_dict['EEC-semi-aquatic'] and results_dict['EEC-spray-drift']:
            results_dict['EEC-total-semi-aquatic'] = terrplant_model.totalsemi(results_dict['EEC-semi-aquatic'],results_dict['EEC-spray-drift'])
        nms = None
        if 'EC25_for_nonlisted_seedling_emergence_monocot' in config_properties:
            nms = config_properties['NOAEC_for_listed_seedling_emergence_monocot']
        if results_dict['EEC-total-dry'] and nms:
            results_dict['nmsRQdry'] = terrplant_model.nmsRQdry(results_dict['EEC-total-dry'],nms)
        if results_dict['EEC-total-semi-aquatic'] and nms:    
            results_dict['nmsRQsemi'] = terrplant_model.nmsRQsemi(results_dict['EEC-total-semi-aquatic'],nms)
            results_dict['nmsRQspray'] = terrplant_model.nmsRQspray(results_dict['EEC-spray-drift'],nms)
        lms = None
        if 'NOAEC_for_listed_seedling_emergence_monocot' in config_properties:
            lms = config_properties['NOAEC_for_listed_seedling_emergence_monocot']
        if results_dict['EEC-total-dry'] and lms:
            results_dict['lmsRQdry'] = terrplant_model.lmsRQdry(results_dict['EEC-total-dry'],lms)
        if results_dict['EEC-total-semi-aquatic'] and lms:
            results_dict['lmsRQsemi'] = terrplant_model.lmsRQsemi(results_dict['EEC-total-semi-aquatic'],lms)
            results_dict['lmsRQspray'] = terrplant_model.lmsRQspray(results_dict['EEC-spray-drift'],lms)
        nds = None
        if 'EC25_for_nonlisted_seedling_emergence_dicot' in config_properties:
            nds = config_properties['EC25_for_nonlisted_seedling_emergence_dicot']
        if results_dict['EEC-total-dry'] and nds:
            results_dict['ndsRQdry'] = terrplant_model.ndsRQdry(results_dict['EEC-total-dry'],nds)
        if results_dict['EEC-total-semi-aquatic'] and nds:    
            results_dict['ndsRQsemi'] = terrplant_model.ndsRQsemi(results_dict['EEC-total-semi-aquatic'],nds)
            results_dict['ndsRQspray'] = terrplant_model.ndsRQspray(results_dict['EEC-spray-drift'],nds)
        lds = None
        if 'NOAEC_for_listed_vegetative_vigor_dicot' in config_properties:
            lds = config_properties['NOAEC_for_listed_vegetative_vigor_dicot']
        if results_dict['EEC-total-dry'] and lds:
            results_dict['ldsRQdry'] = terrplant_model.ldsRQdry(results_dict['EEC-total-dry'],lds)
        if results_dict['EEC-total-semi-aquatic'] and lds:
            results_dict['ldsRQsemi'] = terrplant_model.ldsRQsemi(results_dict['EEC-total-semi-aquatic'],lds)
            results_dict['ldsRQspray'] = terrplant_model.ldsRQspray(results_dict['EEC-spray-drift'],lds)            
        return results_dict
