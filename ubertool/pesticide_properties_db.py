# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

@author: jharston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from google.appengine.api import users
from google.appengine.ext import db
from pesticide_properties import PesticideProperties
import datetime

class PPInp(forms.Form):
    user_pest_configuration = forms.ChoiceField(label="User Saved Pesticide Properties Configuration",required=True)
    config_name = forms.CharField(label="Pesticide Properties Configuration Name", initial="pesticide-properties-config-%s"%datetime.datetime.now())
    chemical_name = forms.CharField(label="Chemical Name")
    Formulated_product_name = forms.CharField(label="Formulated product name")
    seed_treatment_formulation_name = forms.CharField(label="seed_treatment_formulation_name")
    label_epa_reg_no = forms.CharField(label="Label EPA Reg. No.")
    molecular_weight = forms.FloatField(label='Molecular weight (g/mol)')
    percent_ai = forms.FloatField(label='% Active Ingredient')
    henrys_law_constant = forms.FloatField(label="Henry's Law Constant (atm-m^3/mol)")
    vapor_pressure = forms.FloatField(label='Vapor Pressure (torr)')
    solubility = forms.FloatField(label='Solubility(mg/L)')
    Kd = forms.FloatField(label='Kd (mL/g)')
    Koc = forms.FloatField(label='Koc (mL/g OC)')   
    photolysis = forms.FloatField(label='Photolysis, aquatic half-life (days)')
    aerobic_aquatic_metabolism = forms.FloatField(label='Aerobic aquatic metabolism (half-life, days)')
    anaerobic_aquatic_metabolism = forms.FloatField(label='Anaerobic aquatic metabolism (half-life, days)')
    aerobic_soil_metabolism = forms.FloatField(label='Aerobic soil metabolism (half-life, days)')    
    hydrolysis_ph5 = forms.FloatField(label='Hydrolysis: pH=5/acidic (half-life, days)')
    hydrolysis_ph7 = forms.FloatField(label='Hydrolysis: pH=7/neutral (half-life, days)')
    hydrolysis_ph9 = forms.FloatField(label='Hydrolysis: pH=9/alkaline (half-life, days)')
    foliar_extraction = forms.FloatField(label='Foliar extraction, default=0.5 (cm^-1)')
    foliar_decay_rate = forms.FloatField(label='Foliar Decay Rate (day^-1)')
    foliar_dissipation_half_life = forms.FloatField(label='Foliar Dissipation Half-life (days)')
    density_of_product = forms.FloatField(label='Density of product (lbs/gal)')

    