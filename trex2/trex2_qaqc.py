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
import csv
import sys
sys.path.append("../trex2")
from trex2 import trex2_model, trex2_tables
from uber import uber_lib
import logging
logger = logging.getLogger('Trex2QaqcPage')
import rest_funcs

cwd= os.getcwd()
data = csv.reader(open(cwd+'/trex2/trex2_qaqc.csv'))

chem_name = []
use = []
formu_name = []
a_i = []
Application_type = []
seed_treatment_name = []
p_i = []
den = []
m_s_r_p = []
r_s = []
b_w = []
h_l = []
n_a = []
crop_use = []
rate_out = []
day_out = []
ld50_bird = []
lc50_bird = []
NOAEC_bird = []
NOAEL_bird = []
aw_bird_sm = []
aw_bird_md = []
aw_bird_lg = []
Species_of_the_tested_bird_avian_ld50 = []
Species_of_the_tested_bird_avian_lc50 = []
Species_of_the_tested_bird_avian_NOAEC = []
Species_of_the_tested_bird_avian_NOAEL = []
tw_bird_ld50 = []
tw_bird_lc50 = []
tw_bird_NOAEC = []
tw_bird_NOAEL = []
x = []
ld50_mamm = []
lc50_mamm = []
NOAEC_mamm = []
NOAEL_mamm = []
aw_mamm_sm = []
aw_mamm_md = []
aw_mamm_lg = []
tw_mamm = []


######Pre-defined outputs########
EEC_diet_SG_BL_out_exp=[]
EEC_diet_TG_BL_out_exp=[]
EEC_diet_BP_BL_out_exp=[]
EEC_diet_FR_BL_out_exp=[]
EEC_diet_AR_BL_out_exp=[]

EEC_dose_bird_SG_BL_sm_out_exp=[]
EEC_dose_bird_SG_BL_md_out_exp=[]
EEC_dose_bird_SG_BL_lg_out_exp=[]
EEC_dose_bird_TG_BL_sm_out_exp=[]
EEC_dose_bird_TG_BL_md_out_exp=[]
EEC_dose_bird_TG_BL_lg_out_exp=[]
EEC_dose_bird_BP_BL_sm_out_exp=[]
EEC_dose_bird_BP_BL_md_out_exp=[]
EEC_dose_bird_BP_BL_lg_out_exp=[]
EEC_dose_bird_FP_BL_sm_out_exp=[]
EEC_dose_bird_FP_BL_md_out_exp=[]
EEC_dose_bird_FP_BL_lg_out_exp=[]
EEC_dose_bird_AR_BL_sm_out_exp=[]
EEC_dose_bird_AR_BL_md_out_exp=[]
EEC_dose_bird_AR_BL_lg_out_exp=[]
EEC_dose_bird_SE_BL_sm_out_exp=[]
EEC_dose_bird_SE_BL_md_out_exp=[]
EEC_dose_bird_SE_BL_lg_out_exp=[]

ARQ_bird_SG_BL_sm_out_exp=[]
ARQ_bird_SG_BL_md_out_exp=[]
ARQ_bird_SG_BL_lg_out_exp=[]
ARQ_bird_TG_BL_sm_out_exp=[]
ARQ_bird_TG_BL_md_out_exp=[]
ARQ_bird_TG_BL_lg_out_exp=[]
ARQ_bird_BP_BL_sm_out_exp=[]
ARQ_bird_BP_BL_md_out_exp=[]
ARQ_bird_BP_BL_lg_out_exp=[]
ARQ_bird_FP_BL_sm_out_exp=[]
ARQ_bird_FP_BL_md_out_exp=[]
ARQ_bird_FP_BL_lg_out_exp=[]
ARQ_bird_AR_BL_sm_out_exp=[]
ARQ_bird_AR_BL_md_out_exp=[]
ARQ_bird_AR_BL_lg_out_exp=[]
ARQ_bird_SE_BL_sm_out_exp=[]
ARQ_bird_SE_BL_md_out_exp=[]
ARQ_bird_SE_BL_lg_out_exp=[]

ARQ_diet_bird_SG_A_BL_out_exp=[]
ARQ_diet_bird_SG_C_BL_out_exp=[]
ARQ_diet_bird_TG_A_BL_out_exp=[]
ARQ_diet_bird_TG_C_BL_out_exp=[]
ARQ_diet_bird_BP_A_BL_out_exp=[]
ARQ_diet_bird_BP_C_BL_out_exp=[]
ARQ_diet_bird_FP_A_BL_out_exp=[]
ARQ_diet_bird_FP_C_BL_out_exp=[]
ARQ_diet_bird_AR_A_BL_out_exp=[]
ARQ_diet_bird_AR_C_BL_out_exp=[]

EEC_dose_mamm_SG_sm_BL_out_exp=[]
EEC_dose_mamm_SG_md_BL_out_exp=[]
EEC_dose_mamm_SG_lg_BL_out_exp=[]
EEC_dose_mamm_TG_sm_BL_out_exp=[]
EEC_dose_mamm_TG_md_BL_out_exp=[]
EEC_dose_mamm_TG_lg_BL_out_exp=[]
EEC_dose_mamm_BP_sm_BL_out_exp=[]
EEC_dose_mamm_BP_md_BL_out_exp=[]
EEC_dose_mamm_BP_lg_BL_out_exp=[]
EEC_dose_mamm_FP_sm_BL_out_exp=[]
EEC_dose_mamm_FP_md_BL_out_exp=[]
EEC_dose_mamm_FP_lg_BL_out_exp=[]
EEC_dose_mamm_AR_sm_BL_out_exp=[]
EEC_dose_mamm_AR_md_BL_out_exp=[]
EEC_dose_mamm_AR_lg_BL_out_exp=[]
EEC_dose_mamm_SE_sm_BL_out_exp=[]
EEC_dose_mamm_SE_md_BL_out_exp=[]
EEC_dose_mamm_SE_lg_BL_out_exp=[]

