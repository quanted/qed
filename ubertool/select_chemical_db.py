# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

@author: pascact1
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
import sys
sys.path.append('../CAS')
from CAS.CASGql import CASGql
from google.appengine.api import users

class SelectChemicalInp(forms.Form):
    user_id = users.get_current_user().user_id()
    formulated_product_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))