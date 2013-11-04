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

class agdriftInp(forms.Form):    
#    waterbody_type = forms.ChoiceField(required=True,label='Water body type', choices=Waterbody_type_CHOICES,initial='Make a selection')
    application_method = forms.ChoiceField(required=True,label='Application Method', choices=Application_method_CHOICES, initial='Make a selection')    
    ecosystem_type = forms.ChoiceField(required=True,label='Ecosystem type', choices=Ecosystem_type_CHOICES,initial='Make a selection')
    drop_size = forms.ChoiceField(required=True,label='Drop Size Distribution', choices=Drop_size_distribution_CHOICES, initial='Make a selection')    
    boom_height = forms.ChoiceField(required=True,label='Boom height', choices=Boom_height_CHOICES, initial='Make a selection')
    orchard_type = forms.ChoiceField(required=True,label='Orchard type', choices=Orchard_CHOICES, initial='Make a selection')
#    extending_settings = forms.ChoiceField(required=True,label='Optional settings', choices=Extended_settings_CHOICES, initial='Make a selection')
    application_rate = forms.FloatField(required=True,label=mark_safe('Active rate (lb/ac)'))
    distance_aqua = forms.FloatField(required=True,label=mark_safe('Distance to water body from edge of field (ft)'))
    distance_terr = forms.FloatField(required=True,label=mark_safe('Distance to point or area average from edge of field (ft)'))
    aquatic_type = forms.ChoiceField(required=True,label='Aquatic Assessment Type', choices=Aquatic_type_CHOICES, initial='Make a selection')    

