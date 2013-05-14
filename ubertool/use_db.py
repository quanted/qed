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
from use import Use
import logging

APPLICATIONTYPE = (('broadcast','broadcast'),('row/band/in-furrow','row/band/in-furrow'))
APPTYPE = (('liquid','liquid'),('granular','granular'))
YN = (('Yes','Yes'),('No','No'))

class UseInp(forms.Form):
    user_id = users.get_current_user().user_id()
    user = users.get_current_user()
    user_id = user.user_id()
    q = db.Query(Use)
    q.filter('user =',user)
    uses = ()
    uses += ((None,None),)
    logger = logging.getLogger("UseInp")
    for use in q:
        logger.info(use.to_xml())
        uses += ((use.config_name,use.config_name),)
    user_use_configuration = forms.ChoiceField(label="User Saved Use Configuration",required=True, choices=uses)
    config_name = forms.CharField(label="Use Configuration Name", initial="use-config-%s"%user_id)
    #cas = CASGql("apppest:cas","CAS")
    #cas_number = forms.ChoiceField(required=True, choices=cas.getAllChemNamesCASNumsUTF8(None,20))
    cas_number = forms.ChoiceField(required=True)
    formulated_product_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    percent_ai = forms.FloatField(label='% Active Ingredient')
    metfile = forms.FloatField()
    PRZM_scenario = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    EXAMS_environment_file = forms.FloatField()
    application_method = forms.FloatField(label='Application Method (CAM)')
    application_type = forms.ChoiceField(label='Application Type (for terrestrial)',choices=APPLICATIONTYPE, initial='broadcast')
    app_type = forms.ChoiceField(label='Application Type (for terrestrial)',choices=APPTYPE, initial='liquid')
    weight_of_one_granule = forms.FloatField(label='Weight of 1 granule (mg)')
    wetted_in = forms.ChoiceField(label='Wetted In?', choices=YN, initial='Yes')
    incorporation_depth = forms.FloatField(label='Incorporation Depth (cm)')
    percent_incorporated = forms.FloatField(label='% Incorporated (%)')
    application_kg_rate = forms.FloatField(label='Application rate (kg ai/ha)')
    application_lbs_rate = forms.FloatField(label='Application rate (lbs ai/A)')
    seed_treatment_formulation_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),label='Seed treatment formulation name')
    density_of_product = forms.FloatField(label='Density of product (lbs/gal)')
    maximum_seedling_rate_per_use = forms.FloatField(label='Maximum seedling rate per use (lbs/A)')
    application_rate_per_use = forms.FloatField(label='Application rate per use (fl oz/cwt)')    
    application_date = forms.DateField()
    number_of_applications = forms.FloatField(label='Number of applications')
    interval_between_applications = forms.FloatField(label='Interval between applications (days)')
    application_efficiency = forms.FloatField(label='Application Efficiency (fraction)')
    spray_drift = forms.FloatField(label='Spray Drift (fraction)')
    runoff = forms.FloatField(label='Runoff (fraction)')
    