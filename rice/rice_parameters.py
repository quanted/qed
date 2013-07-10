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
# from google.appengine.api import users
# import datetime

class RiceInp(forms.Form):
    # config_name = forms.CharField(label="Use Configuration Name", initial="use-config-%s"%datetime.datetime.now())     
	chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), initial='Fipronil')
	mai = forms.FloatField(required=True,label='Mass of Applied Ingredient to Paddy (kg)', initial=0.056)
	area = forms.FloatField(required=True,label=mark_safe('Area of the Rice Paddy (m<sup>2</sup>)'), initial=10000)
	dsed = forms.FloatField(required=True,label='Sediment Depth (m)', initial=0.01)
	pb = forms.FloatField(required=True,label=mark_safe('Bulk Density of Sediment, &#961;<sub>b</sub> (kg/m<sup>3</sup>)'), initial=1300)
	dw = forms.FloatField(required=True,label='Water Column Depth (m)', initial=0.10)
	osed = forms.FloatField(required=True,label=mark_safe('Porosity of Sediment, K<sub>d</sub>'), initial=0.509)
	Kd = forms.FloatField(required=True,label=mark_safe('Water-Sediment Partitioning Coefficient, K<sub>oc</sub> (L/kg)'), initial=727)