ARQ_dose_mamm_SG_sm_BL_out_exp=[]
CRQ_dose_mamm_SG_sm_BL_out_exp=[]
ARQ_dose_mamm_SG_md_BL_out_exp=[]
CRQ_dose_mamm_SG_md_BL_out_exp=[]
ARQ_dose_mamm_SG_lg_BL_out_exp=[]
CRQ_dose_mamm_SG_lg_BL_out_exp=[]
ARQ_dose_mamm_TG_sm_BL_out_exp=[]
CRQ_dose_mamm_TG_sm_BL_out_exp=[]
ARQ_dose_mamm_TG_md_BL_out_exp=[]
CRQ_dose_mamm_TG_md_BL_out_exp=[]
ARQ_dose_mamm_TG_lg_BL_out_exp=[]
CRQ_dose_mamm_TG_lg_BL_out_exp=[]
ARQ_dose_mamm_BP_sm_BL_out_exp=[]
CRQ_dose_mamm_BP_sm_BL_out_exp=[]
ARQ_dose_mamm_BP_md_BL_out_exp=[]
CRQ_dose_mamm_BP_md_BL_out_exp=[]
ARQ_dose_mamm_BP_lg_BL_out_exp=[]
CRQ_dose_mamm_BP_lg_BL_out_exp=[]
ARQ_dose_mamm_FP_sm_BL_out_exp=[]
CRQ_dose_mamm_FP_sm_BL_out_exp=[]
ARQ_dose_mamm_FP_md_BL_out_exp=[]
CRQ_dose_mamm_FP_md_BL_out_exp=[]
ARQ_dose_mamm_FP_lg_BL_out_exp=[]
CRQ_dose_mamm_FP_lg_BL_out_exp=[]
ARQ_dose_mamm_AR_sm_BL_out_exp=[]
CRQ_dose_mamm_AR_sm_BL_out_exp=[]
ARQ_dose_mamm_AR_md_BL_out_exp=[]
CRQ_dose_mamm_AR_md_BL_out_exp=[]
ARQ_dose_mamm_AR_lg_BL_out_exp=[]
CRQ_dose_mamm_AR_lg_BL_out_exp=[]
ARQ_dose_mamm_SE_sm_BL_out_exp=[]
CRQ_dose_mamm_SE_sm_BL_out_exp=[]
ARQ_dose_mamm_SE_md_BL_out_exp=[]
CRQ_dose_mamm_SE_md_BL_out_exp=[]
ARQ_dose_mamm_SE_lg_BL_out_exp=[]
CRQ_dose_mamm_SE_lg_BL_out_exp=[]

ARQ_diet_mamm_SG_BL_out_exp=[]
CRQ_diet_mamm_SG_BL_out_exp=[]
ARQ_diet_mamm_TG_BL_out_exp=[]
CRQ_diet_mamm_TG_BL_out_exp=[]
ARQ_diet_mamm_BP_BL_out_exp=[]
CRQ_diet_mamm_BP_BL_out_exp=[]
ARQ_diet_mamm_FP_BL_out_exp=[]
CRQ_diet_mamm_FP_BL_out_exp=[]
ARQ_diet_mamm_AR_BL_out_exp=[]
CRQ_diet_mamm_AR_BL_out_exp=[]

LD50_bl_bird_sm_out_exp=[]
LD50_bl_mamm_sm_out_exp=[]
LD50_bl_bird_md_out_exp=[]
LD50_bl_mamm_md_out_exp=[]
LD50_bl_bird_lg_out_exp=[]
LD50_bl_mamm_lg_out_exp=[]

sa_bird_1_s_out_exp=[]
sa_bird_2_s_out_exp=[]
sc_bird_s_out_exp=[]
sa_mamm_1_s_out_exp=[]
sa_mamm_2_s_out_exp=[]
sc_mamm_s_out_exp=[]
sa_bird_1_m_out_exp=[]
sa_bird_2_m_out_exp=[]
sc_bird_m_out_exp=[]
sa_mamm_1_m_out_exp=[]
sa_mamm_2_m_out_exp=[]
sc_mamm_m_out_exp=[]
sa_bird_1_l_out_exp=[]
sa_bird_2_l_out_exp=[]
sc_bird_l_out_exp=[]
sa_mamm_1_l_out_exp=[]
sa_mamm_2_l_out_exp=[]
sc_mamm_l_out_exp=[]

