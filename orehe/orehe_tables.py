#!/usr/bin/env python
# -*- coding:utf-8 -*-
#*********************************************************#
# @@ScriptName: orehe_tables.py
# @@Author: Tao Hong
# @@Create Date: 2013-09-05
# @@Modify Date: 2013-09-05
#*********************************************************#
import numpy
import time, datetime
from django.template import Context, Template
from django.utils.safestring import mark_safe
from orehe import orehe_model
from orehe import orehe_parameters
import time
import datetime

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def gethtmlrowsfromcols(data, headings):
    columns = [data[heading] for heading in headings]

    # get the length of the longest column
    max_len = len(max(columns, key=len))

    for col in columns:
        # padding the short columns with None
        col += [None,] * (max_len - len(col))

    # Then rotate the structure...
    rows = [[col[i] for col in columns] for i in range(max_len)]
    return rows

def getdjtemplate():
    dj_template ="""
    <table class="out_">
    {# headings #}
        <tr>
        {% for heading in headings %}
                <th colspan={{ th_span|default:'1' }}>{{ heading }}</th>
        {% endfor %}
        </tr>
    {% if sub_headings %}
        <tr>
        {% for sub_heading in sub_headings %}
            <th>{{ sub_heading }}</th>
        {% endfor %}
        </tr>
        {% if sub_headings_1 %}
            <tr>
            {% for sub_heading_1 in sub_headings_1 %}
                <th>{{ sub_heading_1|safe }}</th>
            {% endfor %}
            </tr>
        {% endif %}
    {% endif %}
    {# data #}
    {% for row in data %}
    <tr>
        {% for val in row %}
        <td>{{ val|default:''|safe }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
    </table>
    """
    return dj_template



pvuheadings = getheaderpvu()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)


def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>ORE<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html


def table_all(model, all_obj):
    html = timestamp()
    html = html + table_0(all_obj['tab_chem'])
    if 'tab_ie' in model:
        table_ie = table_1(all_obj['tab_ie'])
        html = html + table_ie
    if 'tab_pp' in model:
        table_pp = table_2(all_obj['tab_pp'])
        html = html + table_pp
    if 'tab_tp' in model:
        table_tp = table_3(all_obj['tab_tp'])
        html = html + table_tp
    if 'tab_oa' in model:
        table_oa = table_4(all_obj['tab_oa'])
        html = html + table_oa
    if 'tab_or' in model:
        table_or = table_5(all_obj['tab_or'])
        html = html + table_or
    if 'tab_ab' in model:
        table_ab = table_6(all_obj['tab_ab'])
        html = html + table_ab
    return html



#####Chemical inputs###############################
def gett0data(re_obj):
    data = { 
        "Parameter": ['Active ingredient', 'Exposure duration', 'Dermal POD',
                      'Dermal POD source/study', 'Dermal absorption (0-1)', 'Dermal absorption source/study',
                      'Dermal LOC', 'Inhalation POD', 'Inhalation POD source/study',
                      'Inhalation absorption (0-1)', 'Inhalation LOC', 'Adult weights (dermal)',
                      'Adult weights (inhalation)', 'Children (1 <2 years) weights', 'Combining Risks?'],
        "Value": ['%s' % re_obj.actv_cm, '%s' % re_obj.exdu_cm, '%s' % re_obj.der_pod_cm,
                  '%s' % re_obj.der_pod_sor_cm, '%s' % re_obj.der_abs_cm, '%s' % re_obj.der_abs_sor_cm,
                  '%s' % re_obj.der_loc_cm, '%s' % re_obj.inh_pod_cm, '%s' % re_obj.inh_pod_sor_cm,
                  '%s' % re_obj.inh_abs_cm, '%s' % re_obj.inh_loc_cm, '%s' % re_obj.der_wt_cm,
                  '%s' % re_obj.inh_wt_cm, '%s' % re_obj.chd_wt_cm, '%s' % re_obj.comb_cm,],
        "Units": ['', '', 'mg/kg/day', '', '', '', 
                  '', 'mg/kg/day', '', '', '', 'kg', 'kg', 'kg', ''],
        }
    return data

