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
from exposure_concentrations import ExposureConcentrations

class ECInp(forms.Form):
    user_id = users.get_current_user().user_id()
    user = users.get_current_user()
    user_id = user.user_id()
    q = db.Query(ExposureConcentrations)
    q.filter('user =',user)
    uses = ()
    uses += ((None,None),)
    for use in q:
        #logger.info(use.to_xml())
        uses += ((use.config_name,use.config_name),)
    user_exposure_concentrations_configuration = forms.ChoiceField(label="User Saved Exposure Concentrations Configuration",required=True, choices=uses)
    config_name = forms.CharField(label="Use Configuration Name", initial="use-config-%s"%user_id)
    config_name = forms.CharField(label="Use Configuration Name", initial="use-config-%s"%user_id)
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
    
    