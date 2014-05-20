import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import logging
import rest_funcs
logger = logging.getLogger('RICE Model')
import os
import keys_Picloud_S3
import base64
import urllib
from google.appengine.api import urlfetch
import json

# Daily water intake rate for birds

############Provide the key and connect to EC2####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
url_part1 = os.environ['UBERTOOL_REST_SERVER']
###########################################################################


class rice(object):
    def __init__(self, set_variables=True,run_methods=True,run_type = "single",chemical_name='', mai=1, dsed=1, a=1, pb=1, dw=1, osed=1, kd=1, vars_dict=None):
        self.set_default_variables()
        self.jid = rest_funcs.gen_jid()
        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.chemical_name = chemical_name
                self.mai = mai
                self.dsed = dsed
                self.a = a
                self.pb = pb
                self.dw = dw
                self.osed = osed
                self.kd = kd
                self.run_type = run_type

                all_dic = {"chemical_name":self.chemical_name, "mai":self.mai, "dsed":self.dsed, "a":self.a, "pb":self.pb, "dw":self.dw,
                           "osed":self.osed, "kd":self.kd}
                data = json.dumps(all_dic)

                self.jid = rest_funcs.gen_jid()
                url=os.environ['UBERTOOL_REST_SERVER'] + '/rice/' + self.jid 
                response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
                output_val = json.loads(response.content)['result']
                for key, value in output_val.items():
                    setattr(self, key, value)

    def set_default_variables(self):
        self.run_type = "single"
        self.chemical_name = ''
        self.mai = -1
        self.dsed = -1
        self.a = -1
        self.pb = -1
        self.dw = -1
        self.osed = -1
        self.kd = -1