######Indoor Environment#####
def gett1data_in(re_obj):
    data = { 
        "Parameter": ['Scenario', 'Formulation', 'Application equipment/method',
                      'Type', 'Application rate', 'Area treated or amount handled daily',
                      'Dermal unit exposure', 'Inhalation unit exposure'],
        "Value": ['%s' % re_obj.scna_gh, '%s' % re_obj.form_gh, '%s' % re_obj.apmd_gh,
                  '%s' % re_obj.type_gh, '%s' % re_obj.aprt_gh, '%s' % re_obj.area_gh,
                  '%s' % re_obj.deru_gh, '%s' % re_obj.inhu_gh],
        "Units": ['', '', '', 
                  '', 'lb ai/lb dust', 'lb dust', 
                  'mg/lb ai', 'mg/lb ai'],
        }
    return data

def gett1data_out(re_obj):
    if re_obj.comb_cm == 'No':
        comb_moe_display = 'N/A'
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'Combined (same LOCs)':
        comb_moe_display = '%0.3e' % re_obj.exp_ge_out['comb_moe']
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'ARI (different LOCs)':
        comb_moe_display = 'N/A'
        ari_display = '%0.3e' % re_obj.exp_ge_out['ari']
    data = { 
        "Parameter": ['Adult Dermal Exposure', 'Adult Inhalation Exposure', 
                      'Adult Dermal Absorbed Dose', 'Adult Inhalation Absorbed Dose',
                      'Adult Dermal MOE', 'Adult Inhalation MOE', 
                      'Child (1<2 yrs) Inhalation Exposure', 'Child (1<2 yrs) Inhalation Absorbed Dose', 'Child (1<2 yrs) Inhalation MOE',
                      'Adult Combined Dermal + Inhalation MOE', 'Adult ARI (Dermal + Inhalation)'],
        "Value": ['%0.3e' % re_obj.exp_ge_out['der_exp'], '%0.3e' % re_obj.exp_ge_out['inh_exp'],
                  '%0.3e' % re_obj.exp_ge_out['der_abs_exp'], '%0.3e' % re_obj.exp_ge_out['inh_abs_exp'],
                  '%0.3e' % re_obj.exp_ge_out['der_moe'], '%0.3e' % re_obj.exp_ge_out['inh_moe'],
                  'N/A', 'N/A', 'N/A',
                   comb_moe_display, ari_display],
        "Units": ['mg/day', 'mg/day', 'mg/kg/day', 'mg/kg/day', '', '', 'mg/day', 'mg/kg/day', '', '', ''],
        }
    return data

######Paints / Preservatives#####
def gett2data_in(re_obj):
    data = { 
        "Parameter": ['Scenario', 'Formulation', 'Application equipment/method',
                      'Weight fraction of a.i. in treated paint (0-1)', 'Volume of paint per can',
                      'Paint density', 'Area treated or amount handled daily',
                      'Dermal unit exposure', 'Inhalation unit exposure'],
        "Value": ['%s' % re_obj.scna_pp_ac, '%s' % re_obj.form_pp_ac, '%s' % re_obj.apmd_pp_ac,
                  '%s' % re_obj.wf_pp_ac, '%s' % re_obj.vl_pp_ac,
                  '%s' % re_obj.pd_pp_ac, '%s' % re_obj.area_pp_ac,
                  '%s' % re_obj.deru_pp_ac, '%s' % re_obj.inhu_pp_ac,],
        "Units": ['', '', '', '', 'ml/can', 'g/mL', 'lb dust', 'mg/lb ai', 'mg/lb ai'],
        }
    return data

def gett2data_out(re_obj):
    if re_obj.comb_cm == 'No':
        comb_moe_display = 'N/A'
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'Combined (same LOCs)':
        comb_moe_display = '%0.3e' % re_obj.exp_pp_ac_out['comb_moe']
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'ARI (different LOCs)':
        comb_moe_display = 'N/A'
        ari_display = '%0.3e' % re_obj.exp_pp_ac_out['ari']
    data = { 
        "Parameter": ['Application Rate', 
                      'Adult Dermal Exposure', 'Adult Inhalation Exposure', 
                      'Adult Dermal Absorbed Dose', 'Adult Inhalation Absorbed Dose',
                      'Adult Dermal MOE', 'Adult Inhalation MOE', 
                      'Child (1<2 yrs) Inhalation Exposure', 'Child (1<2 yrs) Inhalation Absorbed Dose', 'Child (1<2 yrs) Inhalation MOE',
                      'Adult Combined Dermal + Inhalation MOE', 'Adult ARI (Dermal + Inhalation)'],
        "Value": ['%0.3e' % re_obj.exp_pp_ac_out['aprt_pp_ac'],
                  '%0.3e' % re_obj.exp_pp_ac_out['der_exp'], '%0.3e' % re_obj.exp_pp_ac_out['inh_exp'],
                  '%0.3e' % re_obj.exp_pp_ac_out['der_abs_exp'], '%0.3e' % re_obj.exp_pp_ac_out['inh_abs_exp'],
                  '%0.3e' % re_obj.exp_pp_ac_out['der_moe'], '%0.3e' % re_obj.exp_pp_ac_out['inh_moe'],
                  '%0.3e' % re_obj.exp_pp_ac_out['inh_exp_cd'], 'N/A', 'N/A',
                   comb_moe_display, ari_display],
        "Units": ['lb ai/can', 'mg/day', 'mg/day', 'mg/kg/day', 'mg/kg/day', '', '', 'mg/day', 'mg/kg/day', '', '', ''],
        }
    return data

