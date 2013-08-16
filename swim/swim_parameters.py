# -*- coding: utf-8 -*-
"""
Created on 2013-08-14

@author: Tao Hong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe


class swimInp_chem(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 2}), label='Chemical name')
    log_kow = forms.FloatField(required=True, label="Log Kow", initial=-0.66)
    mw = forms.FloatField(required=True, label="Molecular weight of substance (g/mol)", initial=197)
    hlc = forms.FloatField(required=True, label=mark_safe("Henry's law constant (atm-m<sup>3</sup>/mole)"), initial=1.27e-7)
    r = forms.FloatField(required=True, label=mark_safe("Gas constant (atm-m<sup>3</sup>/mole-K)"), initial=8.19e-5)
    T = forms.FloatField(required=True, label=mark_safe("Ambient air temp (<sup>o</sup>C)"), initial=25)
    cw = forms.FloatField(required=True, label="Water concentration (mg/L)", initial=3.0)
    noael = forms.FloatField(required=True, label="NOAEL (mg/kg/day)", initial=10.0)

class swimInp_ad(forms.Form):
    bw_aa = forms.FloatField(required=True, label="Body weight all adult (kg)", initial=70)
    bw_fa = forms.FloatField(required=True, label="Body weight female adult (kg)", initial=60)
    sa_a_c = forms.FloatField(required=True, label=mark_safe("Surface area exposed (Competitive, cm<sup>2</sup>)"), initial=18200)
    sa_a_nc = forms.FloatField(required=True, label=mark_safe("Surface area exposed (Non-Competitive, cm<sup>2</sup>)"), initial=18200)
    et_a_c = forms.FloatField(required=True, label="Exposure time (Competitive, hr/day)", initial=3)
    et_a_nc = forms.FloatField(required=True, label="Exposure time (Non-Competitive, hr/day)", initial=1)
    ir_a_c = forms.FloatField(required=True, label="Inhalation rate of pool water (Competitive, L/hr)", initial=3.2)
    ir_a_nc = forms.FloatField(required=True, label="Inhalation rate of pool water (Non-Competitive, L/hr)", initial=1.0)
    igr_a_c = forms.FloatField(required=True, label="Ingestion rate of pool water (Competitive, L/hr)", initial=0.0125)
    igr_a_nc = forms.FloatField(required=True, label="Ingestion rate of pool water (Non-Competitive, L/hr)", initial=0.0125)

class swimInp_c1(forms.Form):
    bw_c1 = forms.FloatField(required=True, label="Body weight (kg)", initial=29)
    sa_c1_c = forms.FloatField(required=True, label=mark_safe("Surface area exposed (Competitive, cm<sup>2</sup>)"), initial=10500)
    sa_c1_nc = forms.FloatField(required=True, label=mark_safe("Surface area exposed (Non-Competitive, cm<sup>2</sup>)"), initial=10500)
    et_c1_c = forms.FloatField(required=True, label="Exposure time (Competitive, hr/day)", initial=1)
    et_c1_nc = forms.FloatField(required=True, label="Exposure time (Non-Competitive, hr/day)", initial=1)
    ir_c1_c = forms.FloatField(required=True, label="Inhalation rate of pool water (Competitive, L/hr)", initial=2.5)
    ir_c1_nc = forms.FloatField(required=True, label="Inhalation rate of pool water (Non-Competitive, L/hr)", initial=1.3)
    igr_c1_c = forms.FloatField(required=True, label="Ingestion rate of pool water (Competitive, L/hr)", initial=0.05)
    igr_c1_nc = forms.FloatField(required=True, label="Ingestion rate of pool water (Non-Competitive, L/hr)", initial=0.05)

class swimInp_c2(forms.Form):
    bw_c2 = forms.FloatField(required=True, label="Body weight (kg)", initial=54)
    sa_c2_c = forms.FloatField(required=True, label=mark_safe("Surface area exposed (Competitive, cm<sup>2</sup>)"), initial=15700)
    sa_c2_nc = forms.FloatField(required=True, label=mark_safe("Surface area exposed (Non-Competitive, cm<sup>2</sup>)"), initial=15700)
    et_c2_c = forms.FloatField(required=True, label="Exposure time (Competitive, hr/day)", initial=2)
    et_c2_nc = forms.FloatField(required=True, label="Exposure time (Non-Competitive, hr/day)", initial=1)
    ir_c2_c = forms.FloatField(required=True, label="Inhalation rate of pool water (Competitive, L/hr)", initial=2.9)
    ir_c2_nc = forms.FloatField(required=True, label="Inhalation rate of pool water (Non-Competitive, L/hr)", initial=1.5)
    igr_c2_c = forms.FloatField(required=True, label="Ingestion Rate of pool water (Competitive, L/hr)", initial=0.025)
    igr_c2_nc = forms.FloatField(required=True, label="Ingestion Rate of pool water (Non-Competitive, L/hr)", initial=0.05)
