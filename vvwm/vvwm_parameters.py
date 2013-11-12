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

# From Variables.F90 in the "Fortranvvwm\source" dir

class vvwmInp_chem(forms.Form):
	# Chemical Tab
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    sorp_K = forms.FloatField(required=True,label='Sorption Coefficient (mL/g)',initial='200')
    unit = ((1,'Koc'),(0,'Kd'))
    sorp_K_unit = forms.ChoiceField(required=True,label='Sorption Coefficient Type',choices=unit,initial='Koc')
    wc_hl = forms.FloatField(required=True,label='Water Column Metabolism Halflife (day)',initial='21')
    w_temp = forms.FloatField(required=True,label=mark_safe('Water Reference Temperature (&deg;C)'),initial='25')
    bm_hl = forms.FloatField(required=True,label='Benthic Metabolism Halflife (day)',initial='75')
    ben_temp = forms.FloatField(required=True,label=mark_safe('Benthic Reference Temperature (&deg;C)'),initial='25')
    QT = forms.FloatField(required=True,label=mark_safe('EXAMS Q10 Vallues (eq. 2-133)'),initial='2')

    ap_hl = forms.FloatField(required=True,label='Aquatic Photolysis Metabolism Halflife (day)',initial='2.0')
    p_ref = forms.FloatField(required=True,label=mark_safe('Photolysis Ref Latitude (&deg;)'),initial='40')
    h_hl = forms.FloatField(required=True,label='Hydrolysis Halflife (day)',initial='')

    mwt = forms.FloatField(required=True,label='MWT',initial='311')
    vp = forms.FloatField(required=True,label='Vapor Pressure (torr)',initial='8e-8')
    sol = forms.FloatField(required=True,label='Solubility (mg/L)',initial='3.3')

    # Add Degradate 1 & Degradate 2 options (checkboxes)

class vvwmInp_appl(forms.Form):
    # Applications Tab
    app_n = forms.FloatField(required=True,label='Number of Applications (50 max)')
    dates = (('1','Absolute Dates'),('0','Relative Dates'))
    sorp_K_unit = forms.ChoiceField(required=True,widget=forms.RadioSelect,label='Choose Way of Entering Application Dates', choices=dates)
    app_rate = forms.FloatField(required=True,label='Application Rate (kg/ha)')
    spray = forms.FloatField(required=True,label='Fraction of application to be applied to water body area (decimal)')

class vvwmInp_waterbody(forms.Form):
	# Water Body Tab
    afield = forms.FloatField(required=True,label=mark_safe('Field Area (m<sup>2</sup>)'))
    area = forms.FloatField(required=True,label=mark_safe('Water Body Area (m<sup>2</sup>)'))
    depth_0 = forms.FloatField(required=True,label='Initial Water Body Depth (m)')
    depth_max = forms.FloatField(required=True,label='Maximum Water Body Depth (m)')
    # Hydraulic Length (m)??  Initial=600
    SimType = ((1,'Varying Volume'),(2,'Constant Volume (no Flowthrough)'),(3,'Constant Volume (with Flowthrough)'))
    SimTypeFlag = forms.ChoiceField(required=True,label='Simulation Type:', choices=SimType, initial='Varying Volume')
    
    Burial = ((1,'Burial'),(0,'No Burial'))
    BurialFlag = forms.ChoiceField(required=True,label='Sediment Accounting:', choices=Burial, initial='No Burial')
    D_over_dx = forms.FloatField(required=True,label='Mass Xfer Coeff. (m/s)',initial='1e-8')
    PRBEN = forms.FloatField(required=True,label='PRBEN',initial='0.5')

    benthic_depth = forms.FloatField(required=True,label='Benthic Depth (m)',initial='0.05')
    porosity = forms.FloatField(required=True,label='Benthic Porosity (g/g)',initial='0.5')
    bulk_density = forms.FloatField(required=True,label=mark_safe('Bulk Density (g/cm<sup>3</sup>)'),initial='1.35')
    FROC2 = forms.FloatField(required=True,label='Benthic foc',initial='0.04')
    DOC2 = forms.FloatField(required=True,label='Benthic DOC',initial='5')
    BNMAS = forms.FloatField(required=True,label=mark_safe('Benthic Biomass (g/cm<sup>2</sup>)'),initial='0.006')
    DFAC = forms.FloatField(required=True,label='DFAC',initial='1.19')
    SUSED = forms.FloatField(required=True,label='Water Column SS (mg/L)',initial='30')
    CHL = forms.FloatField(required=True,label='Chlorophyll (mg/L)',initial='0.005')
    FROC1 = forms.FloatField(required=True,label='Water Column foc',initial='0.04')
    DOC1 = forms.FloatField(required=True,label='Water Column DOC',initial='5')
    PLMAS = forms.FloatField(required=True,label='Water Column Biomass',initial='0.4')

    # Do not know what these are:
	# CLOUD = 0
	# minimum_depth = 0.00001

 #    xAerobic
 #    xBenthic
 #    xPhoto
 #    xHydro

 #    flow_averaging


def form():
    out = vvwmInp_chem()
    return out