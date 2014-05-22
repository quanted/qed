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
import unittest
from StringIO import StringIO
from pprint import pprint
import csv
import sys
sys.path.append("../kabam")
from kabam import kabam_model,kabam_tables
import logging
from uber import uber_lib
import Queue
from collections import OrderedDict
import rest_funcs

logger = logging.getLogger('kabamBatchPage')

# Inputs
chemical_name=[]
l_kow=[]
k_oc=[]
c_wdp=[]
water_column_EEC=[]
c_wto=[]
mineau=[]
x_poc=[]
x_doc=[]
c_ox=[]
w_t=[]
c_ss=[]
oc=[]
k_ow=[]
b_species =[]
bw_quail =[]
bw_duck =[]
bwb_other =[]
avian_ld50=[]
avian_lc50=[]
avian_noaec=[]
m_species =[]
bw_rat =[]
bwm_other =[]
mammalian_ld50=[]
mammalian_lc50=[]
mammalian_chronic_endpoint=[]
lf_p_sediment=[]
lf_p_phytoplankton=[]
lf_p_zooplankton=[]
lf_p_benthic_invertebrates=[]
lf_p_filter_feeders=[]
lf_p_small_fish=[]
lf_p_medium_fish=[]
mf_p_sediment=[]
mf_p_phytoplankton=[]
mf_p_zooplankton=[]
mf_p_benthic_invertebrates=[]
mf_p_filter_feeders=[]
mf_p_small_fish=[]
sf_p_sediment=[]
sf_p_phytoplankton=[]
sf_p_zooplankton=[]
sf_p_benthic_invertebrates=[]
sf_p_filter_feeders=[]
ff_p_sediment=[]
ff_p_phytoplankton=[]
ff_p_zooplankton=[]
ff_p_benthic_invertebrates=[]
beninv_p_sediment=[]
beninv_p_phytoplankton=[]
beninv_p_zooplankton=[]
zoo_p_sediment=[]
zoo_p_phyto=[]
s_lipid=[]
s_NLOM=[]
s_water=[]
v_lb_phytoplankton=[]
v_nb_phytoplankton=[]
v_wb_phytoplankton=[]
wb_zoo=[]
v_lb_zoo=[]
v_nb_zoo=[]
v_wb_zoo=[]
wb_beninv=[]
v_lb_beninv=[]
v_nb_beninv=[]
v_wb_beninv=[]
wb_ff=[]
v_lb_ff=[]
v_nb_ff=[]
v_wb_ff=[]
wb_sf=[]
v_lb_sf=[]
v_nb_sf=[]
v_wb_sf=[]
wb_mf=[]
v_lb_mf=[]
v_nb_mf=[]
v_wb_mf=[]
wb_lf=[]
v_lb_lf=[]
v_nb_lf=[]
v_wb_lf=[]
kg_phytoplankton=[]
kd_phytoplankton=[]
ke_phytoplankton=[]
mo_phytoplankton=[]
mp_phytoplankton=[]
km_phytoplankton=[]
km_zoo=[]
k1_phytoplankton=[]
k2_phytoplankton=[]
k1_zoo=[]
k2_zoo=[]
kd_zoo=[]
ke_zoo=[]
k1_beninv=[]
k2_beninv=[]
kd_beninv=[]
ke_beninv=[]
km_beninv=[]
k1_ff=[]
k2_ff=[]
kd_ff=[]
ke_ff=[]
km_ff=[]
k1_sf=[]
k2_sf=[]
kd_sf=[]
ke_sf=[]
km_sf=[]
k1_mf=[]
k2_mf=[]
kd_mf=[]
ke_mf=[]
km_mf=[]
k1_lf=[]
k2_lf=[]
kd_lf=[]
ke_lf=[]
km_lf=[]
rate_constants=[]

