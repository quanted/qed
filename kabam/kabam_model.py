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
import logging
import sys
import math
import time, datetime

logger = logging.getLogger('Kabam Model')

class kabam(object):
    def __init__(self, set_variables=True,run_methods=True, run_type='single',
            chemical_name='',l_kow=1,k_oc=1,c_wdp=1,water_column_EEC=1,c_wto=1,mineau_scaling_factor=1,x_poc=1,x_doc=1,c_ox=1,w_t=1,c_ss=1,oc=1,k_ow=1,
            Species_of_the_tested_bird='',bw_quail=1,bw_duck=1,bwb_other=1,avian_ld50=1,avian_lc50=1,avian_noaec=1,m_species='',bw_rat=1,bwm_other=1,mammalian_ld50=1,mammalian_lc50=1,mammalian_chronic_endpoint=1,
            lf_p_sediment=1,lf_p_phytoplankton=1,lf_p_zooplankton=1,lf_p_benthic_invertebrates=1,lf_p_filter_feeders=1,lf_p_small_fish=1,lf_p_medium_fish=1,
            mf_p_sediment=1,mf_p_phytoplankton=1,mf_p_zooplankton=1,mf_p_benthic_invertebrates=1,mf_p_filter_feeders=1,mf_p_small_fish=1,
            sf_p_sediment=1,sf_p_phytoplankton=1,sf_p_zooplankton=1,sf_p_benthic_invertebrates=1,sf_p_filter_feeders=1,
            ff_p_sediment=1,ff_p_phytoplankton=1,ff_p_zooplankton=1,ff_p_benthic_invertebrates=1,
            beninv_p_sediment=1,beninv_p_phytoplankton=1,beninv_p_zooplankton=1,
            zoo_p_sediment=1,zoo_p_phyto=1,
            s_lipid=1,s_NLOM=1,s_water=1,
            v_lb_phytoplankton=1,v_nb_phytoplankton=1,v_wb_phytoplankton=1,wb_zoo=1,v_lb_zoo=1,v_nb_zoo=1,v_wb_zoo=1,wb_beninv=1,v_lb_beninv=1,v_nb_beninv=1,v_wb_beninv=1,wb_ff=1,v_lb_ff=1,v_nb_ff=1,v_wb_ff=1,wb_sf=1,v_lb_sf=1,v_nb_sf=1,v_wb_sf=1,wb_mf=1,v_lb_mf=1,v_nb_mf=1,v_wb_mf=1,wb_lf=1,v_lb_lf=1,v_nb_lf=1,v_wb_lf=1,
            kg_phytoplankton=1,kd_phytoplankton=1,ke_phytoplankton=1,mo_phytoplankton=1,mp_phytoplankton=1,km_phytoplankton=1,km_zoo=1,
            k1_phytoplankton=1,k2_phytoplankton=1,
            k1_zoo=1,k2_zoo=1,kd_zoo=1,ke_zoo=1,k1_beninv=1,k2_beninv=1,kd_beninv=1,ke_beninv=1,km_beninv=1,
            k1_ff=1,k2_ff=1,kd_ff=1,ke_ff=1,km_ff=1,k1_sf=1,k2_sf=1,kd_sf=1,ke_sf=1,km_sf=1,k1_mf=1,k2_mf=1,kd_mf=1,ke_mf=1,km_mf=1,k1_lf=1,k2_lf=1,kd_lf=1,ke_lf=1,km_lf=1,
            rate_constants='',s_respire='',phyto_respire='',zoo_respire='',beninv_respire='',ff_respire='',sfish_respire='',mfish_respire='',lfish_respire='',
            
            vars_dict=None):

            # cb_phytoplankton_v=1,cb_zoo_v=1,cb_beninv_v=1,cb_ff_v=1,cb_sf_v=1,cb_mf_v=1,cb_lf_v=1,   ***These were removed from __init__***

        # self.set_default_variables()
        ts = datetime.datetime.now()
        if(time.daylight):
            ts1 = datetime.timedelta(hours=-4)+ts
        else:
            ts1 = datetime.timedelta(hours=-5)+ts
        self.jid = ts1.strftime('%Y%m%d%H%M%S%f')
        
        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.run_type = run_type
                self.chemical_name = chemical_name
                self.l_kow=l_kow
                self.k_oc=k_oc
                self.c_wdp=c_wdp
                self.water_column_EEC=water_column_EEC
                self.c_wto=c_wto
                self.mineau_scaling_factor=mineau_scaling_factor
                self.x_poc=x_poc
                self.x_doc=x_doc
                self.c_ox=c_ox
                self.w_t=w_t
                self.c_ss=c_ss
                self.oc=oc
                self.k_ow=k_ow
                self.Species_of_the_tested_bird = Species_of_the_tested_bird
                self.bw_quail = bw_quail
                self.bw_duck = bw_duck
                self.bwb_other = bwb_other
                if Species_of_the_tested_bird =='178':
                    self.bw_bird = self.bw_quail
                elif Species_of_the_tested_bird =='1580':
                    self.bw_bird = self.bw_duck
                else:
                    self.bw_bird = self.bwb_other           
                self.avian_ld50=avian_ld50
                self.avian_lc50=avian_lc50
                self.avian_noaec=avian_noaec
                self.m_species = m_species
                self.bw_rat = bw_rat
                self.bwm_other = bwm_other
                if m_species =='350':
                    self.bw_mamm = self.bw_rat
                else:
                    self.bw_mamm = self.bwm_other
                self.mammalian_ld50=mammalian_ld50
                self.mammalian_lc50=mammalian_lc50
                self.mammalian_chronic_endpoint=mammalian_chronic_endpoint
                self.lf_p_sediment=lf_p_sediment
                self.lf_p_phytoplankton=lf_p_phytoplankton
                self.lf_p_zooplankton=lf_p_zooplankton
                self.lf_p_benthic_invertebrates=lf_p_benthic_invertebrates
                self.lf_p_filter_feeders=lf_p_filter_feeders
                self.lf_p_small_fish=lf_p_small_fish
                self.lf_p_medium_fish=lf_p_medium_fish
                self.mf_p_sediment=mf_p_sediment
                self.mf_p_phytoplankton=mf_p_phytoplankton
                self.mf_p_zooplankton=mf_p_zooplankton
                self.mf_p_benthic_invertebrates=mf_p_benthic_invertebrates
                self.mf_p_filter_feeders=mf_p_filter_feeders
                self.mf_p_small_fish=mf_p_small_fish
                self.sf_p_sediment=sf_p_sediment
                self.sf_p_phytoplankton=sf_p_phytoplankton
                self.sf_p_zooplankton=sf_p_zooplankton
                self.sf_p_benthic_invertebrates=sf_p_benthic_invertebrates
                self.sf_p_filter_feeders=sf_p_filter_feeders
                self.ff_p_sediment=ff_p_sediment
                self.ff_p_phytoplankton=ff_p_phytoplankton
                self.ff_p_zooplankton=ff_p_zooplankton
                self.ff_p_benthic_invertebrates=ff_p_benthic_invertebrates
                self.beninv_p_sediment=beninv_p_sediment
                self.beninv_p_phytoplankton=beninv_p_phytoplankton
                self.beninv_p_zooplankton=beninv_p_zooplankton
                self.zoo_p_sediment=zoo_p_sediment
                self.zoo_p_phyto=zoo_p_phyto
                self.s_lipid=s_lipid
                self.s_NLOM=s_NLOM
                self.s_water=s_water
                self.v_lb_phytoplankton=v_lb_phytoplankton
                self.v_nb_phytoplankton=v_nb_phytoplankton
                self.v_wb_phytoplankton=v_wb_phytoplankton
                self.wb_zoo=wb_zoo
                self.v_lb_zoo=v_lb_zoo
                self.v_nb_zoo=v_nb_zoo
                self.v_wb_zoo=v_wb_zoo
                self.wb_beninv=wb_beninv
                self.v_lb_beninv=v_lb_beninv
                self.v_nb_beninv=v_nb_beninv
                self.v_wb_beninv=v_wb_beninv
                self.wb_ff=wb_ff
                self.v_lb_ff=v_lb_ff
                self.v_nb_ff=v_nb_ff
                self.v_wb_ff=v_wb_ff
                self.wb_sf=wb_sf
                self.v_lb_sf=v_lb_sf
                self.v_nb_sf=v_nb_sf
                self.v_wb_sf=v_wb_sf
                self.wb_mf=wb_mf
                self.v_lb_mf=v_lb_mf
                self.v_nb_mf=v_nb_mf
                self.v_wb_mf=v_wb_mf
                self.wb_lf=wb_lf
                self.v_lb_lf=v_lb_lf
                self.v_nb_lf=v_nb_lf
                self.v_wb_lf=v_wb_lf
                self.kg_phytoplankton=kg_phytoplankton
                self.kd_phytoplankton=kd_phytoplankton
                self.ke_phytoplankton=ke_phytoplankton
                self.mo_phytoplankton=mo_phytoplankton
                self.mp_phytoplankton=mp_phytoplankton
                self.km_phytoplankton=km_phytoplankton
                self.km_zoo=km_zoo
                self.k1_phytoplankton=k1_phytoplankton
                self.k2_phytoplankton=k2_phytoplankton
                self.k1_zoo=k1_zoo
                self.k2_zoo=k2_zoo
                self.kd_zoo=kd_zoo
                self.ke_zoo=ke_zoo
                self.k1_beninv=k1_beninv
                self.k2_beninv=k2_beninv
                self.kd_beninv=kd_beninv
                self.ke_beninv=ke_beninv
                self.km_beninv=km_beninv
                self.k1_ff=k1_ff
                self.k2_ff=k2_ff
                self.kd_ff=kd_ff
                self.ke_ff=ke_ff
                self.km_ff=km_ff
                self.k1_sf=k1_sf
                self.k2_sf=k2_sf
                self.kd_sf=kd_sf
                self.ke_sf=ke_sf
                self.km_sf=km_sf
                self.k1_mf=k1_mf
                self.k2_mf=k2_mf
                self.kd_mf=kd_mf
                self.ke_mf=ke_mf
                self.km_mf=km_mf
                self.k1_lf=k1_lf
                self.k2_lf=k2_lf
                self.kd_lf=kd_lf
                self.ke_lf=ke_lf
                self.km_lf=km_lf
                # self.k_bw_phytoplankton=k_bw_phytoplankton
                # self.k_bw_zoo=k_bw_zoo
                # self.k_bw_beninv=k_bw_beninv
                # self.k_bw_ff=k_bw_ff
                # self.k_bw_sf=k_bw_sf
                # self.k_bw_mf=k_bw_mf
                # self.k_bw_lf=k_bw_lf
                self.rate_constants=rate_constants
                self.s_respire=s_respire
                self.phyto_respire=phyto_respire
                self.zoo_respire=zoo_respire
                self.beninv_respire=beninv_respire
                self.ff_respire=ff_respire
                self.sfish_respire=sfish_respire
                self.mfish_respire=mfish_respire
                self.lfish_respire=lfish_respire
                if rate_constants == 'a':
                    self.k_bw_phytoplankton_f()
                    self.k1_phytoplankton_f()
                    self.k2_phytoplankton_f()
                    self.ew_zoo_f()
                    self.gv_zoo_f()
                    self.k_bw_zoo_f()
                    self.ed_zoo_f()
                    self.gd_zoo_f()
                    self.k1_zoo_f()
                    self.k2_zoo_f()
                    self.kd_zoo_f()
                    self.v_nd_zoo_f()
                    self.v_wd_zoo_f()
                    self.v_ld_zoo_f()
                    self.gf_zoo_f()
                    self.vlg_zoo_f()
                    self.vng_zoo_f()
                    self.vwg_zoo_f()
                    self.kgb_zoo_f()
                    self.ke_zoo_f()

                    self.k_bw_beninv_f()
                    self.ed_beninv_f()
                    self.gd_beninv_f()
                    self.kg_beninv_f()
                    self.v_ld_beninv_f()
                    self.v_nd_beninv_f()
                    self.v_wd_beninv_f()
                    self.gf_beninv_f()
                    self.vlg_beninv_f()
                    self.vng_beninv_f()
                    self.vwg_beninv_f()
                    self.kgb_beninv_f()
                    self.ew_beninv_f()
                    self.gv_beninv_f()
                    self.k1_beninv_f()
                    self.k2_beninv_f()
                    self.kd_beninv_f()
                    self.ke_beninv_f()

                    self.gv_ff_f()
                    self.ew_ff_f()
                    self.k_bw_ff_f()
                    self.ed_ff_f()
                    self.gd_ff_f()
                    self.kg_ff_f()
                    self.v_ld_ff_f()
                    self.v_nd_ff_f()
                    self.v_wd_ff_f()
                    self.gf_ff_f()
                    self.vlg_ff_f()
                    self.vng_ff_f()
                    self.vwg_ff_f()
                    self.kgb_ff_f()
                    self.k1_ff_f()
                    self.k2_ff_f()
                    self.kd_ff_f()
                    self.ke_ff_f()

                    self.gv_sf_f()
                    self.ew_sf_f()
                    self.k_bw_sf_f()
                    self.ed_sf_f()
                    self.gd_sf_f()
                    self.kg_sf_f()
                    self.v_ld_sf_f()
                    self.v_nd_sf_f()
                    self.v_wd_sf_f()
                    self.gf_sf_f()
                    self.vlg_sf_f()
                    self.vng_sf_f()
                    self.vwg_sf_f()
                    self.kgb_sf_f()
                    self.k1_sf_f()
                    self.k2_sf_f()
                    self.kd_sf_f()
                    self.ke_sf_f()

                    self.gv_mf_f()
                    self.ew_mf_f()
                    self.k_bw_mf_f()
                    self.ed_mf_f()
                    self.gd_mf_f()
                    self.kg_mf_f()
                    self.v_ld_mf_f()
                    self.v_nd_mf_f()
                    self.v_wd_mf_f()
                    self.gf_mf_f()
                    self.vlg_mf_f()
                    self.vng_mf_f()
                    self.vwg_mf_f()
                    self.kgb_mf_f()
                    self.k1_mf_f()
                    self.k2_mf_f()
                    self.kd_mf_f()
                    self.ke_mf_f()
                    
                    self.gv_lf_f()
                    self.ew_lf_f()
                    self.k_bw_lf_f()
                    self.ed_lf_f()
                    self.gd_lf_f()
                    self.kg_lf_f()
                    self.v_ld_lf_f()
                    self.v_nd_lf_f()
                    self.v_wd_lf_f()
                    self.gf_lf_f()
                    self.vlg_lf_f()
                    self.vng_lf_f()
                    self.vwg_lf_f()
                    self.kgb_lf_f()
                    self.k1_lf_f()
                    self.k2_lf_f()
                    self.kd_lf_f()
                    self.ke_lf_f()

                else:
                    self.k1_phytoplankton = k1_phytoplankton
                    self.k2_phytoplankton = k2_phytoplankton
                    self.kd_phytoplankton = kd_phytoplankton
                    self.ke_phytoplankton = ke_phytoplankton
                    self.km_phytoplankton = km_phytoplankton
                    self.k1_zoo = k1_zoo
                    self.k2_zoo = k2_zoo
                    self.kd_zoo = kd_zoo
                    self.ke_zoo = ke_zoo
                    self.km_zoo = km_zoo
                    self.k1_beninv = k1_beninv
                    self.k2_beninv = k2_beninv
                    self.kd_beninv = kd_beninv
                    self.ke_beninv = ke_beninv
                    self.km_beninv = km_beninv
                    self.k1_ff = k1_ff
                    self.k2_ff = k2_ff
                    self.kd_ff = kd_ff
                    self.ke_ff = ke_ff
                    self.km_ff = km_ff
                    self.k1_sf = k1_sf
                    self.k2_sf = k2_sf
                    self.kd_sf = kd_sf
                    self.ke_sf = ke_sf
                    self.km_sf = km_sf
                    self.k1_mf = k1_mf
                    self.k2_mf = k2_mf
                    self.kd_mf = kd_mf
                    self.ke_mf = ke_mf
                    self.km_mf = km_mf
                    self.k1_lf = k1_lf
                    self.k2_lf = k2_lf
                    self.kd_lf = kd_lf
                    self.ke_lf = ke_lf
                    self.km_lf = km_lf
 
                logger.info(vars(self))
            if run_methods:
                self.run_methods()


    # def set_default_variables(self):
    #     self.

    # def set_unit_testing_variables(self):
    #     self.



    def run_methods(self):
        self.phi_f()
        self.c_soc_f()
        self.c_s_f()
        self.sed_om_f()
        self.water_d()
        # self.k_bw_phytoplankton_f()
        # self.k1_phytoplankton_f()
        # self.k2_phytoplankton_f()
        self.cb_phytoplankton_f()
        self.cbl_phytoplankton_f()
        self.cbf_phytoplankton_f()
        self.cbr_phytoplankton_f()
        self.cbfl_phytoplankton_f()
        self.cbaf_phytoplankton_f()
        self.cbafl_phytoplankton_f()
        self.cbsafl_phytoplankton_f()
        # self.gv_zoo_f()
        # self.ew_zoo_f()
        # self.k1_zoo_f()
        # self.k_bw_zoo_f()
        # self.k2_zoo_f()
        # self.ed_zoo_f()
        # self.gd_zoo_f()
        # self.kd_zoo_f()
        self.kg_zoo_f()
        # self.v_ld_zoo_f()
        # self.v_nd_zoo_f()
        # self.v_wd_zoo_f()
        # self.gf_zoo_f()
        # self.vlg_zoo_f()
        # self.vng_zoo_f()
        # self.vwg_zoo_f()
        # self.kgb_zoo_f()
        # self.ke_zoo_f()
        self.diet_zoo_f()
        self.cb_zoo_f()
        self.cbl_zoo_f()
        self.cbd_zoo_f()
        self.cbr_zoo_f()
        self.cbf_zoo_f()
        self.cbfl_zoo_f()
        self.cbaf_zoo_f()
        self.cbafl_zoo_f()
        self.cbsafl_zoo_f()
        self.bmf_zoo_f()
        # self.gv_beninv_f()
        # self.ew_beninv_f()
        # self.k1_beninv_f()
        # self.k_bw_beninv_f()
        # # self.k2_beninv_f()
        # self.ed_beninv_f()
        # self.gd_beninv_f()
        # # self.kd_beninv_f()
        self.kg_beninv_f()
        # self.v_ld_beninv_f()
        # self.v_nd_beninv_f()
        # self.v_wd_beninv_f()
        # self.gf_beninv_f()
        # self.vlg_beninv_f()
        # self.vng_beninv_f()
        # self.vwg_beninv_f()
        # self.kgb_beninv_f()
        # self.ke_beninv_f()
        self.diet_beninv_f()
        self.cb_beninv_f()
        self.cbl_beninv_f()
        self.cbd_beninv_f()
        self.cbr_beninv_f()
        self.cbf_beninv_f()
        self.cbfl_beninv_f()
        self.cbaf_beninv_f()
        self.cbafl_beninv_f()
        self.cbsafl_beninv_f()
        self.bmf_beninv_f()
        # self.gv_ff_f()
        # self.ew_ff_f()
        # # self.k1_ff_f()
        # self.k_bw_ff_f()
        # # self.k2_ff_f()
        # self.ed_ff_f()
        # self.gd_ff_f()
        # # self.kd_ff_f()
        self.kg_ff_f()
        # self.v_ld_ff_f()
        # self.v_nd_ff_f()
        # self.v_wd_ff_f()
        # self.gf_ff_f()
        # self.vlg_ff_f()
        # self.vng_ff_f()
        # self.vwg_ff_f()
        # self.kgb_ff_f()
        # self.ke_ff_f()
        self.diet_ff_f()
        self.cb_ff_f()
        self.cbl_ff_f()
        self.cbd_ff_f()
        self.cbr_ff_f()
        self.cbf_ff_f()
        self.cbfl_ff_f()
        self.cbaf_ff_f()
        self.cbafl_ff_f()
        self.cbsafl_ff_f()
        self.bmf_ff_f()
        # self.gv_sf_f()
        # self.ew_sf_f()
        # # self.k1_sf_f()
        # self.k_bw_sf_f()
        # # self.k2_sf_f()
        # self.ed_sf_f()
        # self.gd_sf_f()
        # # self.kd_sf_f()
        self.kg_sf_f()
        # self.v_ld_sf_f()
        # self.v_nd_sf_f()
        # self.v_wd_sf_f()
        # self.gf_sf_f()
        # self.vlg_sf_f()
        # self.vng_sf_f()
        # self.vwg_sf_f()
        # self.kgb_sf_f()
        # self.ke_sf_f()
        self.diet_sf_f()
        self.cb_sf_f()
        self.cbl_sf_f()
        self.cbd_sf_f()
        self.cbr_sf_f()
        self.cbf_sf_f()
        self.cbfl_sf_f()
        self.cbaf_sf_f()
        self.cbafl_sf_f()
        self.cbsafl_sf_f()
        self.bmf_sf_f()
        # self.gv_mf_f()
        # self.ew_mf_f()
        # # self.k1_mf_f()
        # self.k_bw_mf_f()
        # # self.k2_mf_f()
        # self.ed_mf_f()
        # self.gd_mf_f()
        # # self.kd_mf_f()
        self.kg_mf_f()
        # self.v_ld_mf_f()
        # self.v_nd_mf_f()
        # self.v_wd_mf_f()
        # self.gf_mf_f()
        # self.vlg_mf_f()
        # self.vng_mf_f()
        # self.vwg_mf_f()
        # self.kgb_mf_f()
        # self.ke_mf_f()
        self.diet_mf_f()
        self.cb_mf_f()
        self.cbl_mf_f()
        self.cbd_mf_f()
        self.cbr_mf_f()
        self.cbf_mf_f()
        self.cbfl_mf_f()
        self.cbaf_mf_f()
        self.cbafl_mf_f()
        self.cbsafl_mf_f()
        self.cbmf_mf_f()
        # self.gv_lf_f()
        # self.ew_lf_f()
        # # self.k1_lf_f()
        # self.k_bw_lf_f()
        # # self.k2_lf_f()
        # self.ed_lf_f()
        # self.gd_lf_f()
        # # self.kd_lf_f()
        self.kg_lf_f()
        # self.v_ld_lf_f()
        # self.v_nd_lf_f()
        # self.v_wd_lf_f()
        # self.gf_lf_f()
        # self.vlg_lf_f()
        # self.vng_lf_f()
        # self.vwg_lf_f()
        # self.kgb_lf_f()
        # self.ke_lf_f()
        self.diet_lf_f()
        self.cb_lf_f()
        self.cbl_lf_f()
        self.cbd_lf_f()
        self.cbr_lf_f()
        self.cbf_lf_f()
        self.cbfl_lf_f()
        self.cbaf_lf_f()
        self.cbafl_lf_f()
        self.cbsafl_lf_f()
        self.cbmf_lf_f()
        self.mweight_f()
        self.dfir_f()
        self.wet_food_ingestion_m_f()
        self.drinking_water_intake_m_f()
        self.db4_f()
        self.db5_f()
        self.aweight_f()
        self.dfir_a_f()
        self.wet_food_ingestion_a_f()
        self.drinking_water_intake_a_f()
        self.db4a_f()
        self.db5a_f()
        self.acute_dose_based_m_f()
        self.chronic_dose_based_m_f()
        self.acute_dose_based_a_f()
        self.acute_rq_dose_m_f()
        self.chronic_rq_dose_m_f()
        self.acute_rq_diet_m_f()
        self.chronic_rq_diet_m_f()
        self.acute_rq_dose_a_f()
        self.acute_rq_diet_a_f()
        self.chronic_rq_diet_a_f()

    # calculate Fraction of freely dissolved in water column
    def phi_f(self):
        self.phi =  1 / (1 + (self.x_poc*0.35*self.k_ow) + (self.x_doc*0.08*self.k_ow))
        return self.phi
    #normalized pesticide concentration in sediment    
    def c_soc_f(self):
        self.c_soc = self.k_oc * self.c_wdp
        return self.c_soc
    #calculate concentration of chemical in sediment    
    def c_s_f(self):
        self.c_s = self.c_soc * self.oc
        return self.c_s
    def sed_om_f(self):
        self.sed_om = self.c_s / self.oc
        return self.sed_om
    # water freely dissolved
    def water_d(self):
        self.water_d = self.phi * self.c_wto * 1000000   
        return self.water_d
        
    #determine input for rate constants user input or calculated

    # calculate values
    #############phytoplankton
    # phytoplankton water partition coefficient  
    def k_bw_phytoplankton_f(self):
        self.k_bw_phytoplankton = (self.v_lb_phytoplankton*self.k_ow)+(self.v_nb_phytoplankton*0.35*self.k_ow)+self.v_wb_phytoplankton
        return self.k_bw_phytoplankton
    # rate constant for uptake through respiratory area

    def k1_phytoplankton_f(self):
        self.k1_phytoplankton = 1/(6.0e-5+(5.5/self.k_ow))
        return self.k1_phytoplankton
        
    #rate constant for elimination through the gills for phytoplankton  
    def k2_phytoplankton_f(self):   
        self.k2_phytoplankton = self.k1_phytoplankton/self.k_bw_phytoplankton
        return self.k2_phytoplankton
    # phytoplankton pesticide tissue residue
    def cb_phytoplankton_f(self):   
        self.cb_phytoplankton = (self.k1_phytoplankton * (self.mo_phytoplankton * self.c_wto * self.phi + self.mp_phytoplankton * self.c_wdp)) / (self.k2_phytoplankton + self.ke_phytoplankton + self.kg_phytoplankton + self.km_phytoplankton)
        return self.cb_phytoplankton

    # lipid normalized pesticide residue in phytoplankton    
    def cbl_phytoplankton_f(self):
        self.cbl_phytoplankton = (1e6*self.cb_phytoplankton) / self.v_lb_phytoplankton
        return self.cbl_phytoplankton
    # phytoplankton total bioconcentration factor
    def cbf_phytoplankton_f(self):   
        # kd_phytoplankton = 0 #kd_phytoplankton is always = 0
        self.ke_phytoplankton = 0
        self.km_phytoplankton = 0
        self.kg_phytoplankton = 0
        self.cbf_phytoplankton = ((self.k1_phytoplankton * (self.mo_phytoplankton * self.c_wto * self.phi + self.mp_phytoplankton * self.c_wdp)) / (self.k2_phytoplankton + self.ke_phytoplankton + self.kg_phytoplankton + self.km_phytoplankton)) / self.c_wto
        return self.cbf_phytoplankton
    def cbr_phytoplankton_f(self):   
        # kd_phytoplankton = 0 #kd_phytoplankton is always = 0
        self.ke_phytoplankton = 0
        self.km_phytoplankton = 0
        self.cbr_phytoplankton = ((self.k1_phytoplankton * (self.mo_phytoplankton * self.c_wto * self.phi + self.mp_phytoplankton * self.c_wdp)) / (self.k2_phytoplankton + self.ke_phytoplankton + self.kg_phytoplankton + self.km_phytoplankton))
        return self.cbr_phytoplankton
    #phytoplankton lipid normalized total bioconcentration factor
    def cbfl_phytoplankton_f(self):   
        # kd_phytoplankton = 0 #kd_phytoplankton is always = 0
        self.ke_phytoplankton = 0
        self.km_phytoplankton = 0
        self.kg_phytoplankton = 0
        self.cbfl_phytoplankton = ((self.k1_phytoplankton * (self.mo_phytoplankton * self.c_wto * self.phi + self.mp_phytoplankton * self.c_wdp) / (self.k2_phytoplankton + self.ke_phytoplankton + self.kg_phytoplankton + self.km_phytoplankton))/ self.v_lb_phytoplankton) / (self.c_wto * self.phi)
        return self.cbfl_phytoplankton
    #phytoplankton bioaccumulation factor
    def cbaf_phytoplankton_f(self):   
        self.cbaf_phytoplankton = (1e6 * self.cb_phytoplankton) / self.water_column_EEC
        return self.cbaf_phytoplankton
    # phytoplankton lipid normalized bioaccumulation factor
    def cbafl_phytoplankton_f(self):   
        self.cbafl_phytoplankton = self.cbl_phytoplankton / self.water_d
        return self.cbafl_phytoplankton
    # phytoplankton  biota-sediment accumulation factor
    def cbsafl_phytoplankton_f(self):   
        self.cbsafl_phytoplankton = (self.cb_phytoplankton / self.v_lb_phytoplankton) / self.sed_om
        return self.cbsafl_phytoplankton   
        
    ##################zooplankton
    # ventilation rate     
    def gv_zoo_f(self):  
        self.gv_zoo = (1400 * (self.wb_zoo**0.65))/self.c_ox
        return self.gv_zoo

    # rate constant for elimination through the gills for zooplankton
    def ew_zoo_f(self):
        self.ew_zoo = (1/(1.85+(155/self.k_ow)))           
        return self.ew_zoo

    #uptake rate constant through respiratory area for phytoplankton   
    def k1_zoo_f(self):
        self.k1_zoo = self.ew_zoo * self.gv_zoo / self.wb_zoo
        return self.k1_zoo
    # zooplankton water partition coefficient
    def k_bw_zoo_f(self):
        self.k_bw_zoo = (self.v_lb_zoo * self.k_ow) + (self.v_nb_zoo * 0.035 * self.k_ow) + self.v_wb_zoo
        return self.k_bw_zoo    
    # elimination rate constant through the gills for zooplankton    
    def k2_zoo_f(self):
        self.k2_zoo = self.k1_zoo / self.k_bw_zoo
        return self.k2_zoo
    # zoo plankton dietary pesticide transfer efficiency
    def ed_zoo_f(self):
        self.ed_zoo = 1 / ((.0000003) * self.k_ow + 2.0)
        return self.ed_zoo
    # zooplankton feeding rate

    def gd_zoo_f(self):
        self.gd_zoo = 0.022 * self.wb_zoo**0.85 * math.exp(0.06*self.w_t)
        return self.gd_zoo
    # zooplankton rate constant pesticide uptake by food ingestion
    def kd_zoo_f(self):
        self.kd_zoo = self.ed_zoo * (self.gd_zoo / self.wb_zoo)    
        return self.kd_zoo

    # zooplankton growth rate constant
    def kg_zoo_f(self):
        if self.w_t < 17.5:
            self.kg_zoo = 0.0005 * self.wb_zoo **-0.2
        else:
            self.kg_zoo = 0.00251 * self.wb_zoo **-0.2
        return self.kg_zoo
    #overall lipid content of diet
    def v_ld_zoo_f(self):
        self.v_ld_zoo = self.zoo_p_sediment * self.s_lipid + self.zoo_p_phyto * self.v_lb_phytoplankton
        return self.v_ld_zoo
    # overall nonlipid content of diet
    def v_nd_zoo_f(self):
        self.v_nd_zoo = self.zoo_p_sediment * self.s_NLOM + self.zoo_p_phyto * self.v_nb_phytoplankton
        return self.v_nd_zoo
    # overall water content of diet 
    def v_wd_zoo_f(self):
        self.v_wd_zoo = self.zoo_p_sediment * self.s_water + self.zoo_p_phyto * self.v_wb_phytoplankton
        return self.v_wd_zoo
    # egestion rate of fecal matter   
    def gf_zoo_f(self):
        self.gf_zoo = (((1-.72)*self.v_ld_zoo)+((1-.72)*self.v_nd_zoo)+((1-.25)*self.v_wd_zoo))*self.gd_zoo
        #rr=self.zoo_p_phyto
        #if rr==0:
         #   rr==0.00000001
        #return rr
        return self.gf_zoo

    #lipid content in gut 
    def vlg_zoo_f(self):
        self.vlg_zoo = (1-0.72) * self.v_ld_zoo * self.gd_zoo / self.gf_zoo
        return self.vlg_zoo
    # non lipid content in gut    
    def vng_zoo_f(self):
        self.vng_zoo = (1 - 0.72) * self.v_nd_zoo * self.gd_zoo / self.gf_zoo
        return self.vng_zoo
    # water content in the gut
    def vwg_zoo_f(self):
        self.vwg_zoo = (1 - 0.25) * self.v_wd_zoo * self.gd_zoo / self.gf_zoo
        return self.vwg_zoo    
    # partition coefficient of the pesticide between the gastrointenstinal track and the organism
    def kgb_zoo_f(self):
        self.kgb_zoo = (self.vlg_zoo * self.k_ow + self.vng_zoo * 0.035 * self.k_ow + self.vwg_zoo) / (self.v_lb_zoo * self.k_ow + self.v_nb_zoo * 0.035 * self.k_ow + self.v_wb_zoo) 
        return self.kgb_zoo
    # dietary elimination rate constant    
    def ke_zoo_f(self):
        self.ke_zoo = self.gf_zoo * self.ed_zoo * self.kgb_zoo / self.wb_zoo
     #   self.ke_zoo = self.zoo_p_phyto
        return self.ke_zoo

    def diet_zoo_f(self):     
        self.diet_zoo = self.c_s * self.zoo_p_sediment + self.cb_phytoplankton * self.zoo_p_phyto
        return self.diet_zoo
        
    # zooplankton pesticide tissue residue
    def cb_zoo_f(self):
        self.cb_zoo = (self.k1_zoo * (1.0 * self.phi * self.c_wto + 0 * self.c_wdp) + self.kd_zoo * self.diet_zoo) / (self.k2_zoo + self.ke_zoo + self.kg_zoo + 0)
        # print "cb_zoo =", self.cb_zoo
        return self.cb_zoo
    # zooplankton pesticide tissue residue lipid normalized
    def cbl_zoo_f(self):
        self.cbl_zoo = (1e6*self.cb_zoo) / self.v_lb_zoo
        return self.cbl_zoo
    # zooplankton pesticide concentration originating from uptake through diet k1=0    
    def cbd_zoo_f(self):  
        self.cbd_zoo = (0 * (1.0) * self.phi * self.c_wto + (0 * self.c_wdp) + (self.kd_zoo * (self.diet_zoo))) / (self.k2_zoo + self.ke_zoo + self.kg_zoo + 0)
        # print "cbd_zoo =", self.cbd_zoo
        return self.cbd_zoo
    # zooplankton pesticide concentration originating from uptake through respiration (kd=0)
    def cbr_zoo_f(self):
        self.cbr_zoo = (self.k1_zoo * (1. * self.phi * self.c_wto + 0 * self.c_wdp) + (0 * self.diet_zoo)) / (self.k2_zoo + self.ke_zoo + self.kg_zoo + 0)
        return self.cbr_zoo
    # zooplankton total bioconcentration factor
    def cbf_zoo_f(self):
        self.kd_zoo = 0
        self.ke_zoo = 0
    #    km_zoo = 0 km_zoo is always = 0
        self.kg_zoo = 0
        self.cbf_zoo = ((self.k1_zoo * (1. * self.phi * self.c_wto + 0 * self.c_wdp) + self.kd_zoo * self.diet_zoo) / (self.k2_zoo + self.ke_zoo + self.kg_zoo + 0)) / self.c_wto   
        return self.cbf_zoo
    #zooplankton lipid normalized total bioconcentration factor
    def cbfl_zoo_f(self): 
        self.kd_zoo = 0
        self.ke_zoo = 0
    #    km_zoo = 0 km_zoo is always = 0
        self.kg_zoo = 0
        self.cbfl_zoo = ((self.k1_zoo * (1.0 * self.phi * self.c_wto + 0 * self.c_wdp) + self.kd_zoo * self.diet_zoo) / (self.k2_zoo + self.ke_zoo + self.kg_zoo + 0))/ self.v_lb_zoo / (self.c_wto * self.phi)  
        return self.cbfl_zoo    
    # zooplankton bioaccumulation factor
    def cbaf_zoo_f(self):
        self.cbaf_zoo = (1e6 * self.cb_zoo) / self.water_column_EEC
        return self.cbaf_zoo
    # zooplankton lipid normalized bioaccumulation factor
    def cbafl_zoo_f(self):
        self.cbafl_zoo = self.cbl_zoo / self.water_d
        return self.cbafl_zoo
        
    def cbsafl_zoo_f(self):
        self.cbsafl_zoo = (self.cb_zoo / self.v_lb_zoo) / self.sed_om
        return self.cbsafl_zoo    
    # zooplankton biomagnification factor
    def bmf_zoo_f(self):
        # try:
        #     self.cb_zoo_v=float(self.cb_zoo_v)
        #     self.v_lb_zoo=float(self.v_lb_zoo)
        #     self.zoo_p_phyto=float(self.zoo_p_phyto)
        #     self.cb_phytoplankton_v=float(self.cb_phytoplankton_v)
        #     self.v_lb_phytoplankton=float(self.v_lb_phytoplankton)
        # except ZeroDivisionError:
        #     raise ZeroDivisionError\
        #     ('Dividing by zero.')
        self.bmf_zoo = (self.cb_zoo / self.v_lb_zoo) / (self.zoo_p_phyto * self.cb_phytoplankton / self.v_lb_phytoplankton)
        return self.bmf_zoo
    ################################ benthic invertebrates
    ############################################################
    ## ventilation rate     
    def gv_beninv_f(self):  
        self.gv_beninv = (1400 * ((self.wb_beninv**0.65)/self.c_ox))
        return self.gv_beninv

    # rate constant for elimination through the gills for benthic invertebrates
    def ew_beninv_f(self):
        self.ew_beninv = (1/(1.85+(155/self.k_ow)))           
        return self.ew_beninv

    #uptake rate constant through respiratory area for benthic invertebrates   
    def k1_beninv_f(self):
        self.k1_beninv = ((self.ew_beninv * self.gv_beninv) / self.wb_beninv)   
        return self.k1_beninv
    # benthic invertebrate water partition coefficient
    def k_bw_beninv_f(self):
        self.k_bw_beninv = (self.v_lb_beninv * self.k_ow) + (self.v_nb_beninv * 0.035 * self.k_ow) + self.v_wb_beninv
        return self.k_bw_beninv    
    # elimination rate constant through the gills for zooplankton    
    def k2_beninv_f(self):
        self.k2_beninv = self.k1_beninv / self.k_bw_beninv
        return self.k2_beninv

    # zoo plankton dietary pesticide transfer efficiency
    def ed_beninv_f(self):
        self.ed_beninv = 1 / (.0000003 * self.k_ow + 2.0)
        return self.ed_beninv
    # zooplankton feeding rate

    def gd_beninv_f(self):
        self.gd_beninv = 0.022 * self.wb_beninv**0.85 * math.exp(0.06*self.w_t)
        return self.gd_beninv
    # zooplankton rate constant pesticide uptake by food ingestion
    def kd_beninv_f(self):
        self.kd_beninv = self.ed_beninv * (self.gd_beninv / self.wb_beninv)    
        return self.kd_beninv

    # benthic invertebrate growth rate constant
    def kg_beninv_f(self):
        if self.w_t < 17.5:
            self.kg_beninv = 0.0005 * self.wb_beninv **-0.2
        else:
            self.kg_beninv = 0.00251 * self.wb_beninv **-0.2
        return self.kg_beninv
        
    #overall lipid content of diet
    def v_ld_beninv_f(self):
        self.v_ld_beninv = self.beninv_p_sediment * self.s_lipid + self.beninv_p_phytoplankton * self.v_lb_phytoplankton + self.beninv_p_zooplankton * self.v_lb_zoo
        return self.v_ld_beninv
    # overall nonlipid content of diet
    def v_nd_beninv_f(self):
        self.v_nd_beninv = self.beninv_p_sediment * self.s_NLOM + self.beninv_p_phytoplankton * self.v_nb_phytoplankton + self.beninv_p_zooplankton * self.v_nb_zoo
        return self.v_nd_beninv
    # overall water content of diet 
    def v_wd_beninv_f(self):
        self.v_wd_beninv = self.beninv_p_sediment * self.s_water + self.beninv_p_phytoplankton * self.v_wb_phytoplankton + self.beninv_p_zooplankton * self.v_wb_zoo
        return self.v_wd_beninv
    # egestion rate of fecal matter   
    def gf_beninv_f(self):
        self.gf_beninv = ((1-0.75)*self.v_ld_beninv+(1-0.75)*self.v_nd_beninv+(1-0.25)*self.v_wd_beninv)*self.gd_beninv
        return self.gf_beninv

    #lipid content in gut 
    def vlg_beninv_f(self):
        self.vlg_beninv = (1-0.75) * self.v_ld_beninv * self.gd_beninv / self.gf_beninv
        return self.vlg_beninv
    # non lipid content in gut    
    def vng_beninv_f(self):
        self.vng_beninv = (1 - 0.75) * self.v_nd_beninv * self.gd_beninv / self.gf_beninv
        return self.vng_beninv
    # water content in the gut
    def vwg_beninv_f(self):
        self.vwg_beninv = (1 - 0.25) * self.v_wd_beninv * self.gd_beninv / self.gf_beninv
        return self.vwg_beninv    
    # partition coefficient of the pesticide between the gastrointenstinal track and the organism
    def kgb_beninv_f(self):
        self.kgb_beninv = (self.vlg_beninv * self.k_ow + self.vng_beninv * 0.035 * self.k_ow + self.vwg_beninv) / (self.v_lb_beninv * self.k_ow + self.v_nb_beninv * 0.035 * self.k_ow + self.v_wb_beninv) 
        return self.kgb_beninv    
     
    # dietary elimination rate constant    
    def ke_beninv_f(self):
        self.ke_beninv = self.gf_beninv * self.ed_beninv * (self.kgb_beninv / self.wb_beninv)
        return self.ke_beninv
        
    def diet_beninv_f(self):
        self.diet_beninv = self.c_s * self.beninv_p_sediment + self.cb_phytoplankton * self.beninv_p_phytoplankton + self.cb_zoo * self.beninv_p_zooplankton
        return self.diet_beninv 

    # benthic invertebrates pesticide tissue residue
    def cb_beninv_f(self):
        self.cb_beninv = (self.k1_beninv * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_beninv * self.diet_beninv) / (self.k2_beninv + self.ke_beninv + self.kg_beninv + 0)
        return self.cb_beninv

    def cbl_beninv_f(self):
        self.cbl_beninv = (1e6*self.cb_beninv) / self.v_lb_beninv
        return self.cbl_beninv
    # benthic invertebrates pesticide concentration originating from uptake through diet k1=0
    def cbd_beninv_f(self):
        self.cbd_beninv = (0 * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_beninv * self.diet_beninv) / (self.k2_beninv + self.ke_beninv + self.kg_beninv + 0)
        return self.cbd_beninv
    # benthic invertebrates pesticide concentration originating from uptake through respiration (kd=0)    
    def cbr_beninv_f(self):
        self.cbr_beninv = (self.k1_beninv * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + 0 * self.diet_beninv) / (self.k2_beninv + self.ke_beninv + self.kg_beninv + 0)
        return self.cbr_beninv
    #benthic invertebrate total bioconcentration factor
    def cbf_beninv_f(self):
        self.kd_beninv = 0
        self.ke_beninv = 0
       # km_beninv = 0    is always 0
        self.kg_beninv = 0
        self.cbf_beninv = ((self.k1_beninv * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_beninv * self.diet_beninv) / (self.k2_beninv + self.ke_beninv + self.kg_beninv + 0)) / self.c_wto
        return self.cbf_beninv
    #benthic invertebrate lipid normalized total bioconcentration factor
    def cbfl_beninv_f(self):
        self.kd_beninv = 0
        self.ke_beninv = 0
       # km_beninv = 0    is always 0
        self.kg_beninv = 0
        self.cbfl_beninv = (((self.k1_beninv * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_beninv * self.diet_beninv))/ self.v_lb_beninv / (self.k2_beninv + self.ke_beninv + self.kg_beninv + 0)) / (self.c_wto * self.phi)
        return self.cbfl_beninv    
    # benthic invertebrates bioaccumulation factor
    def cbaf_beninv_f(self):
        self.cbaf_beninv = (1e6 * self.cb_beninv) / self.water_column_EEC
        return self.cbaf_beninv
    # benthic invertebrate lipid normalized bioaccumulation factor
    def cbafl_beninv_f(self):
        self.cbafl_beninv = self.cbl_beninv / self.water_d
        return self.cbafl_beninv

    def cbsafl_beninv_f(self):
        self.cbsafl_beninv = (self.cb_beninv / self.v_lb_beninv) / self.sed_om
        return self.cbsafl_beninv
    # benthic invertebrates biomagnification factor
    def bmf_beninv_f(self):
        self.bmf_beninv = (self.cb_beninv / self.v_lb_beninv) / ((self.beninv_p_zooplankton * self.cb_zoo / self.v_lb_zoo) + (self.beninv_p_phytoplankton * self.cb_phytoplankton / self.v_lb_phytoplankton))
        return self.bmf_beninv    
    
