#!/usr/bin/env python
# -*- coding:utf-8 -*-
#*********************************************************#
# @@ScriptName: orehe_parameters.py
# @@Author: Tao Hong
# @@Create Date: 2013-06-19
# @@Modify Date: 2013-09-05
#*********************************************************#
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models

exdu_select = (('Short-Term','Short-Term'), ('Intermediate-Term','Intermediate-Term'), ('Long-Term','Long-Term'))
der_pod_sor_select = (('Oral','Oral'), ('Route-specific','Route-specific'))
der_abs_sor_select = (('Human study','Human study'), ('Animal study','Animal study'), ('Estimated by POD or LOAEL/NOAEL comparison','Estimated by POD or LOAEL/NOAEL comparison'),
                      ('In vitro study','In vitro study'), ('Other','Other'))
inh_pod_sor_select = (('Oral','Oral'), ('Route-specific','Route-specific'))

der_wt_select = (('80','80'), ('69','69'), ('86','86'))
inh_wt_select = (('80','80'), ('69','69'), ('86','86'))
comb_select = (('No','No'), ('Combined (same LOCs)','Combined (same LOCs)'), ('ARI (different LOCs)','ARI (different LOCs)'))
lab_select= (('oz','oz'), ('g','g'), ('ml','ml'))

scenario_choices = (('tab_ie', 'Indoor Environment'), ('tab_pp', 'Paints / Preservatives'), 
                    ('tab_tp', 'Treated Pets'), ('tab_oa', 'Outdoor Aerosol Space Sprays'), 
                    ('tab_or', 'Outdoor Residential Misting Systems'), ('tab_ab', 'Animal Barn Misting Systems'))

class oreheInp_cm(forms.Form):
    actv_cm = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 2}), label='Active ingredient')
    exdu_cm = forms.ChoiceField(required=True, choices=exdu_select, label='Exposure duration')
    der_pod_cm = forms.FloatField(required=True, label='Dermal POD (mg/kg/day)', initial= 4)
    der_pod_sor_cm = forms.ChoiceField(required=True, choices=der_pod_sor_select, label='Dermal POD source/study')
    der_abs_cm = forms.FloatField(required=True, label='Dermal absorption (0-1)', initial= 0.5)
    der_abs_sor_cm = forms.ChoiceField(required=True, choices=der_abs_sor_select, label='Dermal absorption source/study')
    der_loc_cm = forms.FloatField(required=True, label='Dermal LOC', initial= 21)
    inh_pod_cm = forms.FloatField(required=True, label='Inhalation POD (mg/kg/day)', initial= 1)
    inh_pod_sor_cm = forms.ChoiceField(required=True, choices=inh_pod_sor_select, label='Inhalation POD source/study')
    inh_abs_cm = forms.FloatField(required=True, label='Inhalation absorption (0-1)', initial= 0.6)
    inh_loc_cm = forms.FloatField(required=True, label='Inhalation LOC', initial= 12)
    der_wt_cm = forms.ChoiceField(required=True, choices=der_wt_select, label='Adult weights (dermal kg)')
    inh_wt_cm = forms.ChoiceField(required=True, choices=inh_wt_select, label='Adult weights (inhalation kg)')
    chd_wt_cm = forms.FloatField(required=True, label='Children (1 <2 years) weights (kg)', initial= 11)
    comb_cm = forms.ChoiceField(required=True, choices=comb_select, label='Combining Risks?')
    scenario_cm = forms.MultipleChoiceField(choices=scenario_choices, label='Select scenarios', widget=forms.CheckboxSelectMultiple())

class oreheInp_gh(forms.Form):
    scna_gh = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 2}), label='Scenario', initial='Indoor environment')
    form_gh = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 1}), label='Formulation', initial='Dust/Powder')
    apmd_gh = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 1}), label='Application equipment/method', initial='Plunger Duster')
    type_gh = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 1}), label='Type', initial='Plunger Duster')
    aprt_gh = forms.FloatField(required=True, label='Application rate (lb ai/lb dust)', initial= 1000)
    area_gh = forms.FloatField(required=True, label='Area treated or amount handled daily (lb dust)', initial= 0.5)
    deru_gh = forms.FloatField(required=True, label='Dermal unit exposure (mg/lb ai)', initial= 250)
    inhu_gh = forms.FloatField(required=True, label='Inhalation unit exposure (mg/lb ai)', initial= 1.7)

