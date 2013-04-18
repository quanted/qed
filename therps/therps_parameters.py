
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

Applicationtype_CHOICES=(('Broadcast-Granular','Broadcast-Granular'),('Row/Band/In-furrow-Granular','Row/Band/In-furrow-Granular'),
                         ('Broadcast-Liquid','Broadcast-Liquid'),('Row/Band/In-furrow-Liquid','Row/Band/In-furrow-Liquid'))
Applicationtarget_CHOICES=(('Short grass','Short grass'),('Tall grass','Tall grass'),('Broad-leafed plants/small insects','Broad-leafed plants/small insects'),
                           ('Fruits/pods/seeds/large insects','Fruits/pods/seeds/large insects'))                           
Species_of_the_tested_bird_CHOICES=(('Bobwhite quail','Bobwhite quail'),('Mallard duck','Mallard duck'),('Other','Other'))
BW_range_CHOICES=(('Small','Small'),('Medium','Medium'),('Large','Large'))

class therpsInp(forms.Form):
    chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Alachlor')
    Use = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='Corn')   
    Formulated_product_name = forms.CharField(max_length=255, widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}),initial='NA')    
    percent_ai=forms.FloatField(required=True, label='% a.i. (%)', initial=100)
    application_rate = forms.FloatField(required=True, label='Application rate (lbs a.i./A)',initial=4)
    number_of_applications = forms.FloatField(required=True, label='Number of applications', initial=1)
    Application_target = forms.ChoiceField(required=True, choices=Applicationtarget_CHOICES, initial='Broad-leafed plants/small insects')        
    interval_between_applications = forms.FloatField(required=True, label='Interval between applications (days)', initial=0)
    Foliar_dissipation_half_life = forms.FloatField(required=True, label='Foliar dissipation half-life (days)', initial=35)
    avian_ld50 = forms.FloatField(required=True, label='Avian LD50 (mg/kg-bw)', initial=1499)
    avian_lc50 = forms.FloatField(required=True, label='Avian LC50 (mg/kg-diet)', initial=5620)
    avian_NOAEC = forms.FloatField(required=True,label='Avian NOAEC (mg/kg-diet)', initial=50)
    avian_NOAEL = forms.FloatField(required=True, label='Avian NOAEL (mg/kg-bw)', initial=10)
    Species_of_the_tested_bird = forms.ChoiceField(required=True,label='Species of the tested bird', choices=Species_of_the_tested_bird_CHOICES, initial='Bobwhite quail')
        
    body_weight_of_the_tested_bird=forms.FloatField(required=True, label='Body weight of the tested bird (g)', initial=178)
    mineau_scaling_factor = forms.FloatField(required=True,label='Mineau scaling factor',initial=1.15)
    
    BW_range_a = forms.ChoiceField(required=True, choices=BW_range_CHOICES, label='Body weight range of the assessed amphibian', initial='Small')
    BW_herptile_a = forms.FloatField(required=True, label='Body weight of assessed amphibian (g)', initial=1.4)
    W_p_a = forms.FloatField(required=True, label='''Water content of the assessed amphibian's diet (%)''', initial=85)
    body_weight_of_the_consumed_mammal_a = forms.FloatField(required=True,label='Weight of the mammal consumed by amphibian (g)', initial=35)
    W_p_m_a = forms.FloatField(required=True, label='''Water content of in mammal's diet (consumed by amphibian) (%)''', initial=85)
    body_weight_of_the_consumed_herp_a = forms.FloatField(required=True,label='Weight of the herptile  consumed by amphibian (g)', initial=2.3)
    
    BW_range_r = forms.ChoiceField(required=True, choices=BW_range_CHOICES, label='Body weight range of the assessed reptile', initial='Small')
    BW_herptile_r = forms.FloatField(required=True, label='Body weight of assessed reptile (g)', initial=1.4)
    W_p_r = forms.FloatField(required=True, label='''Water content of the assessed reptile's diet (%)''', initial=85)
    body_weight_of_the_consumed_mammal_r = forms.FloatField(required=True,label='Weight of the mammal consumed by reptile (g)', initial=35)
    W_p_m_r = forms.FloatField(required=True, label='''Water content of in mammal's diet (consumed by reptile) (%)''', initial=85)
    body_weight_of_the_consumed_herp_r = forms.FloatField(required=True,label='Weight of the herptile  consumed by reptile (g)', initial=2.3)
      
    
    
    
    







    