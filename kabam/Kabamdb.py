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

Species_of_the_tested_bird_CHOICES=(('','Make a selection'),('178','Bobwhite quail'),('1580','Mallard duck'),('1','Other'))
Species_of_the_tested_mamm_CHOICES=(('','Make a selection'),('350','Laboratory rat'),('1','Other'))
Diet_for_CHOICES=(('Large Fish','Large Fish'),('Medium Fish','Medium Fish'),('Small Fish','Small Fish'),('Filter Feeder','Filter Feeder'),('Benthic Invertebrates','Benthic Invertebrates'),('Zooplankton','Zooplankton'))
Characteristics_of_aquatic_biota_CHOICES=(('Large Fish','Large Fish'),('Medium Fish','Medium Fish'),('Small Fish','Small Fish'),('Filter Feeder','Filter Feeder'),('Benthic Invertebrates','Benthic Invertebrates'),('Zooplankton','Zooplankton'),('Phytoplankton','Phytoplankton'),('Sediment','Sediment'))
Respire_CHOICES=(('Yes','Yes'),('No','No'))
Rate_constants_CHOICES=(('','Make a selection'),('a','Use default values'),('b','Input rate constants'))

class KabamInp(forms.Form):
    name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    lkow = forms.FloatField(required=True,label=mark_safe('Log K<sub>OW</sub>'))
    Koc = forms.FloatField(required=True,label=mark_safe('K<sub>OC</sub> (L/kg OC)'))
    beec = forms.FloatField(required=True,label=mark_safe('Pore water (benthic) EECs (&#956;g/L)'))
    weec = forms.FloatField(required=True,label=mark_safe('Water Column 1-in-10 year EECs (&#956;g/L)'))
    sf = forms.FloatField(required=True,label='Chemical Specific Mineau scaling factor',initial=1.15)
    cpoc = forms.FloatField(required=True,label=mark_safe('Concentration of Particulate Organic Carbon (X<sub>POC</sub>; kg OC/L)'),initial=0)
    cdoc = forms.FloatField(required=True,label=mark_safe('Concentration of Dissolved Organic Carbon (X<sub>DOC</sub>; kg OC/L)'),initial=0)
    cox = forms.FloatField(required=True,label=mark_safe('Concentration of Dissolved Oxygen (C<sub>OX</sub>; mg O<sup>2</sup>/L)'),initial=5)
    wt = forms.FloatField(required=True,label=mark_safe('Water Temperature (T; &degC)'))
    css = forms.FloatField(required=True,label=mark_safe('Concentration of Suspended Solids (C<sub>SS</sub>; Kg/L)'),initial=3.0e-5)
    oc = forms.FloatField(required=True,label=mark_safe('Sediment Organic Carbon (OC; %)'),initial=4)

    b_species = forms.ChoiceField(required=True,label='Species of the tested bird', choices=Species_of_the_tested_bird_CHOICES, initial='Make a selection')
    bw_quail = forms.FloatField(required=True,label='Weight of the tested bird', initial= '178')
    bw_duck = forms.FloatField(required=True,label='Weight of the tested bird', initial= '1580')
    bwb_other = forms.FloatField(required=True,label='Weight of the tested bird', initial= '7')
    ald50 = forms.FloatField(required=True,label='Avian LD50 (mg/kg-bw)', initial=50)
    alc50 = forms.FloatField(required=True,label='Avian LC50 (mg/kg-diet)', initial=500)
    aNOAEC = forms.FloatField(required=True,label='Avian NOAEC (mg/kg-diet)', initial=10)
    m_species = forms.ChoiceField(required=True,label='Species of the tested mammal', choices=Species_of_the_tested_mamm_CHOICES, initial='Make a selection')
    
    bw_rat=forms.FloatField(required=True, label='Body weight of the tested mammalian (g)', initial='350')
    bwm_other=forms.FloatField(required=True, label='Body weight of the tested mammalian (g)', initial='30')
    mld50 = forms.FloatField(required=True,label='Mammalian LD50 (mg/kg-bw)', initial='50')
    mlc50 = forms.FloatField(required=True,label='Mammalian LC50 (mg/kg-diet)', initial='45')
    m_chronic = forms.FloatField(required=True,label='Mammalian chronic endpoint (ppm)', initial='10')
