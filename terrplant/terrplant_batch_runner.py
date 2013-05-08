import numpy as np
import logging
import sys
sys.path.append("utils")
import json_utils
sys.path.append("./terrplant")
from terrplant import terrplant as terrplant_data

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
            nms = config_properties['NOAEC_for_listed_seedling_emergence_monocot']
        lms = None
        if 'NOAEC_for_listed_seedling_emergence_monocot' in config_properties:
            lms = config_properties['NOAEC_for_listed_seedling_emergence_monocot']
        nds = None
        if 'EC25_for_nonlisted_seedling_emergence_dicot' in config_properties:
            nds = config_properties['EC25_for_nonlisted_seedling_emergence_dicot']
        lds = None
        if 'NOAEC_for_listed_vegetative_vigor_dicot' in config_properties:
            lds = config_properties['NOAEC_for_listed_vegetative_vigor_dicot']
        terrplant = terrplant_data.terrplant(A,I,R,D,nms,lms,nds,lds)
        results_dict['EEC-dry'] = terrplant.rundry()
        results_dict['EEC-semi-aquatic'] = terrplant.runsemi()
        results_dict['EEC-spray-drift'] = terrplant.spray()
        results_dict['EEC-total-dry'] = terrplant.totaldry()
        results_dict['EEC-total-semi-aquatic'] = terrplant.totalsemi()
        results_dict['nmsRQdry'] = terrplant.nmsRQdry()
        results_dict['nmsRQsemi'] = terrplant.nmsRQsemi()
        results_dict['nmsRQspray'] = terrplant.nmsRQspray()
        results_dict['lmsRQdry'] = terrplant.lmsRQdry()
        results_dict['lmsRQsemi'] = terrplant.lmsRQsemi()
        results_dict['lmsRQspray'] = terrplant.lmsRQspray()
        results_dict['ndsRQdry'] = terrplant.ndsRQdry()
        results_dict['ndsRQsemi'] = terrplant.ndsRQsemi()
        results_dict['ndsRQspray'] = terrplant.ndsRQspray()
        results_dict['ldsRQdry'] = terrplant.ldsRQdry()
        results_dict['ldsRQsemi'] = terrplant.ldsRQsemi()
        results_dict['ldsRQspray'] = terrplant.ldsRQspray()            
        return results_dict
