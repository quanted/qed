# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: Jon F.
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe


class vvwmInp_chem(forms.Form):
	# Chemical Tab
    wc_hl_0 = forms.FloatField(required=True,label='Water Column Metabolism Halflife (day)',initial='21')
    w_temp_0 = forms.FloatField(required=True,label=mark_safe('Water Reference Temperature (&deg;C)'),initial='25')
    bm_hl_0 = forms.FloatField(required=True,label='Benthic Metabolism Halflife (day)',initial='75')
    ben_temp_0 = forms.FloatField(required=True,label=mark_safe('Benthic Reference Temperature (&deg;C)'),initial='25')
    ap_hl_0 = forms.FloatField(required=True,label='Aquatic Photolysis Metabolism Halflife (day)',initial='2.0')
    p_ref_0 = forms.FloatField(required=True,label=mark_safe('Photolysis Ref Latitude (&deg;)'),initial='40')
    h_hl_0 = forms.FloatField(required=True,label='Hydrolysis Halflife (day)',initial='')
    mwt_0 = forms.FloatField(required=True,label='MWT',initial='311')
    vp_0 = forms.FloatField(required=True,label='Vapor Pressure (torr)',initial='8e-8')
    sol_0 = forms.FloatField(required=True,label='Solubility (mg/L)',initial='3.3')
    QT = forms.FloatField(required=True,label=mark_safe('EXAMS Q10 Value (eq. 2-133)'),initial='2')

class vvwmInp_chem1(forms.Form):
    wc_hl_1 = forms.FloatField(required=True,label='Water Column Metabolism Halflife (day)',initial='21')
    w_temp_1 = forms.FloatField(required=True,label=mark_safe('Water Reference Temperature (&deg;C)'),initial='25')
    bm_hl_1 = forms.FloatField(required=True,label='Benthic Metabolism Halflife (day)',initial='75')
    ben_temp_1 = forms.FloatField(required=True,label=mark_safe('Benthic Reference Temperature (&deg;C)'),initial='25')
    ap_hl_1 = forms.FloatField(required=True,label='Aquatic Photolysis Metabolism Halflife (day)',initial='2.0')
    p_ref_1 = forms.FloatField(required=True,label=mark_safe('Photolysis Ref Latitude (&deg;)'),initial='40')
    h_hl_1 = forms.FloatField(required=True,label='Hydrolysis Halflife (day)',initial='')
    mwt_1 = forms.FloatField(required=True,label='MWT',initial='311')
    vp_1 = forms.FloatField(required=True,label='Vapor Pressure (torr)',initial='8e-8')
    sol_1 = forms.FloatField(required=True,label='Solubility (mg/L)',initial='3.3')

class vvwmInp_chem2(forms.Form):
    wc_hl_2 = forms.FloatField(required=True,label='Water Column Metabolism Halflife (day)',initial='21')
    w_temp_2 = forms.FloatField(required=True,label=mark_safe('Water Reference Temperature (&deg;C)'),initial='25')
    bm_hl_2 = forms.FloatField(required=True,label='Benthic Metabolism Halflife (day)',initial='75')
    ben_temp_2 = forms.FloatField(required=True,label=mark_safe('Benthic Reference Temperature (&deg;C)'),initial='25')
    ap_hl_2 = forms.FloatField(required=True,label='Aquatic Photolysis Metabolism Halflife (day)',initial='2.0')
    p_ref_2 = forms.FloatField(required=True,label=mark_safe('Photolysis Ref Latitude (&deg;)'),initial='40')
    h_hl_2 = forms.FloatField(required=True,label='Hydrolysis Halflife (day)',initial='')
    mwt_2 = forms.FloatField(required=True,label='MWT',initial='311')
    vp_2 = forms.FloatField(required=True,label='Vapor Pressure (torr)',initial='8e-8')
    sol_2 = forms.FloatField(required=True,label='Solubility (mg/L)',initial='3.3')

class vvwmInp_mcf1(forms.Form):
    convertWC1 = forms.FloatField(required=True,label='Water Column Metabolism')
    convertBen1 = forms.FloatField(required=True,label='Benthic Metabolism')
    convertAP1 = forms.FloatField(required=True,label='Photolysis')
    convertH1 = forms.FloatField(required=True,label='Hydrolysis')

class vvwmInp_mcf2(forms.Form):
    convertWC2 = forms.FloatField(required=True,label='Water Column Metabolism')
    convertBen2 = forms.FloatField(required=True,label='Benthic Metabolism')
    convertAP2 = forms.FloatField(required=True,label='Photolysis')
    convertH2 = forms.FloatField(required=True,label='Hydrolysis')

