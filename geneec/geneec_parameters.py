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

applicationtarget_CHOICES=(('Short grass','Short grass'),('Tall grass','Tall grass'),('Broad-leafed plants/small insects','Broad-leafed plants/small insects'),
                           ('Fruits/pods/seeds/large insects','Fruits/pods/seeds/large insects')) 

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
        
#APPRAT,APPNUM,APSPAC,KOC,METHAF,WETTED,METHOD,
#     AIRFLG,YLOCEN,GRNFLG,GRSIZE,ORCFLG,INCORP,SOL,METHAP,HYDHAP,
#     FOTHAP
     
#                 #1  2,  3, 4 ,5,  6,   7,   8,   9,  10,  11,  12, 13, 14, 15, 16,17)
#a=geneec1.geneec2(4, 10, 5, 10, 3, 'n', 'a', 'd', 10, 'a', 'b', 'b', 1, 0.01, 2, 2, 20)

#1.APPRAT,  APPLICATION RATE
#2.APPNUM,  MAXIMUM NUMBER OF APPLICATION PERMITTED ON LABEL
#3.APSPAC,  INTERVAL IN DAYS BETWEEN PESTICIDE APPLICATIONS
#4.KOC,     ORGANIC CARBON PARTITION COEFFICIENT
#5.METHAF,  AEROBIC METABOLIC SOIL HALFLIFE
#6.WETTED,  FLAG TO INDICATE THE PESTICIDE IS WETTED-IN AND RUNOFF
#7.METHOD,  Application approach
#8.AIRFLG,  FLAG TO INDICATE AERIAL DROPLET SIZE DISTRIBUTION
#9.YLOCEN,  DISTANCE FROM EDGE OF DOWNWIND SWATH TO NEAR EDGE OF POND IN ENGLISH UNITS (FEET)
#10.GRNFLG, FLAG TO INDICATE GROUND SPRAYER TYPE
#11.GRSIZE, SPRAY QUALITY (DROPLET SIZE DISTRIBUTION)
#12.ORCFLG, FLAG TO INDICATE TYPE OF ORCHARD AIRBLAST APPLICATION
#13.INCORP, DEPTH OF INCORPORATION
#14.SOL,    SOLUBILITY
#15.METHAP, AEROBIC METABOLIC HALFLIFE IN THE POND
#16.HYDHAP, HYDROLYSIS HALFLIFE IN THE POND
#17.FOTHAP, PHOTOLYSIS HALFLIFE IN THE POND = NOMINAL HALF-LIFE / 124      
