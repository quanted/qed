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
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), label='Chemical Name',initial='Alachlor')
    select_receptor = forms.ChoiceField(required=True, choices=SELECT_RECEPTOR, label='Select Receptor', initial='Both')
    application_rate = forms.FloatField(required=True, label='Pesticide Application Rate (lbs ai/A)', initial=3)    
    height_of_direct_spray_column = forms.ChoiceField(required=True, label='Direct Spray Column Height (3.3 m - aerial; 1 m - ground)', choices=SELECT_HEIGHT, initial='3.3')    
    spray_drift = forms.FloatField(required=True, label='Fraction of Spray Inhaled',initial=0.4)
    ddsi = forms.ChoiceField(required=True, label='Direct Spray Inhalation Duration (1.5 min. - aerial; 0.5 min. - ground)', choices=SELECT_DURATION, initial='1.5')
    molecular_weight = forms.FloatField(required=True, label='Molecular Weight',help_text='g/mol',initial=225)   
    vapor_pressure = forms.FloatField(required=True, label='Vapor Pressure',help_text='torr',initial=12)
    avian_oral_ld50 = forms.FloatField(required=True, label=mark_safe('Avian Oral LD<sub>50</sub>'),help_text='mg/kg-bw',initial=8)
    body_weight_of_the_assessed_bird = forms.FloatField(required=True, label='Body Weight of Assessed Bird',help_text='kg',initial=0.8)
    body_weight_of_the_tested_bird = forms.FloatField(required=True, label='Body Weight of Tested Bird',help_text='kg',initial=0.7)
    chemical_specific_mineau_scaling_factor = forms.FloatField(required=True, label='Chemical Specific Mineau Scaling Factor', initial='1.15')
    mammalian_inhalation_lc50 = forms.FloatField(required=True, label=mark_safe('Mammalian LC<sub>50</sub>'),help_text='mg/kg-bw',initial=12)
    duration_of_rat_inhalation_study = forms.FloatField(required=True, label='Duration of Rat Inhalation Study',help_text='hrs',initial=24)
    body_weight_of_the_assessed_mammal = forms.FloatField(required=True, label='Body Weight of Assessed Mammal',help_text='kg',initial=3)
    body_weight_of_the_tested_mammal = forms.FloatField(required=True, label='Body Weight of Tested Mammal',help_text='kg',initial=4)
    rat_inhalation_ld50 = forms.FloatField(required=True, label=mark_safe('Rat Inhalation LD<sub>50</sub>'),help_text='mg/kg-bw',initial=3)
    rat_oral_ld50 = forms.FloatField(required=True, label=mark_safe('Rat Oral LD<sub>50</sub>'),help_text='mg/kg-bw',initial=2)