# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 16:13:59 2011

@author: TPurucke
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

Species_of_the_tested_bird_CHOICES=(('','Make a selection'),('178','Bobwhite quail'),('1580','Mallard duck'),('1','Other'))
Species_of_the_tested_mamm_CHOICES=(('','Make a selection'),('350','Laboratory rat'),('1','Other'))
#SELECT_RECEPTOR = (('Avian','Avian'),('Mammalian','Mammalian'),('Both','Both'))

class SIPInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), initial='atrazine')
   # select_receptor = forms.ChoiceField(required=True, choices=SELECT_RECEPTOR, initial='Both')
 #   body_weight_of_bird = forms.FloatField(required=True, label='Body weight of bird (kg)', initial='4')
  #  body_weight_of_mammal = forms.FloatField(required=True,label='Body weight of mammal (kg)', initial='5')
    solubility = forms.FloatField(required=True, label=mark_safe('Solubility @25&deg;C (mg/L)'), initial=33)
    b_species = forms.ChoiceField(required=True,label='Species of the tested bird', choices=Species_of_the_tested_bird_CHOICES, initial='Make a selection')
    bw_quail = forms.FloatField(required=True,label='Weight of the tested bird (g)', initial= 178)
    bw_duck = forms.FloatField(required=True,label='Weight of the tested bird (g)', initial= 1580)
    bwb_other = forms.FloatField(required=True,label='Weight of the tested bird (g)', initial= 200)
  #  body_weight_of_the_assessed_bird = forms.FloatField(required=True, label='Body weight of assessed bird (g)', initial='8')
    aw_bird = forms.FloatField(required=True, label='Body weight of assessed bird (g)', initial=20)
    ld50_a = forms.FloatField(required=True, label='Avian LD50 (mg/kg-bw)', initial=768)
    NOAEC = forms.FloatField(required=True, label='Avian NOAEC (mg/kg)', initial=225)
    m_species = forms.ChoiceField(required=True,label='Species of the tested mammal', choices=Species_of_the_tested_mamm_CHOICES, initial='Make a selection')
    bw_rat=forms.FloatField(required=True, label='Body weight of the tested mammal (g)', initial=350)
    bwm_other=forms.FloatField(required=True, label='Body weight of the assessed mammal (g)', initial=500)
 #   body_weight_of_the_assessed_mammal = forms.FloatField(required=True, label='Body weight of assessed mammal (kg)', initial='5')
    aw_mamm = forms.FloatField(required=True, label='Body weight of assessed mammal (g)', initial=1000)
    ld50_m = forms.FloatField(required=True, label='Mammalian LD50 (mg/kg-bw)', initial=1100)
    mineau_scaling_factor = forms.FloatField(required=True, label='Mineau scaling factor', initial=1.15)
    NOAEL = forms.FloatField(required=True, label='Mammalian NOAEL (mg/kg-bw)', initial=2.5)
