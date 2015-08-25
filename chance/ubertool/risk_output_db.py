# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

@author: jharston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
import sys
sys.path.append('../CAS')
from CAS.CASGql import CASGql
from google.appengine.api import users
from google.appengine.ext import db
from use import Use
import logging
import datetime

APPLICATIONTYPE = (('broadcast','broadcast'),('row/band/in-furrow','row/band/in-furrow'))
APPTYPE = (('liquid','liquid'),('granular','granular'))
YN = (('Yes','Yes'),('No','No'))

class UseInp(forms.Form):
	user_use_configuration = forms.ChoiceField(label="User Saved Use Configuration",required=True)
    config_name = forms.CharField(label="Use Configuration Name", initial="use-config-%s"%datetime.datetime.now())
    gran_bird_ex_derm_dose = forms.FloatField(label='Avian external dermal dose from granular application', required=True)
    gran_repamp_ex_derm_dose = forms.FloatField(label='Reptile/amphibian external dermal dose from granular application', required=True)
    gran_mam_ex_derm_dose = forms.FloatField(label='Mammalian external dermal dose from granular application', required=True)
    fol_bird_ex_derm_dose = forms.FloatField(label='Avian external dermal dose from foliar spray application', required=True)
    fol_repamp_ex_derm_dose = forms.FloatField(label='Reptile/amphibian external dermal dose from foliar spray application', required=True)
    fol_mammalian_ex_derm_dose = forms.FloatField(label='Mammalian external dermal dose from foliar spray application', required=True)
    bgs_bird_ex_derm_dose = forms.FloatField(label='Avian external dermal dose from ground spray application', required=True)
    bgs_repamp_ex_derm_dose = forms.FloatField(label='Reptile/amphibian external dermal dose from ground spray application', required=True)
    bgs_mam_ex_derm_dose = forms.FloatField(label='Mammalian external dermal dose from ground spray application', required=True)
    ratio_gran_bird = forms.FloatField(label='Avian ratio of exposure to toxicity from granular application', required=True)
    LOC_gran_bird = forms.FloatField(label='Avian level of concern from granular application', required=True)
    ratio_gran_rep = forms.FloatField(label='Reptile ratio of exposure from granular application', required=True)
    LOC_gran_rep = forms.FloatField(label='Reptile level of concern from granular application', required=True)
    ratio_gran_amp = forms.FloatField(label='Amphibian ratio of exposure from granular application', required=True)
    LOC_gran_amp = forms.FloatField(label='Amphibian level of concern from granular application', required=True)
    ratio_gran_mam = forms.FloatField(label='Mammalian ratio of exposure from granular application', required=True)
    LOC_gran_mam = forms.FloatField(label='Mammalian level of concern from granular application', required=True)
    ratio_fol_bird = forms.FloatField(label='Avian ratio of exposure from foliar spray application', required=True)
    LOC_fol_bird = forms.FloatField(label='Avian level of concern from foliar spray application', required=True)
    ratio_fol_rep = forms.FloatField(label='Reptile ratio of exposure from foliar spray application', required=True)
    LOC_fol_rep = forms.FloatField(label='Reptile level of concern from foliar spray application', required=True)
    ratio_fol_amp = forms.FloatField(label='Amphibian ratio of exposure from foliar spray application', required=True)
    LOC_fol_amp = forms.FloatField(label='Amphibian level of concern from foliar spray application', required=True)
    ratio_fol_mam = forms.FloatField(label='Mammalian ratio of exposure from foliar spray application', required=True)
    LOC_fol_mam = forms.FloatField(label='Mammalian level of concern from foliar spray application', required=True)
    ratio_bgs_bird = forms.FloatField(label='Avian ratio of exposure from toxicity bare ground spray application', required=True)
    LOC_bgs_bird = forms.FloatField(label='Avian level of concern from toxicity bare ground spray application', required=True)
    ratio_bgs_rep = forms.FloatField(label='Reptile ratio of exposure from toxicity bare ground spray application', required=True)
    LOC_bgs_rep = forms.FloatField(label='Reptile level of concern from toxicity bare ground spray application', required=True)
    ratio_bgs_amp = forms.FloatField(label='Amphibian ratio of exposure from toxicity bare ground spray application', required=True)
    LOC_bgs_amp = forms.FloatField(label='Amphibian level of exposure from toxicity bare ground spray application', required=True)
    ratio_bgs_mam = forms.FloatField(label='Mammalian ratio of exposure from toxicity bare ground spray application', required=True)
    LOC_bgs_mam = forms.FloatField(label='Mammalian level of exposure from toxicity bare ground spray application', required=True)
    EEC_diet_SG = forms.FloatField(label='Dietary based EECs (Short grass)')
    EEC_diet_TG = forms.FloatField(label='Dietary based EECs (Tall grass)')
    EEC_diet_BP = forms.FloatField(label='Dietary based EECs (Broadleaf plants)')
    EEC_diet_FR = forms.FloatField(label='Dietary based EECs (Fruits/Pods/Seeds)')
    EEC_diet_AR = forms.FloatField(label='Dietary based EECs (Arthropods)')
    EEC_dose_bird_SG_sm = forms.FloatField(label='Avian dose based EECs (Short grass/Small bird)')
    EEC_dose_bird_SG_md = forms.FloatField(label='Avian dose based EECs (Short grass/Medium bird)')
    EEC_dose_bird_SG_lg = forms.FloatField(label='Avian dose based EECs (Short grass/Large bird)')
    EEC_dose_bird_TG_sm = forms.FloatField(label='Avian dose based EECs (Tall grass/Small bird)')
    EEC_dose_bird_TG_md = forms.FloatField(label='Avian dose based EECs (Tall grass/Medium bird)')
    EEC_dose_bird_TG_lg = forms.FloatField(label='Avian dose based EECs (Tall grass/Large bird)')
    EEC_dose_bird_BP_sm = forms.FloatField(label='Avian dose based EECs (Broadleaf plants/Small bird)')
    EEC_dose_bird_BP_md = forms.FloatField(label='Avian dose based EECs (Broadleaf plants/Medium bird)')
    EEC_dose_bird_BP_lg = forms.FloatField(label='Avian dose based EECs (Broadleaf plants/Large bird)')
    EEC_dose_bird_FP_sm = forms.FloatField(label='Avian dose based EECs (Fruits/pods/Small bird)')
    EEC_dose_bird_FP_md = forms.FloatField(label='Avian dose based EECs (Fruits/pods/Medium bird)')
    EEC_dose_bird_FP_lg = forms.FloatField(label='Avian dose based EECs (Fruits/pods/Large bird)')
    EEC_dose_bird_AR_sm = forms.FloatField(label='Avian dose based EECs (Arthropods/Small bird)')
    EEC_dose_bird_AR_md = forms.FloatField(label='Avian dose based EECs (Arthropods/Medium bird)')
    EEC_dose_bird_AR_lg = forms.FloatField(label='Avian dose based EECs (Arthropods/Large bird)')
    EEC_dose_bird_SE_sm = forms.FloatField(label='Avian dose based EECs (Seeds/Small bird)')
    EEC_dose_bird_SE_md = forms.FloatField(label='Avian dose based EECs (Seeds/Medium bird)')
    EEC_dose_bird_SE_lg = forms.FloatField(label='Avian dose based EECs (Seeds/Large bird)')
    ARQ_diet_bird_SG_A = forms.FloatField(label='Avian diet based RQs for Short grass (Acute)')
    ARQ_diet_bird_SG_C = forms.FloatField(label='Avian diet based RQs for Short grass (Chronic)')      
    ARQ_diet_bird_TG_A = forms.FloatField(label='Avian diet based RQs for Tall grass (Acute)')          
    ARQ_diet_bird_TG_C = forms.FloatField(label='Avian diet based RQs for Tall grass (Chronic)')  
    ARQ_diet_bird_BP_A = forms.FloatField(label='Avian diet based RQs for Broadleaf plants (Acute)')
    ARQ_diet_bird_BP_C = forms.FloatField(label='Avian diet based RQs for Broadleaf plants (Chronic)') 
    ARQ_diet_bird_FP_A = forms.FloatField(label='Avian diet based RQs for Fruits/Pods (Acute)')      
    ARQ_diet_bird_FP_C = forms.FloatField(label='Avian diet based RQs for Fruits/Pods (Chronic)')      
    ARQ_diet_bird_AR_A = forms.FloatField(label='Avian diet based RQs for Arthropods (Acute)')  
    ARQ_diet_bird_AR_C = forms.FloatField(label='Avian diet based RQs for Arthropods (Chronic)') 
    EEC_dose_mamm_SG_sm = forms.FloatField(label='Avian dose based EECs (Short grass/Small mammal)')
    EEC_dose_mamm_SG_md = forms.FloatField(label='Avian dose based EECs (Short grass/Medium mammal)')
    EEC_dose_mamm_SG_lg = forms.FloatField(label='Avian dose based EECs (Short grass/Large mammal)')
    EEC_dose_mamm_TG_sm = forms.FloatField(label='Avian dose based EECs (Tall grass/Small mammal)')
    EEC_dose_mamm_TG_md = forms.FloatField(label='Avian dose based EECs (Tall grass/Medium mammal)')
    EEC_dose_mamm_TG_lg = forms.FloatField(label='Avian dose based EECs (Tall grass/Large mammal)')
    EEC_dose_mamm_BP_sm = forms.FloatField(label='Avian dose based EECs (Broadleaf plants/Small mammal)')
    EEC_dose_mamm_BP_md = forms.FloatField(label='Avian dose based EECs (Broadleaf plants/Medium mammal)')
    EEC_dose_mamm_BP_lg = forms.FloatField(label='Avian dose based EECs (Broadleaf plants/Large mammal)')
    EEC_dose_mamm_FP_sm = forms.FloatField(label='Avian dose based EECs (Fruits/pods/Small mammal)')
    EEC_dose_mamm_FP_md = forms.FloatField(label='Avian dose based EECs (Fruits/pods/Medium mammal)')
    EEC_dose_mamm_FP_lg = forms.FloatField(label='Avian dose based EECs (Fruits/pods/Large mammal)')
    EEC_dose_mamm_AR_sm = forms.FloatField(label='Avian dose based EECs (Arthropods/Small mammal)')
    EEC_dose_mamm_AR_md = forms.FloatField(label='Avian dose based EECs (Arthropods/Medium mammal)')
    EEC_dose_mamm_AR_lg = forms.FloatField(label='Avian dose based EECs (Arthropods/Large mammal)')
    EEC_dose_mamm_SE_sm = forms.FloatField(label='Avian dose based EECs (Seeds/Small mammal)')
    EEC_dose_mamm_SE_md = forms.FloatField(label='Avian dose based EECs (Seeds/Medium mammal)')
    EEC_dose_mamm_SE_lg = forms.FloatField(label='Avian dose based EECs (Seeds/Large mammal)')
    ARQ_dose_mamm_SG_sm = forms.FloatField(label='Mammalian dose based RQs for Short grass (Acute, small)')
    CRQ_dose_mamm_SG_sm = forms.FloatField(label='Mammalian dose based RQs for Short grass (Chronic, small)')
    ARQ_dose_mamm_SG_md = forms.FloatField(label='Mammalian dose based RQs for Short grass (Acute, medium)')
    CRQ_dose_mamm_SG_md = forms.FloatField(label='Mammalian dose based RQs for Short grass (Chronic, medium)')
    ARQ_dose_mamm_SG_lg = forms.FloatField(label='Mammalian dose based RQs for Short grass (Acute, large)')
    CRQ_dose_mamm_SG_lg = forms.FloatField(label='Mammalian dose based RQs for Short grass (Chronic, large)')
    ARQ_dose_mamm_TG_sm = forms.FloatField(label='Mammalian dose based RQs for Tall grass (Acute, small)')
    CRQ_dose_mamm_TG_sm = forms.FloatField(label='Mammalian dose based RQs for Tall grass (Chronic, small)')
    ARQ_dose_mamm_TG_md = forms.FloatField(label='Mammalian dose based RQs for Tall grass (Acute, medium)')
    CRQ_dose_mamm_TG_md = forms.FloatField(label='Mammalian dose based RQs for Tall grass (Chronic, medium)')
    ARQ_dose_mamm_TG_lg = forms.FloatField(label='Mammalian dose based RQs for Tall grass (Acute, large)')
    CRQ_dose_mamm_TG_lg = forms.FloatField(label='Mammalian dose based RQs for Tall grass (Chronic, large)')
    ARQ_dose_mamm_BP_sm = forms.FloatField(label='Mammalian dose based RQs for Broadleaf plants (Acute, small)')
    CRQ_dose_mamm_BP_sm = forms.FloatField(label='Mammalian dose based RQs for Broadleaf plants (Chronic, small)')
    ARQ_dose_mamm_BP_md = forms.FloatField(label='Mammalian dose based RQs for Broadleaf plants (Acute, medium)')
    CRQ_dose_mamm_BP_md = forms.FloatField(label='Mammalian dose based RQs for Broadleaf plants (Chronic, medium)')
    ARQ_dose_mamm_BP_lg = forms.FloatField(label='Mammalian dose based RQs for Broadleaf plants (Acute, large)')
    CRQ_dose_mamm_BP_lg = forms.FloatField(label='Mammalian dose based RQs for Broadleaf plants (Chronic, large)')
    ARQ_dose_mamm_FP_sm = forms.FloatField(label='Mammalian dose based RQs for Fruits, Pods (Acute, small)')
    CRQ_dose_mamm_FP_sm = forms.FloatField(label='Mammalian dose based RQs for Fruits, Pods (Chronic, small)')
    ARQ_dose_mamm_FP_md = forms.FloatField(label='Mammalian dose based RQs for Fruits, Pods (Acute, medium)')
    CRQ_dose_mamm_FP_md = forms.FloatField(label='Mammalian dose based RQs for Fruits, Pods (Chronic, medium)')
    ARQ_dose_mamm_FP_lg = forms.FloatField(label='Mammalian dose based RQs for Fruits, Pods (Acute, large)')
    CRQ_dose_mamm_FP_lg = forms.FloatField(label='Mammalian dose based RQs for Fruits, Pods (Chronic, large)')
    ARQ_dose_mamm_AR_sm = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Acute, small)')
    CRQ_dose_mamm_AR_sm = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Chronic, small)')
    ARQ_dose_mamm_AR_md = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Acute, medium)')
    CRQ_dose_mamm_AR_md = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Chronic, medium)')
    ARQ_dose_mamm_AR_lg = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Acute, large)')
    CRQ_dose_mamm_AR_lg = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Chronic, large)')
    ARQ_dose_mamm_SE_sm = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Acute, small)')
    CRQ_dose_mamm_SE_sm = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Chronic, small)')
    ARQ_dose_mamm_SE_md = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Acute, medium)')
    CRQ_dose_mamm_SE_md = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Chronic, medium)')
    ARQ_dose_mamm_SE_lg = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Acute, large)')
    CRQ_dose_mamm_SE_lg = forms.FloatField(label='Mammalian dose based RQs for Arthropods (Chronic, large)')
    ARQ_diet_mamm_SG = forms.FloatField(label='Mammalian diet based RQs for Short grass (Acute)')
    CRQ_diet_mamm_SG = forms.FloatField(label='Mammalian diet based RQs for Short grass (Chronic)')      
    ARQ_diet_mamm_TG = forms.FloatField(label='Mammalian diet based RQs for Tall grass (Acute)')          
    CRQ_diet_mamm_TG = forms.FloatField(label='Mammalian diet based RQs for Tall grass (Chronic)')  
    ARQ_diet_mamm_BP = forms.FloatField(label='Mammalian diet based RQs for Broadleaf plants (Acute)')
    CRQ_diet_mamm_BP = forms.FloatField(label='Mammalian diet based RQs for Broadleaf plants (Chronic)') 
    ARQ_diet_mamm_FP = forms.FloatField(label='Mammalian diet based RQs for Fruits/Pods (Acute)')      
    CRQ_diet_mamm_FP = forms.FloatField(label='Mammalian diet based RQs for Fruits/Pods (Chronic)')      
    ARQ_diet_mamm_AR = forms.FloatField(label='Mammalian diet based RQs for Arthropods (Acute)')  
    CRQ_diet_mamm_AR = forms.FloatField(label='Mammalian diet based RQs for Arthropods (Chronic)') 
    LD50_rg_bird_sm = forms.FloatField(label='Avian Banded granular application LD50ft-2 (Small)')
    LD50_rg_bird_md = forms.FloatField(label='Avian Banded granular application LD50ft-2 (Medium)')
    LD50_rg_bird_lg = forms.FloatField(label='Avian Banded granular application LD50ft-2 (Large)')
    LD50_rg_mamm_sm = forms.FloatField(label='Mammalian Banded granular application LD50ft-2 (Small)')
    LD50_rg_mamm_md = forms.FloatField(label='Mammalian Banded granular application LD50ft-2 (Medium)')
    LD50_rg_mamm_lg = forms.FloatField(label='Mammalian Banded granular application LD50ft-2 (Large)')
    LD50_rl_bird_sm = forms.FloatField(label='Avian Banded liquid application LD50ft-2 (Small)')
    LD50_rl_bird_md = forms.FloatField(label='Avian Banded liquid application LD50ft-2 (Medium)')
    LD50_rl_bird_lg = forms.FloatField(label='Avian Banded liquid application LD50ft-2 (Larle)')
    LD50_rl_mamm_sm = forms.FloatField(label='Mammalian Banded liquid application LD50ft-2 (Small)')
    LD50_rl_mamm_md = forms.FloatField(label='Mammalian Banded liquid application LD50ft-2 (Medium)')
    LD50_rl_mamm_lg = forms.FloatField(label='Mammalian Banded liquid application LD50ft-2 (Large)')
    LD50_bg_bird_sm = forms.FloatField(label='Avian Broadcast granular application LD50ft-2 (Small)')
    LD50_bg_bird_md = forms.FloatField(label='Avian Broadcast granular application LD50ft-2 (Medium)')
    LD50_bg_bird_lg = forms.FloatField(label='Avian Broadcast granular application LD50ft-2 (Labge)')
    LD50_bg_mamm_sm = forms.FloatField(label='Mammalian Broadcast granular application LD50ft-2 (Small)')
    LD50_bg_mamm_md = forms.FloatField(label='Mammalian Broadcast granular application LD50ft-2 (Medium)')
    LD50_bg_mamm_lg = forms.FloatField(label='Mammalian Broadcast granular application LD50ft-2 (Large)')
    LD50_bl_bird_sm = forms.FloatField(label='Avian Broadcast granular application LD50ft-2 (Small)')
    LD50_bl_bird_md = forms.FloatField(label='Avian Broadcast granular application LD50ft-2 (Medium)')
    LD50_bl_bird_lg = forms.FloatField(label='Avian Broadcast granular application LD50ft-2 (Lable)')
    LD50_bl_mamm_sm = forms.FloatField(label='Mammalian Broadcast granular application LD50ft-2 (Small)')
    LD50_bl_mamm_md = forms.FloatField(label='Mammalian Broadcast granular application LD50ft-2 (Medium)')
    LD50_bl_mamm_lg = forms.FloatField(label='Mammalian Broadcast granular application LD50ft-2 (Large)')




    
    
















