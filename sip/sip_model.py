# Screening Imbibiton Program v1.0 (SIP)
import rest_funcs
import json
import logging
logger = logging.getLogger('SIP Model')
import os
import keys_Picloud_S3
import base64
# import urllib
# from google.appengine.api import urlfetch
import requests

# Daily water intake rate for birds

############Provide the key and connect to EC2####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
url_part1 = os.environ['UBERTOOL_REST_SERVER']
###########################################################################


class sip(object):
    def __init__(self, set_variables=True,run_methods=True,run_type = "single",chemical_name='', b_species='', m_species='', bw_quail=1, bw_duck=1, bwb_other=1, bw_rat=1, bwm_other=1, sol=1, ld50_a=1, ld50_m=1, aw_bird=1, mineau=1, aw_mamm=1, noaec_d=1, noaec_q=1, noaec_o=1, Species_of_the_bird_NOAEC_CHOICES=1, noael=1,vars_dict=None):
        self.set_default_variables()
        self.jid = rest_funcs.gen_jid()
        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.set_variables(run_type, chemical_name, b_species, m_species, bw_quail, bw_duck, bwb_other, bw_rat, bwm_other, sol, ld50_a, ld50_m, aw_bird, mineau, aw_mamm, noaec_d, noaec_q, noaec_o, Species_of_the_bird_NOAEC_CHOICES, noael)

    def set_default_variables(self):
        self.run_type = "single"
        self.chemical_name = ''
       # self.select_receptor()
        self.bw_bird = -1
        self.bw_quail = -1
        self.bw_duck = -1
        self.bwb_other = -1
        self.bw_rat = -1
        self.bwm_other = -1
        self.b_species = None
        self.m_species = None
        self.bw_mamm = -1
        self.sol = -1
        self.ld50_a = -1
        self.ld50_m = -1
        self.aw_bird = -1
        self.mineau = -1
        self.aw_mamm = -1
        self.noaec = -1
        self.noael = -1

    def set_variables(self, run_type, chemical_name, b_species, m_species, bw_quail, bw_duck, bwb_other, bw_rat, bwm_other, sol, ld50_a, ld50_m, aw_bird, mineau, aw_mamm, noaec_d, noaec_q, noaec_o, Species_of_the_bird_NOAEC_CHOICES, noael):
        self.run_type = run_type
        self.chemical_name = chemical_name
        self.bw_quail = bw_quail
        self.bw_duck = bw_duck
        self.bwb_other = bwb_other
        self.bw_rat = bw_rat
        self.bwm_other = bwm_other
        self.b_species = b_species
        self.m_species = m_species
        if b_species =='178':
            self.bw_bird = self.bw_quail
        elif b_species =='1580':
            self.bw_bird = self.bw_duck
        else:
            self.bw_bird = self.bwb_other
        if m_species =='350':
            self.bw_mamm = self.bw_rat
        else:
            self.bw_mamm = self.bwm_other
        self.sol = sol
        self.ld50_a = ld50_a
        self.ld50_m = ld50_m
        self.aw_bird = aw_bird
        self.mineau = mineau
        self.aw_mamm = aw_mamm
        self.noaec_d = noaec_d
        self.noaec_q = noaec_q
        self.noaec_o = noaec_o
        if Species_of_the_bird_NOAEC_CHOICES == '1':
            self.noaec = self.noaec_q
        elif Species_of_the_bird_NOAEC_CHOICES == '2':
            self.noaec = self.noaec_d
        elif Species_of_the_bird_NOAEC_CHOICES == '3':
            self.noaec = self.noaec_o
        # else:
        #     try:
        #         self.noaec = noaec
        #     except ValueError:
        #         raise ValueError\
        #         ('self.noaec=%g is a non-physical value.' % self.aw_bird)
        self.noael = noael

        all_dic = {"chemical_name":self.chemical_name, "bw_bird":self.bw_bird, "bw_quail":self.bw_quail, "bw_duck":self.bw_duck, "bwb_other":self.bwb_other, "bw_rat":self.bw_rat,
                   "bwm_other":self.bwm_other, "b_species":self.b_species, "m_species":self.m_species, "bw_mamm":self.bw_mamm, "sol":self.sol,
                   "ld50_a":self.ld50_a, "ld50_m":self.ld50_m, "aw_bird":self.aw_bird, "mineau":self.mineau, "aw_mamm":self.aw_mamm, "noaec":self.noaec, "noael":self.noael}
        data = json.dumps(all_dic)

        self.jid = rest_funcs.gen_jid()
        url=os.environ['UBERTOOL_REST_SERVER'] + '/sip/' + self.jid 
        # response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)
        response = requests.post(url, data=data, headers=http_headers, timeout=60)      
        output_val = json.loads(response.content)['result']
        for key, value in output_val.items():
            setattr(self, key, value)

    def set_unit_testing_variables(self):
        self.fw_bird_out_expected = None
        self.fw_mamm_out_expected = None
        self.dose_bird_out_expected = None
        self.dose_mamm_out_expected = None
        self.at_bird_out_expected = None
        self.at_mamm_out_expected = None
        self.fi_bird_out_expected = None
        self.det_out_expected = None
        self.act_out_expected = None
        self.acute_bird_out_expected = None
        self.acuconb_out_expected = None
        self.acute_mamm_out_expected = None
        self.acuconm_out_expected = None
        self.chron_bird_out_expected = None
        self.chronconb_out_expected = None
        self.chron_mamm_out_expected = None
        self.chronconm_out_expected = None