#####################################################
    ###### filter feeders
    ################################################
    ## ventilation rate     
    def gv_ff_f(self):  
        self.gv_ff = (1400.0 * ((self.wb_ff**0.65)/self.c_ox))
        return self.gv_ff

    # rate constant for elimination through the gills for filter feeders
    def ew_ff_f(self):
        self.ew_ff = (1.0/(1.85+(155.0/self.k_ow)))           
        return self.ew_ff

    #uptake rate constant through respiratory area for filter feeders   
    def k1_ff_f(self):
        self.k1_ff = ((self.ew_ff * self.gv_ff) / self.wb_ff)   
        return self.k1_ff
    # filter feeder water partition coefficient
    def k_bw_ff_f(self):
        self.k_bw_ff = (self.v_lb_ff * self.k_ow) + (self.v_nb_ff * 0.035 * self.k_ow) + self.v_wb_ff
        return self.k_bw_ff
    # elimination rate constant through the gills for filter feeders    
    def k2_ff_f(self):
        self.k2_ff = self.k1_ff / self.k_bw_ff
        return self.k2_ff

    # filter feeder dietary pesticide transfer efficiency
    def ed_ff_f(self):
        self.ed_ff = 1 / (.0000003 * self.k_ow + 2.0)
        return self.ed_ff
    # filter feeder feeding rate
    def gd_ff_f(self):
        self.gd_ff = self.gv_ff * self.c_ss * 1
        return self.gd_ff
    # filter feeder rate constant pesticide uptake by food ingestion
    def kd_ff_f(self):
        self.kd_ff = self.ed_ff * (self.gd_ff / self.wb_ff)    
        return self.kd_ff

    # filter feeder growth rate constant
    def kg_ff_f(self):
        if self.w_t < 17.5:
            self.kg_ff = 0.0005 * self.wb_ff **-0.2
        else:
            self.kg_ff = 0.00251 * self.wb_ff **-0.2
        return self.kg_ff
        
    #overall lipid content of diet
    def v_ld_ff_f(self):
        self.v_ld_ff = self.ff_p_sediment * self.s_lipid + self.ff_p_phytoplankton * self.v_lb_phytoplankton + self.ff_p_zooplankton * self.v_lb_zoo
        return self.v_ld_ff
    # overall nonlipid content of diet
    def v_nd_ff_f(self):
        self.v_nd_ff = self.ff_p_sediment * self.s_NLOM + self.ff_p_phytoplankton * self.v_nb_phytoplankton + self.ff_p_zooplankton * self.v_nb_zoo
        return self.v_nd_ff
    # overall water content of diet 
    def v_wd_ff_f(self):
        self.v_wd_ff = self.ff_p_sediment * self.s_water + self.ff_p_phytoplankton * self.v_wb_phytoplankton + self.ff_p_zooplankton * self.v_wb_zoo
        return self.v_wd_ff    
    def gf_ff_f(self):
        self.gf_ff = ((1-0.75)*self.v_ld_ff+(1-0.75)*self.v_nd_ff+(1-0.25)*self.v_wd_ff)*self.gd_ff
        return self.gf_ff
    #lipid content in gut 
    def vlg_ff_f(self):
        self.vlg_ff = (1-0.75) * self.v_ld_ff * self.gd_ff / self.gf_ff
        return self.vlg_ff
    # non lipid content in gut    
    def vng_ff_f(self):
        self.vng_ff = (1 - 0.75) * self.v_nd_ff * self.gd_ff / self.gf_ff
        return self.vng_ff
    # water content in the gut
    def vwg_ff_f(self):
        self.vwg_ff = (1 - 0.25) * self.v_wd_ff * self.gd_ff / self.gf_ff
        return self.vwg_ff    

    def kgb_ff_f(self):
        self.kgb_ff = (self.vlg_ff * self.k_ow + self.vng_ff * 0.035 * self.k_ow + self.vwg_ff) / (self.v_lb_ff * self.k_ow + self.v_nb_ff * 0.035 * self.k_ow + self.v_wb_ff) 
        return self.kgb_ff 
     
    def ke_ff_f(self):
        self.ke_ff = (self.gf_ff * self.ed_ff * self.kgb_ff) / self.wb_ff
        return self.ke_ff
     
    def diet_ff_f(self):  
        self.diet_ff = self.c_s * self.ff_p_sediment + self.cb_phytoplankton * self.ff_p_phytoplankton + self.cb_zoo * self.ff_p_zooplankton + self.cb_beninv * self.ff_p_benthic_invertebrates
        return self.diet_ff 
    # benthic invertebrates pesticide tissue residue
    def cb_ff_f(self):
        self.cb_ff = (self.k1_ff * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_ff * self.diet_ff) / (self.k2_ff + self.ke_ff + self.kg_ff + 0)
        return self.cb_ff
    def cbl_ff_f(self):
        self.cbl_ff = (1e6*self.cb_ff) / self.v_lb_ff
        return self.cbl_ff
    # benthic invertebrates pesticide concentration originating from uptake through diet k1=0  
    def cbd_ff_f(self):
        self.cbd_ff = (0 * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_ff * self.diet_ff) / (self.k2_ff + self.ke_ff + self.kg_ff + 0)
        return self.cbd_ff
    # benthic invertebrates pesticide concentration originating from uptake through respiration (kd=0)    
    def cbr_ff_f(self):
        self.kd_ff = 0
        self.cbr_ff = (self.k1_ff * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + 0 * self.diet_ff) / (self.k2_ff + self.ke_ff + self.kg_ff + 0)
        return self.cbr_ff
    #filter feeder total bioconcentration factor
    def cbf_ff_f(self):
        self.kd_ff = 0
        self.ke_ff = 0
      #  km_ff = 0  is always = 0  
        self.kg_ff = 0
        self.cbf_ff = ((self.k1_ff * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_ff * self.diet_ff) / (self.k2_ff + self.ke_ff + self.kg_ff + 0)) /self.c_wto
        return self.cbf_ff
    # filter feeder lipid normalized bioconcentration factor
    def cbfl_ff_f(self):
        self.kd_ff = 0
        self.ke_ff = 0
      #  km_ff = 0  is always = 0  
        self.kg_ff = 0
        self.cbfl_ff = (((self.k1_ff * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_ff * self.diet_ff) / (self.k2_ff + self.ke_ff + self.kg_ff + 0))) / self.v_lb_ff /(self.c_wto * self.phi)
        return self.cbfl_ff    
    # filter feeder bioaccumulation factor
    def cbaf_ff_f(self):
        self.cbaf_ff = (1e6 * self.cb_ff) / self.water_column_EEC
        return self.cbaf_ff
    # filter feeder lipid normalized bioaccumulation factor
    def cbafl_ff_f(self):
        self.cbafl_ff = self.cbl_ff / self.water_d
        return self.cbafl_ff    
    # filter feeder biota-sediment bioaccumulation factor
    def cbsafl_ff_f(self):
        self.cbsafl_ff = (self.cb_ff / self.v_lb_ff) / self.sed_om
        return self.cbsafl_ff    
    # filter feeder biomagnification factor
    def bmf_ff_f(self):
        self.bmf_ff = (self.cb_ff / self.v_lb_ff) / ((self.ff_p_benthic_invertebrates * self.cb_beninv / self.v_lb_beninv) + (self.ff_p_zooplankton * self.cb_zoo / self.v_lb_zoo) + (self.ff_p_phytoplankton * self.cb_phytoplankton / self.v_lb_phytoplankton))
        return self.bmf_ff
    #########################################################################
    ############# small fish
    ## ventilation rate     
    def gv_sf_f(self):  
        self.gv_sf = (1400.0 * ((self.wb_sf**0.65)/self.c_ox))
        return self.gv_sf

    # rate constant for elimination through the gills for small fish
    def ew_sf_f(self):
        self.ew_sf = (1.0/(1.85+(155.0/self.k_ow)))           
        return self.ew_sf

    #uptake rate constant through respiratory area for small fish  
    def k1_sf_f(self):
        self.k1_sf = ((self.ew_sf * self.gv_sf) / self.wb_sf)   
        return self.k1_sf
    # small fish water partition coefficient
    def k_bw_sf_f(self):
        self.k_bw_sf = (self.v_lb_sf * self.k_ow) + (self.v_nb_sf * 0.035 * self.k_ow) + self.v_wb_sf
        return self.k_bw_sf    
    # elimination rate constant through the gills for small fish   
    def k2_sf_f(self):
        self.k2_sf = self.k1_sf / self.k_bw_sf
        return self.k2_sf 
     # small fish dietary pesticide transfer efficiency
    def ed_sf_f(self):
        self.ed_sf = 1 / (.0000003 * self.k_ow + 2.0)
        return self.ed_sf
    # small fish feeding rate
    def gd_sf_f(self): 
        self.gd_sf = 0.022 * self.wb_sf **0.85 * math.exp(0.06*self.w_t)
        return self.gd_sf
    # small fish rate constant pesticide uptake by food ingestion
    def kd_sf_f(self):
        self.kd_sf = self.ed_sf * self.gd_sf / self.wb_sf  
        return self.kd_sf

    # small fish growth rate constant
    def kg_sf_f(self):
        if self.w_t < 17.5:
            self.kg_sf = 0.0005 * self.wb_sf **-0.2
        else:
            self.kg_sf = 0.00251 * self.wb_sf **-0.2
        return self.kg_sf   
        
    #overall lipid content of diet
    def v_ld_sf_f(self):
        self.v_ld_sf = self.sf_p_sediment * self.s_lipid + self.sf_p_phytoplankton * self.v_lb_phytoplankton + self.sf_p_benthic_invertebrates * self.v_lb_beninv + self.sf_p_zooplankton * self.v_lb_zoo + self.sf_p_filter_feeders * self.v_lb_ff
        return self.v_ld_sf
    # overall nonlipid content of diet
    def v_nd_sf_f(self):
        self.v_nd_sf = self.sf_p_sediment * self.s_NLOM + self.sf_p_phytoplankton * self.v_nb_phytoplankton + self.sf_p_benthic_invertebrates * self.v_nb_beninv + self.sf_p_zooplankton * self.v_nb_zoo + self.sf_p_filter_feeders * self.v_nb_ff
        return self.v_nd_sf
    # overall water content of diet 
    def v_wd_sf_f(self):   
        self.v_wd_sf = self.sf_p_sediment * self.s_water + self.sf_p_phytoplankton * self.v_wb_phytoplankton + self.sf_p_benthic_invertebrates * self.v_wb_beninv + self.sf_p_zooplankton * self.v_wb_zoo + self.sf_p_filter_feeders * self.v_wb_ff
        return self.v_wd_sf   
        
    def gf_sf_f(self):
        self.gf_sf = ((1-0.92)*self.v_ld_sf+(1-0.6)*self.v_nd_sf+(1-0.25)*self.v_wd_sf)*self.gd_sf
        return self.gf_sf
     
    #lipid content in gut 
    def vlg_sf_f(self):
        self.vlg_sf = (1-0.92) * self.v_ld_sf * self.gd_sf / self.gf_sf
        return self.vlg_sf
    # non lipid content in gut    
    def vng_sf_f(self):
        self.vng_sf = (1 - 0.6) * self.v_nd_sf * self.gd_sf / self.gf_sf
        return self.vng_sf
    # water content in the gut
    def vwg_sf_f(self):
        self.vwg_sf = (1 - 0.25) * self.v_wd_sf * self.gd_sf / self.gf_sf
        return self.vwg_sf  

    def kgb_sf_f(self):
        self.kgb_sf = (self.vlg_sf * self.k_ow + self.vng_sf * 0.035 * self.k_ow + self.vwg_sf) / (self.v_lb_sf * self.k_ow + self.v_nb_sf * 0.035 * self.k_ow + self.v_wb_sf) 
        return self.kgb_sf 

    def ke_sf_f(self):
        self.ke_sf = self.gf_sf * self.ed_sf * (self.kgb_sf / self.wb_sf)
        return self.ke_sf

    def diet_sf_f(self):  
        self.diet_sf = self.c_s * self.sf_p_sediment + self.cb_phytoplankton * self.sf_p_phytoplankton + self.cb_zoo * self.sf_p_zooplankton + self.cb_beninv * self.sf_p_benthic_invertebrates + self.cb_ff * self.sf_p_filter_feeders
        return self.diet_sf

     # small fish pesticide tissue residue
    def cb_sf_f(self):
        self.cb_sf = (self.k1_sf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_sf * self.diet_sf) / (self.k2_sf + self.ke_sf + self.kg_sf + 0)
        return self.cb_sf
    # small fish lipid normalized pesticide tissue residue
    def cbl_sf_f(self):
        self.cbl_sf = (1e6*self.cb_sf) / self.v_lb_sf
        return self.cbl_sf
    # small fish pesticide concentration originating from uptake through diet k1=0     
    def cbd_sf_f(self):
        self.cbd_sf = (0 * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_sf * self.diet_sf) / (self.k2_sf + self.ke_sf + self.kg_sf + 0)
        return self.cbd_sf
    # small fish pesticide concentration originating from uptake through respiration (kd=0)
    def cbr_sf_f(self):
        self.cbr_sf = (self.k1_sf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + 0 * self.diet_sf) / (self.k2_sf + self.ke_sf + self.kg_sf + 0)
        return self.cbr_sf
    #small fish total bioconcentration factor
    def cbf_sf_f(self):
        self.kd_sf = 0
        self.ke_sf = 0
    #    km_sf = 0 always = 0
        self.kg_sf = 0
        self.cbf_sf = ((self.k1_sf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_sf * self.diet_sf) / (self.k2_sf + self.ke_sf + self.kg_sf + 0)) / self.c_wto
        return self.cbf_sf    
    # small fish lipid normalized bioconcentration factor
    def cbfl_sf_f(self):
        self.kd_sf = 0
        self.ke_sf = 0
    #    km_sf = 0 always = 0
        self.kg_sf = 0
        self.cbfl_sf = (((self.k1_sf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_sf * self.diet_sf) / (self.k2_sf + self.ke_sf + self.kg_sf + 0)) / self.v_lb_sf) / (self.c_wto * self.phi)
        return self.cbfl_sf     
    # small fish bioaccumulation factor
    def cbaf_sf_f(self):
        self.cbaf_sf = (1e6 * self.cb_sf) / self.water_column_EEC
        return self.cbaf_sf    
    # small fish lipid normalized bioaccumulation factor
    def cbafl_sf_f(self):
        self.cbafl_sf = self.cbl_sf / self.water_d
        return self.cbafl_sf      
    def cbsafl_sf_f(self):
        self.cbsafl_sf = (self.cb_sf / self.v_lb_sf) / self.sed_om
        return self.cbsafl_sf   
    # small fish biomagnification factor
    def bmf_sf_f(self):
        self.bmf_sf = (self.cb_sf / self.v_lb_sf) / ((self.sf_p_filter_feeders * self.cb_ff / self.v_lb_ff) + (self.sf_p_benthic_invertebrates * self.cb_beninv / self.v_lb_beninv) + (self.sf_p_zooplankton * self.cb_zoo / self.v_lb_zoo) + (self.sf_p_phytoplankton * self.cb_phytoplankton / self.v_lb_phytoplankton))
        return self.bmf_sf
           
    ###########################################################################################
    ############ medium fish
    ## ventilation rate     
    def gv_mf_f(self):  
        self.gv_mf = (1400.0 * ((self.wb_mf**0.65)/self.c_ox))
        return self.gv_mf

    # rate constant for elimination through the gills for medium fish
    def ew_mf_f(self):
        self.ew_mf = (1.0/(1.85+(155.0/self.k_ow)))           
        return self.ew_mf

    #uptake rate constant through respiratory area for medium fish  
    def k1_mf_f(self):
        self.k1_mf = ((self.ew_mf * self.gv_mf) / self.wb_mf)   
        return self.k1_mf
    # medium fish water partition coefficient
    def k_bw_mf_f(self):
        self.k_bw_mf = (self.v_lb_mf * self.k_ow) + (self.v_nb_mf * 0.035 * self.k_ow) + self.v_wb_mf
        return self.k_bw_mf    
    # elimination rate constant through the gills for medium fish   
    def k2_mf_f(self):
        self.k2_mf = self.k1_mf / self.k_bw_mf
        return self.k2_mf 
     # medium fish dietary pesticide transfer efficiency
    def ed_mf_f(self):
        self.ed_mf = 1 / (.0000003 * self.k_ow + 2.0)
        return self.ed_mf
    # medium fish feeding rate
    def gd_mf_f(self): 
        self.gd_mf = 0.022 * self.wb_mf **0.85 * math.exp(0.06*self.w_t)
        return self.gd_mf
    # medium fish rate constant pesticide uptake by food ingestion
    def kd_mf_f(self):
        self.kd_mf = self.ed_mf * self.gd_mf / self.wb_mf  
        return self.kd_mf

    # medium fish growth rate constant
    def kg_mf_f(self):
        if self.w_t < 17.5:
            self.kg_mf = 0.0005 * self.wb_mf **-0.2
        else:
            self.kg_mf = 0.00251 * self.wb_mf **-0.2
        return self.kg_mf   
    #overall lipid content of diet
    def v_ld_mf_f(self):
        self.v_ld_mf = self.mf_p_sediment * self.s_lipid + self.mf_p_phytoplankton * self.v_lb_phytoplankton + self.mf_p_benthic_invertebrates * self.v_lb_beninv + self.mf_p_zooplankton * self.v_lb_zoo + self.mf_p_filter_feeders * self.v_lb_ff + self.mf_p_small_fish * self.v_lb_sf
        return self.v_ld_mf
    # overall nonlipid content of diet
    def v_nd_mf_f(self):
        self.v_nd_mf = self.mf_p_sediment * self.s_NLOM + self.mf_p_phytoplankton * self.v_nb_phytoplankton + self.mf_p_benthic_invertebrates * self.v_nb_beninv + self.mf_p_zooplankton * self.v_nb_zoo + self.mf_p_filter_feeders * self.v_nb_ff + self.mf_p_small_fish * self.v_nb_sf
        return self.v_nd_mf
    # overall water content of diet 
    def v_wd_mf_f(self):   
        self.v_wd_mf = self.mf_p_sediment * self.s_water + self.mf_p_phytoplankton * self.v_wb_phytoplankton + self.mf_p_benthic_invertebrates * self.v_wb_beninv + self.mf_p_zooplankton * self.v_wb_zoo + self.mf_p_filter_feeders * self.v_wb_ff + self.mf_p_small_fish * self.v_wb_sf
        return self.v_wd_mf   
    def gf_mf_f(self):
        self.gf_mf = ((1-0.92)*self.v_ld_mf+(1-0.6)*self.v_nd_mf+(1-0.25)*self.v_wd_mf)*self.gd_mf
        return self.gf_mf

    #lipid content in gut 
    def vlg_mf_f(self):
        self.vlg_mf = (1-0.92) * self.v_ld_mf * self.gd_mf / self.gf_mf
        return self.vlg_mf
    # non lipid content in gut    
    def vng_mf_f(self):
        self.vng_mf = (1 - 0.6) * self.v_nd_mf * self.gd_mf / self.gf_mf
        return self.vng_mf
    # water content in the gut
    def vwg_mf_f(self):
        self.vwg_mf = (1 - 0.25) * self.v_wd_mf * self.gd_mf / self.gf_mf
        return self.vwg_mf  

    def kgb_mf_f(self):
        self.kgb_mf = (self.vlg_mf * self.k_ow + self.vng_mf * 0.035 * self.k_ow + self.vwg_mf) / (self.v_lb_mf * self.k_ow + self.v_nb_mf * 0.035 * self.k_ow + self.v_wb_mf) 
        return self.kgb_mf 

    def ke_mf_f(self):
        self.ke_mf = self.gf_mf * self.ed_mf * (self.kgb_mf / self.wb_mf)
        return self.ke_mf

    def diet_mf_f(self):  
        self.diet_mf = self.c_s * self.mf_p_sediment + self.cb_phytoplankton * self.mf_p_phytoplankton + self.cb_zoo * self.mf_p_zooplankton + self.cb_beninv * self.mf_p_benthic_invertebrates + self.cb_ff * self.mf_p_filter_feeders + self.cb_sf * self.mf_p_small_fish
        return self.diet_mf

     # medium fish pesticide tissue residue
    def cb_mf_f(self):
        self.cb_mf = (self.k1_mf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_mf * self.diet_mf) / (self.k2_mf + self.ke_mf + self.kg_mf + 0)
        return self.cb_mf
    # medium fish lipid normalized pesticide tissue residue
    def cbl_mf_f(self):
        self.cbl_mf = (1e6*self.cb_mf) / self.v_lb_mf
        return self.cbl_mf
    # medium fish pesticide concentration originating from uptake through diet k1=0     
    def cbd_mf_f(self): 
        self.cbd_mf = (0 * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_mf * self.diet_mf) / (self.k2_mf + self.ke_mf + self.kg_mf + 0)
        return self.cbd_mf
    # medium fish pesticide concentration originating from uptake through respiration (kd=0)    
    def cbr_mf_f(self):   
        self.cbr_mf = (self.k1_mf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + 0 * self.diet_mf) / (self.k2_mf + self.ke_mf + self.kg_mf + 0)
        return self.cbr_mf  
    # medium fish total bioconcentration factor
    def cbf_mf_f(self):
        self.kd_mf = 0
        self.ke_mf = 0    
        # km_mf = 0    
        self.kg_mf = 0
        self.cbf_mf = ((self.k1_mf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_mf * self.diet_mf) / (self.k2_mf + self.ke_mf + self.kg_mf + 0)) / self.c_wto
        return self.cbf_mf
    # medium fish lipid normalized bioconcentration factor
    def cbfl_mf_f(self):
        self.kd_mf = 0
        self.ke_mf = 0    
        # km_mf = 0    
        self.kg_mf = 0
        self.cbfl_mf = ((((self.k1_mf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_mf * self.diet_mf) / (self.k2_mf + self.ke_mf + self.kg_mf + 0))) / self.v_lb_mf) / (self.c_wto * self.phi)
        return self.cbfl_mf    
    # medium fish bioaccumulation factor
    def cbaf_mf_f(self):
        self.cbaf_mf = (1e6 * self.cb_mf) / self.water_column_EEC
        return self.cbaf_mf    
    # medium fish lipid normalized factor
    def cbafl_mf_f(self):
        self.cbafl_mf = self.cbl_mf / self.water_d
        return self.cbafl_mf     
    def cbsafl_mf_f(self):
        self.cbsafl_mf = (self.cb_mf / self.v_lb_mf) / self.sed_om
        return self.cbsafl_mf
    # medium fish biomagnification factor
    def cbmf_mf_f(self):
        self.cbmf_mf = (self.cb_mf / self.v_lb_mf) / ((self.mf_p_small_fish * self.cb_sf / self.v_lb_sf) + (self.mf_p_filter_feeders * self.cb_ff / self.v_lb_ff) + (self.mf_p_benthic_invertebrates * self.cb_beninv / self.v_lb_beninv) + (self.mf_p_zooplankton * self.cb_zoo / self.v_lb_zoo) + (self.mf_p_phytoplankton * self.cb_phytoplankton / self.v_lb_phytoplankton)) 
        return self.cbmf_mf    
    ###########################################################################################
    ############ large fish
    ## ventilation rate     
    def gv_lf_f(self):  
        self.gv_lf = (1400.0 * ((self.wb_lf**0.65)/self.c_ox))
        return self.gv_lf

    # rate constant for elimination through the gills for large fish
    def ew_lf_f(self):
        self.ew_lf = (1.0/(1.85+(155.0/self.k_ow)))           
        return self.ew_lf

    #uptake rate constant through respiratory area for large fish  
    def k1_lf_f(self):
        self.k1_lf = ((self.ew_lf * self.gv_lf) / self.wb_lf)   
        return self.k1_lf
    # large fish water partition coefficient
    def k_bw_lf_f(self):
        self.k_bw_lf = (self.v_lb_lf * self.k_ow) + (self.v_nb_lf * 0.035 * self.k_ow) + self.v_wb_lf
        return self.k_bw_lf    
    # elimination rate constant through the gills for large fish   
    def k2_lf_f(self):
        self.k2_lf = self.k1_lf / self.k_bw_lf
        return self.k2_lf 
     # large fish dietary pesticide transfer efficiency
    def ed_lf_f(self):
        self.ed_lf = 1 / (.0000003 * self.k_ow + 2.0)
        return self.ed_lf
    # large fish feeding rate
    def gd_lf_f(self): 
        self.gd_lf = 0.022 * self.wb_lf **0.85 * math.exp(0.06*self.w_t)
        return self.gd_lf
    # large fish rate constant pesticide uptake by food ingestion
    def kd_lf_f(self):
        self.kd_lf = self.ed_lf * self.gd_lf / self.wb_lf  
        return self.kd_lf
    # medium fish growth rate constant
    def kg_lf_f(self):
        if self.w_t < 17.5:
            self.kg_lf = 0.0005 * self.wb_lf **-0.2
        else:
            self.kg_lf = 0.00251 * self.wb_lf **-0.2
        return self.kg_lf   

    #overall lipid content of diet
    def v_ld_lf_f(self):
        self.v_ld_lf = self.lf_p_sediment * self.s_lipid + self.lf_p_phytoplankton * self.v_lb_phytoplankton + self.lf_p_benthic_invertebrates * self.v_lb_beninv + self.lf_p_zooplankton * self.v_lb_zoo + self.lf_p_filter_feeders * self.v_lb_ff + self.lf_p_small_fish * self.v_lb_sf + self.lf_p_medium_fish * self.v_lb_mf
        return self.v_ld_lf

    # overall nonlipid content of diet
    def v_nd_lf_f(self):
        self.v_nd_lf = self.lf_p_sediment * self.s_NLOM + self.lf_p_phytoplankton * self.v_nb_phytoplankton + self.lf_p_benthic_invertebrates * self.v_nb_beninv + self.lf_p_zooplankton * self.v_nb_zoo + self.lf_p_filter_feeders * self.v_nb_ff + self.lf_p_small_fish * self.v_nb_sf + self.lf_p_medium_fish * self.v_nb_mf
        return self.v_nd_lf
    # overall water content of diet 
    def v_wd_lf_f(self):   
        self.v_wd_lf = self.lf_p_sediment * self.s_water + self.lf_p_phytoplankton * self.v_wb_phytoplankton + self.lf_p_benthic_invertebrates * self.v_wb_beninv + self.lf_p_zooplankton * self.v_wb_zoo + self.lf_p_filter_feeders * self.v_wb_ff + self.lf_p_small_fish * self.v_wb_sf + self.lf_p_medium_fish * self.v_wb_mf
        return self.v_wd_lf   

    def gf_lf_f(self):
        self.gf_lf = ((1-0.92)*self.v_ld_lf+(1-0.6)*self.v_nd_lf+(1-0.25)*self.v_wd_lf)*self.gd_lf
        return self.gf_lf

    #lipid content in gut 
    def vlg_lf_f(self):
        self.vlg_lf = (1-0.92) * self.v_ld_lf * self.gd_lf / self.gf_lf
        return self.vlg_lf
    # non lipid content in gut    
    def vng_lf_f(self):
        self.vng_lf = (1 - 0.6) * self.v_nd_lf * self.gd_lf / self.gf_lf
        return self.vng_lf
    # water content in the gut
    def vwg_lf_f(self):
        self.vwg_lf = (1 - 0.25) * self.v_wd_lf * self.gd_lf / self.gf_lf
        return self.vwg_lf  

    def kgb_lf_f(self):
        self.kgb_lf = (self.vlg_lf * self.k_ow + self.vng_lf * 0.035 * self.k_ow + self.vwg_lf) / (self.v_lb_lf * self.k_ow + self.v_nb_lf * 0.035 * self.k_ow + self.v_wb_lf) 
        return self.kgb_lf 

    def ke_lf_f(self):
        self.ke_lf = self.gf_lf * self.ed_lf * (self.kgb_lf / self.wb_lf)
        return self.ke_lf

    def diet_lf_f(self):  
        self.diet_lf = self.c_s * self.lf_p_sediment + self.cb_phytoplankton * self.lf_p_phytoplankton + self.cb_zoo * self.lf_p_zooplankton + self.cb_beninv * self.lf_p_benthic_invertebrates + self.cb_ff * self.lf_p_filter_feeders + self.cb_sf * self.lf_p_small_fish + self.cb_mf * self.lf_p_medium_fish
        return self.diet_lf

     # large fish pesticide tissue residue
    def cb_lf_f(self):
        self.cb_lf = (self.k1_lf * (1.0 * self.phi * self.c_wto + 0.00 * self.c_wdp) + self.kd_lf * self.diet_lf) / (self.k2_lf + self.ke_lf + self.kg_lf + 0)
        return self.cb_lf
    # large fish lipid normalized pesticide tissue residue
    def cbl_lf_f(self):
        self.cbl_lf = (1e6*self.cb_lf) / self.v_lb_lf
        return self.cbl_lf
    # large fish pesticide concentration originating from uptake through diet k1=0     
    def cbd_lf_f(self):
        self.cbd_lf = (0 * (1.0 * self.phi * self.c_wto + 0.0 * self.c_wdp) + self.kd_lf * self.diet_lf) / (self.k2_lf + self.ke_lf + self.kg_lf + 0)
        return self.cbd_lf
    # large fish pesticide concentration originating from uptake through respiration (kd=0)    
    def cbr_lf_f(self):
        self.cbr_lf = (self.k1_lf * (1.0 * self.phi * self.c_wto + 0.0 * self.c_wdp) + 0 * self.diet_lf) / (self.k2_lf + self.ke_lf + self.kg_lf + 0)
        return self.cbr_lf  
    # large fish total bioconcentration factor
    def cbf_lf_f(self):
        self.kd_lf = 0
        self.ke_lf = 0    
        #km_lf = 0    
        self.kg_lf = 0
        self.cbf_lf = ((self.k1_lf * (1.0 * self.phi * self.c_wto + 0.00 * self.c_wdp) + self.kd_lf * self.diet_lf) / (self.k2_lf + self.ke_lf + self.kg_lf + 0)) / self.c_wto
        return self.cbf_lf
    # large fish lipid normalized total bioconcentration factor
    def cbfl_lf_f(self):
        self.kd_lf = 0
        self.ke_lf = 0    
        #km_lf = 0    
        self.kg_lf = 0
        self.cbfl_lf = (((self.k1_lf * (1.0 * self.phi * self.c_wto + 0.00 * self.c_wdp) + self.kd_lf * self.diet_lf) / (self.k2_lf + self.ke_lf + self.kg_lf + 0)) / self.v_lb_lf) / (self.c_wto * self.phi)
        return self.cbfl_lf
    # large fish bioaccumulation factor
    def cbaf_lf_f(self):
        self.cbaf_lf = (1e6 * self.cb_lf) / self.water_column_EEC
        return self.cbaf_lf
    # large fish lipid normalized bioaccumulation factor
    def cbafl_lf_f(self):
        self.cbafl_lf = self.cbl_lf / self.water_d
        return self.cbafl_lf  
    # large fish biota-sediment accumulation factors    
    def cbsafl_lf_f(self):
        self.cbsafl_lf = (self.cb_lf / self.v_lb_lf) / self.sed_om
        return self.cbsafl_lf  
    # large fish biomagnification factor
    def cbmf_lf_f(self):
        self.cbmf_lf = (self.cb_lf / self.v_lb_lf) / ((self.lf_p_medium_fish * self.cb_mf / self.v_lb_mf) + (self.lf_p_small_fish * self.cb_sf / self.v_lb_sf) + (self.lf_p_filter_feeders * self.cb_ff / self.v_lb_ff) + (self.lf_p_benthic_invertebrates * self.cb_beninv / self.v_lb_beninv) + (self.lf_p_zooplankton * self.cb_zoo / self.v_lb_zoo) + (self.lf_p_phytoplankton * self.cb_phytoplankton / self.v_lb_phytoplankton)) 
        return self.cbmf_lf
    
    ##########################################################################
    ################################## Mammals EECs
    def mweight_f(self):
        self.cb_a = np.array([[self.cb_phytoplankton, self.cb_zoo, self.cb_beninv, self.cb_ff, self.cb_sf, self.cb_mf, self.cb_lf]])
        self.cb_a2 = self.cb_a * 1000000
        #array of mammal weights       
        self.mweight= np.array([[0.018, 0.085, 0.45, 1.8, 5, 15]])
        return self.mweight

    def dfir_f(self):
        self.dfir = (0.0687*self.mweight**0.822)/self.mweight
        return self.dfir

    def wet_food_ingestion_m_f(self):
        #creation of array for mammals of dry food ingestion rate
        #array of percent water in biota
        self.v_wb_a = np.array([[self.v_wb_phytoplankton, self.v_wb_zoo, self.v_wb_beninv, self.v_wb_ff, self.v_wb_sf, self.v_wb_mf, self.v_wb_lf]])
        #array of % diet of food web for each mammal
        self.diet_mammal = np.array([[0, 0, 1, 0, 0, 0, 0], [0, 0, .34, .33, .33, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0,0,0,0,0,1,0], [0,0,0,0,0,1,0], [0,0,0,0,0,0,1]])
        self.denom1 = self.diet_mammal * self.v_wb_a 
        self.denom1 = ([[ 0., 0., 0.76, 0., 0., 0., 0. ], [ 0., 0., 0.2584, 0.2805, 0.2409, 0., 0. ], [ 0., 0., 0., 0., 0., 0.73, 0. ], [ 0., 0., 0., 0., 0., 0.73, 0. ], [ 0., 0., 0., 0., 0., 0.73, 0. ], [ 0., 0., 0., 0., 0., 0., 0.73 ]])     
        self.denom2 = np.cumsum(self.denom1, axis = 1)
        self.denom3 = self.denom2[:,6] # selects out seventh row of array which is the cumulative sums of the products      
        self.denom4 = 1 - self.denom3
        #wet food ingestion rate for mammals
        self.wet_food_ingestion_m = self.dfir / self.denom4
        return self.wet_food_ingestion_m

    def drinking_water_intake_m_f(self):
        #array of drinking water intake rate for mammals
        self.drinking_water_intake_m = .099 * self.mweight**0.9
        return self.drinking_water_intake_m

    def db4_f(self):
        self.db1 = self.cb_a2 * self.diet_mammal
        self.db2 = np.cumsum(self.db1, axis = 1)
        self.db3 = self.db2[:,6]
        #dose based  EEC
        self.db4 = (self.db3/1000) * self.wet_food_ingestion_m + (self.water_column_EEC / 1000)*(self.drinking_water_intake_m/self.mweight)
        return self.db4

    def db5_f(self):
        #dietary based EEC
        self.db5 = self.db3/1000
        return self.db5

    ##########################################################################
    ################################## Avian EECs
    def aweight_f(self):
        self.aweight= np.array([[0.02, 6.7, 0.07, 2.9, 1.25, 7.5]])
        return self.aweight

    def dfir_a_f(self):
        self.dfir_a = (0.0582*self.aweight**0.651)/self.aweight
        return self.dfir_a

    def wet_food_ingestion_a_f(self):
        self.v_wb_a = np.array([[self.v_wb_phytoplankton, self.v_wb_zoo, self.v_wb_beninv, self.v_wb_ff, self.v_wb_sf, self.v_wb_mf, self.v_wb_lf]])
        self.diet_avian = np.array([[0, 0, .33, 0.33, 0.34, 0, 0], [0, 0, .33, .33, 0, 0.34, 0], [0, 0, 0.5, 0, 0.5,0,0], [0,0,0.5,0,0,0.5,0], [0,0,0,0,0,1,0], [0,0,0,0,0,0,1]])
        self.denom1a = self.diet_avian * self.v_wb_a  
        self.denom2a = np.cumsum(self.denom1a, axis = 1)     
        self.denom3a = self.denom2a[:,6] # selects out seventh row of array which is the cumulative sums of the products
        self.denom4a = 1 - self.denom3a
        self.wet_food_ingestion_a = self.dfir_a / self.denom4a
        return self.wet_food_ingestion_a

    def drinking_water_intake_a_f(self):
        self.drinking_water_intake_a = 0.059 * self.aweight**0.67
        return self.drinking_water_intake_a

    def db4a_f(self):
        self.db1a = self.cb_a2 * self.diet_avian
        self.db2a = np.cumsum(self.db1a, axis = 1)
        self.db3a = self.db2a[:,6]
        #dose based  EEC
        self.db4a = (self.db3a/1000) * self.wet_food_ingestion_a + (self.water_column_EEC / 1000)*(self.drinking_water_intake_a/self.aweight)
        return self.db4a

    def db5a_f(self):
        #dietary based EEC
        self.db5a = (self.db3a/1000)
        return self.db5a
     
    ##################################### toxicity values
    #################################### mammal
    #dose based acute toxicity for mammals
