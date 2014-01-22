# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

SELECT_METHOD = (('Granular','Granular'),('Foliar Spray','Foliar Spray'),('Bare Ground Spray','Bare Ground Spray'))
#AvianDermalType_CHOICES=(('With DTI','With DTI'),('With DTI 90% CI', 'With DTI 90% CI'),('Without DTI','Without DTI'))

class DustInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), label='Chemical Name',initial='Aliphatic Alcohols')
    label_epa_reg_no = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),label='Label EPA Reg. No.',initial='79038')
    #pest_app_method = forms.ChoiceField(choices=SELECT_METHOD, label=mark_safe('Select Pesticide Application Method'),initial='Granular')
    application_rate = forms.FloatField(required=True,label='Maximum Single Application Rate',initial=15.73, help_text='lbs ai/A')
    frac_pest_assumed_at_surface = forms.DecimalField(required=True,label='Fraction of Pesticide Assumed at Surface',initial=.3,help_text='Decimal [0-1]')
    dislodgeable_foliar_residue = forms.FloatField(required=True,label='Dislodgeable Foliar Residue',initial=5, help_text='mg a.i./cm<sup>2</sup>')
    bird_acute_oral_study = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),label='Bird Acute Oral Study (OCSPP 850.2100) MRID#',initial='A304')
    bird_study_add_comm = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),label='Additional Comments About Bird Study (if any)',initial='NA')
    low_bird_acute_oral_ld50 = forms.FloatField(required=True,label=mark_safe('Lowest Bird Acute Oral LD<sub>50</sub> &asymp; Amphibian Dermal LD<sub>50</sub>'),initial=4640,help_text='mg a.i./kg-bw')
    tested_bird_body_weight = forms.FloatField(required=True,label='Tested Bird Body Weight',initial=1580,help_text='g')
    mineau_scaling_factor = forms.FloatField(required=True,label='Mineau Scaling Factor for Birds',initial='1.15')
    mamm_acute_derm_study = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), label='Mammal Acute Dermal (OCSPP 870.1200) MRID#',initial='B202')
    mamm_study_add_comm = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),label='Additional Comments About Mammal Study (if any)',initial='NA')
    mamm_acute_derm_ld50 = forms.FloatField(required=True,label=mark_safe('Mammal Acute Dermal LD<sub>50</sub>'),initial=2000,help_text='mg a.i./kg-bw')
    #aviandermaltype = forms.ChoiceField(required=True, choices=AvianDermalType_CHOICES, initial='With DTI', label='Avian Dermal type')
    mam_acute_oral_ld50 = forms.FloatField(required=True,label=mark_safe('Mammal Acute Oral LD<sub>50</sub>'),initial=3920,help_text='mg a.i./kg-bw')
    tested_mamm_body_weight = forms.FloatField(required=True,label='Tested Mammal Body Weight',initial=350,help_text='g')
