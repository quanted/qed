# -*- coding: utf-8 -*-
"""
Created on Thur Jan 19 16:13:59 2012

@author: JHarston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models

class DDMInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    one_in_ten_peak_exposure_concentration = forms.FloatField(required=True,label='Water column 1-in-10 Year EECs Peak Exposure Concentration (ug/L)')
    one_in_ten_four_day_average_exposure_concentration = forms.FloatField(required=True,label='Water column 1-in-10 Year EECs 4-Day Average Exposure Concentration (ug/L)')
    one_in_ten_twentyone_day_average_exposure_concentration = forms.FloatField(required=True,label='Water column 1-in-10 Year EECs 21-Day Average Exposure Concentration (ug/L)')
    one_in_ten_sixty_day_average_exposure_concentration = forms.FloatField(required=True,label='Water column 1-in-10 Year EECs 60-Day Average Exposure Concentration (ug/L)')
    one_in_ten_ninety_day_average_exposure_concentration = forms.FloatField(required=True,label='Water column 1-in-10 Year EECs 90-Day Average Exposure Concentration (ug/L)')
    pore_water_peak_exposure_concentration = forms.FloatField(required=True,label='Pore water (benthic) EECs Peak Exposure Concentration (ug/L)')
    pore_water_four_day_average_exposure_concentration = forms.FloatField(required=True,label='Pore water (benthic) EECs 4-Day Average Exposure Concentration (ug/L)')
    pore_water_twentyone_day_average_exposure_concentration = forms.FloatField(required=True,label='Pore water (benthic) EECs 21-Day Average Exposure Concentration (ug/L)')
    pore_water_sixty_day_average_exposure_concentration = forms.FloatField(required=True,label='Pore water (benthic) EECs 60-Day Average Exposure Concentration (ug/L)')
    pore_water_ninety_day_average_exposure_concentration = forms.FloatField(required=True,label='Pore water (benthic) EECs 90-Day Average Exposure Concentration (ug/L)')
    acute_toxicity_target_concentration_for_freshwater_fish = forms.FloatField(required=True,label='Acute Toxicity Target Concentration For Most Sensitive Freshwater Fish (LD50 x LOC)')
    chronic_toxicity_target_concentration_for_freshwater_fish = forms.FloatField(required=True,label='Chronic Toxicity Target Concentration For Most Sensitive Freshwater Fish (NOAEC x LOC)')
    acute_toxicity_target_concentration_for_freshwater_invertebrates = forms.FloatField(required=True,label='Acute Toxicity Target Concentration For Most Sensitive Freshwater Invertebrates (LD50 x LOC)')
    chronic_toxicity_target_concentration_for_freshwater_invertebrates = forms.FloatField(required=True,label='Chronic Toxicity Target Concentration For Most Sensitive Freshwater Invertebrates (NOAEC x LOC)')    
    toxicity_target_concentration_for_nonlisted_vascular_plants = forms.FloatField(required=True,label='Toxicity Target Concentration for Most Sensitive Non-listed Vascular Plants (EC50 x LOC)')
    toxicity_target_concentration_for_listed_vascular_plants = forms.FloatField(required=True,label='Toxicity Target Concentration for Most Sensitive Listed Vascular Plants (NOAEC x LOC)')
    toxicity_target_concentration_for_duckweed = forms.FloatField(required=True,label='Toxicity Target Concentration for Duckweed (EC50 x LOC)')
    toxicity_target_concentration_for_duckweed = forms.FloatField(required=True,label='Toxicity Target Concentration for Duckweed (NOAEC x LOC)')
