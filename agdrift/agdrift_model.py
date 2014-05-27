import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from bisect import *
import logging
import rest_funcs
logger = logging.getLogger('agdrift Model')
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


class agdrift(object):
    def __init__(self, set_variables=True, run_methods=True, run_type='single', drop_size = '', ecosystem_type = '', application_method = '', boom_height = '', orchard_type = '', application_rate=1, distance=1,  aquatic_type='', calculation_input='', init_avg_dep_foa = 1, avg_depo_lbac = 1, avg_depo_gha  = 1, deposition_ngL = 1, deposition_mgcm = 1, nasae = 1, y = 1, x = 1, express_y = 1, vars_dict=None):
        self.set_default_variables()
        self.jid = rest_funcs.gen_jid()
        
        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.set_variables(run_type, drop_size, ecosystem_type, application_method, boom_height, orchard_type, application_rate, distance, aquatic_type, calculation_input, init_avg_dep_foa, avg_depo_gha, avg_depo_lbac, deposition_ngL, deposition_mgcm, nasae, y, x, express_y)

    def set_default_variables(self):
        #Currently used variables
        self.run_type = "single"
        self.drop_size = ''
        self.ecosystem_type = '' 
        self.application_method = ''
        self.boom_height = ''
        self.orchard_type = ''
        self.application_rate = 1
        self.distance = 1
        self.aquatic_type = ''
        self.calculation_input = ''
        self.init_avg_dep_foa = -1
        self.avg_depo_lbac = -1
        self.avg_depo_gha  = -1
        self.deposition_ngL = -1
        self.deposition_mgcm = -1
        self.nasae = -1
        self.y = -1
        self.x = -1
        self.express_y = -1
        self.loop_indx = '1'

    def set_variables(self, run_type, drop_size, ecosystem_type, application_method, boom_height, orchard_type, application_rate, distance, aquatic_type, calculation_input, init_avg_dep_foa, avg_depo_gha, avg_depo_lbac, deposition_ngL, deposition_mgcm, nasae, y, x, express_y):
        self.run_type = run_type
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
        self.nasae = nasae
        self.y = y
        self.x = x
        self.express_y = express_y  

        all_dic = {"drop_size":drop_size, "ecosystem_type":ecosystem_type, "application_method":application_method, 
                   "boom_height":boom_height, "orchard_type":orchard_type, "application_rate":application_rate, 
                   "distance":distance, "aquatic_type":aquatic_type, "calculation_input":calculation_input, 
                   "init_avg_dep_foa":init_avg_dep_foa, "avg_depo_gha":avg_depo_gha, "avg_depo_lbac":avg_depo_lbac, 
                   "deposition_ngL":deposition_ngL, "deposition_mgcm":deposition_mgcm, "nasae":nasae, "y":y, "x":x, 
                   "express_y":express_y}
        data = json.dumps(all_dic)

        self.jid = rest_funcs.gen_jid()
        url=os.environ['UBERTOOL_REST_SERVER'] + '/agdrift/' + self.jid 
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
        output_val = json.loads(response.content)['result']
        for key, value in output_val.items():
            setattr(self, key, value)
