# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

@author: jharston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
import sys
sys.path.append('../CAS')
from CAS.CASGql import CASGql
from google.appengine.api import users
from google.appengine.ext import db
import logging
import datetime

APPLICATIONTYPE = (('broadcast','broadcast'),('row/band/in-furrow','row/band/in-furrow'))
APPTYPE = (('liquid','liquid'),('granular','granular'))
YN = (('Yes','Yes'),('No','No'))

class Use_metadataInp(forms.Form):
    user_use_configuration = forms.ChoiceField(label="User Saved Use Configuration",required=True)
    config_name = forms.CharField(label="Use Configuration Name", initial="use-config-%s"%datetime.datetime.now())
    #version_terrplant = forms.CharField(label="TerrPlant Version", initial="1.0")
    #etc...
    percent_ai = forms.FloatField(label="Percent Active Ingredient (%)")
    seed_treatment_formulation_name = forms.CharField(label="Seed Treatment Formulation Name", initial="")
    density_of_product = forms.FloatField(label="Density of Product (lbs/gal)")
    maximum_seedling_rate_per_use = forms.FloatField(label="Maximum Seeding Rate per Use (Crop) (lbs/A)")
    use = forms.CharField(label="Use", initial="")
    seed_crop = forms.CharField(label="Crop Use")
    application_type = forms.ChoiceField(label='Application Type' , choices=APPLICATIONTYPE, initial='broadcast')
    n_a = forms.FloatField(label="Number of Applications")
    ar_lb = forms.FloatField(label="Application rate (lbs ai/A)")
    row_sp = forms.FloatField(label="Row Spacing (inches)")
    bandwidth = forms.FloatField(label="Band width (inches)")
    foliar_dissipation_half_life = forms.FloatField(label="Foliar dissipation half-life (days)")
    frac_pest_surface = forms.FloatField(label="Fraction of pesticide assumed at surface (%)")
    day_out = forms.FloatField(label="Number of Day (of application) (days)")
    aerobic_aquatic_metabolism = forms.FloatField(label="Aerobic Aquatic Metabolism (days)")
    anaerobic_aquatic_metabolism = forms.FloatField("Anaerobic Aquatic Metabolism (days)")
    aerobic_soil_metabolism = forms.FloatField("Aerobic Soil Metabolism (days)")
    foliar_extraction = forms.FloatField(label="Foliar extraction (cm-1)")
    foliar_decay_rate = forms.FloatField(label="Foliar decay rate")
    foliar_dissipation_half_life = forms.FloatField(label="Foliar dissipation half-life")
    application_method = forms.CharField(label="Application Method")
    application_form= forms.ChoiceField(label='Application Form' , choices=APPTYPE, initial='liquid')

    