#     if m_species == '350':
#         acute_dose_based_m = mammalian_ld50 * (0.35 / mweight)**0.25
# #         return acute_dose_based_m
#     else:
#         acute_dose_based_m = mammalian_ld50 * (body_weight_of_the_tested_mamm_other / mweight)**0.25          
# #              return acute_dose_based_m

    def acute_dose_based_m_f(self):
        self.acute_dose_based_m = self.mammalian_ld50 * ((float(self.bw_mamm)/1000) / self.mweight)**0.25
        return self.acute_dose_based_m

# #dose based chronic toxicity for mammals        
#     if m_species == '350':
#         chronic_dose_based_m = (mammalian_chronic_endpoint/20) * ((0.35 / mweight)**0.25)
#     else:
# #            body_weight_of_the_tested_mamm_other = float(body_weight_of_the_tested_mamm_other)
#         chronic_dose_based_m = (mammalian_chronic_endpoint/20) * (body_weight_of_the_tested_mamm_other / mweight)**0.25
# #              return chronic_dose_based_m
    def chronic_dose_based_m_f(self):
        self.chronic_dose_based_m = (self.mammalian_chronic_endpoint / 20) * (((float(self.bw_mamm)/1000) / self.mweight)**0.25)
        return self.chronic_dose_based_m

