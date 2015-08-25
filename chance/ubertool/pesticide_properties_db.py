# -*- coding: utf-8 -*-
"""

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
    photolysis = forms.FloatField(label='Photolysis, aquatic half-life (days)')
    hydrolysis_ph5 = forms.FloatField(label='Hydrolysis: pH=5/acidic (half-life, days)')
    hydrolysis_ph7 = forms.FloatField(label='Hydrolysis: pH=7/neutral (half-life, days)')
    hydrolysis_ph9 = forms.FloatField(label='Hydrolysis: pH=9/alkaline (half-life, days)')
    l_kow = forms.FloatField(label='Log Kow')
    k_oc = forms.FloatField(label='Koc (L/kg OC)')
    c_wdp = forms.FloatField(label='Pore water (benthic) EECs (ug/L)')
    water_column_EEC = forms.FloatField(label='Water column 1 in 10 years EECs (ug/L)')
    




