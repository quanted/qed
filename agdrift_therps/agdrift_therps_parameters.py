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
    #application_rate = forms.FloatField(required=True,label=mark_safe('Active rate (lb/ac)'), initial='0.5')
    aquatic_type = forms.ChoiceField(required=True,label='Aquatic Assessment Type', choices=Aquatic_type_CHOICES, initial='1')    
    calculation_input = forms.ChoiceField(required=True, label = 'Toolbox Input Type', choices=Calculation_input_CHOICES, initial ='Distance')
    distance = forms.FloatField(required=True,label=mark_safe('Distance to water body or terrestrial point from edge of field (ft)'), initial='225')
 #   init_avg_dep_foa = forms.FloatField(required=True,label=mark_safe('Fraction of applied'))
 #   avg_depo_gha = forms.FloatField(required=True,label=mark_safe('Initial Average Deposition (g/ha)'))
 #   avg_depo_lbac = forms.FloatField(required=True,label=mark_safe('Initial Average Deposition (lb/ac)'))
 #   deposition_ngL = forms.FloatField(required=True,label=mark_safe('Initial Average Concentration (ng/L)'))
 #   deposition_mgcm = forms.FloatField(required=True,label=mark_safe('Initial Average Deposiion (mg/cm2)'))


Applicationtype_CHOICES=(('Broadcast-Granular','Broadcast-Granular'),('Row/Band/In-furrow-Granular','Row/Band/In-furrow-Granular'),
                         ('Broadcast-Liquid','Broadcast-Liquid'),('Row/Band/In-furrow-Liquid','Row/Band/In-furrow-Liquid'), ('Seed Treatment', 'Seed Treatment'))
seed_crop_CHOICES=(('33.2', 'corn, all or unspecified'), ('29.6', 'corn, field'), ('22.0', 'corn, pop'), ('33.2', 'corn, sweet'), ('18.9', 'cotton, all or unspecified'), ('18.9', 'cotton, pima'), ('129.0', 'rice'), ('166.7', 'soybean'), ('60.3', 'soybean for edamame'), ('156.0', 'wheat, all or unspecified'), ('136.4', 'wheat, winter'), ('156.0', 'wheat, spring'), ('102.3', 'wheat, hard red winter, dryland'), ('130.0', 'wheat, hard red winter, irrigated'), ('130.0', 'wheat, hard red winter, unspecified'), ('136.4', 'wheat, soft red winter, all'), ('120.0', 'wheat, hard red spring, dryland'), ('156.0', 'wheat, hard red spring, irrigated'), ('156.0', 'wheat, hard red spring, unspecified'), ('85.0', 'wheat, white'), ('120.0', 'wheat, durum'), ('116.0', 'hay or pasture, all or unspecified'), ('35.0', 'perennial legume hay or pasture'), ('15.0', 'alfalfa'), ('9.0', 'birdsfoot trefoil'), ('35.0', 'lespedeza'), ('30.0', 'clover, all or unspecified'), ('9.0', 'clover, alsike'), ('8.0', 'clover, arrowleaf'), ('20.0', 'clover, berseem'), ('30.0', 'clover, crimson'), ('6.0', 'clover, kura'), ('11.0', 'clover, red'), ('20.0', 'clover, rose'), ('5.0', 'clover, white'), ('160.0', 'lupine, all or unspecified'), ('80.0', 'lupine, blue'), ('150.0', 'lupine, narrow leaf'), ('160.0', 'lupine, white'), ('71.0', 'lupine, yellow'), ('9.0', 'crown vetch'), ('25.0', 'perennial grass hay or pasture'), ('25.0', 'festulolium'), ('10.0', 'Kentucky bluegrass'), ('10.0', 'orchard grass'), ('24.0', 'perennial ryegrass'), ('10.0', 'reed canary grass'), ('16.0', 'smooth brome'), ('8.0', 'Bermuda grass'), ('5.0', 'red fescue'), ('15.0', 'tall fescue'), ('8.0', 'timothy'), ('12.0', 'big bluestem'), ('9.0', 'eastern gama grass'), ('12.0', 'indian grass'), ('9.0', 'switch grass'), ('116.0', 'annual grass for forage'), ('24.0', 'annual ryegrass'), ('20.0', 'pearl millet for forage'), ('87.0', 'oats spring, for forage'), ('109.0', 'rye, winter for forage'), ('12.0', 'sorghum for forage'), ('23.0', 'sudan grass for forage'), ('109.0', 'triticale for forage'), ('116.0', 'winter wheat, for forage'), ('10.0', 'teff for forage'), ('10.0', 'asparagus'), ('138.3', 'barley'), ('163.4', 'beans, common or dry'), ('104.8', 'beans, lima'), ('435.6', 'beans, succulent, or green'), ('25.0', 'beets, garden'), ('2.6', 'broccoli'), ('0.4', 'brussels sprouts'), ('72.0', 'buckwheat'), ('2.2', 'cabbage'), ('11.9', 'carrot'), ('0.3', 'cauliflower'), ('50.0', 'cilantro'), ('4.0', 'collards'), ('11.6', 'cucumber'), ('8.0', 'dill weed'), ('100.0', 'ginseng'), ('5.8', 'kale for market'), ('0.8', 'lettuce, all or unspecifed'), ('0.8', 'lettuce, head'), ('0.4', 'lettuce, leaf, Bibb, Boston, or Romaine'), ('30.0', 'millet for feed, all or unspecified'), ('20.0', 'millet for feed, browntop'), ('10.0', 'millet for feed, finger'), ('20.0', 'millet for feed, foxtail'), ('25.0', 'millet for feed, Japanese'), ('15.0', 'millet for feed, pearl'), ('30.0', 'millet for feed, proso'), ('2.2', 'musk melon, all or unspecified'), ('2.2', 'canteloupe'), ('2.2', 'honeydew'), ('2.2', 'casaba'), ('2.2', 'Canary, or Juan Canary'), ('2.2', 'Japanese'), ('2.2', 'Crenshaw'), ('6.0', 'mustard greens'), ('7.0', 'mustard seed'), ('90.0', 'oats'), ('110.0', 'onions, all or unspecified'), ('75.0', 'onions, bulb types except pearl'), ('110.0', 'onions, pearl'), ('4.6', 'onions for seed'), ('75.0', 'onions, bunching (spring or green)'), ('40.0', 'parsley'), ('217.8', 'pea, field'), ('411.0', 'pea, garden'), ('43.6', 'pea, southern'), ('228.3', 'peanut'), ('4.2', 'peppers, all'), ('1.4', 'peppers, bell'), ('4.2', 'peppers, hot (paprika, chili, etc)'), ('6969.6', 'potatoes'), ('4.5', 'pumpkin, all'), ('4.5', 'pumpkin, large or large vine'), ('4.5', 'pumpkin, bush or small fruit/vine'), ('32.7', 'radish'), ('8.2', 'rape'), ('8.2', 'canola'), ('2.0', 'rutabaga'), ('90.0', 'rye'), ('35.0', 'safflower'), ('12.0', 'sesame'), ('9.1', 'sorghum'), ('25.0', 'spinach'), ('8.0', 'squash, all'), ('8.0', 'squash, summer'), ('8.0', 'squash, winter'), ('1.4', 'squash, spagetti'), ('19.8', 'sugar beet for seed production'), ('4.8', 'sugar beet'), ('4.0', 'sunflower'), ('1.1', 'tomatoes'), ('6.0', 'turnip green'), ('1.6', 'turnips'), ('9.1', 'watermelon'))
Species_of_the_tested_bird_CHOICES=(('Bobwhite quail','Bobwhite quail'),('Mallard duck','Mallard duck'),('Other','Other'))

