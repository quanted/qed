# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

@author: jharston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models

#YN = (('Yes','Yes'),('No','No'))

class EcoInp(forms.Form):
    concentration_of_particulate_organic_carbon = forms.FloatField(label='Concentration of particulate organic carbon (kg OC/L)', initial='0')
    concentration_of_dissolved_organic_carbon = forms.FloatField(label='Concentration of dissolved organic carbon (kg OC/L)', initial='0')
    concentration_of_dissolved_oxygen = forms.FloatField(label='Concentration of dissolved oxygen (mg O2/L)', initial='5.0')
    water_temperature = forms.FloatField(label='Water temperature (degrees Celsius)')
    concentration_of_suspended_solids = forms.FloatField(label='Concentration of suspended solids (kg/L)')
    sediment_organic_carbon = forms.FloatField(label='Sediment organic Carbon (%)')