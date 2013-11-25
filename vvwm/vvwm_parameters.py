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
    # Add Degradate 1 & Degradate 2 options (checkboxes)
        # if no checks, deg = 1; if deg1 'checked', deg = 2; if deg2 'checked', deg = 2
    sorp_K = forms.FloatField(required=True,label='Sorption Coefficient (mL/g)',initial='200')
    unit = ((1,'Koc'),(0,'Kd'))
    sorp_K_unit = forms.ChoiceField(required=True,label='Sorption Coefficient Type',choices=unit,initial='Koc')
    wc_hl = forms.FloatField(required=True,label='Water Column Metabolism Halflife (day)',initial='21')
    w_temp = forms.FloatField(required=True,label=mark_safe('Water Reference Temperature (&deg;C)'),initial='25')
    bm_hl = forms.FloatField(required=True,label='Benthic Metabolism Halflife (day)',initial='75')
    ben_temp = forms.FloatField(required=True,label=mark_safe('Benthic Reference Temperature (&deg;C)'),initial='25')

    ap_hl = forms.FloatField(required=True,label='Aquatic Photolysis Metabolism Halflife (day)',initial='2.0')
    p_ref = forms.FloatField(required=True,label=mark_safe('Photolysis Ref Latitude (&deg;)'),initial='40')
    h_hl = forms.FloatField(required=True,label='Hydrolysis Halflife (day)',initial='')
    s_hl = forms.FloatField(required=True,label='Soil Halflife (day)',initial='100')
    s_ref = forms.FloatField(required=True,label=mark_safe('Soil Reference Temp (&deg;C)'),initial='25')
    f_hl = forms.FloatField(required=True,label='Foliar Halflife (day)',initial='')

    mwt = forms.FloatField(required=True,label='MWT',initial='311')
    vp = forms.FloatField(required=True,label='Vapor Pressure (torr)',initial='8e-8')
    sol = forms.FloatField(required=True,label='Solubility (mg/L)',initial='3.3')

    QT = forms.FloatField(required=True,label=mark_safe('EXAMS Q10 Value (eq. 2-133)'),initial='2')
    # Molar Conversion Factors
    # wc_mcf = 
    # ben_mcf = 
    # p_mcf = 
    # h_mcf = 
    # s_mcf = 
    # f_mcf = 

class vvwmInp_appl(forms.Form):
    # Applications Tab
    app_nOpt =(('','Select Value'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
             ('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),
             ('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),
             ('31','31'),('32','23'),('33','33'),('34','34'),('35','35'),('36','36'),('37','37'),('38','38'),('39','39'),('40','40'),
             ('41','41'),('42','24'),('43','43'),('44','44'),('45','45'),('46','46'),('47','47'),('48','48'),('49','49'),('50','50'))
    app_n = forms.ChoiceField(required=True,choices=app_nOpt, label='Number of Applications', initial='')
    dates = (('1','Absolute Dates'),('0','Relative Dates'))
    sorp_K_unit = forms.ChoiceField(required=True,label='Choose Way of Entering Application Dates', choices=dates)
    app_rate = forms.FloatField(required=True,label='Application Rate (kg/ha)')
    spray = forms.FloatField(required=True,label='Fraction of application to be applied to water body area (decimal)')

class vvwmInp_cropland(forms.Form):
    #CropLand Tab
    scenID = forms.FloatField(required=True,label='Scenario ID')

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




# def form():
#     out = vvwmInp_chem()
#     return out