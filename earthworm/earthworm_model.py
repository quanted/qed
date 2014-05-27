# Earthworm Fugacity Modeling (earthworm)

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import logging
logger = logging.getLogger('earthworm Model')
import rest_funcs
import json
import keys_Picloud_S3
import base64
import urllib
from google.appengine.api import urlfetch


# Daily water intake rate for birds

############Provide the key and connect to EC2####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
url_part1 = os.environ['UBERTOOL_REST_SERVER']
###########################################################################

class earthworm(object):
    def __init__(self, set_variables=True,run_methods=True,k_ow=1,l_f_e=1,c_s=1,k_d=1,p_s=1,c_w=1,m_w=1,p_e=1,vars_dict=None):
        self.set_default_variables()
        self.jid = rest_funcs.gen_jid()
        
        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.k_ow = k_ow
                self.l_f_e = l_f_e
                self.c_s = c_s
                self.k_d = k_d
                self.p_s = p_s
                self.c_w = c_w
                self.m_w = m_w
                self.p_e = p_e

                all_dic = {"k_ow":self.k_ow, "l_f_e":self.l_f_e, "c_s":self.c_s, "k_d":self.k_d, "p_s":self.p_s, "c_w":self.c_w,
                           "m_w":self.m_w, "p_e":self.p_e}
                data = json.dumps(all_dic)

                self.jid = rest_funcs.gen_jid()
                url=os.environ['UBERTOOL_REST_SERVER'] + '/earthworm/' + self.jid 
                response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
                output_val = json.loads(response.content)['result']
                for key, value in output_val.items():
                    setattr(self, key, value)

    def set_default_variables(self):
        self.k_ow = -1
        self.l_f_e = -1
        self.c_s = -1
        self.k_d = -1
        self.p_s = -1
        self.c_w = -1
        self.m_w = -1
        self.p_e = -1
        self.earthworm_fugacity_out = -1