#    bw_assess_m = forms.FloatField(required=True,label='Body weight of assessed mammal (g)')
    Diet_lfish = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Large Fish')
    lfish_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='0')
    lfish_p_phyto = forms.FloatField(required=True,label='Phytoplankton (%)', initial='0')
    lfish_p_zoo = forms.FloatField(required=True,label='Zooplankton (%)', initial='0')
    lfish_p_beninv = forms.FloatField(required=True,label='Benthic invertebrates (%)', initial='0')
    lfish_p_ff = forms.FloatField(required=True,label='Filter feeders (%)', initial='0')
    lfish_p_sfish = forms.FloatField(required=True,label='Small Fish (%)', initial='0')
    lfish_p_mfish = forms.FloatField(required=True,label='Medium Fish (%)', initial='100')
    Diet_mfish = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Medium Fish')
    mfish_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='0')
    mfish_p_phyto = forms.FloatField(required=True,label='Phytoplankton (%)', initial='0')
    mfish_p_zoo = forms.FloatField(required=True,label='Zooplankton (%)', initial='0')
    mfish_p_beninv = forms.FloatField(required=True,label='Benthic invertebrates (%)', initial='50')
    mfish_p_ff = forms.FloatField(required=True,label='Filter feeders (%)', initial='0')
    mfish_p_sfish = forms.FloatField(required=True,label='Small Fish (%)', initial='50')
    Diet_sfish = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Small Fish')
    sfish_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='0')
    sfish_p_phyto = forms.FloatField(required=True,label='Phytoplankton (%)', initial='0')
    sfish_p_zoo = forms.FloatField(required=True,label='Zooplankton (%)', initial='50')
    sfish_p_beninv = forms.FloatField(required=True,label='Benthic invertebrates (%)', initial='50')
    sfish_p_ff = forms.FloatField(required=True,label='Filter feeders (%)', initial='0')
    Diet_ff = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Filter Feeder')
    ff_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='34')
    ff_p_phyto = forms.FloatField(required=True,label='Phytoplankton (%)', initial='33')
    ff_p_zoo = forms.FloatField(required=True,label='Zooplankton (%)', initial='33')
    ff_p_beninv = forms.FloatField(required=True,label='Benthic invertebrates (%)', initial='0')
    Diet_invert = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Benthic Invertebrates')
    beninv_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='34')
    beninv_p_phyto = forms.FloatField(required=True,label='Phytoplankton (%)', initial='33')
    beninv_p_zoo = forms.FloatField(required=True,label='Zooplankton (%)', initial='33')
    Diet_zoo = forms.ChoiceField(required=True,label='Diet for', choices=Diet_for_CHOICES, initial='Zooplankton')
    zoo_p_sediment = forms.FloatField(required=True,label='Sediment (%)', initial='0')
    zoo_p_phyto = forms.FloatField(required=True,label='Phytoplankton (%)', initial='100')

    char_s = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Sediment')
    s_lipid = forms.FloatField(required=True, label='% lipids', initial=0)
    s_NLOM = forms.FloatField(required=True, label='% NLOM', initial=4)
    s_water = forms.FloatField(required=True, label='% Water', initial=96)
    s_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='No')
    char_phyto = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Phytoplankton')
    phyto_lipid = forms.FloatField(required=True, label='% lipids', initial=2)
    phyto_NLOM = forms.FloatField(required=True, label='% NLOM', initial=8)
    phyto_water = forms.FloatField(required=True, label='% Water', initial=90)
    phyto_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='No')
    char_zoo = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Zooplankton')
    zoo_ww = forms.FloatField(required=True, label='(kg)', initial=0.0000001)
    zoo_lipid = forms.FloatField(required=True, label='% lipids', initial=3)
    zoo_NLOM = forms.FloatField(required=True, label='% NLOM', initial=12)
    zoo_water = forms.FloatField(required=True, label='% Water', initial=85) 
    zoo_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='No')
    char_beninv = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Benthic Invertebrates')
    beninv_ww = forms.FloatField(required=True, label='(kg)', initial=1.0E-4)
    beninv_lipid = forms.FloatField(required=True, label='% lipids', initial=3)
    beninv_NLOM = forms.FloatField(required=True, label='% NLOM', initial=21)
    beninv_water = forms.FloatField(required=True, label='% Water', initial=76)
    beninv_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='Yes')
    char_ff = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Filter Feeder')
    ff_ww = forms.FloatField(required=True, label='(kg)', initial=1.0E-3)
    ff_lipid = forms.FloatField(required=True, label='% lipids', initial=2)
    ff_NLOM = forms.FloatField(required=True, label='% NLOM', initial=13)
    ff_water = forms.FloatField(required=True, label='% Water', initial=85)
    ff_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='Yes')
    char_sfish = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Small Fish')
    sfish_ww = forms.FloatField(required=True, label='(kg)', initial=1.0E-2)
    sfish_lipid = forms.FloatField(required=True, label='% lipids', initial=4)
    sfish_NLOM = forms.FloatField(required=True, label='% NLOM', initial=23)
    sfish_water = forms.FloatField(required=True, label='% Water', initial=73)
    sfish_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='Yes')
    char_mfish = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Medium Fish')
    mfish_ww = forms.FloatField(required=True, label='(kg)', initial=1.0E-1)
    mfish_lipid = forms.FloatField(required=True, label='% lipids', initial=4)
    mfish_NLOM = forms.FloatField(required=True, label='% NLOM', initial=23)
    mfish_water = forms.FloatField(required=True, label='% Water', initial=73)
    mfish_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='Yes')
    char_lfish = forms.ChoiceField(required=True,label='Characteristics of aquatic biota:', choices=Characteristics_of_aquatic_biota_CHOICES, initial='Large Fish')
    lfish_ww = forms.FloatField(required=True, label='(kg)', initial=1.0)
    lfish_lipid = forms.FloatField(required=True, label='% lipids', initial=4)
    lfish_NLOM = forms.FloatField(required=True, label='% NLOM', initial=23)
    lfish_water = forms.FloatField(required=True, label='% Water', initial=73)
    lfish_respire = forms.ChoiceField(required=True, label='Do organisms in trophic level respire some pore water?', choices=Respire_CHOICES, initial='No')
