# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: JHarston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models

class iecInp(forms.Form):
    LC50 = forms.FloatField(required=True,label='Enter LC50 or LD50',initial='1')
    threshold = forms.FloatField(required=True, label='Enter desired threshold',initial='0.25')
    dose_response = forms.FloatField(required=True, label='Enter slope of does-response',initial=4.5)
    