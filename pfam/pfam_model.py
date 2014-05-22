# -*- coding: utf-8 -*-
import keys_Picloud_S3
import base64
import urllib
from google.appengine.api import urlfetch
import json
import os
import logging
import rest_funcs

############Provide the key and connect to EC2####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
url_part1 = os.environ['UBERTOOL_REST_SERVER']
###########################################################################         

def get_jid(wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
           noa,dd_out,mm_out,ma_out,sr_out,weather,wea_l,nof,date_f1,nod_out,fl_out,wl_out,ml_out,to_out,
           zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
           ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10,area_app):
    all_dic = {"wat_hl" : wat_hl,
               "wat_t" : wat_t,
               "ben_hl" : ben_hl,
               "ben_t" : ben_t,
               "unf_hl" : unf_hl,
               "unf_t" : unf_t,
               "aqu_hl" : aqu_hl,
               "aqu_t" : aqu_t,
               "hyd_hl" : hyd_hl,
               "mw" : mw,
               "vp" : vp,
               "sol" : sol,
               "koc" : koc,
               "hea_h" : hea_h,
               "hea_r_t" : hea_r_t,
               "noa" : noa,
               "dd_out" : dd_out,
               "mm_out" : mm_out,
               "ma_out" : ma_out,
               "sr_out" : sr_out,
               "weather" : weather,
               "wea_l" : wea_l,
               "nof" : nof,
               "date_f1" : date_f1,
               "nod_out" : nod_out,
               "fl_out" : fl_out,
               "wl_out" : wl_out,
               "ml_out" : ml_out,
               "to_out" : to_out,
               "zero_height_ref" : zero_height_ref,
               "days_zero_full" : days_zero_full,
               "days_zero_removal" : days_zero_removal,
               "max_frac_cov" : max_frac_cov,
               "mas_tras_cof" : mas_tras_cof,
               "leak" : leak,
               "ref_d" : ref_d,
               "ben_d" : ben_d,
               "ben_por" : ben_por,
               "dry_bkd" : dry_bkd,
               "foc_wat" : foc_wat,
               "foc_ben" : foc_ben,
               "ss" : ss,
               "wat_c_doc" : wat_c_doc,
               "chl" : chl,
               "dfac" : dfac,
               "q10" : q10,
               "area_app" : area_app}

    data=json.dumps(all_dic)
    jid=rest_funcs.gen_jid()
    url=url_part1 + '/pfam/' + jid
    response_val = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)
    output_val = json.loads(response_val.content)['result']
    return(jid, output_val)

class pfam(object):
    def __init__(self,wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
                 noa,dd_out,mm_out,ma_out,sr_out,weather, wea_l,nof,date_f1,nod_out,fl_out,wl_out,ml_out,to_out,
                 zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
                 ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10,area_app):
      self.wat_hl = wat_hl
      self.wat_t = wat_t
      self.ben_hl = ben_hl
      self.ben_t = ben_t
      self.unf_hl = unf_hl
      self.unf_t = unf_t
      self.aqu_hl = aqu_hl
      self.aqu_t = aqu_t
      self.hyd_hl = hyd_hl
      self.mw = mw
      self.vp = vp
      self.sol = sol
      self.koc = koc
      self.hea_h = hea_h
      self.hea_r_t = hea_r_t

      self.noa = noa
      self.dd_out = dd_out
      self.mm_out = mm_out
      self.ma_out = ma_out
      self.sr_out = sr_out
      self.weather = weather
      self.wea_l = wea_l
      self.nof = nof
      self.date_f1 = date_f1
      self.nod_out = nod_out
      self.fl_out = fl_out
      self.wl_out = wl_out
      self.ml_out = ml_out
      self.to_out = to_out

      self.zero_height_ref = zero_height_ref
      self.days_zero_full = days_zero_full
      self.days_zero_removal = days_zero_removal
      self.max_frac_cov = max_frac_cov
      self.mas_tras_cof = mas_tras_cof
      self.leak = leak
      self.ref_d = ref_d
      self.ben_d = ben_d

      self.ben_por = ben_por
      self.dry_bkd = dry_bkd
      self.foc_wat = foc_wat
      self.foc_ben = foc_ben
      self.ss = ss
      self.wat_c_doc = wat_c_doc
      self.chl = chl
      self.dfac = dfac
      self.q10 = q10
      self.area_app = area_app
        
      self.final_res=get_jid(self.wat_hl, self.wat_t, self.ben_hl, self.ben_t, self.unf_hl, self.unf_t, self.aqu_hl, self.aqu_t, self.hyd_hl, self.mw, self.vp, self.sol, self.koc, self.hea_h, self.hea_r_t, self.noa,
                             self.dd_out, self.mm_out, self.ma_out, self.sr_out, self.weather, self.wea_l, self.nof, self.date_f1, self.nod_out, self.fl_out, self.wl_out, self.ml_out, self.to_out, 
                             self.zero_height_ref, self.days_zero_full, self.days_zero_removal, self.max_frac_cov, self.mas_tras_cof, self.leak, self.ref_d, self.ben_d, self.ben_por, self.dry_bkd, self.foc_wat, self.foc_ben,
                             self.ss, self.wat_c_doc, self.chl, self.dfac, self.q10, self.area_app)
      self.jid = self.final_res[0]
