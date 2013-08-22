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
model_choices = (('tab_hdflr', 'Hard Surface Floor Cleaner'), ('tab_vlflr', 'Vinyl Floor'), ('tab_cpcln', 'Carpet Cleaner'),
                 ('tab_ipcap', 'Impregnated Carpet'), ('tab_mactk', 'Mattress Covers and Ticking'), ('tab_ccpst', 'Clothing/Textile Consumer Product Spray Treatment'),
                 ('tab_ldtpr', 'Laundry Detergent Preservative'), ('tab_clopr', 'Clothing/Textile Material Preservative'), ('tab_impdp', 'Impregnated Diapers'),
                 ('tab_cldst', 'Sprayed Diapers'), ('tab_impty', 'Impregnated Toys'))

class resexposureInp_model(forms.Form):
    model = forms.MultipleChoiceField(choices=model_choices, widget=forms.CheckboxSelectMultiple())

class resexposureInp_hdflr(forms.Form):
    ar_hd = forms.FloatField(required=True, label=mark_safe("Application rate of cleaning solution (ft<sup>2</sup>/gallon)"), initial=1000)
    ai_hd = forms.FloatField(required=True, label="Percent a.i. in cleaning solution (%)", initial=0.1)
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
    et_hd = forms.FloatField(required=True, label="Exposure time (hours/day)", initial=4)
    se_hd = forms.FloatField(required=True, label="Saliva extraction factor (%)", initial=50)

class resexposureInp_vlflr(forms.Form):
    wf_vl = forms.FloatField(required=True, label="Weight fraction of a.i. in vinyl (%)", initial=0.1)
    den_vl = forms.FloatField(required=True, label=mark_safe("Vinyl density (g/cm<sup>3</sup>)"), initial=1.30)
    vt_vl = forms.FloatField(required=True, label="Vinyl thickness (mm)", initial=3.0)
    cf1_vl = forms.FloatField(required=True, label="Conversion factor (cm/mm)", initial=0.001)
    af_vl = forms.FloatField(required=True, label="Availability factor (%)", initial=0.5)
    tf_vl = forms.FloatField(required=True, label="Transfer factor from vinyl to skin (%)", initial=100)
    cf2_vl = forms.FloatField(required=True, label="Conversion factor (mg/g)", initial=1000)
    bw_vl = forms.FloatField(required=True, label="Body weight (kg)", initial=15)
    sa_vl = forms.FloatField(required=True, label=mark_safe("Body surface contacting vinyl (cm<sup>2</sup>/day)"), initial=6600)
    da_vl = forms.FloatField(required=True, label="Dermal absorption (%)", initial=100)
    sa_h_vl = forms.FloatField(required=True, label=mark_safe("Hand to mouth surface area (cm<sup>2</sup>)"), initial=20)
    fq_vl = forms.FloatField(required=True, label="Frequency of hand to mouth contacts (events/hour)", initial=20)
    et_vl = forms.FloatField(required=True, label="Exposure time (hours/day)", initial=4)
    se_vl = forms.FloatField(required=True, label="Saliva extraction efficiency (%)", initial=50)

class resexposureInp_cpcln(forms.Form):
    ar_cc = forms.FloatField(required=True, label=mark_safe("Application rate of cleaning solution (ft<sup>2</sup>/gallon)"), initial=300)
    ai_cc = forms.FloatField(required=True, label="Percent a.i. in cleaning solution (%)", initial=0.1)
    den_cc = forms.FloatField(required=True, label="Cleaning solution density (lb/gallon)", initial=8.35)
    cf1_cc = forms.FloatField(required=True, label="Conversion factor (mg/lb)", initial=4.54e5)
    cf2_cc = forms.FloatField(required=True, label=mark_safe("Conversion factor (ft<sup>2</sup>/cm<sup>2</sup>)"), initial=1.08e-3)
    fr_cc = forms.FloatField(required=True, label="Fraction of solution remaining on floor", initial=0.25)
    tf_cc = forms.FloatField(required=True, label="Transfer factor for carpet", initial=1)
    bw_cc = forms.FloatField(required=True, label="Body weight (kg)", initial=15)
    sa_cc = forms.FloatField(required=True, label=mark_safe("Surface area of body in contact with floor (cm<sup>2</sup>)"), initial=6600)
    da_cc = forms.FloatField(required=True, label="Dermal absorption (%)", initial=100)
    sa_h_cc = forms.FloatField(required=True, label=mark_safe("Surface area of hands in contact with floor (cm<sup>2</sup>)"), initial=20)
    fq_cc = forms.FloatField(required=True, label="Frequency of hand to mouth contacts (events/hour)", initial=20)
    et_cc = forms.FloatField(required=True, label="Exposure time (hours/day)", initial=4)
    se_cc = forms.FloatField(required=True, label="Saliva extraction factor (%)", initial=50)

