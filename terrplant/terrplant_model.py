import rest_funcs
import json
import logging
logger = logging.getLogger('Terrplant Model')
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


class terrplant(object):
    def __init__(self, set_variables=True, run_methods=True, version_terrplant='1.2.2', run_type = "single", A=1, I=1, R=1, D=1, nms=1, lms=1, nds=1, lds=1,
            chemical_name='', pc_code='', use='', application_method='', application_form='', solubility=1, vars_dict=None,):
        self.set_default_variables()
        self.jid = rest_funcs.gen_jid()

        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.set_variables(version_terrplant,run_type,A,I,R,D,nms,lms,nds,lds,chemical_name,pc_code,use,application_method,application_form,solubility)

    def set_default_variables(self):
        #Currently used variables
        self.I = 1
        self.A = 1
        self.D = 1
        self.R = 1
        self.nms = 1
        self.nds = 1
        self.lms = 1
        self.lds = 1
        self.run_type = "single"
        #Variables in the input page
        self.version_terrplant = ''
        self.chemical_name = ''
        self.pc_code = ''
        self.use = ''
        self.application_method = ''
        self.application_form = ''
        self.solubility = 1
        self.nmv = 1
        self.ndv = 1
        self.lmv = 1
        self.ldv = 1

    def set_variables(self,version_terrplant,run_type,A,I,R,D,nms,lms,nds,lds,chemical_name,pc_code,use,application_method,application_form,solubility):
        self.version_terrplant = version_terrplant
        self.run_type = run_type
        self.A = A
        self.I = I
        self.R = R
        self.D = D
        self.nms = nms
        self.lms = lms
        self.nds = nds
        self.lds = lds
        self.chemical_name = chemical_name
        self.pc_code = pc_code
        self.use = use
        self.application_method = application_method
        self.application_form = application_form
        self.solubility = solubility

        all_dic = {"version_terrplant":self.version_terrplant, "run_type":self.run_type, "A":self.A, "I":self.I, "R":self.R, "D":self.D,
                   "nms":self.nms, "lms":self.lms, "nds":self.nds, "lds":self.lds, "chemical_name":self.chemical_name,
                   "pc_code":self.pc_code, "use":self.use, "application_method":self.application_method, "application_form":self.application_form, "solubility":self.solubility}
        data = json.dumps(all_dic)

        self.jid = rest_funcs.gen_jid()
        url=os.environ['UBERTOOL_REST_SERVER'] + '/terrplant/' + self.jid 
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
        output_val = json.loads(response.content)['result']
        for key, value in output_val.items():
            setattr(self, key, value)
            
            # self.rundry_results = self.output_val['rundry_results']
            # self.runsemi_results = self.output_val['runsemi_results']
            # self.totaldry_results = self.output_val['totaldry_results']
            # self.totalsemi_results = self.output_val['totalsemi_results']
            # self.spray_results = self.output_val['spray_results']
            # self.nmsRQdry_results = self.output_val['nmsRQdry_results']
            # self.LOCnmsdry_results = self.output_val['LOCnmsdry_results']
            # self.nmsRQsemi_results = self.output_val['nmsRQsemi_results']
            # self.LOCnmssemi_results = self.output_val['LOCnmssemi_results']
            # self.nmsRQspray_results = self.output_val['nmsRQspray_results']
            # self.LOCnmsspray_results = self.output_val['LOCnmsspray_results']
            # self.lmsRQdry_results = self.output_val['lmsRQdry_results']
            # self.LOClmsdry_results = self.output_val['LOClmsdry_results']
            # self.lmsRQsemi_results = self.output_val['lmsRQsemi_results']
            # self.LOClmssemi_results = self.output_val['LOClmssemi_results']
            # self.lmsRQspray_results = self.output_val['lmsRQspray_results']
            # self.LOClmsspray_results = self.output_val['LOClmsspray_results']
            # self.ndsRQdry_results = self.output_val['ndsRQdry_results']
            # self.LOCndsdry_results = self.output_val['LOCndsdry_results']
            # self.ndsRQsemi_results = self.output_val['ndsRQsemi_results']
            # self.LOCndssemi_results = self.output_val['LOCndssemi_results']
            # self.ndsRQspray_results = self.output_val['ndsRQspray_results']
            # self.LOCndsspray_results = self.output_val['LOCndsspray_results']
            # self.ldsRQdry_results = self.output_val['ldsRQdry_results']
            # self.LOCldsdry_results = self.output_val['LOCldsdry_results']
            # self.ldsRQsemi_results = self.output_val['ldsRQsemi_results']
            # self.LOCldssemi_results = self.output_val['LOCldssemi_results']
            # self.ldsRQspray_results = self.output_val['ldsRQspray_results']
            # self.LOCldsspray_results = self.output_val['LOCldsspray_results']

            # self.rundry_results_expected = self.output_val['rundry_results_expected']
            # self.runsemi_results_expected = self.output_val['runsemi_results_expected']
            # self.spray_results_expected = self.output_val['spray_results_expected']
            # self.totaldry_results_expected = self.output_val['totaldry_results_expected']
            # self.totalsemi_results_expected = self.output_val['totalsemi_results_expected']
            # self.nmsRQdry_results_expected = self.output_val['nmsRQdry_results_expected']
            # self.nmsRQsemi_results_expected = self.output_val['nmsRQsemi_results_expected']
            # self.nmsRQspray_results_expected = self.output_val['nmsRQspray_results_expected']
            # self.lmsRQdry_results_expected = self.output_val['lmsRQdry_results_expected']
            # self.lmsRQsemi_results_expected = self.output_val['lmsRQsemi_results_expected']
            # self.lmsRQspray_results_expected = self.output_val['lmsRQspray_results_expected']
            # self.ndsRQdry_results_expected = self.output_val['ndsRQdry_results_expected']
            # self.ndsRQsemi_results_expected = self.output_val['ndsRQsemi_results_expected']
            # self.ndsRQspray_results_expected = self.output_val['ndsRQspray_results_expected']
            # self.ldsRQdry_results_expected = self.output_val['ldsRQdry_results_expected']
            # self.ldsRQsemi_results_expected = self.output_val['ldsRQsemi_results_expected']
            # self.ldsRQspray_results_expected = self.output_val['ldsRQspray_results_expected']

        # if run_type == "batch":
        #     response = ""
        #     while response =="":
        #         response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
        #     self.output_val = json.loads(response.content)['result']

