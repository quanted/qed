import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe


class loonsinp(forms.Form):
    b = forms.FloatField(required=True, label=mark_safe('Pairing propensity for age &ge; 3'), initial=0.80)
    m = forms.FloatField(required=True, label='Chicks raised to mid-Aug per paired female', initial=0.58)
    r = forms.FloatField(required=True, label='Assumed proportion of chicks that are female', initial=0.50)
    pa = forms.FloatField(required=True, label=mark_safe('Annual survival for age &ge; 3'), initial=0.92)
    sj = forms.FloatField(required=True, label=mark_safe('Annual survival for age < 3'), initial=0.75)
    # rj = forms.FloatField(required=True, label='Proportion of surviving juveniles transitioning into adulthood', initial=0.25)
    t = forms.FloatField(required=True, label='Modeling duration (years)', initial=10)