html_qaqc=""
data.next()
for row_inp in data:
###Inputs###########
    chem_name_temp = str(row_inp[0])
    chem_name.append(chem_name_temp)
    use_temp = str(row_inp[1])
    use.append(use_temp)
    formu_name_temp = str(row_inp[2])
    formu_name.append(formu_name_temp)
    a_i_temp = float(row_inp[3])/100
    a_i.append(a_i_temp)
    Application_type_temp = str(row_inp[4])
    Application_type.append(Application_type_temp)
    seed_treatment_name_temp = str(row_inp[5])
    seed_treatment_name.append(seed_treatment_name_temp)
    m_s_r_p_temp = float(row_inp[6])
    m_s_r_p.append(m_s_r_p_temp)
    crop_use_temp = str(row_inp[7])
    crop_use.append(crop_use_temp)
    r_s_temp = float(row_inp[8])
    r_s.append(r_s_temp)
    b_w_temp = float(row_inp[9])
    b_w.append(b_w_temp)
    try:
        p_i_temp = float(row_inp[10])/100
    except:
        p_i_temp = 'N/A'
    p_i.append(p_i_temp)
    den_temp = float(row_inp[11])
    den.append(den_temp)
    h_l_temp = float(row_inp[12])
    h_l.append(h_l_temp)
    n_a_temp = float(row_inp[13])
    n_a.append(n_a_temp)
    rate_out_temp = row_inp[14]
    rate_out_temp=rate_out_temp.split(',')
    rate_out_temp=[float(i) for i in rate_out_temp]
    rate_out.append(rate_out_temp)
    day_out_temp = str(row_inp[15])
    day_out_temp=day_out_temp.split(',')
    day_out_temp=[float(i) for i in day_out_temp]
    day_out.append(day_out_temp)
    ld50_bird_temp = float(row_inp[16])
    ld50_bird.append(ld50_bird_temp)
    Species_of_the_tested_bird_avian_ld50_temp = str(row_inp[17])
    Species_of_the_tested_bird_avian_ld50.append(Species_of_the_tested_bird_avian_ld50_temp)
    tw_bird_ld50_temp = float(row_inp[18])
    tw_bird_ld50.append(tw_bird_ld50_temp)
    lc50_bird_temp = float(row_inp[19])
    lc50_bird.append(lc50_bird_temp)
    Species_of_the_tested_bird_avian_lc50_temp = str(row_inp[20])
    Species_of_the_tested_bird_avian_lc50.append(Species_of_the_tested_bird_avian_lc50_temp)
    tw_bird_lc50_temp = float(row_inp[21])
    tw_bird_lc50.append(tw_bird_lc50_temp)
    NOAEC_bird_temp = float(row_inp[22])
    NOAEC_bird.append(NOAEC_bird_temp)
    Species_of_the_tested_bird_avian_NOAEC_temp = str(row_inp[23])
    Species_of_the_tested_bird_avian_NOAEC.append(Species_of_the_tested_bird_avian_NOAEC_temp)
    tw_bird_NOAEC_temp = float(row_inp[24])
    tw_bird_NOAEC.append(tw_bird_NOAEC_temp)
    try:
        NOAEL_bird_temp = float(row_inp[25])
    except:
        NOAEL_bird_temp = 'N/A'
    NOAEL_bird.append(NOAEL_bird_temp)
    Species_of_the_tested_bird_avian_NOAEL_temp = str(row_inp[26])
    Species_of_the_tested_bird_avian_NOAEL.append(Species_of_the_tested_bird_avian_NOAEL_temp)
    tw_bird_NOAEL_temp = float(row_inp[27])
    tw_bird_NOAEL.append(tw_bird_NOAEL_temp)
    aw_bird_sm_temp = float(row_inp[28])
    aw_bird_sm.append(aw_bird_sm_temp)
    aw_bird_md_temp = float(row_inp[29])
    aw_bird_md.append(aw_bird_md_temp)
    aw_bird_lg_temp = float(row_inp[30])
    aw_bird_lg.append(aw_bird_lg_temp)
    x_temp = float(row_inp[31])
    x.append(x_temp)
    ld50_mamm_temp = float(row_inp[32])
    ld50_mamm.append(ld50_mamm_temp)
    try:
        lc50_mamm_temp = float(row_inp[33])
    except:
        lc50_mamm_temp = 'N/A'
    lc50_mamm.append(lc50_mamm_temp)
    NOAEC_mamm_temp = float(row_inp[34])
    NOAEC_mamm.append(NOAEC_mamm_temp)
    NOAEL_mamm_temp = float(row_inp[35])
    NOAEL_mamm.append(NOAEL_mamm_temp)
    aw_mamm_sm_temp = float(row_inp[36])
    aw_mamm_sm.append(aw_mamm_sm_temp)
    aw_mamm_md_temp = float(row_inp[37])
    aw_mamm_md.append(aw_mamm_md_temp)
    aw_mamm_lg_temp = float(row_inp[38])
    aw_mamm_lg.append(aw_mamm_lg_temp)
    tw_mamm_temp = float(row_inp[39])
    tw_mamm.append(tw_mamm_temp)

    trex2_obj = trex2_model.trex2("qaqc", chem_name_temp, use_temp, formu_name_temp, a_i_temp, Application_type_temp, seed_treatment_name_temp, m_s_r_p_temp, crop_use_temp, r_s_temp, b_w_temp, p_i_temp, den_temp, h_l_temp, n_a_temp, rate_out_temp, day_out_temp,
                    ld50_bird_temp, lc50_bird_temp, NOAEC_bird_temp, NOAEL_bird_temp, aw_bird_sm_temp, aw_bird_md_temp, aw_bird_lg_temp, 
                    Species_of_the_tested_bird_avian_ld50_temp, Species_of_the_tested_bird_avian_lc50_temp, Species_of_the_tested_bird_avian_NOAEC_temp, Species_of_the_tested_bird_avian_NOAEL_temp,
                    tw_bird_ld50_temp, tw_bird_lc50_temp, tw_bird_NOAEC_temp, tw_bird_NOAEL_temp,
                    x_temp, ld50_mamm_temp, lc50_mamm_temp, NOAEC_mamm_temp, NOAEL_mamm_temp, aw_mamm_sm_temp, aw_mamm_md_temp, aw_mamm_lg_temp, tw_mamm_temp,
                    m_s_r_p_temp)

    if Application_type_temp != 'Seed Treatment':
        EEC_diet_SG_BL_out_exp.append(float(row_inp[40]))
        EEC_diet_TG_BL_out_exp.append(float(row_inp[41]))
        EEC_diet_BP_BL_out_exp.append(float(row_inp[42]))
        EEC_diet_FR_BL_out_exp.append(float(row_inp[43]))
        EEC_diet_AR_BL_out_exp.append(float(row_inp[44]))

        EEC_dose_bird_SG_BL_sm_out_exp.append(float(row_inp[45]))
        EEC_dose_bird_SG_BL_md_out_exp.append(float(row_inp[46]))
        EEC_dose_bird_SG_BL_lg_out_exp.append(float(row_inp[47]))
        EEC_dose_bird_TG_BL_sm_out_exp.append(float(row_inp[48]))
        EEC_dose_bird_TG_BL_md_out_exp.append(float(row_inp[49]))
        EEC_dose_bird_TG_BL_lg_out_exp.append(float(row_inp[50]))
        EEC_dose_bird_BP_BL_sm_out_exp.append(float(row_inp[51]))
        EEC_dose_bird_BP_BL_md_out_exp.append(float(row_inp[52]))
        EEC_dose_bird_BP_BL_lg_out_exp.append(float(row_inp[53]))
        EEC_dose_bird_FP_BL_sm_out_exp.append(float(row_inp[54]))
        EEC_dose_bird_FP_BL_md_out_exp.append(float(row_inp[55]))
        EEC_dose_bird_FP_BL_lg_out_exp.append(float(row_inp[56]))
        EEC_dose_bird_AR_BL_sm_out_exp.append(float(row_inp[57]))
        EEC_dose_bird_AR_BL_md_out_exp.append(float(row_inp[58]))
        EEC_dose_bird_AR_BL_lg_out_exp.append(float(row_inp[59]))
        EEC_dose_bird_SE_BL_sm_out_exp.append(float(row_inp[60]))
        EEC_dose_bird_SE_BL_md_out_exp.append(float(row_inp[61]))
        EEC_dose_bird_SE_BL_lg_out_exp.append(float(row_inp[62]))

        ARQ_bird_SG_BL_sm_out_exp.append(float(row_inp[63]))
        ARQ_bird_SG_BL_md_out_exp.append(float(row_inp[64]))
        ARQ_bird_SG_BL_lg_out_exp.append(float(row_inp[65]))
        ARQ_bird_TG_BL_sm_out_exp.append(float(row_inp[66]))
        ARQ_bird_TG_BL_md_out_exp.append(float(row_inp[67]))
        ARQ_bird_TG_BL_lg_out_exp.append(float(row_inp[68]))
        ARQ_bird_BP_BL_sm_out_exp.append(float(row_inp[69]))
        ARQ_bird_BP_BL_md_out_exp.append(float(row_inp[70]))
        ARQ_bird_BP_BL_lg_out_exp.append(float(row_inp[71]))
        ARQ_bird_FP_BL_sm_out_exp.append(float(row_inp[72]))
        ARQ_bird_FP_BL_md_out_exp.append(float(row_inp[73]))
        ARQ_bird_FP_BL_lg_out_exp.append(float(row_inp[74]))
        ARQ_bird_AR_BL_sm_out_exp.append(float(row_inp[75]))
        ARQ_bird_AR_BL_md_out_exp.append(float(row_inp[76]))
        ARQ_bird_AR_BL_lg_out_exp.append(float(row_inp[77]))
        ARQ_bird_SE_BL_sm_out_exp.append(float(row_inp[78]))
        ARQ_bird_SE_BL_md_out_exp.append(float(row_inp[79]))
        ARQ_bird_SE_BL_lg_out_exp.append(float(row_inp[80]))

        ARQ_diet_bird_SG_A_BL_out_exp.append(float(row_inp[81]))
        ARQ_diet_bird_SG_C_BL_out_exp.append(float(row_inp[82]))
        ARQ_diet_bird_TG_A_BL_out_exp.append(float(row_inp[83]))
        ARQ_diet_bird_TG_C_BL_out_exp.append(float(row_inp[84]))
        ARQ_diet_bird_BP_A_BL_out_exp.append(float(row_inp[85]))
        ARQ_diet_bird_BP_C_BL_out_exp.append(float(row_inp[86]))
        ARQ_diet_bird_FP_A_BL_out_exp.append(float(row_inp[87]))
        ARQ_diet_bird_FP_C_BL_out_exp.append(float(row_inp[88]))
        ARQ_diet_bird_AR_A_BL_out_exp.append(float(row_inp[89]))
        ARQ_diet_bird_AR_C_BL_out_exp.append(float(row_inp[90]))

        EEC_dose_mamm_SG_sm_BL_out_exp.append(float(row_inp[91]))
        EEC_dose_mamm_SG_md_BL_out_exp.append(float(row_inp[92]))
        EEC_dose_mamm_SG_lg_BL_out_exp.append(float(row_inp[93]))
        EEC_dose_mamm_TG_sm_BL_out_exp.append(float(row_inp[94]))
        EEC_dose_mamm_TG_md_BL_out_exp.append(float(row_inp[95]))
        EEC_dose_mamm_TG_lg_BL_out_exp.append(float(row_inp[96]))
        EEC_dose_mamm_BP_sm_BL_out_exp.append(float(row_inp[97]))
        EEC_dose_mamm_BP_md_BL_out_exp.append(float(row_inp[98]))
        EEC_dose_mamm_BP_lg_BL_out_exp.append(float(row_inp[99]))
        EEC_dose_mamm_FP_sm_BL_out_exp.append(float(row_inp[100]))
        EEC_dose_mamm_FP_md_BL_out_exp.append(float(row_inp[101]))
        EEC_dose_mamm_FP_lg_BL_out_exp.append(float(row_inp[102]))
        EEC_dose_mamm_AR_sm_BL_out_exp.append(float(row_inp[103]))
        EEC_dose_mamm_AR_md_BL_out_exp.append(float(row_inp[104]))
        EEC_dose_mamm_AR_lg_BL_out_exp.append(float(row_inp[105]))
        EEC_dose_mamm_SE_sm_BL_out_exp.append(float(row_inp[106]))
        EEC_dose_mamm_SE_md_BL_out_exp.append(float(row_inp[107]))
        EEC_dose_mamm_SE_lg_BL_out_exp.append(float(row_inp[108]))

        ARQ_dose_mamm_SG_sm_BL_out_exp.append(float(row_inp[109]))
        CRQ_dose_mamm_SG_sm_BL_out_exp.append(float(row_inp[110]))
        ARQ_dose_mamm_SG_md_BL_out_exp.append(float(row_inp[111]))
        CRQ_dose_mamm_SG_md_BL_out_exp.append(float(row_inp[112]))
        ARQ_dose_mamm_SG_lg_BL_out_exp.append(float(row_inp[113]))
        CRQ_dose_mamm_SG_lg_BL_out_exp.append(float(row_inp[114]))
        ARQ_dose_mamm_TG_sm_BL_out_exp.append(float(row_inp[115]))
        CRQ_dose_mamm_TG_sm_BL_out_exp.append(float(row_inp[116]))
        ARQ_dose_mamm_TG_md_BL_out_exp.append(float(row_inp[117]))
        CRQ_dose_mamm_TG_md_BL_out_exp.append(float(row_inp[118]))
        ARQ_dose_mamm_TG_lg_BL_out_exp.append(float(row_inp[119]))
        CRQ_dose_mamm_TG_lg_BL_out_exp.append(float(row_inp[120]))
        ARQ_dose_mamm_BP_sm_BL_out_exp.append(float(row_inp[121]))
        CRQ_dose_mamm_BP_sm_BL_out_exp.append(float(row_inp[122]))
        ARQ_dose_mamm_BP_md_BL_out_exp.append(float(row_inp[123]))
        CRQ_dose_mamm_BP_md_BL_out_exp.append(float(row_inp[124]))
        ARQ_dose_mamm_BP_lg_BL_out_exp.append(float(row_inp[125]))
        CRQ_dose_mamm_BP_lg_BL_out_exp.append(float(row_inp[126]))
        ARQ_dose_mamm_FP_sm_BL_out_exp.append(float(row_inp[127]))
        CRQ_dose_mamm_FP_sm_BL_out_exp.append(float(row_inp[128]))
        ARQ_dose_mamm_FP_md_BL_out_exp.append(float(row_inp[129]))
        CRQ_dose_mamm_FP_md_BL_out_exp.append(float(row_inp[130]))
        ARQ_dose_mamm_FP_lg_BL_out_exp.append(float(row_inp[131]))
        CRQ_dose_mamm_FP_lg_BL_out_exp.append(float(row_inp[132]))
        ARQ_dose_mamm_AR_sm_BL_out_exp.append(float(row_inp[133]))
        CRQ_dose_mamm_AR_sm_BL_out_exp.append(float(row_inp[134]))
        ARQ_dose_mamm_AR_md_BL_out_exp.append(float(row_inp[135]))
        CRQ_dose_mamm_AR_md_BL_out_exp.append(float(row_inp[136]))
        ARQ_dose_mamm_AR_lg_BL_out_exp.append(float(row_inp[137]))
        CRQ_dose_mamm_AR_lg_BL_out_exp.append(float(row_inp[138]))
        ARQ_dose_mamm_SE_sm_BL_out_exp.append(float(row_inp[139]))
        CRQ_dose_mamm_SE_sm_BL_out_exp.append(float(row_inp[140]))
        ARQ_dose_mamm_SE_md_BL_out_exp.append(float(row_inp[141]))
        CRQ_dose_mamm_SE_md_BL_out_exp.append(float(row_inp[142]))
        ARQ_dose_mamm_SE_lg_BL_out_exp.append(float(row_inp[143]))
        CRQ_dose_mamm_SE_lg_BL_out_exp.append(float(row_inp[144]))

        ARQ_diet_mamm_SG_BL_out_exp.append(str(row_inp[145]))
        CRQ_diet_mamm_SG_BL_out_exp.append(float(row_inp[146]))
        ARQ_diet_mamm_TG_BL_out_exp.append(str(row_inp[147]))
        CRQ_diet_mamm_TG_BL_out_exp.append(float(row_inp[148]))
        ARQ_diet_mamm_BP_BL_out_exp.append(str(row_inp[149]))
        CRQ_diet_mamm_BP_BL_out_exp.append(float(row_inp[150]))
        ARQ_diet_mamm_FP_BL_out_exp.append(str(row_inp[151]))
        CRQ_diet_mamm_FP_BL_out_exp.append(float(row_inp[152]))
        ARQ_diet_mamm_AR_BL_out_exp.append(str(row_inp[153]))
        CRQ_diet_mamm_AR_BL_out_exp.append(float(row_inp[154]))

        LD50_bl_bird_sm_out_exp.append(float(row_inp[155]))
        LD50_bl_mamm_sm_out_exp.append(float(row_inp[156]))
        LD50_bl_bird_md_out_exp.append(float(row_inp[157]))
        LD50_bl_mamm_md_out_exp.append(float(row_inp[158]))
        LD50_bl_bird_lg_out_exp.append(float(row_inp[159]))
        LD50_bl_mamm_lg_out_exp.append(float(row_inp[160]))

        trex2_obj.EEC_diet_SG_BL_out_exp=EEC_diet_SG_BL_out_exp[0]
        trex2_obj.EEC_diet_TG_BL_out_exp=EEC_diet_TG_BL_out_exp[0]
        trex2_obj.EEC_diet_BP_BL_out_exp=EEC_diet_BP_BL_out_exp[0]
        trex2_obj.EEC_diet_FR_BL_out_exp=EEC_diet_FR_BL_out_exp[0]
        trex2_obj.EEC_diet_AR_BL_out_exp=EEC_diet_AR_BL_out_exp[0]

        trex2_obj.EEC_dose_bird_SG_BL_sm_out_exp=EEC_dose_bird_SG_BL_sm_out_exp[0]
        trex2_obj.EEC_dose_bird_SG_BL_md_out_exp=EEC_dose_bird_SG_BL_md_out_exp[0]
        trex2_obj.EEC_dose_bird_SG_BL_lg_out_exp=EEC_dose_bird_SG_BL_lg_out_exp[0]
        trex2_obj.EEC_dose_bird_TG_BL_sm_out_exp=EEC_dose_bird_TG_BL_sm_out_exp[0]
        trex2_obj.EEC_dose_bird_TG_BL_md_out_exp=EEC_dose_bird_TG_BL_md_out_exp[0]
        trex2_obj.EEC_dose_bird_TG_BL_lg_out_exp=EEC_dose_bird_TG_BL_lg_out_exp[0]
        trex2_obj.EEC_dose_bird_BP_BL_sm_out_exp=EEC_dose_bird_BP_BL_sm_out_exp[0]
        trex2_obj.EEC_dose_bird_BP_BL_md_out_exp=EEC_dose_bird_BP_BL_md_out_exp[0]
        trex2_obj.EEC_dose_bird_BP_BL_lg_out_exp=EEC_dose_bird_BP_BL_lg_out_exp[0]
        trex2_obj.EEC_dose_bird_FP_BL_sm_out_exp=EEC_dose_bird_FP_BL_sm_out_exp[0]
        trex2_obj.EEC_dose_bird_FP_BL_md_out_exp=EEC_dose_bird_FP_BL_md_out_exp[0]
        trex2_obj.EEC_dose_bird_FP_BL_lg_out_exp=EEC_dose_bird_FP_BL_lg_out_exp[0]
        trex2_obj.EEC_dose_bird_AR_BL_sm_out_exp=EEC_dose_bird_AR_BL_sm_out_exp[0]
        trex2_obj.EEC_dose_bird_AR_BL_md_out_exp=EEC_dose_bird_AR_BL_md_out_exp[0]
        trex2_obj.EEC_dose_bird_AR_BL_lg_out_exp=EEC_dose_bird_AR_BL_lg_out_exp[0]
        trex2_obj.EEC_dose_bird_SE_BL_sm_out_exp=EEC_dose_bird_SE_BL_sm_out_exp[0]
        trex2_obj.EEC_dose_bird_SE_BL_md_out_exp=EEC_dose_bird_SE_BL_md_out_exp[0]
        trex2_obj.EEC_dose_bird_SE_BL_lg_out_exp=EEC_dose_bird_SE_BL_lg_out_exp[0]

        trex2_obj.ARQ_bird_SG_BL_sm_out_exp=ARQ_bird_SG_BL_sm_out_exp[0]
        trex2_obj.ARQ_bird_SG_BL_md_out_exp=ARQ_bird_SG_BL_md_out_exp[0]
        trex2_obj.ARQ_bird_SG_BL_lg_out_exp=ARQ_bird_SG_BL_lg_out_exp[0]
        trex2_obj.ARQ_bird_TG_BL_sm_out_exp=ARQ_bird_TG_BL_sm_out_exp[0]
        trex2_obj.ARQ_bird_TG_BL_md_out_exp=ARQ_bird_TG_BL_md_out_exp[0]
        trex2_obj.ARQ_bird_TG_BL_lg_out_exp=ARQ_bird_TG_BL_lg_out_exp[0]
        trex2_obj.ARQ_bird_BP_BL_sm_out_exp=ARQ_bird_BP_BL_sm_out_exp[0]
        trex2_obj.ARQ_bird_BP_BL_md_out_exp=ARQ_bird_BP_BL_md_out_exp[0]
        trex2_obj.ARQ_bird_BP_BL_lg_out_exp=ARQ_bird_BP_BL_lg_out_exp[0]
        trex2_obj.ARQ_bird_FP_BL_sm_out_exp=ARQ_bird_FP_BL_sm_out_exp[0]
        trex2_obj.ARQ_bird_FP_BL_md_out_exp=ARQ_bird_FP_BL_md_out_exp[0]
        trex2_obj.ARQ_bird_FP_BL_lg_out_exp=ARQ_bird_FP_BL_lg_out_exp[0]
        trex2_obj.ARQ_bird_AR_BL_sm_out_exp=ARQ_bird_AR_BL_sm_out_exp[0]
        trex2_obj.ARQ_bird_AR_BL_md_out_exp=ARQ_bird_AR_BL_md_out_exp[0]
        trex2_obj.ARQ_bird_AR_BL_lg_out_exp=ARQ_bird_AR_BL_lg_out_exp[0]
        trex2_obj.ARQ_bird_SE_BL_sm_out_exp=ARQ_bird_SE_BL_sm_out_exp[0]
        trex2_obj.ARQ_bird_SE_BL_md_out_exp=ARQ_bird_SE_BL_md_out_exp[0]
        trex2_obj.ARQ_bird_SE_BL_lg_out_exp=ARQ_bird_SE_BL_lg_out_exp[0]

        trex2_obj.ARQ_diet_bird_SG_A_BL_out_exp=ARQ_diet_bird_SG_A_BL_out_exp[0]
        trex2_obj.ARQ_diet_bird_SG_C_BL_out_exp=ARQ_diet_bird_SG_C_BL_out_exp[0]
        trex2_obj.ARQ_diet_bird_TG_A_BL_out_exp=ARQ_diet_bird_TG_A_BL_out_exp[0]
        trex2_obj.ARQ_diet_bird_TG_C_BL_out_exp=ARQ_diet_bird_TG_C_BL_out_exp[0]
        trex2_obj.ARQ_diet_bird_BP_A_BL_out_exp=ARQ_diet_bird_BP_A_BL_out_exp[0]
        trex2_obj.ARQ_diet_bird_BP_C_BL_out_exp=ARQ_diet_bird_BP_C_BL_out_exp[0]
        trex2_obj.ARQ_diet_bird_FP_A_BL_out_exp=ARQ_diet_bird_FP_A_BL_out_exp[0]
        trex2_obj.ARQ_diet_bird_FP_C_BL_out_exp=ARQ_diet_bird_FP_C_BL_out_exp[0]
        trex2_obj.ARQ_diet_bird_AR_A_BL_out_exp=ARQ_diet_bird_AR_A_BL_out_exp[0]
        trex2_obj.ARQ_diet_bird_AR_C_BL_out_exp=ARQ_diet_bird_AR_C_BL_out_exp[0]

        trex2_obj.EEC_dose_mamm_SG_sm_BL_out_exp=EEC_dose_mamm_SG_sm_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_SG_md_BL_out_exp=EEC_dose_mamm_SG_md_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_SG_lg_BL_out_exp=EEC_dose_mamm_SG_lg_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_TG_sm_BL_out_exp=EEC_dose_mamm_TG_sm_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_TG_md_BL_out_exp=EEC_dose_mamm_TG_md_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_TG_lg_BL_out_exp=EEC_dose_mamm_TG_lg_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_BP_sm_BL_out_exp=EEC_dose_mamm_BP_sm_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_BP_md_BL_out_exp=EEC_dose_mamm_BP_md_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_BP_lg_BL_out_exp=EEC_dose_mamm_BP_lg_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_FP_sm_BL_out_exp=EEC_dose_mamm_FP_sm_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_FP_md_BL_out_exp=EEC_dose_mamm_FP_md_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_FP_lg_BL_out_exp=EEC_dose_mamm_FP_lg_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_AR_sm_BL_out_exp=EEC_dose_mamm_AR_sm_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_AR_md_BL_out_exp=EEC_dose_mamm_AR_md_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_AR_lg_BL_out_exp=EEC_dose_mamm_AR_lg_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_SE_sm_BL_out_exp=EEC_dose_mamm_SE_sm_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_SE_md_BL_out_exp=EEC_dose_mamm_SE_md_BL_out_exp[0]
        trex2_obj.EEC_dose_mamm_SE_lg_BL_out_exp=EEC_dose_mamm_SE_lg_BL_out_exp[0]

        trex2_obj.ARQ_dose_mamm_SG_sm_BL_out_exp=ARQ_dose_mamm_SG_sm_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_SG_sm_BL_out_exp=CRQ_dose_mamm_SG_sm_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_SG_md_BL_out_exp=ARQ_dose_mamm_SG_md_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_SG_md_BL_out_exp=CRQ_dose_mamm_SG_md_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_SG_lg_BL_out_exp=ARQ_dose_mamm_SG_lg_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_SG_lg_BL_out_exp=CRQ_dose_mamm_SG_lg_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_TG_sm_BL_out_exp=ARQ_dose_mamm_TG_sm_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_TG_sm_BL_out_exp=CRQ_dose_mamm_TG_sm_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_TG_md_BL_out_exp=ARQ_dose_mamm_TG_md_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_TG_md_BL_out_exp=CRQ_dose_mamm_TG_md_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_TG_lg_BL_out_exp=ARQ_dose_mamm_TG_lg_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_TG_lg_BL_out_exp=CRQ_dose_mamm_TG_lg_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_BP_sm_BL_out_exp=ARQ_dose_mamm_BP_sm_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_BP_sm_BL_out_exp=CRQ_dose_mamm_BP_sm_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_BP_md_BL_out_exp=ARQ_dose_mamm_BP_md_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_BP_md_BL_out_exp=CRQ_dose_mamm_BP_md_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_BP_lg_BL_out_exp=ARQ_dose_mamm_BP_lg_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_BP_lg_BL_out_exp=CRQ_dose_mamm_BP_lg_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_FP_sm_BL_out_exp=ARQ_dose_mamm_FP_sm_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_FP_sm_BL_out_exp=CRQ_dose_mamm_FP_sm_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_FP_md_BL_out_exp=ARQ_dose_mamm_FP_md_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_FP_md_BL_out_exp=CRQ_dose_mamm_FP_md_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_FP_lg_BL_out_exp=ARQ_dose_mamm_FP_lg_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_FP_lg_BL_out_exp=CRQ_dose_mamm_FP_lg_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_AR_sm_BL_out_exp=ARQ_dose_mamm_AR_sm_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_AR_sm_BL_out_exp=CRQ_dose_mamm_AR_sm_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_AR_md_BL_out_exp=ARQ_dose_mamm_AR_md_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_AR_md_BL_out_exp=CRQ_dose_mamm_AR_md_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_AR_lg_BL_out_exp=ARQ_dose_mamm_AR_lg_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_AR_lg_BL_out_exp=CRQ_dose_mamm_AR_lg_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_SE_sm_BL_out_exp=ARQ_dose_mamm_SE_sm_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_SE_sm_BL_out_exp=CRQ_dose_mamm_SE_sm_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_SE_md_BL_out_exp=ARQ_dose_mamm_SE_md_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_SE_md_BL_out_exp=CRQ_dose_mamm_SE_md_BL_out_exp[0]
        trex2_obj.ARQ_dose_mamm_SE_lg_BL_out_exp=ARQ_dose_mamm_SE_lg_BL_out_exp[0]
        trex2_obj.CRQ_dose_mamm_SE_lg_BL_out_exp=CRQ_dose_mamm_SE_lg_BL_out_exp[0]

        trex2_obj.ARQ_diet_mamm_SG_BL_out_exp=ARQ_diet_mamm_SG_BL_out_exp[0]
        trex2_obj.CRQ_diet_mamm_SG_BL_out_exp=CRQ_diet_mamm_SG_BL_out_exp[0]
        trex2_obj.ARQ_diet_mamm_TG_BL_out_exp=ARQ_diet_mamm_TG_BL_out_exp[0]
        trex2_obj.CRQ_diet_mamm_TG_BL_out_exp=CRQ_diet_mamm_TG_BL_out_exp[0]
        trex2_obj.ARQ_diet_mamm_BP_BL_out_exp=ARQ_diet_mamm_BP_BL_out_exp[0]
        trex2_obj.CRQ_diet_mamm_BP_BL_out_exp=CRQ_diet_mamm_BP_BL_out_exp[0]
        trex2_obj.ARQ_diet_mamm_FP_BL_out_exp=ARQ_diet_mamm_FP_BL_out_exp[0]
        trex2_obj.CRQ_diet_mamm_FP_BL_out_exp=CRQ_diet_mamm_FP_BL_out_exp[0]
        trex2_obj.ARQ_diet_mamm_AR_BL_out_exp=ARQ_diet_mamm_AR_BL_out_exp[0]
        trex2_obj.CRQ_diet_mamm_AR_BL_out_exp=CRQ_diet_mamm_AR_BL_out_exp[0]

        trex2_obj.LD50_bl_bird_sm_out_exp=LD50_bl_bird_sm_out_exp[0]
        trex2_obj.LD50_bl_mamm_sm_out_exp=LD50_bl_mamm_sm_out_exp[0]
        trex2_obj.LD50_bl_bird_md_out_exp=LD50_bl_bird_md_out_exp[0]
        trex2_obj.LD50_bl_mamm_md_out_exp=LD50_bl_mamm_md_out_exp[0]
        trex2_obj.LD50_bl_bird_lg_out_exp=LD50_bl_bird_lg_out_exp[0]
        trex2_obj.LD50_bl_mamm_lg_out_exp=LD50_bl_mamm_lg_out_exp[0]

    else:
        sa_bird_1_s_out_exp.append(float(row_inp[161]))
        sa_bird_2_s_out_exp.append(float(row_inp[162]))
        sc_bird_s_out_exp.append(float(row_inp[163]))
        sa_mamm_1_s_out_exp.append(float(row_inp[164]))
        sa_mamm_2_s_out_exp.append(float(row_inp[165]))
        sc_mamm_s_out_exp.append(float(row_inp[166]))
        sa_bird_1_m_out_exp.append(float(row_inp[167]))
        sa_bird_2_m_out_exp.append(float(row_inp[168]))
        sc_bird_m_out_exp.append(float(row_inp[169]))
        sa_mamm_1_m_out_exp.append(float(row_inp[170]))
        sa_mamm_2_m_out_exp.append(float(row_inp[171]))
        sc_mamm_m_out_exp.append(float(row_inp[172]))
        sa_bird_1_l_out_exp.append(float(row_inp[173]))
        sa_bird_2_l_out_exp.append(float(row_inp[174]))
        sc_bird_l_out_exp.append(float(row_inp[175]))
        sa_mamm_1_l_out_exp.append(float(row_inp[176]))
        sa_mamm_2_l_out_exp.append(float(row_inp[177]))
        sc_mamm_l_out_exp.append(float(row_inp[178]))

        trex2_obj.sa_bird_1_s_out_exp=sa_bird_1_s_out_exp[0]
        trex2_obj.sa_bird_2_s_out_exp=sa_bird_2_s_out_exp[0]
        trex2_obj.sc_bird_s_out_exp=sc_bird_s_out_exp[0]
        trex2_obj.sa_mamm_1_s_out_exp=sa_mamm_1_s_out_exp[0]
        trex2_obj.sa_mamm_2_s_out_exp=sa_mamm_2_s_out_exp[0]
        trex2_obj.sc_mamm_s_out_exp=sc_mamm_s_out_exp[0]
        trex2_obj.sa_bird_1_m_out_exp=sa_bird_1_m_out_exp[0]
        trex2_obj.sa_bird_2_m_out_exp=sa_bird_2_m_out_exp[0]
        trex2_obj.sc_bird_m_out_exp=sc_bird_m_out_exp[0]
        trex2_obj.sa_mamm_1_m_out_exp=sa_mamm_1_m_out_exp[0]
        trex2_obj.sa_mamm_2_m_out_exp=sa_mamm_2_m_out_exp[0]
        trex2_obj.sc_mamm_m_out_exp=sc_mamm_m_out_exp[0]
        trex2_obj.sa_bird_1_l_out_exp=sa_bird_1_l_out_exp[0]
        trex2_obj.sa_bird_2_l_out_exp=sa_bird_2_l_out_exp[0]
        trex2_obj.sc_bird_l_out_exp=sc_bird_l_out_exp[0]
        trex2_obj.sa_mamm_1_l_out_exp=sa_mamm_1_l_out_exp[0]
        trex2_obj.sa_mamm_2_l_out_exp=sa_mamm_2_l_out_exp[0]
        trex2_obj.sc_mamm_l_out_exp=sc_mamm_l_out_exp[0]

    html_qaqc=html_qaqc+trex2_tables.table_all_qaqc(trex2_obj)

class TherpsQaqcPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "TREX 1.5.2 QA/QC")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'trex2','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'therps',
                'model_attributes':'T-Rex QAQC'})
        html = html + html_qaqc
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, trex2_obj.__dict__, 'trex2', 'qaqc')
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TherpsQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