class vvwmInp_cropland(forms.Form):
    #CropLand Tab
    scenID = forms.FloatField(required=True,label='Scenario ID',initial="CAlettuceSTD")

class vvwmInp_waterbody(forms.Form):
	# Water Body Tab
    SimType = ((0,'EPA Reservoir & Pond'),(4,'EPA Reservoir Only'),(5,'EPA Pond Only'),(6,'Reservoir w/ user averaging'),(1,'Varying Volume'),(2,'Constant Volume (w/o Flowthrough)'),(3,'Constant Volume (w/ Flowthrough)'))
    SimTypeFlag = forms.ChoiceField(required=True,label='Simulation Type:', choices=SimType, initial=0)
    # Pond
    fieldArea_Pond = forms.FloatField(required=True,label=mark_safe('Pond Field Area (m<sup>2</sup>)'), initial="100000")
    wbArea_Pond = forms.FloatField(required=True,label=mark_safe('Pond Water Body Area (m<sup>2</sup>)'), initial="10000")
    depth_0_Pond = forms.FloatField(required=True,label='Pond Initial Water Body Depth (m)', initial="2")
    depth_max_Pond = forms.FloatField(required=True,label='Pond Maximum Water Body Depth (m)', initial="2")
    hyd_len_Pond = forms.FloatField(required=True,label='Pond Hydraulic Length (m)', initial="356.8")
    # Reservoir
    fieldArea_Reservoir = forms.FloatField(required=True,label=mark_safe('Reservoir Field Area (m<sup>2</sup>)'), initial="1728000")
    wbArea_Reservoir = forms.FloatField(required=True,label=mark_safe('Reservoir Water Body Area (m<sup>2</sup>)'), initial="52600")
    depth_0_Reservoir = forms.FloatField(required=True,label='Reservoir Initial Water Body Depth (m)', initial="2.74")
    depth_max_Reservoir = forms.FloatField(required=True,label='Reservoir Maximum Water Body Depth (m)', initial="2.74")
    hyd_len_Reservoir = forms.FloatField(required=True,label='Reservoir Hydraulic Length (m)', initial="600")
    # Custom
    fieldArea_Custom = forms.FloatField(required=True,label=mark_safe('Custom Field Area (m<sup>2</sup>)'), initial="100000")
    wbArea_Custom = forms.FloatField(required=True,label=mark_safe('Custom Water Body Area (m<sup>2</sup>)'), initial="10000")
    depth_0_Custom = forms.FloatField(required=True,label='Custom Initial Water Body Depth (m)', initial="2")
    depth_max_Custom = forms.FloatField(required=True,label='Custom Maximum Water Body Depth (m)', initial="2")
    hyd_len_Custom = forms.FloatField(required=True,label='Custom Hydraulic Length (m)', initial="356.8")
    resAvgBox_Custom = forms.FloatField(required=True,label='')
    
    Burial = ((1,'Burial'),(0,'No Burial'))
    BurialFlag = forms.ChoiceField(required=True,label='Sediment Accounting:', choices=Burial, initial=0)

class vvwmInp_waterbody_WCparms(forms.Form):
    DFAC = forms.FloatField(required=True,label='DFAC',initial='1.19')
    SUSED = forms.FloatField(required=True,label='Water Column SS (mg/L)',initial='30')
    CHL = forms.FloatField(required=True,label='Chlorophyll (mg/L)',initial='0.005')
    FROC1 = forms.FloatField(required=True,label='Water Column foc',initial='0.04')
    DOC1 = forms.FloatField(required=True,label='Water Column DOC',initial='5')
    PLMAS = forms.FloatField(required=True,label='Water Column Biomass',initial='0.4')

class vvwmInp_waterbody_Bparms(forms.Form):
    benthic_depth = forms.FloatField(required=True,label='Benthic Depth (m)',initial='0.05')
    porosity = forms.FloatField(required=True,label='Benthic Porosity (g/g)',initial='0.5')
    bulk_density = forms.FloatField(required=True,label=mark_safe('Bulk Density (g/cm<sup>3</sup>)'),initial='1.35')
    FROC2 = forms.FloatField(required=True,label='Benthic foc',initial='0.04')
    DOC2 = forms.FloatField(required=True,label='Benthic DOC',initial='5')
    BNMAS = forms.FloatField(required=True,label=mark_safe('Benthic Biomass (g/cm<sup>2</sup>)'),initial='0.006')
    PRBEN = forms.FloatField(required=True,label='PRBEN',initial='0.5')
    D_over_dx = forms.FloatField(required=True,label='Mass Xfer Coeff. (m/s)',initial='1e-8')