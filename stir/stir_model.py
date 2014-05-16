import numpy as np
import logging
logger = logging.getLogger('stir Model')
import sys
import math
import json
import rest_funcs
import os
import keys_Picloud_S3
import base64
import urllib
from google.appengine.api import urlfetch

############Provide the key and connect to EC2####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
url_part1 = os.environ['UBERTOOL_REST_SERVER']
###########################################################################

class StirModel(object):
    def __init__(self,set_variables=True, run_methods=True, run_type = "single",
            chemical_name=None,application_rate=None,column_height=None,spray_drift_fraction=None,direct_spray_duration=None, 
            molecular_weight=None,vapor_pressure=None,avian_oral_ld50=None, body_weight_assessed_bird=None, body_weight_tested_bird=None, 
            mineau_scaling_factor=None,mammal_inhalation_lc50=None,duration_mammal_inhalation_study=None,body_weight_assessed_mammal=None, 
            body_weight_tested_mammal=None,mammal_oral_ld50=None,
            vars_dict=None):
        self.set_default_variables()
        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.set_variables(run_type,chemical_name,application_rate,column_height,spray_drift_fraction,direct_spray_duration, 
                    molecular_weight,vapor_pressure,avian_oral_ld50, body_weight_assessed_bird, body_weight_tested_bird, mineau_scaling_factor, 
                    mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal, body_weight_tested_mammal, 
                    mammal_oral_ld50)

    def set_default_variables(self):
        #inputs
        self.jid = rest_funcs.gen_jid()
        self.run_type = 'single'
        self.chemical_name = ''
        self.application_rate = 1
        self.column_height = 1
        self.spray_drift_fraction = 1
        self.direct_spray_duration = 1
        self.molecular_weight = 1
        self.vapor_pressure = 1
        self.avian_oral_ld50 = 1
        self.body_weight_assessed_bird = 1
        self.body_weight_tested_bird = 1
        self.mineau_scaling_factor = 1
        self.mammal_inhalation_lc50 = 1
        self.duration_mammal_inhalation_study = 1
        self.body_weight_assessed_mammal = 1
        self.body_weight_tested_mammal = 1
        self.mammal_oral_ld50 = 1
        self.run_type = "single"



    # def __str__(self):
    #     #inputs
    #     string_rep = ''
    #     string_rep = string_rep + self.chemical_name + "\n"
    #     string_rep = string_rep + "application_rate = %.2e \n" % self.application_rate
    #     string_rep = string_rep + "column_height = %.2e \n" % self.column_height
    #     string_rep = string_rep + "spray_drift_fraction = %.2e \n" % self.spray_drift_fraction
    #     string_rep = string_rep + "direct_spray_duration = %.2e \n" % self.direct_spray_duration
    #     string_rep = string_rep + "molecular_weight = %.2e \n" % self.molecular_weight
    #     string_rep = string_rep + "vapor_pressure = %.2e \n" % self.vapor_pressure
    #     string_rep = string_rep + "avian_oral_ld50 = %.2e \n" % self.avian_oral_ld50
    #     string_rep = string_rep + "body_weight_assessed_bird = %.2e \n" % self.body_weight_assessed_bird
    #     string_rep = string_rep + "body_weight_tested_bird = %.2e \n" % self.body_weight_tested_bird
    #     string_rep = string_rep + "mineau_scaling_factor = %.2e \n" % self.mineau_scaling_factor
    #     string_rep = string_rep + "mammal_inhalation_lc50 = %.2e \n" % self.mammal_inhalation_lc50
    #     string_rep = string_rep + "duration_mammal_inhalation_study = %.2e \n" % self.duration_mammal_inhalation_study
    #     string_rep = string_rep + "body_weight_assessed_mammal = %.2e \n" % self.body_weight_assessed_mammal
    #     string_rep = string_rep + "body_weight_tested_mammal = %.2e \n" % self.body_weight_tested_mammal
    #     string_rep = string_rep + "mammal_oral_ld50 = %.2e \n" % self.mammal_oral_ld50
    #     #outputs
    #     string_rep = string_rep + "sat_air_conc = %.2e \n" % self.sat_air_conc
    #     string_rep = string_rep + "inh_rate_avian = %.2e \n" % self.inh_rate_avian
    #     string_rep = string_rep + "vid_avian = %.2e \n" % self.vid_avian
    #     string_rep = string_rep + "inh_rate_mammal = %.2e \n" % self.inh_rate_mammal
    #     string_rep = string_rep + "vid_mammal = %.2e \n" % self.vid_mammal
    #     string_rep = string_rep + "ar2 = %.2e \n" % self.ar2
    #     string_rep = string_rep + "air_conc = %.2e \n" % self.air_conc
    #     string_rep = string_rep + "sid_avian = %.2e \n" % self.sid_avian
    #     string_rep = string_rep + "sid_mammal = %.2e \n" % self.sid_mammal
    #     string_rep = string_rep + "cf = %.2e \n" % self.cf
    #     string_rep = string_rep + "mammal_inhalation_ld50 = %.2e \n" % self.self.mammal_inhalation_ld50
    #     string_rep = string_rep + "adjusted_mammal_inhalation_ld50 = %.2e \n" % self.adjusted_mammal_inhalation_ld50
    #     string_rep = string_rep + "estimated_avian_inhalation_ld50 = %.2e \n" % self.estimated_avian_inhalation_ld50
    #     string_rep = string_rep + "adjusted_avian_inhalation_ld50 = %.2e \n" % self.adjusted_avian_inhalation_ld50
    #     string_rep = string_rep + "ratio_vid_avian = %.2e \n" % self.ratio_vid_avian
    #     string_rep = string_rep + "ratio_sid_avian = %.2e \n" % self.ratio_sid_avian
    #     string_rep = string_rep + "ratio_vid_mammal = %.2e \n" % self.ratio_vid_mammal
    #     string_rep = string_rep + "ratio_sid_mammal = %.2e \n" % self.ratio_sid_mammal
    #     string_rep = string_rep + "loc_vid_avian =" + self.loc_vid_avian + "\n"
    #     string_rep = string_rep + "loc_sid_avian =" + self.loc_sid_avian + "\n"
    #     string_rep = string_rep + "loc_vid_mammal =" + self.loc_vid_mammal + "\n"
    #     string_rep = string_rep + "loc_sid_mammal =" + self.loc_sid_mammal + "\n"
        # return string_rep

    def set_variables(self,run_type,chemical_name,application_rate,column_height,spray_drift_fraction,direct_spray_duration, 
            molecular_weight,vapor_pressure,avian_oral_ld50,body_weight_assessed_bird,body_weight_tested_bird,mineau_scaling_factor, 
            mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal,body_weight_tested_mammal, 
            mammal_oral_ld50):
        self.run_type = run_type
        self.chemical_name = chemical_name
        self.application_rate = application_rate
        self.column_height = column_height
        self.spray_drift_fraction = spray_drift_fraction
        self.direct_spray_duration = direct_spray_duration
        self.molecular_weight = molecular_weight
        self.vapor_pressure = vapor_pressure
        self.avian_oral_ld50 = avian_oral_ld50
        self.body_weight_assessed_bird = body_weight_assessed_bird
        self.body_weight_tested_bird = body_weight_tested_bird
        self.mineau_scaling_factor = mineau_scaling_factor
        self.mammal_inhalation_lc50 = mammal_inhalation_lc50
        self.duration_mammal_inhalation_study = duration_mammal_inhalation_study
        self.body_weight_assessed_mammal = body_weight_assessed_mammal
        self.body_weight_tested_mammal = body_weight_tested_mammal
        self.mammal_oral_ld50 = mammal_oral_ld50

        all_dic = {"run_type":self.run_type, "chemical_name":self.chemical_name, "application_rate":self.application_rate, "column_height":self.column_height, "spray_drift_fraction":self.spray_drift_fraction, "direct_spray_duration":self.direct_spray_duration, "molecular_weight":self.molecular_weight,
                   "vapor_pressure":self.vapor_pressure, "avian_oral_ld50":self.avian_oral_ld50, "body_weight_assessed_bird":self.body_weight_assessed_bird, "body_weight_tested_bird":self.body_weight_tested_bird, "body_weight_tested_bird":self.body_weight_tested_bird,
                   "mineau_scaling_factor":self.mineau_scaling_factor, "mammal_inhalation_lc50":self.mammal_inhalation_lc50, "duration_mammal_inhalation_study":self.duration_mammal_inhalation_study, "body_weight_assessed_mammal":self.body_weight_assessed_mammal, "body_weight_tested_mammal":self.body_weight_tested_mammal, "mammal_oral_ld50":self.mammal_oral_ld50}
        data = json.dumps(all_dic)

        self.jid = rest_funcs.gen_jid()
        url=os.environ['UBERTOOL_REST_SERVER'] + '/stir/' + self.jid 
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
        output_val = json.loads(response.content)['result']
        for key, value in output_val.items():
            setattr(self, key, value)

    def set_unit_testing_variables(self):
        self.chemical_name_expected = None
        self.sat_air_conc_expected = None
        self.inh_rate_avian_expected = None
        self.vid_avian_expected = None
        self.inh_rate_mammal_expected = None
        self.vid_mammal_expected = None
        self.ar2_expected = None
        self.air_conc_expected = None
        self.sid_avian_expected = None
        self.sid_mammal_expected = None
        self.cf_expected = None
        self.mammal_inhalation_ld50_expected = None
        self.adjusted_mammal_inhalation_ld50_expected = None
        self.estimated_avian_inhalation_ld50_expected = None
        self.adjusted_avian_inhalation_ld50_expected = None
        self.ratio_vid_avian_expected = None
        self.ratio_sid_avian_expected = None
        self.ratio_vid_mammal_expected = None
        self.ratio_sid_mammal_expected = None
        self.loc_vid_avian_expected = None
        self.loc_sid_avian_expected = None
        self.loc_vid_mammal_expected = None
        self.loc_sid_mammal_expected = None
