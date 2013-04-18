# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy
import cgi
import cgitb
cgitb.enable()
import unittest
from StringIO import StringIO
import cStringIO
import logging 
from rice import rice_output
import csv
from therps import therps_model

chem_name=[]
use=[]
formu_name=[]
a_i=[]
a_r=[]
n_a=[]
a_t=[]
i_a=[]
h_l=[]
ld50_bird=[]
lc50_bird=[]
NOAEC_bird=[]
NOAEL_bird=[]
Species_of_the_tested_bird=[]
tw_bird=[]
x=[]
bw_range_a=[]
bw_herp_a=[]
wp_herp_a=[] #Water content of the assessed amphibian's diet (%)
c_mamm_a=[]
wp_mamm_a=[] #Water content of in mammal's diet (consumed by amphibian)
c_herp_a=[]
bw_range_r=[]
bw_herp_r=[]
wp_herp_r=[]
c_mamm_r=[]
wp_mamm_r=[]
c_herp_r=[]

######Pre-defined outputs########
am_d_EEC=[]
am_d_EEC_hm=[]
am_d_EEC_im=[] 
am_d_EEC_tpa=[] 
am_ds_a_EEC=[]
am_ds_a_EEC_hm=[]
am_ds_a_EEC_im=[]
am_ds_a_EEC_tpa=[]
am_ds_a_RQ=[]
am_ds_a_RQ_hm=[]
am_ds_a_RQ_im=[]
am_ds_a_RQ_tpa=[]
am_d_a_RQ=[]
am_d_a_RQ_hm=[]
am_d_a_RQ_im=[]
am_d_a_RQ_tpa=[]
am_d_c_RQ=[]
am_d_c_RQ_hm=[]
am_d_c_RQ_im=[]
am_d_c_RQ_tpa=[]

rp_d_EEC=[]
rp_d_EEC_hm=[]
rp_d_EEC_im=[]
rp_d_EEC_tpa=[]
rp_ds_a_EEC=[]
rp_ds_a_EEC_hm=[]
rp_ds_a_EEC_im=[]
rp_ds_a_EEC_tpa=[]
rp_ds_a_RQ=[]
rp_ds_a_RQ_hm=[]
rp_ds_a_RQ_im=[]
rp_ds_a_RQ_tpa=[]
rp_d_a_RQ=[]
rp_d_a_RQ_hm=[]
rp_d_a_RQ_im=[]
rp_d_a_RQ_tpa=[]
rp_d_c_RQ=[]
rp_d_c_RQ_hm=[]
rp_d_c_RQ_im=[]
rp_d_c_RQ_tpa=[]

def html_table(row_inp,iter):
###Inputs###########
    chem_name_temp=str(row_inp[0])
    chem_name.append(chem_name_temp)
    use_temp=str(row_inp[1])
    use.append(use_temp)
    formu_name_temp=str(row_inp[2])
    formu_name.append(formu_name_temp)
    a_i_temp=float(row_inp[3])/100
    a_i.append(a_i_temp)
    a_r_temp=float(row_inp[4])
    a_r.append(a_r_temp)
    n_a_temp=float(row_inp[5])
    n_a.append(n_a_temp)
    a_t_temp=str(row_inp[6])
    a_t.append(a_t_temp)
    i_a_temp=float(row_inp[7])
    i_a.append(i_a_temp)
    h_l_temp=float(row_inp[8])
    h_l.append(h_l_temp)
    ld50_bird_temp=float(row_inp[9])
    ld50_bird.append(ld50_bird_temp)
    lc50_bird_temp=float(row_inp[10])
    lc50_bird.append(lc50_bird_temp)
    NOAEC_bird_temp=float(row_inp[11])
    NOAEC_bird.append(NOAEC_bird_temp)
    NOAEL_bird_temp=float(row_inp[12])
    NOAEL_bird.append(NOAEL_bird_temp)
    Species_of_the_tested_bird_temp=str(row_inp[13])
    Species_of_the_tested_bird.append(Species_of_the_tested_bird_temp)
    tw_bird_temp=float(row_inp[14])
    tw_bird.append(tw_bird_temp)
    x_temp=float(row_inp[15])
    x.append(x_temp)
    bw_range_a_temp=str(row_inp[16])
    bw_range_a.append(bw_range_a_temp)
    bw_herp_a_temp=float(row_inp[17])
    bw_herp_a.append(bw_herp_a_temp)
    wp_herp_a_temp=float(row_inp[18])/100
    wp_herp_a.append(wp_herp_a_temp)
    c_mamm_a_temp=float(row_inp[19])
    c_mamm_a.append(c_mamm_a_temp)
    wp_mamm_a_temp=float(row_inp[20])/100
    wp_mamm_a.append(wp_mamm_a_temp)
    c_herp_a_temp=float(row_inp[21])
    c_herp_a.append(c_herp_a_temp)
    bw_range_r_temp=str(row_inp[22])
    bw_range_r.append(bw_range_r_temp)
    bw_herp_r_temp=float(row_inp[23])
    bw_herp_r.append(bw_herp_r_temp)
    wp_herp_r_temp=float(row_inp[24])/100
    wp_herp_r.append(wp_herp_r_temp)
    c_mamm_r_temp=float(row_inp[25])
    c_mamm_r.append(c_mamm_r_temp)
    wp_mamm_r_temp=float(row_inp[26])/100
    wp_mamm_r.append(wp_mamm_r_temp)
    c_herp_r_temp=float(row_inp[27])
    c_herp_r.append(c_herp_r_temp)