#     #################################### avian
#     #dose based acute toxicity for birds
#     if Species_of_the_tested_bird == '178':
#         acute_dose_based_a = avian_ld50 * (aweight/0.178)**(mineau_scaling_factor-1)
#     elif Species_of_the_tested_bird == '1580':
#         acute_dose_based_a = avian_ld50 * (aweight/1.58)**(mineau_scaling_factor-1)
#     else: 
#         acute_dose_based_a = avian_ld50 * (aweight/float(body_weight_of_the_tested_bird_other))**(mineau_scaling_factor-1)
# #          return acute_dose_based_a
    
    def acute_dose_based_a_f(self):
        self.acute_dose_based_a = self.avian_ld50 * (self.aweight/(float(self.bw_bird)/1000))**(self.mineau_scaling_factor-1)
        return self.acute_dose_based_a

    ##################################### RQ Values
    #RQ dose based for mammals
    def acute_rq_dose_m_f(self):
        self.acute_rq_dose_m = self.db4 / self.acute_dose_based_m
        return self.acute_rq_dose_m

    def chronic_rq_dose_m_f(self):
        self.chronic_rq_dose_m = self.db4 / self.chronic_dose_based_m
        return self.chronic_rq_dose_m
    
    #RQ diet based for mammals
    def acute_rq_diet_m_f(self):
        self.acute_rq_diet_m = self.db5 / self.mammalian_lc50
        return self.acute_rq_diet_m

    def chronic_rq_diet_m_f(self):
        self.chronic_rq_diet_m = self.db5 / self.mammalian_chronic_endpoint
        return self.chronic_rq_diet_m

    #RQ dose based for birds
    def acute_rq_dose_a_f(self):
        self.acute_rq_dose_a = self.db4a / self.acute_dose_based_a
        return self.acute_rq_dose_a

    #RQ diet based for birds
    def acute_rq_diet_a_f(self):
        self.acute_rq_diet_a = self.db5a / self.avian_lc50
        return self.acute_rq_diet_a

    def chronic_rq_diet_a_f(self):
        self.chronic_rq_diet_a = self.db5a / self.avian_noaec
        return self.chronic_rq_diet_a