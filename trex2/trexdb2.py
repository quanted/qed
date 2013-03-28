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
Applicationtarget_CHOICES=(('Short grass','Short grass'),('Tall grass','Tall grass'),('Broad-leafed plants/small insects','Broad-leafed plants/small insects'),
                           ('Fruits/pods/seeds','Fruits/pods/seeds'), ('Insects','Insects') )
                           
Species_of_the_tested_bird_CHOICES=(('178','Bobwhite quail'),('1580','Mallard duck'),('','Other'))
_Bird_type=['Herbivores and insectivores','Granivores']
_Mammal_type=['Herbivores and insectivores','Granivores']

#class MultiAutoField(forms.MultipleChoiceField):  

#class Car(models.Model):
#    manufacturer = models.ForeignKey('Manufacturer')
        
class trexInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Alachlor')
    Use = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Corn')   
    Formulated_product_name = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='NA')    
    percent_ai=forms.FloatField(required=True, label='% a.i. (%)', initial=100)
    Application_type = forms.ChoiceField(required=True, choices=Applicationtype_CHOICES, initial='Broadcast-Granular')
   #Application_type = forms.MultipleChoiceField(required=True, choices=Applicationtype_CHOICES, widget=forms.CheckboxSelectMultiple)
    Application_target = forms.ChoiceField(required=True, choices=Applicationtarget_CHOICES, initial='Short grass')        
    percent_incorporated = forms.FloatField(required=True, label='% Incorporated (%)',initial=0)
    seed_treatment_formulation_name = forms.CharField(max_length=255, label='Seed treatment formulation name', widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))    
    density_of_product = forms.FloatField(required=True,label='Density of product (lbs/gal)',initial=8.33)
    maximum_seedling_rate_per_use = forms.FloatField(required=True, label='Maximum seeding rate per use (lbs/A)', initial=100)
    row_sp = forms.FloatField(required=True, label='Row spacing (inch)', initial=0)    
    bandwidth = forms.FloatField(required=True, label='Bandwidth (inch)', initial=0)    
# class trexApp(forms.Form):    
    # number_of_applications = forms.FloatField(required=True, label='Number of applications', initial=1)
   # application_rate = forms.FloatField(required=True, label='Granular application rate (lbs a.i./A)',initial=4)
   # application_rate_l = forms.FloatField(required=True,label='Liquid application rate (fl oz/A)', initial=36) #only for LD50-2, 
   # application_rate_per_use = forms.FloatField(required=True, label='Application rate per use (fl oz/cwt)', initial=36)
  #  interval_between_applications = forms.FloatField(required=True, label='Interval between applications (days)', initial=0)


class trexAnimal(forms.Form):    
    Foliar_dissipation_half_life = forms.FloatField(required=True, label='Foliar dissipation half-life (days)', initial=35)
    avian_ld50 = forms.FloatField(required=True, label='Avian LD50 (mg/kg-bw)', initial=1499)
    avian_lc50 = forms.FloatField(required=True, label='Avian LC50 (mg/kg-diet)', initial=5620)
    avian_NOAEC = forms.FloatField(required=True,label='Avian NOAEC (mg/kg-diet)', initial=50)
    avian_NOAEL = forms.FloatField(required=True, label='Avian NOAEL (mg/kg-bw)', initial=10)
   # Bird_type = forms.CharField(required=True, choices=_Bird_type, initial='Herbivores and insectivores')    
    body_weight_of_the_assessed_bird = forms.FloatField(required=True,label='Body weight of assessed bird (g)',initial=20)
    Species_of_the_tested_bird = forms.ChoiceField(required=True,label='Species of the tested bird', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')

    def get_STB_choices(Species_of_the_tested_bird):
        if Species_of_the_tested_bird=='178':
            a33= 178
        elif Species_of_the_tested_bird=='1580':
            a33= 1580
        else:
            a33= 178
        return a33
    

        
    body_weight_of_the_tested_bird=forms.FloatField(required=True, label='Body weight of the tested bird (g)', initial=get_STB_choices(Species_of_the_tested_bird))
    mineau_scaling_factor = forms.FloatField(required=True,label='Mineau scaling factor',initial=1.15)
    mammalian_ld50 = forms.FloatField(required=True, label='Mammalian LD50 (mg/kg-bw)', initial=930)
    mammalian_lc50 = forms.FloatField(required=True, label='Mammalian LC50 (mg/kg-diet)', initial=4000)
    mammalian_NOAEC = forms.FloatField(required=True, label='Mammalian NOAEC (mg/kg-diet)', initial=30)
    mammalian_NOAEL = forms.FloatField(required=True, label='Mammalian NOAEL (mg/kg-bw)', initial=1.5)
  #  Mammal_type = forms.CharField(required=True, choices=_Mammal_type, initial='Herbivores and insectivores')         
    body_weight_of_the_assessed_mammal = forms.FloatField(required=True,label='Body weight of assessed mammal (g)', initial=15)
    body_weight_of_the_tested_mammal = forms.FloatField(required=True,label='Body weight of tested mammal (g)', initial=350)    
    # mass_fraction_of_water_in_the_mammal_food = db.StringProperty(required=True,label='Mass fraction of water in the bird food', initial = 0.5)
    # mass_fraction_of_water_in_the_bird_food = db.StringProperty(required=True,label='Mass fraction of water in the mammal food',initial=0.5)