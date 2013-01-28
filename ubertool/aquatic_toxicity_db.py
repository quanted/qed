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

class ATInp(forms.Form):
    user_id = users.get_current_user().user_id()
    config_name = forms.CharField(label="Use Configuration Name", initial="use-config-%s"%user_id)
    acute_toxicity_target_concentration_for_freshwater_fish = forms.FloatField(label='Acute Toxicity Target Concentration For Most Sensitive Freshwater Fish')
    chronic_toxicity_target_concentration_for_freshwater_fish = forms.FloatField(label='Chronic Toxicity Target Concentration For Most Sensitive Freshwater Fish')
    acute_toxicity_target_concentration_for_freshwater_invertebrates = forms.FloatField(label='Acute Toxicity Target Concentration For Most Sensitive Freshwater Invertebrates')
    chronic_toxicity_target_concentration_for_freshwater_invertebrates = forms.FloatField(label='Chronic Toxicity Target Concentration For Most Sensitive Freshwater Invertebrates')    
    toxicity_target_concentration_for_nonlisted_vascular_plants = forms.FloatField(label='Toxicity Target Concentration for Most Sensitive Non-listed Vascular Plants')
    toxicity_target_concentration_for_listed_vascular_plants = forms.FloatField(label='Toxicity Target Concentration for Most Sensitive Listed Vascular Plants')
    toxicity_target_concentration_for_duckweed = forms.FloatField(label='Toxicity Target Concentration for Duckweed')
    created = db.DateTimeProperty(auto_now_add=True)    
    