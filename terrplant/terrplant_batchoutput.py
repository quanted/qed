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
import sys
sys.path.append("../terrplant")
from terrplant import terrplant_model
import csv
import numpy

A=[]
I=[]
R=[]
D=[]
nms=[]
lms=[]
nds=[]
lds=[]

######Pre-defined outputs########
rundry_out = []
runsemi_out = []
spray_out = []
totaldry_out = []
totalsemi_out = []
nmsRQdry_out = []
LOCnmsdry_out = []
nmsRQsemi_out = []
LOCnmssemi_out = []
nmsRQspray_out = []
LOCnmsspray_out = []
lmsRQdry_out = []
LOClmsdry_out = []
lmsRQsemi_out = []
LOClmssemi_out = []
lmsRQspray_out = []
LOClmsspray_out = []
ndsRQdry_out = []
LOCndsdry_out = []
ndsRQsemi_out = []
LOCndssemi_out = []
ndsRQspray_out = []
LOCndsspray_out = []
ldsRQdry_out = []
LOCldsdry_out = []
ldsRQsemi_out = []
LOCldssemi_out = []
ldsRQspray_out = []
LOCldsspray_out = []

logger = logging.getLogger("TerrPlantBatchOutput")

def html_table(row_inp,iter):
    A_temp=float(row_inp[0])
    A.append(A_temp)
    I_temp=float(row_inp[1])
    I.append(I_temp)
    R_temp=float(row_inp[2])
    R.append(R_temp)
    D_temp=float(row_inp[3])
    D.append(D_temp)
    nms_temp=float(row_inp[4])
    nms.append(nms_temp)
    lms_temp=float(row_inp[5])        
    lms.append(lms_temp)
    nds_temp=float(row_inp[6])   
    nds.append(nds_temp)
    lds_temp=float(row_inp[7])
    lds.append(lds_temp)
    terr = terrplant_model.terrplant(True,True,A_temp,I_temp,R_temp,D_temp,nms_temp,lms_temp,nds_temp,lds_temp)
    rundry_temp=terr.rundry_results
    rundry_out.append(rundry_temp)
    runsemi_temp=terr.runsemi_results
    runsemi_out.append(runsemi_temp)
    spray_temp=terr.spray_results
    spray_out.append(spray_temp)
    totaldry_temp=terr.totaldry_results
    totaldry_out.append(totaldry_temp)
    totalsemi_temp=terr.totalsemi_results
    totalsemi_out.append(totalsemi_temp)
    nmsRQdry_temp=terr.nmsRQdry_results
    nmsRQdry_out.append(nmsRQdry_temp)
    LOCnmsdry_temp=terr.LOCnmsdry_results
    LOCnmsdry_out.append(LOCnmsdry_temp)
    nmsRQsemi_temp=terr.nmsRQsemi_results
    nmsRQsemi_out.append(nmsRQsemi_temp)
    LOCnmssemi_temp=terr.LOCnmssemi_results
    LOCnmssemi_out.append(LOCnmssemi_temp)
    nmsRQspray_temp=terr.nmsRQspray_results
    nmsRQspray_out.append(nmsRQspray_temp)
    LOCnmsspray_temp=terr.LOCnmsspray_results
    LOCnmsspray_out.append(LOCnmsspray_temp)
    lmsRQdry_temp=terr.lmsRQdry_results
    lmsRQdry_out.append(lmsRQdry_temp)
    LOClmsdry_temp=terr.LOClmsdry_results
    LOClmsdry_out.append(LOClmsdry_temp)
    lmsRQsemi_temp=terr.lmsRQsemi_results
    lmsRQsemi_out.append(lmsRQsemi_temp)
    LOClmssemi_temp=terr.LOClmssemi_results
    LOClmssemi_out.append(LOClmssemi_temp)
    lmsRQspray_temp=terr.lmsRQspray_results
    lmsRQspray_out.append(lmsRQspray_temp)
    LOClmsspray_temp=terr.LOClmsspray_results
    LOClmsspray_out.append(LOClmsspray_temp)
    ndsRQdry_temp=terr.ndsRQdry_results
    ndsRQdry_out.append(ndsRQdry_temp)
    LOCndsdry_temp=terr.LOCndsdry_results
    LOCndsdry_out.append(LOCndsdry_temp)
    ndsRQsemi_temp=terr.ndsRQsemi_results
    ndsRQsemi_out.append(ndsRQsemi_temp)
    LOCndssemi_temp=terr.LOCndssemi_results
    LOCndssemi_out.append(LOCndssemi_temp)
    ndsRQspray_temp=terr.ndsRQspray_results
    ndsRQspray_out.append(ndsRQspray_temp)
    LOCndsspray_temp=terr.LOCndsspray_results
    LOCndsspray_out.append(LOCndsspray_temp)
    ldsRQdry_temp=terr.ldsRQdry_results
    ldsRQdry_out.append(ldsRQdry_temp)
    LOCldsdry_temp=terr.LOCldsdry_results
    LOCldsdry_out.append(LOCldsdry_temp)
    ldsRQsemi_temp=terr.ldsRQsemi_results
    ldsRQsemi_out.append(ldsRQsemi_temp)
    LOCldssemi_temp=terr.LOCldssemi_results
    LOCldssemi_out.append(LOCldssemi_temp)
    ldsRQspray_temp=terr.ldsRQspray_results
    ldsRQspray_out.append(ldsRQspray_temp)
    LOCldsspray_temp=terr.LOCldsspray_results
    LOCldsspray_out.append(LOCldsspray_temp)


    Input_header="""<table border="1">
                        <tr><H3>Batch Calculation of Iteration %s</H3></tr><br>
                        <tr>
                            <td><b>Input Name</b></td>
                            <td><b>Input value</b></td>
                            <td><b>Unit</b></td>
                        </tr>"""%(iter)
    Input_A="""<tr>
                    <td>Application Rate</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(A_temp) 
    Input_I="""<tr>
                    <td>Incorporation</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(I_temp)                         
    Input_R="""<tr>
                    <td>Runoff Fraction</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(R_temp)                          
    Input_D="""<tr>
                    <td>Drift Fraction</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(D_temp)  
    Input_nms="""<tr>
                    <td>EC25 for monocot seedlings</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(nms_temp) 
    Input_lms="""<tr>
                    <td>NOAEC for monocot seedlings</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(lms_temp)                        
    Input_nds="""<tr>
                    <td>EC25 for dicot seedlings</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(nds_temp)
    Input_lds="""<tr>
                    <td>NOAEC for dicot seedlings</td>
                    <td>%s</td>
                    <td>-</td>
                </tr></table><br>""" %(lds_temp) 


    Output_header="""<table border="1">
                        <tr>
                            <td><b>Output Name</b></td>
                            <td><b>Output value</b></td>
                            <td><b>Unit</b></td>
                        </tr>"""
    Output_rundry="""<tr>
                    <td>EEC for runoff to dry areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(rundry_temp)
    Output_runsemi="""<tr>
                    <td>EEC for runoff to semi-aquatic areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(runsemi_temp)                         
    Output_spray="""<tr>
                    <td>EEC for spray drift</td>
                    <td>%s</td>
                    <td>-/td>
                </tr>""" %(spray_temp)                         
    Output_totaldry="""<tr>
                    <td>EEC total for dry areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(totaldry_temp)  
    Output_totalsemi="""<tr>
                    <td>EEC total for semi-aquatic areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(totalsemi_temp) 
    Output_nmsRQdry="""<tr>
                    <td>Risk Quotient for non-listed monocot seedlings exposed to Pesticide X in a dry area</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(nmsRQdry_temp)                     
    Output_LOCnmsdry="""<tr>
                    <td>Level of concern for non-listed monocot seedlings exposed to pesticide X in a dry area</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(LOCnmsdry_temp) 
    Output_nmsRQsemi="""<tr>
                    <td>Risk Quotient for non-listed monocot seedlings exposed to Pesticide X in a semi-aquatic area</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(nmsRQsemi_temp)                         
    Output_LOCnmssemi="""<tr>
                    <td>Level of concern for non-listed monocot seedlings exposed to pesticide X in a semi-aquatic area</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(LOCnmssemi_temp)                        
    Output_nmsRQspray="""<tr>
                    <td>Risk Quotient for non-listed monocot seedlings exposed to Pesticide X via SPRAY drift</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(nmsRQspray_temp)  
    Output_LOCnmsspray="""<tr>
                    <td>Level of concern for non-listed monocot seedlings exposed to pesticide via spray drift</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(LOCnmsspray_temp) 
    Output_lmsRQdry="""<tr>
                    <td>Risk Quotient for listed monocot seedlings exposed to Pesticide X in a dry areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(lmsRQdry_temp)                      
    Output_LOClmsdry="""<tr>
                    <td>Level of concern for listed monocot seedlings exposed to pesticide via runoff in a dry area</td>
                    <td>%s</td>
                    <td>L/kg</td>
                </tr>""" %(LOClmsdry_temp)
    Output_lmsRQsemi="""<tr>
                    <td>Risk Quotient for listed monocot seedlings exposed to Pesticide X in a semi-aquatic area</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(lmsRQsemi_temp) 
    Output_LOClmssemi="""<tr>
                    <td>Level of concern for listed monocot seedlings exposed to pesticide X in semi-aquatic areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(LOClmssemi_temp)
    Output_lmsRQspray="""<tr>
                    <td>Risk Quotient for listed monocot seedlings exposed to Pesticide X via spray drift</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(lmsRQspray_temp) 
    Output_LOClmsspray="""<tr>
                    <td>Level of concern for listed monocot seedlings exposed to pesticide X via spray drift</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(LOClmsspray_temp) 
    Output_ndsRQdry="""<tr>
                    <td>Risk Quotient for non-listed dicot seedlings exposed to Pesticide X in dry areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(ndsRQdry_temp) 
    Output_LOCndsdry="""<tr>
                    <td>Level of concern for non-listed dicot seedlings exposed to pesticide X in dry areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(LOCndsdry_temp) 
    Output_ndsRQsemi="""<tr>
                    <td>Risk Quotient for non-listed dicot seedlings exposed to Pesticide X in semi-aquatic areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(ndsRQsemi_temp) 
    Output_LOCndssemi="""<tr>
                    <td>Level of concern for non-listed dicot seedlings exposed to pesticide X in semi-aquatic areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(LOCndssemi_temp) 
    Output_ndsRQspray="""<tr>
                    <td>Risk Quotient for non-listed dicot seedlings exposed to Pesticide X via spray drift</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(ndsRQspray_temp) 
    Output_LOCndsspray="""<tr>
                    <td>Level of concern for non-listed dicot seedlings exposed to pesticide X via spray drift</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(LOCndsspray_temp) 
    Output_ldsRQdry="""<tr>
                    <td>Risk Quotient for listed dicot seedlings exposed to Pesticide X in dry areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(ldsRQdry_temp) 
    Output_LOCldsdry="""<tr>
                    <td>Level of concern for listed dicot seedlings exposed to pesticideX in dry areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(LOCldsdry_temp) 
    Output_ldsRQsemi="""<tr>
                    <td>Risk Quotient for listed dicot seedlings exposed to Pesticide X in semi-aquatic areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(ldsRQsemi_temp) 
    Output_LOCldssemi="""<tr>
                    <td>Level of concern for listed dicot seedlings exposed to pesticide X in dry areas</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(LOCldssemi_temp)  
    Output_ldsRQspray="""<tr>
                    <td>Risk Quotient for listed dicot seedlings exposed to Pesticide X via spray drift</td>
                    <td>%s</td>
                    <td>-</td>
                </tr>""" %(ldsRQspray_temp)                        
    Output_LOCldsspray="""<tr>
                    <td>Level of concern for listed dicot seedlings exposed to pesticide X via spray drift</td>
                    <td>%s</td>
                    <td>-</td>
                </tr></table><br>""" %(LOCldsspray_temp)

    Inout_table = Input_header+Input_A+Input_I+Input_R+Input_D+Input_nms+Input_lms+Input_nds+Input_lds
    Inout_table += Output_header+Output_rundry+Output_runsemi+Output_spray+Output_totaldry+Output_totalsemi
    Inout_table += Output_nmsRQdry+Output_LOCnmsdry+Output_nmsRQsemi+Output_LOCnmssemi+Output_nmsRQspray+Output_LOCnmsspray
    Inout_table += Output_lmsRQdry+Output_LOClmsdry+Output_lmsRQsemi+Output_LOClmssemi+Output_lmsRQspray+Output_LOClmsspray
    Inout_table += Output_ndsRQdry+Output_LOCndsdry+Output_ndsRQsemi+Output_LOCndssemi+Output_ndsRQspray+Output_LOCndsspray
    Inout_table += Output_ldsRQdry+Output_LOCldsdry+Output_ldsRQsemi+Output_LOCldssemi+Output_ldsRQspray+Output_LOCldsspray
               
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
    sum_A="""<tr>
                    <td>Application Rate</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>-</td>
                </tr>""" %(numpy.mean(A), numpy.std(A), numpy.min(A), numpy.max(A))
    sum_I="""<tr>
                    <td>Incorporation</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>-</td>
                </tr>""" %(numpy.mean(I), numpy.std(I), numpy.min(I), numpy.max(I)) 
    sum_R="""<tr>
                    <td>Runoff Fraction</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>-</td>
                </tr>""" %(numpy.mean(R), numpy.std(R), numpy.min(R), numpy.max(R)) 
    sum_D="""<tr>
                    <td>Drift Fraction</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>-</td>
                </tr>""" %(numpy.mean(D), numpy.std(D), numpy.min(D), numpy.max(D)) 
    sum_nms="""<tr>
                    <td>EC25 for monocot seedlings</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>-</td>
                </tr>""" %(numpy.mean(nms), numpy.std(nms), numpy.min(nms), numpy.max(nms)) 
    sum_lms="""<tr>
                    <td>NOAEC for monocot seedlings</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>-</td>
                </tr>""" %(numpy.mean(lms), numpy.std(lms), numpy.min(lms), numpy.max(lms)) 
    sum_nds="""<tr>
                    <td>EC25 for dicot seedlings</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>-</td>
                </tr>""" %(numpy.mean(nds), numpy.std(nds), numpy.min(nds), numpy.max(nds)) 
    sum_lds="""<tr>
                    <td>NOAEC for dicot seedlings</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>-</td>
                </tr>""" %(numpy.mean(lds), numpy.std(lds), numpy.min(lds), numpy.max(lds)) 
                        
 
    sum_output_header="""<table border="1">
                        <tr>
                            <td><b>Output Name</b></td>
                            <td><b>Mean</b></td>
                            <td><b>Std.</b></td>
                            <td><b>Min</b></td>
                            <td><b>Max</b></td>                             
                            <td><b>Unit</b></td>
                        </tr>"""
    sum_output_rundry="""<tr>
                    <td>EEC for runoff to dry areas</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td id="rundry" data-val='%s' style="display: none"></td>                   
                    <td>-</td>
                </tr>""" %(numpy.mean(rundry_out), numpy.std(rundry_out), numpy.min(rundry_out), numpy.max(rundry_out),rundry_out) 
    sum_output_runsemi="""<tr>
                    <td>EEC for runoff to semi-aquatic areas</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>   
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                       
                    <td>-</td>
                </tr>""" %(numpy.mean(runsemi_out), numpy.std(runsemi_out), numpy.min(runsemi_out), numpy.max(runsemi_out))                         
    sum_output_spray="""<tr>
                    <td>EEC for spray drift</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                        
                    <td>-</td>
                </tr>""" %(numpy.mean(spray_out), numpy.std(spray_out), numpy.min(spray_out), numpy.max(spray_out))                          
    sum_output_totaldry="""<tr>
                    <td>EEC total for dry areas</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>-</td>
                </tr>""" %(numpy.mean(totaldry_out), numpy.std(totaldry_out), numpy.min(totaldry_out), numpy.max(totaldry_out))  
    sum_output_totalsemi="""<tr>
                    <td>EEC total for semi-aquatic areas</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                     
                    <td>-</td>
                </tr>""" %(numpy.mean(totalsemi_out), numpy.std(totalsemi_out), numpy.min(totalsemi_out), numpy.max(totalsemi_out)) 
    sum_output_nmsRQdry="""<tr>
                    <td>Risk Quotient for non-listed monocot seedlings exposed to pesticide X in a dry area</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>  
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                        
                    <td>-</td>
                </tr>""" %(numpy.mean(nmsRQdry_out), numpy.std(nmsRQdry_out), numpy.min(nmsRQdry_out), numpy.max(nmsRQdry_out))                        
    sum_output_nmsRQsemi="""<tr>
                    <td>Risk Quotient for non-listed monocot seedlings exposed to Pesticide X in a semi-aquatic area</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>-</td>
                </tr>""" %(numpy.mean(nmsRQsemi_out), numpy.std(nmsRQsemi_out), numpy.min(nmsRQsemi_out), numpy.max(nmsRQsemi_out))  
    sum_output_nmsRQspray="""<tr>
                    <td>Risk Quotient for non-listed monocot seedlings exposed to Pesticide X via spray drift</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>-</td>
                </tr>""" %(numpy.mean(nmsRQspray_out), numpy.std(nmsRQspray_out), numpy.min(nmsRQspray_out), numpy.max(nmsRQspray_out)) 
    sum_output_lmsRQdry="""<tr>
                    <td>Risk Quotient for listed monocot seedlings exposed to Pesticide X in a dry areas</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>   
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                       
                    <td>-</td>
                </tr>""" %(numpy.mean(lmsRQdry_out), numpy.std(lmsRQdry_out), numpy.min(lmsRQdry_out), numpy.max(lmsRQdry_out))                         
    sum_output_lmsRQsemi="""<tr>
                    <td>Risk Quotient for listed monocot seedlings exposed to Pesticide X in a semi-aquatic area</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                        
                    <td>-</td>
                </tr>""" %(numpy.mean(lmsRQsemi_out), numpy.std(lmsRQsemi_out), numpy.min(lmsRQsemi_out), numpy.max(lmsRQsemi_out))                          
    sum_output_lmsRQspray="""<tr>
                    <td>Risk Quotient for listed monocot seedlings exposed to Pesticide X via spray drift</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>-</td>
                </tr>""" %(numpy.mean(lmsRQspray_out), numpy.std(lmsRQspray_out), numpy.min(lmsRQspray_out), numpy.max(lmsRQspray_out))  
    sum_output_ndsRQdry="""<tr>
                    <td>Risk Quotient for non-listed dicot seedlings exposed to Pesticide X in dry areas</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                     
                    <td>-</td>
                </tr>""" %(numpy.mean(ndsRQdry_out), numpy.std(ndsRQdry_out), numpy.min(ndsRQdry_out), numpy.max(ndsRQdry_out)) 
    sum_output_ndsRQsemi="""<tr>
                    <td>Risk Quotient for non-listed dicot seedlings exposed to Pesticide X in semi-aquatic areas</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                     
                    <td>-</td>
                </tr>""" %(numpy.mean(ndsRQsemi_out), numpy.std(ndsRQsemi_out), numpy.min(ndsRQsemi_out), numpy.max(ndsRQsemi_out)) 
    sum_output_ndsRQspray="""<tr>
                    <td>Risk Quotient for non-listed dicot seedlings exposed to Pesticide X in dry areas</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                     
                    <td>-</td>
                </tr>""" %(numpy.mean(ndsRQspray_out), numpy.std(ndsRQspray_out), numpy.min(ndsRQspray_out), numpy.max(ndsRQspray_out)) 
    sum_output_ldsRQdry="""<tr>
                    <td>Risk Quotient for listed dicot seedlings exposed to Pesticide X in DdryRY areas</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                     
                    <td>-</td>
                </tr>""" %(numpy.mean(ldsRQdry_out), numpy.std(ldsRQdry_out), numpy.min(ldsRQdry_out), numpy.max(ldsRQdry_out)) 
    sum_output_ldsRQsemi="""<tr>
                    <td>Risk Quotient for listed dicot seedlings exposed to Pesticide X in semi-aquatic areas</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                     
                    <td>-</td>
                </tr>""" %(numpy.mean(ldsRQsemi_out), numpy.std(ldsRQsemi_out), numpy.min(ldsRQsemi_out), numpy.max(ldsRQsemi_out))
    sum_output_ldsRQspray="""<tr>
                    <td>Risk Quotient for listed dicot seedlings exposed to Pesticide X via spray drift</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                     
                    <td>-</td>
                </tr></table><br>""" %(numpy.mean(ldsRQspray_out), numpy.std(ldsRQspray_out), numpy.min(ldsRQspray_out), numpy.max(ldsRQspray_out))

    sum_fig="""<H3>Historgram</H3><br>
               <div id="calculate">
                   <div class="block">
                        <label>How many buckets (Default is based on Sturgis rule):</label>
                        <input type="text" id="buckets" value=%s></div><br>
                        <button type="submit" id="calc">Calculate Historgram</button></div><br>
                <div id="chart1"></div><br>"""%(int(1+3.3*np.log10(len(sum_output_rundry)))) #number of bins coming from Sturgis rule         
                                     
    sum_html=sum_header+sum_A+sum_I+sum_R+sum_D+sum_nms+sum_lms+sum_nds+sum_lds
    sum_html+=sum_output_header+sum_output_rundry+sum_output_runsemi+sum_output_spray+sum_output_totaldry+sum_output_totalsemi+sum_output_nmsRQdry
    sum_html+=sum_output_nmsRQsemi+sum_output_nmsRQspray+sum_output_lmsRQdry+sum_output_lmsRQsemi+sum_output_lmsRQspray+sum_output_ndsRQdry
    sum_html+=sum_output_ndsRQsemi+sum_output_ndsRQspray+sum_output_ldsRQdry+sum_output_ldsRQsemi+sum_output_ldsRQspray
    sum_html+=sum_fig

    return sum_html+iter_html



              
class TerrPlantBatchOutputPage(webapp.RequestHandler):
    def post(self):
        text_file1 = open('terrplant/terrplant_description.txt','r')
        x = text_file1.read()
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['upfile']
        iter_html=loop_html(thefile)        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'terrplant','page':'batchinput'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {})
        html = html + iter_html
        html = html + template.render(templatepath + 'terrplant-batchoutput-jqplot.html', {})                
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TerrPlantBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

