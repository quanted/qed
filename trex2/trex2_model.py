import logging
import sys
logger = logging.getLogger('trex2 model')
import rest_funcs
import json
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

#food intake for birds
class trex2(object):
    def __init__(self, run_type, chem_name, use, formu_name, a_i, Application_type, seed_treatment_formulation_name, seed_crop, seed_crop_v, r_s, b_w, p_i, den, h_l, n_a, ar_lb, day_out,
              ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, aw_bird_sm, aw_bird_md, aw_bird_lg, 
              Species_of_the_tested_bird_avian_ld50, Species_of_the_tested_bird_avian_lc50, Species_of_the_tested_bird_avian_NOAEC, Species_of_the_tested_bird_avian_NOAEL, 
              tw_bird_ld50, tw_bird_lc50, tw_bird_NOAEC, tw_bird_NOAEL, x, ld50_mamm, lc50_mamm, NOAEC_mamm, NOAEL_mamm, aw_mamm_sm, aw_mamm_md, aw_mamm_lg, tw_mamm,
              m_s_r_p):
        self.jid = rest_funcs.gen_jid()
        self.run_type=run_type
        self.chem_name=chem_name
        self.use=use
        self.formu_name=formu_name
        self.a_i=a_i
        self.a_i_t1=100*float(a_i)
        self.Application_type=Application_type
        self.seed_treatment_formulation_name=seed_treatment_formulation_name
        self.seed_crop=seed_crop
        self.seed_crop_v=seed_crop_v
        self.r_s=r_s
        self.b_w=b_w
        self.b_w_t1=12*float(b_w)
        self.p_i=p_i
        try:
            self.p_i_t1=100*float(p_i)
        except:
            self.p_i_t1='N/A'
        self.den=den
        self.h_l=h_l
        self.n_a=n_a
        self.ar_lb=ar_lb
        self.day_out=day_out
        self.ld50_bird=ld50_bird
        self.lc50_bird=lc50_bird
        self.NOAEC_bird=NOAEC_bird
        self.NOAEL_bird=NOAEL_bird
        self.aw_bird_sm=aw_bird_sm
        self.aw_bird_md=aw_bird_md
        self.aw_bird_lg=aw_bird_lg

        self.Species_of_the_tested_bird_avian_ld50=Species_of_the_tested_bird_avian_ld50
        self.Species_of_the_tested_bird_avian_lc50=Species_of_the_tested_bird_avian_lc50
        self.Species_of_the_tested_bird_avian_NOAEC=Species_of_the_tested_bird_avian_NOAEC
        self.Species_of_the_tested_bird_avian_NOAEL=Species_of_the_tested_bird_avian_NOAEL

        self.tw_bird_ld50=tw_bird_ld50
        self.tw_bird_lc50=tw_bird_lc50
        self.tw_bird_NOAEC=tw_bird_NOAEC
        self.tw_bird_NOAEL=tw_bird_NOAEL
        self.x=x
        self.ld50_mamm=ld50_mamm
        self.lc50_mamm=lc50_mamm
        self.NOAEC_mamm=NOAEC_mamm
        self.NOAEL_mamm=NOAEL_mamm
        self.aw_mamm_sm=aw_mamm_sm
        self.aw_mamm_md=aw_mamm_md
        self.aw_mamm_lg=aw_mamm_lg
        self.tw_mamm=tw_mamm
        self.m_s_r_p=m_s_r_p

        all_dic = {"chem_name":self.chem_name, "use":self.use, "formu_name":self.formu_name, "a_i":self.a_i, 
                   "Application_type":self.Application_type, "seed_treatment_formulation_name":self.seed_treatment_formulation_name, 
                   "seed_crop":self.seed_crop, "seed_crop_v":self.seed_crop_v, "r_s":self.r_s, "b_w":self.b_w, "p_i":self.p_i, 
                   "den":self.den, "h_l":self.h_l, "n_a":self.n_a, "ar_lb":self.ar_lb, "day_out":self.day_out, "ld50_bird":self.ld50_bird, 
                   "lc50_bird":self.lc50_bird, "NOAEC_bird":self.NOAEC_bird, "NOAEL_bird":self.NOAEL_bird, "aw_bird_sm":self.aw_bird_sm, 
                   "aw_bird_md":self.aw_bird_md, "aw_bird_lg":self.aw_bird_lg, "Species_of_the_tested_bird_avian_ld50":self.Species_of_the_tested_bird_avian_ld50, 
                   "Species_of_the_tested_bird_avian_lc50":self.Species_of_the_tested_bird_avian_lc50, "Species_of_the_tested_bird_avian_NOAEC":self.Species_of_the_tested_bird_avian_NOAEC, 
                   "Species_of_the_tested_bird_avian_NOAEL":self.Species_of_the_tested_bird_avian_NOAEL, "tw_bird_ld50":self.tw_bird_ld50, "tw_bird_lc50":self.tw_bird_lc50, 
                   "tw_bird_NOAEC":self.tw_bird_NOAEC, "tw_bird_NOAEL":self.tw_bird_NOAEL, "x":self.x, "ld50_mamm":self.ld50_mamm, "lc50_mamm":self.lc50_mamm, "NOAEC_mamm":self.NOAEC_mamm, 
                   "NOAEL_mamm":self.NOAEL_mamm, "aw_mamm_sm":self.aw_mamm_sm, "aw_mamm_md":self.aw_mamm_md, "aw_mamm_lg":self.aw_mamm_lg, "tw_mamm":self.tw_mamm, "m_s_r_p":self.m_s_r_p}
        data = json.dumps(all_dic)

        self.jid = rest_funcs.gen_jid()
        url=os.environ['UBERTOOL_REST_SERVER'] + '/trex2/' + self.jid 
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
        output_val = json.loads(response.content, cls=rest_funcs.NumPyDecoder)['result']
        output_val_uni=json.loads(output_val, cls=rest_funcs.NumPyDecoder)
        for key, value in output_val_uni.items():
            setattr(self, key, value)


