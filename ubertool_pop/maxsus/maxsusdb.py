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

class maxsusInp(forms.Form):
#    N_o = forms.FloatField(required=True,label=mark_safe('Initial amount of individuals (N<sub>0</sub>)'),initial=100)
    K = forms.FloatField(required=True,label='Carrying capacity (K)',initial=1000)
    rho = forms.FloatField(required=True,label=mark_safe('Initial growth rate in percent (&#961;)'),initial=4)
#    q = forms.FloatField(required=True,label='Catchability (q)', initial=0.4)
#    E = forms.FloatField(required=True,label='Effort (E)',initial=0.4)  
#    T = forms.FloatField(required=True,label='Number of time intervals (T)',initial=200)