# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

SELECT_METHOD = (('Granular','Granular'),('Foliar Spray','Foliar Spray'),('Bare Ground Spray','Bare Ground Spray'))

class DustInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), label='Chemical Name')
    label_epa_reg_no = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),label='Label EPA Reg. No.')
    pest_app_method = forms.ChoiceField(choices=SELECT_METHOD, label=mark_safe('Select Pesticide Application Method'),initial='Granular')
    application_rate = forms.FloatField(required=True,label='Maximum Single Application Rate (lbs ai/A)')
    frac_pest_assumed_at_surface = forms.FloatField(required=True,label='Fraction of Pesticide Assumed at Surface (decimal expression)')
    dislodgeable_foliar_residue = forms.FloatField(required=True,label=mark_safe('Dislodgeable Foliar Residue (mg a.i./cm<sup>2</sup>)'))
    bird_acute_oral_study = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),label='Bird Acute Oral Study (OCSPP 850.2100) MRID#')
    bird_study_add_comm = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),label='Additional Comments About Bird Study (if any)')
    low_bird_acute_oral_ld50 = forms.FloatField(required=True,label=mark_safe('Lowest Bird Acute Oral LD<sub>50</sub> &asymp; Amphibian Dermal LD<sub>50</sub> (mg a.i./kg-bw) '))
    tested_bird_body_weight = forms.FloatField(required=True,label='Tested Bird Body Weight (g)')
    mineau = forms.FloatField(required=True,label='Mineau Scaling Factor for Birds',initial='1.15')
    mamm_acute_derm_study = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), label='Mammal Acute Dermal (OCSPP 870.1200) MRID#')
    mamm_study_add_comm = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),label='Additional Comments About Mammal Study (if any)')
    mamm_acute_derm_ld50 = forms.FloatField(required=True,label=mark_safe('Mammal Acute Dermal LD<sub>50</sub> (mg a.i./kg-bw)'))
    tested_mamm_body_weight = forms.FloatField(required=True,label='Tested Mammal Body Weight (g)')
