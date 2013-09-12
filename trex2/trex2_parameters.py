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
seed_crop_CHOICES=(('33.2', 'corn, all or unspecified'), ('29.6', 'corn, field'), ('22.0', 'corn, pop'), ('33.2', 'corn, sweet'), ('18.9', 'cotton, all or unspecified'), ('18.9', 'cotton, pima'), ('129.0', 'rice'), ('166.7', 'soybean'), ('60.3', 'soybean for edamame'), ('156.0', 'wheat, all or unspecified'), ('136.4', 'wheat, winter'), ('156.0', 'wheat, spring'), ('102.3', 'wheat, hard red winter, dryland'), ('130.0', 'wheat, hard red winter, irrigated'), ('130.0', 'wheat, hard red winter, unspecified'), ('136.4', 'wheat, soft red winter, all'), ('120.0', 'wheat, hard red spring, dryland'), ('156.0', 'wheat, hard red spring, irrigated'), ('156.0', 'wheat, hard red spring, unspecified'), ('85.0', 'wheat, white'), ('120.0', 'wheat, durum'), ('116.0', 'hay or pasture, all or unspecified'), ('35.0', 'perennial legume hay or pasture'), ('15.0', 'alfalfa'), ('9.0', 'birdsfoot trefoil'), ('35.0', 'lespedeza'), ('30.0', 'clover, all or unspecified'), ('9.0', 'clover, alsike'), ('8.0', 'clover, arrowleaf'), ('20.0', 'clover, berseem'), ('30.0', 'clover, crimson'), ('6.0', 'clover, kura'), ('11.0', 'clover, red'), ('20.0', 'clover, rose'), ('5.0', 'clover, white'), ('160.0', 'lupine, all or unspecified'), ('80.0', 'lupine, blue'), ('150.0', 'lupine, narrow leaf'), ('160.0', 'lupine, white'), ('71.0', 'lupine, yellow'), ('9.0', 'crown vetch'), ('25.0', 'perennial grass hay or pasture'), ('25.0', 'festulolium'), ('10.0', 'Kentucky bluegrass'), ('10.0', 'orchard grass'), ('24.0', 'perennial ryegrass'), ('10.0', 'reed canary grass'), ('16.0', 'smooth brome'), ('8.0', 'Bermuda grass'), ('5.0', 'red fescue'), ('15.0', 'tall fescue'), ('8.0', 'timothy'), ('12.0', 'big bluestem'), ('9.0', 'eastern gama grass'), ('12.0', 'indian grass'), ('9.0', 'switch grass'), ('116.0', 'annual grass for forage'), ('24.0', 'annual ryegrass'), ('20.0', 'pearl millet for forage'), ('87.0', 'oats spring, for forage'), ('109.0', 'rye, winter for forage'), ('12.0', 'sorghum for forage'), ('23.0', 'sudan grass for forage'), ('109.0', 'triticale for forage'), ('116.0', 'winter wheat, for forage'), ('10.0', 'teff for forage'), ('10.0', 'asparagus'), ('138.3', 'barley'), ('163.4', 'beans, common or dry'), ('104.8', 'beans, lima'), ('435.6', 'beans, succulent, or green'), ('25.0', 'beets, garden'), ('2.6', 'broccoli'), ('0.4', 'brussels sprouts'), ('72.0', 'buckwheat'), ('2.2', 'cabbage'), ('11.9', 'carrot'), ('0.3', 'cauliflower'), ('50.0', 'cilantro'), ('4.0', 'collards'), ('11.6', 'cucumber'), ('8.0', 'dill weed'), ('100.0', 'ginseng'), ('5.8', 'kale for market'), ('0.8', 'lettuce, all or unspecifed'), ('0.8', 'lettuce, head'), ('0.4', 'lettuce, leaf, Bibb, Boston, or Romaine'), ('30.0', 'millet for feed, all or unspecified'), ('20.0', 'millet for feed, browntop'), ('10.0', 'millet for feed, finger'), ('20.0', 'millet for feed, foxtail'), ('25.0', 'millet for feed, Japanese'), ('15.0', 'millet for feed, pearl'), ('30.0', 'millet for feed, proso'), ('2.2', 'musk melon, all or unspecified'), ('2.2', 'canteloupe'), ('2.2', 'honeydew'), ('2.2', 'casaba'), ('2.2', 'Canary, or Juan Canary'), ('2.2', 'Japanese'), ('2.2', 'Crenshaw'), ('6.0', 'mustard greens'), ('7.0', 'mustard seed'), ('90.0', 'oats'), ('110.0', 'onions, all or unspecified'), ('75.0', 'onions, bulb types except pearl'), ('110.0', 'onions, pearl'), ('4.6', 'onions for seed'), ('75.0', 'onions, bunching (spring or green)'), ('40.0', 'parsley'), ('217.8', 'pea, field'), ('411.0', 'pea, garden'), ('43.6', 'pea, southern'), ('228.3', 'peanut'), ('4.2', 'peppers, all'), ('1.4', 'peppers, bell'), ('4.2', 'peppers, hot (paprika, chili, etc)'), ('6969.6', 'potatoes'), ('4.5', 'pumpkin, all'), ('4.5', 'pumpkin, large or large vine'), ('4.5', 'pumpkin, bush or small fruit/vine'), ('32.7', 'radish'), ('8.2', 'rape'), ('8.2', 'canola'), ('2.0', 'rutabaga'), ('90.0', 'rye'), ('35.0', 'safflower'), ('12.0', 'sesame'), ('9.1', 'sorghum'), ('25.0', 'spinach'), ('8.0', 'squash, all'), ('8.0', 'squash, summer'), ('8.0', 'squash, winter'), ('1.4', 'squash, spagetti'), ('19.8', 'sugar beet for seed production'), ('4.8', 'sugar beet'), ('4.0', 'sunflower'), ('1.1', 'tomatoes'), ('6.0', 'turnip green'), ('1.6', 'turnips'), ('9.1', 'watermelon'))
Species_of_the_tested_bird_CHOICES=(('Bobwhite quail','Bobwhite quail'),('Mallard duck','Mallard duck'),('Other','Other'))

