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
import csv
from therps import therps_tables,therps_model
from uber import uber_lib
import Queue
from collections import OrderedDict
import rest_funcs

chem_name=[]
use=[]
formu_name=[]
a_i=[]
a_i_disp=[]
a_r=[]
n_a=[]
i_a=[]
h_l=[]
ld50_bird=[]
Species_of_the_tested_bird_avian_ld50=[]
bw_avian_ld50=[]
lc50_bird=[]
Species_of_the_tested_bird_avian_lc50=[]
bw_avian_lc50=[]
NOAEC_bird=[]
Species_of_the_tested_bird_avian_NOAEC=[]
bw_avian_NOAEC=[]
NOAEL_bird=[]
Species_of_the_tested_bird_avian_NOAEL=[]
bw_avian_NOAEL=[]
x=[]
c_mamm_a=[]
c_herp_a=[]
bw_herp_a_sm=[]
bw_herp_a_md=[]
bw_herp_a_lg=[]
wp_herp_a_sm=[]
wp_herp_a_md=[]
wp_herp_a_lg=[]

######Pre-defined outputs########
EEC_diet_herp_BL_out=[]
EEC_ARQ_herp_BL_out=[]
EEC_CRQ_herp_BL_out=[]
EEC_diet_herp_FR_out=[]
EEC_ARQ_herp_FR_out=[]
EEC_CRQ_herp_FR_out=[]
EEC_diet_herp_HM_out=[]
EEC_ARQ_herp_HM_out=[]
EEC_CRQ_herp_HM_out=[]
EEC_diet_herp_IM_out=[]
EEC_ARQ_herp_IM_out=[]
EEC_CRQ_herp_IM_out=[]
EEC_diet_herp_TP_out=[]
EEC_ARQ_herp_TP_out=[]
EEC_CRQ_herp_TP_out=[]
LD50_AD_sm_out=[]
LD50_AD_md_out=[]
LD50_AD_lg_out=[]
EEC_dose_BP_sm_out=[]
EEC_dose_BP_md_out=[]
EEC_dose_BP_lg_out=[]
ARQ_dose_BP_sm_out=[]
ARQ_dose_BP_md_out=[]
ARQ_dose_BP_lg_out=[]
EEC_dose_FR_sm_out=[]
EEC_dose_FR_md_out=[]
EEC_dose_FR_lg_out=[]
ARQ_dose_FR_sm_out=[]
ARQ_dose_FR_md_out=[]
ARQ_dose_FR_lg_out=[]
EEC_dose_HM_md_out=[]
EEC_dose_HM_lg_out=[]
ARQ_dose_HM_md_out=[]
ARQ_dose_HM_lg_out=[]
EEC_dose_IM_md_out=[]
EEC_dose_IM_lg_out=[]
ARQ_dose_IM_md_out=[]
ARQ_dose_IM_lg_out=[]
EEC_dose_TP_md_out=[]
EEC_dose_TP_lg_out=[]
ARQ_dose_TP_md_out=[]
ARQ_dose_TP_lg_out=[]

EEC_diet_herp_BL_out_mean=[]
EEC_ARQ_herp_BL_out_mean=[]
EEC_CRQ_herp_BL_out_mean=[]
EEC_diet_herp_FR_out_mean=[]
EEC_ARQ_herp_FR_out_mean=[]
EEC_CRQ_herp_FR_out_mean=[]
EEC_diet_herp_HM_out_mean=[]
EEC_ARQ_herp_HM_out_mean=[]
EEC_CRQ_herp_HM_out_mean=[]
EEC_diet_herp_IM_out_mean=[]
EEC_ARQ_herp_IM_out_mean=[]
EEC_CRQ_herp_IM_out_mean=[]
EEC_diet_herp_TP_out_mean=[]
EEC_ARQ_herp_TP_out_mean=[]
EEC_CRQ_herp_TP_out_mean=[]
LD50_AD_sm_out_mean=[]
LD50_AD_md_out_mean=[]
LD50_AD_lg_out_mean=[]
EEC_dose_BP_sm_out_mean=[]
EEC_dose_BP_md_out_mean=[]
EEC_dose_BP_lg_out_mean=[]
ARQ_dose_BP_sm_out_mean=[]
ARQ_dose_BP_md_out_mean=[]
ARQ_dose_BP_lg_out_mean=[]
EEC_dose_FR_sm_out_mean=[]
EEC_dose_FR_md_out_mean=[]
EEC_dose_FR_lg_out_mean=[]
ARQ_dose_FR_sm_out_mean=[]
ARQ_dose_FR_md_out_mean=[]
ARQ_dose_FR_lg_out_mean=[]
EEC_dose_HM_md_out_mean=[]
EEC_dose_HM_lg_out_mean=[]
ARQ_dose_HM_md_out_mean=[]
ARQ_dose_HM_lg_out_mean=[]
EEC_dose_IM_md_out_mean=[]
EEC_dose_IM_lg_out_mean=[]
ARQ_dose_IM_md_out_mean=[]
ARQ_dose_IM_lg_out_mean=[]
EEC_dose_TP_md_out_mean=[]
EEC_dose_TP_lg_out_mean=[]
ARQ_dose_TP_md_out_mean=[]
ARQ_dose_TP_lg_out_mean=[]

