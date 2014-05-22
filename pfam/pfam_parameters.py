# -*- coding: utf-8 -*-
"""
Created on Feb 14 2013

@author: THong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.utils.safestring import mark_safe

weather_CHOICES=(('','Make a selection'),('wTest','test1'))

class PFAMInp_chem(forms.Form):
    wat_hl = forms.FloatField(required=True,label='Water Column Half life (days)', initial=30)
    wat_t = forms.FloatField(required=True,label=mark_safe('@Temperature (&#8451)'), initial=20)
    ben_hl = forms.FloatField(required=True,label='Benthic Compartment Half Life (days)', initial=65)
    ben_t = forms.FloatField(required=True,label=mark_safe('@Temperature (&#8451)'), initial=20)
    unf_hl = forms.FloatField(required=True,label='Unflooded Soil Half Life (days)', initial=61)
    unf_t = forms.FloatField(required=True,label=mark_safe('@Temperature (&#8451)'), initial=20)
    aqu_hl = forms.FloatField(required=True,label='Aqueous Near-Surface Photolysis Half Life (days)', initial=2.5)
    aqu_t = forms.FloatField(required=True,label=mark_safe('@Degrees Latitude'), initial=40)
    hyd_hl = forms.FloatField(required=True,label='Hydrolysis Half Life (days)', initial=79)
    mw = forms.FloatField(required=True,label='Molecular Weight (g/mol)', initial=202)
    vp = forms.FloatField(required=True,label='Vapor Pressure (torr)', initial=1.3e-6)
    sol = forms.FloatField(required=True,label='Solubility (mg/l)', initial=100)
    koc = forms.FloatField(required=True,label='Koc (ml/g)', initial=50)
    hea_h = forms.FloatField(required=True,label='Heat of Henry (J/mol)', initial=20000)
    hea_r_t = forms.FloatField(required=True,label=mark_safe('Henry Reference Temperature (&#8451)'), initial=20)
    
class PFAMInp_loc(forms.Form):
    weather= forms.ChoiceField(required=True,label='Weather File', choices=weather_CHOICES, initial='Make a selection')
    wea_l = forms.FloatField(required=True,label='@Latitude (for Photolysis Calculations)', initial=28)
    
class PFAMInp_cro(forms.Form):
    zero_height_ref= forms.DateField(required=True,label='Zero Height Reference (MM/DD)', initial='04/01')
    days_zero_full = forms.IntegerField(required=True,label='Days from Zero Height to Full Height', initial=60)
    days_zero_removal = forms.IntegerField(required=True,label='Days from Zero Height to Removal', initial=150)
    max_frac_cov = forms.FloatField(required=True,label='Maximum Fractional Area Coverage', initial=0.99)
    
class PFAMInp_phy(forms.Form):
    mas_tras_cof = forms.FloatField(required=True,label='Mass Transfer Coefficient (m/s)', initial=1e-8)
    leak = forms.FloatField(required=True,label='Leakage (m/d)', initial=0)
    ref_d = forms.FloatField(required=True,label='Reference Depth (m)', initial=0.1)
    ben_d = forms.FloatField(required=True,label='Benthic Depth (m)', initial=0.05)
    ben_por = forms.FloatField(required=True,label='Benthic Porosity', initial=0.5)
    dry_bkd = forms.FloatField(required=True,label=mark_safe('Dry Bulk Density (g/cm<sup>3</sup>)'), initial=1.35)
    foc_wat = forms.FloatField(required=True,label='Foc Water Column on SS', initial=0.04)
    foc_ben = forms.FloatField(required=True,label='Foc Benthic', initial=0.01)
    ss = forms.FloatField(required=True,label='SS (mg/L)', initial=30)
    wat_c_doc = forms.FloatField(required=True,label='Water column DOC (mg/L)', initial=5.0)
    chl = forms.FloatField(required=True,label='Chlorophyll, CHL (mg/L)', initial=0.005)
    dfac = forms.FloatField(required=True,label='Dfac', initial=1.19)
    q10 = forms.FloatField(required=True,label='Q10', initial=2)
class PFAMInp_out(forms.Form):
    area_app = forms.FloatField(required=True,label=mark_safe('Area of Application (m<sup>2</sup>)'), initial=20000)
