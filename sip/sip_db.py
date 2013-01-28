# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 16:13:59 2011

@author: TPurucke
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models

SELECT_RECEPTOR = (('Avian','Avian'),('Mammalian','Mammalian'),('Both','Both'))

class SIPInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    select_receptor = forms.ChoiceField(required=True, choices=SELECT_RECEPTOR, initial='Both')
    body_weight_of_bird = forms.FloatField(required=True, label='Body weight of bird (kg)')
    body_weight_of_mammal = forms.FloatField(required=True,label='Body weight of mammal (kg)')
    solubility = forms.FloatField(required=True, label='Solubility(mg/L)')
    ld50 = forms.FloatField(required=True, label='LD50 (mg/kg-bw)')
    body_weight_of_the_assessed_bird = forms.FloatField(required=True, label='Body weight of assessed bird (kg)')
    body_weight_of_the_tested_bird = forms.FloatField(required=True, label='Body weight of tested bird (kg)')
    body_weight_of_the_assessed_mammal = forms.FloatField(required=True, label='Body weight of assessed mammal (kg)')
    body_weight_of_the_tested_mammal = forms.FloatField(required=True, label='Body weight of tested mammal (kg)')
    mineau_scaling_factor = forms.FloatField(required=True, label='Mineau scaling factor', initial='1.15')
    NOAEC = forms.FloatField(required=True, label='NOAEC (mg/kg)')
    NOAEL = forms.FloatField(required=True, label='NOAEL (mg/kg)')