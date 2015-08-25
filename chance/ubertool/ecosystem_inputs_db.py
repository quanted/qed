# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

@author: jharston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db
from ecosystem_inputs import EcosystemInputs
import datetime
#YN = (('Yes','Yes'),('No','No'))

class EcoInp(forms.Form):
    user_ecosystem_configuration = forms.ChoiceField(label="User Saved Ecosystem Inputs Configuration",required=True)
    config_name = forms.CharField(label="EcosystemInputs Configuration Name", initial="eco-config-%s"%datetime.datetime.now())
    x_poc = forms.FloatField(label='Concentration of particulate organic carbon (kg OC/L)', initial='0')
    x_doc = forms.FloatField(label='Concentration of dissolved organic carbon (kg OC/L)', initial='0')
    c_ox = forms.FloatField(label='Concentration of dissolved oxygen (mg O2/L)', initial='5.0')
    w_t = forms.FloatField(label='Water temperature (degrees Celsius)')
    c_ss = forms.FloatField(label='Concentration of suspended solids (kg/L)')
    oc = forms.FloatField(label='Sediment organic Carbon (%)')