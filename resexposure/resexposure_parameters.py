# -*- coding: utf-8 -*-
"""
Created on 2013-08-19

@author: Tao Hong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe
model_choices = (('tab_hdflr','Hard Surface Floor Cleaner'), 
                 ('tab_vlflr','Vinyl Floor'), 
                 ('tab_cpcln','Carpet Cleaner'))

class resexposureInp_model(forms.Form):
    model = forms.MultipleChoiceField(choices=model_choices, widget=forms.CheckboxSelectMultiple())

class resexposureInp_hdflr(forms.Form):
    ar_hd = forms.FloatField(required=True, label=mark_safe("Application rate of cleaning solution (ft<sup>2</sup>/gallon)"), initial=1000)
    ai_hd = forms.FloatField(required=True, label="Percent a.i. in cleaning solution (%)", initial=100)
    den_hd = forms.FloatField(required=True, label="Cleaning solution density (lb/gallon)", initial=8.35)
    cf1_hd = forms.FloatField(required=True, label="Conversion factor (mg/lb)", initial=4.54e5)
    cf2_hd = forms.FloatField(required=True, label=mark_safe("Conversion factor (ft<sup>2</sup>/cm<sup>2</sup>)"), initial=1.08e-3)
    fr_hd = forms.FloatField(required=True, label="Fraction of solution remaining on floor", initial=0.25)
    tf_hd = forms.FloatField(required=True, label="Transfer factor for hard surfaces", initial=1)
    sa_hd = forms.FloatField(required=True, label=mark_safe("Surface area of body in contact with floor (cm<sup>2</sup>)"), initial=6600)
    da_hd = forms.FloatField(required=True, label="Dermal absorption (%)", initial=100)
    bw_hd = forms.FloatField(required=True, label="Body weight (kg)", initial=15)
    sa_h_hd = forms.FloatField(required=True, label=mark_safe("Surface area of hands in contact with floor (cm<sup>2</sup>)"), initial=20)
    fq_hd = forms.FloatField(required=True, label="Frequency of hand to mouth contacts (events/hour)", initial=20)
    et_hd = forms.FloatField(required=True, label="Exposure Time (hours/day)", initial=4)
    se_hd = forms.FloatField(required=True, label="Saliva Extraction Factor (%)", initial=50)

class resexposureInp_vlflr(forms.Form):
    wf_vl = forms.FloatField(required=True, label="Weight fraction of a.i. in vinyl (%)"), initial=0.1)
    den_vl = forms.FloatField(required=True, label=mark_safe("Vinyl Density (g/cm<sup>3</sup>)"), initial=1.30)
    vt_vl = forms.FloatField(required=True, label="Vinyl Thickness (mm)", initial=3.0)
    cf1_vl = forms.FloatField(required=True, label="Conversion factor (cm/mm)", initial=0.001)
    af_vl = forms.FloatField(required=True, label="Availability Factor (%)", initial=0.5)
    tf_vl = forms.FloatField(required=True, label="Transfer Factor from Vinyl to Skin (%)", initial=100)
    cf2_vl = forms.FloatField(required=True, label="Conversion factor (mg/g)", initial=1000)
    bw_vl = forms.FloatField(required=True, label="Body weight (kg)", initial=15)
    sa_vl = forms.FloatField(required=True, label=mark_safe("Body Surface Contacting Vinyl (cm<sup>2</sup>/day)"), initial=6600)
    da_vl = forms.FloatField(required=True, label="Dermal absorption (%)", initial=100)
    sa_h_vl = forms.FloatField(required=True, label=mark_safe("Hand to Mouth Surface Area (cm<sup>2</sup>)"), initial=20)
    fq_vl = forms.FloatField(required=True, label="Frequency of hand to mouth contacts (events/hour)", initial=20)
    et_vl = forms.FloatField(required=True, label="Exposure Time (hours/day)", initial=4)
    se_vl = forms.FloatField(required=True, label="Saliva Extraction Efficiency (%)", initial=50)


class resexposureInp_cpcln(forms.Form):
    bw_c1 = forms.FloatField(required=True, label="Body weight (kg)", initial=29)
    sa_c1_c = forms.FloatField(required=True, label=mark_safe("Surface area exposed (Competitive, cm<sup>2</sup>)"), initial=10500)
    sa_c1_nc = forms.FloatField(required=True, label=mark_safe("Surface area exposed (Non-Competitive, cm<sup>2</sup>)"), initial=10500)
    et_c1_c = forms.FloatField(required=True, label="Exposure time (Competitive, hr/day)", initial=1)
    et_c1_nc = forms.FloatField(required=True, label="Exposure time (Non-Competitive, hr/day)", initial=1)
    ir_c1_c = forms.FloatField(required=True, label="Inhalation rate of pool water (Competitive, L/hr)", initial=2.5)
    ir_c1_nc = forms.FloatField(required=True, label="Inhalation rate of pool water (Non-Competitive, L/hr)", initial=1.3)
    igr_c1_c = forms.FloatField(required=True, label="Ingestion rate of pool water (Competitive, L/hr)", initial=0.05)
    igr_c1_nc = forms.FloatField(required=True, label="Ingestion rate of pool water (Non-Competitive, L/hr)", initial=0.05)
