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
from aquatic_toxicity import AquaticToxicity

class ATInp(forms.Form):
    user_id = users.get_current_user().user_id()
    user = users.get_current_user()
    user_id = user.user_id()
    q = db.Query(AquaticToxicity)
    q.filter('user =',user)
    uses = ()
    uses += ((None,None),)
    for use in q:
        #logger.info(use.to_xml())
        uses += ((use.config_name,use.config_name),)
    user_use_configuration = forms.ChoiceField(label="Aquatic Toxicity Saved Use Configuration",required=True, choices=uses)
    config_name = forms.CharField(label="Aquatic Toxicity Configuration Name", initial="aquatic-toxicity-config-%s"%user_id)
    acute_toxicity_target_concentration_for_freshwater_fish = forms.FloatField(label='Acute Toxicity Target Concentration For Most Sensitive Freshwater Fish')
    chronic_toxicity_target_concentration_for_freshwater_fish = forms.FloatField(label='Chronic Toxicity Target Concentration For Most Sensitive Freshwater Fish')
    acute_toxicity_target_concentration_for_freshwater_invertebrates = forms.FloatField(label='Acute Toxicity Target Concentration For Most Sensitive Freshwater Invertebrates')
    chronic_toxicity_target_concentration_for_freshwater_invertebrates = forms.FloatField(label='Chronic Toxicity Target Concentration For Most Sensitive Freshwater Invertebrates')    
    toxicity_target_concentration_for_nonlisted_vascular_plants = forms.FloatField(label='Toxicity Target Concentration for Most Sensitive Non-listed Vascular Plants')
    toxicity_target_concentration_for_listed_vascular_plants = forms.FloatField(label='Toxicity Target Concentration for Most Sensitive Listed Vascular Plants')
    toxicity_target_concentration_for_duckweed = forms.FloatField(label='Toxicity Target Concentration for Duckweed')
    created = db.DateTimeProperty(auto_now_add=True)    
    