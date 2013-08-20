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
    molecular_weight = forms.FloatField(label="Molecular Weight (g/mol)")
    henrys_law_constant = forms.FloatField(label="Henry's Law Constant (atm-m^3/mol)")
    vapor_pressure = forms.FloatField(label='Vapor Pressure (torr)')
    solubility = forms.FloatField(label='Solubility(mg/L)')
    solubility_ppm = forms.FloatField(label='Solubility(ppm)')
    Kd = forms.FloatField(label='Kd (mL/g)')
    Koc = forms.FloatField(label='Koc (mL/g OC)')   
    photolysis = forms.FloatField(label='Photolysis, aquatic half-life (days)')
    hydrolysis_ph5 = forms.FloatField(label='Hydrolysis: pH=5/acidic (half-life, days)')
    hydrolysis_ph7 = forms.FloatField(label='Hydrolysis: pH=7/neutral (half-life, days)')
    hydrolysis_ph9 = forms.FloatField(label='Hydrolysis: pH=9/alkaline (half-life, days)')
