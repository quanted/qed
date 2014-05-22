# -*- coding: utf-8 -*-
"""
Created on 11/07/2013

@author: Tao Hong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.utils.safestring import mark_safe


#Chemical tab
class przm5Inp_chem(forms.Form):
    # deg_choice = ((0,'None'), (1,'Degradate 1'), (2,'Degradate 2'))
    # deg_check = forms.ChoiceField(required=True, label='Degradate', choices=deg_choice, initial='None')
    koc_check_choice = ((1,'Koc'), (0,'Kd'))
    koc_check = forms.ChoiceField(required=True, label='Sorption Coefficient Type', choices=koc_check_choice, initial='Koc')
    Koc_0 = forms.FloatField(required=True, label='Sorption Coefficient (mL/g)', initial=200)
    soilHalfLife_0 = forms.FloatField(required=True, label='Soil Halflife (day)', initial=100)
    # Below was changed by Jon F. (soilHalfLife_ref  -> soilHalfLifeRef)
    soilHalfLifeRef_0 = forms.FloatField(required=True,label=mark_safe('Soil Reference Temp (&deg;C)'),initial=25)
    foliarHalfLife_0 = forms.FloatField(required=True, label='Foliar Halflife (day)', initial=44)

class przm5Inp_chem0(forms.Form):
    deg_choice = (('0','None'), ('1','1 Degradate'), ('2','2 Degradates'))
    deg_check = forms.ChoiceField(required=True, label='Number of Degradates?', choices=deg_choice, initial=0)

class przm5Inp_chem1(forms.Form):
    #Degradate 1
    Koc_1 = forms.FloatField(required=True,label='Sorption Coefficient (mL/g)', initial=200)
    # unit_1 = ((1,'Koc'),(0,'Kd'))
    # sorp_K_unit_1 = forms.ChoiceField(required=True,label='Sorption Coefficient Type',choices=unit_1)
    soilHalfLife_1 = forms.FloatField(required=True,label='Soil Halflife (day)', initial=100)
    soilHalfLifeRef_1 = forms.FloatField(required=True,label=mark_safe('Soil Reference Temp (&deg;C)'), initial=25)
    foliarHalfLife_1 = forms.FloatField(required=True,label='Foliar Halflife (day)', initial=44)

class przm5Inp_mcf1(forms.Form):
    # Molar Conversion Factors 1
    convertSoil1 = forms.FloatField(required=True,label='Soil', initial=0.70)
    convert_Foliar1 = forms.FloatField(required=True,label='Foliar', initial=0.82)

class przm5Inp_chem2(forms.Form):
    #Degradate 2
    Koc_2 = forms.FloatField(required=True,label='Sorption Coefficient (mL/g)', initial=200)
    # unit_2 = ((1,'Koc'),(0,'Kd'))
    # sorp_K_unit_2 = forms.ChoiceField(required=True,label='Sorption Coefficient Type',choices=unit_2)
    soilHalfLife_2 = forms.FloatField(required=True,label='Soil Halflife (day)', initial=100)
    soilHalfLifeRef_2 = forms.FloatField(required=True,label=mark_safe('Soil Reference Temp (&deg;C)'), initial=25)
    foliarHalfLife_2 = forms.FloatField(required=True,label='Foliar Halflife (day)', initial=44)

class przm5Inp_mcf2(forms.Form):
    # Molar Conversion Factors 2

    # Removed because this isn't in the SWC anymore
    deg2_srcSel = ((1,'Degradate 1'),(0,'Parent'))
    deg2_source = forms.ChoiceField(required=True, choices=deg2_srcSel, label='Source of Degradate 2', initial=1)
    convertSoil2 = forms.FloatField(required=True,label='Soil', initial=0.80)
    convert_Foliar2 = forms.FloatField(required=True,label='Foliar')

#Application tab
class przm5Inp_appl(forms.Form):
    # water_body_type_check = forms.CharField(initial='Pond')
    # Eff = forms.FloatField(required=True, label='Eff.', initial=0.95)
    # spray = forms.FloatField(required=True, label='Drift/T', initial=0.05)

    app_date_type_choice = (('0','Absolute Dates'),('1','Relative Dates'))
    app_date_type = forms.ChoiceField(required=True,label='Choose Way of Entering Application Dates', choices=app_date_type_choice)
    app_nOpt =(('','Select Value'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
             ('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),
             ('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),
             ('31','31'),('32','23'),('33','33'),('34','34'),('35','35'),('36','36'),('37','37'),('38','38'),('39','39'),('40','40'),
             ('41','41'),('42','24'),('43','43'),('44','44'),('45','45'),('46','46'),('47','47'),('48','48'),('49','49'),('50','50'))
    noa = forms.ChoiceField(required=True,choices=app_nOpt, label='Number of Applications', initial='')
    specifyYearsSel = (('1','Yes'), ('0','No'))
    specifyYears = forms.ChoiceField(label='Specify Years?', choices=specifyYearsSel, initial='0')
    pond_res_customSel = ((1,'Pond'), (2,'Reservoir'), (3,'Custom'))
    pond_res_custom = forms.ChoiceField(label='Enter Eff. & Drift/T for', choices=pond_res_customSel, initial=1)

#Crop/land tab
class przm5Inp_cropland(forms.Form):
    dvf_choice = (('','Make a Selection'), ('test.dvf','test.dvf'))
    dvf_file = forms.ChoiceField(required=True, label='Weather File', choices=dvf_choice, initial='test.dvf')
    Emerge_text=forms.CharField(label='Emerge (DD/MM)', initial='16/02')
    Mature_text=forms.CharField(label='Mature (DD/MM)', initial='05/05')
    Harvest_text=forms.CharField(label='Harvest (DD/MM)', initial='12/05')
    pfac = forms.FloatField(required=True, label='Pan Factor', initial=0.79)
    snowmelt = forms.FloatField(required=True, label='Snowmelt Factor', initial=0.00)
    evapDepth = forms.FloatField(required=True, label='Evaportation Depth', initial=17.5)
    rootDepth = forms.FloatField(required=True, label='Root Depth (cm)', initial=12)
    canopyCover = forms.FloatField(required=True, label='Canopy Cover (%)', initial=90)
    canopyHeight = forms.FloatField(required=True, label='Canopy Height (cm)', initial=30)
    canopyHoldup = forms.FloatField(required=True, label='Canopy Holdup (cm)', initial=0.25)
    irr_choice = ((0,'None'), (1,'Over Canopy'), (2,'Under Canopy'))
    irflag = forms.ChoiceField(required=True, label='Irrigation', choices=irr_choice, initial='None')
    # temp_choice = ((0,'No'), (1,'Yes'))
    # tempflag = forms.ChoiceField(required=True, label='Simulate Temperature', choices=temp_choice, initial='No')
    fleach = forms.FloatField(required=True, label='Extra Water Fraction', initial=0.96)
    depletion = forms.FloatField(required=True, label='Allowed Depletion', initial=0.97)
    rateIrrig = forms.FloatField(required=True, label='Max Rate', initial=0.98)
    # albedo = forms.FloatField(required=True, label='Albedo', initial=0.40)
    # bcTemp = forms.FloatField(required=True, label='Lower BC Temperature', initial=23)
    post_choice = ((1,'Surface Applied'), (2,'Removed'), (3,'Left as Foliage'))
    PestDispHarvest = forms.ChoiceField(required=True, label='Post-Harvest Foliage', choices=post_choice, initial='Surface Applied')


#Runoff tab
class przm5Inp_runoff(forms.Form):
    uslek = forms.FloatField(required=True, label='USLE K', initial=0.37)
    uslels = forms.FloatField(required=True, label='USLE LS', initial=1.34)
    uslep = forms.FloatField(required=True, label='USLE P', initial=0.5)
    ireg = forms.FloatField(required=True, label='IREG', initial=1)
    slope = forms.FloatField(required=True, label='Slope (%)', initial=6)
    NumberOfFactors_choice = ((26,26), (27,27))
    # NumberOfFactors = forms.ChoiceField(required=True, label='No. of Time-Varing Factors', choices=NumberOfFactors_choice, initial=26)
    rDepthBox = forms.FloatField(required=True, label='R-Depth (cm)', initial=2.0)
    rDeclineBox = forms.FloatField(required=True, label='R-Decline (1/cm)', initial=1.55)
    rBypassBox = forms.FloatField(required=True, label='Efficiency', initial=0.266)
    eDepthBox = forms.FloatField(required=True, label='E-Depth (cm)', initial=0.1)
    eDeclineBox = forms.FloatField(required=True, label='E-Decline (1/cm)', initial=0)


#Water Body tab
class przm5Inp_waterbody(forms.Form):
    fieldSize = forms.FloatField(required=True, label='Area of Field (ha.)', initial=10)
    hydlength = forms.FloatField(required=True, label='Hydraulic Length (m)', initial=356.8)
