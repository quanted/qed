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
import datetime

YN = (('Yes','Yes'),('No','No'))

class TTInp(forms.Form):
    user_terrestrial_toxicity_configuration = forms.ChoiceField(label="User Saved Terrestrial Toxicity Configuration",required=True)
    config_name = forms.CharField(label="Use Configuration Name", initial="use-config-%s"%datetime.datetime.now())
    avian_ld50 = forms.FloatField(label='Avian LD50 (mg/kg-bw)')
    low_bird_acute_oral_ld50 = forms.FloatField(label='Avian LD50 lowest dose(mg/kg-bw)')
    mamm_acute_derm_ld50 = forms.FloatField(label='Mammalian acute Dermal LD50')
    mamm_acute_derm_study = forms.CharField(label='Mammalian acute dermal LD50 study')
    bird_acute_oral_study = forms.CharField(label='Avian acute oral study MRID number')
    bird_study_add_comm = forms.CharField(label='bird_study_add_comm')
    Species_of_the_tested_bird = forms.CharField(Label='Species_of_the_tested_bird')
    mamm_study_add_comm = forms.CharField(label='mamm_study_add_comm')
    avian_lc50 = forms.FloatField(label='Avian LC50 (mg/kg-bw)')
    avian_NOAEC = forms.FloatField(label='Avian NOAEC (mg/kg-diet)')
    avian_NOAEL = forms.FloatField(label='Avian NOAEL (mg/kg-bw)')
    tested_bird_body_weight = forms.FloatField(label='Body weight of the tested bird (g)')
    tested_mamm_body_weight = forms.FloatField(label='Body weight of the tested mammal (g)') 
    body_weight_of_the_assessed_bird = forms.FloatField(label='Body weight of assessed bird (g)')
    body_weight_of_the_assessed_bird_sm = forms.FloatField(label='Body weight of assessed small bird (g)')
    body_weight_of_the_assessed_bird_md = forms.FloatField(label='Body weight of assessed medium bird (g)')
    body_weight_of_the_assessed_bird_lg = forms.FloatField(label='Body weight of assessed large bird (g)')
    body_weight_of_the_assessed_mammal_sm = forms.FloatField(label='Body weight of assessed small mammal (g)')
    body_weight_of_the_assessed_mammal_md = forms.FloatField(label='Body weight of assessed medium mammal (g)')
    body_weight_of_the_assessed_mammal_lg = forms.FloatField(label='Body weight of assessed large mammal (g)')
    bw_quail = forms.FloatField(label='Body weight of the assessed quail (g)')
    bw_duck = forms.FloatField(label='Body weight of the assessed duck (g)')
    bwb_other = forms.FloatField(label='Body weight of the assessed bird (g)')
    mineau_scaling_factor = forms.FloatField(label='Chemical Mineau scaling factor')
    mammalian_ld50 = forms.FloatField(label='Mammalian LD50 (mg/kg-bw)')
    mammalian_lc50 = forms.FloatField(label='Mammalian LC50 (mg/kg-diet)')
    mammalian_inhalation_lc50 = forms.FloatField(label='Mammalian Inhalation LC50 (mg/L)')
    duration_of_rat_study = forms.FloatField(label='Duration of Rat Study (hrs)')
    mammalian_NOAEC = forms.FloatField(label='Mammalian NOAEC (mg/kg-diet)')
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
                                                                                                                                