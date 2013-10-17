#!/usr/bin/env python
# -*- coding:utf-8 -*-
#*********************************************************#
# @@ScriptName: orehe_batchoutput.py
# @@Author: Tao Hong
# @@Create Date: 2013-09-05
# @@Modify Date: 2013-09-06
#*********************************************************#
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from StringIO import StringIO
import csv
import sys
sys.path.append("../orehe")
from orehe import orehe_model, orehe_tables
import logging

logger = logging.getLogger('oreheBatchPage')


#inputs
actv_cm = []
exdu_cm = []
der_pod_cm = []
der_pod_sor_cm = []
der_abs_cm = []
der_abs_sor_cm = []
der_loc_cm = []
inh_pod_cm = []
inh_pod_sor_cm = []
inh_abs_cm = []
inh_loc_cm = []
der_wt_cm = []
inh_wt_cm = []
chd_wt_cm = []
comb_cm = []

scna_gh = []
form_gh = []
apmd_gh = []
type_gh = []
aprt_gh = []
area_gh = []
deru_gh = []
inhu_gh = []

scna_pp_ac = []
form_pp_ac = []
apmd_pp_ac = []
wf_pp_ac = []
vl_pp_ac = []
pd_pp_ac = []
area_pp_ac = []
deru_pp_ac = []
inhu_pp_ac = []

scna_tp_dp = []
form_tp_dp = []
apmd_tp_dp = []
aai_tp_dp = []
aa_tp_dp = []
area_tp_dp = []
deru_tp_dp = []
inhu_tp_dp = []

lab_oa = []
ai_oa = []
at_oz_oa = []
at_g_oa = []
at_ml_oa = []
den_oa = []
deru_oa = []
inhu_oa = []

ai_or = []
ds_or = []
nd_or = []
den_or = []
dr_or = []
deru_or = []
inhu_or = []

ai_ab = []
ds_ab = []
nd_ab = []
den_ab = []
dr_ab = []
deru_ab = []
inhu_ab = []

run_ie = []
run_pp = []
run_tp = []
run_oa = []
run_or = []
run_ab = []

#outputs

