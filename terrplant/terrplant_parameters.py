# -*- coding: utf-8 -*-
"""

"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

SELECT_INCORPORATION = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'))

SELECT_DRIFT = (('0.01','0.01'),('0.05','0.05'),('0','0'))

SELECT_RUN = (('0.01','0.01'),('0.02','0.02'),('0.05','0.05'))

SELECT_VERSION = (('1.2.2','1.2.2'),)

class TerrPlantInp(forms.Form):
    version_terrplant = forms.ChoiceField(required=True, choices=SELECT_VERSION, label='Version',initial='1.2.2')
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),label='Chemical Name',initial='Alachlor')
    pc_code = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), label='PC Code',initial='90501')
    use = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), label='Use',initial='Corn')
    application_method = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), label='Application Method',initial='Ground')
    application_form = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), label='Application Form',initial='Spray')
    solubility = forms.FloatField(label='Solubility',initial=240)
    incorporation = forms.ChoiceField(required=True, choices=SELECT_INCORPORATION, label='Incorporation Depth (in)')    
    application_rate = forms.FloatField(required=True,label='Application rate (lbs ai/A)',initial=4)    
    drift_fraction = forms.ChoiceField(required=True, choices=SELECT_DRIFT, label='Drift Fraction',initial=0.01)
    runoff_fraction = forms.ChoiceField(required=True, choices=SELECT_RUN, label='Runoff Fraction',initial=0.05)
    EC25_for_nonlisted_seedling_emergence_monocot = forms.FloatField(required=True, label=mark_safe('EC<sub>25</sub> for Non-listed Seedling Emergence Monocot'),initial=0.0067)
    EC25_for_nonlisted_seedling_emergence_dicot = forms.FloatField(required=True, label=mark_safe('EC<sub>25</sub> for Non-listed Seedling Emergence Dicot'),initial=0.034)
    NOAEC_for_listed_seedling_emergence_monocot = forms.FloatField(required=True, label=mark_safe('NOAEC for Non-listed Seedling Emergence Monocot'),initial=0.0023)
    NOAEC_for_listed_seedling_emergence_dicot = forms.FloatField(required=True, label=mark_safe('NOAEC for Non-listed Seedling Emergence Dicot'),initial=0.019)
    EC25_for_nonlisted_vegetative_vigor_monocot = forms.FloatField(label=mark_safe('EC<sub>25</sub> for Non-listed Vegetative Vigor Monocot'),initial=0.068)
    EC25_for_nonlisted_vegetative_vigor_dicot = forms.FloatField(label=mark_safe('EC<sub>25</sub> for Non-listed Vegetative Vigor Dicot'),initial=1.4)
    NOAEC_for_listed_vegetative_vigor_monocot = forms.FloatField(label=mark_safe('NOAEC for Non-listed Vegetative Vigor Monocot'),initial=0.037)
    NOAEC_for_listed_vegetative_vigor_dicot = forms.FloatField(label=mark_safe('NOAEC for Non-listed Vegetative Vigor Dicot'),initial=0.67)