class resexposureInp_ipcap(forms.Form):
    den_ic = forms.FloatField(required=True, label=mark_safe("Carpet density (mg/cm<sup>2</sup>)"), initial=122)
    wf_ic = forms.FloatField(required=True, label=mark_safe("Weight fraction of a.i. in carpet"), initial=0.001)
    tf_ic = forms.FloatField(required=True, label="Transfer factor from carpet to skin", initial=1)
    bw_ic = forms.FloatField(required=True, label="Body weight (kg)", initial=15)
    sa_ic = forms.FloatField(required=True, label=mark_safe("Surface area of body in contact with carpet (cm<sup>2</sup>)"), initial=6600)
    da_ic = forms.FloatField(required=True, label="Dermal absorption (%)", initial=100)
    sa_h_ic = forms.FloatField(required=True, label=mark_safe("Surface area of hands in contact with floor (cm<sup>2</sup>)"), initial=20)
    fq_ic = forms.FloatField(required=True, label="Frequency of hand to mouth contacts (events/hour)", initial=20)
    et_ic = forms.FloatField(required=True, label="Exposure time (hours/day)", initial=8)
    se_ic = forms.FloatField(required=True, label="Saliva extraction factor (%)", initial=50)

class resexposureInp_mactk(forms.Form):
    wf_mt = forms.FloatField(required=True, label="Weight fraction of a.i. in vinyl (%)", initial=0.1)
    den_mt = forms.FloatField(required=True, label=mark_safe("Vinyl density (g/cm<sup>3</sup>)"), initial=10)
    tf_mt = forms.FloatField(required=True, label="Transfer factor from vinyl to skin (%)", initial=100)
    bw_mt = forms.FloatField(required=True, label="Body weight (kg)", initial=15)
    pf_mt = forms.FloatField(required=True, label="Protection factor from single layer of clothing/sheet (%)", initial=50)
    sa_mt = forms.FloatField(required=True, label=mark_safe("Body surface contacting vinyl (cm<sup>2</sup>/day)"), initial=6600)
    da_mt = forms.FloatField(required=True, label="Dermal absorption (%)", initial=100)

class resexposureInp_ccpst(forms.Form):
    wa_ct = forms.FloatField(required=True, label=mark_safe("Water absorption rate (mg/cm<sup>2</sup>)"), initial=198)
    wf_ct = forms.FloatField(required=True, label="Weight fraction of a.i. in product (%)", initial=0.1)
    bw_ct = forms.FloatField(required=True, label="Body weight (kg)", initial=15)
    tf_ct = forms.FloatField(required=True, label="Transfer factor from clothing to skin (%)", initial=100)
    sa_ct = forms.FloatField(required=True, label=mark_safe("Surface area of body in contact with clothing (cm<sup>2</sup>)"), initial=5700)
    da_ct = forms.FloatField(required=True, label="Dermal absorption (%)", initial=100)
    sa_m_ct = forms.FloatField(required=True, label=mark_safe("Surface area of textile mouthed (cm<sup>2</sup>)"), initial=100)
    se_ct = forms.FloatField(required=True, label="Saliva extraction factor (%)", initial=50)

