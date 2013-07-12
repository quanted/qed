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

APPLICATIONTYPE = (('broadcast','broadcast'),('row/band/in-furrow','row/band/in-furrow'))
APPTYPE = (('liquid','liquid'),('granular','granular'))
YN = (('Yes','Yes'),('No','No'))

class Use_metadataInp(forms.Form):
    user_use_configuration = forms.ChoiceField(label="User Saved Use Configuration",required=True)
    config_name = forms.CharField(label="Use Configuration Name", initial="use-config-%s"%datetime.datetime.now())
    