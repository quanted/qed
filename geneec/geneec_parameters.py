# -*- coding: utf-8 -*-
"""
Crcreated on April 9 14:50:59 2012

@author: Tao Hong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

applicationtarget_CHOICES=(('a','Short grass'),('b','Tall grass'),('c','Broad-leafed plants/small insects'),
                           ('d','Fruits/pods/seeds/large insects')) 

wet_in_CHOICES=(('Yes','Yes'),('No','No'))

applicationmethod_CHOICES=(('','Pick an application method'),('a','Aerial Spray'),('b','Ground Spray'),
                         ('c','Airblast Spray (Orchard & Vineyard)'),('d','Granular (Non-Spray)'))

wet_in_CHOICES=(('Yes','Yes'),('No','No'))

aerial_size_dist_CHOICES=(('a','Very Fine to Fine'),('b','Fine to Medium (EFED Default)'),
                        ('c','Medium to Coarse'),('d','Coarse to Very Coarse')) 

ground_spray_CHOICES=(('a','Low Boom Ground Spray (20" or less)'),
                    ('b','High Boom Ground Spray (20-50"; EFED Default)')) 

spray_quality_CHOICES=(('a','Fine (EFED Default)'),
                    ('b','Medium-Coarse'))  
 
airblast_type_CHOICES=(('a','Orchards and Dormant Vineyards'),
                    ('b','Foliated Vineyards')) 


class GENEECInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    application_target = forms.ChoiceField(required=True, choices=applicationtarget_CHOICES, initial='Short grass')        
    application_rate = forms.FloatField(required=True,label='Application rate (lbs a.i./A)',initial=4)
    number_of_applications = forms.FloatField(required=True,label='Number of applications',initial=5)
    interval_between_applications = forms.FloatField(required=True,label='Interval between applications (days)',initial=6)
    Koc = forms.FloatField(required=True,label=mark_safe('K<sub>OC</sub> (mL/g OC)'),initial=2)   
    aerobic_soil_metabolism = forms.FloatField(required=True,label='Aerobic soil metabolism half-life (days)',initial=7)    
    wet_in = forms.ChoiceField(required=True, choices=wet_in_CHOICES, initial='Yes')        
    
    application_method = forms.ChoiceField(required=True, choices=applicationmethod_CHOICES,initial='Pick an application method')
    #A1
    aerial_size_dist = forms.ChoiceField(required=True, choices=aerial_size_dist_CHOICES, initial='Very Fine to Fine')
    #B1
    ground_spray_type = forms.ChoiceField(required=True, choices=ground_spray_CHOICES, initial='Low Boom Ground Spray (20" or less)')                                          
    #C1
    airblast_type = forms.ChoiceField(required=True, choices=airblast_type_CHOICES, initial='Orchards and Dormant Vineyards')    
    #B2    
    spray_quality = forms.ChoiceField(required=True, choices=spray_quality_CHOICES, initial='Fine (EFED Default)')
    
    no_spray_drift = forms.FloatField(required=True,label='Width of the no-spray zone (feet)',initial=12)    
    incorporation_depth = forms.FloatField(required=True,label='Incorporation Depth (inch)',initial=2)    
    solubility = forms.FloatField(required=True,label='Solubility (mg/L)',initial=3)
    aerobic_aquatic_metabolism = forms.FloatField(required=True,label='Aerobic aquatic metabolism half-life (days)',initial=6)
    hydrolysis = forms.FloatField(required=True,label='Hydrolysis: pH=7/neutral half-life (days)',initial=10)
    photolysis_aquatic_half_life = forms.FloatField(required=True,label='Photolysis, aquatic half-life (days)',initial=11)
        
