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

class leslieInp(forms.Form):
#    N_o = forms.FloatField(required=True,label=mark_safe('Initial amount of individuals'),initial=1)
    T = forms.FloatField(required=True,label='Number of time intervals',initial=10)
    S = forms.ChoiceField(required=True,choices=S_select, label='Number of modeled stages', initial='Please choose')
