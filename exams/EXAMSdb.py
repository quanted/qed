# -*- coding: utf-8 -*-
"""
Created on 06-06-2013

"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.utils.safestring import mark_safe


class EXAMSInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    molecular_weight = forms.FloatField(required=True, label='Molecular weight (g/mol)') 
    solubility = forms.FloatField(required=True, label='Solubility(mg/L)')
    Koc = forms.FloatField(required=True, label='Aquatic Sediment Koc (mL/g)')   
    vapor_pressure = forms.FloatField(required=True, label='Vapor Pressure (torr)')
    aerobic_aquatic_metabolism = forms.FloatField(required=True, label='Aerobic aquatic metabolism (days)')
    anaerobic_aquatic_metabolism = forms.FloatField(required=True, label='Anaerobic aquatic metabolism (days)')
    aquatic_direct_photolysis = forms.FloatField(required=True, label='Aquatic Direct Photolysis (days)')

class EXAMSPh(forms.Form):
    temperature = forms.FloatField(required=True, label=mark_safe('Test Temperature (<sup>o</sup>C)'))
    n_ph = forms.FloatField(required=True, label='Number of Different pH')

    # aerobic_soil_metabolism = forms.FloatField(required=True,label='Aerobic soil metabolism (half-life, days)')    
    # hydrolysis_ph5 = forms.FloatField(required=True,label='Hydrolysis: pH=5/acidic (half-life, days)')
    # hydrolysis_ph7 = forms.FloatField(required=True,label='Hydrolysis: pH=7/neutral (half-life, days)')
    # hydrolysis_ph9 = forms.FloatField(required=True,label='Hydrolysis: pH=9/alkaline (half-life, days)')

