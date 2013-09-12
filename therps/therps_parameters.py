
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

Species_of_the_tested_bird_CHOICES=(('Bobwhite quail','Bobwhite quail'),('Mallard duck','Mallard duck'),('Other','Other'))

class trexInp_chem(forms.Form):    
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Fluxapyroxad')
    Use = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Dried shelled beans (except soybeans)')   
    Formulated_product_name = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='NA')    
    percent_ai=forms.FloatField(required=True, label='% a.i. (%)', initial=100)
    Foliar_dissipation_half_life = forms.FloatField(required=True, label='Foliar dissipation half-life (days)', initial=35)
    number_of_applications = forms.FloatField(required=True, label='Number of applications', initial=2)
    interval_between_applications = forms.FloatField(required=True, label='Interval between applications (days)', initial=7)
    application_rate = forms.FloatField(required=True, label='Application rate (lbs a.i./A)',initial=0.18)

class trexInp_bird(forms.Form):    
    avian_ld50 = forms.FloatField(required=True, label='Avian LD50 (mg/kg-bw)', initial=2000)
    Species_of_the_tested_bird_avian_ld50 = forms.ChoiceField(required=True,label='Test species (for Avian LD50)', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
    bw_avian_ld50 = forms.FloatField(required=True,label='Weight (g)', initial= '178')
    avian_lc50 = forms.FloatField(required=True, label='Avian LC50 (mg/kg-diet)', initial=2457)
    Species_of_the_tested_bird_avian_lc50 = forms.ChoiceField(required=True,label='Test species (for Avian LC50)', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
    bw_avian_lc50 = forms.FloatField(required=True,label='Weight (g)', initial= '178')
    avian_NOAEC = forms.FloatField(required=True,label='Avian NOAEC (mg/kg-diet)', initial=100)
    Species_of_the_tested_bird_avian_NOAEC = forms.ChoiceField(required=True,label='Test species (for Avian NOAEC)', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
    bw_avian_NOAEC = forms.FloatField(required=True,label='Weight (g)', initial= '178')
    avian_NOAEL = forms.FloatField(required=True, label='Avian NOAEL (mg/kg-bw)', initial=7.8)
    Species_of_the_tested_bird_avian_NOAEL = forms.ChoiceField(required=True,label='Test species (for Avian NOAEL)', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
    bw_avian_NOAEL = forms.FloatField(required=True,label='Weight (g)', initial= '178')

    # Species_of_the_tested_bird = forms.ChoiceField(required=True,label='Species of the tested bird', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
    # body_weight_of_the_tested_bird=forms.FloatField(required=True, label='Body weight of the tested bird (g)', initial=178)
    mineau_scaling_factor = forms.FloatField(required=True,label='Mineau scaling factor',initial=1.15)

class trexInp_herp(forms.Form):    
    BW_herptile_a_sm = forms.FloatField(required=True, label='Body weight of assessed small herptile (g)', initial=2.0)
    W_p_a_sm = forms.FloatField(required=True, label="Water content of the assessed small herptile's diet (%)", initial=85)
    BW_herptile_a_md = forms.FloatField(required=True, label='Body weight of assessed medium herptile (g)', initial=20)
    W_p_a_md = forms.FloatField(required=True, label="Water content of the assessed medium herptile's diet (%)", initial=85)
    BW_herptile_a_lg = forms.FloatField(required=True, label='Body weight of assessed large herptile (g)', initial=200)
    W_p_a_lg = forms.FloatField(required=True, label="Water content of the assessed large herptile's diet (%)", initial=85)
    body_weight_of_the_consumed_mammal_a = forms.FloatField(required=True,label='Weight of the mammal consumed by assessed frog (g)', initial=15)
    body_weight_of_the_consumed_herp_a = forms.FloatField(required=True,label='Weight of the herptile  consumed by assessed frog (g)', initial=15)


