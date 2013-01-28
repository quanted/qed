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


class PPInp(forms.Form):
    user_id = users.get_current_user().user_id()
    config_name = forms.CharField(label="Use Configuration Name", initial="use-config-%s"%user_id)
    molecular_weight = forms.FloatField(label='Molecular weight (g/mol)')
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
    