######Output###########
    if a_t_temp=='Short grass':
       para_temp=240       #coefficient used to estimate initial conc.
    elif a_t_temp=='Tall grass':
       para_temp=110
    elif a_t_temp=='Broad-leafed plants/small insects':
       para_temp=135
    elif a_t_temp=='Fruits/pods/seeds/large insects':
       para_temp=15

    am_d_EEC.append(therps_model.EEC_diet(therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
    am_d_EEC_hm.append(therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp))
    am_d_EEC_im.append(therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp)) 
    am_d_EEC_tpa.append(therps_model.EEC_diet_tp(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_a_temp, wp_herp_a_temp))
    am_ds_a_EEC.append(therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_a_temp, therps_model.fi_herp, wp_herp_a_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
    am_ds_a_EEC_hm.append(therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, bw_herp_a_temp, c_mamm_a_temp, wp_mamm_a_temp))
    am_ds_a_EEC_im.append(therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, bw_herp_a_temp, c_mamm_a_temp, wp_mamm_a_temp))
    am_ds_a_EEC_tpa.append(therps_model.EEC_dose_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, bw_herp_a_temp, c_herp_a_temp, wp_herp_a_temp))
    am_ds_a_RQ.append(therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_a_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, wp_herp_a_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
    am_ds_a_RQ_hm.append(therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_a_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, c_mamm_a_temp, wp_mamm_a_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp))
    am_ds_a_RQ_im.append(therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_a_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, c_mamm_a_temp, wp_mamm_a_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp))
    am_ds_a_RQ_tpa.append(therps_model.ARQ_dose_tp(therps_model.EEC_dose_tp, therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_a_temp, wp_herp_a_temp, therps_model.at_bird, ld50_bird_temp, bw_herp_a_temp, tw_bird_temp, x_temp))
    am_d_a_RQ.append(therps_model.ARQ_diet_herp(therps_model.EEC_diet, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
    am_d_a_RQ_hm.append(therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp))
    am_d_a_RQ_im.append(therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp))
    am_d_a_RQ_tpa.append(therps_model.ARQ_diet_tp(therps_model.EEC_diet_tp, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_a_temp, wp_herp_a_temp))
    am_d_c_RQ.append(therps_model.CRQ_diet_herp(therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
    am_d_c_RQ_hm.append(therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp))
    am_d_c_RQ_im.append(therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp))
    am_d_c_RQ_tpa.append(therps_model.CRQ_diet_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_a_temp, wp_herp_a_temp))

    rp_d_EEC.append(therps_model.EEC_diet(therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
    rp_d_EEC_hm.append(therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))
    rp_d_EEC_im.append(therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))
    rp_d_EEC_tpa.append(therps_model.EEC_diet_tp(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_r_temp, wp_herp_r_temp))
    rp_ds_a_EEC.append(therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_r_temp, therps_model.fi_herp, wp_herp_r_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
    rp_ds_a_EEC_hm.append(therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, bw_herp_r_temp, c_mamm_r_temp, wp_mamm_r_temp))
    rp_ds_a_EEC_im.append(therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, bw_herp_r_temp, c_mamm_r_temp, wp_mamm_r_temp))
    rp_ds_a_EEC_tpa.append(therps_model.EEC_dose_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, bw_herp_r_temp, c_herp_r_temp, wp_herp_r_temp))
    rp_ds_a_RQ.append(therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_r_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, wp_herp_r_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
    rp_ds_a_RQ_hm.append(therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_r_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, c_mamm_r_temp, wp_mamm_r_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp))
    rp_ds_a_RQ_im.append(therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_r_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, c_mamm_r_temp, wp_mamm_r_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp))
    rp_ds_a_RQ_tpa.append(therps_model.ARQ_dose_tp(therps_model.EEC_dose_tp, therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_r_temp, wp_herp_r_temp, therps_model.at_bird, ld50_bird_temp, bw_herp_r_temp, tw_bird_temp, x_temp))
    rp_d_a_RQ.append(therps_model.ARQ_diet_herp(therps_model.EEC_diet, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
    rp_d_a_RQ_hm.append(therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))
    rp_d_a_RQ_im.append(therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))
    rp_d_a_RQ_tpa.append(therps_model.ARQ_diet_tp(therps_model.EEC_diet_tp, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_r_temp, wp_herp_r_temp))
    rp_d_c_RQ.append(therps_model.CRQ_diet_herp(therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
    rp_d_c_RQ_hm.append(therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))
    rp_d_c_RQ_im.append(therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))
    rp_d_c_RQ_tpa.append(therps_model.CRQ_diet_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_r_temp, wp_herp_r_temp))                                                                                                                                   

    Input_table = """<table border="1">
                        <tr><H3>Batch Calculation of Iteration %s</H3></tr><br>
                        <tr>
                            <td><b>Input Name</b></td>
                            <td><b>Input value</b></td>
                            <td><b>Unit</b></td>
                        </tr>"""%(iter)
    Input_table= Input_table + """<tr>
                    <td>Chemical name</td>
                    <td>%s</td>
                    <td></td>
                </tr>""" %(chem_name_temp) 
    Input_table = Input_table + """<tr>
                    <td>Use</td>
                    <td>%s</td>
                    <td></td>
                </tr>""" %(use_temp)                         
    Input_table = Input_table + """<tr>
                    <td>Formulated product name</td>
                    <td>%s</td>
                    <td></td>
                </tr>""" %(formu_name_temp)                          
    Input_table = Input_table + """<tr>
                   <td>Percentage of a.i</td>
                   <td>%s</td>
                   <td>&#37;</td>
               </tr>""" %(a_i_temp*100)  
    Input_table = Input_table + """<tr>
                   <td>Application rate</td>
                   <td>%s</td>
                   <td>lbs a.i./A</td>
               </tr>""" %(a_r_temp) 
    Input_table = Input_table + """<tr>
                   <td>Number of applications</td>
                   <td>%s</td>
                   <td></td>
               </tr>""" %(n_a_temp)                        
    Input_table = Input_table + """<tr>
                   <td>Application target</td>
                   <td>%s</td>
                   <td></td>
               </tr>""" %(a_t_temp)  
    Input_table = Input_table + """<tr>
                   <td>Interval between applications</td>
                   <td>%s</td>
                   <td>days</td>
               </tr>""" %(i_a_temp)  
    Input_table = Input_table + """<tr>
                   <td>Foliar dissipation half life</td>
                   <td>%s</td>
                   <td>days</td>
               </tr>""" %(h_l_temp)  
    Input_table = Input_table + """<tr>
                   <td>Avian LD50</td>
                   <td>%s</td>
                   <td>mg/kg-bw</td>
               </tr>""" %(ld50_bird_temp)  
    Input_table = Input_table + """<tr>
                   <td>Avian LC50</td>
                   <td>%s</td>
                   <td>mg/kg-diet</td>
               </tr>""" %(lc50_bird_temp)  
    Input_table = Input_table + """<tr>
                   <td>Avian NOAEC</td>
                   <td>%s</td>
                   <td>mg/kg-diet</td>
               </tr>""" %(NOAEC_bird_temp)  
    Input_table = Input_table + """<tr>
                   <td>Avian NOAEL</td>
                   <td>%s</td>
                   <td>mg/kg-bw</td>
               </tr>""" %(NOAEL_bird_temp)  
    Input_table = Input_table + """<tr>
                   <td>Species of the tested bird</td>
                   <td>%s</td>
                   <td></td>
               </tr>""" %(Species_of_the_tested_bird_temp)  
    Input_table = Input_table + """<tr>
                   <td>Body weight of the tested bird</td>
                   <td>%s</td>
                   <td>g</td>
               </tr>""" %(tw_bird_temp)  
    Input_table = Input_table + """<tr>
                   <td>Mineau scaling factor</td>
                   <td>%s</td>
                   <td></td>
               </tr>""" %(x_temp) 
    Input_table = Input_table + """<tr>
                   <td>Body weight range of the assessed amphibian</td>
                   <td>%s</td>
                   <td></td>
               </tr>""" %(bw_range_a_temp) 
    Input_table = Input_table + """<tr>
                   <td>Body weight of assessed amphibian</td>
                   <td>%s</td>
                   <td>g</td>
               </tr>""" %(bw_herp_a_temp) 
    Input_table = Input_table + """<tr>
                   <td>Water content of the assessed amphibian's diet</td>
                   <td>%s</td>
                   <td>&#37;</td>
               </tr>""" %(wp_herp_a_temp*100) 
    Input_table = Input_table + """<tr>
                   <td>Weight of the mammal consumed by amphibian</td>
                   <td>%s</td>
                   <td>g</td>
               </tr>""" %(c_mamm_a_temp) 
    Input_table = Input_table + """<tr>
                   <td>Water content of in mammal's diet (consumed by amphibian)</td>
                   <td>%s</td>
                   <td>&#37;</td>
               </tr>""" %(wp_mamm_a_temp*100) 
    Input_table = Input_table + """<tr>
                   <td>Weight of the herptile consumed by amphibian</td>
                   <td>%s</td>
                   <td>g</td>
               </tr>""" %(c_herp_a_temp) 
    Input_table = Input_table + """<tr>
                   <td>Body weight range of the assessed reptile</td>
                   <td>%s</td>
                   <td></td>
               </tr>""" %(bw_range_r_temp) 
    Input_table = Input_table + """<tr>
                   <td>Body weight of assessed reptile</td>
                   <td>%s</td>
                   <td>g</td>
               </tr>""" %(bw_herp_r_temp) 
    Input_table = Input_table + """<tr>
                   <td>Water content of the assessed reptile's diet</td>
                   <td>%s</td>
                   <td>&#37;</td>
               </tr>""" %(wp_herp_r_temp*100) 
    Input_table = Input_table + """<tr>
                   <td>Weight of the mammal consumed by reptile</td>
                   <td>%s</td>
                   <td>g</td>
               </tr>""" %(c_mamm_r_temp) 
    Input_table = Input_table + """<tr>
                   <td>Water content of in mammal's diet (consumed by reptile)</td>
                   <td>%s</td>
                   <td>&#37;</td>
               </tr>""" %(wp_mamm_r_temp*100) 
    Input_table = Input_table + """<tr>
                   <td>Weight of the herptile consumed by reptile</td>
                   <td>%s</td>
                   <td>g</td>
               </tr></table><br>""" %(c_herp_r_temp) 

    Output_table = """<table border="1">
                        <tr>
                            <td><b>Output Name</b></td>
                            <td><b>Output value</b></td>
                            <td><b>Unit</b></td>
                        </tr>"""
    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based EECs for %s</td>
                            <td>%0.2E</td>
                            <td>ppm</td>
                          </tr>""" %(a_t_temp, therps_model.EEC_diet(therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp)) 
    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based EECs for %s herbivore mammals</td>
                            <td>%0.2E</td>
                            <td>ppm</td>
                          </tr>""" %(bw_range_a_temp, therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp))
    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based EECs for %s insectivore mammals</td>
                            <td>%0.2E</td>
                            <td>ppm</td>
                          </tr>""" %(bw_range_a_temp, therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp))
    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based EECs for %s terrestrial phase amphibians </td>
                            <td>%0.2E</td>
                            <td>ppm</td>
                          </tr>""" %(bw_range_a_temp, therps_model.EEC_diet_tp(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_a_temp, wp_herp_a_temp))
    Output_table = Output_table + """<tr>
                            <td>Amphibian dose-based acute EECs for %s </td>
                            <td>%0.2E</td>
                            <td>mg/kg-bw</td>
                          </tr>""" %(a_t_temp, therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_a_temp, therps_model.fi_herp, wp_herp_a_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))  
    Output_table = Output_table + """<tr>
                            <td>Amphibian dose-based acute EECs for %s herbivore mammals </td>
                            <td>%0.2E</td>
                            <td>mg/kg-bw</td>
                          </tr>""" %(bw_range_a_temp, therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, bw_herp_a_temp, c_mamm_a_temp, wp_mamm_a_temp))
    Output_table = Output_table + """<tr>
                            <td>Amphibian dose-based acute EECs for %s insectivore mammals </td>
                            <td>%0.2E</td>
                            <td>mg/kg-bw</td>
                          </tr>""" %(bw_range_a_temp, therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, bw_herp_a_temp, c_mamm_a_temp, wp_mamm_a_temp))
    Output_table = Output_table + """<tr>
                            <td>Amphibian dose-based acute EECs for %s terrestrial phase amphibians </td>
                            <td>%0.2E</td>
                            <td>mg/kg-bw</td>
                          </tr>""" %(bw_range_a_temp, therps_model.EEC_dose_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, bw_herp_a_temp, c_herp_a_temp, wp_herp_a_temp))
    Output_table = Output_table + """<tr>
                            <td>Amphibian dose-based acute RQs for %s </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(a_t_temp, therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_a_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, wp_herp_a_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))


    Output_table = Output_table + """<tr>
                            <td>Amphibian dose-based acute RQs for %s herbivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_a_temp, therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_a_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, c_mamm_a_temp, wp_mamm_a_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp))

    Output_table = Output_table + """<tr>
                            <td>Amphibian dose-based acute RQs for %s insectivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_a_temp, therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_a_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, c_mamm_a_temp, wp_mamm_a_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp))

    Output_table = Output_table + """<tr>
                            <td>Amphibian dose-based acute RQs for %s terrestrial phase amphibians </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_a_temp, therps_model.ARQ_dose_tp(therps_model.EEC_dose_tp, therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_a_temp, wp_herp_a_temp, therps_model.at_bird, ld50_bird_temp, bw_herp_a_temp, tw_bird_temp, x_temp))

    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based acute RQs for %s </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(a_t_temp, therps_model.ARQ_diet_herp(therps_model.EEC_diet, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))

    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based acute RQs for %s herbivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_a_temp, therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp))

    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based acute RQs for %s insectivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_a_temp, therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp))

    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based acute RQs for %s terrestrial phase amphibians </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_a_temp, therps_model.ARQ_diet_tp(therps_model.EEC_diet_tp, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_a_temp, wp_herp_a_temp))
                            
    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based chronic RQs for %s </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(a_t_temp, therps_model.CRQ_diet_herp(therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
 
    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based chronic RQs for %s herbivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_a_temp, therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp))

    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based chronic RQs for %s insectivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_a_temp, therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_a_temp, wp_mamm_a_temp))

    Output_table = Output_table + """<tr>
                            <td>Amphibian dietary-based chronic RQs for %s terrestrial phase amphibians </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_a_temp, therps_model.CRQ_diet_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_a_temp, wp_herp_a_temp))
             

    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based EECs for %s </td>
                            <td>%0.2E</td>
                            <td>ppm</td>
                          </tr>""" %(a_t_temp, therps_model.EEC_diet(therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))

    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based EECs for %s herbivore mammals </td>
                            <td>%0.2E</td>
                            <td>ppm</td>
                          </tr>""" %(bw_range_r_temp, therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))
          
    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based EECs for %s insectivore mammals </td>
                            <td>%0.2E</td>
                            <td>ppm</td>
                          </tr>""" %(bw_range_r_temp, therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))
         
    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based EECs for %s terrestrial phase amphibians </td>
                            <td>%0.2E</td>
                            <td>ppm</td>
                          </tr>""" %(bw_range_r_temp, therps_model.EEC_diet_tp(therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_r_temp, wp_herp_r_temp))
              
    Output_table = Output_table + """<tr>
                            <td>Reptile dose-based acute EECs for %s </td>
                            <td>%0.2E</td>
                            <td>mg/kg-bw</td>
                          </tr>"""%(a_t_temp, therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_r_temp, therps_model.fi_herp, wp_herp_r_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))

    Output_table = Output_table + """<tr>
                            <td>Reptile dose-based acute EECs for %s herbivore mammals </td>
                            <td>%0.2E</td>
                            <td>mg/kg-bw</td>
                          </tr>""" %(bw_range_r_temp, therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, bw_herp_r_temp, c_mamm_r_temp, wp_mamm_r_temp))
 
    Output_table = Output_table + """<tr>
                            <td>Reptile dose-based acute EECs for %s insectivore mammals </td>
                            <td>%0.2E</td>
                            <td>mg/kg-bw</td>
                          </tr>""" %(bw_range_r_temp, therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, bw_herp_r_temp, c_mamm_r_temp, wp_mamm_r_temp))
                           
    Output_table = Output_table + """<tr>
                            <td>Reptile dose-based acute EECs for %s terrestrial phase amphibians </td>
                            <td>%0.2E</td>
                            <td>mg/kg-bw</td>
                          </tr>""" %(bw_range_r_temp, therps_model.EEC_dose_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, bw_herp_r_temp, c_herp_r_temp, wp_herp_r_temp))
                            
    Output_table = Output_table + """<tr>
                            <td>Reptile dose-based acute RQs for %s </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(a_t_temp, therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_r_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, wp_herp_r_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))
                             
    Output_table = Output_table + """<tr>
                            <td>Reptile dose-based acute RQs for %s herbivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_r_temp, therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_r_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, c_mamm_r_temp, wp_mamm_r_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp))
                          
    Output_table = Output_table + """<tr>
                            <td>Reptile dose-based acute RQs for %s insectivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_r_temp, therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_r_temp, therps_model.fi_herp, therps_model.at_bird, ld50_bird_temp, tw_bird_temp, x_temp, c_mamm_r_temp, wp_mamm_r_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp))

    Output_table = Output_table + """<tr>
                            <td>Reptile dose-based acute RQs for %s terrestrial phase amphibians </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_r_temp, therps_model.ARQ_dose_tp(therps_model.EEC_dose_tp, therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_r_temp, wp_herp_r_temp, therps_model.at_bird, ld50_bird_temp, bw_herp_r_temp, tw_bird_temp, x_temp))

    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based acute RQs for %s </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(a_t_temp, therps_model.ARQ_diet_herp(therps_model.EEC_diet, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))


    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based acute RQs for %s herbivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_r_temp, therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))

    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based acute RQs for %s insectivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_r_temp, therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))

    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based acute RQs for %s terrestrial phase amphibians </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_r_temp, therps_model.ARQ_diet_tp(therps_model.EEC_diet_tp, lc50_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_r_temp, wp_herp_r_temp))
                            

    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based chronic RQs for %s </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(a_t_temp, therps_model.CRQ_diet_herp(therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, para_temp, h_l_temp))

    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based chronic RQs for %s herbivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_r_temp, therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 240, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))
                           

    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based chronic RQs for %s insectivore mammals </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_r_temp, therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 15, h_l_temp, therps_model.fi_mamm, c_mamm_r_temp, wp_mamm_r_temp))

    Output_table = Output_table + """<tr>
                            <td>Reptile dietary-based chronic RQs for %s terrestrial phase amphibians </td>
                            <td>%0.2E</td>
                            <td></td>
                          </tr>""" %(bw_range_r_temp, therps_model.CRQ_diet_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, NOAEC_bird_temp, therps_model.C_0, n_a_temp, i_a_temp, a_r_temp, a_i_temp, 135, h_l_temp, therps_model.fi_herp, c_herp_r_temp, wp_herp_r_temp))            

    Inout_table = Input_table+Output_table
    return Inout_table  


def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    exclud_list = ['', " ", "  ", "   ", "    ", "     ", "      ", "       ", "        ", "         ", "          "]
    i=1

    iter_html=""
    for row in reader:
        if row[3] in exclud_list:
            break
        iter_html = iter_html +html_table(row,i)
        i=i+1
    sum_html ="""<table border="1">
                        <tr><H3>Summary Statistics (Iterations=%s)</H3></tr><br>
                        <tr>
                            <td><b>Input Name</b></td>
                            <td><b>Mean</b></td>
                            <td><b>Std.</b></td>
                            <td><b>Min</b></td>
                            <td><b>Max</b></td>                            
                            <td><b>Unit</b></td>
                        </tr>"""%(i-1)
                        
    sum_html = sum_html + """<tr>
                    <td>Percentage of a.i</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                    
                    <td>&#37;</td>
                </tr>""" %(numpy.mean(a_i)*100, numpy.std(a_i)*100, numpy.min(a_i)*100, numpy.max(a_i)*100)  
    sum_html = sum_html + """<tr>
                    <td>Application rate</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>   
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                       
                    <td>lbs a.i./A</td>
                </tr>""" %(numpy.mean(a_r), numpy.std(a_r), numpy.min(a_r), numpy.max(a_r))                         
    sum_html = sum_html + """<tr>
                    <td>Number of applications</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                        
                    <td></td>
                </tr>""" %(numpy.mean(n_a), numpy.std(n_a), numpy.min(n_a), numpy.max(n_a))                          
    sum_html = sum_html + """<tr>
                    <td>Interval between applications</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>days</td>
                </tr>""" %(numpy.mean(i_a), numpy.std(i_a), numpy.min(i_a), numpy.max(i_a))  
    sum_html = sum_html + """<tr>
                    <td>Foliar dissipation half life</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td> 
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                     
                    <td>days</td>
                </tr>""" %(numpy.mean(h_l), numpy.std(h_l), numpy.min(h_l), numpy.max(h_l)) 
    sum_html = sum_html + """<tr>
                    <td>Avian LD50</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>  
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                        
                    <td>mg/kg-bw</td>
                </tr>""" %(numpy.mean(ld50_bird), numpy.std(ld50_bird), numpy.min(ld50_bird), numpy.max(ld50_bird))                        
    sum_html = sum_html + """<tr>
                    <td>Avian LC50</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>mg/kg-diet</td>
                </tr>""" %(numpy.mean(lc50_bird), numpy.std(lc50_bird), numpy.min(lc50_bird), numpy.max(lc50_bird))  
    sum_html = sum_html + """<tr>
                    <td>Avian NOAEC</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>mg/kg-diet</td>
                </tr>""" %(numpy.mean(NOAEC_bird), numpy.std(NOAEC_bird), numpy.min(NOAEC_bird), numpy.max(NOAEC_bird))  
    sum_html = sum_html + """<tr>
                    <td>Avian NOAEL</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>mg/kg-bw</td>
                </tr>""" %(numpy.mean(NOAEL_bird), numpy.std(NOAEL_bird), numpy.min(NOAEL_bird), numpy.max(NOAEL_bird))  
    sum_html = sum_html + """<tr>
                    <td>Body weight of the tested bird</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>g</td>
                </tr>""" %(numpy.mean(tw_bird), numpy.std(tw_bird), numpy.min(tw_bird), numpy.max(tw_bird))  
    sum_html = sum_html + """<tr>
                    <td>Mineau scaling factor</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td></td>
                </tr>""" %(numpy.mean(x), numpy.std(x), numpy.min(x), numpy.max(x))  
    sum_html = sum_html + """<tr>
                    <td>Body weight of assessed amphibian</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>g</td>
                </tr>""" %(numpy.mean(bw_herp_a), numpy.std(bw_herp_a), numpy.min(bw_herp_a), numpy.max(bw_herp_a))  
    sum_html = sum_html + """<tr>
                    <td>Body weight of assessed amphibian</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>g</td>
                </tr>""" %(numpy.mean(bw_herp_a), numpy.std(bw_herp_a), numpy.min(bw_herp_a), numpy.max(bw_herp_a))  
    sum_html = sum_html + """<tr>
                    <td>Water content of the assessed amphibian's diet</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>&#37;</td>
                </tr>""" %(numpy.mean(wp_herp_a)*100, numpy.std(wp_herp_a)*100, numpy.min(wp_herp_a)*100, numpy.max(wp_herp_a)*100)  
    sum_html = sum_html + """<tr>
                    <td>Weight of the mammal consumed by amphibian</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>g</td>
                </tr>""" %(numpy.mean(c_mamm_a), numpy.std(c_mamm_a), numpy.min(c_mamm_a), numpy.max(c_mamm_a))  
    sum_html = sum_html + """<tr>
                    <td>Water content of in mammal's diet (consumed by amphibian)</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>&#37;</td>
                </tr>""" %(numpy.mean(wp_herp_a)*100, numpy.std(wp_herp_a)*100, numpy.min(wp_herp_a)*100, numpy.max(wp_herp_a)*100)  
    sum_html = sum_html + """<tr>
                    <td>Water content of in mammal's diet (consumed by amphibian)</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>&#37;</td>
                </tr>""" %(numpy.mean(wp_herp_a)*100, numpy.std(wp_herp_a)*100, numpy.min(wp_herp_a)*100, numpy.max(wp_herp_a)*100)  
    sum_html = sum_html + """<tr>
                    <td>Weight of the herptile consumed by amphibian</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td></td>
                </tr>""" %(numpy.mean(c_herp_a), numpy.std(c_herp_a), numpy.min(c_herp_a), numpy.max(c_herp_a))  
    sum_html = sum_html + """<tr>
                    <td>Body weight of assessed reptile</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>g</td>
                </tr>""" %(numpy.mean(bw_herp_r), numpy.std(bw_herp_r), numpy.min(bw_herp_r), numpy.max(bw_herp_r))  
    sum_html = sum_html + """<tr>
                    <td>Water content of the assessed reptile's diet</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>&#37;</td>
                </tr>""" %(numpy.mean(wp_herp_r)*100, numpy.std(wp_herp_r)*100, numpy.min(wp_herp_r)*100, numpy.max(wp_herp_r)*100)  
    sum_html = sum_html + """<tr>
                    <td>Weight of the mammal consumed by reptile</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>g</td>
                </tr>""" %(numpy.mean(c_mamm_r), numpy.std(c_mamm_r), numpy.min(c_mamm_r), numpy.max(c_mamm_r))  
    sum_html = sum_html + """<tr>
                    <td>Water content of in mammal's diet (consumed by reptile)</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>&#37;</td>
                </tr>""" %(numpy.mean(wp_mamm_r)*100, numpy.std(wp_mamm_r)*100, numpy.min(wp_mamm_r)*100, numpy.max(wp_mamm_r)*100) 
    sum_html = sum_html + """<tr>
                    <td>Weight of the herptile consumed by reptile</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>
                    <td>%5.2f</td>                                          
                    <td>g</td>
                </tr></table><br>""" %(numpy.mean(c_herp_r), numpy.std(c_herp_r), numpy.min(c_herp_r), numpy.max(c_herp_r)) 

    sum_html = sum_html + """<table border="1">
                        <tr>
                            <td><b>Output Name</b></td>
                            <td><b>Mean</b></td>
                            <td><b>Std.</b></td>
                            <td><b>Min</b></td>
                            <td><b>Max</b></td>                             
                            <td><b>Unit</b></td>
                        </tr>"""

    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based EECs</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>ppm</td>
                </tr>""" %(numpy.mean(am_d_EEC), numpy.std(am_d_EEC), numpy.min(am_d_EEC), numpy.max(am_d_EEC))
   
    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based EECs for herbivore mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>ppm</td>
                </tr>""" %(numpy.mean(am_d_EEC_hm), numpy.std(am_d_EEC_hm), numpy.min(am_d_EEC_hm), numpy.max(am_d_EEC_hm))
   
    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based EECs for insectivore mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>ppm</td>
                </tr>""" %(numpy.mean(am_d_EEC_im), numpy.std(am_d_EEC_im), numpy.min(am_d_EEC_im), numpy.max(am_d_EEC_im))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based EECs for terrestrial phase amphibians</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>ppm</td>
                </tr>""" %(numpy.mean(am_d_EEC_tpa), numpy.std(am_d_EEC_tpa), numpy.min(am_d_EEC_tpa), numpy.max(am_d_EEC_tpa))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dose-based acute EECs</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>mg/kg-bw</td>
                </tr>""" %(numpy.mean(am_ds_a_EEC), numpy.std(am_ds_a_EEC), numpy.min(am_ds_a_EEC), numpy.max(am_ds_a_EEC))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dose-based acute EECs for herbivore mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>mg/kg-bw</td>
                </tr>""" %(numpy.mean(am_ds_a_EEC_hm), numpy.std(am_ds_a_EEC_hm), numpy.min(am_ds_a_EEC_hm), numpy.max(am_ds_a_EEC_hm))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dose-based acute EECs for insectivore mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>mg/kg-bw</td>
                </tr>""" %(numpy.mean(am_ds_a_EEC_im), numpy.std(am_ds_a_EEC_im), numpy.min(am_ds_a_EEC_im), numpy.max(am_ds_a_EEC_im))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dose-based acute EECs for terrestrial phase amphibians</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>mg/kg-bw</td>
                </tr>""" %(numpy.mean(am_ds_a_EEC_tpa), numpy.std(am_ds_a_EEC_tpa), numpy.min(am_ds_a_EEC_tpa), numpy.max(am_ds_a_EEC_tpa))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dose-based acute RQs</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_ds_a_RQ), numpy.std(am_ds_a_RQ), numpy.min(am_ds_a_RQ), numpy.max(am_ds_a_RQ))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dose-based acute RQs for herbivore mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_ds_a_RQ_hm), numpy.std(am_ds_a_RQ_hm), numpy.min(am_ds_a_RQ_hm), numpy.max(am_ds_a_RQ_hm))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dose-based acute RQs for insectivore mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_ds_a_RQ_im), numpy.std(am_ds_a_RQ_im), numpy.min(am_ds_a_RQ_im), numpy.max(am_ds_a_RQ_im))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dose-based acute RQs for terrestrial phase amphibians</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_ds_a_RQ_tpa), numpy.std(am_ds_a_RQ_tpa), numpy.min(am_ds_a_RQ_tpa), numpy.max(am_ds_a_RQ_tpa))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based acute RQs</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_d_a_RQ), numpy.std(am_d_a_RQ), numpy.min(am_d_a_RQ), numpy.max(am_d_a_RQ))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based acute RQs for herbivore mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_d_a_RQ_hm), numpy.std(am_d_a_RQ_hm), numpy.min(am_d_a_RQ_hm), numpy.max(am_d_a_RQ_hm))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based acute RQs for insectivore mammals</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_d_a_RQ_im), numpy.std(am_d_a_RQ_im), numpy.min(am_d_a_RQ_im), numpy.max(am_d_a_RQ_im))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based acute RQs for terrestrial phase amphibians</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_d_a_RQ_im), numpy.std(am_d_a_RQ_im), numpy.min(am_d_a_RQ_im), numpy.max(am_d_a_RQ_im))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based chronic RQs</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_d_c_RQ), numpy.std(am_d_c_RQ), numpy.min(am_d_c_RQ), numpy.max(am_d_c_RQ))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based chronic RQs for herbivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_d_c_RQ_hm), numpy.std(am_d_c_RQ_hm), numpy.min(am_d_c_RQ_hm), numpy.max(am_d_c_RQ_hm))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based chronic RQs for insectivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_d_c_RQ_im), numpy.std(am_d_c_RQ_im), numpy.min(am_d_c_RQ_im), numpy.max(am_d_c_RQ_im))
    sum_html = sum_html + """<tr>
                    <td>Amphibian dietary-based chronic RQs for terrestrial phase amphibians </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(am_d_c_RQ_tpa), numpy.std(am_d_c_RQ_tpa), numpy.min(am_d_c_RQ_tpa), numpy.max(am_d_c_RQ_tpa))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based EECs </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>ppm</td>
                </tr>""" %(numpy.mean(rp_d_EEC), numpy.std(rp_d_EEC), numpy.min(rp_d_EEC), numpy.max(rp_d_EEC))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based EECs for herbivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>ppm</td>
                </tr>""" %(numpy.mean(rp_d_EEC_hm), numpy.std(rp_d_EEC_hm), numpy.min(rp_d_EEC_hm), numpy.max(rp_d_EEC_hm))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based EECs for insectivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>ppm</td>
                </tr>""" %(numpy.mean(rp_d_EEC_im), numpy.std(rp_d_EEC_im), numpy.min(rp_d_EEC_im), numpy.max(rp_d_EEC_im))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based EECs for terrestrial phase amphibians </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>ppm</td>
                </tr>""" %(numpy.mean(rp_d_EEC_tpa), numpy.std(rp_d_EEC_tpa), numpy.min(rp_d_EEC_tpa), numpy.max(rp_d_EEC_tpa))
    sum_html = sum_html + """<tr>
                    <td>Reptile dose-based acute EECs </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>mg/kg-bw</td>
                </tr>""" %(numpy.mean(rp_ds_a_EEC), numpy.std(rp_ds_a_EEC), numpy.min(rp_ds_a_EEC), numpy.max(rp_ds_a_EEC))
    sum_html = sum_html + """<tr>
                    <td>Reptile dose-based acute EECs for herbivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>mg/kg-bw</td>
                </tr>""" %(numpy.mean(rp_ds_a_EEC_hm), numpy.std(rp_ds_a_EEC_hm), numpy.min(rp_ds_a_EEC_hm), numpy.max(rp_ds_a_EEC_hm))
    sum_html = sum_html + """<tr>
                    <td>Reptile dose-based acute EECs for insectivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>mg/kg-bw</td>
                </tr>""" %(numpy.mean(rp_ds_a_EEC_im), numpy.std(rp_ds_a_EEC_im), numpy.min(rp_ds_a_EEC_im), numpy.max(rp_ds_a_EEC_im))
    sum_html = sum_html + """<tr>
                    <td>Reptile dose-based acute EECs for terrestrial phase amphibians </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td>mg/kg-bw</td>
                </tr>""" %(numpy.mean(rp_ds_a_EEC_tpa), numpy.std(rp_ds_a_EEC_tpa), numpy.min(rp_ds_a_EEC_tpa), numpy.max(rp_ds_a_EEC_tpa))
    sum_html = sum_html + """<tr>
                    <td>Reptile dose-based acute RQs </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_ds_a_RQ), numpy.std(rp_ds_a_RQ), numpy.min(rp_ds_a_RQ), numpy.max(rp_ds_a_RQ))
    sum_html = sum_html + """<tr>
                    <td>Reptile dose-based acute RQs for herbivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_ds_a_RQ_hm), numpy.std(rp_ds_a_RQ_hm), numpy.min(rp_ds_a_RQ_hm), numpy.max(rp_ds_a_RQ_hm))
    sum_html = sum_html + """<tr>
                    <td>Reptile dose-based acute RQs for insectivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_ds_a_RQ_im), numpy.std(rp_ds_a_RQ_im), numpy.min(rp_ds_a_RQ_im), numpy.max(rp_ds_a_RQ_im))
    sum_html = sum_html + """<tr>
                    <td>Reptile dose-based acute RQs for terrestrial phase amphibians </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_ds_a_RQ_tpa), numpy.std(rp_ds_a_RQ_tpa), numpy.min(rp_ds_a_RQ_tpa), numpy.max(rp_ds_a_RQ_tpa))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based acute RQs </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_d_a_RQ), numpy.std(rp_d_a_RQ), numpy.min(rp_d_a_RQ), numpy.max(rp_d_a_RQ))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based acute RQs for herbivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_d_a_RQ_hm), numpy.std(rp_d_a_RQ_hm), numpy.min(rp_d_a_RQ_hm), numpy.max(rp_d_a_RQ_hm))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based acute RQs for insectivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_d_a_RQ_im), numpy.std(rp_d_a_RQ_im), numpy.min(rp_d_a_RQ_im), numpy.max(rp_d_a_RQ_im))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based acute RQs for terrestrial phase amphibians </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_d_a_RQ_tpa), numpy.std(rp_d_a_RQ_tpa), numpy.min(rp_d_a_RQ_tpa), numpy.max(rp_d_a_RQ_tpa))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based chronic RQs </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_d_c_RQ), numpy.std(rp_d_c_RQ), numpy.min(rp_d_c_RQ), numpy.max(rp_d_c_RQ))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based chronic RQs for herbivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_d_c_RQ_hm), numpy.std(rp_d_c_RQ_hm), numpy.min(rp_d_c_RQ_hm), numpy.max(rp_d_c_RQ_hm))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based chronic RQs for herbivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_d_c_RQ_hm), numpy.std(rp_d_c_RQ_hm), numpy.min(rp_d_c_RQ_hm), numpy.max(rp_d_c_RQ_hm))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based chronic RQs for insectivore mammals </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_d_c_RQ_im), numpy.std(rp_d_c_RQ_im), numpy.min(rp_d_c_RQ_im), numpy.max(rp_d_c_RQ_im))
    sum_html = sum_html + """<tr>
                    <td>Reptile dietary-based chronic RQs for terrestrial phase amphibians </td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>
                    <td>%0.2E</td>                      
                    <td></td>
                </tr>""" %(numpy.mean(rp_d_c_RQ_tpa), numpy.std(rp_d_c_RQ_tpa), numpy.min(rp_d_c_RQ_tpa), numpy.max(rp_d_c_RQ_tpa))      
                                     
    total_html=sum_html+iter_html    
    return total_html


class TherpsBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['upfile']
        # reader = csv.reader(thefile.file.read().splitlines())
        # header = reader.next()
        # exclud_list = ['', " ", "  ", "   ", "    ", "     ", "      ", "       ", "        ", "         ", "          "]
        # i=1

        # for row in reader:
        #     if row[3] in exclud_list:
        #         break

            # print html_table(row,i)

        # print loop_html(thefile)
            # i=i+1

        # iter_html=loop_html(thefile)        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'therps','page':'batchinput'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {})
        html = html + loop_html(thefile)
        # html = html + template.render(templatepath + 'rice-batchoutput-jqplot.html', {})                
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TherpsBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

