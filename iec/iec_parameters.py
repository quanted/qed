# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

class iecInp(forms.Form):
    LC50 = forms.FloatField(required=True,label=mark_safe('Enter LC<sub>50</sub> or LD<sub>50</sub>'),initial='1')
    threshold = forms.FloatField(required=True, label='Enter desired threshold',initial='0.25')
    dose_response = forms.FloatField(required=True, label='Enter slope of does-response',initial=4.5)
    