class oreheInp_pp_ac(forms.Form):
    scna_pp_ac = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 2}), label='Scenario', initial='Paints / Preservatives')
    form_pp_ac = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 2}), label='Formulation', initial='Paints / Preservatives/ Stains')
    apmd_pp_ac = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 2}), label='Application equipment/method', initial='Aerosol can (RTU)')
    wf_pp_ac = forms.FloatField(required=True, label='Weight fraction of a.i. in treated paint (0-1)', initial= 0.4)
    vl_pp_ac = forms.FloatField(required=True, label='Volume of paint per can (ml/can)', initial= 45)
    pd_pp_ac = forms.FloatField(required=True, label='Paint density (g/mL)', initial= 23)
    area_pp_ac = forms.FloatField(required=True, label='Area treated or amount handled daily (lb dust)', initial= 3)
    deru_pp_ac = forms.FloatField(required=True, label='Dermal unit exposure (mg/lb ai)', initial= 370)
    inhu_pp_ac = forms.FloatField(required=True, label='Inhalation unit exposure (mg/lb ai)', initial= 3)

class oreheInp_tp_dp(forms.Form):
    scna_tp_dp = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 2}), label='Scenario', initial='Treated Pets')
    form_tp_dp = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 2}), label='Formulation', initial='Liquid concentrate')
    apmd_tp_dp = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 2}), label='Application equipment/method', initial='Dip')
    aai_tp_dp = forms.FloatField(required=True, label='Amount a.i. (% a.i.)', initial= 90)
    aa_tp_dp = forms.FloatField(required=True, label='Amount applied (g)', initial= 1000)
    area_tp_dp = forms.FloatField(required=True, label='Area treated or amount handled daily (lb dust)', initial= 2)
    deru_tp_dp = forms.FloatField(required=True, label='Dermal unit exposure (mg/lb ai)', initial= 100)
    inhu_tp_dp = forms.FloatField(required=True, label='Inhalation unit exposure (mg/lb ai)', initial= 0.027)

class oreheInp_oa(forms.Form):
    lab_oa = forms.ChoiceField(required=True, choices=lab_select, label='Label unit')
    ai_oa = forms.FloatField(required=True, label='Amount a.i. (% a.i.)', initial= 90)
    at_oz_oa = forms.FloatField(required=True, label='Amount of product in can (oz/can)', initial= 13)
    at_g_oa = forms.FloatField(required=True, label='Amount of product in can (g/can)', initial= 13)
    at_ml_oa = forms.FloatField(required=True, label='Amount of product in can (ml/can)', initial= 13)
    den_oa = forms.FloatField(required=True, label='Density of product (g/ml)', initial= 1)
    deru_oa = forms.FloatField(required=True, label='Dermal unit exposure (mg/lb ai)', initial= 370)
    inhu_oa = forms.FloatField(required=True, label='Inhalation unit exposure (mg/lb ai)', initial= 3.0)

class oreheInp_or(forms.Form):
    ai_or = forms.FloatField(required=True, label='Amount a.i. (% a.i.)', initial= 5)
    ds_or = forms.FloatField(required=True, label='Drum size (gallons)', initial= 55)
    nd_or = forms.FloatField(required=True, label='Number of drums filled per day', initial= 1)
    den_or = forms.FloatField(required=True, label='Density (lbs/gallon)', initial= 8.34)
    dr_or = forms.FloatField(required=True, label='Dilution (concentrate/concentrate+water)', initial= 0.033)
    deru_or = forms.FloatField(required=True, label='Dermal unit exposure (mg/lb ai)', initial= 0.232)
    inhu_or = forms.FloatField(required=True, label='Inhalation unit exposure (mg/lb ai)', initial= 0.000219)

class oreheInp_ab(forms.Form):
    ai_ab = forms.FloatField(required=True, label='Amount a.i. (% a.i.)', initial= 5)
    ds_ab = forms.FloatField(required=True, label='Drum size (gallons)', initial= 55)
    nd_ab = forms.FloatField(required=True, label='Number of drums filled per day', initial= 1)
    den_ab = forms.FloatField(required=True, label='Density (lbs/gallon)', initial= 8.34)
    dr_ab = forms.FloatField(required=True, label='Dilution (concentrate/concentrate+water)', initial= 0.033)
    deru_ab = forms.FloatField(required=True, label='Dermal unit exposure (mg/lb ai)', initial= 0.232)
    inhu_ab = forms.FloatField(required=True, label='Inhalation unit exposure (mg/lb ai)', initial= 0.000219)
