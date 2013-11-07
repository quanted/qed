# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: JHarston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

class swcInp_chem(forms.Form):
	# Chemical Tab
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    sorp_K = forms.FloatField(required=True,label='Sorption Coefficient (mL/g)')
    unit = (('1','Koc'),('0','Kd'))
    sorp_K_unit = forms.ChoiceField(required=True,widget=forms.RadioSelect,label='Sorption Coefficient Type', choices=unit)
    wc_hl = forms.FloatField(required=True,label='Water Column Metabolism Halflife (day)')
    w_temp = forms.FloatField(required=True,label=mark_safe('Water Reference Temperature (&deg;C)'))
    bm_hl = forms.FloatField(required=True,label='Benthic Metabolism Halflife (day)')
    ben_temp = forms.FloatField(required=True,label=mark_safe('Benthic Reference Temperature (&deg;C)'))
    ap_hl = forms.FloatField(required=True,label='Aquatic Photolysis Metabolism Halflife (day)')
    p_ref = forms.FloatField(required=True,label=mark_safe('Photolysis Ref Latitude (&deg;)'))
    h_hl = forms.FloatField(required=True,label='Hydrolysis Halflife (day)')
    s_hl = forms.FloatField(required=True,label='Soil Halflife (day)')
    s_ref = forms.FloatField(required=True,label=mark_safe('Soil Ref (&deg;)'))
    f_hl = forms.FloatField(required=True,label='Foliar Halflife (day)')
    mwt = forms.FloatField(required=True,label='MWT')
    vp = forms.FloatField(required=True,label='Vapor Pressure (torr)')
    sol = forms.FloatField(required=True,label='Solubility (mg/L)')

    
class swcInp_appl(forms.Form):
    # Applications Tab
    app_n = forms.FloatField(required=True,label='Number of Applications (50 max)')
    dates = (('1','Absolute Dates'),('0','Relative Dates'))
    sorp_K_unit = forms.ChoiceField(required=True,widget=forms.RadioSelect,label='Choose Way of Entering Application Dates', choices=dates)

    
class swcInp_cropland(forms.Form):
	# Crop/Land Tab
    temp = forms.FloatField(required=True,label='Temporary Crop/Land Tab')

    
class swcInp_runoff(forms.Form):
# 	# Runoff Tab
    temp = forms.FloatField(required=True,label='Temporary Runoff Tab')


    
class swcInp_waterbody(forms.Form):
	# Water Body Tab
    temp = forms.FloatField(required=True,label='Temporary Water Body Tab')
