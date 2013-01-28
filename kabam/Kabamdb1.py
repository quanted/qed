# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: thong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.utils.safestring import mark_safe
from django.db import models
from google.appengine.api import rdbms

Species_of_the_tested_bird_CHOICES=(('178','Bobwhite quail'),('1580','Mallard duck'),('','Other'))
Species_of_the_tested_mamm_CHOICES=(('350','Laboratory rat'),('1','Other'))
Diet_for_CHOICES=(('Large Fish','Large Fish'),('Medium Fish','Medium Fish'),('Small Fish','Small Fish'),('Filter Feeder','Filter Feeder'),('Benthic Invertebrates','Benthic Invertebrates'),('Zooplankton','Zooplankton'))
Characteristics_of_aquatic_biota_CHOICES=(('Large Fish','Large Fish'),('Medium Fish','Medium Fish'),('Small Fish','Small Fish'),('Filter Feeder','Filter Feeder'),('Benthic Invertebrates','Benthic Invertebrates'),('Zooplankton','Zooplankton'),('Phytoplankton','Phytoplankton'),('Sediment','Sediment'))
Respire_CHOICES=(('Yes','Yes'),('No','No'))
Rate_constants_CHOICES=(('','Make a selection'),('a','Use default values'),('b','Input rate constants'))

class KabamInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    l_kow = forms.FloatField(required=True,label=mark_safe('Log K<sub>OW</sub>'))
    Koc = forms.FloatField(required=True,label=mark_safe('K<sub>OC</sub> (L/kg OC)'))
    pore_water_benthic_EECs = forms.FloatField(required=True,label=mark_safe('Pore water (benthic) EECs (&#956;g/L)'))
    water_column_1_in_10_year_EECs = forms.FloatField(required=True,label=mark_safe('Water Column 1-in-10 year EECs (&#956;g/L)'))
    chemical_specific_mineau_scaling_factor = forms.FloatField(required=True,label='Chemical Specific Mineau scaling factor',initial=1.15)
    c_poc = forms.FloatField(required=True,label=mark_safe('Concentration of Particulate Organic Carbon (X<sub>POC</sub>; kg OC/L)'),initial=0)
    c_doc = forms.FloatField(required=True,label=mark_safe('Concentration of Dissolved Organic Carbon (X<sub>DOC</sub>; kg OC/L)'),initial=0)
    c_ox = forms.FloatField(required=True,label=mark_safe('Concentration of Dissolved Oxygen (C<sub>OX</sub>; mg O<sup>2</sup>/L)'),initial=5)
    w_t = forms.FloatField(required=True,label=mark_safe('Water Temperature (T; &degC)'))
    c_ss = forms.FloatField(required=True,label=mark_safe('Concentration of Suspended Solids (C<sub>SS</sub>; Kg/L)'),initial=3.0e-5)
    oc = forms.FloatField(required=True,label=mark_safe('Sediment Organic Carbon (OC; %)'),initial=4)

    Species_of_the_tested_bird = forms.ChoiceField(required=True,label='Species of the tested bird', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
    Body_weight_of_the_tested_bird = forms.FloatField(required=True,label='Weight of the tested bird', initial= 178)
    avian_ld50 = forms.FloatField(required=True,label='Avian LD50 (mg/kg-bw)', initial=50)
    avian_lc50 = forms.FloatField(required=True,label='Avian LC50 (mg/kg-diet)', initial=500)
    avian_NOAEC = forms.FloatField(required=True,label='Avian NOAEC (mg/kg-diet)', initial=10)
    Species_of_the_tested_mamm = forms.ChoiceField(required=True,label='Species of the tested mammal', choices=Species_of_the_tested_mamm_CHOICES, initial='Laboratory rat')
    
    body_weight_of_the_tested_mamm=forms.FloatField(required=True, label='Body weight of the tested mammalian (g)', initial='350')
    mammalian_ld50 = forms.FloatField(required=True,label='Mammalian LD50 (mg/kg-bw)')
    mammalian_lc50 = forms.FloatField(required=True,label='Mammalian LC50 (mg/kg-diet)')
    mammalian_chronic_endpoint = forms.FloatField(required=True,label='Mammalian chronic endpoint (ppm)')
    body_weight_of_the_assessed_mamm = forms.FloatField(required=True,label='Body weight of assessed mammal (g)')
    Diet_for_large_fish = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Large Fish')
    large_fish_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='0')
    large_fish_p_phytoplankton = forms.FloatField(required=True,label='Phytoplankton (%)', initial='0')
    large_fish_p_zooplankton = forms.FloatField(required=True,label='Zooplankton (%)', initial='0')
    large_fish_p_benthic_invertebrates = forms.FloatField(required=True,label='Benthic invertebrates (%)', initial='0')
    large_fish_p_filter_feeders = forms.FloatField(required=True,label='Filter feeders (%)', initial='0')
    large_fish_p_small_fish = forms.FloatField(required=True,label='Small Fish (%)', initial='0')
    large_fish_p_fish_medium = forms.FloatField(required=True,label='Medium Fish (%)', initial='100')
    Diet_for_medium_fish = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Medium Fish')
    medium_fish_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='0')
    medium_fish_p_phytoplankton = forms.FloatField(required=True,label='Phytoplankton (%)', initial='0')
    medium_fish_p_zooplankton = forms.FloatField(required=True,label='Zooplankton (%)', initial='0')
    medium_fish_p_benthic_invertebrates = forms.FloatField(required=True,label='Benthic invertebrates (%)', initial='50')
    medium_fish_p_filter_feeders = forms.FloatField(required=True,label='Filter feeders (%)', initial='0')
    medium_fish_p_small_fish = forms.FloatField(required=True,label='Small Fish (%)', initial='50')
    Diet_for_small_fish = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Small Fish')
    small_fish_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='0')
    small_fish_p_phytoplankton = forms.FloatField(required=True,label='Phytoplankton (%)', initial='0')
    small_fish_p_zooplankton = forms.FloatField(required=True,label='Zooplankton (%)', initial='50')
    small_fish_p_benthic_invertebrates = forms.FloatField(required=True,label='Benthic invertebrates (%)', initial='50')
    small_fish_p_filter_feeders = forms.FloatField(required=True,label='Filter feeders (%)', initial='0')
    Diet_for_filter_feeder = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Filter Feeder')
    filter_feeder_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='34')
    filter_feeder_p_phytoplankton = forms.FloatField(required=True,label='Phytoplankton (%)', initial='33')
    filter_feeder_p_zooplankton = forms.FloatField(required=True,label='Zooplankton (%)', initial='33')
    filter_feeder_p_benthic_invertebrates = forms.FloatField(required=True,label='Benthic invertebrates (%)', initial='0')
    Diet_for_invertebrates = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Benthic Invertebrates')
    benthic_invertebrates_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='34')
    benthic_invertebrates_p_phytoplankton = forms.FloatField(required=True,label='Phytoplankton (%)', initial='33')
    benthic_invertebrates_p_zooplankton = forms.FloatField(required=True,label='Zooplankton (%)', initial='33')
    Diet_for_zooplankton = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Zooplankton')
    zooplankton_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='0')
    zooplankton_p_phytoplankton = forms.FloatField(required=True,label='Phytoplankton (%)', initial='100')

    characteristics_sediment = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Sediment')
    sediment_lipid = forms.FloatField(required=True, label='% lipids', initial=0)
    sediment_NLOM = forms.FloatField(required=True, label='% NLOM', initial=4)
    sediment_water = forms.FloatField(required=True, label='% Water', initial=96)
    sediment_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='No')
    characteristics_phytoplankton = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Phytoplankton')
    phytoplankton_lipid = forms.FloatField(required=True, label='% lipids', initial=2)
    phytoplankton_NLOM = forms.FloatField(required=True, label='% NLOM', initial=8)
    phytoplankton_water = forms.FloatField(required=True, label='% Water', initial=90)
    phytoplankton_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='No')
    characteristics_zooplankton = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Zooplankton')
    zooplankton_wet_weight = forms.FloatField(required=True, label='(kg)', initial=1.0E-7)
    zooplankton_lipid = forms.FloatField(required=True, label='% lipids', initial=3)
    zooplankton_NLOM = forms.FloatField(required=True, label='% NLOM', initial=12)
    zooplankton_water = forms.FloatField(required=True, label='% Water', initial=85)
    zooplankton_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='No')
    characteristics_benthic_invertebrates = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Benthic Invertebrates')
    benthic_invertebrates_wet_weight = forms.FloatField(required=True, label='(kg)', initial=1.0E-4)
    benthic_invertebrates_lipid = forms.FloatField(required=True, label='% lipids', initial=3)
    benthic_invertebrates_NLOM = forms.FloatField(required=True, label='% NLOM', initial=21)
    benthic_invertebrates_water = forms.FloatField(required=True, label='% Water', initial=76)
    benthic_invertebrates_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='Yes')
    characteristics_filter_feeders = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Filter Feeder')
    filter_feeders_wet_weight = forms.FloatField(required=True, label='(kg)', initial=1.0E-3)
    filter_feeders_lipid = forms.FloatField(required=True, label='% lipids', initial=2)
    filter_feeders_NLOM = forms.FloatField(required=True, label='% NLOM', initial=13)
    filter_feeders_water = forms.FloatField(required=True, label='% Water', initial=85)
    filter_feeders_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='Yes')
    characteristics_small_fish = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Small Fish')
    small_fish_wet_weight = forms.FloatField(required=True, label='(kg)', initial=1.0E-2)
    small_fish_lipid = forms.FloatField(required=True, label='% lipids', initial=4)
    small_fish_NLOM = forms.FloatField(required=True, label='% NLOM', initial=23)
    small_fish_water = forms.FloatField(required=True, label='% Water', initial=73)
    small_fish_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='Yes')
    characteristics_medium_fish = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Medium Fish')
    medium_fish_wet_weight = forms.FloatField(required=True, label='(kg)', initial=1.0E-1)
    medium_fish_lipid = forms.FloatField(required=True, label='% lipids', initial=4)
    medium_fish_NLOM = forms.FloatField(required=True, label='% NLOM', initial=23)
    medium_fish_water = forms.FloatField(required=True, label='% Water', initial=73)
    medium_fish_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='Yes')
    characteristics_large_fish = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Large Fish')
    large_fish_wet_weight = forms.FloatField(required=True, label='(kg)', initial=1.0)
    large_fish_lipid = forms.FloatField(required=True, label='% lipids', initial=4)
    large_fish_NLOM = forms.FloatField(required=True, label='% NLOM', initial=23)
    large_fish_water = forms.FloatField(required=True, label='% Water', initial=73)
    large_fish_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='No')
