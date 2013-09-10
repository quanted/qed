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
from exposure import Exposure
import datetime

class ECInp(forms.Form):
    user_exposure_concentrations_configuration = forms.ChoiceField(label="User Saved Exposure Concentrations Configuration Name",required=True)
    exposure_concentrations_config_name = forms.CharField(label="Exposure Concentrations Configuration Name", initial="exposure-concentrations-config-%s"%datetime.datetime.now())
    interval_between_applications = forms.FloatField(label='Interval between applications (days)')
    column_height = forms.FloatField(label='Column Height (m)')
    spray_drift = forms.FloatField(label='Spray Drift Fraction')
    drift_fraction = forms.FloatField(label='Drift Fraction')
    direct_spray_duration = forms.FloatField(label='Direct Spray Duration (min)')
    incorporation_depth = forms.FloatField(label='Incorporation Depth')
    percent_incorporated = forms.FloatField(label='Percent Incorporated')
    runoff_fraction = forms.FloatField(label='Runoff')    
    one_in_ten_peak_exposure_concentration = forms.FloatField(label='Water column 1-in-10 Year EECs Peak Exposure Concentration (ug/L)')
    one_in_ten_four_day_average_exposure_concentration = forms.FloatField(label='Water column 1-in-10 Year EECs 4-Day Average Exposure Concentration (ug/L)')
    one_in_ten_twentyone_day_average_exposure_concentration = forms.FloatField(label='Water column 1-in-10 Year EECs 21-Day Average Exposure Concentration (ug/L)')
    one_in_ten_sixty_day_average_exposure_concentration = forms.FloatField(label='Water column 1-in-10 Year EECs 60-Day Average Exposure Concentration (ug/L)')
    one_in_ten_ninety_day_average_exposure_concentration = forms.FloatField(label='Water column 1-in-10 Year EECs 90-Day Average Exposure Concentration (ug/L)')
    maximum_peak_exposure_concentration = forms.FloatField(label='Water column maximum EECs Peak Exposure Concentration (ug/L)')
    maximum_four_day_average_exposure_concentration = forms.FloatField(label='Water column maximum EECs 4-Day Average Exposure Concentration (ug/L)')
    maximum_twentyone_day_average_exposure_concentration = forms.FloatField(label='Water column maximum EECs 21-Day Average Exposure Concentration (ug/L)')
    maximum_sixty_day_average_exposure_concentration = forms.FloatField(label='Water column maximum EECs 60-Day Average Exposure Concentration (ug/L)')
    maximum_ninety_day_average_exposure_concentration = forms.FloatField(label='Water column maximum EECs 90-Day Average Exposure Concentration (ug/L)')
    pore_water_peak_exposure_concentration = forms.FloatField(label='Pore water (benthic) EECs Peak Exposure Concentration (ug/L)')
    pore_water_four_day_average_exposure_concentration = forms.FloatField(label='Pore water (benthic) EECs 4-Day Average Exposure Concentration (ug/L)')
    pore_water_twentyone_day_average_exposure_concentration = forms.FloatField(label='Pore water (benthic) EECs 21-Day Average Exposure Concentration (ug/L)')
    pore_water_sixty_day_average_exposure_concentration = forms.FloatField(label='Pore water (benthic) EECs 60-Day Average Exposure Concentration (ug/L)')
    pore_water_ninety_day_average_exposure_concentration = forms.FloatField(label='Pore water (benthic) EECs 90-Day Average Exposure Concentration (ug/L)')
    
    