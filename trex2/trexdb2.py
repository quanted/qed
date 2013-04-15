# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 16:13:59 2011

@author: TPurucke
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

Applicationtype_CHOICES=(('Broadcast-Granular','Broadcast-Granular'),('Row/Band/In-furrow-Granular','Row/Band/In-furrow-Granular'),
                         ('Broadcast-Liquid','Broadcast-Liquid'),('Row/Band/In-furrow-Liquid','Row/Band/In-furrow-Liquid'), ('Seed Treatment', 'Seed Treatment'))
#Applicationtarget_CHOICES=(('Short grass','Short grass'),('Tall grass','Tall grass'),('Broad-leafed plants/small insects','Broad-leafed plants/small insects'),
#                           ('Fruits/pods/seeds','Fruits/pods/seeds'), ('Insects','Insects') )                      
seed_crop_CHOICES=(('33.19', 'corn, all or unspecified'), ('27.04', 'corn, field'), ('27.04', 'corn, pop'), ('33.19', 'corn, sweet'), ('150', 'cotton, all or unspecified'), ('13.33', 'cotton, pima'), ('129', 'rice'), ('166.67', 'soybean'), ('104.5', 'soybean for edamame'), ('157.1', 'wheat, all or unspecified'), ('157', 'wheat, winter'), ('156', 'wheat, spring'), ('120', 'wheat, hard red winter, dryland'), ('130', 'wheat, hard red winter, irrigated'), ('130', 'wheat, hard red winter, unspecified'), ('157.1', 'wheat, soft red winter, all'), ('120', 'wheat, hard red spring, dryland'), ('146', 'wheat, hard red spring, irrigated'), ('146', 'wheat, hard red spring, unspecified'), ('156', 'wheat, white'), ('156', 'wheat, durum'), ('116', 'hay or pasture, all or unspecified'), ('35', 'perennial legume hay or pasture'), ('90', 'alfalfa'), ('15', 'birdsfoot trefoil'), ('35', 'lespedeza'), ('30', 'clover, all or unspecified'), ('9', 'clover, alsike'), ('8', 'clover, arrowleaf'), ('20', 'clover, berseem'), ('20', 'clover, crimson'), ('30', 'clover, kura'), ('6', 'clover, red'), ('11', 'clover, rose'), ('20', 'clover, white'), ('160', 'lupine, all or unspecified'), ('80', 'lupine, blue'), ('150', 'lupine, narrow leaf'), ('160', 'lupine, white'), ('71', 'lupine, yellow'), ('5', 'crown vetch'), ('30', 'perennial grass hay or pasture'), ('30', 'festulolium'), ('25', 'Kentucky bluegrass'), ('10', 'orchard grass'), ('10', 'perennial ryegrass'), ('24', 'reed canary grass'), ('10', 'smooth brome'), ('16', 'Bermuda grass'), ('8', 'red fescue'), ('5', 'tall fescue'), ('15', 'timothy'), ('8', 'big bluestem'), ('12', 'eastern gama grass'), ('9', 'indian grass'), ('12', 'switch grass'), ('116', 'annual grass for forage'), ('9', 'annual ryegrass'), ('24', 'pearl millet for forage'), ('20', 'oats spring, for forage'), ('87', 'rye, winter for forage'), ('109', 'sorghum for forage'), ('24', 'sudan grass for forage'), ('23', 'triticale for forage'), ('109', 'winter wheat, for forage'), ('116', 'teff for forage'), ('10', 'asparagus'), ('138.3', 'barley'), ('140.01', 'beans, common or dry'), ('163.35', 'beans, lima'), ('213.53', 'beans, succulent, or green'), ('435.6', 'beets, garden'), ('25', 'broccoli'), ('0.44', 'brussels sprouts'), ('0.15', 'buckwheat'), ('72', 'cabbage'), ('11.95', 'carrot'), ('5.69', 'cauliflower'), ('0.18', 'cilantro'), ('50', 'collards'), ('11.62', 'cucumber'), ('5.81', 'dill weed'), ('8', 'ginseng'), ('100', 'kale for market'), ('0.98', 'lettuce, all or unspecifed'), ('0.78', 'lettuce, head'), ('0.39', 'lettuce, leaf, Bibb, Boston, or Romaine'), ('71', 'millet for feed, all or unspecified'), ('71', 'millet for feed, browntop'), ('20', 'millet for feed, finger'), ('10', 'millet for feed, foxtail'), ('20', 'millet for feed, Japanese'), ('25', 'millet for feed, pearl'), ('15', 'millet for feed, proso'), ('0.8', 'musk melon, all or unspecified'), ('0.8', 'canteloupe'), ('0.8', 'honeydew'), ('0.8', 'casaba'), ('0.8', 'Canary, or Juan Canary'), ('0.8', 'Japanese'), ('0.8', 'Crenshaw'), ('6', 'mustard greens'), ('4', 'mustard seed'), ('7', 'oats'), ('110', 'onions, all or unspecified'), ('75', 'onions, bulb types except pearl'), ('110', 'onions, pearl'), ('4.59', 'onions for seed'), ('75', 'onions, bunching (spring or green)'), ('40', 'parsley'), ('217.8', 'pea, field'), ('411', 'pea, garden'), ('275', 'pea, southern'), ('228.26', 'peanut'), ('170', 'peppers, all'), ('170', 'peppers, bell'), ('4.18', 'peppers, hot (paprika, chili, etc)'), ('6969.6', 'potatoes'), ('4.54', 'pumpkin, all'), ('4.54', 'pumpkin, large or large vine'), ('4.54', 'pumpkin, bush or small fruit/vine'), ('8.01', 'squash, all'), ('6.1', 'squash, summer'), ('3.8', 'squash, winter'), ('3.78', 'squash, spagetti'), ('32.67', 'radish'), ('30.63', 'rape'), ('30.63', 'canola'), ('7.74', 'rutabaga'), ('2', 'rye'), ('90', 'safflower'), ('35', 'sesame'), ('12', 'sorghum'), ('60.31', 'spinach'), ('25', 'sugar beet for seed production'), ('25', 'sugar beet'), ('1.82', 'sunflower'), ('6.3', 'turnip green'), ('4', 'tomatoes'), ('1.57', 'turnips'), ('9.08', 'watermelon'))
Species_of_the_tested_bird_CHOICES=(('178','Bobwhite quail'),('1580','Mallard duck'),('','Other'))
#_Bird_type=['Herbivores and insectivores','Granivores']
#_Mammal_type=['Herbivores and insectivores','Granivores']
#class MultiAutoField(forms.MultipleChoiceField):  
        
