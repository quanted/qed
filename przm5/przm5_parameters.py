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
    koc_check_choice = ((1,'Koc'), (0,'Kd'))
    koc_check = forms.ChoiceField(required=True, label='Sorption Coefficient Type', choices=koc_check_choice, initial='Koc')
    Koc_0 = forms.FloatField(required=True, label='Sorption Coefficient (mL/g)', initial=200)
    soilHalfLife_0 = forms.FloatField(required=True, label='Soil Halflife (day)', initial=100)
    foliarHalfLife_0 = forms.FloatField(required=True, label='Foliar Halflife (day)', initial=44)
    deg_choice = ((0,'None'), (1,'Degradate 1'), (2,'Degradate 2'))
    deg_check = forms.ChoiceField(required=True, label='Degradate', choices=deg_choice, initial='None')


#Application tab
class przm5Inp_appl(forms.Form):
    water_body_type_check = forms.CharField(initial='Pond')
    fieldSize = forms.FloatField(required=True, label='Area of Field (ha.)', initial=10)
    hydlength = forms.FloatField(required=True, label='Hydraulic Length (m)', initial=356.8)
    app_date_type_choice = ((0,'Absolute'), (1,'Relative'))
    app_date_type = forms.ChoiceField(required=True, label='Application Date Type', choices=app_date_type_choice, initial=0)

    # Eff = forms.FloatField(required=True, label='Eff.', initial=0.95)
    # spray = forms.FloatField(required=True, label='Drift/T', initial=0.05)



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
    NumberOfFactors = forms.ChoiceField(required=True, label='No. of Time-Varing Factors', choices=NumberOfFactors_choice, initial=26)
    rDepthBox = forms.FloatField(required=True, label='R-Depth (cm)', initial=2.0)
    rDeclineBox = forms.FloatField(required=True, label='R-Decline (1/cm)', initial=1.55)
    rBypassBox = forms.FloatField(required=True, label='Efficiency', initial=0.266)
    eDepthBox = forms.FloatField(required=True, label='E-Depth (cm)', initial=0.1)
    eDeclineBox = forms.FloatField(required=True, label='E-Decline (1/cm)', initial=0)
