# -*- coding: utf-8 -*-
"""
@author: Taohong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models

Scenario_select = (('','Select a scenario'),('CA Almonds MLRA-17', 'CA Almonds MLRA-17'), ('CA Citrus   MLRA-17', 'CA Citrus   MLRA-17'), ('CA Cotton   MLRA-17', 'CA Cotton   MLRA-17'), ('CA Grape  MLRA-17', 'CA Grape  MLRA-17'), ('CA Lettuce  MLRA-14', 'CA Lettuce  MLRA-14'), ('CA Onions MLRA-17', 'CA Onions MLRA-17'), ('CA Tomato MLRA-17', 'CA Tomato MLRA-17'), ('FL Avocado MLRA-156A', 'FL Avocado MLRA-156A'), ('FL Cabbage   MLRA-155', 'FL Cabbage   MLRA-155'), ('FL Carrots MLRA-156B', 'FL Carrots MLRA-156B'), ('FL Citrus   MLRA-156A', 'FL Citrus   MLRA-156A'), ('FL Cucumber   MLRA-156A', 'FL Cucumber   MLRA-156A'), ('FL Peppers MLRA-156A', 'FL Peppers MLRA-156A'), ('FL Strawberry   MLRA-155', 'FL Strawberry   MLRA-155'), ('FL Sugarcane   MLRA-156A', 'FL Sugarcane   MLRA-156A'), ('FL Tomato   MLRA-155', 'FL Tomato   MLRA-155'), ('FL Turf  MLRA-155', 'FL Turf  MLRA-155'), ('GA Onions MLRA-153A/133A', 'GA Onions MLRA-153A/133A'), ('GA Peach   MLRA-133A', 'GA Peach   MLRA-133A'), ('GA Pecan   MLRA-133A', 'GA Pecan   MLRA-133A'), ('ID Potato   MLRA-11B', 'ID Potato   MLRA-11B'), ('IL Corn   MLRA-108', 'IL Corn   MLRA-108'), ('KS Sorghum   MLRA-112', 'KS Sorghum   MLRA-112'), ('LA Sugarcane   MLRA-131', 'LA Sugarcane   MLRA-131'), ('ME Potato   MLRA-146', 'ME Potato   MLRA-146'), ('MI Asparagus MLRA-96', 'MI Asparagus MLRA-96'), ('MI Beans MLRA-99', 'MI Beans MLRA-99'), ('MI Cherry   MLRA-96', 'MI Cherry   MLRA-96'), ('MN Sugarbeet   MLRA-56', 'MN Sugarbeet   MLRA-56'), ('MS Corn   MLRA-134', 'MS Corn   MLRA-134'), ('MS Cotton   MLRA-134', 'MS Cotton   MLRA-134'), ('MS Soybean   MLRA-134', 'MS Soybean   MLRA-134'), ('NC Apple   MLRA-130', 'NC Apple   MLRA-130'), ('NC Corn - E   MLRA-153A', 'NC Corn - E   MLRA-153A'), ('NC Cotton   MLRA-133A', 'NC Cotton   MLRA-133A'), ('NC Peanut   MLRA-153A', 'NC Peanut   MLRA-153A'), ('NC Sweet Potato MLRA-133', 'NC Sweet Potato MLRA-133'), ('NC Tobacco   MLRA-133A', 'NC Tobacco   MLRA-133A'), ('ND Canola   MLRA-55A', 'ND Canola   MLRA-55A'), ('ND Wheat   MLRA-56', 'ND Wheat   MLRA-56'), ('NY Grape   MLRA-100/101', 'NY Grape   MLRA-100/101'), ('OH Corn   MLRA-111', 'OH Corn   MLRA-111'), ('OR Apple   MLRA-2', 'OR Apple   MLRA-2'), ('OR Christmas Trees  MLRA-2', 'OR Christmas Trees  MLRA-2'), ('OR Filberts   MLRA-2', 'OR Filberts   MLRA-2'), ('OR Grass Seed   MLRA-2', 'OR Grass Seed   MLRA-2'), ('OR Hops   MLRA-2', 'OR Hops   MLRA-2'), ('OR Mint   MLRA-2', 'OR Mint   MLRA-2'), ('PA Apple   MLRA-148', 'PA Apple   MLRA-148'), ('PA Corn   MLRA-148', 'PA Corn   MLRA-148'), ('PA Turf  MLRA-148', 'PA Turf  MLRA-148'), ('PR Coffee MLRA-270', 'PR Coffee MLRA-270'))
Ap_select =(('','Select an application timing'),('1','Relative to planting'),('2','Relative to emergence'),('3','Relative to maturity'),('4','Relative to harvest'),('5','Enter your own dates'))
Ap_m_select = (('','Select an application method'),('1','Aerial'),('2','Ground Sprayer'),('3','Airblast'),('4','Other equipment'))
Unit_select = (('1','kg/ha'),('2','lb/acre'))
CAM_1_select = (('2','2-Interception based on crop canopy'),('9','9-Linear foliar based on crop canop'))
CAM_2_select = (('1', '1-Soil applied (4cm incorporation, linearly decreasing with depth)'), ('2','2-Interception based on crop canopy'),('9','9-Linear foliar based on crop canop'))
CAM_3_select = (('2','2-Interception based on crop canopy'),('9','9-Linear foliar based on crop canop'))
CAM_4_select = (('1','1-Soil applied (4cm incorporation, linearly decreasing with depth)'),('4','4-Soil applied (user-defined incorporation, uniform with depth)'),('5','5-Soil applied (user-defined incorporation, linearly increasing with depth)'),('6','6-Soil applied (user-defined incorporation, linearly decreasing with depth)'),('7','7-Soil applied, T-Band granular application'),('8','8-Soil applied, chemical incorporated depth specified by user'))
NOA_select =(('','Select the number of applications'),('1','1'),('2','2'),('3','3'),('4','4'))


class PRZMInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2, 'readonly':'readonly'}), initial='Forchlorfenuron')#Alachlor
    NOA = forms.ChoiceField(required=True,choices=NOA_select, label='Number of applications', initial='')
    Scenarios = forms.ChoiceField(required=True,choices=Scenario_select, label='Standard OPP/EFED Scenarios', initial='')
    Unit = forms.ChoiceField(widget=forms.RadioSelect(), choices=Unit_select, label='Application unit')
    
    Apt=forms.ChoiceField(required=True,choices=Ap_select, label='Application timing 1')
    # Date_apt=forms.CharField(label='Application Date (MM/DD)', initial='05/10')
    DayRe = forms.FloatField(required=True,label='Days relevant to the application 1',initial=0)
    Ap_m = forms.ChoiceField(required=True,choices=Ap_m_select, label='Application method 1')  
    Ar = forms.FloatField(required=True,label='Application rate 1')#,initial=1
    CAM_1 = forms.ChoiceField(required=True,choices=CAM_1_select, label='Chemical application Method (CAM)') 
    CAM_2 = forms.ChoiceField(required=True,choices=CAM_2_select, label='Chemical application Method (CAM)') 
    CAM_3 = forms.ChoiceField(required=True,choices=CAM_3_select, label='Chemical application Method (CAM)') 
    CAM_4 = forms.ChoiceField(required=True,choices=CAM_4_select, label='Chemical application Method (CAM)')
    DEPI = forms.FloatField(required=True,label='Incorporation depth (DEPI, cm) ',initial=4.00)
    
    
#    DDMM = forms.FloatField(required=True,label='Days and months',initial='0101')
    
#    Modeled_Start = forms.FloatField(required=True,label='Simulation Start Year',initial=1961)
#    Modeled_end = forms.FloatField(required=True,label='Simulation End Year',initial=1990)
#    Modeled_zones = forms.FloatField(required=True,label='Modeled zones',initial=1)
#    Number_crop = forms.FloatField(required=True,label='Number of simulated crops',initial=3)
    
    
    