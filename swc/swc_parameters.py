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

class swcInp_chem(forms.Form):
	# Chemical Tab
    chemical_name = forms.CharField(label='Parent Chemical Name', widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
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

class swcInp_chem0(forms.Form):
    n_chemSel = (('1','Degradate 1'), ('2','Degradate 2'))
    n_chem = forms.MultipleChoiceField(label='Degradates?', choices=n_chemSel, widget=forms.CheckboxSelectMultiple())

class swcInp_chem1(forms.Form):
    #Degradate 1
    # sorp_K_1 = forms.FloatField(required=True,label='Sorption Coefficient (mL/g)')
    # unit_1 = ((1,'Koc'),(0,'Kd'))
    # sorp_K_unit_1 = forms.ChoiceField(required=True,label='Sorption Coefficient Type',choices=unit_1)
    wc_hl_1 = forms.FloatField(required=True,label='Water Column Metabolism Halflife (day)')
    w_temp_1 = forms.FloatField(required=True,label=mark_safe('Water Reference Temperature (&deg;C)'))
    bm_hl_1 = forms.FloatField(required=True,label='Benthic Metabolism Halflife (day)')
    ben_temp_1 = forms.FloatField(required=True,label=mark_safe('Benthic Reference Temperature (&deg;C)'))
    ap_hl_1 = forms.FloatField(required=True,label='Aquatic Photolysis Metabolism Halflife (day)')
    p_ref_1 = forms.FloatField(required=True,label=mark_safe('Photolysis Ref Latitude (&deg;)'))
    h_hl_1 = forms.FloatField(required=True,label='Hydrolysis Halflife (day)')
    # s_hl_1 = forms.FloatField(required=True,label='Soil Halflife (day)')
    # s_ref_1 = forms.FloatField(required=True,label=mark_safe('Soil Reference Temp (&deg;C)'))
    # f_hl_1 = forms.FloatField(required=True,label='Foliar Halflife (day)')
    mwt_1 = forms.FloatField(required=True,label='MWT')
    vp_1 = forms.FloatField(required=True,label='Vapor Pressure (torr)')
    sol_1 = forms.FloatField(required=True,label='Solubility (mg/L)')

class swcInp_mcf1(forms.Form):
    # Molar Conversion Factors 1
    wc_mcf_1 = forms.FloatField(required=True,label='Water Column Metabolism')
    ben_mcf_1 = forms.FloatField(required=True,label='Benthic Metabolism')
    p_mcf_1 = forms.FloatField(required=True,label='Photolysis')
    h_mcf_1 = forms.FloatField(required=True,label='Hydrolysis')
    s_mcf_1 = forms.FloatField(required=True,label='Soil')
    f_mcf_1 = forms.FloatField(required=True,label='Foliar')

class swcInp_chem2(forms.Form):
    #Degradate 2
    # sorp_K_2 = forms.FloatField(required=True,label='Sorption Coefficient (mL/g)')
    # unit_2 = ((1,'Koc'),(0,'Kd'))
    # sorp_K_unit_2 = forms.ChoiceField(required=True,label='Sorption Coefficient Type',choices=unit_2)
    wc_hl_2 = forms.FloatField(required=True,label='Water Column Metabolism Halflife (day)')
    w_temp_2 = forms.FloatField(required=True,label=mark_safe('Water Reference Temperature (&deg;C)'))
    bm_hl_2 = forms.FloatField(required=True,label='Benthic Metabolism Halflife (day)')
    ben_temp_2 = forms.FloatField(required=True,label=mark_safe('Benthic Reference Temperature (&deg;C)'))
    ap_hl_2 = forms.FloatField(required=True,label='Aquatic Photolysis Metabolism Halflife (day)')
    p_ref_2 = forms.FloatField(required=True,label=mark_safe('Photolysis Ref Latitude (&deg;)'))
    h_hl_2 = forms.FloatField(required=True,label='Hydrolysis Halflife (day)')
    # s_hl_2 = forms.FloatField(required=True,label='Soil Halflife (day)')
    # s_ref_2 = forms.FloatField(required=True,label=mark_safe('Soil Reference Temp (&deg;C)'))
    # f_hl_2 = forms.FloatField(required=True,label='Foliar Halflife (day)')
    mwt_2 = forms.FloatField(required=True,label='MWT')
    vp_2 = forms.FloatField(required=True,label='Vapor Pressure (torr)')
    sol_2 = forms.FloatField(required=True,label='Solubility (mg/L)')

class swcInp_mcf2(forms.Form):
    # Molar Conversion Factors 2
    wc_mcf_2 = forms.FloatField(required=True,label='Water Column Metabolism')
    ben_mcf_2 = forms.FloatField(required=True,label='Benthic Metabolism')
    p_mcf_2 = forms.FloatField(required=True,label='Photolysis')
    h_mcf_2 = forms.FloatField(required=True,label='Hydrolysis')
    s_mcf_2 = forms.FloatField(required=True,label='Soil')
    f_mcf_2 = forms.FloatField(required=True,label='Foliar')
    deg2_srcSel = ((1,'Degradate 1'),(0,'Parent'))
    deg2_src = forms.ChoiceField(widget=forms.RadioSelect(), choices=deg2_srcSel, label='Source of Degradate 2', initial=1)

class swcInp_appl(forms.Form):
    # Applications Tab
    datesSel = (('1','Absolute Dates'),('0','Relative Dates'))
    dates = forms.ChoiceField(required=True,label='Choose Way of Entering Application Dates', choices=datesSel)
    app_nOpt =(('','Select Value'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
             ('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),
             ('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),
             ('31','31'),('32','23'),('33','33'),('34','34'),('35','35'),('36','36'),('37','37'),('38','38'),('39','39'),('40','40'),
             ('41','41'),('42','24'),('43','43'),('44','44'),('45','45'),('46','46'),('47','47'),('48','48'),('49','49'),('50','50'))
    app_n = forms.ChoiceField(required=True,choices=app_nOpt, label='Number of Applications', initial='')
    specifyYearsSel = (('1','Yes'), ('0','No'))
    specifyYears = forms.ChoiceField(label='Specify Years?', choices=specifyYearsSel, initial='0')
    
class swcInp_cropland(forms.Form):
	# Crop/Land Tab
    scenID = forms.FloatField(required=True,label='Scenario ID')

    
class swcInp_runoff(forms.Form):
# 	# Runoff Tab
    temp = forms.FloatField(required=True,label='Temporary Runoff Tab')

    
class swcInp_waterbody(forms.Form):
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
