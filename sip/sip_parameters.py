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
   # select_receptor = forms.ChoiceField(required=True, choices=SELECT_RECEPTOR, initial='Both')
    body_weight_of_bird = forms.FloatField(required=True, label='Body weight of bird (kg)', initial='4')
    body_weight_of_mammal = forms.FloatField(required=True,label='Body weight of mammal (kg)', initial='5')
    solubility = forms.FloatField(required=True, label='Solubility(mg/L)', initial='2')
    ld50_a = forms.FloatField(required=True, label='Avian LD50 (mg/kg-bw)', initial='3')
    ld50_m = forms.FloatField(required=True, label='Mammalian LD50 (mg/kg-bw)', initial='6')
    body_weight_of_the_assessed_bird = forms.FloatField(required=True, label='Body weight of assessed bird (kg)', initial='8')
    body_weight_of_the_tested_bird = forms.FloatField(required=True, label='Body weight of tested bird (kg)', initial='9')
    body_weight_of_the_assessed_mammal = forms.FloatField(required=True, label='Body weight of assessed mammal (kg)', initial='5')
    body_weight_of_the_tested_mammal = forms.FloatField(required=True, label='Body weight of tested mammal (kg)', initial='4')
    mineau_scaling_factor = forms.FloatField(required=True, label='Mineau scaling factor', initial='1.15')
    NOAEC = forms.FloatField(required=True, label='NOAEC (mg/kg)', initial='7')
    NOAEL = forms.FloatField(required=True, label='NOAEL (mg/kg)', initial='8')