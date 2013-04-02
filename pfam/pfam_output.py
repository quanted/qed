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

import sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
import keys_Picloud_S3

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
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
        
        x_date1=json.dumps(final_res[2][1]) 
        x_re_v_f = [float(i) for i in final_res[2][2]]
        x_re_c_f = [float(i) for i in final_res[2][3]]
        
        x_date2=json.dumps(final_res[2][4]) 
        x_water = [float(i) for i in final_res[2][5]]
        x_water_level = [float(i) for i in final_res[2][6]]
        x_ben_tot = [float(i) for i in final_res[2][7]]
        x_ben_por = [float(i)*1000000 for i in final_res[2][8]]
        
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
                            <td><div align="center">Koc</div></td>
                            <td><div align="center">ml/g</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>  
                          <tr>
                            <td><div align="center">Heat of Henry</div></td>
                            <td><div align="center">J/mol</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Henry Reference Temperature</div></td>
                            <td><div align="center">&#8451</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                                                                                                                                                                                                                       
        </table><br>"""%(wat_t,wat_hl,ben_t,ben_hl,unf_t,unf_hl,aqu_t,aqu_hl,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t)
        
        html = html + """
        <table class="out_application_pre" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="5"><div align="center">Application Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Number of Applications</div></td>
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
                            <td><div align="center">Weather File</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Latitude (for Photolysis Calculations)</div></td>
                            <td><div align="center">degree</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                           
        </table><br>"""%(weather, wea_l)    

        html = html + """
        <table class="out_floods_pre" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="5"><div align="center">Floods Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Number of Events</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Number of Events</div></td>
                            <td><div align="center"></div></td>
                            <td id="nof_out"><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Date for Event 1</div></td>
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
                            <td><div align="center">Zero Height Reference</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Days from Zero Height to Full Height</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Days from Zero Height to Removal</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Maximum Fractional Area Coverage</div></td>
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
                            <td><div align="center">Mass Transfer Coefficient</div></td>
                            <td><div align="center">m</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Leakage</div></td>
                            <td><div align="center">m/d</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Reference Depth</div></td>
                            <td><div align="center">m</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Benthic Depth</div></td>
                            <td><div align="center">m</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Benthic Porosity</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>   
                          <tr>
                            <td><div align="center">Dry Bulk Density</div></td>
                            <td><div align="center">g/cm<sup>3</sup></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Foc Water Column on SS</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>  
                          <tr>
                            <td><div align="center">Foc Benthic</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">SS</div></td>
                            <td><div align="center">mg/L</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Water column DOC</div></td>
                            <td><div align="center">mg/L</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Chlorophyll, CHL</div></td>
                            <td><div align="center">mg/L</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Dfac</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Q10</div></td>
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
                            <th scope="col"><div align="center">Outputs</div></th>
                            <th scope="col"><div align="center">Value</div></th>                            
                          </tr>
                          <tr>
                            <td><div align="center">Simulation is finished. Please download your file from here</div></td>
                            <td><div align="center"><a href=%s>Link</a></div></td>
                          </tr>
                          <tr style="display: none">
                            <td id="x_date1" data-val='%s'></td>
                            <td id="x_re_v_f" data-val='%s'></td>
                            <td id="x_re_c_f" data-val='%s'></td>
                            <td id="x_date2" data-val='%s'></td>
                            <td id="x_water" data-val='%s'></td>
                            <td id="x_water_level" data-val='%s'></td>
                            <td id="x_ben_tot" data-val='%s'></td>
                            <td id="x_ben_por" data-val='%s'></td>
                          </tr>
        </table><br>"""%(final_res[2][0], x_date1, x_re_v_f, x_re_c_f, x_date2, x_water, x_water_level, x_ben_tot, x_ben_por)  

        html = html +"""
        <table class="display" width="550" border="0">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">Please select the display range</div></th>
                          </tr>
        </table><br>"""

        html = html +"""
        <div id="date_range_slider_1"></div>
        <div>
            <div style="float:left">Display interval:</div>
            <div style="float:left"><select id="display_interval_1">
                                        <option value="1 month">1 month</option>
                                        <option value="3 month" selected>3 month</option>
                                        <option value="6 month">6 month</option>
                                        <option value="1 year">1 year</option>
                                    </select>
            </div>
        </div>
        <div><button type="button" id="calc1">Generate</button></div>
        <div id="chart1" style="margin-top:20px; margin-left:20px; width:650px; height:400px;"></div>
        <div id="chart2" style="margin-top:20px; margin-left:20px; width:650px; height:400px;"></div>
        <div id="chart3" style="margin-top:20px; margin-left:20px; width:650px; height:400px;"></div>        
        """

        html = html + template.render(templatepath + 'pfam-output.html', {})                                 
        html = html + template.render(templatepath + '04uberoutput_end.html', {})

        html = html + """
          <form method="post" target="_blank" action=pdf.html>
            <table align="center" class="getpdf">
            </table>
          </form>
        """

        html = html + template.render(templatepath + 'getpdf_jquery.html', {})

        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', PFAMOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    