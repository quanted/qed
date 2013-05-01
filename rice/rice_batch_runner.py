import numpy as np
import logging
import sys
sys.path.append("utils")
import json_utils
sys.path.append("./rice")
import rice_model

logger = logging.getLogger("RiceBatchRunner")


class RiceBatchRunner():
    
    def runRiceModel(self,config_properties):
        riceModelResults = {}
        #this is where properties are searched, converted as needed, and any available methods are called
        if 'application_kg_rate' in config_properties:
            if 'area_of_the_rice_paddy' in config_properties:
                riceModelResults['mai1']=rice_model.mai1(config_properties['application_kg_rate'], config_properties['area_of_the_rice_paddy'])
                if riceModelResults['mai1']:
                    if 'water_column_depth' in config_properties:
                        if 'sediment_depth' in config_properties:
                            if 'porosity_of_sediment' in config_properties:
                                if 'bulk_density_of_sediment' in config_properties:
                                    if 'Kd' in config_properties:
                                        riceModelResults['cw']=rice_model.cw(riceModelResults['mai1'], config_properties['water_column_depth'], config_properties['sediment_depth'], config_properties['porosity_of_sediment'], config_properties['bulk_density_of_sediment'], config_properties['Kd'])
        return riceModelResults