# Outputs
cb_phytoplankton=[]
cb_zoo=[]
cb_beninv=[]
cb_ff=[]
cb_sf=[]
cb_mf=[]
cb_lf=[]
cbl_phytoplankton=[]
cbl_zoo=[]
cbl_beninv=[]
cbl_ff=[]
cbl_sf=[]
cbl_mf=[]
cbl_lf=[]
cbd_zoo=[]
cbd_beninv=[]
cbd_ff=[]
cbd_sf=[]
cbd_mf=[]
cbd_lf=[]
cbr_phytoplankton=[]
cbr_zoo=[]
cbr_beninv=[]
cbr_ff=[]
cbr_sf=[]
cbr_mf=[]
cbr_lf=[]
cbf_phytoplankton=[]
cbf_zoo=[]
cbf_beninv=[]
cbf_ff=[]
cbf_sf=[]
cbf_mf=[]
cbf_lf=[]
cbaf_phytoplankton=[]
cbaf_zoo=[]
cbaf_beninv=[]
cbaf_ff=[]
cbaf_sf=[]
cbaf_mf=[]
cbaf_lf=[]
cbfl_phytoplankton=[]
cbfl_zoo=[]
cbfl_beninv=[]
cbfl_ff=[]
cbfl_sf=[]
cbfl_mf=[]
cbfl_lf=[]
cbafl_phytoplankton=[]
cbafl_zoo=[]
cbafl_beninv=[]
cbafl_ff=[]
cbafl_sf=[]
cbafl_mf=[]
cbafl_lf=[]
bmf_zoo=[]
bmf_beninv=[]
bmf_ff=[]
bmf_sf=[]
cbmf_mf=[]
cbmf_lf=[]
cbsafl_phytoplankton=[]
cbsafl_zoo=[]
cbsafl_beninv=[]
cbsafl_ff=[]
cbsafl_sf=[]
cbsafl_mf=[]
cbsafl_lf=[]
jid_all = []
jid_batch = []
kabam_obj =[]
kabam_obj_all =[]

logger = logging.getLogger("kabamBatchOutput")

