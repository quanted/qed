# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import unittest
from StringIO import StringIO
import cStringIO
import logging 
from sip import sip_model
import csv
import numpy

bw_bird=[]
bw_mamm=[]
avian_ld50=[]
mammalian_ld50=[]
sol = []
aw_bird=[]
tw_bird=[]
mineau=[]
aw_mamm=[]
tw_mamm=[]
avian_noaec=[]
avian_noael=[]
mammalian_noaec=[]
mammalian_noael=[]

######Pre-defined outputs########
fw_bird_out = []
fw_mamm_out = []
dose_bird_out = []
dose_mamm_out = []
at_bird_out = []
at_mamm_out = []
fi_bird_out = []
det_out = []
act_out = []
acute_bird_out = []
acuconb_out = []
acute_mamm_out = []
acuconm_out = []
chron_bird_out = []
chronconb_out = []
chron_mamm_out = []
chronconm_out = []

logger = logging.getLogger("SIPBatchOutput")

def html_table(row_inp,iter):
    bw_bird_temp=float(row_inp[0])
    bw_bird.append(bw_bird_temp)
    bw_mamm_temp=float(row_inp[1])
    bw_mamm.append(bw_mamm_temp)
    sol_temp=float(row_inp[2])
    sol.append(sol_temp)
    avian_ld50_temp=float(row_inp[3])
    avian_ld50.append(avian_ld50_temp)
    mammalian_ld50_temp=float(row_inp[4])
    mammalian_ld50.append(mammalian_ld50_temp)
    aw_bird_temp=float(row_inp[5])        
    aw_bird.append(aw_bird_temp)
    tw_bird_temp=float(row_inp[6])   
    tw_bird.append(tw_bird_temp)
    mineau_temp=float(row_inp[7])
    mineau.append(mineau_temp)
    aw_mamm_temp=float(row_inp[8])
    aw_mamm.append(aw_mamm_temp)
    tw_mamm_temp=float(row_inp[9])   
    tw_mamm.append(tw_mamm_temp)
    avian_noaec_temp=float(row_inp[10])   
    avian_noaec.append(avian_noaec_temp)
    avian_noael_temp=float(row_inp[11])   
    avian_noael.append(avian_noael_temp)
    mammalian_noaec_temp=float(row_inp[12])   
    mammalian_noaec.append(mammalian_noaec_temp)
    mammalian_noael_temp=float(row_inp[13])   
    mammalian_noael.append(mammalian_noael_temp)
    

    fw_bird_temp=sip_model.fw_bird(bw_bird_temp)
    fw_bird_out.append(fw_bird_temp)
    fw_mamm_temp=sip_model.fw_mamm(bw_mamm_temp)
    fw_mamm_out.append(fw_mamm_temp)
    dose_bird_temp=sip_model.dose_bird(fw_bird_temp,sol_temp,bw_bird_temp)
    dose_bird_out.append(dose_bird_temp)
    dose_mamm_temp=sip_model.dose_mamm(fw_mamm_temp,sol_temp,bw_mamm_temp)
    dose_mamm_out.append(dose_mamm_temp)
    at_bird_temp=sip_model.at_bird(avian_ld50_temp,aw_bird_temp,tw_bird_temp,mineau_temp)
    at_bird_out.append(at_bird_temp)
    at_mamm_temp=sip_model.at_mamm(mammalian_ld50_temp,aw_mamm_temp,tw_mamm_temp)
    at_mamm_out.append(at_mamm_temp)
    fi_bird_temp=sip_model.fi_bird(bw_bird_temp)
    fi_bird_out.append(fi_bird_temp)
    det_temp=sip_model.det(avian_noaec_temp,fi_bird_temp,bw_bird_temp)
    det_out.append(det_temp)
    act_temp=sip_model.act(mammalian_noael_temp,tw_mamm_temp,aw_mamm_temp)
    act_out.append(act_temp)
    acute_bird_temp=sip_model.acute_bird(dose_bird_temp,at_bird_temp)
    acute_bird_out.append(acute_bird_temp)
    acuconb_temp=sip_model.acuconb(acute_bird_temp)
    acuconb_out.append(acuconb_temp)
    acute_mamm_temp=sip_model.acute_mamm(dose_mamm_temp,at_mamm_temp)
    acute_mamm_out.append(acute_mamm_temp)
    acuconm_temp=sip_model.acuconm(acute_mamm_temp)
    acuconm_out.append(acuconm_temp)
    chron_bird_temp=sip_model.chron_bird(dose_bird_temp,det_temp)
    chron_bird_out.append(chron_bird_temp)
    chronconb_temp=sip_model.chronconb(chron_bird_temp)
    chronconb_out.append(chronconb_temp)
    chron_mamm_temp=sip_model.chron_mamm(dose_mamm_temp,act_temp)
    chron_mamm_out.append(chron_mamm_temp)
    chronconm_temp=sip_model.chronconm(chron_mamm_temp)
    chronconm_out.append(chronconm_temp)


    Input_header="""<table border="1">
                        <tr><H3>Batch Calculation of Iteration %s</H3></tr><br>
                        <tr>
                            <td><b>Input Name</b></td>
                            <td><b>Input value</b></td>
                            <td><b>Unit</b></td>
                        </tr>"""%(iter)
    Input_bw_bird="""<tr>
                    <td>Body weight of bird</td>
                    <td>%s</td>
                    <td>kg</td>
                </tr>""" %(bw_bird_temp) 
    Input_bw_mamm="""<tr>
                    <td>Body weight of mammal</td>
                    <td>%s</td>
                    <td>kg</td>
                </tr>""" %(bw_mamm_temp)                         
    Input_sol="""<tr>
                    <td>Solubility</td>
                    <td>%s</td>
                    <td>m<sup>2</sup></td>
                </tr>""" %(sol_temp)                          
    Input_avian_ld50="""<tr>
                    <td>Avian LD50</td>
                    <td>%s</td>
                    <td>kg/m<sup>3</sup></td>
                </tr>""" %(avian_ld50_temp)  
    Input_mammalian_ld50="""<tr>
                    <td>Mammalian LD50</td>
                    <td>%s</td>
                    <td>m</td>
                </tr>""" %(mammalian_ld50_temp) 
    Input_aw_bird="""<tr>
                    <td>Body weight of the assessed bird</td>
                    <td>%s</td>
                    <td>kg</td>
                </tr>""" %(aw_bird_temp)                        
    Input_tw_bird="""<tr>
                    <td>Body weight of the tested bird</td>
                    <td>%s</td>
                    <td>kg</td>
                </tr>""" %(tw_bird_temp)
    Input_mineau="""<tr>
                    <td>Mineau scaling factor</td>
                    <td>%s</td>
                    <td>kg</td>
                </tr>""" %(mineau_temp) 
    Input_aw_mamm="""<tr>
                    <td>Body weight of the assessed mammal</td>
                    <td>%s</td>
                    <td>kg</td>
                </tr>""" %(aw_mamm_temp)                         
    Input_tw_mamm="""<tr>
                    <td>Body weight of the tested mammal</td>
                    <td>%s</td>
                    <td>kg</td>
                </tr>""" %(tw_mamm_temp)                          
    Input_avian_noaec="""<tr>
                    <td>Avian NOAEC</td>
                    <td>%s</td>
                    <td>kg/m<sup>3</sup></td>
                </tr>""" %(avian_noaec_temp)  
    Input_avian_noael="""<tr>
                    <td>Avian NOAEL</td>
                    <td>%s</td>
                    <td>m</td>
                </tr>""" %(avian_noael_temp) 
    Input_mammalian_noaec="""<tr>
                    <td>Mammalian NOAEC</td>
                    <td>%s</td>
                    <td>kg/m<sup>3</sup></td>
                </tr>""" %(mammalian_noaec_temp)  
    Input_mammalian_noael="""<tr>
                    <td>Mammalian NOAEL</td>
                    <td>%s</td>
                    <td>m</td>
                </tr></table><br>""" %(mammalian_noael_temp) 

    Output_header="""<table border="1">
                        <tr>
                            <td><b>Output Name</b></td>
                            <td><b>Output value</b></td>
                            <td><b>Unit</b></td>
                        </tr>"""
    Output_fw_bird="""<tr>
                    <td>Daily water intake rate for birds</td>
                    <td>%s</td>
                    <td>kg</td>
                </tr>""" %(fw_bird_temp) 
    Output_fw_mamm="""<tr>
                    <td>Daily water intake rate for mammalsh</td>
                    <td>%s</td>
                    <td>m</td>
                </tr>""" %(fw_mamm_temp)                         
    Output_dose_bird="""<tr>
                    <td>Upper bound estimate of exposure for birds</td>
                    <td>%s</td>
                    <td>m<sup>2</sup></td>
                </tr>""" %(dose_bird_temp)                          
    Output_dose_mamm="""<tr>
                    <td>Upper bound estimate of exposure for mammals</td>
                    <td>%s</td>
                    <td>kg/m<sup>3</sup></td>
                </tr>""" %(dose_mamm_temp)  
    Output_at_bird="""<tr>
                    <td>Acute adjusted toxicity value for birds</td>
                    <td>%s</td>
                    <td>m</td>
                </tr>""" %(at_bird_temp) 
    Output_at_mamm="""<tr>
                    <td>Acute adjusted toxicity value for mammals</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(at_mamm_temp)                        
    Output_fi_bird="""<tr>
                    <td>Adjusted chronic toxicity values for birds</td>
                    <td>%s</td>
                    <td>L/kg</td>
                </tr>""" %(fi_bird_temp) 
    Output_det="""<tr>
                    <td>Dose-equivalent chronic toxicity value for birds</td>
                    <td>%s</td>
                    <td>m</td>
                </tr>""" %(det_temp)                         
    Output_act="""<tr>
                    <td>Adjusted chronic toxicty value for mammals</td>
                    <td>%s</td>
                    <td>m<sup>2</sup></td>
                </tr>""" %(act_temp)                          
    Output_acute_bird="""<tr>
                    <td>Acute exposures for birds</td>
                    <td>%s</td>
                    <td>kg/m<sup>3</sup></td>
                </tr>""" %(acute_bird_temp)  
    Output_acuconb="""<tr>
                    <td>acuconb</td>
                    <td>%s</td>
                    <td>m</td>
                </tr>""" %(acuconb_temp) 
    Output_acute_mamm="""<tr>
                    <td>Acute exposures for mammals</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(acute_mamm_temp)                        
    Output_acuconm="""<tr>
                    <td>acuconm</td>
                    <td>%s</td>
                    <td>L/kg</td>
                </tr>""" %(acuconm_temp)
    Output_chron_bird="""<tr>
                    <td>Chronic Exposures for birds</td>
                    <td>%s</td>
                    <td>kg</td>
                </tr>""" %(chron_bird_temp) 
    Output_chronconb="""<tr>
                    <td>chronconb</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(chronconb_temp)                        
    Output_chron_mamm="""<tr>
                    <td>Chronic exposures for mammals</td>
                    <td>%s</td>
                    <td>L/kg</td>
                </tr></table><br>""" %(chron_mamm_temp)

    Inout_table = Input_header+Input_bw_bird+Input_bw_mamm+Input_sol+Input_avian_ld50+Input_mammalian_ld50+Input_aw_bird+Input_tw_bird+Input_mineau+Input_aw_mamm+Input_tw_mamm+Input_avian_noaec+Input_avian_noael+Input_mammalian_noaec+Input_mammalian_noael+Output_header+Output_fw_bird+Output_fw_mamm+Output_dose_bird+Output_dose_mamm+Output_at_bird+Output_at_mamm+Output_fi_bird+Output_det+Output_act+Output_acute_bird+Output_acuconb+Output_acute_mamm+Output_acuconm+Output_chron_bird+Output_chronconb+Output_chron_mamm  
               
    return Inout_table  
                
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    logger.info(header)
    i=1
    iter_html=""
    for row in reader:
        iter_html = iter_html +html_table(row,i)
        i=i+1
    sum_header ="""<table border="1">
                        <tr><H3>Summary Statistics (Iterations=%s)</H3></tr><br>
                        <tr>
                            <td><b>Input Name</b></td>
                            <td><b>Mean</b></td>
                            <td><b>Std.</b></td>
                            <td><b>Min</b></td>
                            <td><b>Max</b></td>                            
                            <td><b>Unit</b></td>
                        </tr>"""%(i-1)
                        
    sum_bw_bird="""<tr>
                    <td>Daily water intake rate for birds</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>ml</td>
                </tr>""" %(numpy.mean(bw_bird), numpy.std(bw_bird), numpy.min(bw_bird), numpy.max(bw_bird)) 
    sum_bw_mamm="""<tr>
                    <td>Body weight of mammal</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>   
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                       
                    <td>m</td>
                </tr>""" %(numpy.mean(bw_mamm), numpy.std(bw_mamm), numpy.min(bw_mamm), numpy.max(bw_mamm))                         
    sum_sol="""<tr>
                    <td>Solubility</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                        
                    <td>m<sup>2</sup></td>
                </tr>""" %(numpy.mean(sol), numpy.std(sol), numpy.min(sol), numpy.max(sol))                          
    sum_avian_ld50="""<tr>
                    <td>Avian LD50</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>kg/m<sup>3</sup></td>
                </tr>""" %(numpy.mean(avian_ld50), numpy.std(avian_ld50), numpy.min(avian_ld50), numpy.max(avian_ld50))  
    sum_mammalian_ld50="""<tr>
                    <td>Mammalian LD50</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                     
                    <td>m</td>
                </tr>""" %(numpy.mean(mammalian_ld50), numpy.std(mammalian_ld50), numpy.min(mammalian_ld50), numpy.max(mammalian_ld50)) 
    sum_aw_bird="""<tr>
                    <td>Body weight of the assessed bird</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>  
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                        
                    <td>kg</td>
                </tr>""" %(numpy.mean(aw_bird), numpy.std(aw_bird), numpy.min(aw_bird), numpy.max(aw_bird))                        
    sum_tw_bird="""<tr>
                    <td>Body weight of the tested bird</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>kg</td>
                </tr>""" %(numpy.mean(tw_bird), numpy.std(tw_bird), numpy.min(tw_bird), numpy.max(tw_bird))  
    sum_aw_mamm="""<tr>
                    <td>Body weight of the assessed mammal</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>ml</td>
                </tr>""" %(numpy.mean(aw_mamm), numpy.std(aw_mamm), numpy.min(aw_mamm), numpy.max(aw_mamm)) 
    sum_tw_mamm="""<tr>
                    <td>Body weight of the tested mammal</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>   
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                       
                    <td>m</td>
                </tr>""" %(numpy.mean(tw_mamm), numpy.std(tw_mamm), numpy.min(tw_mamm), numpy.max(tw_mamm))                         
    sum_avian_noaec="""<tr>
                    <td>Avian NOAEC</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                        
                    <td>m<sup>2</sup></td>
                </tr>""" %(numpy.mean(avian_noaec), numpy.std(avian_noaec), numpy.min(avian_noaec), numpy.max(avian_noaec))                          
    sum_avian_noael="""<tr>
                    <td>Avian NOAEL</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>kg/m<sup>3</sup></td>
                </tr>""" %(numpy.mean(avian_noael), numpy.std(avian_noael), numpy.min(avian_noael), numpy.max(avian_noael))  
    sum_mammalian_noaec="""<tr>
                    <td>Mammalian NOAEC</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                     
                    <td>m</td>
                </tr>""" %(numpy.mean(mammalian_noaec), numpy.std(mammalian_noaec), numpy.min(mammalian_noaec), numpy.max(mammalian_noaec)) 
    sum_mammalian_noael="""<tr>
                    <td>Mammalian NOAEL</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>  
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                        
                    <td>kg</td>
                </tr></table><br>""" %(numpy.mean(mammalian_noael), numpy.std(mammalian_noael), numpy.min(mammalian_noael), numpy.max(mammalian_noael))                          

    sum_output_header="""<table border="1">
                        <tr>
                            <td><b>Output Name</b></td>
                            <td><b>Mean</b></td>
                            <td><b>Std.</b></td>
                            <td><b>Min</b></td>
                            <td><b>Max</b></td>                             
                            <td><b>Unit</b></td>
                        </tr>"""
    sum_output_fw_bird="""<tr>
                    <td>Daily water intake rate for birds</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td id="fw_bird_raw" data-val='%s' style="display: none"></td>                    
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(fw_bird_out), numpy.std(fw_bird_out), numpy.min(fw_bird_out), numpy.max(fw_bird_out),fw_bird_out)
    sum_output_fw_mamm="""<tr>
                    <td>Daily water intake rate for mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(fw_mamm_out), numpy.std(fw_mamm_out), numpy.min(fw_mamm_out), numpy.max(fw_mamm_out))
    sum_output_dose_bird="""<tr>
                    <td>Upper bound estimate of exposure for birds</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(dose_bird_out), numpy.std(dose_bird_out), numpy.min(dose_bird_out), numpy.max(dose_bird_out))
    sum_output_dose_mamm="""<tr>
                    <td>Upper bound estimate of exposure for mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(dose_mamm_out), numpy.std(dose_mamm_out), numpy.min(dose_mamm_out), numpy.max(dose_mamm_out))
    sum_output_at_bird="""<tr>
                    <td>Acute adjusted toxicity value for birds</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(at_bird_out), numpy.std(at_bird_out), numpy.min(at_bird_out), numpy.max(at_bird_out))
    sum_output_at_mamm="""<tr>
                    <td>Acute adjusted toxicity value for mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(at_mamm_out), numpy.std(at_mamm_out), numpy.min(at_mamm_out), numpy.max(at_mamm_out))
    sum_output_fi_bird="""<tr>
                    <td>Adjusted chronic toxicity values for birds</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(fi_bird_out), numpy.std(fi_bird_out), numpy.min(fi_bird_out), numpy.max(fi_bird_out))
    sum_output_det="""<tr>
                    <td>Dose-equivalent chronic toxicity value for birds</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(det_out), numpy.std(det_out), numpy.min(det_out), numpy.max(det_out))
    sum_output_act="""<tr>
                    <td>Adjusted chronic toxicty value for mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(act_out), numpy.std(act_out), numpy.min(act_out), numpy.max(act_out))
    sum_output_acute_bird="""<tr>
                    <td>Acute exposures for birds</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(acute_bird_out), numpy.std(acute_bird_out), numpy.min(acute_bird_out), numpy.max(acute_bird_out))
    sum_output_acute_mamm="""<tr>
                    <td>Acute exposures for mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(acute_mamm_out), numpy.std(acute_mamm_out), numpy.min(acute_mamm_out), numpy.max(acute_mamm_out))
    sum_output_chron_bird="""<tr>
                    <td>Chronic Exposures for birds</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(chron_bird_out), numpy.std(chron_bird_out), numpy.min(chron_bird_out), numpy.max(chron_bird_out))
    sum_output_chron_mamm="""<tr>
                    <td>Chronic exposures for mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>lbs a.i./A</td>
                </tr></table><br>""" %(numpy.mean(chron_mamm_out), numpy.std(chron_mamm_out), numpy.min(chron_mamm_out), numpy.max(chron_mamm_out))


    sum_fig="""<H3>Historgram</H3><br>
               <div id="calculate">
                   <div class="block">
                        <label>How many buckets (Default is based on Sturgis rule):</label>
                        <input type="text" id="buckets" value=%s></div><br>
                        <button type="submit" id="calc">Calculate Historgram</button></div><br>
                <div id="chart1"></div><br>"""%(int(1+3.3*np.log10(len(sum_output_fw_bird)))) #number of bins coming from Sturgis rule         
                                     
    sum_html=sum_header+sum_bw_bird+sum_bw_mamm+sum_sol+sum_avian_ld50+sum_mammalian_ld50+sum_aw_bird+sum_tw_bird+sum_aw_mamm+sum_tw_mamm+sum_avian_noaec+sum_avian_noael+sum_mammalian_noaec+sum_mammalian_noael+sum_output_header+sum_output_fw_bird+sum_output_fw_mamm+sum_output_dose_bird+sum_output_dose_mamm+sum_output_at_bird+sum_output_at_mamm+sum_output_fi_bird+sum_output_det+sum_output_act+sum_output_acute_bird+sum_output_acute_mamm+sum_output_chron_bird+sum_output_chron_mamm+sum_fig

    return sum_html+iter_html



              
class SIPBatchOutputPage(webapp.RequestHandler):
    def post(self):
        text_file1 = open('sip/sip_description.txt','r')
        x = text_file1.read()
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['upfile']
        iter_html=loop_html(thefile)        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'sip','page':'batchinput'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {})
        html = html + iter_html
        html = html + template.render(templatepath + 'sip-batchoutput-jqplot.html', {})                
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', SIPBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

