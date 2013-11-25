import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import numpy as np
from bisect import *
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
    agdrift_object = agdrift(True,False,vars_dict=agdrift_vars)
    return agdrift_object

class agdrift(object):
    def __init__(self, set_variables=True, run_methods=True, drop_size = '', ecosystem_type = '', application_method = '', boom_height = '', orchard_type = '', application_rate='', distance='',  aquatic_type='', calculation_input='', init_avg_dep_foa='', avg_depo_gha='', avg_depo_lbac='', deposition_ngL='', deposition_mgcm='', vars_dict=None):
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
                self.application_rate = application_rate
                self.distance = distance
                self.aquatic_type = aquatic_type
                self.calculation_input = calculation_input
                self.init_avg_dep_foa = init_avg_dep_foa
                self.avg_depo_gha = avg_depo_gha
                self.avg_depo_lbac = avg_depo_lbac
                self.deposition_ngL = deposition_ngL
                self.deposition_mgcm = deposition_mgcm
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
        self.application_rate = ''
        self.distance = ''
        self.aquatic_type = ''
        self.calculation_input = ''
        self.init_avg_dep_foa = -1
        self.avg_depo_lbac = -1
        self.avg_depo_gha  = -1
        self.deposition_ngL = -1
        self.deposition_mgcm = -1


    def set_variables(self, drop_size, ecosystem_type, application_method, boom_height, orchard_type, application_rate, distance, aquatic_type, calculation_input, init_avg_dep_foa, avg_depo_gha, avg_depo_lbac, deposition_ngL, deposition_mgcm):
        self.drop_size = drop_size
        self.ecosystem_type = ecosystem_type 
        self.application_method = application_method
        self.boom_height = boom_height
        self.orchard_type = orchard_type  
        self.application_rate = application_rate
        self.distance = distance
        self.aquatic_type = aquatic_type
        self.calculation_input = calculation_input
        self.init_avg_dep_foa = init_avg_dep_foa
        self.avg_depo_gha = avg_depo_gha
        self.avg_depo_lbac = avg_depo_lbac
        self.deposition_ngL = deposition_ngL
        self.deposition_mgcm = deposition_mgcm
    def run_methods(self):
        self.results()
        if (self.calculation_input == 'Distance' ):
            self.extrapolate_from_fig(self.ecosystem_type, self.distance, bisect_left, self.x, self.y)
            self.deposition_foa_to_lbac_f(self.init_avg_dep_foa, self.application_rate)
            self.deposition_lbac_to_gha_f(self.avg_depo_lbac)
            self.deposition_gha_to_ngL_f(self.aquatic_type, self.avg_depo_gha)
            self.deposition_gha_to_mgcm_f(self.avg_depo_gha)

        elif (self.calculation_input == 'Fraction'):
            self.extrapolate_from_fig2(self.ecosystem_type, self.init_avg_dep_foa, bisect_left, self.x, self.y)
            self.deposition_foa_to_lbac_f(self.init_avg_dep_foa, self.application_rate)
            self.deposition_lbac_to_gha_f(self.avg_depo_lbac)
            self.deposition_gha_to_ngL_f(self.aquatic_type, self.avg_depo_gha)
            self.deposition_gha_to_mgcm_f(self.avg_depo_gha)

        elif (self.calculation_input == 'Initial Average Deposition (g/ha)'):
            self.deposition_ghac_to_lbac_f(self.avg_depo_gha)
            #print self.avg_depo_lbac 
            self.deposition_lbac_to_foa_f(self.avg_depo_lbac, self.application_rate)
            self.extrapolate_from_fig2(self.ecosystem_type, self.init_avg_dep_foa, bisect_left, self.x, self.y)
            self.deposition_gha_to_ngL_f(self.aquatic_type, self.avg_depo_gha)
            self.deposition_gha_to_mgcm_f(self.avg_depo_gha)

        elif (self.calculation_input == 'Initial Average Deposition (lb/ac)'):     
            print self.avg_depo_lbac
            self.deposition_lbac_to_gha_f(self.avg_depo_lbac)
            self.deposition_gha_to_ngL_f(self.aquatic_type, self.avg_depo_gha)
            self.deposition_gha_to_mgcm_f(self.avg_depo_gha)
            self.deposition_lbac_to_foa_f(self.avg_depo_lbac, self.application_rate)
            self.extrapolate_from_fig2(self.ecosystem_type, self.init_avg_dep_foa, bisect_left, self.x, self.y)

        elif (self.calculation_input == 'Initial Average Concentration (ng/L)'):
            self.deposition_ngL_2_gha_f(self.deposition_ngL)
            self.deposition_ghac_to_lbac_f(self.avg_depo_gha)
            self.deposition_lbac_to_foa_f(self.avg_depo_lbac, self.application_rate)
            self.extrapolate_from_fig2(self.ecosystem_type, self.init_avg_dep_foa, bisect_left, self.x, self.y)
            self.deposition_gha_to_mgcm_f(self.avg_depo_gha)

        else:  
            self.deposition_mgcm_to_gha_f(self.deposition_mgcm)
            self.deposition_ghac_to_lbac_f(self.avg_depo_gha)
            self.deposition_lbac_to_foa_f(self.avg_depo_lbac, self.application_rate)
            self.extrapolate_from_fig2(self.ecosystem_type, self.init_avg_dep_foa, bisect_left, self.x, self.y)
            self.deposition_gha_to_ngL_f(self.aquatic_type, self.avg_depo_gha)

    # def results(self):
    #     self.pond_ground_high_vf2f = [0.0616,0.0572,0.0455,0.0376,0.0267,0.0194,0.013,0.0098,0.0078,0.0064,0.0053,0.0046,0.0039,0.0035,0.003,0.0027,0.0024,0.0022,0.002,0.0018,0.0017,0.0015,0.0014,0.0013,0.0012]
    #     self.pond_ground_high_f2m = [0.0165,0.0137,0.0104,0.009,0.0071,0.0056,0.0042,0.0034,0.0028,0.0024,0.0021,0.0019,0.0017,0.0015,0.0014,0.0013,0.0012,0.0011,0.001,0.00095,0.0009,0.0008,0.0008,0.0007,0.0007]
    #     self.pond_ground_low_vf2f = [0.0268,0.0231,0.0167,0.0136,0.01,0.0076,0.0054,0.0043,0.0036,0.0031,0.0027,0.0024,0.0021,0.0019,0.0017,0.0016,0.0015,0.0013,0.0012,0.0012,0.0011,0.001,0.001,0.0009,0.0009]
    #     self.pond_ground_low_f2m = [0.0109,0.0086,0.0065,0.0056,0.0045,0.0036,0.0028,0.0023,0.0019,0.0017,0.0015,0.0013,0.0012,0.0011,0.001,0.0009,0.0009,0.0008,0.0008,0.0007,0.0007,0.0006,0.0006,0.0006,0.0006]
        
    # #####one less value (begin)
    #     self.pond_aerial_vf2f = [0.2425,0.2409,0.2344,0.2271,0.2083,0.1829,0.1455,0.1204,0.103,0.0904,0.0809,0.0734,0.0674,0.0625,0.0584,0.055,0.0521,0.0497,0.0476,0.0458,0.0442,0.0428,0.0416,0.0405,0.0396]
    #     self.pond_aerial_f2m = [0.1266,0.1247,0.1172,0.1094,0.0926,0.0743,0.0511,0.0392,0.0321,0.0272,0.0238,0.0212,0.0193,0.0177,0.0165,0.0155,0.0146,0.0139,0.0133,0.0128,0.0124,0.012,0.0117,0.0114,0.0111]
    #     self.pond_aerial_m2c = [0.0892,0.0900,0.0800,0.0700,0.0600,0.0400,0.0300,0.0200,0.0200,0.0130,0.0112,0.0099,0.0090,0.0083,0.0077,0.0073,0.0069,0.0066,0.0063,0.0060,0.0058,0.0056,0.0055,0.0053,0.0052]
    #     self.pond_aerial_c2vc = [0.0892,0.0900,0.0800,0.0700,0.0600,0.0400,0.0300,0.0200,0.0200,0.0130,0.0112,0.0099,0.0090,0.0083,0.0077,0.0073,0.0069,0.0066,0.0063,0.0060,0.0058,0.0056,0.0055,0.0053,0.0052]
    #     self.terr_aerial_vf2f = [0.5000,0.4913,0.4564,0.4220,0.3588,0.3039,0.2247,0.1741,0.1403,0.1171,0.1010,0.0893,0.0799,0.0729,0.0671,0.0626,0.0585,0.0550,0.0519,0.0494,0.0475,0.0458,0.0442,0.0428,0.0416]
    #     self.terr_aerial_f2m = [0.4999,0.4808,0.4046,0.3365,0.2231,0.1712,0.0979,0.0638,0.0469,0.0374,0.0312,0.0266,0.0234,0.021,0.0192,0.0177,0.0164,0.0154,0.0146,0.0139,0.0133,0.0128,0.0124,0.012,0.0117]
    #     self.terr_aerial_m2c =[0.5,0.4776,0.3882,0.3034,0.1711,0.1114,0.0561,0.0346,0.0249,0.0188,0.015,0.0126,0.011,0.0098,0.0089,0.0082,0.0077,0.0072,0.0069,0.0065,0.0063,0.006,0.0058,0.0056,0.0055]
    #     self.terr_aerial_c2vc =[0.5,0.4776,0.3882,0.3034,0.1711,0.1114,0.0561,0.0346,0.0249,0.0188,0.015,0.0126,0.011,0.0098,0.0089,0.0082,0.0077,0.0072,0.0069,0.0065,0.0063,0.006,0.0058,0.0056,0.0055]
    #     self.terr_ground_vf2f = [1.06,0.8564,0.4475,0.2595,0.104,0.05,0.0248,0.0164,0.012,0.0093,0.0075,0.0062,0.0053,0.0045,0.0039,0.0034,0.003,0.0027,0.0024,0.0022,0.002,0.0018,0.0017,0.0015,0.0014]
    # #####one less value (end)

    #     self.terr_ground_f2m = [1.01,0.3731,0.0889,0.0459,0.0208,0.0119,0.007,0.0051,0.004,0.0033,0.0028,0.0024,0.0021,0.0019,0.0017,0.0015,0.0014,0.0013,0.0012,0.0011,0.001,0.0009,0.0009,0.0008,0.0008]
    #     self.pond_airblast_normal = [0.0011,0.0011,0.001,0.0009,0.0007,0.0005,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000978,0.0000863,0.0000769,0.0000629,0.0000626,0.0000571,0.0000523,0.0000482,0.0000446,0.0000414,0.0000386,0.0000361,0.0000339]
    #     self.pond_airblast_dense = [0.0145,0.014,0.0122,0.0106,0.0074,0.005,0.003,0.0022,0.0017,0.0014,0.0012,0.0011,0.001,0.0009,0.0008,0.0007,0.0007,0.0006,0.0006,0.0005,0.0005,0.0005,0.0005,0.0004,0.0004]
    #     self.pond_airblast_sparse = [0.0416,0.0395,0.0323,0.0258,0.015,0.0077,0.0031,0.0017,0.001,0.0007,0.0005,0.0004,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000898,0.0000771,0.0000668,0.0000583,0.0000513,0.0000453,0.0000405]
    #     self.pond_airblast_vineyard = [0.0024,0.0023,0.0018,0.0014,0.0009,0.0006,0.0003,0.0002,0.0002,0.0001,0.0001,0.0001,0.0000881,0.0000765,0.0000672,0.0000596,0.0000533,0.000048,0.0000435,0.0000397,0.0000363,0.0000334,0.0000309,0.0000286,0.0000267]
    #     self.pond_airblast_orchard = [0.0218,0.0208,0.0175,0.0145,0.0093,0.0056,0.0031,0.0021,0.0016,0.0013,0.0011,0.0009,0.0008,0.0007,0.0007,0.0006,0.0005,0.0005,0.0005,0.0004,0.0004,0.0004,0.0004,0.0003,0.0003]
    #     self.terr_airblast_normal = [0.0089,0.0081,0.0058,0.0042,0.0023,0.0012,0.0006,0.0004,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000965,0.0000765,0.0000625,0.0000523,0.0000446,0.0000387]
    #     self.terr_airblast_dense = [0.1155,0.1078,0.0834,0.0631,0.033,0.0157,0.0065,0.0038,0.0026,0.002,0.0016,0.0014,0.0012,0.0011,0.0009,0.0008,0.0007,0.0006,0.0005,0.0005]
    #     self.terr_airblast_sparse = [0.4763,0.4385,0.3218,0.2285,0.1007,0.0373,0.0103,0.0044,0.0023,0.0014,0.0009,0.0006,0.0005,0.0004,0.0003,0.0002,0.0001,0.0000889,0.0000665,0.0000514]
    #     self.terr_airblast_vineyard = [0.0376,0.0324,0.0195,0.012,0.0047,0.0019,0.0008,0.0004,0.0003,0.0002,0.0002,0.0001,0.0001,0.0001,0.000087,0.0000667,0.0000531,0.0000434,0.0000363,0.000031]
    #     self.terr_airblast_orchard = [0.2223,0.2046,0.1506,0.108,0.0503,0.021,0.0074,0.004,0.0026,0.0019,0.0015,0.0012,0.0011,0.0009,0.0008,0.0006,0.0005,0.0005,0.0004,0.0004]

    #     if (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Fine'):
    #         self.y = self.pond_aerial_vf2f
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Medium'):
    #         self.y = self.pond_aerial_f2m
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Coarse'):
    #         self.y = self.pond_aerial_m2c   
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Very Coarse'):
    #         self.y = self.pond_aerial_c2vc      
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Fine' and self.boom_height == 'Low'):
    #         self.y = self.pond_ground_low_vf2f
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Medium' and self.boom_height == 'Low'): 
    #         self.y = self.pond_ground_low_f2m
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Fine' and self.boom_height == 'High'):
    #         self.y = self.pond_ground_high_vf2f
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Medium' and self.boom_height == 'High'): 
    #         self.y = self.pond_ground_high_f2m
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Fine'):
    #         self.y = self.terr_aerial_vf2f
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Medium'):
    #         self.y = self.terr_aerial_f2m
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Coarse'):
    #         self.y = self.terr_aerial_m2c   
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Very Coarse'):
    #         self.y = self.terr_aerial_c2vc   
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Ground' and self.drop_size == 'Fine'):
    #         self.y = self.terr_ground_vf2f
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Ground' and self.drop_size == 'Medium'): 
    #         self.y = self.terr_ground_f2m  
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Normal'):
    #         self.y = self.pond_airblast_normal
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Dense'):
    #         self.y = self.pond_airblast_dense                        
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Sparse'):
    #         self.y = self.pond_airblast_sparse
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Vineyard'):
    #         self.y = self.pond_airblast_vineyard            
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Orchard'):
    #         self.y = pond_airblast_orchard
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Normal'):
    #         self.y = self.terr_airblast_normal
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]            
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Dense'):
    #         self.y = self.terr_airblast_dense
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Sparse'):
    #         self.y = self.terr_airblast_sparse
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Vineyard'):
    #         self.y = self.terr_airblast_vineyard
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Orchard'):
    #         self.y = self.terr_airblast_orchard
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
    #         self.z = 4
    #     else:
    #         #print 2
    #         self.y = 3
    #     return self.x, self.y

    def results(self):
       self.pond_ground_high_vf2f = [6.164E+00,4.251E+00,3.425E+00,2.936E+00,2.607E+00,2.364E+00,2.173E+00,
2.017E+00,1.886E+00,1.773E+00,1.674E+00,1.586E+00,1.508E+00,1.437E+00,
1.372E+00,1.314E+00,1.260E+00,1.210E+00,1.163E+00,1.120E+00,1.080E+00,
 1.042E+00,1.007E+00,9.740E-01,9.427E-01,9.132E-01,8.853E-01,8.588E-01,
 8.337E-01,8.099E-01,7.871E-01,7.655E-01,7.449E-01,7.251E-01,7.063E-01,
 6.882E-01,6.709E-01,6.544E-01,6.385E-01,6.232E-01,6.085E-01,5.944E-01,
 5.808E-01,5.677E-01,5.551E-01,5.429E-01,5.312E-01,5.198E-01,5.089E-01,
4.983E-01,4.880E-01,4.781E-01,4.685E-01,4.592E-01,4.502E-01,4.415E-01,
4.331E-01,4.249E-01,4.169E-01,4.092E-01,4.017E-01,3.944E-01,3.873E-01,
3.804E-01,3.737E-01,3.672E-01,3.609E-01,3.547E-01,3.487E-01,3.428E-01,
3.371E-01,3.316E-01,3.262E-01,3.209E-01,3.157E-01,3.107E-01,3.058E-01,
3.010E-01,2.964E-01,2.918E-01,2.874E-01,2.830E-01,2.788E-01,2.746E-01,
2.706E-01,2.666E-01,2.628E-01,2.590E-01,2.553E-01,2.516E-01,2.481E-01,
2.446E-01,2.412E-01,2.379E-01,2.347E-01,2.315E-01,2.284E-01,2.253E-01,
2.223E-01,2.194E-01,2.165E-01]
        self.pond_ground_high_f2m = [1.650E+00,9.842E-01,8.413E-01,7.572E-01,6.978E-01,6.515E-01,6.135E-01,
5.813E-01,5.534E-01,5.287E-01,5.067E-01,4.868E-01,4.686E-01,4.520E-01,
4.367E-01,4.225E-01,4.093E-01,3.970E-01,3.854E-01,3.745E-01,3.643E-01,
 3.546E-01,3.454E-01,3.368E-01,3.285E-01,3.206E-01,3.131E-01,3.060E-01,
2.991E-01,2.926E-01,2.863E-01,2.803E-01,2.745E-01,2.689E-01,2.636E-01,
2.584E-01,2.535E-01,2.487E-01,2.440E-01,2.396E-01,2.353E-01,2.311E-01,
2.270E-01,2.231E-01,2.193E-01,2.157E-01,2.121E-01,2.086E-01,2.053E-01,
2.020E-01,1.988E-01,1.958E-01,1.928E-01,1.898E-01,1.870E-01,1.842E-01,
1.815E-01,1.789E-01,1.764E-01,1.739E-01,1.714E-01,1.690E-01,1.667E-01,
1.645E-01,1.623E-01,1.601E-01,1.580E-01,1.559E-01,1.539E-01,1.520E-01,
1.500E-01,1.481E-01,1.463E-01,1.445E-01,1.427E-01,1.410E-01,1.393E-01,
1.376E-01,1.360E-01,1.344E-01,1.329E-01,1.313E-01,1.298E-01,1.284E-01,
1.269E-01,1.255E-01,1.241E-01,1.227E-01,1.214E-01,1.201E-01,1.188E-01,
1.175E-01,1.163E-01,1.151E-01,1.139E-01,1.127E-01,1.115E-01,1.104E-01,
1.093E-01,1.082E-01,1.071E-01]
        self.pond_ground_low_vf2f = [2.681E+00,1.549E+00,1.250E+00,1.087E+00,9.800E-01,9.006E-01,8.380E-01,
 7.864E-01,7.426E-01,7.047E-01,6.714E-01,6.417E-01,6.150E-01,5.908E-01,
5.687E-01,5.484E-01,5.296E-01,5.122E-01,4.960E-01,4.809E-01,4.667E-01,
4.534E-01,4.409E-01,4.290E-01,4.178E-01,4.072E-01,3.971E-01,3.875E-01,
3.783E-01,3.696E-01,3.613E-01,3.533E-01,3.456E-01,3.383E-01,3.313E-01,
3.246E-01,3.181E-01,3.118E-01,3.058E-01,3.000E-01,2.944E-01,2.890E-01,
2.838E-01,2.788E-01,2.739E-01,2.692E-01,2.646E-01,2.602E-01,2.559E-01,
2.517E-01,2.477E-01,2.438E-01,2.400E-01,2.363E-01,2.327E-01,2.292E-01,
2.258E-01,2.225E-01,2.193E-01,2.161E-01,2.131E-01,2.101E-01,2.072E-01,
2.043E-01,2.016E-01,1.989E-01,1.962E-01,1.937E-01,1.911E-01,1.887E-01,
1.863E-01,1.839E-01,1.816E-01,1.794E-01,1.772E-01,1.751E-01,1.730E-01,
1.709E-01,1.689E-01,1.669E-01,1.650E-01,1.631E-01,1.612E-01,1.594E-01,
1.576E-01,1.559E-01,1.542E-01,1.525E-01,1.508E-01,1.492E-01,1.476E-01,
1.461E-01,1.445E-01,1.430E-01,1.415E-01,1.401E-01,1.387E-01,1.373E-01,
1.359E-01,1.345E-01,1.332E-01]
        self.pond_ground_low_f2m = [1.090E+00,6.124E-01,5.272E-01,4.774E-01,4.422E-01,4.147E-01,3.922E-01,
3.730E-01,3.563E-01,3.416E-01,3.284E-01,3.165E-01,3.056E-01,2.956E-01,
2.863E-01,2.778E-01,2.698E-01,2.623E-01,2.553E-01,2.487E-01,2.425E-01,
2.366E-01,2.311E-01,2.258E-01,2.207E-01,2.159E-01,2.113E-01,2.069E-01,
2.027E-01,1.987E-01,1.948E-01,1.911E-01,1.876E-01,1.841E-01,1.808E-01,
1.776E-01,1.746E-01,1.716E-01,1.687E-01,1.659E-01,1.633E-01,1.607E-01,
1.581E-01,1.557E-01,1.533E-01,1.510E-01,1.488E-01,1.466E-01,1.445E-01,
1.425E-01,1.405E-01,1.385E-01,1.366E-01,1.348E-01,1.330E-01,1.312E-01,
1.295E-01,1.279E-01,1.263E-01,1.247E-01,1.231E-01,1.216E-01,1.201E-01,
1.187E-01,1.173E-01,1.159E-01,1.145E-01,1.132E-01,1.119E-01,1.107E-01,
1.094E-01,1.082E-01,1.070E-01,1.059E-01,1.047E-01,1.036E-01,1.025E-01,
1.014E-01,1.004E-01,9.935E-02,9.834E-02,9.734E-02,9.637E-02,9.541E-02,
9.447E-02,9.354E-02,9.263E-02,9.174E-02,9.087E-02,9.001E-02,8.916E-02,
8.833E-02,8.751E-02,8.671E-02,8.591E-02,8.514E-02,8.437E-02,8.362E-02,
8.288E-02,8.215E-02,8.143E-02]
        
    # #####one less value (begin)
         self.pond_aerial_vf2f = [2.425E+01,2.319E+01,2.227E+01,2.144E+01,2.069E+01,1.997E+01,1.930E+01,1.866E+01,1.806E+01,1.749E+01,1.696E+01,1.645E+01,1.596E+01,1.549E+01,1.506E+01,1.464E+01,1.425E+01,1.388E+01,1.353E+01,1.320E+01,1.288E+01,1.257E+01,1.228E+01,1.200E+01,1.174E+01,1.149E+01,1.125E+01,1.103E+01,1.081E+01,1.059E+01,1.039E+01,1.020E+01,1.001E+01,9.837E+00,9.670E+00,
            9.510E+00,9.350E+00,9.200E+00,9.058E+00,8.920E+00,8.780E+00,8.650E+00,8.520E+00,8.400E+00,8.290E+00,8.170E+00,8.060E+00,7.950E+00,7.850E+00,7.750E+00,7.650E+00,7.554E+00,7.460E+00,7.370E+00,7.290E+00,7.200E+00,7.120E+00,7.040E+00,6.960E+00,6.880E+00,6.810E+00,6.741E+00,6.670E+00,6.600E+00,6.540E+00,6.470E+00,6.410E+00,6.350E+00,6.290E+00,6.230E+00,6.170E+00,6.120E+00,6.060E+00,6.010E+00,5.960E+00,5.904E+00,5.850E+00,5.806E+00,5.760E+00,5.710E+00,5.670E+00,5.624E+00,5.580E+00,5.540E+00,5.490E+00,5.450E+00,5.413E+00,5.370E+00,5.340E+00,5.300E+00,5.260E+00,5.230E+00,5.190E+00,5.160E+00,5.120E+00,5.090E+00,5.060E+00,5.030E+00,5.000E+00,4.970E+00,4.940E+00]
         self.pond_aerial_f2m = [1.266E+01,1.142E+01,1.050E+01,9.757E+00,9.147E+00,8.623E+00,8.146E+00,
                        7.698E+00,7.271E+00,6.871E+00,6.509E+00,6.188E+00,5.899E+00,5.635E+00,
                        5.388E+00,5.160E+00,4.953E+00,4.765E+00,4.594E+00,4.437E+00,4.291E+00,
                        4.154E+00,4.025E+00,3.903E+00,3.789E+00,3.682E+00,3.581E+00,3.488E+00,
                        3.403E+00,3.323E+00,3.245E+00,3.170E+00,3.097E+00,3.027E+00,2.961E+00,
                        2.898E+00,2.839E+00,2.783E+00,2.729E+00,2.677E+00,2.627E+00,2.579E+00,
                        2.533E+00,2.488E+00,2.446E+00,2.405E+00,2.366E+00,2.329E+00,2.292E+00,
                        2.258E+00,2.225E+00,2.193E+00,2.162E+00,2.132E+00,2.104E+00,2.076E+00,
                        2.049E+00,2.023E+00,1.998E+00,1.974E+00,1.950E+00,1.928E+00,1.905E+00,
                        1.884E+00,1.863E+00,1.842E+00,1.823E+00,1.804E+00,1.785E+00,1.767E+00,
                        1.749E+00,1.732E+00,1.715E+00,1.698E+00,1.683E+00,1.667E+00,1.652E+00,
                        1.637E+00,1.623E+00,1.608E+00,1.595E+00,1.581E+00,1.568E+00,1.555E+00,
                        1.543E+00,1.531E+00,1.519E+00,1.507E+00,1.496E+00,1.485E+00,1.474E+00,
                        1.464E+00,1.454E+00,1.444E+00,1.434E+00,1.425E+00,1.416E+00,1.407E+00,
                        1.398E+00,1.389E+00,1.381E+00]
         self.pond_aerial_m2c = [8.918E+00,7.649E+00,6.759E+00,6.103E+00,5.593E+00,5.180E+00,4.829E+00,
 4.513E+00,4.217E+00,3.934E+00,3.670E+00,3.437E+00,3.239E+00,3.070E+00,
2.920E+00,2.782E+00,2.654E+00,2.535E+00,2.426E+00,2.324E+00,2.232E+00,
2.149E+00,2.072E+00,2.001E+00,1.933E+00,1.869E+00,1.808E+00,1.750E+00,
1.696E+00,1.645E+00,1.598E+00,1.553E+00,1.511E+00,1.471E+00,1.434E+00,
1.399E+00,1.365E+00,1.334E+00,1.304E+00,1.276E+00,1.249E+00,1.223E+00,
1.198E+00,1.175E+00,1.153E+00,1.132E+00,1.113E+00,1.094E+00,1.076E+00,
1.058E+00,1.041E+00,1.026E+00,1.010E+00,9.957E-01,9.816E-01,9.681E-01,
9.551E-01,9.427E-01,9.307E-01,9.191E-01,9.080E-01,8.972E-01,8.868E-01,
8.768E-01,8.671E-01,8.578E-01,8.487E-01,8.399E-01,8.313E-01,8.231E-01,
8.151E-01,8.073E-01,7.998E-01,7.926E-01,7.855E-01,7.787E-01,7.720E-01,
7.655E-01,7.591E-01,7.529E-01,7.468E-01,7.409E-01,7.352E-01,7.296E-01,
7.242E-01,7.188E-01,7.136E-01,7.085E-01,7.035E-01,6.986E-01,6.939E-01,
6.892E-01,6.847E-01,6.802E-01,6.758E-01,6.716E-01,6.674E-01,6.633E-01,
6.593E-01,6.554E-01,6.516E-01]
         self.pond_aerial_c2vc = [6.879E+00,5.622E+00,4.785E+00,4.190E+00,3.747E+00,3.401E+00,3.123E+00,&
 2.893E+00,2.692E+00,2.505E+00,2.331E+00,2.175E+00,2.043E+00,1.930E+00,
1.830E+00,1.738E+00,1.653E+00,1.574E+00,1.501E+00,1.434E+00,1.373E+00,
1.318E+00,1.268E+00,1.221E+00,1.178E+00,1.137E+00,1.099E+00,1.064E+00,
1.031E+00,1.000E+00,9.720E-01,9.456E-01,9.208E-01,8.977E-01,8.761E-01,
8.559E-01,8.369E-01,8.190E-01,8.020E-01,7.858E-01,7.705E-01,7.559E-01,
7.420E-01,7.287E-01,7.161E-01,7.039E-01,6.923E-01,6.811E-01,6.703E-01,
6.599E-01,6.497E-01,6.399E-01,6.304E-01,6.211E-01,6.121E-01,6.034E-01,
5.948E-01,5.865E-01,5.783E-01,5.703E-01,5.626E-01,5.550E-01,5.476E-01,
5.403E-01,5.332E-01,5.263E-01,5.194E-01,5.127E-01,5.062E-01,4.998E-01,
4.935E-01,4.874E-01,4.815E-01,4.756E-01,4.699E-01,4.643E-01,4.589E-01,
4.536E-01,4.484E-01,4.434E-01,4.384E-01,4.336E-01,4.290E-01,4.244E-01,
4.200E-01,4.157E-01,4.115E-01,4.075E-01,4.035E-01,3.997E-01,3.960E-01,
3.924E-01,3.889E-01,3.855E-01,3.822E-01,3.790E-01,3.759E-01,3.729E-01,
3.700E-01,3.671E-01,3.644E-01]
    #     self.terr_aerial_vf2f = [0.5000,0.4913,0.4564,0.4220,0.3588,0.3039,0.2247,0.1741,0.1403,0.1171,0.1010,0.0893,0.0799,0.0729,0.0671,0.0626,0.0585,0.0550,0.0519,0.0494,0.0475,0.0458,0.0442,0.0428,0.0416]
    #     self.terr_aerial_f2m = [0.4999,0.4808,0.4046,0.3365,0.2231,0.1712,0.0979,0.0638,0.0469,0.0374,0.0312,0.0266,0.0234,0.021,0.0192,0.0177,0.0164,0.0154,0.0146,0.0139,0.0133,0.0128,0.0124,0.012,0.0117]
    #     self.terr_aerial_m2c =[0.5,0.4776,0.3882,0.3034,0.1711,0.1114,0.0561,0.0346,0.0249,0.0188,0.015,0.0126,0.011,0.0098,0.0089,0.0082,0.0077,0.0072,0.0069,0.0065,0.0063,0.006,0.0058,0.0056,0.0055]
    #     self.terr_aerial_c2vc =[0.5,0.4776,0.3882,0.3034,0.1711,0.1114,0.0561,0.0346,0.0249,0.0188,0.015,0.0126,0.011,0.0098,0.0089,0.0082,0.0077,0.0072,0.0069,0.0065,0.0063,0.006,0.0058,0.0056,0.0055]
    #     self.terr_ground_vf2f = [1.06,0.8564,0.4475,0.2595,0.104,0.05,0.0248,0.0164,0.012,0.0093,0.0075,0.0062,0.0053,0.0045,0.0039,0.0034,0.003,0.0027,0.0024,0.0022,0.002,0.0018,0.0017,0.0015,0.0014]
    # #####one less value (end)

    #     self.terr_ground_f2m = [1.01,0.3731,0.0889,0.0459,0.0208,0.0119,0.007,0.0051,0.004,0.0033,0.0028,0.0024,0.0021,0.0019,0.0017,0.0015,0.0014,0.0013,0.0012,0.0011,0.001,0.0009,0.0009,0.0008,0.0008]
    #     self.pond_airblast_normal = [0.0011,0.0011,0.001,0.0009,0.0007,0.0005,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000978,0.0000863,0.0000769,0.0000629,0.0000626,0.0000571,0.0000523,0.0000482,0.0000446,0.0000414,0.0000386,0.0000361,0.0000339]
    #     self.pond_airblast_dense = [0.0145,0.014,0.0122,0.0106,0.0074,0.005,0.003,0.0022,0.0017,0.0014,0.0012,0.0011,0.001,0.0009,0.0008,0.0007,0.0007,0.0006,0.0006,0.0005,0.0005,0.0005,0.0005,0.0004,0.0004]
    #     self.pond_airblast_sparse = [0.0416,0.0395,0.0323,0.0258,0.015,0.0077,0.0031,0.0017,0.001,0.0007,0.0005,0.0004,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000898,0.0000771,0.0000668,0.0000583,0.0000513,0.0000453,0.0000405]
    #     self.pond_airblast_vineyard = [0.0024,0.0023,0.0018,0.0014,0.0009,0.0006,0.0003,0.0002,0.0002,0.0001,0.0001,0.0001,0.0000881,0.0000765,0.0000672,0.0000596,0.0000533,0.000048,0.0000435,0.0000397,0.0000363,0.0000334,0.0000309,0.0000286,0.0000267]
    #     self.pond_airblast_orchard = [0.0218,0.0208,0.0175,0.0145,0.0093,0.0056,0.0031,0.0021,0.0016,0.0013,0.0011,0.0009,0.0008,0.0007,0.0007,0.0006,0.0005,0.0005,0.0005,0.0004,0.0004,0.0004,0.0004,0.0003,0.0003]
    #     self.terr_airblast_normal = [0.0089,0.0081,0.0058,0.0042,0.0023,0.0012,0.0006,0.0004,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000965,0.0000765,0.0000625,0.0000523,0.0000446,0.0000387]
    #     self.terr_airblast_dense = [0.1155,0.1078,0.0834,0.0631,0.033,0.0157,0.0065,0.0038,0.0026,0.002,0.0016,0.0014,0.0012,0.0011,0.0009,0.0008,0.0007,0.0006,0.0005,0.0005]
    #     self.terr_airblast_sparse = [0.4763,0.4385,0.3218,0.2285,0.1007,0.0373,0.0103,0.0044,0.0023,0.0014,0.0009,0.0006,0.0005,0.0004,0.0003,0.0002,0.0001,0.0000889,0.0000665,0.0000514]
    #     self.terr_airblast_vineyard = [0.0376,0.0324,0.0195,0.012,0.0047,0.0019,0.0008,0.0004,0.0003,0.0002,0.0002,0.0001,0.0001,0.0001,0.000087,0.0000667,0.0000531,0.0000434,0.0000363,0.000031]
    #     self.terr_airblast_orchard = [0.2223,0.2046,0.1506,0.108,0.0503,0.021,0.0074,0.004,0.0026,0.0019,0.0015,0.0012,0.0011,0.0009,0.0008,0.0006,0.0005,0.0005,0.0004,0.0004]

    #     if (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Fine'):
    #         self.y = self.pond_aerial_vf2f
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Medium'):
    #         self.y = self.pond_aerial_f2m
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Coarse'):
    #         self.y = self.pond_aerial_m2c   
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Very Coarse'):
    #         self.y = self.pond_aerial_c2vc      
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Fine' and self.boom_height == 'Low'):
    #         self.y = self.pond_ground_low_vf2f
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Medium' and self.boom_height == 'Low'): 
    #         self.y = self.pond_ground_low_f2m
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Fine' and self.boom_height == 'High'):
    #         self.y = self.pond_ground_high_vf2f
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Medium' and self.boom_height == 'High'): 
    #         self.y = self.pond_ground_high_f2m
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Fine'):
    #         self.y = self.terr_aerial_vf2f
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Medium'):
    #         self.y = self.terr_aerial_f2m
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Coarse'):
    #         self.y = self.terr_aerial_m2c   
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Very Coarse'):
    #         self.y = self.terr_aerial_c2vc   
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Ground' and self.drop_size == 'Fine'):
    #         self.y = self.terr_ground_vf2f
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Ground' and self.drop_size == 'Medium'): 
    #         self.y = self.terr_ground_f2m  
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Normal'):
    #         self.y = self.pond_airblast_normal
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Dense'):
    #         self.y = self.pond_airblast_dense                        
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Sparse'):
    #         self.y = self.pond_airblast_sparse
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Vineyard'):
    #         self.y = self.pond_airblast_vineyard            
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Orchard'):
    #         self.y = pond_airblast_orchard
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Normal'):
    #         self.y = self.terr_airblast_normal
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]            
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Dense'):
    #         self.y = self.terr_airblast_dense
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Sparse'):
    #         self.y = self.terr_airblast_sparse
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Vineyard'):
    #         self.y = self.terr_airblast_vineyard
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
    #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.orchard_type == 'Orchard'):
    #         self.y = self.terr_airblast_orchard
    #         self.x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
    #         self.z = 4
    #     else:
    #         #print 2
    #         self.y = 3
    #     return self.x, self.y


    def extrapolate_from_fig(self, ecosystem_type, distance, bisect_left, x, y): 
        self.distance = int(self.distance)   
        if self.distance in self.x:
            y_index = x.index(self.distance)
            self.init_avg_dep_foa = self.y[y_index] 
        else:
            i= bisect_left(self.x, self.distance) #find largest distance closest to value
            low1 = self.x[i-1] #assign nearest lowest x value for interpolation
            high1 = self.x[i] #assign nearest highest x value for interpolation
            low_i = i-1    #assign index values to use to find nearest y values for interpolation            
            high_i = i      #assign index values to use to find nearest y values for interpolation
            self.init_avg_dep_foa = ((self.distance - low1) * (self.y[high_i] - self.y[low_i]) / (high1 - low1)) + self.y[low_i]
        return self.init_avg_dep_foa
       
    def extrapolate_from_fig2(self, ecosystem_type, init_avg_dep_foa, bisect_left, x, y):
        self.init_avg_dep_foa = float(self.init_avg_dep_foa)
        if self.init_avg_dep_foa in self.y:
            x_index = y.index(self.init_avg_dep_foa)
            self.distance = self.x[x_index]    
        else:
            i = min(enumerate(self.y), key=lambda x: abs(x[1]-self.init_avg_dep_foa)) #finds smallest closest value closest to input value
            #i = bisect_left(self.y, self.init_avg_dep_foa) #find largest foa closest to value
            #print self.y
            #print self.init_avg_dep_foa
            #print i[0]
            #print i[1]
            i2 = i[0]
            low1 = self.y[i2] #assign nearest lowest x value for interpolation
            high1 = self.y[i2-1] #assign nearest highest x value for interpolation
            low_i = i2    #assign index values to use to find nearest y values for interpolation            
            high_i = i2-1      #assign index values to use to find nearest y values for interpolation
            print self.y
            print low1
            print high1
            print low_i
            print high_i
            self.distance = ((self.init_avg_dep_foa - low1) * (self.x[high_i] - self.x[low_i]) / (high1 - low1)) + self.x[low_i]
        return self.distance

    def deposition_foa_to_lbac_f(self, init_avg_dep_foa, application_rate):
        self.application_rate = float(self.application_rate)
        self.avg_depo_lbac = self.init_avg_dep_foa * self.application_rate 
        #print self.avg_depo_lbac
        return self.avg_depo_lbac

    def deposition_lbac_to_gha_f(self, avg_depo_lbac):
        self.avg_depo_lbac = float(self.avg_depo_lbac)
        self.avg_depo_gha = self.avg_depo_lbac * (453.592) / 0.404686
        #print self.avg_depo_gha
        return self.avg_depo_gha    
    def deposition_gha_to_ngL_f(self, aquatic_type, avg_depo_gha):
        if (self.aquatic_type == '1'):

            self.deposition_ngL = self.avg_depo_gha * 0.05 * 1000
        else:
            self.deposition_ngL = self.avg_depo_gha * 0.05 * 1000 * (6.56 / 0.4921)
        return self.deposition_ngL

    def deposition_gha_to_mgcm_f(self, avg_depo_gha):
        self.deposition_mgcm = self.avg_depo_gha * 0.00001
        return self.deposition_mgcm

    def deposition_ngL_2_gha_f(self, deposition_ngL):
        self.deposition_ngL =float(self.deposition_ngL)
        if (self.aquatic_type == '1'):
            self.avg_depo_gha = self.deposition_ngL / (0.05 * 1000)
        else:
            self.avg_depo_gha = ((self.deposition_ngL / 6.56) * 0.4921) / (0.05 * 1000)
        return self.avg_depo_gha    

    def deposition_ghac_to_lbac_f(self, avg_depo_gha):
        self.avg_depo_gha = float(self.avg_depo_gha)
        self.avg_depo_lbac = (self.avg_depo_gha * 0.00220462 / 2.47105 ) 
        return self.avg_depo_lbac    

    def deposition_lbac_to_foa_f(self, avg_depo_lbac, application_rate):
        self.application_rate = float(self.application_rate)
        self.init_avg_dep_foa =  self.avg_depo_lbac / self.application_rate  
        return self.init_avg_dep_foa

    def deposition_mgcm_to_gha_f(self, deposition_mgcm):
        self.deposition_mgcm = float(self.deposition_mgcm)
        self.avg_depo_gha = self.deposition_mgcm /  0.00001 
        return self.avg_depo_gha




    
    