class trexInp_chem(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Atrazine')
    use = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Corn')   
    Formulated_product_name = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Aatrex')    
    percent_ai=forms.FloatField(required=True, label='% a.i. (%)', initial=42.6)
    Application_type = forms.ChoiceField(required=True, choices=Applicationtype_CHOICES, initial='Broadcast-Liquid')
    percent_incorporated = forms.FloatField(required=True, label='% Incorporated (%)',initial=100)
    seed_treatment_formulation_name = forms.CharField(max_length=255, label='Seed treatment formulation name', widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))    
    seed_crop = forms.ChoiceField(required=True,label='Crop use', choices=seed_crop_CHOICES, initial='Corn')
    seed_crop_v = forms.CharField(required=True, label='Crop use verbal', widget=forms.HiddenInput)
    density_of_product = forms.FloatField(required=True,label='Density of product (lbs/gal)',initial=8.33)
    maximum_seedling_rate_per_use = forms.FloatField(required=True, label='Seeding rate (lbs/acre)', initial=100)
    row_sp = forms.FloatField(required=True, label='Row spacing (inch)', initial=1)    
    bandwidth = forms.FloatField(required=True, label='Bandwidth (inch)', initial=1)
    Foliar_dissipation_half_life = forms.FloatField(required=True, label='Foliar dissipation half-life (days)', initial=35)

class trexInp_bird(forms.Form):
    avian_ld50 = forms.FloatField(required=True, label='Avian LD50 (mg/kg-bw)', initial=768)
    Species_of_the_tested_bird_avian_ld50 = forms.ChoiceField(required=True,label='Test species (for Avian LD50)', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
    bw_avian_ld50 = forms.FloatField(required=True,label='Weight (g)', initial= '178')
    avian_lc50 = forms.FloatField(required=True, label='Avian LC50 (mg/kg-diet)', initial=718)
    Species_of_the_tested_bird_avian_lc50 = forms.ChoiceField(required=True,label='Test species (for Avian LC50)', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
    bw_avian_lc50 = forms.FloatField(required=True,label='Weight (g)', initial= '178')
    avian_NOAEC = forms.FloatField(required=True,label='Avian NOAEC (mg/kg-diet)', initial=225)
    Species_of_the_tested_bird_avian_NOAEC = forms.ChoiceField(required=True,label='Test species (for Avian NOAEC)', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
    bw_avian_NOAEC = forms.FloatField(required=True,label='Weight (g)', initial= '178')
    avian_NOAEL = forms.FloatField(required=True, label='Avian NOAEL (mg/kg-bw)')
    Species_of_the_tested_bird_avian_NOAEL = forms.ChoiceField(required=True,label='Test species (for Avian NOAEL)', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
    bw_avian_NOAEL = forms.FloatField(required=True,label='Weight (g)', initial= '178')
    body_weight_of_the_assessed_bird_small = forms.FloatField(required=True,label='Body weight of assessed bird small (g)',initial=20)
    body_weight_of_the_assessed_bird_medium = forms.FloatField(required=True,label='Body weight of assessed bird medium (g)',initial=100)
    body_weight_of_the_assessed_bird_large = forms.FloatField(required=True,label='Body weight of assessed bird large (g)',initial=1000)
    # Species_of_the_tested_bird = forms.ChoiceField(required=True,label='Species of the tested bird', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
    # bw_quail = forms.FloatField(required=True,label='Weight of the tested bird', initial= '178')
    # bw_duck = forms.FloatField(required=True,label='Weight of the tested bird', initial= '1580')
    # bwb_other = forms.FloatField(required=True,label='Weight of the tested bird', initial= '7')
    mineau_scaling_factor = forms.FloatField(required=True,label='Mineau scaling factor',initial=1.15)

class trexInp_mammal(forms.Form):
    mammalian_ld50 = forms.FloatField(required=True, label='Mammalian LD50 (mg/kg-bw)', initial=1100)
    mammalian_lc50 = forms.FloatField(required=True, label='Mammalian LC50 (mg/kg-diet)')
    mammalian_NOAEC = forms.FloatField(required=True, label='Mammalian NOAEC (mg/kg-diet)', initial=2.5)
    mammalian_NOAEL = forms.FloatField(required=True, label='Mammalian NOAEL (mg/kg-bw)')
    body_weight_of_the_assessed_mammal_small = forms.FloatField(required=True,label='Body weight of assessed mammal small (g)', initial=15)
    body_weight_of_the_assessed_mammal_medium = forms.FloatField(required=True,label='Body weight of assessed mammal medium (g)', initial=35)
    body_weight_of_the_assessed_mammal_large = forms.FloatField(required=True,label='Body weight of assessed mammal large (g)', initial=1000)
    body_weight_of_the_tested_mammal = forms.FloatField(required=True,label='Body weight of tested mammal (g)', initial=350)    