def html_table(row_inp,iter):
    logger.info("iteration: " + str(iter))
    chemical_name.append(row_inp[0])
    l_kow.append(float(row_inp[1]))
    k_oc.append(float(row_inp[2]))
    c_wdp.append(float(row_inp[3]) / 1000000)
    water_column_EEC.append(float(row_inp[4]))
    c_wto.append(float(row_inp[4]) / 1000000)
    mineau.append(float(row_inp[5]))
    x_poc.append(float(row_inp[6]))
    x_doc.append(float(row_inp[7]))
    c_ox.append(float(row_inp[8]))
    w_t.append(float(row_inp[9]))
    c_ss.append(float(row_inp[10]))
    oc.append(float(row_inp[11]) / 100)
    k_ow.append(10**(float(row_inp[1])))
    b_species.append(row_inp[12])
    bw_quail.append(float(row_inp[13]))
    bw_duck.append(float(row_inp[14]))
    bwb_other.append(float(row_inp[15]))
    avian_ld50.append(float(row_inp[16]))
    avian_lc50.append(float(row_inp[17]))
    avian_noaec.append(float(row_inp[18]))
    m_species.append(row_inp[19])
    bw_rat.append(float(row_inp[20]))
    bwm_other.append(float(row_inp[21]))
    mammalian_ld50.append(float(row_inp[22]))
    mammalian_lc50.append(float(row_inp[23]))
    mammalian_chronic_endpoint.append(float(row_inp[24]))
    lf_p_sediment.append(float(row_inp[25]) / 100)
    lf_p_phytoplankton.append(float(row_inp[26]) / 100)
    lf_p_zooplankton.append(float(row_inp[27]) / 100)
    lf_p_benthic_invertebrates.append(float(row_inp[28]) / 100)
    lf_p_filter_feeders.append(float(row_inp[29]) / 100)
    lf_p_small_fish.append(float(row_inp[30]) / 100)
    lf_p_medium_fish.append(float(row_inp[31]) / 100)
    mf_p_sediment.append(float(row_inp[32]))
    mf_p_phytoplankton.append(float(row_inp[33]))
    mf_p_zooplankton.append(float(row_inp[34]))
    mf_p_benthic_invertebrates.append(float(row_inp[35]) / 100)
    mf_p_filter_feeders.append(float(row_inp[36]))
    mf_p_small_fish.append(float(row_inp[37]) / 100)
    sf_p_sediment.append(float(row_inp[38]))
    sf_p_phytoplankton.append(float(row_inp[39]))
    sf_p_zooplankton.append(float(row_inp[40]) / 100)
    sf_p_benthic_invertebrates.append(float(row_inp[41]) / 100)
    sf_p_filter_feeders.append(float(row_inp[42]))
    ff_p_sediment.append(float(row_inp[43]) / 100)
    ff_p_phytoplankton.append(float(row_inp[44]) / 100)
    ff_p_zooplankton.append(float(row_inp[45]) / 100)
    ff_p_benthic_invertebrates.append(float(row_inp[46]))
    beninv_p_sediment.append(float(row_inp[47]) / 100)
    beninv_p_phytoplankton.append(float(row_inp[48]) / 100)
    beninv_p_zooplankton.append(float(row_inp[49]) / 100)
    zoo_p_sediment.append(float(row_inp[50]))
    zoo_p_phyto.append(float(row_inp[51]) / 100)
    s_lipid.append(float(row_inp[52]) / 100)
    s_NLOM.append(float(row_inp[53]) / 100)
    s_water.append(float(row_inp[54]) / 100)
    v_lb_phytoplankton.append(float(row_inp[55]) / 100)
    v_nb_phytoplankton.append(float(row_inp[56]) / 100)
    v_wb_phytoplankton.append(float(row_inp[57]) / 100)
    wb_zoo.append(float(row_inp[58]))
    v_lb_zoo.append(float(row_inp[59]) / 100)
    v_nb_zoo.append(float(row_inp[60]) / 100)
    v_wb_zoo.append(float(row_inp[61]) / 100)
    wb_beninv.append(float(row_inp[62]))
    v_lb_beninv.append(float(row_inp[63]) / 100)
    v_nb_beninv.append(float(row_inp[64]) / 100)
    v_wb_beninv.append(float(row_inp[65]) / 100)
    wb_ff.append(float(row_inp[66]))
    v_lb_ff.append(float(row_inp[67]) / 100)
    v_nb_ff.append(float(row_inp[68]) / 100)
    v_wb_ff.append(float(row_inp[69]) / 100)
    wb_sf.append(float(row_inp[70]))
    v_lb_sf.append(float(row_inp[71]) / 100)
    v_nb_sf.append(float(row_inp[72]) / 100)
    v_wb_sf.append(float(row_inp[73]) / 100)
    wb_mf.append(float(row_inp[74]))
    v_lb_mf.append(float(row_inp[75]) / 100)
    v_nb_mf.append(float(row_inp[76]) / 100)
    v_wb_mf.append(float(row_inp[77]) / 100)
    wb_lf.append(float(row_inp[78]))
    v_lb_lf.append(float(row_inp[79]) / 100)
    v_nb_lf.append(float(row_inp[80]) / 100)
    v_wb_lf.append(float(row_inp[81]) / 100)
    kg_phytoplankton.append(float(row_inp[82]))
    kd_phytoplankton.append(float(row_inp[83]))
    ke_phytoplankton.append(float(row_inp[84]))
    mo_phytoplankton.append(float(row_inp[85]))
    mp_phytoplankton.append(float(row_inp[86]))
    km_phytoplankton.append(float(row_inp[87]))
    km_zoo.append(float(row_inp[88]))
    k1_phytoplankton.append(float(row_inp[89]))
    k2_phytoplankton.append(float(row_inp[90]))
    k1_zoo.append(float(row_inp[91]))
    k2_zoo.append(float(row_inp[92]))
    kd_zoo.append(float(row_inp[93]))
    ke_zoo.append(float(row_inp[94]))
    k1_beninv.append(float(row_inp[95]))
    k2_beninv.append(float(row_inp[96]))
    kd_beninv.append(float(row_inp[97]))
    ke_beninv.append(float(row_inp[98]))
    km_beninv.append(float(row_inp[99]))
    k1_ff.append(float(row_inp[100]))
    k2_ff.append(float(row_inp[101]))
    kd_ff.append(float(row_inp[102]))
    ke_ff.append(float(row_inp[103]))
    km_ff.append(float(row_inp[104]))
    k1_sf.append(float(row_inp[105]))
    k2_sf.append(float(row_inp[106]))
    kd_sf.append(float(row_inp[107]))
    ke_sf.append(float(row_inp[108]))
    km_sf.append(float(row_inp[109]))
    k1_mf.append(float(row_inp[110]))
    k2_mf.append(float(row_inp[111]))
    kd_mf.append(float(row_inp[112]))
    ke_mf.append(float(row_inp[113]))
    km_mf.append(float(row_inp[114]))
    k1_lf.append(float(row_inp[115]))
    k2_lf.append(float(row_inp[116]))
    kd_lf.append(float(row_inp[117]))
    ke_lf.append(float(row_inp[118]))
    km_lf.append(float(row_inp[119]))
    rate_constants.append(row_inp[120])


    kabam_obj = kabam_model.kabam(
            True,True,'batch', chemical_name[iter],l_kow[iter],k_oc[iter],c_wdp[iter],water_column_EEC[iter],c_wto[iter],mineau[iter],x_poc[iter],x_doc[iter],c_ox[iter],w_t[iter],c_ss[iter],oc[iter],k_ow[iter],
            b_species[iter],bw_quail[iter],bw_duck[iter],bwb_other[iter],avian_ld50[iter],avian_lc50[iter],avian_noaec[iter],m_species[iter],bw_rat[iter],bwm_other[iter],mammalian_ld50[iter],mammalian_lc50[iter],mammalian_chronic_endpoint[iter],
            lf_p_sediment[iter],lf_p_phytoplankton[iter],lf_p_zooplankton[iter],lf_p_benthic_invertebrates[iter],lf_p_filter_feeders[iter],lf_p_small_fish[iter],lf_p_medium_fish[iter],
            mf_p_sediment[iter],mf_p_phytoplankton[iter],mf_p_zooplankton[iter],mf_p_benthic_invertebrates[iter],mf_p_filter_feeders[iter],mf_p_small_fish[iter],
            sf_p_sediment[iter],sf_p_phytoplankton[iter],sf_p_zooplankton[iter],sf_p_benthic_invertebrates[iter],sf_p_filter_feeders[iter],
            ff_p_sediment[iter],ff_p_phytoplankton[iter],ff_p_zooplankton[iter],ff_p_benthic_invertebrates[iter],
            beninv_p_sediment[iter],beninv_p_phytoplankton[iter],beninv_p_zooplankton[iter],
            zoo_p_sediment[iter],zoo_p_phyto[iter],
            s_lipid[iter],s_NLOM[iter],s_water[iter],
            v_lb_phytoplankton[iter],v_nb_phytoplankton[iter],v_wb_phytoplankton[iter],wb_zoo[iter],v_lb_zoo[iter],v_nb_zoo[iter],v_wb_zoo[iter],wb_beninv[iter],v_lb_beninv[iter],v_nb_beninv[iter],v_wb_beninv[iter],wb_ff[iter],v_lb_ff[iter],v_nb_ff[iter],v_wb_ff[iter],wb_sf[iter],v_lb_sf[iter],v_nb_sf[iter],v_wb_sf[iter],wb_mf[iter],v_lb_mf[iter],v_nb_mf[iter],v_wb_mf[iter],wb_lf[iter],v_lb_lf[iter],v_nb_lf[iter],v_wb_lf[iter],
            kg_phytoplankton[iter],kd_phytoplankton[iter],ke_phytoplankton[iter],mo_phytoplankton[iter],mp_phytoplankton[iter],km_phytoplankton[iter],km_zoo[iter],
            k1_phytoplankton[iter],k2_phytoplankton[iter],
            k1_zoo[iter],k2_zoo[iter],kd_zoo[iter],ke_zoo[iter],k1_beninv[iter],k2_beninv[iter],kd_beninv[iter],ke_beninv[iter],km_beninv[iter],
            k1_ff[iter],k2_ff[iter],kd_ff[iter],ke_ff[iter],km_ff[iter],k1_sf[iter],k2_sf[iter],kd_sf[iter],ke_sf[iter],km_sf[iter],k1_mf[iter],k2_mf[iter],kd_mf[iter],ke_mf[iter],km_mf[iter],k1_lf[iter],k2_lf[iter],kd_lf[iter],ke_lf[iter],km_lf[iter],
            rate_constants[iter]
            )

    # kabam_obj = kabam_model.kabam(
    #         True,True,'batch', chemical_name[iter-1],l_kow[iter-1],k_oc[iter-1],c_wdp[iter-1],water_column_EEC[iter-1],c_wto[iter-1],mineau[iter-1],x_poc[iter-1],x_doc[iter-1],c_ox[iter-1],w_t[iter-1],c_ss[iter-1],oc[iter-1],k_ow[iter-1],
    #         b_species[iter-1],bw_quail[iter-1],bw_duck[iter-1],bwb_other[iter-1],avian_ld50[iter-1],avian_lc50[iter-1],avian_noaec[iter-1],m_species[iter-1],bw_rat[iter-1],bwm_other[iter-1],mammalian_ld50[iter-1],mammalian_lc50[iter-1],mammalian_chronic_endpoint[iter-1],
    #         lf_p_sediment[iter-1],lf_p_phytoplankton[iter-1],lf_p_zooplankton[iter-1],lf_p_benthic_invertebrates[iter-1],lf_p_filter_feeders[iter-1],lf_p_small_fish[iter-1],lf_p_medium_fish[iter-1],
    #         mf_p_sediment[iter-1],mf_p_phytoplankton[iter-1],mf_p_zooplankton[iter-1],mf_p_benthic_invertebrates[iter-1],mf_p_filter_feeders[iter-1],mf_p_small_fish[iter-1],
    #         sf_p_sediment[iter-1],sf_p_phytoplankton[iter-1],sf_p_zooplankton[iter-1],sf_p_benthic_invertebrates[iter-1],sf_p_filter_feeders[iter-1],
    #         ff_p_sediment[iter-1],ff_p_phytoplankton[iter-1],ff_p_zooplankton[iter-1],ff_p_benthic_invertebrates[iter-1],
    #         beninv_p_sediment[iter-1],beninv_p_phytoplankton[iter-1],beninv_p_zooplankton[iter-1],
    #         zoo_p_sediment[iter-1],zoo_p_phyto[iter-1],
    #         s_lipid[iter-1],s_NLOM[iter-1],s_water[iter-1],
    #         v_lb_phytoplankton[iter-1],v_nb_phytoplankton[iter-1],v_wb_phytoplankton[iter-1],wb_zoo[iter-1],v_lb_zoo[iter-1],v_nb_zoo[iter-1],v_wb_zoo[iter-1],wb_beninv[iter-1],v_lb_beninv[iter-1],v_nb_beninv[iter-1],v_wb_beninv[iter-1],wb_ff[iter-1],v_lb_ff[iter-1],v_nb_ff[iter-1],v_wb_ff[iter-1],wb_sf[iter-1],v_lb_sf[iter-1],v_nb_sf[iter-1],v_wb_sf[iter-1],wb_mf[iter-1],v_lb_mf[iter-1],v_nb_mf[iter-1],v_wb_mf[iter-1],wb_lf[iter-1],v_lb_lf[iter-1],v_nb_lf[iter-1],v_wb_lf[iter-1],
    #         kg_phytoplankton[iter-1],kd_phytoplankton[iter-1],ke_phytoplankton[iter-1],mo_phytoplankton[iter-1],mp_phytoplankton[iter-1],km_phytoplankton[iter-1],km_zoo[iter-1],
    #         k1_phytoplankton[iter-1],k2_phytoplankton[iter-1],
    #         k1_zoo[iter-1],k2_zoo[iter-1],kd_zoo[iter-1],ke_zoo[iter-1],k1_beninv[iter-1],k2_beninv[iter-1],kd_beninv[iter-1],ke_beninv[iter-1],km_beninv[iter-1],
    #         k1_ff[iter-1],k2_ff[iter-1],kd_ff[iter-1],ke_ff[iter-1],km_ff[iter-1],k1_sf[iter-1],k2_sf[iter-1],kd_sf[iter-1],ke_sf[iter-1],km_sf[iter-1],k1_mf[iter-1],k2_mf[iter-1],kd_mf[iter-1],ke_mf[iter-1],km_mf[iter-1],k1_lf[iter-1],k2_lf[iter-1],kd_lf[iter-1],ke_lf[iter-1],km_lf[iter-1],
    #         rate_constants[iter-1]
    #         )


    cb_phytoplankton.append(kabam_obj.cb_phytoplankton)
    cb_zoo.append(kabam_obj.cb_zoo)
    cb_beninv.append(kabam_obj.cb_beninv)
    cb_ff.append(kabam_obj.cb_ff)
    cb_sf.append(kabam_obj.cb_sf)
    cb_mf.append(kabam_obj.cb_mf)
    cb_lf.append(kabam_obj.cb_lf)
    cbl_phytoplankton.append(kabam_obj.cbl_phytoplankton)
    cbl_zoo.append(kabam_obj.cbl_zoo)
    cbl_beninv.append(kabam_obj.cbl_beninv)
    cbl_ff.append(kabam_obj.cbl_ff)
    cbl_sf.append(kabam_obj.cbl_sf)
    cbl_mf.append(kabam_obj.cbl_mf)
    cbl_lf.append(kabam_obj.cbl_lf)
    cbd_zoo.append(kabam_obj.cbd_zoo)
    cbd_beninv.append(kabam_obj.cbd_beninv)
    cbd_ff.append(kabam_obj.cbd_ff)
    cbd_sf.append(kabam_obj.cbd_sf)
    cbd_mf.append(kabam_obj.cbd_mf)
    cbd_lf.append(kabam_obj.cbd_lf)
    cbr_phytoplankton.append(kabam_obj.cbr_phytoplankton)
    cbr_zoo.append(kabam_obj.cbr_zoo)
    cbr_beninv.append(kabam_obj.cbr_beninv)
    cbr_ff.append(kabam_obj.cbr_ff)
    cbr_sf.append(kabam_obj.cbr_sf)
    cbr_mf.append(kabam_obj.cbr_mf)
    cbr_lf.append(kabam_obj.cbr_lf)
    cbf_phytoplankton.append(kabam_obj.cbf_phytoplankton)
    cbf_zoo.append(kabam_obj.cbf_zoo)
    cbf_beninv.append(kabam_obj.cbf_beninv)
    cbf_ff.append(kabam_obj.cbf_ff)
    cbf_sf.append(kabam_obj.cbf_sf)
    cbf_mf.append(kabam_obj.cbf_mf)
    cbf_lf.append(kabam_obj.cbf_lf)
    cbaf_phytoplankton.append(kabam_obj.cbaf_phytoplankton)
    cbaf_zoo.append(kabam_obj.cbaf_zoo)
    cbaf_beninv.append(kabam_obj.cbaf_beninv)
    cbaf_ff.append(kabam_obj.cbaf_ff)
    cbaf_sf.append(kabam_obj.cbaf_sf)
    cbaf_mf.append(kabam_obj.cbaf_mf)
    cbaf_lf.append(kabam_obj.cbaf_lf)
    cbfl_phytoplankton.append(kabam_obj.cbfl_phytoplankton)
    cbfl_zoo.append(kabam_obj.cbfl_zoo)
    cbfl_beninv.append(kabam_obj.cbfl_beninv)
    cbfl_ff.append(kabam_obj.cbfl_ff)
    cbfl_sf.append(kabam_obj.cbfl_sf)
    cbfl_mf.append(kabam_obj.cbfl_mf)
    cbfl_lf.append(kabam_obj.cbfl_lf)
    cbafl_phytoplankton.append(kabam_obj.cbafl_phytoplankton)
    cbafl_zoo.append(kabam_obj.cbafl_zoo)
    cbafl_beninv.append(kabam_obj.cbafl_beninv)
    cbafl_ff.append(kabam_obj.cbafl_ff)
    cbafl_sf.append(kabam_obj.cbafl_sf)
    cbafl_mf.append(kabam_obj.cbafl_mf)
    cbafl_lf.append(kabam_obj.cbafl_lf)
    bmf_zoo.append(kabam_obj.bmf_zoo)
    bmf_beninv.append(kabam_obj.bmf_beninv)
    bmf_ff.append(kabam_obj.bmf_ff)
    bmf_sf.append(kabam_obj.bmf_sf)
    cbmf_mf.append(kabam_obj.cbmf_mf)
    cbmf_lf.append(kabam_obj.cbmf_lf)
    cbsafl_phytoplankton.append(kabam_obj.cbsafl_phytoplankton)
    cbsafl_zoo.append(kabam_obj.cbsafl_zoo)
    cbsafl_beninv.append(kabam_obj.cbsafl_beninv)
    cbsafl_ff.append(kabam_obj.cbsafl_ff)
    cbsafl_sf.append(kabam_obj.cbsafl_sf)
    cbsafl_mf.append(kabam_obj.cbsafl_mf)
    cbsafl_lf.append(kabam_obj.cbsafl_lf)

    if iter==0:
        acute_dose_based_m_array = np.array((kabam_obj.acute_dose_based_m))
        global acute_dose_based_m_array
        acute_dose_based_a_array = np.array((kabam_obj.acute_dose_based_a))
        global acute_dose_based_a_array
        chronic_dose_based_m_array = np.array((kabam_obj.chronic_dose_based_m))
        global chronic_dose_based_m_array
        acute_rq_dose_m_array = np.array((kabam_obj.acute_rq_dose_m))
        global acute_rq_dose_m_array
        acute_rq_dose_a_array = np.array((kabam_obj.acute_rq_dose_a))
        global acute_rq_dose_a_array
        acute_rq_diet_a_array = np.array((kabam_obj.acute_rq_diet_a))
        global acute_rq_diet_a_array
        chronic_rq_dose_m_array = np.array((kabam_obj.chronic_rq_dose_m))
        global chronic_rq_dose_m_array
        chronic_rq_diet_m_array = np.array((kabam_obj.chronic_rq_diet_m))
        global chronic_rq_diet_m_array
        chronic_rq_diet_a_array = np.array((kabam_obj.chronic_rq_diet_a))
        global chronic_rq_diet_a_array
    else:
        acute_dose_based_m_array = np.vstack((acute_dose_based_m_array,kabam_obj.acute_dose_based_m))
        acute_dose_based_a_array = np.vstack((acute_dose_based_a_array,kabam_obj.acute_dose_based_a))
        chronic_dose_based_m_array = np.vstack((chronic_dose_based_m_array,kabam_obj.chronic_dose_based_m))
        acute_rq_dose_m_array = np.vstack((acute_rq_dose_m_array,kabam_obj.acute_rq_dose_m))
        acute_rq_dose_a_array = np.vstack((acute_rq_dose_a_array,kabam_obj.acute_rq_dose_a))
        acute_rq_diet_a_array = np.vstack((acute_rq_diet_a_array,kabam_obj.acute_rq_diet_a))
        chronic_rq_dose_m_array = np.vstack((chronic_rq_dose_m_array,kabam_obj.chronic_rq_dose_m))
        chronic_rq_diet_m_array = np.vstack((chronic_rq_diet_m_array,kabam_obj.chronic_rq_diet_m))
        chronic_rq_diet_a_array = np.vstack((chronic_rq_diet_a_array,kabam_obj.chronic_rq_diet_a))

    batch_header = """
        <div class="out_">
            <br><H3>Batch Calculation of Iteration %s:</H3>
        </div>
        """%(iter)

    kabam_obj.loop_indx = str(iter)

    jid_all.append(kabam_obj.jid)
    kabam_obj_all.append(kabam_obj)    
    if iter == 0:
        jid_batch.append(kabam_obj.jid)
    html = batch_header + kabam_tables.table_all(kabam_obj)
    
    return html