#class trexInp(forms.Form):
class trexInp_chem(forms.Form):    
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Alachlor')
    Use = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Corn')   
    Formulated_product_name = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='NA')    
    percent_ai=forms.FloatField(required=True, label='% a.i. (%)', initial=100)
    Application_type = forms.ChoiceField(required=True, choices=Applicationtype_CHOICES, initial='Broadcast-Granular')
   #Application_type = forms.MultipleChoiceField(required=True, choices=Applicationtype_CHOICES, widget=forms.CheckboxSelectMultiple)
 #   Application_target = forms.ChoiceField(required=True, choices=Applicationtarget_CHOICES, initial='Short grass')        
    percent_incorporated = forms.FloatField(required=True, label='% Incorporated (%)',initial=0)
    seed_treatment_formulation_name = forms.CharField(max_length=255, label='Seed treatment formulation name', widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))    
    seed_crop = forms.ChoiceField(required=True,label='Crop use', choices=seed_crop_CHOICES, initial='Corn')
    density_of_product = forms.FloatField(required=True,label='Density of product (lbs/gal)',initial=8.33)
    maximum_seedling_rate_per_use = forms.FloatField(required=True, label='Maximum seeding rate per use (lbs/A)', initial=100)
    row_sp = forms.FloatField(required=True, label='Row spacing (inch)', initial=0)    
    bandwidth = forms.FloatField(required=True, label='Bandwidth (inch)', initial=0)
    Foliar_dissipation_half_life = forms.FloatField(required=True, label='Foliar dissipation half-life (days)', initial=35)
