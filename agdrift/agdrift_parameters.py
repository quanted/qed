# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: MSnyder
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

Application_method_CHOICES=(('','Make a selection'),('Aerial','Tier I Aerial'),('Ground','Tier I Ground'),('Orchard/Airblast','Tier I Orchard/Airblast'))
Drop_size_distribution_CHOICES=(('','Make a selection'),('Fine','Very fine to fine'),('Medium','Fine to Medium'),('Coarse','Medium to Coarse'), ('Very Coarse','Coarse to Very Coarse'))
Boom_height_CHOICES=(('','Make a selection'),('Low','Low'),('High','High'))
Ecosystem_type_CHOICES=(('','Make a selection'),('EPA Pond','Aquatic Assessment'),('Terrestrial', 'Terrestrial Assessment')) #Aquatic Assessment
#Waterbody_type_CHOICES=(('','Make a selection'),('EPA Pond','EPA Pond'),('Lake', 'Lake'), ('Watercourse', 'Watercourse')) #Aquatic Assessment
#Orchard_CHOICES=(('','Make a selection'),('Vineyard in leaf','Vineyard in leaf'),('Orchard or dormant vineyard','Orchard or dormant vineyard'))
#Waterbody_type_CHOICES=(('','Make a selection'),('EPA Pond','EPA Pond'),('Lake', 'Lake'), ('Watercourse', 'Watercourse')) #Aquatic Assessment
Orchard_CHOICES=(('','Make a selection'),('Normal','Normal (Stone and Pome Fruit Vineyard)'),('Dense','Dense (Citrus, tall trees)'), ('Sparse', 'Sparse (Young, dormant)'),('Vineyard', 'Vineyard'),('Orchard','Orchard'))
Aquatic_type_CHOICES=(('','Make a selection'),('1','EPA Defined Pond'),('2', 'EPA Defined Wetland'))
Calculation_input_CHOICES=(('','Make a selection'), ('Distance','Distance to waterbody or field'), ('Fraction','Fraction of applied'),('Initial Average Deposition (g/ha)','Initial Average Deposition (g/ha)'),('Initial Average Deposition (lb/ac)', 'Initial Average Deposition (lb/ac)'),('Initial Average Concentration (ng/L)', 'Initial Average Concentration (ng/L)'), ('Initial Average Deposiion (mg/cm2)','Initial Average Deposition (mg/cm2)'))
class agdriftInp(forms.Form):    
#    waterbody_type = forms.ChoiceField(required=True,label='Water body type', choices=Waterbody_type_CHOICES,initial='Make a selection')
    application_method = forms.ChoiceField(required=True,label='Application Method', choices=Application_method_CHOICES, initial='Make a selection')    
    ecosystem_type = forms.ChoiceField(required=True,label='Ecosystem type', choices=Ecosystem_type_CHOICES,initial='EPA Pond')
    drop_size = forms.ChoiceField(required=True,label='Drop Size Distribution', choices=Drop_size_distribution_CHOICES, initial='Medium')    
    boom_height = forms.ChoiceField(required=True,label='Boom height', choices=Boom_height_CHOICES, initial='High')
    orchard_type = forms.ChoiceField(required=True,label='Orchard type', choices=Orchard_CHOICES, initial='Orchard')
#    extending_settings = forms.ChoiceField(required=True,label='Optional settings', choices=Extended_settings_CHOICES, initial='Make a selection')
    application_rate = forms.FloatField(required=True,label=mark_safe('Active rate (lb/ac)'), initial='0.5')
    aquatic_type = forms.ChoiceField(required=True,label='Aquatic Assessment Type', choices=Aquatic_type_CHOICES, initial='1')    
    calculation_input = forms.ChoiceField(required=True, label = 'Toolbox Input Type', choices=Calculation_input_CHOICES, initial ='Distance')
    distance = forms.FloatField(required=True,label=mark_safe('Distance to water body or terrestrial point from edge of field (ft)'), initial='225')
 #   init_avg_dep_foa = forms.FloatField(required=True,label=mark_safe('Fraction of applied'))
 #   avg_depo_gha = forms.FloatField(required=True,label=mark_safe('Initial Average Deposition (g/ha)'))
 #   avg_depo_lbac = forms.FloatField(required=True,label=mark_safe('Initial Average Deposition (lb/ac)'))
 #   deposition_ngL = forms.FloatField(required=True,label=mark_safe('Initial Average Concentration (ng/L)'))
 #   deposition_mgcm = forms.FloatField(required=True,label=mark_safe('Initial Average Deposiion (mg/cm2)'))