def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    logger.info(header)
    i=0
    iter_html=""
    for row in reader:
        iter_html = iter_html +html_table(row,i)
        i=i+1
    sum_html = kabam_tables.table_all_sum(kabam_tables.sumheadings,kabam_tables.tmpl,l_kow,k_oc,c_wdp,water_column_EEC,mineau,x_poc,x_doc,c_ox,w_t,c_ss,oc,k_ow,
                bw_quail,bw_duck,bwb_other,avian_ld50,avian_lc50,avian_noaec,bw_rat,bwm_other,mammalian_ld50,mammalian_lc50,mammalian_chronic_endpoint,
                #Outputs
                kabam_tables.sumheadings_out,acute_dose_based_m_array,acute_dose_based_a_array,chronic_dose_based_m_array,acute_rq_dose_m_array,acute_rq_dose_a_array,acute_rq_diet_a_array,chronic_rq_dose_m_array,chronic_rq_diet_m_array,chronic_rq_diet_a_array)
    return sum_html+iter_html

              
class kabamBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['file-0']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        # html = uber_lib.SkinChk(ChkCookie)
        # html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'kabam','page':'batchinput'})
        # html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = template.render(templatepath + '04uberbatch_start.html', {
                'model':'kabam',
                'model_attributes':'Kabam Batch Output'})
        html = html + kabam_tables.timestamp("",jid_batch[0])
        html = html + iter_html
        # html = html + template.render(templatepath + 'kabam-batchoutput-jqplot.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        # html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.batch_save_dic(html, [x.__dict__ for x in kabam_obj], 'kabam', 'batch', jid_batch[0], ChkCookie, templatepath)
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', kabamBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