def html_table(row, iter):
    all_obj_temp = {}
    scenario_cm_temp = []
    actv_cm_temp = row[0]
    actv_cm.append(actv_cm_temp)
    exdu_cm_temp = row[1]
    exdu_cm.append(exdu_cm_temp)
    der_pod_cm_temp = float(row[2])
    der_pod_cm.append(der_pod_cm_temp)
    der_pod_sor_cm_temp = row[3]
    der_pod_sor_cm.append(der_pod_sor_cm_temp)
    der_abs_cm_temp = float(row[4])
    der_abs_cm.append(der_abs_cm_temp)
    der_abs_sor_cm_temp = row[5]
    der_abs_sor_cm.append(der_abs_sor_cm_temp)
    der_loc_cm_temp = float(row[6])
    der_loc_cm.append(der_loc_cm_temp)
    inh_pod_cm_temp = float(row[7])
    inh_pod_cm.append(inh_pod_cm_temp)
    inh_pod_sor_cm_temp = row[8]
    inh_pod_sor_cm.append(inh_pod_sor_cm_temp)
    inh_abs_cm_temp = float(row[9])
    inh_abs_cm.append(inh_abs_cm_temp)
    inh_loc_cm_temp = float(row[10])
    inh_loc_cm.append(inh_loc_cm_temp)
    der_wt_cm_temp = float(row[11])
    der_wt_cm.append(der_wt_cm_temp)
    inh_wt_cm_temp = float(row[12])
    inh_wt_cm.append(inh_wt_cm_temp)
    chd_wt_cm_temp = float(row[13])
    chd_wt_cm.append(chd_wt_cm_temp)
    comb_cm_temp = row[14]
    comb_cm.append(comb_cm_temp)
    chem_obj_temp = orehe_model.orehe_chem(actv_cm_temp, exdu_cm_temp, der_pod_cm_temp, der_pod_sor_cm_temp, der_abs_cm_temp, der_abs_sor_cm_temp, der_loc_cm_temp, 
                                          inh_pod_cm_temp, inh_pod_sor_cm_temp, inh_abs_cm_temp, inh_loc_cm_temp, der_wt_cm_temp, inh_wt_cm_temp, chd_wt_cm_temp, comb_cm_temp)
    all_obj_temp['tab_chem'] = chem_obj_temp


    run_ie_temp = float(row[15])
    run_ie.append(run_ie_temp)
    if run_ie_temp == 1:
        scenario_cm_temp.append('tab_ie')
        scna_gh_temp = row[16]
        scna_gh.append(scna_gh_temp)
        form_gh_temp = row[17]
        form_gh.append(form_gh_temp)
        apmd_gh_temp = row[18]
        apmd_gh.append(apmd_gh_temp)
        type_gh_temp = row[19]
        type_gh.append(type_gh_temp)
        aprt_gh_temp = float(row[20])
        aprt_gh.append(aprt_gh_temp)
        area_gh_temp = float(row[21])
        area_gh.append(area_gh_temp)
        deru_gh_temp = float(row[22])
        deru_gh.append(deru_gh_temp)
        inhu_gh_temp = float(row[23])
        inhu_gh.append(inhu_gh_temp)
        ie_obj_temp = orehe_model.orehe_ge(actv_cm_temp, exdu_cm_temp, der_pod_cm_temp, der_pod_sor_cm_temp, der_abs_cm_temp, der_abs_sor_cm_temp, der_loc_cm_temp, 
                                          inh_pod_cm_temp, inh_pod_sor_cm_temp, inh_abs_cm_temp, inh_loc_cm_temp, der_wt_cm_temp, inh_wt_cm_temp, chd_wt_cm_temp, comb_cm_temp, 
                                          scna_gh_temp, form_gh_temp, apmd_gh_temp, type_gh_temp, aprt_gh_temp, area_gh_temp, deru_gh_temp, inhu_gh_temp)
        all_obj_temp['tab_ie'] = ie_obj_temp


    run_pp_temp = float(row[24])
    run_pp.append(run_pp_temp)
    if run_pp_temp == 1:
        scenario_cm_temp.append('tab_pp')
        scna_pp_ac_temp = row[25]
        scna_pp_ac.append(scna_pp_ac_temp)
        form_pp_ac_temp = row[26]
        form_pp_ac.append(form_pp_ac_temp)
        apmd_pp_ac_temp = row[27]
        apmd_pp_ac.append(apmd_pp_ac_temp)
        wf_pp_ac_temp = float(row[28])
        wf_pp_ac.append(wf_pp_ac_temp)
        vl_pp_ac_temp = float(row[29])
        vl_pp_ac.append(vl_pp_ac_temp)
        pd_pp_ac_temp = float(row[30])
        pd_pp_ac.append(pd_pp_ac_temp)
        area_pp_ac_temp = float(row[31])
        area_pp_ac.append(area_pp_ac_temp)
        deru_pp_ac_temp = float(row[32])
        deru_pp_ac.append(deru_pp_ac_temp)
        inhu_pp_ac_temp = float(row[33])
        inhu_pp_ac.append(inhu_pp_ac_temp)
        pp_obj_temp = orehe_model.orehe_pp_ac(actv_cm_temp, exdu_cm_temp, der_pod_cm_temp, der_pod_sor_cm_temp, der_abs_cm_temp, der_abs_sor_cm_temp, der_loc_cm_temp, 
                                              inh_pod_cm_temp, inh_pod_sor_cm_temp, inh_abs_cm_temp, inh_loc_cm_temp, der_wt_cm_temp, inh_wt_cm_temp, chd_wt_cm_temp, comb_cm_temp, 
                                              scna_pp_ac_temp, form_pp_ac_temp, apmd_pp_ac_temp, wf_pp_ac_temp, vl_pp_ac_temp, pd_pp_ac_temp, area_pp_ac_temp, deru_pp_ac_temp, inhu_pp_ac_temp)
        all_obj_temp['tab_pp'] = pp_obj_temp


    run_tp_temp = float(row[34])
    run_tp.append(run_tp_temp)
    if run_tp_temp == 1:
        scenario_cm_temp.append('tab_tp')
        scna_tp_dp_temp = row[35]
        scna_tp_dp.append(scna_tp_dp)
        form_tp_dp_temp = row[36]
        form_tp_dp.append(form_tp_dp)
        apmd_tp_dp_temp = row[37]
        apmd_tp_dp.append(apmd_tp_dp)
        aai_tp_dp_temp = float(row[38])
        aai_tp_dp.append(aai_tp_dp)
        aa_tp_dp_temp = float(row[39])
        aa_tp_dp.append(aa_tp_dp)
        area_tp_dp_temp = float(row[40])
        area_tp_dp.append(area_tp_dp)
        deru_tp_dp_temp = float(row[41])
        deru_tp_dp.append(deru_tp_dp)
        inhu_tp_dp_temp = float(row[42])
        inhu_tp_dp.append(inhu_tp_dp)
        tp_obj_temp = orehe_model.orehe_tp_dp(actv_cm_temp, exdu_cm_temp, der_pod_cm_temp, der_pod_sor_cm_temp, der_abs_cm_temp, der_abs_sor_cm_temp, der_loc_cm_temp, 
                                              inh_pod_cm_temp, inh_pod_sor_cm_temp, inh_abs_cm_temp, inh_loc_cm_temp, der_wt_cm_temp, inh_wt_cm_temp, chd_wt_cm_temp, comb_cm_temp, 
                                              scna_tp_dp_temp, form_tp_dp_temp, apmd_tp_dp_temp, aai_tp_dp_temp, aa_tp_dp_temp, area_tp_dp_temp, deru_tp_dp_temp, inhu_tp_dp_temp)
        all_obj_temp['tab_tp'] = tp_obj_temp


    run_oa_temp = float(row[43])
    run_oa.append(run_oa_temp)
    if run_oa_temp == 1:
        scenario_cm_temp.append('tab_oa')
        lab_oa_temp = row[44]
        lab_oa.append(lab_oa)
        ai_oa_temp = float(row[45])
        ai_oa.append(ai_oa)
        at_oz_oa_temp = row[46]
        at_oz_oa.append(at_oz_oa)
        at_g_oa_temp = row[47]
        at_g_oa.append(at_g_oa)
        at_ml_oa_temp = row[48]
        at_ml_oa.append(at_ml_oa)
        den_oa_temp = row[49]
        den_oa.append(den_oa)
        deru_oa_temp = float(row[50])
        deru_oa.append(deru_oa)
        inhu_oa_temp = float(row[51])
        inhu_oa.append(inhu_oa)
        oa_obj_temp = orehe_model.orehe_oa(actv_cm_temp, exdu_cm_temp, der_pod_cm_temp, der_pod_sor_cm_temp, der_abs_cm_temp, der_abs_sor_cm_temp, der_loc_cm_temp, 
                                           inh_pod_cm_temp, inh_pod_sor_cm_temp, inh_abs_cm_temp, inh_loc_cm_temp, der_wt_cm_temp, inh_wt_cm_temp, chd_wt_cm_temp, comb_cm_temp, 
                                           lab_oa_temp, ai_oa_temp, at_oz_oa_temp, at_g_oa_temp, at_ml_oa_temp, den_oa_temp, deru_oa_temp, inhu_oa_temp)
        all_obj_temp['tab_oa'] = oa_obj_temp


    run_or_temp = float(row[52])
    run_or.append(run_or_temp)
    if run_or_temp == 1:
        scenario_cm_temp.append('tab_or')
        ai_or_temp = float(row[53])
        ai_or.append(ai_or_temp)
        ds_or_temp = float(row[54])
        ds_or.append(ds_or_temp)
        nd_or_temp = float(row[55])
        nd_or.append(nd_or_temp)
        den_or_temp = float(row[56])
        den_or.append(den_or_temp)
        dr_or_temp = float(row[57])
        dr_or.append(dr_or_temp)
        deru_or_temp = float(row[58])
        deru_or.append(deru_or_temp)
        inhu_or_temp = float(row[59])
        inhu_or.append(inhu_or_temp)
        or_tab_temp = orehe_model.orehe_or(actv_cm_temp, exdu_cm_temp, der_pod_cm_temp, der_pod_sor_cm_temp, der_abs_cm_temp, der_abs_sor_cm_temp, der_loc_cm_temp, 
                                           inh_pod_cm_temp, inh_pod_sor_cm_temp, inh_abs_cm_temp, inh_loc_cm_temp, der_wt_cm_temp, inh_wt_cm_temp, chd_wt_cm_temp, comb_cm_temp, 
                                           ai_or_temp, ds_or_temp, nd_or_temp, den_or_temp, dr_or_temp, deru_or_temp, inhu_or_temp)
        all_obj_temp['tab_or'] = or_tab_temp


    run_ab_temp = float(row[60])
    run_ab.append(run_ab_temp)
    if run_ab_temp == 1:
        scenario_cm_temp.append('tab_ab')
        ai_ab_temp = float(row[61])
        ai_ab.append(ai_ab_temp)
        ds_ab_temp = float(row[62])
        ds_ab.append(ds_ab_temp)
        nd_ab_temp = float(row[63])
        nd_ab.append(nd_ab_temp)
        den_ab_temp = float(row[64])
        den_ab.append(den_ab_temp)
        dr_ab_temp = float(row[65])
        dr_ab.append(dr_ab_temp)
        deru_ab_temp = float(row[66])
        deru_ab.append(deru_ab_temp)
        inhu_ab_temp = float(row[67])
        inhu_ab.append(inhu_ab_temp)
        ab_tab_temp = orehe_model.orehe_ab(actv_cm_temp, exdu_cm_temp, der_pod_cm_temp, der_pod_sor_cm_temp, der_abs_cm_temp, der_abs_sor_cm_temp, der_loc_cm_temp, 
                                           inh_pod_cm_temp, inh_pod_sor_cm_temp, inh_abs_cm_temp, inh_loc_cm_temp, der_wt_cm_temp, inh_wt_cm_temp, chd_wt_cm_temp, comb_cm_temp, 
                                           ai_ab_temp, ds_ab_temp, nd_ab_temp, den_ab_temp, dr_ab_temp, deru_ab_temp, inhu_ab_temp)
        all_obj_temp['tab_ab'] = ab_tab_temp




    Input_header="""<H3 class="out_0 collapsible" id="section0"><span></span>Batch Calculation of Iteration %s</H3>
                        <div class="out_">
                 """%(iter)

    table_all_out = orehe_tables.table_all(scenario_cm_temp, all_obj_temp)
    html_table_temp = Input_header + table_all_out + "</div><br>"

    return html_table_temp           
    
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    reader.next()
    reader.next()
    reader.next()
    i=1
    iter_html=""
    for row in reader:
        iter_html = iter_html +html_table(row,i)
        i=i+1
    return iter_html


class oreheBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['upfile']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', 'title')
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'orehe','page':'batchinput'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {
                'model':'orehe',
                'model_attributes':'ORE Batch Output'})
        # html = html + orehe_tables.timestamp()
        html = html + iter_html
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', oreheBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()



