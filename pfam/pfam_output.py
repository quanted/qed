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
from pfam import input_edit
import base64
import urllib
from google.appengine.api import urlfetch
from datetime import datetime,timedelta

############Provide the key and connect to the picloud####################
api_key='3355'
api_secretkey='212ed160e3f416fdac8a3b71c90f3016722856b9'
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string}
###########################################################################               

def get_jid(wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
           noa,dd_out,mm_out,ma_out,sr_out,weather,wea_l,nof,date_f1,nod_out,fl_out,wl_out,ml_out,to_out,
           zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
           ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10,area_app):

    url='https://api.picloud.com/r/3303/pfam_s1'
    input_list=[wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
           noa,dd_out,mm_out,ma_out,sr_out,weather,wea_l,nof,date_f1,nod_out,fl_out,wl_out,ml_out,to_out,
           zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
           ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10,area_app]
    input_list=json.dumps(input_list)
    
#    wat_hl=json.dumps(wat_hl)
#    wat_t=json.dumps(wat_t)
#    ben_hl=json.dumps(ben_hl)
#    ben_t=json.dumps(ben_t)
#    unf_hl=json.dumps(unf_hl)
#    unf_t=json.dumps(unf_t)
#    aqu_hl=json.dumps(aqu_hl)
#    aqu_t=json.dumps(aqu_t)
#    hyd_hl=json.dumps(hyd_hl)
#    mw=json.dumps(mw)
#    vp=json.dumps(vp)
#    sol=json.dumps(sol)
#    koc=json.dumps(koc)
#    hea_h=json.dumps(hea_h)
#    hea_r_t=json.dumps(hea_r_t)
#    noa=json.dumps(noa)
#    dd_out=json.dumps(dd_out)
#    mm_out=json.dumps(mm_out)
#    ma_out=json.dumps(ma_out)
#    sr_out=json.dumps(sr_out)
#    weather=json.dumps(weather)
#    wea_l=json.dumps(wea_l)
#    nof=json.dumps(nof)
#    date_f1=json.dumps(date_f1)
#    nod_out=json.dumps(nod_out)
#    fl_out=json.dumps(fl_out)
#    wl_out=json.dumps(wl_out)
#    ml_out=json.dumps(ml_out)
#    to_out=json.dumps(to_out)
#    zero_height_ref=json.dumps(zero_height_ref)
#    days_zero_full=json.dumps(days_zero_full)
#    days_zero_removal=json.dumps(days_zero_removal)
#    max_frac_cov=json.dumps(max_frac_cov)
#    mas_tras_cof=json.dumps(mas_tras_cof)
#    leak=json.dumps(leak)
#    ref_d=json.dumps(ref_d)
#    ben_d=json.dumps(ben_d)
#    ben_por=json.dumps(ben_por)
#    dry_bkd=json.dumps(dry_bkd)
#    foc_wat=json.dumps(foc_wat)
#    foc_ben=json.dumps(foc_ben)
#    ss=json.dumps(ss)
#    wat_c_doc=json.dumps(wat_c_doc)
#    chl=json.dumps(chl)
#    dfac=json.dumps(dfac)
#    q10=json.dumps(q10)

      
#    data = urllib.urlencode({"wat_hl":wat_hl,"wat_t":wat_t,"ben_hl":ben_hl,"ben_t":ben_t,"unf_hl":unf_hl,"unf_t":unf_t,
#                             "aqu_hl":aqu_hl,"aqu_t":aqu_t,"hyd_hl":hyd_hl,"mw":mw,"vp":vp,"sol":sol,"koc":koc,"hea_h":hea_h,
#                             "hea_r_t":hea_r_t,"noa":noa,"dd_out":dd_out,"mm_out":mm_out,"ma_out":ma_out,"sr_out":sr_out,
#                             "weather":weather,"wea_l":wea_l,"nof":nof,"date_f1":date_f1,"nod_out":nod_out,"fl_out":fl_out,
#                             "wl_out":wl_out,"ml_out":ml_out,"to_out":to_out,"zero_height_ref":zero_height_ref,
#                             "days_zero_full":days_zero_full,"days_zero_removal":days_zero_removal,"max_frac_cov":max_frac_cov,
#                             "mas_tras_cof":mas_tras_cof,"leak":leak,"ref_d":ref_d,"ben_d":ben_d,"ben_por":ben_por,
#                             "dry_bkd":dry_bkd,"foc_wat":foc_wat,"foc_ben":foc_ben,"ss":ss,"wat_c_doc":wat_c_doc,"chl":chl,
#                             "dfac":dfac,"q10":q10})

    data = urllib.urlencode({"input_list":input_list})

    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers) 
    jid= json.loads(response.content)['jid']
    output_st = ''
        
    while output_st!="done":
        response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid, headers=http_headers)
        output_st = json.loads(response_st.content)['info']['%s' %jid]['status']

    url_val = 'https://api.picloud.com/job/result/?jid='+str(jid)
    response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
    output_val = json.loads(response_val.content)['result']
    return(jid, output_st, output_val)

