# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

@author: jharston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from google.appengine.api import users
from google.appengine.ext import db
from terrestrial_toxicity import TerrestrialToxicity

YN = (('Yes','Yes'),('No','No'))

class TTInp(forms.Form):
    user_id = users.get_current_user().user_id()
    user = users.get_current_user()
    user_id = user.user_id()
    q = db.Query(TerrestrialToxicity)
    q.filter('user =',user)
    uses = ()
    uses += ((None,None),)
    for use in q:
        #logger.info(use.to_xml())
        uses += ((use.config_name,use.config_name),)
    user_terrestrial_toxicity_configuration = forms.ChoiceField(label="User Saved Terrestrial Toxicity Configuration",required=True, choices=uses)
    config_name = forms.CharField(label="Use Configuration Name", initial="use-config-%s"%user_id)
    avian_ld50 = forms.FloatField(label='Avian LD50 (mg/kg-bw)')
    avian_lc50 = forms.FloatField(label='Avian LC50 (mg/kg-bw)')
    avian_NOAEC = forms.FloatField(label='Avian NOAEC (mg/kg-diet)')
    avian_NOAEL = forms.FloatField(label='Avian NOAEL (mg/kg-bw)')
    body_weight_of_the_assessed_bird = forms.FloatField(label='Body weight of assessed bird (g)')
    body_weight_of_the_assessed_bird = forms.FloatField(label='Body weight of assessed bird (kg)')
    mineau_scaling_factor = forms.FloatField(label='Chemical Mineau scaling factor')
    mammalian_ld50 = forms.FloatField(label='Mammalian LD50 (mg/kg-bw)')
    mammalian_lc50 = forms.FloatField(label='Mammalian LC50 (mg/kg-diet)')
    mammalian_inhalation_lc50 = forms.FloatField(label='Mammalian Inhalation LC50 (mg/L)')
    duration_of_rat_study = forms.FloatField(label='Duration of Rat Study (hrs)')
    mammlian_NOAEC = forms.FloatField(label='Mammalian NOAEC (mg/kg-diet)')
    mammalian_NOAEL = forms.FloatField(label='Mammalian NOAEL (mg/kg-bw)')
    amphibian_bw = forms.FloatField(label='Amphibian Body Weight (g)')    
    terrestrial_phase_amphibian_ld50 = forms.FloatField(label='Terrestrial phase amphibian LD50 (mg/kg-bw)')
    terrestrial_phase_amphibian_lc50 = forms.FloatField(label='Terrestrial phase amphibian LC50 (mg/kg-diet)')
    terrestrial_phase_amphibian_NOAEC = forms.FloatField(label='Terrestrial phase amphibian NOAEC (mg/kg-diet)')
    terrestrial_phase_amphibian_NOAEL = forms.FloatField(label='Terrestrial phase amphibian NOAEL (mg/kg-bw)')
    reptile_bw = forms.FloatField(label='Reptile Body Weight (g)')     
    terrestrial_phase_reptile_ld50 = forms.FloatField(label='Terrestrial phase reptile LD50 (mg/kg-bw)')
    terrestrial_phase_reptile_lc50 = forms.FloatField(label='Terrestrial phase reptile LC50 (mg/kg-diet)')
    terrestrial_phase_reptile_NOAEC = forms.FloatField(label='Terrestrial phase reptile NOAEC (mg/kg-diet)')
    terrestrial_phase_reptile_NOAEL = forms.FloatField(label='Terrestrial phase reptile NOAEL (mg/kg-bw)')
    EC25_for_nonlisted_seedling_emergence_monocot = forms.FloatField()
    EC25_for_nonlisted_seedling_emergence_dicot = forms.FloatField()
    NOAEC_for_listed_seedling_emergence_monocot = forms.FloatField()
    NOAEC_for_listed_seedling_emergence_dicot = forms.FloatField()
    EC25_for_nonlisted_vegetative_vigor_monocot = forms.FloatField()
    EC25_for_nonlisted_vegetative_vigor_dicot = forms.FloatField()
    NOAEC_for_listed_vegetative_vigor_monocot = forms.FloatField()
    NOAEC_for_listed_vegetative_vigor_dicot = forms.FloatField()
    Small_medium_and_large_BW_of_assessed_herptile_listed_species = forms.FloatField(label='Small, medium, and large BW of assessed herptile listed species (g)')
    percent_water_content_of_small_med_large_herptile_species_diet = forms.FloatField(label='Percent water content of small, med, large herptile species diet')    
    taxonomic_group = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),label='What taxonomic group are you assessing?')    
    eat_mammals = forms.ChoiceField(label='Does the assessed animal eat mammals' , choices=YN, initial='Yes')
    eat_amphibians_reptiles = forms.ChoiceField(label='Does the assessed animal eat amphibians or reptiles?' , choices=YN, initial='Yes')
    