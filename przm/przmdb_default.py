# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: JHarston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models

EFFICIENCY = (('0.95','0.95'),('0.99','0.99'))

class PRZMInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    incorporation_depth = forms.FloatField(required=True,label='Incorporation Depth (cm)')    
    percent_incorporated = forms.FloatField(required=True,label='Percent Incorporated (%)')
    application_rate = forms.FloatField(required=True,label='Application rate (kgs/ha)')
    application_date = forms.DateField()
    number_of_applications = forms.FloatField(required=True,label='Number of applications')
    interval_between_applications = forms.FloatField(required=True,label='Interval between applications (days)')
    application_efficiency = forms.ChoiceField(required=True,choices=EFFICIENCY,label='Application efficiency (0.95 for aerial; 0.99 for ground,airblast)')
    spray_drift = forms.FloatField(required=True,label='Spray Drift (fraction)')
    molecular_weight = forms.FloatField(required=True,label='Molecular weight (g/mol)') 
    henrys_law_constant = forms.FloatField(required=True,label="Henry's Law Constant (atm-m^3/mol)")
    vapor_pressure = forms.FloatField(required=True,label='Vapor Pressure (torr)')
    solubility = forms.FloatField(required=True,label='Solubility(mg/L)')
    Kd = forms.FloatField(required=True,label='Kd (mL/g)')
    Koc = forms.FloatField(required=True,label='Koc (mL/g OC)')
    photolysis = forms.FloatField(required=True, label='Photolysis, aquatic half-life (days)')
    aerobic_aquatic_metabolism = forms.FloatField(required=True,label='Aerobic aquatic metabolism (half-life, days)')
    anaerobic_aquatic_metabolism = forms.FloatField(required=True,label='Anaerobic aquatic metabolism (half-life, days)')
    aerobic_soil_metabolism = forms.FloatField(required=True,label='Aerobic soil metabolism (half-life, days)')    
    hydrolysis_ph5 = forms.FloatField(required=True,label='Hydrolysis: pH=5/acidic (half-life, days)')
    hydrolysis_ph7 = forms.FloatField(required=True,label='Hydrolysis: pH=7/neutral (half-life, days)')
    hydrolysis_ph9 = forms.FloatField(required=True,label='Hydrolysis: pH=9/alkaline (half-life, days)')
    foliar_extraction = forms.FloatField(required=True,label='Foliar extraction, default=0.5 (cm^-1)')
    foliar_decay_rate = forms.FloatField(required=True,label='Foliar Decay Rate (day^-1)')
    foliar_dissipation_half_life = forms.FloatField(required=True,label='Foliar Dissipation Half-life (days)')
    
    