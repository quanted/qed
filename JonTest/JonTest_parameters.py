# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: JHarston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models

class JonTestChem(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Dangerous Chemical X')
    body_weight_of_bird0 = forms.FloatField(required=True,label='Temp Input 0',initial='0')

class JonTestChem0(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Dangerous Chemical Y')
    body_weight_of_bird0 = forms.FloatField(required=True,label='Temp Input 0.0',initial='0.0')

class JonTestChem1(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Dangerous Chemical Y')
    body_weight_of_bird0 = forms.FloatField(required=True,label='Temp Input 0.1',initial='0.1')

class JonTestApp(forms.Form):
    body_weight_of_bird1 = forms.FloatField(required=True,label='Temp Input 1',initial='1')
    body_weight_of_bird2 = forms.FloatField(required=True,label='Temp Input 2',initial='2')

class JonTestCL(forms.Form):
    body_weight_of_bird3 = forms.FloatField(required=True,label='Temp Input 3',initial='3')
    body_weight_of_bird4 = forms.FloatField(required=True,label='Temp Input 4',initial='4')

class JonTestWB(forms.Form):
    body_weight_of_bird5 = forms.FloatField(required=True,label='Temp Input 5',initial='5')
    body_weight_of_bird6 = forms.FloatField(required=True,label='Temp Input 6',initial='6')