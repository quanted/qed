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

    
    
















