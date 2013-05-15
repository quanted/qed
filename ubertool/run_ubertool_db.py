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
import logging
import datetime


class RunUbertoolInp(forms.Form):
    logger = logging.getLogger("RunUbertoolInp")
    user_ubertool_configuration = forms.ChoiceField(label="User Saved Use Configuration",required=True)
    config_name = forms.CharField(label="Ubertool Configuration Name", initial="ubertool-config-%s"%datetime.datetime.now())
    use_configuration = forms.ChoiceField(required=True)
    pest_configuration = forms.ChoiceField(required=True)
    exposures_configuration = forms.ChoiceField(required=True)
    aquatic_configuration = forms.ChoiceField(required=True)
    terrestrial_configuration = forms.ChoiceField(required=True)
    ecosystems_configuration = forms.ChoiceField(required=True)