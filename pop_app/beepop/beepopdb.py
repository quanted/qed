# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:50:59 2012

@author: MSnyder
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
#Weather_scenario_CHOICES=(('','Make a selection'),('1','Midwestern'),('2','Southwestern'))
Swarm_CHOICES=(('','Make a selection'),('Yes','Yes'),('No','No'))
Winter_kill_CHOICES=(('','Make a selection'),('Yes','Yes'),('No','No'))

class beepopInp(forms.Form):
    initial_colony_size = forms.FloatField(required=True,label='Number of bees in colony', initial=30000)
#    starting_date = forms.FloatField(required=True,label='Starting date of simulation', initial = 1)
# #   weather_conditions = forms.ChoiceField(required=True,label='Regional weather selection', choices=Weather_scenario_CHOICES, initial='Make a selection')
    sperm_obtained = forms.FloatField(required=True,label='Sperm obtained by the queen during mating', initial=5000000)
    potential_eggs_laid = forms.FloatField(required=True,label='Potential number of eggs laid per day', initial=1500)
 #   no_foraging_days = forms.FloatField(required=True,label='Number of days a bee can forage before it dies', initial=20)
    brood_cycles = forms.FloatField(required=True,label='Number of brood cycles in the simulation', initial=1)
    days_to_adult_worker = forms.FloatField(required=True,label='Number of days before larvae develop into adult workers', initial=21)
    days_to_adult_drones = forms.FloatField(required=True,label='Number of days before larvae develop into adult drones', initial=24)
    days_from_adult_to_forager = forms.FloatField(required=True,label='Number of days before adult workers develop into adult foragers', initial=21)
    number_of_forages = forms.FloatField(required=True,label='Number of days foragers can forage', initial=10)
    egg_mortality = forms.FloatField(required=True,label='Percentage of eggs surviving to adults', initial=.85)
    adult_brood_ratio = forms.FloatField(required=True,label='Maximum ratio of adults to brood in a colony', initial=3)
    swarm = forms.ChoiceField(required=True,label='Swarm event', choices=Swarm_CHOICES,initial='Make a selection')
    stop_lay = forms.FloatField(required=True,label='Day Queen stops laying eggs (Jday)', initial=166)
    start_lay = forms.FloatField(required=True,label='Day New Queen begins laying eggs (Jday)',  initial=181)
    lay_maximum = forms.FloatField(required=True,label='Day New Queen begins laying eggs at maximum rate (Jday)',  initial=186)
    swarm_date = forms.FloatField(required=True,label='Day of swarm (Jday)',  initial=168)
    winter_kill = forms.ChoiceField(required=True,label='Winter Kill Event', choices=Winter_kill_CHOICES,initial='Make a selection')
    kill_percent = forms.FloatField(required=True,label='Percent dying during winter',  initial=15)


  