#####input parameters for rate constants
    rate_c = forms.ChoiceField(required=True, label='Rate constants for uptake and elimination', choices=Rate_constants_CHOICES, initial='Make a selection')
    phyto_k1 = forms.FloatField(required=True, label=mark_safe('phytoplankton k<sub>1</sub> (L/kg*d)'))
    phyto_k2 = forms.FloatField(required=True, label=mark_safe('phytoplankton k<sub>2</sub> (d<sup>-1</sup>)'))
    phyto_kd = forms.FloatField(required=True, label=mark_safe('phytoplankton k<sub>D</sub> (kg-food/kg-org/d)'), initial=0)
    phyto_ke = forms.FloatField(required=True, label=mark_safe('phytoplankton k<sub>E</sub> (d<sup>-1</sup>)'), initial=0)
    phyto_km = forms.FloatField(required=True, label=mark_safe('phytoplankton k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    zoo_k1 = forms.FloatField(required=True, label=mark_safe('zooplankton k<sub>1</sub> (L/kg*d)'))
    zoo_k2 = forms.FloatField(required=True, label=mark_safe('zooplankton k<sub>2</sub> (d<sup>-1</sup>)'))
    zoo_kd = forms.FloatField(required=True, label=mark_safe('zooplankton k<sub>D</sub> (kg-food/kg-org/d)'))
    zoo_ke = forms.FloatField(required=True, label=mark_safe('zooplankton k<sub>E</sub> (d<sup>-1</sup>)'))
    zoo_km = forms.FloatField(required=True, label=mark_safe('zooplankton k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    beninv_k1 = forms.FloatField(required=True, label=mark_safe('benthic invertebrates k<sub>1</sub> (L/kg*d)'))
    beninv_k2 = forms.FloatField(required=True, label=mark_safe('benthic invertebrates k<sub>2</sub> (d<sup>-1</sup>)'))
    beninv_kd = forms.FloatField(required=True, label=mark_safe('benthic invertebrates k<sub>D</sub> (kg-food/kg-org/d)'))
    beninv_ke = forms.FloatField(required=True, label=mark_safe('benthic invertebrates k<sub>E</sub> (d<sup>-1</sup>)'))
    beninv_km = forms.FloatField(required=True, label=mark_safe('benthic invertebrates k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    ff_k1 = forms.FloatField(required=True, label=mark_safe('filter feeders k<sub>1</sub> (L/kg*d)'))
    ff_k2 = forms.FloatField(required=True, label=mark_safe('filter feeders k<sub>2</sub> (d<sup>-1</sup>)'))
    ff_kd = forms.FloatField(required=True, label=mark_safe('filter feeders k<sub>D</sub> (kg-food/kg-org/d)'))
    ff_ke = forms.FloatField(required=True, label=mark_safe('filter feeders k<sub>E</sub> (d<sup>-1</sup>)'))
    ff_km = forms.FloatField(required=True, label=mark_safe('filter feeders k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    sfish_k1 = forms.FloatField(required=True, label=mark_safe('small fish k<sub>1</sub> (L/kg*d)'))
    sfish_k2 = forms.FloatField(required=True, label=mark_safe('small fish k<sub>2</sub> (d<sup>-1</sup>)'))
    sfish_kd = forms.FloatField(required=True, label=mark_safe('small fish k<sub>D</sub> (kg-food/kg-org/d)'))
    sfish_ke = forms.FloatField(required=True, label=mark_safe('small fish k<sub>E</sub> (d<sup>-1</sup>)'))
    sfish_km = forms.FloatField(required=True, label=mark_safe('small fish k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    mfish_k1 = forms.FloatField(required=True, label=mark_safe('medium fish k<sub>1</sub> (L/kg*d)'))
    mfish_k2 = forms.FloatField(required=True, label=mark_safe('medium fish k<sub>2</sub> (d<sup>-1</sup>)'))
    mfish_kd = forms.FloatField(required=True, label=mark_safe('medium fish k<sub>D</sub> (kg-food/kg-org/d)'))
    mfish_ke = forms.FloatField(required=True, label=mark_safe('medium fish k<sub>E</sub> (d<sup>-1</sup>)'))
    mfish_km = forms.FloatField(required=True, label=mark_safe('medium fish k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)
    lfish_k1 = forms.FloatField(required=True, label=mark_safe('large fish k<sub>1</sub> (L/kg*d)'))
    lfish_k2 = forms.FloatField(required=True, label=mark_safe('large fish k<sub>2</sub> (d<sup>-1</sup>)'))
    lfish_kd = forms.FloatField(required=True, label=mark_safe('large fish k<sub>D</sub> (kg-food/kg-org/d)'))
    lfish_ke = forms.FloatField(required=True, label=mark_safe('large fish k<sub>E</sub> (d<sup>-1</sup>)'))
    lfish_km = forms.FloatField(required=True, label=mark_safe('large fish k<sub>M</sub> (d<sup>-1</sup>)'),initial=0)



























