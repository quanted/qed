# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: JHarston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

S_select =(('','Please choose'), ('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'))

class lesliedrInp(forms.Form):
    animal_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 17, 'rows': 2}), initial='C. dubia')    
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 17, 'rows': 2}), initial='Spinosad')
    HL = forms.FloatField(required=True,label='Chemical half life (days)',initial=2)
    C = forms.FloatField(required=True,label=mark_safe('Initial concentration (&#956;g/l)'),initial=10)   
    T = forms.FloatField(required=True,label='Simulation durations (days)',initial=10)
    #M_{48} = \frac{1}_{1+e^{-\alpha \times \ln C - \beta}}
    a = forms.FloatField(required=True,label=mark_safe('Logistic model parameter (&#945;)'),initial=0.746)
    b = forms.FloatField(required=True,label=mark_safe('Logistic model parameter (&#946;)'),initial=0.617)
    c = forms.FloatField(required=True,label=mark_safe('Intensity of the density dependence (&#947;)'),initial=0.00548)   
    S = forms.ChoiceField(required=True,choices=S_select, label='Number of age class', initial='Please choose')