#input parameters for rate constants
    rate_constants = forms.ChoiceField(required=True, label='Rate constants for uptake and elimination', choices=Rate_constants_CHOICES, initial='Make a selection')
    phytoplankton_k1 = forms.FloatField(required=True, label=mark_safe('phytoplankton k<sub>1</sub> (L/kg*d)'))
    phytoplankton_k2 = forms.FloatField(required=True, label=mark_safe('phytoplankton k<sub>2</sub> (d<sup>-1</sup>)'))
    phytoplankton_kd = forms.FloatField(required=True, label=mark_safe('phytoplankton k<sub>D</sub> (kg-food/kg-org/d)'), initial=0)
    phytoplankton_ke = forms.FloatField(required=True, label=mark_safe('phytoplankton k<sub>E</sub> (d<sup>-1</sup>)'), initial=0)
    phytoplankton_km = forms.FloatField(required=True, label=mark_safe('phytoplankton k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    zooplankton_k1 = forms.FloatField(required=True, label=mark_safe('zooplankton k<sub>1</sub> (L/kg*d)'))
    zooplankton_k2 = forms.FloatField(required=True, label=mark_safe('zooplankton k<sub>2</sub> (d<sup>-1</sup>)'))
    zooplankton_kd = forms.FloatField(required=True, label=mark_safe('zooplankton k<sub>D</sub> (kg-food/kg-org/d)'))
    zooplankton_ke = forms.FloatField(required=True, label=mark_safe('zooplankton k<sub>E</sub> (d<sup>-1</sup>)'))
    zooplankton_km = forms.FloatField(required=True, label=mark_safe('zooplankton k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    benthic_invertebrates_k1 = forms.FloatField(required=True, label=mark_safe('benthic invertebrates k<sub>1</sub> (L/kg*d)'))
    benthic_invertebrates_k2 = forms.FloatField(required=True, label=mark_safe('benthic invertebrates k<sub>2</sub> (d<sup>-1</sup>)'))
    benthic_invertebrates_kd = forms.FloatField(required=True, label=mark_safe('benthic invertebrates k<sub>D</sub> (kg-food/kg-org/d)'))
    benthic_invertebrates_ke = forms.FloatField(required=True, label=mark_safe('benthic invertebrates k<sub>E</sub> (d<sup>-1</sup>)'))
    benthic_invertebrates_km = forms.FloatField(required=True, label=mark_safe('benthic invertebrates k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    filter_feeders_k1 = forms.FloatField(required=True, label=mark_safe('filter feeders k<sub>1</sub> (L/kg*d)'))
    filter_feeders_k2 = forms.FloatField(required=True, label=mark_safe('filter feeders k<sub>2</sub> (d<sup>-1</sup>)'))
    filter_feeders_kd = forms.FloatField(required=True, label=mark_safe('filter feeders k<sub>D</sub> (kg-food/kg-org/d)'))
    filter_feeders_ke = forms.FloatField(required=True, label=mark_safe('filter feeders k<sub>E</sub> (d<sup>-1</sup>)'))
    filter_feeders_km = forms.FloatField(required=True, label=mark_safe('filter feeders k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    small_fish_k1 = forms.FloatField(required=True, label=mark_safe('small fish k<sub>1</sub> (L/kg*d)'))
    small_fish_k2 = forms.FloatField(required=True, label=mark_safe('small fish k<sub>2</sub> (d<sup>-1</sup>)'))
    small_fish_kd = forms.FloatField(required=True, label=mark_safe('small fish k<sub>D</sub> (kg-food/kg-org/d)'))
    small_fish_ke = forms.FloatField(required=True, label=mark_safe('small fish k<sub>E</sub> (d<sup>-1</sup>)'))
    small_fish_km = forms.FloatField(required=True, label=mark_safe('small fish k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    medium_fish_k1 = forms.FloatField(required=True, label=mark_safe('medium fish k<sub>1</sub> (L/kg*d)'))
    medium_fish_k2 = forms.FloatField(required=True, label=mark_safe('medium fish k<sub>2</sub> (d<sup>-1</sup>)'))
    medium_fish_kd = forms.FloatField(required=True, label=mark_safe('medium fish k<sub>D</sub> (kg-food/kg-org/d)'))
    medium_fish_ke = forms.FloatField(required=True, label=mark_safe('medium fish k<sub>E</sub> (d<sup>-1</sup>)'))
    medium_fish_km = forms.FloatField(required=True, label=mark_safe('medium fish k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    large_fish_k1 = forms.FloatField(required=True, label=mark_safe('large fish k<sub>1</sub> (L/kg*d)'))
    large_fish_k2 = forms.FloatField(required=True, label=mark_safe('large fish k<sub>2</sub> (d<sup>-1</sup>)'))
    large_fish_kd = forms.FloatField(required=True, label=mark_safe('large fish k<sub>D</sub> (kg-food/kg-org/d)'))
    large_fish_ke = forms.FloatField(required=True, label=mark_safe('large fish k<sub>E</sub> (d<sup>-1</sup>)'))
    large_fish_km = forms.FloatField(required=True, label=mark_safe('large fish k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)




























