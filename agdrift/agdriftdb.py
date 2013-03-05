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

Application_method_CHOICES=(('','Make a selection'),('Aerial','Aerial'),('Ground','Ground'),('Orchard/Airblast','Orchard/Airblast'))
Drop_size_distribution_CHOICES=(('','Make a selection'),('Fine','Very fine to fine'),('Medium','Fine to Medium'),('Coarse','Medium to Coarse'))
Boom_height_CHOICES=(('','Make a selection'),('Low','Low'),('High','High'))
Ecosystem_type_CHOICES=(('','Make a selection'),('EPA Pond','EPA Pond'),('Terrestrial', 'Terrestrial')) #Aquatic Assessment
#Waterbody_type_CHOICES=(('','Make a selection'),('EPA Pond','EPA Pond'),('Lake', 'Lake'), ('Watercourse', 'Watercourse')) #Aquatic Assessment
#Orchard_CHOICES=(('','Make a selection'),('Vineyard in leaf','Vineyard in leaf'),('Orchard or dormant vineyard','Orchard or dormant vineyard'))
#Waterbody_type_CHOICES=(('','Make a selection'),('EPA Pond','EPA Pond'),('Lake', 'Lake'), ('Watercourse', 'Watercourse')) #Aquatic Assessment
Orchard_CHOICES=(('','Make a selection'),('Normal','Normal (Stone and Pome Fruit Vineyard)'),('Dense','Dense (Citrus, tall trees)'), ('Sparse', 'Sparse (Young, dormant)'),('Vineyard', 'Vineyard'),('Orchard','Orchard'))

#Extended_settings_CHOICES=(('','Make a selection'),('1','Use default'),('2', 'Enter number of swaths'))
#Assessment_type_CHOICES=(('','Make a selection'),('1','None'),('2', 'Aquatic Assessment'), ('3', 'Terrestrial Assessment'), ('4', 'Spray Block'), ('5', 'Stream Assessment'), ('6', 'Multiple Applications  '))
#Waterbody_type_CHOICES=(('','Make a selection'),('1','EPA Pond'),('2', 'EPA Wetland'), ('3', 'User-Defined'), ('4', 'Spray Block'), ('5', 'Stream Assessment'), ('6', 'Multiple Applications  ')) #Aquatic Assessment
#Field_type_CHOICES=(('','Make a selection'),('1','Point'),('2', 'User Defined')) #Terrestrial Assessment
#definition_CHOICES=(('','Make a selection'),('1','Deposition'),('2', 'Pond integrated deposition')) #Spray Block
#results_CHOICES=(('','Make a selection'),('1','single point'),('2', 'Given times'), ('3','Given distances')) #Stream
class agdriftInp(forms.Form):    
#    waterbody_type = forms.ChoiceField(required=True,label='Water body type', choices=Waterbody_type_CHOICES,initial='Make a selection')
    application_method = forms.ChoiceField(required=True,label='Application Method', choices=Application_method_CHOICES, initial='Make a selection')    
    ecosystem_type = forms.ChoiceField(required=True,label='Ecosystem type', choices=Ecosystem_type_CHOICES,initial='Make a selection')
    drop_size = forms.ChoiceField(required=True,label='Drop Size Distribution', choices=Drop_size_distribution_CHOICES, initial='Make a selection')    
    boom_height = forms.ChoiceField(required=True,label='Boom height', choices=Boom_height_CHOICES, initial='Make a selection')
    orchard_type = forms.ChoiceField(required=True,label='Orchard type', choices=Orchard_CHOICES, initial='Make a selection')
#    extending_settings = forms.ChoiceField(required=True,label='Optional settings', choices=Extended_settings_CHOICES, initial='Make a selection')
#    application_rate = forms.FloatField(required=True,label=mark_safe('Application rate for active ingredient'))
#    assessment_type = forms.ChoiceField(required=True,label='Assessment Type', choices=Assessment_type_CHOICES,initial='Make a selection')
#    width = forms.FloatField(required=True,label=mark_safe('width'))
#    depth = forms.FloatField(required=True,label=mark_safe('depth'))
#    waterbody_type = forms.ChoiceField(required=True,label='Water body type', choices=Waterbody_type_CHOICES,initial='Make a selection')
#    distance_to_waterbody = forms.FloatField(required=True,label=mark_safe('Distance to waterbody from edge of field'))
#    field_definition = forms.ChoiceField(required=True,label='Field Type', choices=Field_type_CHOICES,initial='Make a selection')
#    definition = forms.ChoiceField(required=True,label='Definition',choices=definition_CHOICES, initial='Make a selection')
#    sprayblock_sprayline_length = forms.FloatField(required=True,label=mark_safe('Spray Block Line Length')) #stream
#    sprayblock_turn_around = forms.FloatField(required=True,label=mark_safe('Spray Block Turn Around Time')) #stream
#    stream_width = forms.FloatField(required=True,label=mark_safe('Stream width')) #stream
#    stream_depth = forms.FloatField(required=True,label=mark_safe('Stream depth')) #stream
#    stream_flow_rate = forms.FloatField(required=True,label=mark_safe('Stream flow rate')) #stream
#    stream_flow_speed = forms.FloatField(required=True,label=mark_safe('Stream flow speed')) #stream
#    distance_to_center = forms.FloatField(required=True,label=mark_safe('Distance from edge of field to center of stream')) #stream
#    riparian_interception = forms.FloatField(required=True,label=mark_safe('Riparian interception factor')) #stream
#    instream_decay = forms.FloatField(required=True,label=mark_safe('Instream chemical decay rate')) #stream
#    recharge_rate = forms.FloatField(required=True,label=mark_safe('Recharge rate')) #stream
#    results = forms.ChoiceField(required=True,label='Calculate results at:', choices=results_CHOICES, initial='Make a selection')#stream
#    time_begin = forms.FloatField(required=True,label=mark_safe('Time begin')) #stream
#    time_end = forms.FloatField(required=True,label=mark_safe('Time end')) #stream
#    downstream_distance = forms.FloatField(required=True,label=mark_safe('Downstream distance')) #stream
