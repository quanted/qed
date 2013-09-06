#!/usr/bin/env python
# -*- coding:utf-8 -*-
#*********************************************************#
# @@ScriptName: orehe_output.py
# @@Author: Tao Hong
# @@Create Date: 2013-06-19
# @@Modify Date: 2013-09-06
#*********************************************************#

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
from orehe import orehe_model
from orehe import orehe_tables



class oreheOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        scenario_cm = form.getvalue('scenario_cm')
        all_obj = {}

        actv_cm = form.getvalue('actv_cm')
        exdu_cm = form.getvalue('exdu_cm')
        der_pod_cm = float(form.getvalue('der_pod_cm'))
        der_pod_sor_cm = form.getvalue('der_pod_sor_cm')
        der_abs_cm = float(form.getvalue('der_abs_cm'))
        der_abs_sor_cm = form.getvalue('der_abs_sor_cm')
        der_loc_cm = float(form.getvalue('der_loc_cm'))
        inh_pod_cm = float(form.getvalue('inh_pod_cm'))
        inh_pod_sor_cm = form.getvalue('inh_pod_sor_cm')
        inh_abs_cm = float(form.getvalue('inh_abs_cm'))
        inh_loc_cm = float(form.getvalue('inh_loc_cm'))
        der_wt_cm = float(form.getvalue('der_wt_cm'))
        inh_wt_cm = float(form.getvalue('inh_wt_cm'))
        chd_wt_cm = float(form.getvalue('chd_wt_cm'))
        comb_cm = form.getvalue('comb_cm')
        
        chem_obj = orehe_model.orehe_chem(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                          inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm)
        all_obj['tab_chem'] = chem_obj

        if 'tab_ie' in scenario_cm:
            scna_gh = form.getvalue('scna_gh')
            form_gh = form.getvalue('form_gh')
            apmd_gh = form.getvalue('apmd_gh')
            type_gh = form.getvalue('type_gh')
            aprt_gh = float(form.getvalue('aprt_gh'))
            area_gh = float(form.getvalue('area_gh'))
            deru_gh = float(form.getvalue('deru_gh'))
            inhu_gh = float(form.getvalue('inhu_gh'))

            ie_obj = orehe_model.orehe_ge(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                          inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                                          scna_gh, form_gh, apmd_gh, type_gh, aprt_gh, area_gh, deru_gh, inhu_gh)
            all_obj['tab_ie'] = ie_obj

        if 'tab_pp' in scenario_cm:
            scna_pp_ac = form.getvalue('scna_pp_ac')
            form_pp_ac = form.getvalue('form_pp_ac')
            apmd_pp_ac = form.getvalue('apmd_pp_ac')
            wf_pp_ac = float(form.getvalue('wf_pp_ac'))
            vl_pp_ac = float(form.getvalue('vl_pp_ac'))
            pd_pp_ac = float(form.getvalue('pd_pp_ac'))
            area_pp_ac = float(form.getvalue('area_pp_ac'))
            deru_pp_ac = float(form.getvalue('deru_pp_ac'))
            inhu_pp_ac = float(form.getvalue('inhu_pp_ac'))

            pp_obj = orehe_model.orehe_pp_ac(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                             inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                                             scna_pp_ac, form_pp_ac, apmd_pp_ac, wf_pp_ac, vl_pp_ac, pd_pp_ac, area_pp_ac, deru_pp_ac, inhu_pp_ac)
            all_obj['tab_pp'] = pp_obj

        if 'tab_tp' in scenario_cm:
            scna_tp_dp = form.getvalue('scna_tp_dp')
            form_tp_dp = form.getvalue('form_tp_dp')
            apmd_tp_dp = form.getvalue('apmd_tp_dp')
            aai_tp_dp = float(form.getvalue('aai_tp_dp'))
            aa_tp_dp = float(form.getvalue('aa_tp_dp'))
            area_tp_dp = float(form.getvalue('area_tp_dp'))
            deru_tp_dp = float(form.getvalue('deru_tp_dp'))
            inhu_tp_dp = float(form.getvalue('inhu_tp_dp'))

            tp_obj = orehe_model.orehe_tp_dp(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                             inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                                             scna_tp_dp, form_tp_dp, apmd_tp_dp, aai_tp_dp, aa_tp_dp, area_tp_dp, deru_tp_dp, inhu_tp_dp)
            all_obj['tab_tp'] = tp_obj


        if 'tab_oa' in scenario_cm:
            lab_oa = form.getvalue('lab_oa')
            ai_oa = float(form.getvalue('ai_oa'))
            at_oz_oa = float(form.getvalue('at_oz_oa'))
            at_g_oa = float(form.getvalue('at_g_oa'))
            at_ml_oa = float(form.getvalue('at_ml_oa'))
            den_oa = float(form.getvalue('den_oa'))
            deru_oa = float(form.getvalue('deru_oa'))
            inhu_oa = float(form.getvalue('inhu_oa'))

            oa_obj = orehe_model.orehe_oa(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                          inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                                          lab_oa, ai_oa, at_oz_oa, at_g_oa, at_ml_oa, den_oa, deru_oa, inhu_oa)
            all_obj['tab_oa'] = oa_obj

        if 'tab_or' in scenario_cm:
            ai_or = float(form.getvalue('ai_or'))
            ds_or = float(form.getvalue('ds_or'))
            nd_or = float(form.getvalue('nd_or'))
            den_or = float(form.getvalue('den_or'))
            dr_or = float(form.getvalue('dr_or'))
            deru_or = float(form.getvalue('deru_or'))
            inhu_or = float(form.getvalue('inhu_or'))

            or_tab = orehe_model.orehe_or(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                          inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                                          ai_or, ds_or, nd_or, den_or, dr_or, deru_or, inhu_or)
            all_obj['tab_or'] = or_tab

        if 'tab_ab' in scenario_cm:
            ai_ab = float(form.getvalue('ai_ab'))
            ds_ab = float(form.getvalue('ds_ab'))
            nd_ab = float(form.getvalue('nd_ab'))
            den_ab = float(form.getvalue('den_ab'))
            dr_ab = float(form.getvalue('dr_ab'))
            deru_ab = float(form.getvalue('deru_ab'))
            inhu_ab = float(form.getvalue('inhu_ab'))

            ab_tab = orehe_model.orehe_ab(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                          inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                                          ai_ab, ds_ab, nd_ab, den_ab, dr_ab, deru_ab, inhu_ab)
            all_obj['tab_ab'] = ab_tab



        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html',  {'model':'orehe','page':'output'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'orehe', 
                'model_attributes':'ORE Output'})
        html = html + orehe_tables.table_all(scenario_cm, all_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', oreheOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