jid_all = []
jid_batch = []
therps_obj_all = []

def html_table(row_inp,iter):
    while True:
        row_inp_temp_all = row_inp_all.get()
        if row_inp_temp_all is None:
            break
        else:
            row_inp = row_inp_temp_all[0]
            iter = row_inp_temp_all[1]
###Inputs###########
    chem_name_temp=str(row_inp[0])
    chem_name.append(chem_name_temp)
    use_temp=str(row_inp[1])
    use.append(use_temp)
    formu_name_temp=str(row_inp[2])
    formu_name.append(formu_name_temp)
    a_i_temp=float(row_inp[3])/100
    a_i.append(a_i_temp)
    a_i_disp.append(100*a_i_temp)
    a_r_temp=float(row_inp[4])
    a_r.append(a_r_temp)
    n_a_temp=float(row_inp[5])
    n_a.append(n_a_temp)
    i_a_temp=float(row_inp[6])
    i_a.append(i_a_temp)
    h_l_temp=float(row_inp[7])
    h_l.append(h_l_temp)
    ld50_bird_temp=float(row_inp[8])
    ld50_bird.append(ld50_bird_temp)
    Species_of_the_tested_bird_avian_ld50_temp=str(row_inp[9])
    Species_of_the_tested_bird_avian_ld50.append(Species_of_the_tested_bird_avian_ld50_temp)
    bw_avian_ld50_temp=float(row_inp[10])
    bw_avian_ld50.append(bw_avian_ld50_temp)
    lc50_bird_temp=float(row_inp[11])
    lc50_bird.append(lc50_bird_temp)
    Species_of_the_tested_bird_avian_lc50_temp=str(row_inp[12])
    Species_of_the_tested_bird_avian_lc50.append(Species_of_the_tested_bird_avian_lc50_temp)
    bw_avian_lc50_temp=float(row_inp[13])
    bw_avian_lc50.append(bw_avian_lc50_temp)
    NOAEC_bird_temp=float(row_inp[14])
    NOAEC_bird.append(NOAEC_bird_temp)
    Species_of_the_tested_bird_avian_NOAEC_temp=str(row_inp[15])
    Species_of_the_tested_bird_avian_NOAEC.append(Species_of_the_tested_bird_avian_NOAEC_temp)
    bw_avian_NOAEC_temp=float(row_inp[16])
    bw_avian_NOAEC.append(bw_avian_NOAEC_temp)
    NOAEL_bird_temp=float(row_inp[17])
    NOAEL_bird.append(NOAEL_bird_temp)
    Species_of_the_tested_bird_avian_NOAEL_temp=str(row_inp[18])
    Species_of_the_tested_bird_avian_NOAEL.append(Species_of_the_tested_bird_avian_NOAEL_temp)
    bw_avian_NOAEL_temp=float(row_inp[19])
    bw_avian_NOAEL.append(bw_avian_NOAEL_temp)
    x_temp=float(row_inp[20])
    x.append(x_temp)
    c_mamm_a_temp=float(row_inp[21])
    c_mamm_a.append(c_mamm_a_temp)
    c_herp_a_temp=float(row_inp[22])
    c_herp_a.append(c_herp_a_temp)
    bw_herp_a_sm_temp=float(row_inp[23])
    bw_herp_a_sm.append(bw_herp_a_sm_temp)
    wp_herp_a_sm_temp=float(row_inp[24])/100
    wp_herp_a_sm.append(wp_herp_a_sm_temp)
    bw_herp_a_md_temp=float(row_inp[25])
    bw_herp_a_md.append(bw_herp_a_md_temp)
    wp_herp_a_md_temp=float(row_inp[26])/100
    wp_herp_a_md.append(wp_herp_a_md_temp)
    bw_herp_a_lg_temp=float(row_inp[27])
    bw_herp_a_lg.append(bw_herp_a_lg_temp)
    wp_herp_a_lg_temp=float(row_inp[28])/100
    wp_herp_a_lg.append(wp_herp_a_lg_temp)

    Input_header="""<div class="out_">
                        <br><H3>Batch Calculation of Iteration %s</H3>
                    </div>"""%(iter)

    therps_obj_temp = therps_model.therps("batch",chem_name_temp, use_temp, formu_name_temp, a_i_temp, h_l_temp, n_a_temp, i_a_temp, a_r_temp, 
                                          ld50_bird_temp, lc50_bird_temp, NOAEC_bird_temp, NOAEL_bird_temp, 
                                          Species_of_the_tested_bird_avian_ld50_temp, Species_of_the_tested_bird_avian_lc50_temp, Species_of_the_tested_bird_avian_NOAEC_temp, Species_of_the_tested_bird_avian_NOAEL_temp,
                                          bw_avian_ld50_temp, bw_avian_lc50_temp, bw_avian_NOAEC_temp, bw_avian_NOAEL_temp,
                                          x_temp, bw_herp_a_sm_temp, bw_herp_a_md_temp, bw_herp_a_lg_temp, wp_herp_a_sm_temp, wp_herp_a_md_temp, wp_herp_a_lg_temp, c_mamm_a_temp, c_herp_a_temp)

    table_all_out = therps_tables.table_all(therps_obj_temp)
    html_table_temp = Input_header + table_all_out[0] + "<br>"
    out_html_all[iter]=html_table_temp

    EEC_diet_herp_BL_temp=table_all_out[3]['EEC_diet_herp_BL']
    EEC_diet_herp_BL_out.append(EEC_diet_herp_BL_temp)
    EEC_CRQ_herp_BL_temp=table_all_out[3]['EEC_CRQ_herp_BL']
    EEC_CRQ_herp_BL_out.append(EEC_CRQ_herp_BL_temp)
    EEC_diet_herp_FR_temp=table_all_out[3]['EEC_diet_herp_FR']
    EEC_diet_herp_FR_out.append(EEC_diet_herp_FR_temp)
    EEC_CRQ_herp_FR_temp=table_all_out[3]['EEC_CRQ_herp_FR']
    EEC_CRQ_herp_FR_out.append(EEC_CRQ_herp_FR_temp)
    EEC_CRQ_herp_HM_temp=table_all_out[3]['EEC_CRQ_herp_HM']
    EEC_CRQ_herp_HM_out.append(EEC_CRQ_herp_HM_temp)
    EEC_diet_herp_IM_temp=table_all_out[3]['EEC_diet_herp_IM']
    EEC_diet_herp_IM_out.append(EEC_diet_herp_IM_temp)
    EEC_CRQ_herp_IM_temp=table_all_out[3]['EEC_CRQ_herp_IM']
    EEC_CRQ_herp_IM_out.append(EEC_CRQ_herp_IM_temp)
    EEC_diet_herp_TP_temp=table_all_out[3]['EEC_diet_herp_TP']
    EEC_diet_herp_TP_out.append(EEC_diet_herp_TP_temp)
    EEC_CRQ_herp_TP_temp=table_all_out[3]['EEC_CRQ_herp_TP']
    EEC_CRQ_herp_TP_out.append(EEC_CRQ_herp_TP_temp)

    EEC_ARQ_herp_BL_temp=table_all_out[2]['EEC_ARQ_herp_BL']
    EEC_ARQ_herp_BL_out.append(EEC_ARQ_herp_BL_temp)
    EEC_ARQ_herp_FR_temp=table_all_out[2]['EEC_ARQ_herp_FR']
    EEC_ARQ_herp_FR_out.append(EEC_ARQ_herp_FR_temp)
    EEC_diet_herp_HM_temp=table_all_out[2]['EEC_diet_herp_HM']
    EEC_diet_herp_HM_out.append(EEC_diet_herp_HM_temp)
    EEC_ARQ_herp_HM_temp=table_all_out[2]['EEC_ARQ_herp_HM']
    EEC_ARQ_herp_HM_out.append(EEC_ARQ_herp_HM_temp)
    EEC_ARQ_herp_IM_temp=table_all_out[2]['EEC_ARQ_herp_IM']
    EEC_ARQ_herp_IM_out.append(EEC_ARQ_herp_IM_temp)
    EEC_ARQ_herp_TP_temp=table_all_out[2]['EEC_ARQ_herp_TP']
    EEC_ARQ_herp_TP_out.append(EEC_ARQ_herp_TP_temp)


    LD50_AD_sm_temp=table_all_out[1]['LD50_AD_sm']
    LD50_AD_sm_out.append(LD50_AD_sm_temp)
    LD50_AD_md_temp=table_all_out[1]['LD50_AD_md']
    LD50_AD_md_out.append(LD50_AD_md_temp)
    LD50_AD_lg_temp=table_all_out[1]['LD50_AD_lg']
    LD50_AD_lg_out.append(LD50_AD_lg_temp)
    EEC_dose_BP_sm_temp=table_all_out[1]['EEC_dose_BP_sm']
    EEC_dose_BP_sm_out.append(EEC_dose_BP_sm_temp)
    EEC_dose_BP_md_temp=table_all_out[1]['EEC_dose_BP_md']
    EEC_dose_BP_md_out.append(EEC_dose_BP_md_temp)
    EEC_dose_BP_lg_temp=table_all_out[1]['EEC_dose_BP_lg']
    EEC_dose_BP_lg_out.append(EEC_dose_BP_lg_temp)
    ARQ_dose_BP_sm_temp=table_all_out[1]['ARQ_dose_BP_sm']
    ARQ_dose_BP_sm_out.append(ARQ_dose_BP_sm_temp)
    ARQ_dose_BP_md_temp=table_all_out[1]['ARQ_dose_BP_md']
    ARQ_dose_BP_md_out.append(ARQ_dose_BP_md_temp)
    ARQ_dose_BP_lg_temp=table_all_out[1]['ARQ_dose_BP_lg']
    ARQ_dose_BP_lg_out.append(ARQ_dose_BP_lg_temp)
    EEC_dose_FR_sm_temp=table_all_out[1]['EEC_dose_FR_sm']
    EEC_dose_FR_sm_out.append(EEC_dose_FR_sm_temp)
    EEC_dose_FR_md_temp=table_all_out[1]['EEC_dose_FR_md']
    EEC_dose_FR_md_out.append(EEC_dose_FR_md_temp)
    EEC_dose_FR_lg_temp=table_all_out[1]['EEC_dose_FR_lg']
    EEC_dose_FR_lg_out.append(EEC_dose_FR_lg_temp)
    ARQ_dose_FR_sm_temp=table_all_out[1]['ARQ_dose_FR_sm']
    ARQ_dose_FR_sm_out.append(ARQ_dose_FR_sm_temp)
    ARQ_dose_FR_md_temp=table_all_out[1]['ARQ_dose_FR_md']
    ARQ_dose_FR_md_out.append(ARQ_dose_FR_md_temp)
    ARQ_dose_FR_lg_temp=table_all_out[1]['ARQ_dose_FR_lg']
    ARQ_dose_FR_lg_out.append(ARQ_dose_FR_lg_temp)
    EEC_dose_HM_md_temp=table_all_out[1]['EEC_dose_HM_md']
    EEC_dose_HM_md_out.append(EEC_dose_HM_md_temp)
    EEC_dose_HM_lg_temp=table_all_out[1]['EEC_dose_HM_lg']
    EEC_dose_HM_lg_out.append(EEC_dose_HM_lg_temp)
    ARQ_dose_HM_md_temp=table_all_out[1]['ARQ_dose_HM_md']
    ARQ_dose_HM_md_out.append(ARQ_dose_HM_md_temp)
    ARQ_dose_HM_lg_temp=table_all_out[1]['ARQ_dose_HM_lg']
    ARQ_dose_HM_lg_out.append(ARQ_dose_HM_lg_temp)
    EEC_dose_IM_md_temp=table_all_out[1]['EEC_dose_IM_md']
    EEC_dose_IM_md_out.append(EEC_dose_IM_md_temp)
    EEC_dose_IM_lg_temp=table_all_out[1]['EEC_dose_IM_lg']
    EEC_dose_IM_lg_out.append(EEC_dose_IM_lg_temp)
    ARQ_dose_IM_md_temp=table_all_out[1]['ARQ_dose_IM_md']
    ARQ_dose_IM_md_out.append(ARQ_dose_IM_md_temp)
    ARQ_dose_IM_lg_temp=table_all_out[1]['ARQ_dose_IM_lg']
    ARQ_dose_IM_lg_out.append(ARQ_dose_IM_lg_temp)
    EEC_dose_TP_md_temp=table_all_out[1]['EEC_dose_TP_md']
    EEC_dose_TP_md_out.append(EEC_dose_TP_md_temp)
    EEC_dose_TP_lg_temp=table_all_out[1]['EEC_dose_TP_lg']
    EEC_dose_TP_lg_out.append(EEC_dose_TP_lg_temp)
    ARQ_dose_TP_md_temp=table_all_out[1]['ARQ_dose_TP_md']
    ARQ_dose_TP_md_out.append(ARQ_dose_TP_md_temp)
    ARQ_dose_TP_lg_temp=table_all_out[1]['ARQ_dose_TP_lg']
    ARQ_dose_TP_lg_out.append(ARQ_dose_TP_lg_temp)