########################Treated Pets#################
def gett3data_in(re_obj):
    data = { 
        "Parameter": ['Scenario', 'Formulation', 'Application equipment/method',
                      'Amount a.i.', 'Amount applied',
                      'Area treated or amount handled daily', 'Dermal unit exposure (mg/lb ai)',
                      'Inhalation unit exposure (mg/lb ai)'],
        "Value": ['%s' % re_obj.scna_tp_dp, '%s' % re_obj.form_tp_dp, '%s' % re_obj.apmd_tp_dp,
                  '%s' % (100*re_obj.aai_tp_dp), '%s' % re_obj.aa_tp_dp,
                  '%s' % re_obj.area_tp_dp, '%s' % re_obj.deru_tp_dp,
                  '%s' % re_obj.inhu_tp_dp],
        "Units": ['', '', '', '%', 'g', 'lb dust', 'mg/lb ai', 'mg/lb ai'],
        }
    return data

def gett3data_out(re_obj):
    if re_obj.comb_cm == 'No':
        comb_moe_display = 'N/A'
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'Combined (same LOCs)':
        comb_moe_display = '%0.3e' % re_obj.exp_tp_dp_out['comb_moe']
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'ARI (different LOCs)':
        comb_moe_display = 'N/A'
        ari_display = '%0.3e' % re_obj.exp_tp_dp_out['ari']
    data = { 
        "Parameter": ['Application Rate', 
                      'Adult Dermal Exposure', 'Adult Inhalation Exposure', 
                      'Adult Dermal Absorbed Dose', 'Adult Inhalation Absorbed Dose',
                      'Adult Dermal MOE', 'Adult Inhalation MOE', 
                      'Child (1<2 yrs) Inhalation Exposure', 'Child (1<2 yrs) Inhalation Absorbed Dose', 'Child (1<2 yrs) Inhalation MOE',
                      'Adult Combined Dermal + Inhalation MOE', 'Adult ARI (Dermal + Inhalation)'],
        "Value": ['%0.3e' % re_obj.exp_tp_dp_out['aprt_tp_dp'],
                  '%0.3e' % re_obj.exp_tp_dp_out['der_exp'], '%0.3e' % re_obj.exp_tp_dp_out['inh_exp'],
                  '%0.3e' % re_obj.exp_tp_dp_out['der_abs_exp'], '%0.3e' % re_obj.exp_tp_dp_out['inh_abs_exp'],
                  '%0.3e' % re_obj.exp_tp_dp_out['der_moe'], '%0.3e' % re_obj.exp_tp_dp_out['inh_moe'],
                  '%0.3e' % re_obj.exp_tp_dp_out['inh_exp_cd'], 'N/A', 'N/A',
                   comb_moe_display, ari_display],
        "Units": ['lb ai/pet', 'mg/day', 'mg/day', 'mg/kg/day', 'mg/kg/day', '', '', 'mg/day', 'mg/kg/day', '', '', ''],
        }
    return data

#############Outdoor Aerosol Space Sprays############
def gett4data_in(re_obj):
    if re_obj.lab_oa == 'oz':
        at_val_display = '%s' % re_obj.at_oz_oa
        at_unit_display = 'oz/can'
        den_display = 'N/A'
    elif re_obj.lab_oa == 'g':
        at_val_display = '%s' % re_obj.at_g_oa
        at_unit_display = 'g/can'
        den_display = 'N/A'
    elif re_obj.lab_oa == 'ml':
        at_val_display = '%s' % re_obj.at_ml_oa
        at_unit_display = 'ml/can'
        den_display = '%s' % re_obj.den_oa

    data = { 
        "Parameter": ['Scenario', 'Label unit', 'Amount a.i.',
                      'Amount of product in can', 'Density of product',
                      'Dermal unit exposure (mg/lb ai)', 'Inhalation unit exposure (mg/lb ai)'],
        "Value": ['Outdoor Aerosol Space Sprays (OASS)', 'N/A', '%s' % (100*re_obj.ai_oa),
                  at_val_display, den_display,
                  '%s' % re_obj.deru_oa, '%s' % re_obj.inhu_oa],
        "Units": ['', re_obj.lab_oa, '%', at_unit_display, 'g/ml', 'mg/lb ai', 'mg/lb ai'],
        }
    return data