class trexInp_chem(forms.Form):    
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Fluxapyroxad')
    Use = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Dried shelled beans (except soybeans)')   
    Formulated_product_name = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='NA')    
    percent_ai=forms.FloatField(required=True, label='% a.i. (%)', initial=100)
    Foliar_dissipation_half_life = forms.FloatField(required=True, label='Foliar dissipation half-life (days)', initial=35)
    number_of_applications = forms.FloatField(required=True, label='Number of applications', initial=1)
    interval_between_applications = forms.FloatField(required=True, label='Interval between applications (days)', initial=0)
    application_rate = forms.FloatField(required=True, label='Application rate (lbs a.i./A)',initial=0.18)

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

class trexInp_herp(forms.Form):    
    BW_herptile_a_sm = forms.FloatField(required=True, label='Body weight of assessed small herptile (g)', initial=2.0)
    W_p_a_sm = forms.FloatField(required=True, label="Water content of the assessed small herptile's diet (%)", initial=85)
    BW_herptile_a_md = forms.FloatField(required=True, label='Body weight of assessed medium herptile (g)', initial=20)
    W_p_a_md = forms.FloatField(required=True, label="Water content of the assessed medium herptile's diet (%)", initial=85)
    BW_herptile_a_lg = forms.FloatField(required=True, label='Body weight of assessed large herptile (g)', initial=200)
    W_p_a_lg = forms.FloatField(required=True, label="Water content of the assessed large herptile's diet (%)", initial=85)
    body_weight_of_the_consumed_mammal_a = forms.FloatField(required=True,label='Weight of the mammal consumed by assessed frog (g)', initial=15)
    body_weight_of_the_consumed_herp_a = forms.FloatField(required=True,label='Weight of the herptile  consumed by assessed frog (g)', initial=15)

