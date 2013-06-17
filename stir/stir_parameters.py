# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

SELECT_RECEPTOR = (('Avian','Avian'),('Mammalian','Mammalian'),('Both','Both'))

SELECT_HEIGHT = (('3.3','3.3'),('1','1'))

SELECT_DURATION = (('1.5','1.5'),('0.5','0.5'))

class STIRInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), label='Chemical Name',initial='Quinoxyfen')
    application_rate = forms.FloatField(required=True, label='Pesticide Application Rate (lbs ai/A)', initial=0.107)    
    column_height = forms.ChoiceField(required=True, label='Direct Spray Column Height (3.3 m - aerial; 1 m - ground)', choices=SELECT_HEIGHT, initial='3.3')    
    spray_drift_fraction = forms.FloatField(required=True, label='Fraction of Spray Inhaled',initial=0.9)
    direct_spray_duration = forms.ChoiceField(required=True, label='Direct Spray Inhalation Duration (1.5 min. - aerial; 0.5 min. - ground)', 
        choices=SELECT_DURATION, initial='1.5')
    molecular_weight = forms.FloatField(required=True, label='Molecular Weight',help_text='g/mol',initial=308.14)   
    vapor_pressure = forms.FloatField(required=True, label='Vapor Pressure',help_text='mmHg',initial=9.e-8)
    avian_oral_ld50 = forms.FloatField(required=True, label=mark_safe('Lowest Avian Oral LD<sub>50</sub>'),help_text='mg/kg-bw',initial=2292.)
    body_weight_assessed_bird = forms.FloatField(required=True, label='Body Weight of Assessed Bird',help_text='kg',initial=0.02)
    body_weight_tested_bird = forms.FloatField(required=True, label='Body Weight of Tested Bird',help_text='kg',initial=0.178)
    mineau_scaling_factor = forms.FloatField(required=True, label='Chemical Specific Mineau Scaling Factor', initial='1.15')
    mammal_inhalation_lc50 = forms.FloatField(required=True, label=mark_safe('Lowest Mammal (Rat) Inhalation LC<sub>50</sub>'),help_text='mg/kg-bw',initial=3.38)
    duration_mammal_inhalation_study = forms.FloatField(required=True, label='Duration of Mammal (Rat) Inhalation Study',help_text='hrs',initial=4.)
    body_weight_assessed_mammal = forms.FloatField(required=True, label='Body Weight of Assessed Mammal',help_text='kg',initial=0.015)
    body_weight_tested_mammal = forms.FloatField(required=True, label='Body Weight of Tested Mammal',help_text='kg',initial=0.35)
    mammal_oral_ld50 = forms.FloatField(required=True, label=mark_safe('Lowest Mammal (Rat) Oral LD<sub>50</sub>'),help_text='mg/kg-bw',initial=5000.)