def gett4data_out(re_obj):
    if re_obj.comb_cm == 'No':
        comb_moe_display = 'N/A'
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'Combined (same LOCs)':
        comb_moe_display = '%0.3e' % re_obj.exp_oa_out['comb_moe']
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'ARI (different LOCs)':
        comb_moe_display = 'N/A'
        ari_display = '%0.3e' % re_obj.exp_oa_out['ari']
    data = { 
        "Parameter": ['Application Rate', 
                      'Adult Dermal Exposure', 'Adult Inhalation Exposure', 
                      'Adult Dermal Absorbed Dose', 'Adult Inhalation Absorbed Dose',
                      'Adult Dermal MOE', 'Adult Inhalation MOE', 
                      'Adult Combined Dermal + Inhalation MOE', 'Adult ARI (Dermal + Inhalation)'],
        "Value": ['%0.3e' % re_obj.exp_oa_out['aprt_oa'],
                  '%0.3e' % re_obj.exp_oa_out['der_exp'], '%0.3e' % re_obj.exp_oa_out['inh_exp'],
                  '%0.3e' % re_obj.exp_oa_out['der_abs_exp'], '%0.3e' % re_obj.exp_oa_out['inh_abs_exp'],
                  '%0.3e' % re_obj.exp_oa_out['der_moe'], '%0.3e' % re_obj.exp_oa_out['inh_moe'],
                   comb_moe_display, ari_display],
        "Units": ['lb ai/day', 'mg/day', 'mg/day', 'mg/kg/day', 'mg/kg/day', '', '', '', ''],
        }
    return data

#############Outdoor Residential Misting Systems############
def gett5data_in(re_obj):
    data = { 
        "Parameter": ['Scenario', 'Amount a.i.', 'Drum size',
                      'Number of drums filled per day', 'Density',
                      'Dilution (concentrate/concentrate+water)', 
                      'Dermal unit exposure (mg/lb ai)', 'Inhalation unit exposure (mg/lb ai)'],
        "Value": ['Outdoor Residential Misting Systems (ORMS)', '%s' % (100*re_obj.ai_or), '%s' % re_obj.ds_or,
                  '%s' % re_obj.nd_or, '%s' % re_obj.den_or, 
                  '%s' % re_obj.dr_or, 
                  '%s' % re_obj.deru_or, '%s' % re_obj.inhu_or],
        "Units": ['', '%', 'gallons', '', 'lbs/gallon', '' 'mg/lb ai', 'mg/lb ai'],
        }
    return data

def gett5data_out(re_obj):
    if re_obj.comb_cm == 'No':
        comb_moe_display = 'N/A'
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'Combined (same LOCs)':
        comb_moe_display = '%0.3e' % re_obj.exp_or_out['comb_moe']
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'ARI (different LOCs)':
        comb_moe_display = 'N/A'
        ari_display = '%0.3e' % re_obj.exp_or_out['ari']
    data = { 
        "Parameter": ['Application Rate', 
                      'Adult Dermal Exposure', 'Adult Inhalation Exposure', 
                      'Adult Dermal Absorbed Dose', 'Adult Inhalation Absorbed Dose',
                      'Adult Dermal MOE', 'Adult Inhalation MOE', 
                      'Adult Combined Dermal + Inhalation MOE', 'Adult ARI (Dermal + Inhalation)'],
        "Value": ['%0.3e' % re_obj.exp_or_out['aprt_or'],
                  '%0.3e' % re_obj.exp_or_out['der_exp'], '%0.3e' % re_obj.exp_or_out['inh_exp'],
                  '%0.3e' % re_obj.exp_or_out['der_abs_exp'], '%0.3e' % re_obj.exp_or_out['inh_abs_exp'],
                  '%0.3e' % re_obj.exp_or_out['der_moe'], '%0.3e' % re_obj.exp_or_out['inh_moe'],
                   comb_moe_display, ari_display],
        "Units": ['lb ai/day', 'mg/day', 'mg/day', 'mg/kg/day', 'mg/kg/day', '', '', '', ''],
        }
    return data

