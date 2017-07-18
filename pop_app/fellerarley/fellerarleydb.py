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

Ite_select =(('1','1'),('5','5'),('10','10'),('20','20'))

class fellerarleyInp(forms.Form):
    N_o = forms.FloatField(required=True,label=mark_safe('Initial amount of individuals (N<sub>0</sub>)'),initial=1)
    rho = forms.FloatField(required=True,label=mark_safe('Probability of birth in a time step (%)'),initial=4)
    beta = forms.FloatField(required=True,label=mark_safe('Probability of death in a time step (%)'),initial=2)   
    T = forms.FloatField(required=True,label='Number of time intervals (T)',initial=100)
    Ite = forms.ChoiceField(required=True,choices=Ite_select, label='Number of iterations', initial=10)
