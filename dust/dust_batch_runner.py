import numpy as np
import logging
import sys
sys.path.append("utils")
import json_utils
sys.path.append("./dust")
import dust_model

class DustBatchRunner():

    def runTerrPlantModel(self,config_properties,results_dict):
        results_dict = {}
        #this is where properties are searched, converted as needed, and any available methods are called
