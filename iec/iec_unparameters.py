# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

dist_choices=(('','Select distribution'), ('Log-normal','Log-normal'), ('Uniform','Uniform'))

class iecInp(forms.Form):
    NOI = forms.IntegerField(required=True, label='Numer of Iterations', initial=100)
    LC50 = forms.ChoiceField(required=True,label=mark_safe('Enter LC<sub>50</sub> or LD<sub>50</sub>'), choices=dist_choices, initial='')
    LC50_mean = forms.FloatField(required=True, label=mark_safe('LC<sub>50</sub> or LD<sub>50</sub> Mean'), initial='1.0')
    LC50_std = forms.FloatField(required=True, label=mark_safe('LC<sub>50</sub> or LD<sub>50</sub> Std.'), initial='0.10')
    LC50_lower = forms.FloatField(required=True, label=mark_safe('LC<sub>50</sub> or LD<sub>50</sub> lower bound'), initial='0.10')
    LC50_upper = forms.FloatField(required=True, label=mark_safe('LC<sub>50</sub> or LD<sub>50</sub> upper bound'), initial='1.50')

    threshold = forms.ChoiceField(required=True, label='Enter desired threshold', choices=dist_choices, initial='')
    threshold_mean = forms.FloatField(required=True, label='Threshold Mean', initial='0.25')
    threshold_std = forms.FloatField(required=True, label='Threshold Std.', initial='0.10')
    threshold_lower = forms.FloatField(required=True, label='Threshold lower bound', initial='0.05')
    threshold_upper = forms.FloatField(required=True, label='Threshold upper bound', initial='0.75')

    dose_response = forms.ChoiceField(required=True, label='Enter slope of does-response', choices=dist_choices, initial='')
    dose_response_mean = forms.FloatField(required=True, label='Dose_response Mean', initial='4.50')
    dose_response_std = forms.FloatField(required=True, label='Dose_response Std.', initial='0.50')
    dose_response_lower = forms.FloatField(required=True, label='Dose_response lower bound', initial='3.00')
    dose_response_upper = forms.FloatField(required=True, label='Dose_response upper bound', initial='6.00')