#############Animal Barn Misting Systems############
def gett6data_in(re_obj):
    data = { 
        "Parameter": ['Scenario', 'Amount a.i.', 'Drum size',
                      'Number of drums filled per day', 'Density',
                      'Dilution (concentrate/concentrate+water)', 
                      'Dermal unit exposure (mg/lb ai)', 'Inhalation unit exposure (mg/lb ai)'],
        "Value": ['Animal Barn Misting Systems', '%s' % (100*re_obj.ai_ab), '%s' % re_obj.ds_ab,
                  '%s' % re_obj.nd_ab, '%s' % re_obj.den_ab, 
                  '%s' % re_obj.dr_ab, 
                  '%s' % re_obj.deru_ab, '%s' % re_obj.inhu_ab],
        "Units": ['', '%', 'gallons', '', 'lbs/gallon', '' 'mg/lb ai', 'mg/lb ai'],
        }
    return data

def gett6data_out(re_obj):
    if re_obj.comb_cm == 'No':
        comb_moe_display = 'N/A'
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'Combined (same LOCs)':
        comb_moe_display = '%0.3e' % re_obj.exp_ab_out['comb_moe']
        ari_display = 'N/A'
    elif re_obj.comb_cm == 'ARI (different LOCs)':
        comb_moe_display = 'N/A'
        ari_display = '%0.3e' % re_obj.exp_ab_out['ari']
    data = { 
        "Parameter": ['Application Rate', 
                      'Adult Dermal Exposure', 'Adult Inhalation Exposure', 
                      'Adult Dermal Absorbed Dose', 'Adult Inhalation Absorbed Dose',
                      'Adult Dermal MOE', 'Adult Inhalation MOE', 
                      'Adult Combined Dermal + Inhalation MOE', 'Adult ARI (Dermal + Inhalation)'],
        "Value": ['%0.3e' % re_obj.exp_ab_out['aprt_ab'],
                  '%0.3e' % re_obj.exp_ab_out['der_exp'], '%0.3e' % re_obj.exp_ab_out['inh_exp'],
                  '%0.3e' % re_obj.exp_ab_out['der_abs_exp'], '%0.3e' % re_obj.exp_ab_out['inh_abs_exp'],
                  '%0.3e' % re_obj.exp_ab_out['der_moe'], '%0.3e' % re_obj.exp_ab_out['inh_moe'],
                   comb_moe_display, ari_display],
        "Units": ['lb ai/day', 'mg/day', 'mg/day', 'mg/kg/day', 'mg/kg/day', '', '', '', ''],
        }
    return data















###################################################################################################
def table_0(re_obj):
        #pre-table 0
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Chemical Inputs</H3>
        <div class="out_1">
            <div class="out_1 container_output">
        """
        #table 0 input
        t0data_in = gett0data(re_obj)
        t0rows_in = gethtmlrowsfromcols(t0data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t0rows_in, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

######Indoor Environment#####
def table_1(re_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Indoor Environment:</H3>
        <div class="out_1">
            <H4 class="out_1 collapsible" id="section1"><span></span>Inputs</H4>
            <div class="out_1 container_output">
        """
        #table 1 input
        t1data_in = gett1data_in(re_obj)
        t1rows_in = gethtmlrowsfromcols(t1data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows_in, headings=pvuheadings)))
        html = html + """
                </div>
        """
        html = html + """
        <div class="out_1">
            <H4 class="out_1 collapsible" id="section2"><span></span>Output</H4>
            <div class="out_1 container_output">
        """
        #table 1 output
        t1data_out = gett1data_out(re_obj)
        t1rows_out = gethtmlrowsfromcols(t1data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows_out, headings=pvuheadings)))
        html = html + """
                </div><br>
        """
        return html

