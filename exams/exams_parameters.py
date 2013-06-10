# -*- coding: utf-8 -*-
"""
Created on 06-06-2013

"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.utils.safestring import mark_safe

scenario_select = (('','Select a scenario'),('CA Almonds MLRA-17', 'CA Almonds MLRA-17'), ('CA Citrus   MLRA-17', 'CA Citrus   MLRA-17'), ('CA Cotton   MLRA-17', 'CA Cotton   MLRA-17'), ('CA Grape  MLRA-17', 'CA Grape  MLRA-17'), ('CA Lettuce  MLRA-14', 'CA Lettuce  MLRA-14'), ('CA Onions MLRA-17', 'CA Onions MLRA-17'), ('CA Tomato MLRA-17', 'CA Tomato MLRA-17'), ('FL Avocado MLRA-156A', 'FL Avocado MLRA-156A'), ('FL Cabbage   MLRA-155', 'FL Cabbage   MLRA-155'), ('FL Carrots MLRA-156B', 'FL Carrots MLRA-156B'), ('FL Citrus   MLRA-156A', 'FL Citrus   MLRA-156A'), ('FL Cucumber   MLRA-156A', 'FL Cucumber   MLRA-156A'), ('FL Peppers MLRA-156A', 'FL Peppers MLRA-156A'), ('FL Strawberry   MLRA-155', 'FL Strawberry   MLRA-155'), ('FL Sugarcane   MLRA-156A', 'FL Sugarcane   MLRA-156A'), ('FL Tomato   MLRA-155', 'FL Tomato   MLRA-155'), ('FL Turf  MLRA-155', 'FL Turf  MLRA-155'), ('GA Onions MLRA-153A/133A', 'GA Onions MLRA-153A/133A'), ('GA Peach   MLRA-133A', 'GA Peach   MLRA-133A'), ('GA Pecan   MLRA-133A', 'GA Pecan   MLRA-133A'), ('ID Potato   MLRA-11B', 'ID Potato   MLRA-11B'), ('IL Corn   MLRA-108', 'IL Corn   MLRA-108'), ('KS Sorghum   MLRA-112', 'KS Sorghum   MLRA-112'), ('LA Sugarcane   MLRA-131', 'LA Sugarcane   MLRA-131'), ('ME Potato   MLRA-146', 'ME Potato   MLRA-146'), ('MI Asparagus MLRA-96', 'MI Asparagus MLRA-96'), ('MI Beans MLRA-99', 'MI Beans MLRA-99'), ('MI Cherry   MLRA-96', 'MI Cherry   MLRA-96'), ('MN Sugarbeet   MLRA-56', 'MN Sugarbeet   MLRA-56'), ('MS Corn   MLRA-134', 'MS Corn   MLRA-134'), ('MS Cotton   MLRA-134', 'MS Cotton   MLRA-134'), ('MS Soybean   MLRA-134', 'MS Soybean   MLRA-134'), ('NC Apple   MLRA-130', 'NC Apple   MLRA-130'), ('NC Corn - E   MLRA-153A', 'NC Corn - E   MLRA-153A'), ('NC Cotton   MLRA-133A', 'NC Cotton   MLRA-133A'), ('NC Peanut   MLRA-153A', 'NC Peanut   MLRA-153A'), ('NC Sweet Potato MLRA-133', 'NC Sweet Potato MLRA-133'), ('NC Tobacco   MLRA-133A', 'NC Tobacco   MLRA-133A'), ('ND Canola   MLRA-55A', 'ND Canola   MLRA-55A'), ('ND Wheat   MLRA-56', 'ND Wheat   MLRA-56'), ('NY Grape   MLRA-100/101', 'NY Grape   MLRA-100/101'), ('OH Corn   MLRA-111', 'OH Corn   MLRA-111'), ('OR Apple   MLRA-2', 'OR Apple   MLRA-2'), ('OR Christmas Trees  MLRA-2', 'OR Christmas Trees  MLRA-2'), ('OR Filberts   MLRA-2', 'OR Filberts   MLRA-2'), ('OR Grass Seed   MLRA-2', 'OR Grass Seed   MLRA-2'), ('OR Hops   MLRA-2', 'OR Hops   MLRA-2'), ('OR Mint   MLRA-2', 'OR Mint   MLRA-2'), ('PA Apple   MLRA-148', 'PA Apple   MLRA-148'), ('PA Corn   MLRA-148', 'PA Corn   MLRA-148'), ('PA Turf  MLRA-148', 'PA Turf  MLRA-148'), ('PR Coffee MLRA-270', 'PR Coffee MLRA-270'))
farm_select = (('No','No'), ('Yes','Yes'))

class EXAMSInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
    scenarios = forms.ChoiceField(required=True,choices=scenario_select, label='Standard OPP/EFED Scenarios', initial='')
    farm_pond = forms.ChoiceField(required=True,choices=farm_select, label='Farm pond (no flow)', initial='')
    molecular_weight = forms.FloatField(required=True, label='Molecular weight (g/mol)') 
    solubility = forms.FloatField(required=True, label='Solubility(mg/L)')
    Koc = forms.FloatField(required=True, label='Aquatic Sediment Koc (mL/g)')   
    vapor_pressure = forms.FloatField(required=True, label='Vapor Pressure (torr)')
    aerobic_aquatic_metabolism = forms.FloatField(required=True, label='Aerobic aquatic metabolism (days)')
    anaerobic_aquatic_metabolism = forms.FloatField(required=True, label='Anaerobic aquatic metabolism (days)')
    aquatic_direct_photolysis = forms.FloatField(required=True, label='Aquatic Direct Photolysis (days)')
    temperature = forms.FloatField(required=True, label=mark_safe('Test Temperature (<sup>o</sup>C)'))