class resexposureInp_ldtpr(forms.Form):
    ap_lp = forms.FloatField(required=True, label="Amount of undiluted product used (mg)", initial=150000)
    wf_lp = forms.FloatField(required=True, label="Weight fraction of a.i. in product (%)", initial=0.1)
    den_lp = forms.FloatField(required=True, label=mark_safe("Density of fabric (mg/cm<sup>2</sup>)"), initial=10)
    wfd_lp = forms.FloatField(required=True, label="Weight fraction of detergent deposited on fabric (%)", initial=5)
    tw_lp = forms.FloatField(required=True, label="Total weight of fabric (mg)", initial=1e6)
    bw_lp = forms.FloatField(required=True, label="Body weight (kg)", initial=15)
    sa_lp = forms.FloatField(required=True, label=mark_safe("Body surface area contacting clothing (cm<sup>2</sup>)"), initial=5700)
    tf_cs_lp = forms.FloatField(required=True, label="Weight fraction transferred from clothing to skin (%)", initial=100)
    tf_r_lp = forms.FloatField(required=True, label="Weight fraction remaining on skin (%)", initial=100)
    da_lp = forms.FloatField(required=True, label="Dermal absorption (%)", initial=100)
    sa_m_lp = forms.FloatField(required=True, label=mark_safe("Surface area of textile mouthed (cm<sup>2</sup>)"), initial=100)
    se_lp = forms.FloatField(required=True, label="Saliva extraction factor (%)", initial=50)

class resexposureInp_clopr(forms.Form):
    den_cp = forms.FloatField(required=True, label=mark_safe("Fabric density (mg/cm<sup>2</sup>)"), initial=10)
    wf_cp = forms.FloatField(required=True, label="Weight fraction of a.i. in product (%)", initial=0.1)
    bw_cp = forms.FloatField(required=True, label="Body weight (kg)", initial=15)
    tf_cs_cp = forms.FloatField(required=True, label="Transfer factor from clothing to skin (%)", initial=100)
    sa_cp = forms.FloatField(required=True, label=mark_safe("Surface area of body in contact with clothing (cm<sup>2</sup>)"), initial=5700)
    da_cp = forms.FloatField(required=True, label="Dermal absorption (%)", initial=100)
    sa_m_cp = forms.FloatField(required=True, label=mark_safe("Surface area of textile mouthed (cm<sup>2</sup>)"), initial=100)
    se_cp = forms.FloatField(required=True, label="Saliva extraction factor (%)", initial=50)

class resexposureInp_impdp(forms.Form):
    am_id = forms.FloatField(required=True, label="Amount of treated material within diaper (g)", initial=10)
    wf_id = forms.FloatField(required=True, label="Weight fraction of a.i. in product (%)", initial=0.1)
    tf_id = forms.FloatField(required=True, label="Transferable residue from diaper to skin (%)", initial=100)
    fq_id = forms.FloatField(required=True, label="Exposure frequency (diapers/day)", initial=8)
    da_id = forms.FloatField(required=True, label="Dermal absorption (%)", initial=100)
    bw_id = forms.FloatField(required=True, label="Body weight (kg)", initial=9)

class resexposureInp_cldst(forms.Form):
    ar_sd = forms.FloatField(required=True, label=mark_safe("Product absorption rate (mg/cm<sup>2</sup>)"), initial=198)
    wf_sd = forms.FloatField(required=True, label="Weight fraction of a.i. in product (%)", initial=0.1)
    tf_sd = forms.FloatField(required=True, label="Transferable residue from diaper to skin (%)", initial=100)
    sa_sd = forms.FloatField(required=True, label=mark_safe("Surface area of body in contact with diaper (cm<sup>2</sup>)"), initial=462)
    fq_sd = forms.FloatField(required=True, label="Exposure frequency (diapers/day)", initial=8)
    da_sd = forms.FloatField(required=True, label="Dermal absorption (%)", initial=100)
    bw_sd = forms.FloatField(required=True, label="Body weight (kg)", initial=9)

class resexposureInp_impty(forms.Form):
    wf_ip = forms.FloatField(required=True, label="Weight fraction of a.i. in product (%)", initial=0.1)
    wt_ip = forms.FloatField(required=True, label=mark_safe("Weight of 500cm<sup>2</sup> toy (g)"), initial=50)
    fr_sa_ip = forms.FloatField(required=True, label="Fraction available at toy surface (%)", initial=0.5)
    sa_ip = forms.FloatField(required=True, label=mark_safe("Surface area of toy (cm<sup>2</sup>)"), initial=500)
    sa_m_ip = forms.FloatField(required=True, label=mark_safe("Surface area of mouthed (cm<sup>2</sup>)"), initial=500)
    se_ip = forms.FloatField(required=True, label="Saliva extraction factor (%)", initial=50)
    bw_ip = forms.FloatField(required=True, label="Body weight (kg)", initial=15)




