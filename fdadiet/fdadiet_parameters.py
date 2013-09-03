# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: JHarston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

class fdadietInp(forms.Form):
	chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='component X')
	trade_name = forms.CharField(label='Commercial or Trade Names',widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
	atuse_conc = forms.FloatField(label=mark_safe('"At-Use" Concentration (ppm, &#956;g/mg)'),initial='200')
	choose_use = (('1','Tank Residue (Volumetric)'),('0','Surface Residue (Surface Area)'))
	run_use = forms.ChoiceField(required=True,widget=forms.RadioSelect,label='Calculation Type', choices=choose_use)
	
	vol = forms.FloatField(label='Volume of tank (gal)',initial='4000')
	d = forms.FloatField(label='Cross-sectional diameter of tank (ft)*',initial='6')
	h = forms.FloatField(label='Length of tank (ft)*',initial='19.9')
	sa = forms.FloatField(label=mark_safe('Surface Area of tank (ft<sup>2</sup>)*'),initial='')
	intake_avg = forms.FloatField(label='Average Intake of Food (g/person/day)',initial='125')
	intake_90th = forms.FloatField(label='90th Percentile Intake of Food (g/person/day)',initial='320')

	residue = forms.FloatField(label=mark_safe('Sanitizer Residue (mg/cm<sup>2</sup>)'),initial='1')
	worst_case_est = forms.FloatField(label=mark_safe('"Worst-Case" Estimate of Exposure (cm<sup>2</sup>/person/day)'),initial='4000')