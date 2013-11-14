# -*- coding: utf-8 -*-
"""
Created on 11/07/2013

@author: Tao Hong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms


koc_check_choice=[('1', 'Koc'), ('2', 'Kd')]

class przm5Inp_chem(forms.Form):
    koc_check = forms.ChoiceField(label='Partitioning Coefficient Type', choices=koc_check_choice, widget=forms.RadioSelect())
    Koc1 = forms.FloatField(required=True, label='Sorption_Coeff (ml/g)')


