# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: MSnyder
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models

class beekhouryInp(forms.Form):
    w = forms.FloatField(required=True,label='Egg laying rate factor', initial=20000)
    alpha = forms.FloatField(required=True,label='Alpha', initial=0.25)
    theta = forms.FloatField(required=True,label='Theta', initial=0.75)
    l = forms.FloatField(required=True,label='Daily laying rate', initial=2000)
    mo = forms.FloatField(required=True,label='Background mortality', initial=0.154)
    deltam = forms.FloatField(required=True,label='Forager mortality', initial=0.15)
    no = forms.FloatField(required=True,label='Colony Size', initial=10000)
    t = forms.FloatField(required=True,label='Number of days', initial=200)