##################################################################
############average case##########################################
##################################################################
    EEC_diet_herp_BL_temp_mean=table_all_out[6]['EEC_diet_herp_BL']
    EEC_diet_herp_BL_out_mean.append(EEC_diet_herp_BL_temp_mean)
    EEC_CRQ_herp_BL_temp_mean=table_all_out[6]['EEC_CRQ_herp_BL']
    EEC_CRQ_herp_BL_out_mean.append(EEC_CRQ_herp_BL_temp_mean)
    EEC_diet_herp_FR_temp_mean=table_all_out[6]['EEC_diet_herp_FR']
    EEC_diet_herp_FR_out_mean.append(EEC_diet_herp_FR_temp_mean)
    EEC_CRQ_herp_FR_temp_mean=table_all_out[6]['EEC_CRQ_herp_FR']
    EEC_CRQ_herp_FR_out_mean.append(EEC_CRQ_herp_FR_temp_mean)
    EEC_CRQ_herp_HM_temp_mean=table_all_out[6]['EEC_CRQ_herp_HM']
    EEC_CRQ_herp_HM_out_mean.append(EEC_CRQ_herp_HM_temp_mean)
    EEC_diet_herp_IM_temp_mean=table_all_out[6]['EEC_diet_herp_IM']
    EEC_diet_herp_IM_out_mean.append(EEC_diet_herp_IM_temp_mean)
    EEC_CRQ_herp_IM_temp_mean=table_all_out[6]['EEC_CRQ_herp_IM']
    EEC_CRQ_herp_IM_out_mean.append(EEC_CRQ_herp_IM_temp_mean)
    EEC_diet_herp_TP_temp_mean=table_all_out[6]['EEC_diet_herp_TP']
    EEC_diet_herp_TP_out_mean.append(EEC_diet_herp_TP_temp_mean)
    EEC_CRQ_herp_TP_temp_mean=table_all_out[6]['EEC_CRQ_herp_TP']
    EEC_CRQ_herp_TP_out_mean.append(EEC_CRQ_herp_TP_temp_mean)

    EEC_ARQ_herp_BL_temp_mean=table_all_out[5]['EEC_ARQ_herp_BL']
    EEC_ARQ_herp_BL_out_mean.append(EEC_ARQ_herp_BL_temp_mean)
    EEC_ARQ_herp_FR_temp_mean=table_all_out[5]['EEC_ARQ_herp_FR']
    EEC_ARQ_herp_FR_out_mean.append(EEC_ARQ_herp_FR_temp_mean)
    EEC_diet_herp_HM_temp_mean=table_all_out[5]['EEC_diet_herp_HM']
    EEC_diet_herp_HM_out_mean.append(EEC_diet_herp_HM_temp_mean)
    EEC_ARQ_herp_HM_temp_mean=table_all_out[5]['EEC_ARQ_herp_HM']
    EEC_ARQ_herp_HM_out_mean.append(EEC_ARQ_herp_HM_temp_mean)
    EEC_ARQ_herp_IM_temp_mean=table_all_out[5]['EEC_ARQ_herp_IM']
    EEC_ARQ_herp_IM_out_mean.append(EEC_ARQ_herp_IM_temp_mean)
    EEC_ARQ_herp_TP_temp_mean=table_all_out[5]['EEC_ARQ_herp_TP']
    EEC_ARQ_herp_TP_out_mean.append(EEC_ARQ_herp_TP_temp_mean)


    LD50_AD_sm_temp_mean=table_all_out[4]['LD50_AD_sm']
    LD50_AD_sm_out_mean.append(LD50_AD_sm_temp_mean)
    LD50_AD_md_temp_mean=table_all_out[4]['LD50_AD_md']
    LD50_AD_md_out_mean.append(LD50_AD_md_temp_mean)
    LD50_AD_lg_temp_mean=table_all_out[4]['LD50_AD_lg']
    LD50_AD_lg_out_mean.append(LD50_AD_lg_temp_mean)
    EEC_dose_BP_sm_temp_mean=table_all_out[4]['EEC_dose_BP_sm']
    EEC_dose_BP_sm_out_mean.append(EEC_dose_BP_sm_temp_mean)
    EEC_dose_BP_md_temp_mean=table_all_out[4]['EEC_dose_BP_md']
    EEC_dose_BP_md_out_mean.append(EEC_dose_BP_md_temp_mean)
    EEC_dose_BP_lg_temp_mean=table_all_out[4]['EEC_dose_BP_lg']
    EEC_dose_BP_lg_out_mean.append(EEC_dose_BP_lg_temp_mean)
    ARQ_dose_BP_sm_temp_mean=table_all_out[4]['ARQ_dose_BP_sm']
    ARQ_dose_BP_sm_out_mean.append(ARQ_dose_BP_sm_temp_mean)
    ARQ_dose_BP_md_temp_mean=table_all_out[4]['ARQ_dose_BP_md']
    ARQ_dose_BP_md_out_mean.append(ARQ_dose_BP_md_temp_mean)
    ARQ_dose_BP_lg_temp_mean=table_all_out[4]['ARQ_dose_BP_lg']
    ARQ_dose_BP_lg_out_mean.append(ARQ_dose_BP_lg_temp_mean)
    EEC_dose_FR_sm_temp_mean=table_all_out[4]['EEC_dose_FR_sm']
    EEC_dose_FR_sm_out_mean.append(EEC_dose_FR_sm_temp_mean)
    EEC_dose_FR_md_temp_mean=table_all_out[4]['EEC_dose_FR_md']
    EEC_dose_FR_md_out_mean.append(EEC_dose_FR_md_temp_mean)
    EEC_dose_FR_lg_temp_mean=table_all_out[4]['EEC_dose_FR_lg']
    EEC_dose_FR_lg_out_mean.append(EEC_dose_FR_lg_temp_mean)
    ARQ_dose_FR_sm_temp_mean=table_all_out[4]['ARQ_dose_FR_sm']
    ARQ_dose_FR_sm_out_mean.append(ARQ_dose_FR_sm_temp_mean)
    ARQ_dose_FR_md_temp_mean=table_all_out[4]['ARQ_dose_FR_md']
    ARQ_dose_FR_md_out_mean.append(ARQ_dose_FR_md_temp_mean)
    ARQ_dose_FR_lg_temp_mean=table_all_out[4]['ARQ_dose_FR_lg']
    ARQ_dose_FR_lg_out_mean.append(ARQ_dose_FR_lg_temp_mean)
    EEC_dose_HM_md_temp_mean=table_all_out[4]['EEC_dose_HM_md']
    EEC_dose_HM_md_out_mean.append(EEC_dose_HM_md_temp_mean)
    EEC_dose_HM_lg_temp_mean=table_all_out[4]['EEC_dose_HM_lg']
    EEC_dose_HM_lg_out_mean.append(EEC_dose_HM_lg_temp_mean)
    ARQ_dose_HM_md_temp_mean=table_all_out[4]['ARQ_dose_HM_md']
    ARQ_dose_HM_md_out_mean.append(ARQ_dose_HM_md_temp_mean)
    ARQ_dose_HM_lg_temp_mean=table_all_out[4]['ARQ_dose_HM_lg']
    ARQ_dose_HM_lg_out_mean.append(ARQ_dose_HM_lg_temp_mean)
    EEC_dose_IM_md_temp_mean=table_all_out[4]['EEC_dose_IM_md']
    EEC_dose_IM_md_out_mean.append(EEC_dose_IM_md_temp_mean)
    EEC_dose_IM_lg_temp_mean=table_all_out[4]['EEC_dose_IM_lg']
    EEC_dose_IM_lg_out_mean.append(EEC_dose_IM_lg_temp_mean)
    ARQ_dose_IM_md_temp_mean=table_all_out[4]['ARQ_dose_IM_md']
    ARQ_dose_IM_md_out_mean.append(ARQ_dose_IM_md_temp_mean)
    ARQ_dose_IM_lg_temp_mean=table_all_out[4]['ARQ_dose_IM_lg']
    ARQ_dose_IM_lg_out_mean.append(ARQ_dose_IM_lg_temp_mean)
    EEC_dose_TP_md_temp_mean=table_all_out[4]['EEC_dose_TP_md']
    EEC_dose_TP_md_out_mean.append(EEC_dose_TP_md_temp_mean)
    EEC_dose_TP_lg_temp_mean=table_all_out[4]['EEC_dose_TP_lg']
    EEC_dose_TP_lg_out_mean.append(EEC_dose_TP_lg_temp_mean)
    ARQ_dose_TP_md_temp_mean=table_all_out[4]['ARQ_dose_TP_md']
    ARQ_dose_TP_md_out_mean.append(ARQ_dose_TP_md_temp_mean)
    ARQ_dose_TP_lg_temp_mean=table_all_out[4]['ARQ_dose_TP_lg']
    ARQ_dose_TP_lg_out_mean.append(ARQ_dose_TP_lg_temp_mean)
    jid_all.append(therps_obj_temp.jid)
                therps_obj_all.append(therps_obj_temp)    
                if iter == 1:
                    jid_batch.append(therps_obj_temp.jid)
    return html_table_temp  

