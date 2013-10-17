import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import numpy as np
import logging
import sys
import math
from django.utils import simplejson

logger = logging.getLogger('agdrift Model')


def toJSON(agdrift_object):
    agdrift_vars = vars(agdrift_object)
    agdrift_json = simplejson.dumps(agdrift_vars)
    return agdrift_json

def fromJSON(json_string):
    agdrift_vars = simplejson.loads(json_string)
    agdrift_object = terrplant(True,False,vars_dict=agdrift_vars)
    return agdrift_object

class agdrift(object):
    def __init__(self, set_variables=True, run_methods=True, drop_size = '', ecosystem_type = '', application_method = '', boom_height = '', orchard_type = '', vars_dict=None):
        self.set_default_variables()
        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.drop_size = drop_size
                self.ecosystem_type = ecosystem_type 
                self.application_method = application_method
                self.boom_height = boom_height
                self.orchard_type = orchard_type


            if run_methods:
                self.run_methods()
                logger.info(vars(self))
            # if run_methods:
            #     self.run_methods()

    def set_default_variables(self):
 #Currently used variables
        self.drop_size = ''
        self.ecosystem_type = '' 
        self.application_method = ''
        self.boom_height = ''
        self.orchard_type = ''
    def set_variables(self, drop_size, ecosystem_type, application_method, boom_height, orchard_type):
        self.drop_size = drop_size
        self.ecosystem_type = ecosystem_type 
        self.application_method = application_method
        self.boom_height = boom_height
        self.orchard_type = orchard_type    
    def run_methods(self):
        self.results()

    def results(self):
        self.pond_ground_high_vf2f = [0.0616,0.0572,0.0455,0.0376,0.0267,0.0194,0.013,0.0098,0.0078,0.0064,0.0053,0.0046,0.0039,0.0035,0.003,0.0027,0.0024,0.0022,0.002,0.0018,0.0017,0.0015,0.0014,0.0013,0.0012]
        self.pond_ground_high_f2m = [0.0165,0.0137,0.0104,0.009,0.0071,0.0056,0.0042,0.0034,0.0028,0.0024,0.0021,0.0019,0.0017,0.0015,0.0014,0.0013,0.0012,0.0011,0.001,0.00095,0.0009,0.0008,0.0008,0.0007,0.0007]
        self.pond_ground_low_vf2f = [0.0268,0.0231,0.0167,0.0136,0.01,0.0076,0.0054,0.0043,0.0036,0.0031,0.0027,0.0024,0.0021,0.0019,0.0017,0.0016,0.0015,0.0013,0.0012,0.0012,0.0011,0.001,0.001,0.0009,0.0009]
        self.pond_ground_low_f2m = [0.0109,0.0086,0.0065,0.0056,0.0045,0.0036,0.0028,0.0023,0.0019,0.0017,0.0015,0.0013,0.0012,0.0011,0.001,0.0009,0.0009,0.0008,0.0008,0.0007,0.0007,0.0006,0.0006,0.0006,0.0006]
        
    #####one less value (begin)
        self.pond_aerial_vf2f = [0.2425,0.2409,0.2344,0.2271,0.2083,0.1829,0.1455,0.1204,0.103,0.0904,0.0809,0.0734,0.0674,0.0625,0.0584,0.055,0.0521,0.0497,0.0476,0.0458,0.0442,0.0428,0.0416,0.0405,0.0396]
        self.pond_aerial_f2m = [0.1266,0.1247,0.1172,0.1094,0.0926,0.0743,0.0511,0.0392,0.0321,0.0272,0.0238,0.0212,0.0193,0.0177,0.0165,0.0155,0.0146,0.0139,0.0133,0.0128,0.0124,0.012,0.0117,0.0114,0.0111]
        self.pond_aerial_m2c = [0.0892,0.0900,0.0800,0.0700,0.0600,0.0400,0.0300,0.0200,0.0200,0.0130,0.0112,0.0099,0.0090,0.0083,0.0077,0.0073,0.0069,0.0066,0.0063,0.0060,0.0058,0.0056,0.0055,0.0053,0.0052]
        self.terr_aerial_vf2f = [0.5000,0.4913,0.4564,0.4220,0.3588,0.3039,0.2247,0.1741,0.1403,0.1171,0.1010,0.0893,0.0799,0.0729,0.0671,0.0626,0.0585,0.0550,0.0519,0.0494,0.0475,0.0458,0.0442,0.0428,0.0416]
        self.terr_aerial_f2m = [0.4999,0.4808,0.4046,0.3365,0.2231,0.1712,0.0979,0.0638,0.0469,0.0374,0.0312,0.0266,0.0234,0.021,0.0192,0.0177,0.0164,0.0154,0.0146,0.0139,0.0133,0.0128,0.0124,0.012,0.0117]
        self.terr_aerial_m2c =[0.5,0.4776,0.3882,0.3034,0.1711,0.1114,0.0561,0.0346,0.0249,0.0188,0.015,0.0126,0.011,0.0098,0.0089,0.0082,0.0077,0.0072,0.0069,0.0065,0.0063,0.006,0.0058,0.0056,0.0055]
        self.terr_ground_vf2f = [1.06,0.8564,0.4475,0.2595,0.104,0.05,0.0248,0.0164,0.012,0.0093,0.0075,0.0062,0.0053,0.0045,0.0039,0.0034,0.003,0.0027,0.0024,0.0022,0.002,0.0018,0.0017,0.0015,0.0014]
    #####one less value (end)

        self.terr_ground_f2m = [1.01,0.3731,0.0889,0.0459,0.0208,0.0119,0.007,0.0051,0.004,0.0033,0.0028,0.0024,0.0021,0.0019,0.0017,0.0015,0.0014,0.0013,0.0012,0.0011,0.001,0.0009,0.0009,0.0008,0.0008]
        self.pond_airblast_normal = [0.0011,0.0011,0.001,0.0009,0.0007,0.0005,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000978,0.0000863,0.0000769,0.0000629,0.0000626,0.0000571,0.0000523,0.0000482,0.0000446,0.0000414,0.0000386,0.0000361,0.0000339]
        self.pond_airblast_dense = [0.0145,0.014,0.0122,0.0106,0.0074,0.005,0.003,0.0022,0.0017,0.0014,0.0012,0.0011,0.001,0.0009,0.0008,0.0007,0.0007,0.0006,0.0006,0.0005,0.0005,0.0005,0.0005,0.0004,0.0004]
        self.pond_airblast_sparse = [0.0416,0.0395,0.0323,0.0258,0.015,0.0077,0.0031,0.0017,0.001,0.0007,0.0005,0.0004,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000898,0.0000771,0.0000668,0.0000583,0.0000513,0.0000453,0.0000405]
        self.pond_airblast_vineyard = [0.0024,0.0023,0.0018,0.0014,0.0009,0.0006,0.0003,0.0002,0.0002,0.0001,0.0001,0.0001,0.0000881,0.0000765,0.0000672,0.0000596,0.0000533,0.000048,0.0000435,0.0000397,0.0000363,0.0000334,0.0000309,0.0000286,0.0000267]
        self.pond_airblast_orchard = [0.0218,0.0208,0.0175,0.0145,0.0093,0.0056,0.0031,0.0021,0.0016,0.0013,0.0011,0.0009,0.0008,0.0007,0.0007,0.0006,0.0005,0.0005,0.0005,0.0004,0.0004,0.0004,0.0004,0.0003,0.0003]
        self.terr_airblast_normal = [0.0089,0.0081,0.0058,0.0042,0.0023,0.0012,0.0006,0.0004,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000965,0.0000765,0.0000625,0.0000523,0.0000446,0.0000387]
        self.terr_airblast_dense = [0.1155,0.1078,0.0834,0.0631,0.033,0.0157,0.0065,0.0038,0.0026,0.002,0.0016,0.0014,0.0012,0.0011,0.0009,0.0008,0.0007,0.0006,0.0005,0.0005]
        self.terr_airblast_sparse = [0.4763,0.4385,0.3218,0.2285,0.1007,0.0373,0.0103,0.0044,0.0023,0.0014,0.0009,0.0006,0.0005,0.0004,0.0003,0.0002,0.0001,0.0000889,0.0000665,0.0000514]
        self.terr_airblast_vineyard = [0.0376,0.0324,0.0195,0.012,0.0047,0.0019,0.0008,0.0004,0.0003,0.0002,0.0002,0.0001,0.0001,0.0001,0.000087,0.0000667,0.0000531,0.0000434,0.0000363,0.000031]
        self.terr_airblast_orchard = [0.2223,0.2046,0.1506,0.108,0.0503,0.021,0.0074,0.004,0.0026,0.0019,0.0015,0.0012,0.0011,0.0009,0.0008,0.0006,0.0005,0.0005,0.0004,0.0004]

        if (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Fine'):
            self.y = self.pond_aerial_vf2f
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Medium'):
            self.y = self.pond_aerial_f2m
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Coarse'):
            self.y = self.pond_aerial_m2c   
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Fine' and self.boom_height == 'Low'):
            self.y = self.pond_ground_low_vf2f
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Medium' and self.boom_height == 'Low'): 
            self.y = self.pond_ground_low_f2m
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Fine' and self.boom_height == 'High'):
            self.y = self.pond_ground_high_vf2f
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Medium' and self.boom_height == 'High'): 
            self.y = self.pond_ground_high_f2m
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Fine'):
            self.y = self.terr_aerial_vf2f
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Medium'):
            self.y = self.terr_aerial_f2m
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Coarse'):
            self.y = self.terr_aerial_m2c   
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Ground' and self.drop_size == 'Fine'):
            self.y = self.terr_ground_vf2f
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Ground' and self.drop_size == 'Medium'): 
            self.y = self.terr_ground_f2m  
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Normal'):
            self.y = self.pond_airblast_normal
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Dense'):
            self.y = self.pond_airblast_dense                        
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Sparse'):
            self.y = self.pond_airblast_sparse
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Vineyard'):
            self.y = self.pond_airblast_vineyard            
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Orchard'):
            self.y = pond_airblast_orchard
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Normal'):
            self.y = self.terr_airblast_normal
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]            
        elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Dense'):
            self.y = self.terr_airblast_dense
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Sparse'):
            self.y = self.terr_airblast_sparse
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Vineyard'):
            self.y = self.terr_airblast_vineyard
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Orchard'):
            self.y = self.terr_airblast_orchard
            self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
            self.z = 4
        else:
            print 2
            self.y = 3
        return self.x, self.y