#def get_jid(a,b):
#    url='https://api.picloud.com/r/3303/pfam_s1'
#    input_list=[a,b]
#    input_list=json.dumps(input_list)
#
#    data = urllib.urlencode({"input_list":input_list})
#    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers) 
#    jid= json.loads(response.content)['jid']
#    output_st = '' 
#    
#    while output_st!="done":
#        response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid, headers=http_headers)
#        output_st = json.loads(response_st.content)['info']['%s' %jid]['status']
#
#    url_val = 'https://api.picloud.com/job/result/?jid='+str(jid)
#    response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
#    output_val = json.loads(response_val.content)['result']       
#    return(jid, output_st, output_val)

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
        
        final_res=get_jid(wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
                            noa,dd_out.tolist(),mm_out.tolist(),ma_out.tolist(),sr_out.tolist(),weather, wea_l,
                            nof,date_f1,nod_out.tolist(),fl_out.tolist(),wl_out.tolist(),ml_out.tolist(),to_out.tolist(),
                            zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
                            ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10,area_app)
           
#        print final_res
        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'pfam','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'pfam', 
                'model_attributes':'PFAM Output'})
        html = html + """
        <table class="out_chemical" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="5"><div align="center">Chemical Inputs</div></th>
                          </tr>        
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>           
                          <tr>
                            <td><div align="center">Water Column Half life @%s &#8451</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Benthic Compartment Half Life @%s &#8451</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>      
                          <tr>
                            <td><div align="center">Unflooded Soil Half Life @%s &#8451</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                                                
                          <tr>
                            <td><div align="center">Aqueous Near-Surface Photolysis Half Life @%s Degrees Latitude</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Hydrolysis Half Life</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Molecular Weight</div></td>
                            <td><div align="center">g/mol</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Vapor Pressure</div></td>
                            <td><div align="center">torr</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>  
                          <tr>
                            <td><div align="center">Solubility</div></td>
                            <td><div align="center">mg/l</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>      
                          <tr>
                            <td><div align="center">Koc</td>
                            <td><div align="center">ml/g</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>  
                          <tr>
                            <td><div align="center">Heat of Henry</td>
                            <td><div align="center">J/mol</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Henry Reference Temperature</td>
                            <td><div align="center">&#8451</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                                                                                                                                                                                                                       
        </table><br>"""%(wat_t,wat_hl,ben_t,ben_hl,unf_t,unf_hl,aqu_t,aqu_hl,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t)
        
        html = html + """
        <table width="550" border="1">
                          <tr>
                            <th scope="col" colspan="5"><div align="center">Application Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Number of Applications</td>
                            <td><div align="center"></div></td>
                            <td id="noa_out"><div align="center">%s</div></td>
                          </tr></table>
        <table class="out_application" width="550" border="1">
                          <tr>
                            <th scope="col" width="50"><div align="center">App#</div></th>
                            <th scope="col" width="125"><div align="center">Month</div></th>                            
                            <th scope="col" width="125"><div align="center">Day</div></th>
                            <th scope="col" width="125"><div align="center">Mass Applied (kg/hA)</div></th>
                            <th scope="col" width="125"><div align="center">Slow Release (1/day)</div></th>
                          </tr>
                          <tr>          
                            <td id="mm_out" data-val='%s' style="display: none"></td>  
                            <td id="dd_out" data-val='%s' style="display: none"></td>  
                            <td id="ma_out" data-val='%s' style="display: none"></td>  
                            <td id="sr_out" data-val='%s' style="display: none"></td>  
                          </tr>                               
       </table><br>"""%(noa,mm_out.tolist(),dd_out.tolist(),ma_out.tolist(),sr_out.tolist())
        
        html = html + """
        <table class="out_location" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">Location Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Weather File</td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Latitude (for Photolysis Calculations)</td>
                            <td><div align="center">degree</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                           
        </table><br>"""%(weather, wea_l)    

        html = html + """
        <table width="550" border="1">
                          <tr>
                            <th scope="col" colspan="5"><div align="center">Floods Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Number of Events</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Number of Events</td>
                            <td><div align="center"></div></td>
                            <td id="nof_out"><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Date for Event 1</td>
                            <td><div align="center"></div></td>
                            <td id="noa_out"><div align="center">%s</div></td>
                          </tr></table>
        <table class="out_floods" width="550" border="1">
                          <tr>
                            <th scope="col" width="50"><div align="center">Event#</div></th>
                            <th scope="col" width="100"><div align="center">Number of days</div></th>                            
                            <th scope="col" width="100"><div align="center">Fill Level (m)</div></th>
                            <th scope="col" width="100"><div align="center">Wier Level (m)</div></th>
                            <th scope="col" width="100"><div align="center">Min. Level (m)</div></th>
                            <th scope="col" width="100"><div align="center">Turn Over (1/day)</div></th>                            
                          </tr>
                          <tr>          
                            <td id="nod_out" data-val='%s' style="display: none"></td>  
                            <td id="fl_out" data-val='%s' style="display: none"></td>  
                            <td id="wl_out" data-val='%s' style="display: none"></td>  
                            <td id="ml_out" data-val='%s' style="display: none"></td>
                            <td id="to_out" data-val='%s' style="display: none"></td>  
                          </tr>                               
       </table><br>"""%(nof, date_f1, nod_out.tolist(), fl_out.tolist(), wl_out.tolist(), ml_out.tolist(), to_out.tolist())

        html = html + """
        <table class="out_location" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">Crop Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Zero Height Reference</td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Days from Zero Height to Full Height</td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Days from Zero Height to Removal</td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Maximum Fractional Area Coverage</td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                                                                                    
        </table><br>"""%(zero_height_ref, days_zero_full, days_zero_removal, max_frac_cov)       
        
        html = html + """
        <table class="out_physical" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">Physical Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Mass Transfer Coefficient</td>
                            <td><div align="center">m</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Leakage </td>
                            <td><div align="center">m/d</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Reference Depth</td>
                            <td><div align="center">m</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Benthic Depth</td>
                            <td><div align="center">m</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Benthic Porosity</td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>   
                          <tr>
                            <td><div align="center">Dry Bulk Density</td>
                            <td><div align="center">g/cm<sup>3</sup></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Foc Water Column on SS</td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>  
                          <tr>
                            <td><div align="center">Foc Benthic</td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">SS</td>
                            <td><div align="center">mg/L</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Water column DOC</td>
                            <td><div align="center">mg/L</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Chlorophyll, CHL</td>
                            <td><div align="center">mg/L</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Dfac</td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Q10</td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                                                                                                                                                                                                                                                                                                                        
        </table><br>"""%(mas_tras_cof, leak, ref_d, ben_d, ben_por, dry_bkd, foc_wat, foc_ben, ss, wat_c_doc, chl, dfac, q10)   

        html = html + """
        <table class="out_output" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">Output Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>
                          <tr>             
                            <th scope="col" width="250"><div align="center">Area of Application</div></th>
                            <th scope="col" width="150"><div align="center">m<sup>2</sup></div></th>                            
                            <th scope="col" width="150"><div align="center">%s</div></th>
                          </tr>
        </table><br>"""%(area_app)   
        
        html = html + """
        <table class="results" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">PFAM Results</div></th>
                          </tr>
                          <tr>
                            <th scope="col">Outputs</div></th>
                            <th scope="col">Value</div></th>                            
                          </tr>
                          <tr>
                            <td>Simulation is finished. Please download your file from here</td>
                            <td><a href=%s>Link</a></td>
                          </tr>         
        </table><br>"""%(final_res[2])                              


        html = html + template.render(templatepath + 'pfam-output.html', {})                                 
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', PFAMOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    