######Output###########

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


    sum_1=therps_tables.table_sum_1(i, a_i_disp, h_l, n_a, i_a, a_r)
    sum_2=therps_tables.table_sum_2(ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, bw_avian_ld50, bw_avian_lc50, bw_avian_NOAEC, bw_avian_NOAEL, x)
    sum_3=therps_tables.table_sum_3(bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, wp_herp_a_lg, c_mamm_a, c_herp_a)
    sum_4="""
    <br>
        <H3 class="out_1 collapsible" id="section3"><span></span>T-herps Batch outputs:</H3>
        <div class="out_">
    """
    sum_5=therps_tables.table_sum_5("Upper Bound Kenaga", EEC_diet_herp_BL_out, EEC_ARQ_herp_BL_out, EEC_diet_herp_FR_out, EEC_ARQ_herp_FR_out, EEC_diet_herp_HM_out, EEC_ARQ_herp_HM_out, EEC_diet_herp_IM_out, EEC_ARQ_herp_IM_out, EEC_diet_herp_TP_out, EEC_ARQ_herp_TP_out)
    sum_6=therps_tables.table_sum_6("Upper Bound Kenaga", EEC_diet_herp_BL_out, EEC_CRQ_herp_BL_out, EEC_diet_herp_FR_out, EEC_CRQ_herp_FR_out, EEC_diet_herp_HM_out, EEC_CRQ_herp_HM_out, EEC_diet_herp_IM_out, EEC_CRQ_herp_IM_out, EEC_diet_herp_TP_out, EEC_CRQ_herp_TP_out)
    sum_7=therps_tables.table_sum_7("Upper Bound Kenaga", bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, LD50_AD_sm_out, LD50_AD_md_out, LD50_AD_lg_out,
                  EEC_dose_BP_sm_out, EEC_dose_BP_md_out, EEC_dose_BP_lg_out, ARQ_dose_BP_sm_out, ARQ_dose_BP_md_out, ARQ_dose_BP_lg_out,
                  EEC_dose_FR_sm_out, EEC_dose_FR_md_out, EEC_dose_FR_lg_out, ARQ_dose_FR_sm_out, ARQ_dose_FR_md_out, ARQ_dose_FR_lg_out,
                  EEC_dose_HM_md_out, EEC_dose_HM_lg_out, ARQ_dose_HM_md_out, ARQ_dose_HM_lg_out,
                  EEC_dose_IM_md_out, EEC_dose_IM_lg_out, ARQ_dose_IM_md_out, ARQ_dose_IM_lg_out,
                  EEC_dose_TP_md_out, EEC_dose_TP_lg_out, ARQ_dose_TP_md_out, ARQ_dose_TP_lg_out)

    sum_8=therps_tables.table_sum_5("Mean Kenaga", EEC_diet_herp_BL_out_mean, EEC_ARQ_herp_BL_out_mean, EEC_diet_herp_FR_out_mean, EEC_ARQ_herp_FR_out_mean, EEC_diet_herp_HM_out_mean, EEC_ARQ_herp_HM_out_mean, EEC_diet_herp_IM_out_mean, EEC_ARQ_herp_IM_out_mean, EEC_diet_herp_TP_out_mean, EEC_ARQ_herp_TP_out_mean)
    sum_9=therps_tables.table_sum_6("Mean Kenaga", EEC_diet_herp_BL_out_mean, EEC_CRQ_herp_BL_out_mean, EEC_diet_herp_FR_out_mean, EEC_CRQ_herp_FR_out_mean, EEC_diet_herp_HM_out_mean, EEC_CRQ_herp_HM_out_mean, EEC_diet_herp_IM_out_mean, EEC_CRQ_herp_IM_out_mean, EEC_diet_herp_TP_out_mean, EEC_CRQ_herp_TP_out_mean)
    sum_10=therps_tables.table_sum_7("Mean Kenaga", bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, LD50_AD_sm_out_mean, LD50_AD_md_out_mean, LD50_AD_lg_out_mean,
                  EEC_dose_BP_sm_out_mean, EEC_dose_BP_md_out_mean, EEC_dose_BP_lg_out_mean, ARQ_dose_BP_sm_out_mean, ARQ_dose_BP_md_out_mean, ARQ_dose_BP_lg_out_mean,
                  EEC_dose_FR_sm_out_mean, EEC_dose_FR_md_out_mean, EEC_dose_FR_lg_out_mean, ARQ_dose_FR_sm_out_mean, ARQ_dose_FR_md_out_mean, ARQ_dose_FR_lg_out_mean,
                  EEC_dose_HM_md_out_mean, EEC_dose_HM_lg_out_mean, ARQ_dose_HM_md_out_mean, ARQ_dose_HM_lg_out_mean,
                  EEC_dose_IM_md_out_mean, EEC_dose_IM_lg_out_mean, ARQ_dose_IM_md_out_mean, ARQ_dose_IM_lg_out_mean,
                  EEC_dose_TP_md_out_mean, EEC_dose_TP_lg_out_mean, ARQ_dose_TP_md_out_mean, ARQ_dose_TP_lg_out_mean)
    html_end = """
        </div>
    """
    return sum_1+sum_2+sum_3+sum_4+sum_7+sum_5+sum_6+ sum_10+sum_8+sum_9+iter_html+html_end
    # return sum_1+sum_2+sum_3+iter_html


class TherpsBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['file-0']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        # html = uber_lib.SkinChk(ChkCookie)
        # html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'therps','page':'batchinput'})
        # html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = template.render(templatepath + '04uberbatch_start.html', {
                'model':'therps',
                'model_attributes':'T-Herps Batch Output'})
        html = html + therps_tables.timestamp("",jid_batch[0])
        html = html + iter_html
        #html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        # html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.batch_save_dic(html, [x.__dict__ for x in therps_obj_all], 'therps', 'batch', jid_batch[0], ChkCookie, templatepath)
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TherpsBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

