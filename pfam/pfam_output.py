# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import math 
import cgitb
import json
cgitb.enable()
from pfam import pfam_model, pfam_tables
import base64
import urllib
from google.appengine.api import urlfetch
from uber import uber_lib
import rest_funcs
import keys_Picloud_S3


class PFAMOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        ######Chemical#######        
        wat_hl = form.getvalue('wat_hl')
        wat_t = form.getvalue('wat_t')
        ben_hl = form.getvalue('ben_hl')
        ben_t = form.getvalue('ben_t')
        unf_hl = form.getvalue('unf_hl')
        unf_t = form.getvalue('unf_t')
        aqu_hl = form.getvalue('aqu_hl')
        aqu_t = form.getvalue('aqu_t')
        hyd_hl = form.getvalue('hyd_hl')
        mw = form.getvalue('mw')
        vp = form.getvalue('vp')
        sol = form.getvalue('sol')
        koc = form.getvalue('koc')
        hea_h = form.getvalue('hea_h')
        hea_r_t = form.getvalue('hea_r_t')
        ######Application#######        
        noa = form.getvalue('noa')
        mm_out = np.zeros(shape=(int(noa),1))
        dd_out = np.zeros(shape=(int(noa),1))
        ma_out = np.zeros(shape=(int(noa),1))
        sr_out = np.zeros(shape=(int(noa),1))
        for i in range(int(noa)):
            j=i+1
            mm_temp = form.getvalue('mm'+str(j))
            mm_out[i,] = int(mm_temp) 
            dd_temp = form.getvalue('dd'+str(j))
            dd_out[i,] = int(dd_temp)         
            ma_temp = form.getvalue('ma'+str(j))
            ma_out[i,] = ma_temp   
            sr_temp = form.getvalue('sr'+str(j))
            sr_out[i,] = sr_temp
                      
        ######Location#######        
        weather = form.getvalue('weather')
        wea_l = form.getvalue('wea_l')
        ######Floods#######    
        nof = form.getvalue('nof')
        date_f1 = form.getvalue('date_f1')
        nod_out = np.zeros(shape=(int(nof),1))
        fl_out = np.zeros(shape=(int(nof),1))
        wl_out = np.zeros(shape=(int(nof),1))
        ml_out = np.zeros(shape=(int(nof),1))
        to_out = np.zeros(shape=(int(nof),1))
        for k in range(int(nof)):
            jj=k+1
            if (jj==1):
                nod_out[k,] = int(0)
            else:                
                nod_temp = form.getvalue('nod'+str(jj))
                nod_out[k,] = int(nod_temp) 
            fl_temp = form.getvalue('fl'+str(jj))
            fl_out[k,] = fl_temp         
            wl_temp = form.getvalue('wl'+str(jj))
            wl_out[k,] = wl_temp   
            ml_temp = form.getvalue('ml'+str(jj))
            ml_out[k,] = ml_temp  
            to_temp = form.getvalue('to'+str(jj))
            to_out[k,] = to_temp                  
        ######Crop#######    
        zero_height_ref = form.getvalue('zero_height_ref')
        days_zero_full = form.getvalue('days_zero_full')
        days_zero_removal = form.getvalue('days_zero_removal')
        max_frac_cov = form.getvalue('max_frac_cov')
        ######Physical#######    
        mas_tras_cof = form.getvalue('mas_tras_cof')
        leak = form.getvalue('leak')
        ref_d = form.getvalue('ref_d')
        ben_d = form.getvalue('ben_d')
        ben_por = form.getvalue('ben_por')
        dry_bkd = form.getvalue('dry_bkd')
        foc_wat = form.getvalue('foc_wat')
        foc_ben = form.getvalue('foc_ben')
        ss = form.getvalue('ss')
        wat_c_doc = form.getvalue('wat_c_doc')
        chl = form.getvalue('chl')
        dfac = form.getvalue('dfac')
        q10 = form.getvalue('q10')
        ######Output#######  
        area_app = form.getvalue('area_app')
        
        pfam_obj=pfam_model.pfam(wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
                            noa,dd_out.tolist(),mm_out.tolist(),ma_out.tolist(),sr_out.tolist(),weather, wea_l,
                            nof,date_f1,nod_out.tolist(),fl_out.tolist(),wl_out.tolist(),ml_out.tolist(),to_out.tolist(),
                            zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
                            ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10,area_app)
        
        x_date1=json.dumps(pfam_obj.final_res[1][1]) 
        x_re_v_f = [float(i) for i in pfam_obj.final_res[1][2]]
        x_re_c_f = [float(i) for i in pfam_obj.final_res[1][3]]
        setattr(pfam_obj, "x_date1", x_date1)
        setattr(pfam_obj, "x_re_v_f", x_re_v_f)
        setattr(pfam_obj, "x_re_c_f", x_re_c_f)

        x_date2=json.dumps(pfam_obj.final_res[1][4]) 
        x_water = [float(i) for i in pfam_obj.final_res[1][5]]
        x_water_level = [float(i) for i in pfam_obj.final_res[1][6]]
        x_ben_tot = [float(i) for i in pfam_obj.final_res[1][7]]
        x_ben_por = [float(i)*1000000 for i in pfam_obj.final_res[1][8]]
        setattr(pfam_obj, "x_date2", x_date2)
        setattr(pfam_obj, "x_water", x_water)
        setattr(pfam_obj, "x_water_level", x_water_level)
        setattr(pfam_obj, "x_ben_tot", x_ben_tot)
        setattr(pfam_obj, "x_ben_por", x_ben_por)

        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "PFAM Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'pfam','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'pfam', 
                'model_attributes':'PFAM Output'})
        html = html + pfam_tables.table_all(pfam_obj)
        html = html + template.render(templatepath + 'pfam-output.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, pfam_obj.__dict__, 'pfam', 'single')
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', PFAMOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