######Paints / Preservatives#####
def table_2(re_obj):
        #pre-table 2
        html = """
        <H3 class="out_2 collapsible" id="section2"><span></span>Paints / Preservatives:</H3>
        <div class="out_2">
            <H4 class="out_2 collapsible" id="section2"><span></span>Inputs</H4>
            <div class="out_2 container_output">
        """
        #table 2 input
        t2data_in = gett2data_in(re_obj)
        t2rows_in = gethtmlrowsfromcols(t2data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows_in, headings=pvuheadings)))
        html = html + """
                </div>
        """
        html = html + """
        <div class="out_2">
            <H4 class="out_2 collapsible" id="section2"><span></span>Output</H4>
            <div class="out_2 container_output">
        """
        #table 2 output
        t2data_out = gett2data_out(re_obj)
        t2rows_out = gethtmlrowsfromcols(t2data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows_out, headings=pvuheadings)))
        html = html + """
                </div><br>
        """
        return html

######Treated Pets#####
def table_3(re_obj):
        #pre-table 3
        html = """
        <H3 class="out_3 collapsible" id="section3"><span></span>Treated Pets:</H3>
        <div class="out_3">
            <H4 class="out_3 collapsible" id="section3"><span></span>Inputs</H4>
            <div class="out_3 container_output">
        """
        #table 3 input
        t3data_in = gett3data_in(re_obj)
        t3rows_in = gethtmlrowsfromcols(t3data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows_in, headings=pvuheadings)))
        html = html + """
                </div>
        """
        html = html + """
        <div class="out_3">
            <H4 class="out_3 collapsible" id="section3"><span></span>Output</H4>
            <div class="out_3 container_output">
        """
        #table 3 output
        t3data_out = gett3data_out(re_obj)
        t3rows_out = gethtmlrowsfromcols(t3data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows_out, headings=pvuheadings)))
        html = html + """
                </div><br>
        """
        return html

#############Outdoor Aerosol Space Sprays############
def table_4(re_obj):
        #pre-table 4
        html = """
        <H3 class="out_4 collapsible" id="section4"><span></span>Outdoor Aerosol Space Sprays:</H3>
        <div class="out_4">
            <H4 class="out_4 collapsible" id="section4"><span></span>Inputs</H4>
            <div class="out_4 container_output">
        """
        #table 4 input
        t4data_in = gett4data_in(re_obj)
        t4rows_in = gethtmlrowsfromcols(t4data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t4rows_in, headings=pvuheadings)))
        html = html + """
                </div>
        """
        html = html + """
        <div class="out_4">
            <H4 class="out_4 collapsible" id="section4"><span></span>Output</H4>
            <div class="out_4 container_output">
        """
        #table 4 output
        t4data_out = gett4data_out(re_obj)
        t4rows_out = gethtmlrowsfromcols(t4data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t4rows_out, headings=pvuheadings)))
        html = html + """
                </div><br>
        """
        return html

#############Outdoor Residential Misting Systems############
def table_5(re_obj):
        #pre-table 5
        html = """
        <H3 class="out_5 collapsible" id="section5"><span></span>Outdoor Residential Misting Systems:</H3>
        <div class="out_5">
            <H4 class="out_5 collapsible" id="section5"><span></span>Inputs</H4>
            <div class="out_5 container_output">
        """
        #table 5 input
        t5data_in = gett5data_in(re_obj)
        t5rows_in = gethtmlrowsfromcols(t5data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t5rows_in, headings=pvuheadings)))
        html = html + """
                </div>
        """
        html = html + """
        <div class="out_5">
            <H4 class="out_5 collapsible" id="section5"><span></span>Output</H4>
            <div class="out_5 container_output">
        """
        #table 5 output
        t5data_out = gett5data_out(re_obj)
        t5rows_out = gethtmlrowsfromcols(t5data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t5rows_out, headings=pvuheadings)))
        html = html + """
                </div><br>
        """
        return html

#############Animal Barn Misting Systems############
def table_6(re_obj):
        #pre-table 6
        html = """
        <H3 class="out_6 collapsible" id="section6"><span></span>Animal Barn Misting Systems:</H3>
        <div class="out_6">
            <H4 class="out_6 collapsible" id="section6"><span></span>Inputs</H4>
            <div class="out_6 container_output">
        """
        #table 6 input
        t6data_in = gett6data_in(re_obj)
        t6rows_in = gethtmlrowsfromcols(t6data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t6rows_in, headings=pvuheadings)))
        html = html + """
                </div>
        """
        html = html + """
        <div class="out_6">
            <H4 class="out_6 collapsible" id="section6"><span></span>Output</H4>
            <div class="out_6 container_output">
        """
        #table 6 output
        t6data_out = gett6data_out(re_obj)
        t6rows_out = gethtmlrowsfromcols(t6data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t6rows_out, headings=pvuheadings)))
        html = html + """
                </div><br>
        """
        return html