# class trexApp(forms.Form):    
    # number_of_applications = forms.FloatField(required=True, label='Number of applications', initial=1)
   # application_rate = forms.FloatField(required=True, label='Granular application rate (lbs a.i./A)',initial=4)
   # application_rate_l = forms.FloatField(required=True,label='Liquid application rate (fl oz/A)', initial=36) #only for LD50-2, 
   # application_rate_per_use = forms.FloatField(required=True, label='Application rate per use (fl oz/cwt)', initial=36)
  #  interval_between_applications = forms.FloatField(required=True, label='Interval between applications (days)', initial=0)
class trexInp_bird(forms.Form):    
    avian_ld50 = forms.FloatField(required=True, label='Avian LD50 (mg/kg-bw)', initial=1499)
    avian_lc50 = forms.FloatField(required=True, label='Avian LC50 (mg/kg-diet)', initial=5620)
    avian_NOAEC = forms.FloatField(required=True,label='Avian NOAEC (mg/kg-diet)', initial=50)
    avian_NOAEL = forms.FloatField(required=True, label='Avian NOAEL (mg/kg-bw)', initial=10)
   # Bird_type = forms.CharField(required=True, choices=_Bird_type, initial='Herbivores and insectivores')    
    body_weight_of_the_assessed_bird_small = forms.FloatField(required=True,label='Body weight of assessed bird small (g)',initial=20)
    body_weight_of_the_assessed_bird_medium = forms.FloatField(required=True,label='Body weight of assessed bird medium (g)',initial=100)
    body_weight_of_the_assessed_bird_large = forms.FloatField(required=True,label='Body weight of assessed bird large (g)',initial=1000)
    Species_of_the_tested_bird = forms.ChoiceField(required=True,label='Species of the tested bird', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')

    def get_STB_choices(Species_of_the_tested_bird):
        if Species_of_the_tested_bird=='178':
            a33= 178
        elif Species_of_the_tested_bird=='1580':
            a33= 1580
        else:
            a33= 178
        return a33
    bw_quail = forms.FloatField(required=True,label='Weight of the tested bird', initial= '178')
    bw_duck = forms.FloatField(required=True,label='Weight of the tested bird', initial= '1580')
    bwb_other = forms.FloatField(required=True,label='Weight of the tested bird', initial= '7')
    #body_weight_of_the_tested_bird=forms.FloatField(required=True, label='Body weight of the tested bird (g)', initial=get_STB_choices(Species_of_the_tested_bird))
    mineau_scaling_factor = forms.FloatField(required=True,label='Mineau scaling factor',initial=1.15)
class trexInp_mammal(forms.Form):  
    mammalian_ld50 = forms.FloatField(required=True, label='Mammalian LD50 (mg/kg-bw)', initial=930)
    mammalian_lc50 = forms.FloatField(required=True, label='Mammalian LC50 (mg/kg-diet)', initial=4000)
    mammalian_NOAEC = forms.FloatField(required=True, label='Mammalian NOAEC (mg/kg-diet)', initial=30)
    mammalian_NOAEL = forms.FloatField(required=True, label='Mammalian NOAEL (mg/kg-bw)', initial=1.5)
  #  Mammal_type = forms.CharField(required=True, choices=_Mammal_type, initial='Herbivores and insectivores')         
    body_weight_of_the_assessed_mammal_small = forms.FloatField(required=True,label='Body weight of assessed mammal small (g)', initial=15)
    body_weight_of_the_assessed_mammal_medium = forms.FloatField(required=True,label='Body weight of assessed mammal medium (g)', initial=35)
    body_weight_of_the_assessed_mammal_large = forms.FloatField(required=True,label='Body weight of assessed mammal large (g)', initial=1000)

    body_weight_of_the_tested_mammal = forms.FloatField(required=True,label='Body weight of tested mammal (g)', initial=350)    
    # mass_fraction_of_water_in_the_mammal_food = db.StringProperty(required=True,label='Mass fraction of water in the bird food', initial = 0.5)
    # mass_fraction_of_water_in_the_bird_food = db.StringProperty(required=True,label='Mass fraction of water in the mammal food',initial=0.5)