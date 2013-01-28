# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: JHarston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models

SELECT_RECEPTOR = (('Avian','Avian'),('Mammalian','Mammalian'),('Both','Both'))

SELECT_HEIGHT = (('3.3','3.3'),('1','1'))

SELECT_DURATION = (('1.5','1.5'),('0.5','0.5'))

class STIRInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    select_receptor = forms.ChoiceField(required=True, choices=SELECT_RECEPTOR, initial='Both')
    application_rate = forms.FloatField(required=True, label='Pesticide Application rate (lbs ai/A)')    
    height_of_direct_spray_column = forms.ChoiceField(required=True, label='Height of Sirect Spray Column (3.3 m for aerial spray or 1 m for ground spray)', choices=SELECT_HEIGHT, initial='3.3')    
    spray_drift = forms.FloatField(required=True, label='Fraction of Spray Inhaled')
    ddsi = forms.ChoiceField(required=True, label='Duration of direct spray inhalation (1.5 minutes for aerial and 0.5 minutes for ground applications)', choices=SELECT_DURATION, initial='1.5')
    molecular_weight = forms.FloatField(required=True, label='Molecular weight (g/mol)')   
    vapor_pressure = forms.FloatField(required=True, label='Vapor Pressure (torr)')
    avian_oral_ld50 = forms.FloatField(required=True, label='Avian Oral LD50 (mg/kg-bw)')
    body_weight_of_the_assessed_bird = forms.FloatField(required=True, label='Body Weight of Assessed Bird (kg)')
    body_weight_of_the_tested_bird = forms.FloatField(required=True, label='Body Weight of Tested Bird (kg)')
    chemical_specific_mineau_scaling_factor = forms.FloatField(required=True, label='Chemical Specific Mineau Scaling Factor', initial='1.15')
    mammalian_inhalation_lc50 = forms.FloatField(required=True, label='Mammalian LC50 (mg/kg-bw)')
    duration_of_rat_inhalation_study = forms.FloatField(required=True, label='Duration of Rat Inhalation Study (hrs)')
    body_weight_of_the_assessed_mammal = forms.FloatField(required=True, label='Body Weight of Assessed Mammal (kg)')
    body_weight_of_the_tested_mammal = forms.FloatField(required=True, label='Body Weight of Tested Mammal (kg)')
    rat_inhalation_ld50 = forms.FloatField(required=True, label='Rat Inhalation LD50 (mg/kg-bw)')
    rat_oral_ld50 = forms.FloatField(required=True, label='Rat Oral LD50 (mg/kg-bw)')