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

APPLICATIONTYPE=(('Broadcast-Granular','Broadcast-Granular'),('Row/Band/In-furrow-Granular','Row/Band/In-furrow-Granular'),
                         ('Broadcast-Liquid','Broadcast-Liquid'),('Row/Band/In-furrow-Liquid','Row/Band/In-furrow-Liquid'))

YN=(('Yes','Yes'),('No','No'))

class ECInp(forms.Form):
    user_id = users.get_current_user().user_id()
    user = users.get_current_user()
    user_id = user.user_id()
    q = db.Query(Exposure)
    q.filter('user =',user)
    uses = ()
    uses += ((None,None),)
    for use in q:
        #logger.info(use.to_xml())
        uses += ((use.config_name,use.config_name),)
    cas_number = forms.ChoiceField(required=True)
    formulated_product_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    metfile = forms.FloatField()
    PRZM_scenario = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    EXAMS_environment_file = forms.FloatField()
    application_method = forms.FloatField(label='Application Method (CAM)')
    app_type = forms.ChoiceField(label='Application Type (for terrestrial)',choices=APPLICATIONTYPE, initial='liquid')
    weight_of_one_granule = forms.FloatField(label='Weight of 1 granule (mg)')
    wetted_in = forms.ChoiceField(label='Wetted In?', choices=YN, initial='Yes')
    incorporation_depth = forms.FloatField(label='Incorporation Depth (cm)')
    application_kg_rate = forms.FloatField(label='Application rate (kg ai/ha)')
    application_lbs_rate = forms.FloatField(label='Application rate (lbs ai/A)')
    application_rate_per_use = forms.FloatField(label='Application rate per use (fl oz/cwt)')    
    application_date = forms.DateField()
    interval_between_applications = forms.FloatField(label='Interval between applications (days)')
    application_efficiency = forms.FloatField(label='Application Efficiency (fraction)')
    spray_drift = forms.FloatField(label='Spray Drift (fraction)')
    runoff = forms.FloatField(label='Runoff (fraction)')    
    user_exposure_concentrations_configuration = forms.ChoiceField(label="User Saved Exposure Concentrations Configuration",required=True, choices=uses)
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
    frac_pest_surface = forms.FloatField(label='Fraction of pesticide assumed at surface')
    
    




    



    







    