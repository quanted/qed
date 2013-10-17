# -*- coding: utf-8 -*-
"""
Created on 2013-08-12

@author: Hong, Tao
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

tire_select = (('Tier 2','Tier 2'), ('Tier 3','Tier 3'))


class idreamInp(forms.Form):
    tier = forms.ChoiceField(required=True, choices=tire_select, label='Select Tier')
    ai_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), label = 'Subject active ingredient')
    prod_re = forms.FloatField(required=True, label=mark_safe('Product residue (mg/cm<sup>3</sup>)'), initial=1)
    ai = forms.FloatField(required=True, label='In-use active concentration (%)', initial=0.10)
    liq_rte = forms.FloatField(required=True, label='Liquid residue transfer efficiency (%)', initial=100)
    fruit_rte = forms.FloatField(required=True, label='Fruit residue transfer efficiency (%)', initial=70)
    bread_rte = forms.FloatField(required=True, label='Bread residue transfer efficiency (%)', initial=20)
    cheese_rte = forms.FloatField(required=True, label='Cheese residue transfer efficiency (%)', initial=55)
    veg_rte = forms.FloatField(required=True, label='Vegetable residue transfer efficiency (%)', initial=70)
    meat_rte = forms.FloatField(required=True, label='Meat residue transfer efficiency (%)', initial=80)
    pure_rte = forms.FloatField(required=True, label='Purees residue transfer efficiency (%)', initial=100)
    piec_rte = forms.FloatField(required=True, label='Pieces residue transfer efficiency (%)', initial=55)
    powd_rte = forms.FloatField(required=True, label='Powders residue transfer efficiency (%)', initial=20)
