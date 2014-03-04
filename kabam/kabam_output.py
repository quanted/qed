# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:34:41 2012

@author: msnyde02
"""
# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import sys
sys.path.append("../kabam")
from kabam import kabam_model,kabam_tables
from uber import uber_lib
from django.template import Context, Template
from django.utils import simplejson
import rest_funcs

class KabamOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        chemical_name = form.getvalue('name')
        l_kow = float(form.getvalue('lkow'))
        k_oc = float(form.getvalue('Koc'))
        c_wdp_2 = float(form.getvalue('beec'))
        c_wdp = float(form.getvalue('beec')) / 1000000
        water_column_EEC = float(form.getvalue('weec'))
        c_wto = float(water_column_EEC) / 1000000
        mineau_scaling_factor = float(form.getvalue('sf'))
        x_poc = float(form.getvalue('cpoc'))
        x_doc = float(form.getvalue('cdoc'))
        c_ox = float(form.getvalue('cox'))
        w_t = float(form.getvalue('wt'))
        c_ss = float(form.getvalue('css'))
        oc = float(form.getvalue('oc'))/100
        k_ow = 10**(float(l_kow))
        Species_of_the_tested_bird = form.getvalue('Species_of_the_tested_bird')
        bw_quail = form.getvalue('bw_quail')
        bw_duck = form.getvalue('bw_duck')
        bwb_other = form.getvalue('bwb_other')
        avian_ld50 = float(form.getvalue('ald50'))
        avian_lc50 = float(form.getvalue('alc50'))
        avian_noaec = float(form.getvalue('aNOAEC'))
        m_species = form.getvalue('m_species')
        bw_rat=form.getvalue('bw_rat')
        bwm_other=form.getvalue('bwm_other')
#        print 'weight=', body_weight_of_the_tested_mamm_other
        mammalian_ld50 = float(form.getvalue('mld50'))
        mammalian_lc50 = float(form.getvalue('mlc50'))
        mammalian_chronic_endpoint = float(form.getvalue('m_chronic'))
#        body_weight_of_the_assessed_mamm = float(form.getvalue('bw_assess_m'))
        #diet_for_large_fish = form.getvalue('Diet_lfish')
        lf_p_sediment = float(form.getvalue('lfish_p_sediment'))/100
        lf_p_phytoplankton = float(form.getvalue('lfish_p_phyto'))/100
        lf_p_zooplankton = float(form.getvalue('lfish_p_zoo'))/100
        lf_p_benthic_invertebrates = float(form.getvalue('lfish_p_beninv'))/100
        lf_p_filter_feeders = float(form.getvalue('lfish_p_ff'))/100
        lf_p_small_fish = float(form.getvalue('lfish_p_sfish'))/100
        lf_p_medium_fish = float(form.getvalue('lfish_p_mfish'))/100
        #diet_for_medium_fish = form.getvalue('Diet_mfish')
        mf_p_sediment = float(form.getvalue('mfish_p_sediment'))
        #print type(mf_p_sediment)
        mf_p_sediment = float(mf_p_sediment)
        mf_p_phytoplankton = float(form.getvalue('mfish_p_phyto'))
        mf_p_zooplankton = float(form.getvalue('mfish_p_zoo'))
        mf_p_benthic_invertebrates = float(form.getvalue('mfish_p_beninv'))/100
        mf_p_filter_feeders = float(form.getvalue('mfish_p_ff'))
        mf_p_small_fish = float(form.getvalue('mfish_p_sfish'))/100
        #diet_for_small_fish = form.getvalue('Diet_sfish')
        sf_p_sediment = float(form.getvalue('sfish_p_sediment'))
        sf_p_phytoplankton = float(form.getvalue('sfish_p_phyto'))
        sf_p_zooplankton = float(form.getvalue('sfish_p_zoo'))/100
        sf_p_benthic_invertebrates = float(form.getvalue('sfish_p_beninv'))/100
        sf_p_filter_feeders = float(form.getvalue('sfish_p_ff'))
        #diet_for_filter_feeder = form.getvalue('Diet_ff')
        ff_p_sediment = float(form.getvalue('ff_p_sediment'))/100
        ff_p_phytoplankton = float(form.getvalue('ff_p_phyto'))/100
        ff_p_zooplankton = float(form.getvalue('ff_p_zoo'))/100
        ff_p_benthic_invertebrates = float(form.getvalue('ff_p_beninv'))
        #diet_for_invertebrates = form.getvalue('Diet_invert')
        beninv_p_sediment = float(form.getvalue('beninv_p_sediment'))/100
        beninv_p_phytoplankton = float(form.getvalue('beninv_p_phyto'))/100
        beninv_p_zooplankton = float(form.getvalue('beninv_p_zoo'))/100
        #diet_for_zooplankton = form.getvalue('Diet_zoo')
        zoo_p_sediment = float(form.getvalue('zoo_p_sediment'))
        zoo_p_phyto = float(form.getvalue('zoo_p_phyto'))/100
        #characteristics_sediment = form.getvalue('char_s')
        s_lipid = float(form.getvalue('s_lipid'))/100
        s_NLOM = float(form.getvalue('s_NLOM'))/100
        s_water = float(form.getvalue('s_water'))/100
        s_respire = form.getvalue('s_respire')
        #characteristics_phytoplankton = form.getvalue('char_phyto')
        v_lb_phytoplankton = float(form.getvalue('phyto_lipid'))/100
        v_nb_phytoplankton = float(form.getvalue('phyto_NLOM'))/100
        v_wb_phytoplankton = float(form.getvalue('phyto_water'))/100
        phyto_respire = form.getvalue('phyto_respire')
        #characteristics_zooplankton = form.getvalue('char_zoo')
        wb_zoo = float(form.getvalue('zoo_ww'))
        v_lb_zoo = float(form.getvalue('zoo_lipid'))/100
        v_nb_zoo = float(form.getvalue('zoo_NLOM'))/100
        v_wb_zoo = float(form.getvalue('zoo_water'))/100
        zoo_respire = form.getvalue('zoo_respire')
        #characteristics_benthic_invertebrates = form.getvalue('char_beninv')
        wb_beninv = float(form.getvalue('beninv_ww'))
        v_lb_beninv = float(form.getvalue('beninv_lipid'))/100
        v_nb_beninv = float(form.getvalue('beninv_NLOM'))/100
        v_wb_beninv = float(form.getvalue('beninv_water'))/100
        beninv_respire = form.getvalue('beninv_respire')
        #characteristics_ff = form.getvalue('char_ff')
        wb_ff = float(form.getvalue('ff_ww'))
        v_lb_ff = float(form.getvalue('ff_lipid'))/100
        v_nb_ff = float(form.getvalue('ff_NLOM'))/100
        v_wb_ff = float(form.getvalue('ff_water'))/100
        ff_respire = form.getvalue('ff_respire')
        #characteristics_smfish = form.getvalue('char_sfish')
        wb_sf = float(form.getvalue('sfish_ww'))
        v_lb_sf = float(form.getvalue('sfish_lipid'))/100
        v_nb_sf = float(form.getvalue('sfish_NLOM'))/100
        v_wb_sf = float(form.getvalue('sfish_water'))/100
        sfish_respire = form.getvalue('sfish_respire')
        #characteristics_medfish = form.getvalue('char_mfish')
        wb_mf = float(form.getvalue('mfish_ww'))
        v_lb_mf = float(form.getvalue('mfish_lipid'))/100
        v_nb_mf = float(form.getvalue('mfish_NLOM'))/100
        v_wb_mf = float(form.getvalue('mfish_water'))/100
        mfish_respire = form.getvalue('mfish_respire')
        #characteristics_larfish = form.getvalue('char_lfish')
        wb_lf = float(form.getvalue('lfish_ww'))
        v_lb_lf = float(form.getvalue('lfish_lipid'))/100
        v_nb_lf = float(form.getvalue('lfish_NLOM'))/100
        v_wb_lf = float(form.getvalue('lfish_water'))/100
        lfish_respire = form.getvalue('lfish_respire')
        rate_constants = form.getvalue('rate_c')
        # phytoplankton growth rate constant
        kg_phytoplankton = 0.1
        # phytoplankton diet uptake rate constant
        kd_phytoplankton = 0
        #phytoplankton fecal elimination rate constant  
        ke_phytoplankton = 0
        # fraction of respiratory ventilation involving overlying water
        mo_phytoplankton = 1
        # fraction of respiratory ventilation involving pore water
        mp_phytoplankton = 0    
        # rate constant for pesticide metabolic transformation
        km_phytoplankton = 0
         # rate constant for pesticide metabolic transformation
        km_zoo = 0

        # k_bw_phytoplankton = 0
        # k_bw_zoo = 0
        # k_bw_beninv = 0
        # k_bw_ff = 0
        # k_bw_sf = 0
        # k_bw_mf = 0
        # k_bw_lf = 0
        # cb_phytoplankton_v = 0
        # cb_zoo_v = 0
        # cb_beninv_v = 0
        # cb_ff_v = 0
        # cb_sf_v = 0
        # cb_mf_v = 0
        # cb_lf_v = 0
        k1_phytoplankton = float(form.getvalue('phyto_k1'))
        k2_phytoplankton = float(form.getvalue('phyto_k2'))
        kd_phytoplankton = float(form.getvalue('phyto_kd'))
        ke_phytoplankton = float(form.getvalue('phyto_ke'))
        km_phytoplankton = float(form.getvalue('phyto_km'))
        k1_zoo = float(form.getvalue('zoo_k1'))
        k2_zoo = float(form.getvalue('zoo_k2'))
        kd_zoo = float(form.getvalue('zoo_kd'))
        ke_zoo = float(form.getvalue('zoo_ke'))
        km_zoo = float(form.getvalue('zoo_km'))
        k1_beninv = float(form.getvalue('beninv_k1'))
        k2_beninv = float(form.getvalue('beninv_k2'))
        kd_beninv = float(form.getvalue('beninv_kd'))
        ke_beninv = float(form.getvalue('beninv_ke'))
        km_beninv = float(form.getvalue('beninv_km'))
        k1_ff = float(form.getvalue('ff_k1'))
        k2_ff = float(form.getvalue('ff_k2'))
        kd_ff = float(form.getvalue('ff_kd'))
        ke_ff = float(form.getvalue('ff_ke'))
        km_ff = float(form.getvalue('ff_km'))
        k1_sf = float(form.getvalue('sfish_k1'))
        k2_sf = float(form.getvalue('sfish_k2'))
        kd_sf = float(form.getvalue('sfish_kd'))
        ke_sf = float(form.getvalue('sfish_ke'))
        km_sf = float(form.getvalue('sfish_km'))
        k1_mf = float(form.getvalue('mfish_k1'))
        k2_mf = float(form.getvalue('mfish_k2'))
        kd_mf = float(form.getvalue('mfish_kd'))
        ke_mf = float(form.getvalue('mfish_ke'))
        km_mf = float(form.getvalue('mfish_km'))
        k1_lf = float(form.getvalue('lfish_k1'))
        k2_lf = float(form.getvalue('lfish_k2'))
        kd_lf = float(form.getvalue('lfish_kd'))
        ke_lf = float(form.getvalue('lfish_ke'))
        km_lf = float(form.getvalue('lfish_km'))

        # else: # calculate values for rate constants
        #     k_bw_phytoplankton = kabam_model.k_bw_phytoplankton_f(v_lb_phytoplankton, v_nb_phytoplankton, k_ow, v_wb_phytoplankton)
        #     k1_phytoplankton = k1_phytoplankton_f(k_ow)
        #     k2_phytoplankton = k2_phytoplankton_f(k_ow, k1_phytoplankton, k_bw_phytoplankton)
        #     k_bw_zoo = k_bw_zoo_f(v_lb_zoo, k_ow, v_nb_zoo, v_wb_zoo)
        #     k1_zoo = k1_zoo_f(k_ow, wb_zoo, c_ox)
        #     k2_zoo = k2_zoo_f(k_bw_zoo, k1_zoo)
        #     kd_zoo = kd_zoo_f(k_ow, wb_zoo, w_t)               
        #     ke_zoo = ke_zoo_f(k_ow, wb_zoo, v_lb_zoo, v_nb_zoo, zoo_p_sediment, s_lipid, s_NLOM, zoo_p_phyto, v_lb_phytoplankton, v_nb_phytoplankton, s_water, v_wb_phytoplankton, w_t, v_wb_zoo)
        #     k_bw_beninv = k_bw_beninv_f(v_lb_beninv, k_ow, v_nb_beninv, v_wb_beninv)                
        #     k1_beninv = k1_beninv_f(k_ow, wb_beninv, c_ox)        
        #     k2_beninv = k2_beninv_f(k1_beninv, k_bw_beninv)                
        #     kd_beninv = kd_beninv_f(k_ow, wb_beninv, w_t)                
        #     ke_beninv = ke_beninv_f(k_ow, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t, v_lb_beninv, v_nb_beninv, v_wb_beninv)
        #     k_bw_ff = k_bw_ff_f(v_lb_ff, k_ow, v_nb_ff, v_wb_ff)                
        #     k1_ff = k1_ff_f(k_ow, wb_ff, c_ox)
        #     k2_ff = k2_ff_f(k1_ff, k_bw_ff)                
        #     kd_ff = kd_ff_f(k_ow, wb_ff, w_t, c_ss, c_ox)
        #     ke_ff = ke_ff_f(k_ow, ff_p_sediment, v_lb_ff, v_nb_ff, v_wb_ff, ff_p_phytoplankton,  c_ss, c_ox, s_lipid, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t)
        #     k_bw_sf = k_bw_sf_f(v_lb_sf, k_ow, v_nb_sf, v_wb_sf)                
        #     k1_sf = k1_sf_f(k_ow, wb_sf, c_ox)
        #     k2_sf = k2_sf_f(k1_sf, k_bw_sf)
        #     kd_sf = kd_sf_f(k_ow, wb_sf, w_t, c_ss, c_ox)
        #     ke_sf = ke_sf_f(k_ow, v_lb_sf, v_nb_sf, v_wb_sf, c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, ff_p_zooplankton, s_NLOM, v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, c_ss, wb_ff,  wb_sf, w_t, v_nb_beninv, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, v_wb_beninv, v_wb_ff, sf_p_filter_feeders, v_lb_ff)
        #     k_bw_mf = k_bw_mf_f(v_lb_mf, k_ow, v_nb_mf, v_wb_mf)                
        #     k1_mf = k1_mf_f(k_ow, wb_mf, c_ox)
        #     k2_mf = k2_mf_f(k1_mf, k_bw_mf) 
        #     kd_mf = kd_mf_f(k_ow, wb_mf, w_t, c_ss, c_ox)
        #     ke_mf = ke_mf_f(k_ow, v_lb_mf, v_nb_mf, v_wb_mf, wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
        #     k_bw_lf = k_bw_lf_f(v_lb_lf, k_ow, v_nb_lf, v_wb_lf)
        #     k1_lf = k1_lf_f(k_ow, wb_lf, c_ox)
        #     k2_lf = k2_lf_f(k1_lf, k_bw_lf)
        #     kd_lf = kd_lf_f(k_ow, wb_lf, w_t, c_ss, c_ox)
        #     ke_lf = ke_lf_f(k_ow, v_lb_lf, v_nb_lf, v_wb_lf, wb_lf, s_lipid, lf_p_sediment, v_lb_phytoplankton, lf_p_phytoplankton, v_lb_beninv, v_lb_zoo, lf_p_benthic_invertebrates, lf_p_zooplankton, lf_p_filter_feeders, v_lb_ff, v_lb_sf, lf_p_small_fish, s_water, lf_p_medium_fish, v_nb_mf, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_wb_sf, wb_mf, w_t, mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, v_lb_mf, v_wb_mf, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf)

        # cb_phytoplankton_v = cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)   
        # cb_zoo_v = cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment)
        # cb_beninv_v = cb_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv)
        # cb_ff_v = cb_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
        # cb_sf_v = cb_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
        # cb_mf_v = cb_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
        # cb_lf_v = cb_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)


        #     k_bw_phytoplankton = k_bw_phytoplankton_f(v_lb_phytoplankton, v_nb_phytoplankton, k_ow, v_wb_phytoplankton)
        #     k1_phytoplankton = k1_phytoplankton_f(k_ow)
        #     k2_phytoplankton = k2_phytoplankton_f(k_ow, k1_phytoplankton, k_bw_phytoplankton)
        #     k_bw_zoo = k_bw_zoo_f(v_lb_zoo, k_ow, v_nb_zoo, v_wb_zoo)
        #     k1_zoo = k1_zoo_f(k_ow, wb_zoo, c_ox)
        #     k2_zoo = k2_zoo_f(k_bw_zoo, k1_zoo)
        #     kd_zoo = kd_zoo_f(k_ow, wb_zoo, w_t)               
        #     ke_zoo = ke_zoo_f(k_ow, wb_zoo, v_lb_zoo, v_nb_zoo, zoo_p_sediment, s_lipid, s_NLOM, zoo_p_phyto, v_lb_phytoplankton, v_nb_phytoplankton, s_water, v_wb_phytoplankton, w_t, v_wb_zoo)
        #     k_bw_beninv = k_bw_beninv_f(v_lb_beninv, k_ow, v_nb_beninv, v_wb_beninv)                
        #     k1_beninv = k1_beninv_f(k_ow, wb_beninv, c_ox)        
        #     k2_beninv = k2_beninv_f(k1_beninv, k_bw_beninv)                
        #     kd_beninv = kd_beninv_f(k_ow, wb_beninv, w_t)                
        #     ke_beninv = ke_beninv_f(k_ow, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t, v_lb_beninv, v_nb_beninv, v_wb_beninv)
        #     k_bw_ff = k_bw_ff_f(v_lb_ff, k_ow, v_nb_ff, v_wb_ff)                
        #     k1_ff = k1_ff_f(k_ow, wb_ff, c_ox)
        #     k2_ff = k2_ff_f(k1_ff, k_bw_ff)                
        #     kd_ff = kd_ff_f(k_ow, wb_ff, w_t, c_ss, c_ox)
        #     ke_ff = ke_ff_f(k_ow, ff_p_sediment, v_lb_ff, v_nb_ff, v_wb_ff, ff_p_phytoplankton,  c_ss, c_ox, s_lipid, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t)
        #     k_bw_sf = k_bw_sf_f(v_lb_sf, k_ow, v_nb_sf, v_wb_sf)                
        #     k1_sf = k1_sf_f(k_ow, wb_sf, c_ox)
        #     k2_sf = k2_sf_f(k1_sf, k_bw_sf)
        #     kd_sf = kd_sf_f(k_ow, wb_sf, w_t, c_ss, c_ox)
        #     ke_sf = ke_sf_f(k_ow, v_lb_sf, v_nb_sf, v_wb_sf, c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, ff_p_zooplankton, s_NLOM, v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, c_ss, wb_ff,  wb_sf, w_t, v_nb_beninv, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, v_wb_beninv, v_wb_ff, sf_p_filter_feeders, v_lb_ff)
        #     k_bw_mf = k_bw_mf_f(v_lb_mf, k_ow, v_nb_mf, v_wb_mf)                
        #     k1_mf = k1_mf_f(k_ow, wb_mf, c_ox)
        #     k2_mf = k2_mf_f(k1_mf, k_bw_mf) 
        #     kd_mf = kd_mf_f(k_ow, wb_mf, w_t, c_ss, c_ox)
        #     ke_mf = ke_mf_f(k_ow, v_lb_mf, v_nb_mf, v_wb_mf, wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
        #     k_bw_lf = k_bw_lf_f(v_lb_lf, k_ow, v_nb_lf, v_wb_lf)
        #     k1_lf = k1_lf_f(k_ow, wb_lf, c_ox)
        #     k2_lf = k2_lf_f(k1_lf, k_bw_lf)
        #     kd_lf = kd_lf_f(k_ow, wb_lf, w_t, c_ss, c_ox)
        #     ke_lf = ke_lf_f(k_ow, v_lb_lf, v_nb_lf, v_wb_lf, wb_lf, s_lipid, lf_p_sediment, v_lb_phytoplankton, lf_p_phytoplankton, v_lb_beninv, v_lb_zoo, lf_p_benthic_invertebrates, lf_p_zooplankton, lf_p_filter_feeders, v_lb_ff, v_lb_sf, lf_p_small_fish, s_water, lf_p_medium_fish, v_nb_mf, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_wb_sf, wb_mf, w_t, mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, v_lb_mf, v_wb_mf, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf)
            
        # cb_phytoplankton_v = cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)   
        # cb_zoo_v = cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment)
        # cb_beninv_v = cb_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv)
        # cb_ff_v = cb_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
        # cb_sf_v = cb_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
        # cb_mf_v = cb_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
        # cb_lf_v = cb_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)





        kabam_obj = kabam_model.kabam(
            True,True,'single',chemical_name,l_kow,k_oc,c_wdp,water_column_EEC,c_wto,mineau_scaling_factor,x_poc,x_doc,c_ox,w_t,c_ss,oc,k_ow,
            Species_of_the_tested_bird,bw_quail,bw_duck,bwb_other,avian_ld50,avian_lc50,avian_noaec,m_species,bw_rat,bwm_other,mammalian_ld50,mammalian_lc50,mammalian_chronic_endpoint,
            lf_p_sediment,lf_p_phytoplankton,lf_p_zooplankton,lf_p_benthic_invertebrates,lf_p_filter_feeders,lf_p_small_fish,lf_p_medium_fish,
            mf_p_sediment,mf_p_phytoplankton,mf_p_zooplankton,mf_p_benthic_invertebrates,mf_p_filter_feeders,mf_p_small_fish,
            sf_p_sediment,sf_p_phytoplankton,sf_p_zooplankton,sf_p_benthic_invertebrates,sf_p_filter_feeders,
            ff_p_sediment,ff_p_phytoplankton,ff_p_zooplankton,ff_p_benthic_invertebrates,
            beninv_p_sediment,beninv_p_phytoplankton,beninv_p_zooplankton,
            zoo_p_sediment,zoo_p_phyto,
            s_lipid,s_NLOM,s_water,
            v_lb_phytoplankton,v_nb_phytoplankton,v_wb_phytoplankton,wb_zoo,v_lb_zoo,v_nb_zoo,v_wb_zoo,wb_beninv,v_lb_beninv,v_nb_beninv,v_wb_beninv,wb_ff,v_lb_ff,v_nb_ff,v_wb_ff,wb_sf,v_lb_sf,v_nb_sf,v_wb_sf,wb_mf,v_lb_mf,v_nb_mf,v_wb_mf,wb_lf,v_lb_lf,v_nb_lf,v_wb_lf,
            kg_phytoplankton,kd_phytoplankton,ke_phytoplankton,mo_phytoplankton,mp_phytoplankton,km_phytoplankton,km_zoo,
            k1_phytoplankton,k2_phytoplankton,
            k1_zoo,k2_zoo,kd_zoo,ke_zoo,k1_beninv,k2_beninv,kd_beninv,ke_beninv,km_beninv,
            k1_ff,k2_ff,kd_ff,ke_ff,km_ff,k1_sf,k2_sf,kd_sf,ke_sf,km_sf,k1_mf,k2_mf,kd_mf,ke_mf,km_mf,k1_lf,k2_lf,kd_lf,ke_lf,km_lf,
            rate_constants,s_respire,phyto_respire,zoo_respire,beninv_respire,ff_respire,sfish_respire,mfish_respire,lfish_respire, None
            )

            # cb_phytoplankton_v,cb_zoo_v,cb_beninv_v,cb_ff_v,cb_sf_v,cb_mf_v,cb_lf_v   ***Removed from kabam_obj above***
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "Kabam Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'kabam','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'kabam',
                'model_attributes':'Kabam Output'})
        html = html + kabam_tables.timestamp(kabam_obj,"")
        html = html + kabam_tables.table_all(kabam_obj)
        html = html + kabam_tables.bar_f(kabam_obj)
        html = html + template.render(templatepath + 'kabam_output_jqplot.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, kabam_obj.__dict__, "kabam", "single")
        self.response.out.write(html)
        
app = webapp.WSGIApplication([('/.*', KabamOutputPage)], debug=True)
           
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
