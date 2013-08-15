# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:34:41 2012

@author: msnyde02
"""

# -*- coding: utf-8 -*-


import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from kabam import Kabamdb
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
import math

cgitb.enable()


# calculate Fraction of freely dissolved in water column
def phi_f(x_poc, x_doc, k_ow):
    x_poc=float(x_poc)
    x_doc=float(x_doc)
    k_ow=float(k_ow)
    phi =  1 / (1 + (x_poc*0.35*k_ow) + (x_doc*0.08*k_ow))
    return phi
#calculate concentration of chemical in sediment    
def c_s_f(c_wdp, k_oc, oc):
    c_soc=c_soc_f(c_wdp, k_oc)
    oc=float(oc)
    c_wdp=float(c_wdp)
    k_oc=float(k_oc)
    c_soc=c_soc_f(c_wdp, k_oc)
    return c_soc*oc
#normalized pesticide concentration in sediment    
def c_soc_f(c_wdp, k_oc):
    c_wdp=float(c_wdp)
    k_oc=float(k_oc)
    return c_wdp*k_oc    
# water freely dissolved
def water_d(x_poc, x_doc, k_ow, c_wto):
    phi = phi_f(x_poc, x_doc, k_ow)
    water_d = phi * c_wto * 1000000   
    return water_d
    
#determine input for rate constants user input or calculated

# calculate values
#############phytoplankton

    
# phytoplankton water partition coefficient  
def k_bw_phytoplankton_f(v_lb_phytoplankton, v_nb_phytoplankton, k_ow, v_wb_phytoplankton):
    v_lb_phytoplankton=float(v_lb_phytoplankton)
    v_nb_phytoplankton=float(v_nb_phytoplankton)
    v_wb_phytoplankton=float(v_wb_phytoplankton)
    k_bw_phytoplankton = (v_lb_phytoplankton*k_ow)+(v_nb_phytoplankton*0.35*k_ow)+v_wb_phytoplankton
    return k_bw_phytoplankton
# rate constant for uptake through respiratory area
def k1_phytoplankton_f(k_ow):
    k_ow=float(k_ow)
    return 1/(6.0e-5+(5.5/k_ow))
    
#rate constant for elimination through the gills for phytoplankton  
def k2_phytoplankton_f(k_ow, k1_phytoplankton, k_bw_phytoplankton):   
    k2_phytoplankton = k1_phytoplankton/k_bw_phytoplankton
    return k2_phytoplankton
# phytoplankton pesticide tissue residue
def cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc):   
    phi = phi_f(x_poc, x_doc, k_ow)
    cb_phytoplankton = (k1_phytoplankton * (mo_phytoplankton * c_wto * phi + mp_phytoplankton * c_wdp)) / (k2_phytoplankton + ke_phytoplankton + kg_phytoplankton + km_phytoplankton)
    return cb_phytoplankton


# lipid normalized pesticide residue in phytoplankton    
def cbl_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton):    
    cb_phytoplankton = cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)
    return cb_phytoplankton / v_lb_phytoplankton
#phytoplankton total bioconcentration factor
def cbcf_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc):   
    # kd_phytoplankton = 0 #kd_phytoplankton is always = 0
    ke_phytoplankton = 0
    km_phytoplankton = 0
    kg_phytoplankton = 0
    phi = phi_f(x_poc, x_doc, k_ow)
    cbcf_phytoplankton = ((k1_phytoplankton * (mo_phytoplankton * c_wto * phi + mp_phytoplankton * c_wdp)) / (k2_phytoplankton + ke_phytoplankton + kg_phytoplankton + km_phytoplankton)) / c_wto
    return cbcf_phytoplankton
#phytoplankton lipid normalized total bioconcentration factor
def cbcfl_phytoplankton_f(v_lb_phytoplankton, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc):   
    # kd_phytoplankton = 0 #kd_phytoplankton is always = 0
    ke_phytoplankton = 0
    km_phytoplankton = 0
    kg_phytoplankton = 0
    phi = phi_f(x_poc, x_doc, k_ow) 
    cbcfl_phytoplankton = ((k1_phytoplankton * (mo_phytoplankton * c_wto * phi + mp_phytoplankton * c_wdp) / (k2_phytoplankton + ke_phytoplankton + kg_phytoplankton + km_phytoplankton))/ v_lb_phytoplankton) / (c_wto * phi)
    return cbcfl_phytoplankton
#phytoplankton bioaccumulation factor
def cbaf_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc):   
    phi = phi_f(x_poc, x_doc, k_ow)
    cbaf_phytoplankton = ((k1_phytoplankton * (mo_phytoplankton * c_wto * phi + mp_phytoplankton * c_wdp)) / (k2_phytoplankton + ke_phytoplankton + kg_phytoplankton + km_phytoplankton)) / c_wto
    return cbaf_phytoplankton
# phytoplankton lipid normalized bioaccumulation factor
def cbafl_phytoplankton_f(v_lb_phytoplankton, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc):   
    phi = phi_f(x_poc, x_doc, k_ow)
    cbafl_phytoplankton = (((k1_phytoplankton * (mo_phytoplankton * c_wto * phi + mp_phytoplankton * c_wdp)) / (k2_phytoplankton + ke_phytoplankton + kg_phytoplankton + km_phytoplankton)) / v_lb_phytoplankton )/ (c_wto * phi)
    return cbafl_phytoplankton
# phytoplankton  biota-sediment accumulation factor
def cbsafl_phytoplankton_f(k_oc, v_lb_phytoplankton, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc):   
    phi = phi_f(x_poc, x_doc, k_ow)
    c_soc = c_soc_f(c_wdp, k_oc)
    cbsafl_phytoplankton = (((k1_phytoplankton * (mo_phytoplankton * c_wto * phi + mp_phytoplankton * c_wdp)) / (k2_phytoplankton + ke_phytoplankton + kg_phytoplankton + km_phytoplankton)) / v_lb_phytoplankton )/ (c_soc)
    return cbsafl_phytoplankton   
    
##################zooplankton
# ventilation rate     
def gv_zoo_f(wb_zoo, c_ox):  
    wb_zoo = float(wb_zoo)
    c_ox = float(c_ox)
    gv_zoo = (1400 * (wb_zoo**0.65))/c_ox
    return gv_zoo

# rate constant for elimination through the gills for zooplankton
def ew_zoo_f(k_ow):
    ew_zoo = (1/(1.85+(155/k_ow)))           
    return ew_zoo

#uptake rate constant through respiratory area for phytoplankton   
def k1_zoo_f(k_ow, wb_zoo, c_ox):
    ew_zoo = ew_zoo_f(k_ow)    
    gv_zoo = gv_zoo_f(wb_zoo, c_ox) 
    k1_zoo = ((ew_zoo * gv_zoo) / wb_zoo)   
    return k1_zoo
# zooplankton water partition coefficient
def k_bw_zoo_f(v_lb_zoo, k_ow, v_nb_zoo, v_wb_zoo):
    v_lb_zoo = float(v_lb_zoo)
    v_nb_zoo = float(v_nb_zoo)
    v_wb_zoo = float(v_wb_zoo)
    k_bw_zoo = (v_lb_zoo * k_ow) + (v_nb_zoo * 0.035 * k_ow) + v_wb_zoo
    return k_bw_zoo    
# elimination rate constant through the gills for zooplankton    
def k2_zoo_f(k_bw_zoo, k1_zoo):
    k2_zoo = k1_zoo / k_bw_zoo
    return k2_zoo
# zoo plankton dietary pesticide transfer efficiency
def ed_zoo_f(k_ow):
    ed_zoo = 1 / ((.0000003) * k_ow + 2.0)
    return ed_zoo
# zooplankton feeding rate

def gd_zoo_f(wb_zoo, w_t):
    gd_zoo = 0.022 * wb_zoo**0.85 * math.exp(0.06*w_t)
    return gd_zoo
# zooplankton rate constant pesticide uptake by food ingestion
def kd_zoo_f(k_ow, wb_zoo, w_t):
    ed_zoo = ed_zoo_f(k_ow)
    gd_zoo = gd_zoo_f(wb_zoo, w_t)
    kd_zoo = ed_zoo * (gd_zoo / wb_zoo)    
    return kd_zoo

# zooplankton growth rate constant
def kg_zoo_f(wb_zoo, w_t):
    if w_t < 17.5:
        kg_zoo = 0.0005 * wb_zoo **-0.2
    else:
        kg_zoo = 0.00251 * wb_zoo **-0.2
    return kg_zoo
#overall lipid content of diet
def v_ld_zoo_f(zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton):
    v_ld_zoo = float(zoo_p_sediment) * float(s_lipid) + float(zoo_p_phyto) * float(v_lb_phytoplankton)
    return v_ld_zoo
# overall nonlipid content of diet
def v_nd_zoo_f(zoo_p_sediment, s_NLOM, zoo_p_phyto, v_nb_phytoplankton):
    v_nd_zoo = zoo_p_sediment * s_NLOM + zoo_p_phyto * v_nb_phytoplankton
    return v_nd_zoo
# overall water content of diet 
def v_wd_zoo_f(zoo_p_sediment, s_water, zoo_p_phyto, v_wb_phytoplankton):
    v_wd_zoo = zoo_p_sediment * s_water + zoo_p_phyto * v_wb_phytoplankton
    return v_wd_zoo
# egestion rate of fecal matter   
def gf_zoo_f(zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, s_water, v_wb_phytoplankton, wb_zoo, w_t):
    v_ld_zoo = v_ld_zoo_f(zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton)
    v_nd_zoo = v_nd_zoo_f(zoo_p_sediment, s_NLOM, zoo_p_phyto, v_nb_phytoplankton)
    v_wd_zoo = v_wd_zoo_f(zoo_p_sediment, s_water, zoo_p_phyto, v_wb_phytoplankton)
    gd_zoo = gd_zoo_f(wb_zoo, w_t)
    gf_zoo = (((1-.72)*v_ld_zoo)+((1-.72)*v_nd_zoo)+((1-.25)*v_wd_zoo))*gd_zoo
    #rr=zoo_p_phyto
    #if rr==0:
     #   rr==0.00000001
    #return rr
    return gf_zoo

#lipid content in gut 
def vlg_zoo_f(wb_zoo, w_t, zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, s_water, v_wb_phytoplankton):
    gd_zoo = gd_zoo_f(wb_zoo, w_t)
    gf_zoo = gf_zoo_f(zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, s_water, v_wb_phytoplankton, wb_zoo, w_t)
    v_ld_zoo = v_ld_zoo_f(zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton)
    vlg_zoo = (1-0.72) * v_ld_zoo * gd_zoo / gf_zoo
    return vlg_zoo
# non lipid content in gut    
def vng_zoo_f(zoo_p_sediment, s_NLOM, zoo_p_phyto, v_nb_phytoplankton, wb_zoo, w_t, s_lipid, v_lb_phytoplankton, s_water, v_wb_phytoplankton):
    v_nd_zoo = v_nd_zoo_f(zoo_p_sediment, s_NLOM, zoo_p_phyto, v_nb_phytoplankton)
    gd_zoo = gd_zoo_f(wb_zoo, w_t)
    gf_zoo = gf_zoo_f(zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, s_water, v_wb_phytoplankton, wb_zoo, w_t)
    vng_zoo = (1 - 0.72) * v_nd_zoo * gd_zoo / gf_zoo
    return vng_zoo
# water content in the gut
def vwg_zoo_f(zoo_p_sediment, s_water, zoo_p_phyto, v_wb_phytoplankton, wb_zoo, w_t, s_lipid, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton):
    v_wd_zoo = v_wd_zoo_f(zoo_p_sediment, s_water, zoo_p_phyto, v_wb_phytoplankton)
    gd_zoo = gd_zoo_f(wb_zoo, w_t)
    gf_zoo = gf_zoo_f(zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, s_water, v_wb_phytoplankton, wb_zoo, w_t)
    vwg_zoo = (1 - 0.25) * v_wd_zoo * gd_zoo / gf_zoo
    return vwg_zoo    
# partition coefficient of the pesticide between the gastrointenstinal track and the organism
def kgb_zoo_f(k_ow, v_lb_zoo, v_nb_zoo, wb_zoo, zoo_p_sediment, s_water, zoo_p_phyto, v_wb_phytoplankton, w_t, s_lipid, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, v_wb_zoo):
    vlg_zoo = vlg_zoo_f(wb_zoo, w_t, zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, s_water, v_wb_phytoplankton)
    vng_zoo = vng_zoo_f(zoo_p_sediment, s_NLOM, zoo_p_phyto, v_nb_phytoplankton, wb_zoo, w_t, s_lipid, v_lb_phytoplankton, s_water, v_wb_phytoplankton)
    vwg_zoo = vwg_zoo_f(zoo_p_sediment, s_water, zoo_p_phyto, v_wb_phytoplankton, wb_zoo, w_t, s_lipid, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton)
    kgb_zoo = (vlg_zoo * k_ow + vng_zoo * 0.035 * k_ow + vwg_zoo) / (v_lb_zoo * k_ow + v_nb_zoo * 0.035 * k_ow + v_wb_zoo) 
    return kgb_zoo
# dietary elimination rate constant    
def ke_zoo_f(k_ow, wb_zoo, v_lb_zoo, v_nb_zoo, zoo_p_sediment, s_lipid, s_NLOM, zoo_p_phyto, v_lb_phytoplankton, v_nb_phytoplankton, s_water, v_wb_phytoplankton, w_t, v_wb_zoo):
    ed_zoo = ed_zoo_f(k_ow)
    gf_zoo = gf_zoo_f(zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, s_water, v_wb_phytoplankton, wb_zoo, w_t)
    kgb_zoo = kgb_zoo_f(k_ow, v_lb_zoo, v_nb_zoo, wb_zoo, zoo_p_sediment, s_water, zoo_p_phyto, v_wb_phytoplankton, w_t, s_lipid, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, v_wb_zoo)
    ke_zoo = gf_zoo * ed_zoo * kgb_zoo / wb_zoo
 #   ke_zoo = zoo_p_phyto
    return ke_zoo

def diet_zoo_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto):  
    cb_phytoplankton = cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)
    c_s = c_s_f(c_wdp, k_oc, oc)    
    diet_zoo = c_s * zoo_p_sediment + cb_phytoplankton * zoo_p_phyto
    return diet_zoo
    
# zooplankton pesticide tissue residue
def cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment):
    phi = phi_f(x_poc, x_doc, k_ow)    
#    k1_zoo = k1_zoo_f(k_ow, wb_zoo, c_ox)
   # kd_zoo = kd_zoo_f(k_ow, wb_zoo, w_t)
    diet_zoo = diet_zoo_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto)
 #   k2_zoo = k2_zoo_f(k_ow,  wb_zoo, c_ox, v_nb_zoo, v_wb_zoo, v_lb_zoo)
    # ke_zoo = ke_zoo_f(k_ow, wb_zoo, v_lb_zoo, v_nb_zoo, zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, s_water, v_wb_phytoplankton, w_t, v_wb_zoo)
    kg_zoo = kg_zoo_f(wb_zoo, w_t)
    cb_zoo = (k1_zoo * (1.0 * phi * c_wto + 0 * c_wdp) + kd_zoo * diet_zoo) / (k2_zoo + ke_zoo + kg_zoo + 0)    
    return cb_zoo
# zooplankton pesticide tissue residue lipid normalized
def cbl_zoo_f(k_ow, wb_zoo, c_ox, w_t, k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, v_nb_zoo, v_wb_zoo, v_lb_zoo, zoo_p_sediment, s_lipid, zoo_p_phyto, s_NLOM, s_water):
    cb_zoo = cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment)
    cbl_zoo = cb_zoo / v_lb_zoo
    return cbl_zoo
# zooplankton pesticide concentration originating from uptake through diet k1=0    
def cbd_zoo_f(k_ow, wb_zoo, c_ox, w_t, k1_phytoplankton, kd_zoo, c_wdp, c_wto, k2_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, ke_zoo):
    phi = phi_f(x_poc, x_doc, k_ow)    
    k1_zoo = 0
    #kd_zoo = kd_zoo_f(k_ow, wb_zoo, w_t)
    diet_zoo = diet_zoo_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto)
   # k2_zoo = k2_zoo_f(k_ow,  wb_zoo, c_ox, v_nb_zoo, v_wb_zoo, v_lb_zoo)
    #ke_zoo = ke_zoo_f(k_ow, wb_zoo, v_lb_zoo, v_nb_zoo, zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, s_water, v_wb_phytoplankton, w_t, v_wb_zoo)
    kg_zoo = kg_zoo_f(wb_zoo, w_t)
    cbd_zoo = (k1_zoo * (1.0) * phi * c_wto + (0 * c_wdp) + (kd_zoo * (diet_zoo))) / (k2_zoo + ke_zoo + kg_zoo + 0)
    return cbd_zoo
# zooplankton pesticide concentration originating from uptake through respiration (kd=0)    
def cbr_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k1_zoo, k2_zoo, ke_zoo, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto):
    phi = phi_f(x_poc, x_doc, k_ow)     
    #k1_zoo = k1_zoo_f(k_ow, wb_zoo, c_ox)
    kd_zoo = 0
    diet_zoo = diet_zoo_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto)
    #k2_zoo = k2_zoo_f(k_ow,  wb_zoo, c_ox, v_nb_zoo, v_wb_zoo, v_lb_zoo)
    #ke_zoo = ke_zoo_f(k_ow, wb_zoo, v_lb_zoo, v_nb_zoo, zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, s_water, v_wb_phytoplankton, w_t, v_wb_zoo)
    kg_zoo = kg_zoo_f(wb_zoo, w_t)
    cbr_zoo = (k1_zoo * (1.0) * phi * c_wto + (0 * c_wdp) + (kd_zoo * (diet_zoo))) / (k2_zoo + ke_zoo + kg_zoo + 0)
    return cbr_zoo    
# zooplankton total bioconcentration factor
def cbf_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment):
    phi = phi_f(x_poc, x_doc, k_ow)    
    kd_zoo = 0
    ke_zoo = 0
#    km_zoo = 0 km_zoo is always = 0
    kg_zoo = 0
    diet_zoo = diet_zoo_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto)
    cbf_zoo = ((k1_zoo * (1.0 * phi * c_wto + 0 * c_wdp) + kd_zoo * diet_zoo) / (k2_zoo + ke_zoo + kg_zoo + 0)) / c_wto   
    return cbf_zoo
#zooplankton lipid normalized total bioconcentration factor
def cbfl_zoo_f(v_lb_zoo, k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment):
    phi = phi_f(x_poc, x_doc, k_ow)    
    kd_zoo = 0
    ke_zoo = 0
#    km_zoo = 0 km_zoo is always = 0
    kg_zoo = 0
    diet_zoo = diet_zoo_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto)
    cbfl_zoo = ((k1_zoo * (1.0 * phi * c_wto + 0 * c_wdp) + kd_zoo * diet_zoo) / (k2_zoo + ke_zoo + kg_zoo + 0))/ v_lb_zoo / (c_wto * phi)  
    return cbfl_zoo    
# zooplankton bioaccumulation factor
def cbaf_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_zoo = diet_zoo_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto)
    kg_zoo = kg_zoo_f(wb_zoo, w_t)
    cbaf_zoo = ((k1_zoo * (1.0 * phi * c_wto + 0 * c_wdp) + kd_zoo * diet_zoo) / (k2_zoo + ke_zoo + kg_zoo + 0)) / c_wto   
    return cbaf_zoo
# zooplankton lipid normalized bioaccumulation factor
def cbafl_zoo_f(v_lb_zoo, k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_zoo = diet_zoo_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto)
    kg_zoo = kg_zoo_f(wb_zoo, w_t)
    cbafl_zoo = (((k1_zoo * (1.0 * phi * c_wto + 0 * c_wdp) + kd_zoo * diet_zoo) / (k2_zoo + ke_zoo + kg_zoo + 0)) / v_lb_zoo) / (c_wto * phi)         
    return cbafl_zoo
    
def cbsafl_zoo_f(v_lb_zoo, k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_zoo = diet_zoo_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto)
    kg_zoo = kg_zoo_f(wb_zoo, w_t)
    c_soc = c_soc_f(c_wdp, k_oc) 
    cbsafl_zoo = (((k1_zoo * (1.0 * phi * c_wto + 0 * c_wdp) + kd_zoo * diet_zoo) / (k2_zoo + ke_zoo + kg_zoo + 0) ) / v_lb_zoo) / (c_soc)   
    return cbsafl_zoo    
# zooplankton biomagnification factor
def bmf_zoo_f(cb_zoo_v, v_lb_zoo, zoo_p_phyto, cb_phytoplankton_v, v_lb_phytoplankton):
    bmf_zoo = (cb_zoo_v / v_lb_zoo) / (zoo_p_phyto * cb_phytoplankton_v / v_lb_phytoplankton)
    return bmf_zoo
################################ benthic invertebrates
############################################################
## ventilation rate     
def gv_beninv_f(wb_beninv, c_ox):  
    wb_beninv = float(wb_beninv)
    c_ox = float(c_ox)
    gv_beninv = (1400 * ((wb_beninv**0.65)/c_ox))
    return gv_beninv

# rate constant for elimination through the gills for benthic invertebrates
def ew_beninv_f(k_ow):
    ew_beninv = (1/(1.85+(155/k_ow)))           
    return ew_beninv

#uptake rate constant through respiratory area for benthic invertebrates   
def k1_beninv_f(k_ow, wb_beninv, c_ox):
    ew_beninv = ew_beninv_f(k_ow)    
    gv_beninv = gv_beninv_f(wb_beninv, c_ox) 
    k1_beninv = ((ew_beninv * gv_beninv) / wb_beninv)   
    return k1_beninv
# benthic invertebrate water partition coefficient
def k_bw_beninv_f(v_lb_beninv, k_ow, v_nb_beninv, v_wb_beninv):
    v_lb_beninv = float(v_lb_beninv)
    v_nb_beninv = float(v_nb_beninv)
    v_wb_beninv = float(v_wb_beninv)
    k_bw_beninv = (v_lb_beninv * k_ow) + (v_nb_beninv * 0.035 * k_ow) + v_wb_beninv
    return k_bw_beninv    
# elimination rate constant through the gills for zooplankton    
def k2_beninv_f(k1_beninv, k_bw_beninv):
   # k_bw_beninv = k_bw_beninv_f(v_lb_beninv, k_ow, v_nb_beninv, v_wb_beninv)
    k2_beninv = k1_beninv / k_bw_beninv
    return k2_beninv

# zoo plankton dietary pesticide transfer efficiency
def ed_beninv_f(k_ow):
    ed_beninv = 1 / (.0000003 * k_ow + 2.0)
    return ed_beninv
# zooplankton feeding rate

def gd_beninv_f(wb_beninv, w_t):
    gd_beninv = 0.022 * wb_beninv**0.85 * math.exp(0.06*w_t)
    return gd_beninv
# zooplankton rate constant pesticide uptake by food ingestion
def kd_beninv_f(k_ow, wb_beninv, w_t):
    ed_beninv = ed_beninv_f(k_ow)
    gd_beninv = gd_beninv_f(wb_beninv, w_t)
    kd_beninv = ed_beninv * (gd_beninv / wb_beninv)    
    return kd_beninv

# benthic invertebrate growth rate constant
def kg_beninv_f(wb_beninv, w_t):
    if w_t < 17.5:
        kg_beninv = 0.0005 * wb_beninv **-0.2
    else:
        kg_beninv = 0.00251 * wb_beninv **-0.2
    return kg_beninv
    
#overall lipid content of diet
def v_ld_beninv_f(beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo):
    v_ld_beninv = float(beninv_p_sediment) * float(s_lipid) + float(beninv_p_phytoplankton) * float(v_lb_phytoplankton) + beninv_p_zooplankton * v_lb_zoo
    return v_ld_beninv
# overall nonlipid content of diet
def v_nd_beninv_f(beninv_p_sediment, s_NLOM, beninv_p_phytoplankton, v_nb_phytoplankton, beninv_p_zooplankton, v_nb_zoo):
    v_nd_beninv = beninv_p_sediment * s_NLOM + beninv_p_phytoplankton * v_nb_phytoplankton + beninv_p_zooplankton * v_nb_zoo
    return v_nd_beninv
# overall water content of diet 
def v_wd_beninv_f(beninv_p_sediment, s_water, beninv_p_phytoplankton, v_wb_phytoplankton, beninv_p_zooplankton, v_wb_zoo):
    v_wd_beninv = beninv_p_sediment * s_water + beninv_p_phytoplankton * v_wb_phytoplankton + beninv_p_zooplankton * v_wb_zoo
    return v_wd_beninv
# egestion rate of fecal matter   
def gf_beninv_f(beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t):
    v_ld_beninv = v_ld_beninv_f(beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo)
    v_nd_beninv = v_nd_beninv_f(beninv_p_sediment, s_NLOM, beninv_p_phytoplankton, v_nb_phytoplankton, beninv_p_zooplankton, v_nb_zoo)
    v_wd_beninv = v_wd_beninv_f(beninv_p_sediment, s_water, beninv_p_phytoplankton, v_wb_phytoplankton, beninv_p_zooplankton, v_wb_zoo)
    gd_beninv = gd_beninv_f(wb_beninv, w_t)
    gf_beninv = ((1-0.75)*v_ld_beninv+(1-0.75)*v_nd_beninv+(1-0.25)*v_wd_beninv)*gd_beninv
    return gf_beninv

#lipid content in gut 
def vlg_beninv_f(wb_beninv, w_t, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo):
    gd_beninv = gd_beninv_f(wb_beninv, w_t)
    gf_beninv = gf_beninv_f(beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t)
    v_ld_beninv = v_ld_beninv_f(beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo)
    vlg_beninv = (1-0.75) * v_ld_beninv * gd_beninv / gf_beninv
    return vlg_beninv
# non lipid content in gut    
def vng_beninv_f(beninv_p_sediment, s_NLOM, beninv_p_phytoplankton, v_nb_phytoplankton, beninv_p_zooplankton, v_nb_zoo, wb_beninv, w_t, s_lipid, v_lb_phytoplankton, v_lb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo):
    v_nd_beninv = v_nd_beninv_f(beninv_p_sediment, s_NLOM, beninv_p_phytoplankton, v_nb_phytoplankton, beninv_p_zooplankton, v_nb_zoo)
    gd_beninv = gd_beninv_f(wb_beninv, w_t)
    gf_beninv = gf_beninv_f(beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t)
    vng_beninv = (1 - 0.75) * v_nd_beninv * gd_beninv / gf_beninv
    return vng_beninv
# water content in the gut
def vwg_beninv_f(beninv_p_sediment, s_water, beninv_p_phytoplankton, v_wb_phytoplankton, beninv_p_zooplankton, v_wb_zoo, s_lipid, v_lb_phytoplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, wb_beninv, w_t):
    v_wd_beninv = v_wd_beninv_f(beninv_p_sediment, s_water, beninv_p_phytoplankton, v_wb_phytoplankton, beninv_p_zooplankton, v_wb_zoo)
    gd_beninv = gd_beninv_f(wb_beninv, w_t)
    gf_beninv = gf_beninv_f(beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t)
    vwg_beninv = (1 - 0.25) * v_wd_beninv * gd_beninv / gf_beninv
    return vwg_beninv    
# partition coefficient of the pesticide between the gastrointenstinal track and the organism
def kgb_beninv_f(wb_beninv, w_t, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, k_ow, v_lb_beninv, v_nb_beninv, v_wb_beninv):
    vlg_beninv = vlg_beninv_f(wb_beninv, w_t, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo)
    vng_beninv = vng_beninv_f(beninv_p_sediment, s_NLOM, beninv_p_phytoplankton, v_nb_phytoplankton, beninv_p_zooplankton, v_nb_zoo, wb_beninv, w_t, s_lipid, v_lb_phytoplankton, v_lb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo)
    vwg_beninv = vwg_beninv_f(beninv_p_sediment, s_water, beninv_p_phytoplankton, v_wb_phytoplankton, beninv_p_zooplankton, v_wb_zoo, s_lipid, v_lb_phytoplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, wb_beninv, w_t)
    kgb_beninv = (vlg_beninv * k_ow + vng_beninv * 0.035 * k_ow + vwg_beninv) / (v_lb_beninv * k_ow + v_nb_beninv * 0.035 * k_ow + v_wb_beninv) 
    return kgb_beninv    
 
# dietary elimination rate constant    
def ke_beninv_f(k_ow, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t, v_lb_beninv, v_nb_beninv, v_wb_beninv):
    ed_beninv = ed_beninv_f(k_ow)
    gf_beninv = gf_beninv_f(beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t)
    kgb_beninv = kgb_beninv_f(wb_beninv, w_t, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, k_ow, v_lb_beninv, v_nb_beninv, v_wb_beninv)
    ke_beninv = gf_beninv * ed_beninv * (kgb_beninv / wb_beninv)
    return ke_beninv
    
def diet_beninv_f(k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, c_ox, w_t, v_nb_zoo, v_wb_zoo, v_lb_zoo, s_lipid, s_NLOM, s_water, beninv_p_phytoplankton, beninv_p_zooplankton, beninv_p_sediment):  
    cb_phytoplankton = cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)
    c_s = c_s_f(c_wdp, k_oc, oc)  
    cb_zoo = cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment)
    diet_beninv = c_s * beninv_p_sediment + cb_phytoplankton * beninv_p_phytoplankton + cb_zoo * beninv_p_zooplankton
    return diet_beninv 

# benthic invertebrates pesticide tissue residue
def cb_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv):
    phi = phi_f(x_poc, x_doc, k_ow)    
    #k1_beninv = k1_beninv_f(k_ow, wb_beninv, c_ox)
    #kd_beninv = kd_beninv_f(k_ow, wb_beninv, w_t)
    diet_beninv = diet_beninv_f(k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, c_ox, w_t, v_nb_zoo, v_wb_zoo, v_lb_zoo, s_lipid, s_NLOM, s_water, beninv_p_phytoplankton, beninv_p_zooplankton, beninv_p_sediment)
    #k2_beninv = k2_beninv_f(k_ow,  wb_beninv, c_ox, v_nb_beninv, v_wb_beninv, v_lb_beninv)
    #ke_beninv = ke_beninv_f(k_ow, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t, v_lb_beninv, v_nb_beninv)
    kg_beninv = kg_beninv_f(wb_beninv, w_t)
    cb_beninv = (k1_beninv * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_beninv * diet_beninv) / (k2_beninv + ke_beninv + kg_beninv + 0)
    return cb_beninv

def cbl_beninv_f(k_ow, wb_zoo, c_ox, w_t, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, v_nb_zoo, v_wb_zoo, v_lb_zoo, zoo_p_sediment, s_lipid, zoo_p_phyto, s_NLOM, s_water, v_lb_beninv, beninv_p_zooplankton, beninv_p_phytoplankton, beninv_p_sediment, v_nb_beninv, v_wb_beninv, wb_beninv, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k1_beninv, k2_beninv, kd_beninv, ke_beninv):
    cb_beninv = cb_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv)
    cbl_beninv = cb_beninv / v_lb_beninv
    return cbl_beninv
# benthic invertebrates pesticide concentration originating from uptake through diet k1=0     
def cbd_beninv_f(x_poc, x_doc, k_ow, wb_beninv, c_ox, k1_beninv, k2_beninv, ke_beninv, kd_beninv, w_t, k1_phytoplankton, c_wdp, v_wb_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo):
    phi = phi_f(x_poc, x_doc, k_ow)    
    #kd_beninv = 0
    k1_beninv = 0
    # kd_beninv = kd_beninv_f(k_ow, wb_beninv, w_t)
    diet_beninv = diet_beninv_f(k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, c_ox, w_t, v_nb_zoo, v_wb_zoo, v_lb_zoo, s_lipid, s_NLOM, s_water, beninv_p_phytoplankton, beninv_p_zooplankton, beninv_p_sediment)
    #k2_beninv = k2_beninv_f(k_ow,  wb_beninv, c_ox, v_nb_beninv, v_wb_beninv, v_lb_beninv)
    #ke_beninv = ke_beninv_f(k_ow, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t, v_lb_beninv, v_nb_beninv)
    kg_beninv = kg_beninv_f(wb_beninv, w_t)
    cbd_beninv = (k1_beninv * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_beninv * diet_beninv) / (k2_beninv + ke_beninv + kg_beninv + 0)
    return cbd_beninv
# benthic invertebrates pesticide concentration originating from uptake through respiration (kd=0)    
def cbr_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, k1_zoo, k2_zoo, kd_zoo, ke_zoo):
    phi = phi_f(x_poc, x_doc, k_ow)    
    #k1_beninv = k1_beninv_f(k_ow, wb_beninv, c_ox)
    kd_beninv = 0
    diet_beninv = diet_beninv_f(k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, c_ox, w_t, v_nb_zoo, v_wb_zoo, v_lb_zoo, s_lipid, s_NLOM, s_water, beninv_p_phytoplankton, beninv_p_zooplankton, beninv_p_sediment)
    #k2_beninv = k2_beninv_f(k_ow,  wb_beninv, c_ox, v_nb_beninv, v_wb_beninv, v_lb_beninv)
    #ke_beninv = ke_beninv_f(k_ow, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t, v_lb_beninv, v_nb_beninv)
    kg_beninv = kg_beninv_f(wb_beninv, w_t)
    cbr_beninv = (k1_beninv * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_beninv * diet_beninv) / (k2_beninv + ke_beninv + kg_beninv + 0)
    return cbr_beninv  
#benthic invertebrate total bioconcentration factor
def cbf_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_beninv = diet_beninv_f(k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, c_ox, w_t, v_nb_zoo, v_wb_zoo, v_lb_zoo, s_lipid, s_NLOM, s_water, beninv_p_phytoplankton, beninv_p_zooplankton, beninv_p_sediment)
    kd_beninv = 0
    ke_beninv = 0
   # km_beninv = 0    is always 0
    kg_beninv = 0
    cbf_beninv = ((k1_beninv * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_beninv * diet_beninv) / (k2_beninv + ke_beninv + kg_beninv + 0)) / c_wto
    return cbf_beninv
#benthic invertebrate lipid normalized total bioconcentration factor
def cbfl_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_beninv = diet_beninv_f(k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, c_ox, w_t, v_nb_zoo, v_wb_zoo, v_lb_zoo, s_lipid, s_NLOM, s_water, beninv_p_phytoplankton, beninv_p_zooplankton, beninv_p_sediment)
    kd_beninv = 0
    ke_beninv = 0
   # km_beninv = 0    is always 0
    kg_beninv = 0
    cbfl_beninv = (((k1_beninv * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_beninv * diet_beninv))/ v_lb_beninv / (k2_beninv + ke_beninv + kg_beninv + 0)) / (c_wto * phi)
    return cbfl_beninv    
# benthic invertebrates bioaccumulation factor
def cbaf_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_beninv = diet_beninv_f(k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, c_ox, w_t, v_nb_zoo, v_wb_zoo, v_lb_zoo, s_lipid, s_NLOM, s_water, beninv_p_phytoplankton, beninv_p_zooplankton, beninv_p_sediment)
    kg_beninv = kg_beninv_f(wb_beninv, w_t)
    cbaf_beninv = ((k1_beninv * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_beninv * diet_beninv) / (k2_beninv + ke_beninv + kg_beninv + 0)) / c_wto
    return cbaf_beninv
# benthic invertebrate lipid normalized bioaccumulation factor
def cbafl_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_beninv = diet_beninv_f(k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, c_ox, w_t, v_nb_zoo, v_wb_zoo, v_lb_zoo, s_lipid, s_NLOM, s_water, beninv_p_phytoplankton, beninv_p_zooplankton, beninv_p_sediment)
    kg_beninv = kg_beninv_f(wb_beninv, w_t)
    cbafl_beninv = (((k1_beninv * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_beninv * diet_beninv) / (k2_beninv + ke_beninv + kg_beninv + 0)) / v_lb_beninv) / (c_wto * phi)
    return cbafl_beninv

def cbsafl_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_beninv = diet_beninv_f(k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, c_ox, w_t, v_nb_zoo, v_wb_zoo, v_lb_zoo, s_lipid, s_NLOM, s_water, beninv_p_phytoplankton, beninv_p_zooplankton, beninv_p_sediment)
    kg_beninv = kg_beninv_f(wb_beninv, w_t)
    c_soc = c_soc_f(c_wdp, k_oc) 
    cbsafl_beninv = (((k1_beninv * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_beninv * diet_beninv) / (k2_beninv + ke_beninv + kg_beninv + 0)) / v_lb_beninv) / (c_soc)
    return cbsafl_beninv
# benthic invertebrates biomagnification factor
def bmf_beninv_f(cb_beninv_v, v_lb_beninv, beninv_p_zooplankton, cb_zoo_v, v_lb_zoo, beninv_p_phytoplankton, cb_phytoplankton_v, v_lb_phytoplankton):
    bmf_beninv = (cb_beninv_v / v_lb_beninv) / ((beninv_p_zooplankton * cb_zoo_v / v_lb_zoo) + (beninv_p_phytoplankton * cb_phytoplankton_v / v_lb_phytoplankton))
    return bmf_beninv    
    
#####################################################
###### filter feeders
################################################
## ventilation rate     
def gv_ff_f(wb_ff, c_ox):  
    wb_ff = float(wb_ff)
    c_ox = float(c_ox)
    gv_ff = (1400.0 * ((wb_ff**0.65)/c_ox))
    return gv_ff

# rate constant for elimination through the gills for filter feeders
def ew_ff_f(k_ow):
    ew_ff = (1.0/(1.85+(155.0/k_ow)))           
    return ew_ff

#uptake rate constant through respiratory area for filter feeders   
def k1_ff_f(k_ow, wb_ff, c_ox):
    ew_ff = ew_ff_f(k_ow)    
    gv_ff = gv_ff_f(wb_ff, c_ox) 
    k1_ff = ((ew_ff * gv_ff) / wb_ff)   
    return k1_ff
# filter feeder water partition coefficient
def k_bw_ff_f(v_lb_ff, k_ow, v_nb_ff, v_wb_ff):
    v_lb_ff = float(v_lb_ff)
    v_nb_ff = float(v_nb_ff)
    v_wb_ff = float(v_wb_ff)
    k_bw_ff = (v_lb_ff * k_ow) + (v_nb_ff * 0.035 * k_ow) + v_wb_ff
    return k_bw_ff    
# elimination rate constant through the gills for filter feeders    
def k2_ff_f(k1_ff, k_bw_ff):
    k2_ff = k1_ff / k_bw_ff
    return k2_ff

# filter feeder dietary pesticide transfer efficiency
def ed_ff_f(k_ow):
    ed_ff = 1 / (.0000003 * k_ow + 2.0)
    return ed_ff
# filter feeder feeding rate
def gd_ff_f(c_ss, wb_ff, c_ox):
    c_ss = float(c_ss)
    gv_ff = gv_ff_f(wb_ff, c_ox)
    gd_ff = gv_ff * c_ss * 1
    return gd_ff
# filter feeder rate constant pesticide uptake by food ingestion
def kd_ff_f(k_ow, wb_ff, w_t, c_ss, c_ox):
    ed_ff = ed_ff_f(k_ow)
    gd_ff = gd_ff_f(c_ss, wb_ff, c_ox )
    kd_ff = ed_ff * (gd_ff / wb_ff)    
    return kd_ff

# filter feeder growth rate constant
def kg_ff_f(wb_ff, w_t):
    if w_t < 17.5:
        kg_ff = 0.0005 * wb_ff **-0.2
    else:
        kg_ff = 0.00251 * wb_ff **-0.2
    return kg_ff
    
#overall lipid content of diet
def v_ld_ff_f(ff_p_sediment, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo):
    v_ld_ff = float(ff_p_sediment) * float(s_lipid) + float(ff_p_phytoplankton) * float(v_lb_phytoplankton) + ff_p_zooplankton * v_lb_zoo
    return v_ld_ff
# overall nonlipid content of diet
def v_nd_ff_f(ff_p_sediment, s_NLOM, ff_p_phytoplankton, v_nb_phytoplankton, ff_p_zooplankton, v_nb_zoo):
    v_nd_ff = ff_p_sediment * s_NLOM + ff_p_phytoplankton * v_nb_phytoplankton + ff_p_zooplankton * v_nb_zoo
    return v_nd_ff
# overall water content of diet 
def v_wd_ff_f(ff_p_sediment, s_water, ff_p_phytoplankton, v_wb_phytoplankton, ff_p_zooplankton, v_wb_zoo):
    v_wd_ff = ff_p_sediment * s_water + ff_p_phytoplankton * v_wb_phytoplankton + ff_p_zooplankton * v_wb_zoo
    return v_wd_ff    

def gf_ff_f(c_ss, c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t):
    v_ld_ff = v_ld_ff_f(ff_p_sediment, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo)
    v_nd_ff = v_nd_ff_f(ff_p_sediment, s_NLOM, ff_p_phytoplankton, v_nb_phytoplankton, ff_p_zooplankton, v_nb_zoo)
    v_wd_ff = v_wd_ff_f(ff_p_sediment, s_water, ff_p_phytoplankton, v_wb_phytoplankton, ff_p_zooplankton, v_wb_zoo)
    gd_ff = gd_ff_f(c_ss, wb_ff, c_ox )
    gf_ff = ((1-0.75)*v_ld_ff+(1-0.75)*v_nd_ff+(1-0.25)*v_wd_ff)*gd_ff
    return gf_ff

#lipid content in gut 
def vlg_ff_f(ff_p_sediment, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, c_ss, c_ox, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t):
    v_ld_ff = v_ld_ff_f(ff_p_sediment, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo)
    gd_ff = gd_ff_f(c_ss, wb_ff, c_ox)
    gf_ff = gf_ff_f(c_ss, c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t)
    vlg_ff = (1-0.75) * v_ld_ff * gd_ff / gf_ff
    return vlg_ff
# non lipid content in gut    
def vng_ff_f(ff_p_sediment, c_ss, c_ox, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t):
    v_nd_ff = v_nd_ff_f(ff_p_sediment, s_NLOM, ff_p_phytoplankton, v_nb_phytoplankton, ff_p_zooplankton, v_nb_zoo)    
    gd_ff = gd_ff_f(c_ss, wb_ff, c_ox)
    gf_ff = gf_ff_f(c_ss, c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t)
    vng_ff = (1 - 0.75) * v_nd_ff * gd_ff / gf_ff
    return vng_ff
# water content in the gut
def vwg_ff_f(ff_p_sediment, ff_p_phytoplankton,  c_ss, c_ox, s_lipid, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t):
    v_wd_ff = v_wd_ff_f(ff_p_sediment, s_water, ff_p_phytoplankton, v_wb_phytoplankton, ff_p_zooplankton, v_wb_zoo)
    gd_ff = gd_ff_f(c_ss, wb_ff, c_ox)
    gf_ff = gf_ff_f(c_ss, c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t)
    vwg_ff = (1 - 0.25) * v_wd_ff * gd_ff / gf_ff
    return vwg_ff    

def kgb_ff_f(k_ow, ff_p_sediment, v_lb_ff, v_nb_ff, v_wb_ff, ff_p_phytoplankton,  c_ss, c_ox, s_lipid, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t):
    vlg_ff = vlg_ff_f(ff_p_sediment, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, c_ss, c_ox, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t)
    vng_ff = vng_ff_f(ff_p_sediment, c_ss, c_ox, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t)
    vwg_ff = vwg_ff_f(ff_p_sediment, ff_p_phytoplankton,  c_ss, c_ox, s_lipid, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t)
    kgb_ff = (vlg_ff * k_ow + vng_ff * 0.035 * k_ow + vwg_ff) / (v_lb_ff * k_ow + v_nb_ff * 0.035 * k_ow + v_wb_ff) 
    return kgb_ff 
 
def ke_ff_f(k_ow, ff_p_sediment, v_lb_ff, v_nb_ff, v_wb_ff, ff_p_phytoplankton,  c_ss, c_ox, s_lipid, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t):
    ed_ff = ed_ff_f(k_ow)
    gf_ff = gf_ff_f(c_ss, c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t)
    kgb_ff = kgb_ff_f(k_ow, ff_p_sediment, v_lb_ff, v_nb_ff, v_wb_ff, ff_p_phytoplankton,  c_ss, c_ox, s_lipid, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t)
    ke_ff = gf_ff * ed_ff * (kgb_ff / wb_ff)
    return ke_ff
 
def diet_ff_f(ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates):  
    cb_phytoplankton = cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)
    c_s = c_s_f(c_wdp, k_oc, oc)  
    cb_zoo = cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment)    
    cb_beninv = cb_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv)    
    diet_ff = c_s * ff_p_sediment + cb_phytoplankton * ff_p_phytoplankton + cb_zoo * ff_p_zooplankton + cb_beninv * ff_p_benthic_invertebrates
    return diet_ff 

# benthic invertebrates pesticide tissue residue
def cb_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_ff = diet_ff_f(ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
    kg_ff = kg_ff_f(wb_ff, w_t)
    cb_ff = (k1_ff * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_ff * diet_ff) / (k2_ff + ke_ff + kg_ff + 0)
    return cb_ff

def cbl_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, v_lb_ff):
    cb_ff = cb_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
    cbl_ff = cb_ff / v_lb_ff
    return cbl_ff
# benthic invertebrates pesticide concentration originating from uptake through diet k1=0     
def cbd_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates):
    k1_ff = 0    
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_ff = diet_ff_f(ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
    kg_ff = kg_ff_f(wb_ff, w_t)
    cbd_ff = (k1_ff * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_ff * diet_ff) / (k2_ff + ke_ff + kg_ff + 0)
    return cbd_ff
# benthic invertebrates pesticide concentration originating from uptake through respiration (kd=0)    
def cbr_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_ff = diet_ff_f(ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
    kg_ff = kg_ff_f(wb_ff, w_t)  
    kd_ff = 0
    cbr_ff = (k1_ff * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_ff * diet_ff) / (k2_ff + ke_ff + kg_ff + 0)
    return cbr_ff  
#filter feeder total bioconcentration factor
def cbf_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_ff = diet_ff_f(ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
    kd_ff = 0
    ke_ff = 0
  #  km_ff = 0  is always = 0  
    kg_ff = 0
    cbf_ff = ((k1_ff * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_ff * diet_ff) / (k2_ff + ke_ff + kg_ff + 0)) /c_wto
    return cbf_ff
# filter feeder lipid normalized bioconcentration factor
def cbfl_ff_f(v_lb_ff, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_ff = diet_ff_f(ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
    kd_ff = 0
    ke_ff = 0
  #  km_ff = 0  is always = 0  
    kg_ff = 0
    cbfl_ff = (((k1_ff * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_ff * diet_ff) / (k2_ff + ke_ff + kg_ff + 0))) / v_lb_ff /(c_wto * phi)
    return cbfl_ff    
# filter feeder bioaccumulation factor
def cbaf_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_ff = diet_ff_f(ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
    kg_ff = kg_ff_f(wb_ff, w_t)
    cbaf_ff = ((k1_ff * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_ff * diet_ff) / (k2_ff + ke_ff + kg_ff + 0)) / c_wto 
    return cbaf_ff
# filter feeder lipid normalized bioaccumulation factor
def cbafl_ff_f(v_lb_ff, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_ff = diet_ff_f(ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
    kg_ff = kg_ff_f(wb_ff, w_t)
    cbafl_ff = (((k1_ff * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_ff * diet_ff) / (k2_ff + ke_ff + kg_ff + 0)) / v_lb_ff) / (c_wto * phi)
    return cbafl_ff    
# filter feeder biota-sediment bioaccumulation factor
def cbsafl_ff_f(v_lb_ff, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_ff = diet_ff_f(ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
    kg_ff = kg_ff_f(wb_ff, w_t)
    c_soc = c_soc_f(c_wdp, k_oc) 
    cbsafl_ff = (((k1_ff * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_ff * diet_ff) / (k2_ff + ke_ff + kg_ff + 0)) / v_lb_ff) / (c_soc)
    return cbsafl_ff    
# filter feeder biomagnification factor
def bmf_ff_f(cb_ff_v, v_lb_ff, ff_p_benthic_invertebrates, cb_beninv_v, v_lb_beninv, ff_p_zooplankton, cb_zoo_v, v_lb_zoo, ff_p_phytoplankton, cb_phytoplankton_v, v_lb_phytoplankton):
    bmf_ff = (cb_ff_v / v_lb_ff) / ((ff_p_benthic_invertebrates * cb_beninv_v / v_lb_beninv) + (ff_p_zooplankton * cb_zoo_v / v_lb_zoo) + (ff_p_phytoplankton * cb_phytoplankton_v / v_lb_phytoplankton))
    return bmf_ff
#########################################################################
############# small fish
## ventilation rate     
def gv_sf_f(wb_sf, c_ox):  
    wb_sf = float(wb_sf)
    c_ox = float(c_ox)
    gv_sf = (1400.0 * ((wb_sf**0.65)/c_ox))
    return gv_sf

# rate constant for elimination through the gills for small fish
def ew_sf_f(k_ow):
    ew_sf = (1.0/(1.85+(155.0/k_ow)))           
    return ew_sf

#uptake rate constant through respiratory area for small fish  
def k1_sf_f(k_ow, wb_sf, c_ox):
    ew_sf = ew_sf_f(k_ow)    
    gv_sf = gv_sf_f(wb_sf, c_ox) 
    k1_sf = ((ew_sf * gv_sf) / wb_sf)   
    return k1_sf
# small fish water partition coefficient
def k_bw_sf_f(v_lb_sf, k_ow, v_nb_sf, v_wb_sf):
    v_lb_sf = float(v_lb_sf)
    v_nb_sf = float(v_nb_sf)
    v_wb_sf = float(v_wb_sf)
    k_bw_sf = (v_lb_sf * k_ow) + (v_nb_sf * 0.035 * k_ow) + v_wb_sf
    return k_bw_sf    
# elimination rate constant through the gills for small fish   
def k2_sf_f(k1_sf, k_bw_sf):
    k2_sf = k1_sf / k_bw_sf
    return k2_sf 
 # small fish dietary pesticide transfer efficiency
def ed_sf_f(k_ow):
    ed_sf = 1 / (.0000003 * k_ow + 2.0)
    return ed_sf
# small fish feeding rate
def gd_sf_f(wb_sf, w_t): 
    gd_sf = 0.022 * wb_sf **0.85 * math.exp(0.06*w_t)
    return gd_sf
# small fish rate constant pesticide uptake by food ingestion
def kd_sf_f(k_ow, wb_sf, w_t, c_ss, c_ox):
    ed_sf = ed_sf_f(k_ow)
    gd_sf = gd_sf_f(wb_sf, w_t)
    kd_sf = ed_sf * gd_sf / wb_sf  
    return kd_sf

# small fish growth rate constant
def kg_sf_f(wb_sf, w_t):
    if w_t < 17.5:
        kg_sf = 0.0005 * wb_sf **-0.2
    else:
        kg_sf = 0.00251 * wb_sf **-0.2
    return kg_sf   
    
#overall lipid content of diet
def v_ld_sf_f(sf_p_sediment, s_lipid, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff):
    v_ld_sf = sf_p_sediment * s_lipid + sf_p_phytoplankton * v_lb_phytoplankton + sf_p_benthic_invertebrates * v_lb_beninv + sf_p_zooplankton * v_lb_zoo + sf_p_filter_feeders * v_lb_ff
    return v_ld_sf
# overall nonlipid content of diet
def v_nd_sf_f(sf_p_sediment, s_NLOM, sf_p_phytoplankton, v_nb_phytoplankton, sf_p_benthic_invertebrates, v_nb_beninv, sf_p_zooplankton, v_nb_zoo, sf_p_filter_feeders, v_nb_ff):
    v_nd_sf = sf_p_sediment * s_NLOM + sf_p_phytoplankton * v_nb_phytoplankton + sf_p_benthic_invertebrates * v_nb_beninv + sf_p_zooplankton * v_nb_zoo + sf_p_filter_feeders * v_nb_ff
    return v_nd_sf
# overall water content of diet 
def v_wd_sf_f(sf_p_sediment, s_water, sf_p_phytoplankton, v_wb_phytoplankton, sf_p_benthic_invertebrates, v_wb_beninv, sf_p_zooplankton, v_wb_zoo, sf_p_filter_feeders, v_wb_ff):   
    v_wd_sf = sf_p_sediment * s_water + sf_p_phytoplankton * v_wb_phytoplankton + sf_p_benthic_invertebrates * v_wb_beninv + sf_p_zooplankton * v_wb_zoo + sf_p_filter_feeders * v_wb_ff
    return v_wd_sf   
    
def gf_sf_f(s_lipid, s_NLOM, wb_sf, w_t, s_water, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff):
    v_ld_sf = v_ld_sf_f(sf_p_sediment, s_lipid, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff)    
    v_nd_sf = v_nd_sf_f(sf_p_sediment, s_NLOM, sf_p_phytoplankton, v_nb_phytoplankton, sf_p_benthic_invertebrates, v_nb_beninv, sf_p_zooplankton, v_nb_zoo, sf_p_filter_feeders, v_nb_ff)
    v_wd_sf = v_wd_sf_f(sf_p_sediment, s_water, sf_p_phytoplankton, v_wb_phytoplankton, sf_p_benthic_invertebrates, v_wb_beninv, sf_p_zooplankton, v_wb_zoo, sf_p_filter_feeders, v_wb_ff)
    gd_sf = gd_sf_f(wb_sf, w_t )
    gf_sf = ((1-0.92)*v_ld_sf+(1-0.6)*v_nd_sf+(1-0.25)*v_wd_sf)*gd_sf
    return gf_sf
 
#lipid content in gut 
def vlg_sf_f(s_NLOM, s_lipid, wb_sf, w_t, s_water, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff,  v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff):
    v_ld_sf = v_ld_sf_f(sf_p_sediment, s_lipid, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff)
    gd_sf = gd_sf_f(wb_sf, w_t)
    gf_sf = gf_sf_f(s_lipid, s_NLOM, wb_sf, w_t, s_water, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff)
    vlg_sf = (1-0.92) * v_ld_sf * gd_sf / gf_sf
    return vlg_sf
# non lipid content in gut    
def vng_sf_f(c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, ff_p_zooplankton, s_NLOM,  v_nb_phytoplankton, v_nb_zoo,  v_wb_phytoplankton, v_wb_zoo, c_ss, wb_ff,  wb_sf, w_t, s_water, v_nb_beninv, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff, v_wb_ff, v_wb_beninv):
    v_nd_sf = v_nd_sf_f(sf_p_sediment, s_NLOM, sf_p_phytoplankton, v_nb_phytoplankton, sf_p_benthic_invertebrates, v_nb_beninv, sf_p_zooplankton, v_nb_zoo, sf_p_filter_feeders, v_nb_ff)    
    gd_sf = gd_sf_f(wb_sf, w_t)
    gf_sf = gf_sf_f(s_lipid, s_NLOM, wb_sf, w_t, s_water, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff)
    vng_sf = (1 - 0.6) * v_nd_sf * gd_sf / gf_sf
    return vng_sf
# water content in the gut
def vwg_sf_f(s_lipid, s_water, s_NLOM, v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo, v_lb_ff, wb_sf, w_t, sf_p_sediment, sf_p_phytoplankton, v_wb_phytoplankton, sf_p_benthic_invertebrates, v_wb_beninv, v_wb_zoo, sf_p_zooplankton,  sf_p_filter_feeders, v_wb_ff):
    v_wd_sf = v_wd_sf_f(sf_p_sediment, s_water, sf_p_phytoplankton, v_wb_phytoplankton, sf_p_benthic_invertebrates, v_wb_beninv, sf_p_zooplankton, v_wb_zoo, sf_p_filter_feeders, v_wb_ff)
    gd_sf = gd_sf_f(wb_sf, w_t)
    gf_sf = gf_sf_f(s_lipid, s_NLOM, wb_sf, w_t, s_water, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff)
    vwg_sf = (1 - 0.25) * v_wd_sf * gd_sf / gf_sf
    return vwg_sf  

def kgb_sf_f(k_ow, v_lb_sf, v_nb_sf, v_wb_sf, c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, ff_p_zooplankton, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, c_ss, wb_ff,  wb_sf, w_t, v_nb_beninv, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff, v_wb_ff, v_wb_beninv):
    vlg_sf = vlg_sf_f(s_NLOM, s_lipid, wb_sf, w_t, s_water, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff,  v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff)
    vng_sf = vng_sf_f(c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, ff_p_zooplankton, s_NLOM,  v_nb_phytoplankton, v_nb_zoo,  v_wb_phytoplankton, v_wb_zoo, c_ss, wb_ff,  wb_sf, w_t, s_water,  v_nb_beninv, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff, v_wb_ff, v_wb_beninv)
    vwg_sf = vwg_sf_f(s_lipid, s_water, s_NLOM, v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo, v_lb_ff, wb_sf, w_t, sf_p_sediment, sf_p_phytoplankton, v_wb_phytoplankton, sf_p_benthic_invertebrates, v_wb_beninv, v_wb_zoo, sf_p_zooplankton, sf_p_filter_feeders, v_wb_ff)
    kgb_sf = (vlg_sf * k_ow + vng_sf * 0.035 * k_ow + vwg_sf) / (v_lb_sf * k_ow + v_nb_sf * 0.035 * k_ow + v_wb_sf) 
    return kgb_sf 

def ke_sf_f(k_ow, v_lb_sf, v_nb_sf, v_wb_sf, c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, ff_p_zooplankton, s_NLOM, v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, c_ss, wb_ff,  wb_sf, w_t, v_nb_beninv, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, v_wb_beninv, v_wb_ff, sf_p_filter_feeders, v_lb_ff):
    ed_sf = ed_sf_f(k_ow)
    gf_sf = gf_sf_f(s_lipid, s_NLOM, wb_sf, w_t, s_water, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff)
    kgb_sf = kgb_sf_f(k_ow, v_lb_sf, v_nb_sf, v_wb_sf, c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, ff_p_zooplankton, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, c_ss, wb_ff,  wb_sf, w_t, v_nb_beninv, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff, v_wb_ff, v_wb_beninv)
    ke_sf = gf_sf * ed_sf * (kgb_sf / wb_sf)
    return ke_sf

def diet_sf_f(sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):  
    cb_phytoplankton = cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)
    c_s = c_s_f(c_wdp, k_oc, oc)  
    cb_zoo = cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment)    
    cb_beninv = cb_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv)    
    cb_ff = cb_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)    
    diet_sf = c_s * sf_p_sediment + cb_phytoplankton * sf_p_phytoplankton + cb_zoo * sf_p_zooplankton + cb_beninv * sf_p_benthic_invertebrates + cb_ff * sf_p_filter_feeders
    return diet_sf

 # small fish pesticide tissue residue
def cb_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_sf = diet_sf_f(sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_sf = kg_sf_f(wb_sf, w_t)
    cb_sf = (k1_sf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_sf * diet_sf) / (k2_sf + ke_sf + kg_sf + 0)
    return cb_sf
# small fish lipid normalized pesticide tissue residue
def cbl_sf_f(v_lb_sf, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    cb_sf = cb_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    cbl_sf = cb_sf / v_lb_sf
    return cbl_sf
# small fish pesticide concentration originating from uptake through diet k1=0     
def cbd_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    k1_sf = 0    
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_sf = diet_sf_f(sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_sf = kg_sf_f(wb_sf, w_t)
    cbd_sf = (k1_sf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_sf * diet_sf) / (k2_sf + ke_sf + kg_sf + 0)
    return cbd_sf
# small fish pesticide concentration originating from uptake through respiration (kd=0)    
def cbr_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_sf = diet_sf_f(sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_sf = kg_sf_f(wb_sf, w_t) 
    kd_sf = 0
    cbr_sf = (k1_sf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_sf * diet_sf) / (k2_sf + ke_sf + kg_sf + 0)
    return cbr_sf  
#small fish total bioconcentration factor
def cbf_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_sf = diet_sf_f(sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kd_sf = 0
    ke_sf = 0
#    km_sf = 0 always = 0
    kg_sf = 0
    cbf_sf = ((k1_sf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_sf * diet_sf) / (k2_sf + ke_sf + kg_sf + 0)) / c_wto
    return cbf_sf    
# small fish lipid normalized bioconcentration factor
def cbfl_sf_f(v_lb_sf, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_sf = diet_sf_f(sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kd_sf = 0
    ke_sf = 0
#    km_sf = 0 always = 0
    kg_sf = 0
    cbfl_sf = (((k1_sf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_sf * diet_sf) / (k2_sf + ke_sf + kg_sf + 0)) / v_lb_sf) / (c_wto * phi)
    return cbfl_sf     
# small fish bioaccumulation factor
def cbaf_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_sf = diet_sf_f(sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_sf = kg_sf_f(wb_sf, w_t)
    cbaf_sf = ((k1_sf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_sf * diet_sf) / (k2_sf + ke_sf + kg_sf + 0)) / c_wto
    return cbaf_sf    
# small fish lipid normalized bioaccumulation factor
def cbafl_sf_f(v_lb_sf, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_sf = diet_sf_f(sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_sf = kg_sf_f(wb_sf, w_t)
    cbafl_sf = (((k1_sf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_sf * diet_sf) / (k2_sf + ke_sf + kg_sf + 0)) / v_lb_sf) / (c_wto * phi)
    return cbafl_sf      
def cbsafl_sf_f(v_lb_sf, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_sf = diet_sf_f(sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_sf = kg_sf_f(wb_sf, w_t)
    c_soc = c_soc_f(c_wdp, k_oc)
    cbsafl_sf = (((k1_sf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_sf * diet_sf) / (k2_sf + ke_sf + kg_sf + 0)) / v_lb_sf) / (c_soc)
    return cbsafl_sf   
# small fish biomagnification factor
def bmf_sf_f(cb_sf_v, v_lb_sf, sf_p_filter_feeders, cb_ff_v,v_lb_ff, sf_p_benthic_invertebrates, cb_beninv_v, v_lb_beninv, sf_p_zooplankton, cb_zoo_v, v_lb_zoo, sf_p_phytoplankton, cb_phytoplankton_v, v_lb_phytoplankton):
    bmf_sf = (cb_sf_v / v_lb_sf) / ((sf_p_filter_feeders * cb_ff_v / v_lb_ff) + (sf_p_benthic_invertebrates * cb_beninv_v / v_lb_beninv) + (sf_p_zooplankton * cb_zoo_v / v_lb_zoo) + (sf_p_phytoplankton * cb_phytoplankton_v / v_lb_phytoplankton))
    return bmf_sf
       
###########################################################################################
############ medium fish
## ventilation rate     
def gv_mf_f(wb_mf, c_ox):  
    wb_mf = float(wb_mf)
    c_ox = float(c_ox)
    gv_mf = (1400.0 * ((wb_mf**0.65)/c_ox))
    return gv_mf

# rate constant for elimination through the gills for medium fish
def ew_mf_f(k_ow):
    ew_mf = (1.0/(1.85+(155.0/k_ow)))           
    return ew_mf

#uptake rate constant through respiratory area for medium fish  
def k1_mf_f(k_ow, wb_mf, c_ox):
    ew_mf = ew_mf_f(k_ow)    
    gv_mf = gv_mf_f(wb_mf, c_ox) 
    k1_mf = ((ew_mf * gv_mf) / wb_mf)   
    return k1_mf
# medium fish water partition coefficient
def k_bw_mf_f(v_lb_mf, k_ow, v_nb_mf, v_wb_mf):
    v_lb_mf = float(v_lb_mf)
    v_nb_mf = float(v_nb_mf)
    v_wb_mf = float(v_wb_mf)
    k_bw_mf = (v_lb_mf * k_ow) + (v_nb_mf * 0.035 * k_ow) + v_wb_mf
    return k_bw_mf    
# elimination rate constant through the gills for medium fish   
def k2_mf_f(k1_mf, k_bw_mf):
    k2_mf = k1_mf / k_bw_mf
    return k2_mf 
 # medium fish dietary pesticide transfer efficiency
def ed_mf_f(k_ow):
    ed_mf = 1 / (.0000003 * k_ow + 2.0)
    return ed_mf
# medium fish feeding rate
def gd_mf_f(wb_mf, w_t): 
    gd_mf = 0.022 * wb_mf **0.85 * math.exp(0.06*w_t)
    return gd_mf
# medium fish rate constant pesticide uptake by food ingestion
def kd_mf_f(k_ow, wb_mf, w_t, c_ss, c_ox):
    ed_mf = ed_mf_f(k_ow)
    gd_mf = gd_mf_f(wb_mf, w_t)
    kd_mf = ed_mf * gd_mf / wb_mf  
    return kd_mf

# medium fish growth rate constant
def kg_mf_f(wb_mf, w_t):
    if w_t < 17.5:
        kg_mf = 0.0005 * wb_mf **-0.2
    else:
        kg_mf = 0.00251 * wb_mf **-0.2
    return kg_mf   
#overall lipid content of diet
def v_ld_mf_f(mf_p_sediment, s_lipid, mf_p_phytoplankton, v_lb_phytoplankton, mf_p_benthic_invertebrates, v_lb_beninv, mf_p_zooplankton, v_lb_zoo, mf_p_filter_feeders, v_lb_ff, mf_p_small_fish, v_lb_sf):
    v_ld_mf = mf_p_sediment * s_lipid + mf_p_phytoplankton * v_lb_phytoplankton + mf_p_benthic_invertebrates * v_lb_beninv + mf_p_zooplankton * v_lb_zoo + mf_p_filter_feeders * v_lb_ff + mf_p_small_fish * v_lb_sf
    return v_ld_mf
# overall nonlipid content of diet
def v_nd_mf_f(mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf):
    v_nd_mf = mf_p_sediment * s_NLOM + mf_p_phytoplankton * v_nb_phytoplankton + mf_p_benthic_invertebrates * v_nb_beninv + mf_p_zooplankton * v_nb_zoo + mf_p_filter_feeders * v_nb_ff + mf_p_small_fish * v_nb_sf
    return v_nd_mf
# overall water content of diet 
def v_wd_mf_f(mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf):   
    v_wd_mf = mf_p_sediment * s_water + mf_p_phytoplankton * v_wb_phytoplankton + mf_p_benthic_invertebrates * v_wb_beninv + mf_p_zooplankton * v_wb_zoo + mf_p_filter_feeders * v_wb_ff + mf_p_small_fish * v_wb_sf
    return v_wd_mf   
def gf_mf_f(wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf):
    v_ld_mf = v_ld_mf_f(mf_p_sediment, s_lipid, mf_p_phytoplankton, v_lb_phytoplankton, mf_p_benthic_invertebrates, v_lb_beninv, mf_p_zooplankton, v_lb_zoo, mf_p_filter_feeders, v_lb_ff, mf_p_small_fish, v_lb_sf)    
    v_nd_mf = v_nd_mf_f(mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf)
    v_wd_mf = v_wd_mf_f(mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
    gd_mf = gd_mf_f(wb_mf, w_t)
    gf_mf = ((1-0.92)*v_ld_mf+(1-0.6)*v_nd_mf+(1-0.25)*v_wd_mf)*gd_mf
    return gf_mf

#lipid content in gut 
def vlg_mf_f(wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf):
    v_ld_mf = v_ld_mf_f(mf_p_sediment, s_lipid, mf_p_phytoplankton, v_lb_phytoplankton, mf_p_benthic_invertebrates, v_lb_beninv, mf_p_zooplankton, v_lb_zoo, mf_p_filter_feeders, v_lb_ff, mf_p_small_fish, v_lb_sf)
    gd_mf = gd_mf_f(wb_mf, w_t)
    gf_mf = gf_mf_f(wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
    vlg_mf = (1-0.92) * v_ld_mf * gd_mf / gf_mf
    return vlg_mf
# non lipid content in gut    
def vng_mf_f(s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_water, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_wb_sf, wb_mf, w_t, mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf):
    v_nd_mf = v_nd_mf_f(mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf)    
    gd_mf = gd_mf_f(wb_mf, w_t)
    gf_mf = gf_mf_f(wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
    vng_mf = (1 - 0.6) * v_nd_mf * gd_mf / gf_mf
    return vng_mf
# water content in the gut
def vwg_mf_f(wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf):
    v_wd_mf = v_wd_mf_f(mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
    gd_mf = gd_mf_f(wb_mf, w_t)
    gf_mf = gf_mf_f(wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
    vwg_mf = (1 - 0.25) * v_wd_mf * gd_mf / gf_mf
    return vwg_mf  

def kgb_mf_f(k_ow, v_lb_mf, v_nb_mf, v_wb_mf, wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf):
    vlg_mf = vlg_mf_f(wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
    vng_mf = vng_mf_f(s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_water, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_wb_sf, wb_mf, w_t, mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf)
    vwg_mf = vwg_mf_f(wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
    kgb_mf = (vlg_mf * k_ow + vng_mf * 0.035 * k_ow + vwg_mf) / (v_lb_mf * k_ow + v_nb_mf * 0.035 * k_ow + v_wb_mf) 
    return kgb_mf 

def ke_mf_f(k_ow, v_lb_mf, v_nb_mf, v_wb_mf, wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf):
    ed_mf = ed_mf_f(k_ow) 
    gf_mf = gf_mf_f(wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
    kgb_mf = kgb_mf_f(k_ow, v_lb_mf, v_nb_mf, v_wb_mf, wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
    ke_mf = gf_mf * ed_mf * (kgb_mf / wb_mf)
    return ke_mf

def diet_mf_f(mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):  
    cb_phytoplankton = cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)
    c_s = c_s_f(c_wdp, k_oc, oc)  
    cb_zoo = cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment)    
    cb_beninv = cb_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv)    
    cb_ff = cb_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)    
    cb_sf = cb_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    diet_mf = c_s * mf_p_sediment + cb_phytoplankton * mf_p_phytoplankton + cb_zoo * mf_p_zooplankton + cb_beninv * mf_p_benthic_invertebrates + cb_ff * mf_p_filter_feeders + cb_sf * mf_p_small_fish
    return diet_mf

 # medium fish pesticide tissue residue
def cb_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_mf = diet_mf_f(mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)  
    kg_mf = kg_mf_f(wb_mf, w_t)
    cb_mf = (k1_mf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_mf * diet_mf) / (k2_mf + ke_mf + kg_mf + 0)
    return cb_mf
# medium fish lipid normalized pesticide tissue residue
def cbl_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders, v_lb_mf):
    cb_mf = cb_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    cbl_mf = cb_mf / v_lb_mf
    return cbl_mf
# medium fish pesticide concentration originating from uptake through diet k1=0     
def cbd_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    k1_mf = 0    
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_mf = diet_mf_f(mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)  
    kg_mf = kg_mf_f(wb_mf, w_t)
    cbd_mf = (k1_mf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_mf * diet_mf) / (k2_mf + ke_mf + kg_mf + 0)
    return cbd_mf
# medium fish pesticide concentration originating from uptake through respiration (kd=0)    
def cbr_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):   
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_mf = diet_mf_f(mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)  
    kg_mf = kg_mf_f(wb_mf, w_t)
    kd_mf = 0
    cbr_mf = (k1_mf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_mf * diet_mf) / (k2_mf + ke_mf + kg_mf + 0)
    return cbr_mf  
# medium fish total bioconcentration factor
def cbf_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_mf = diet_mf_f(mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)  
    kd_mf = 0
    ke_mf = 0    
    # km_mf = 0    
    kg_mf = 0
    cbf_mf = ((k1_mf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_mf * diet_mf) / (k2_mf + ke_mf + kg_mf + 0)) / c_wto
    return cbf_mf
# medium fish lipid normalized bioconcentration factor
def cbfl_mf_f(v_lb_mf, k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_mf = diet_mf_f(mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)  
    kd_mf = 0
    ke_mf = 0    
    # km_mf = 0    
    kg_mf = 0
    cbfl_mf = ((((k1_mf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_mf * diet_mf) / (k2_mf + ke_mf + kg_mf + 0))) / v_lb_mf) / (c_wto * phi)
    return cbfl_mf    
# medium fish bioaccumulation factor
def cbaf_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_mf = diet_mf_f(mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)  
    kg_mf = kg_mf_f(wb_mf, w_t)
    cbaf_mf = ((k1_mf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_mf * diet_mf) / (k2_mf + ke_mf + kg_mf + 0)) / c_wto
    return cbaf_mf    
# medium fish lipid normalized factor
def cbafl_mf_f(v_lb_mf, k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_mf = diet_mf_f(mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)  
    kg_mf = kg_mf_f(wb_mf, w_t)
    cbafl_mf = (((k1_mf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_mf * diet_mf) / (k2_mf + ke_mf + kg_mf + 0)) / v_lb_mf) / (c_wto * phi)
    return cbafl_mf     
def cbsafl_mf_f(v_lb_mf, k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_mf = diet_mf_f(mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)  
    kg_mf = kg_mf_f(wb_mf, w_t)
    c_soc = c_soc_f(c_wdp, k_oc)
    cbsafl_mf = (((k1_mf * (0.95 * phi * c_wto + 0.05 * c_wdp) + kd_mf * diet_mf) / (k2_mf + ke_mf + kg_mf + 0)) / v_lb_mf) / (c_soc)
    return cbsafl_mf
# medium fish biomagnification factor
def cbmf_mf_f(cb_mf_v, v_lb_mf, mf_p_small_fish, cb_sf_v, v_lb_sf, mf_p_filter_feeders, cb_ff_v, v_lb_ff, mf_p_benthic_invertebrates, cb_beninv_v, v_lb_beninv, mf_p_zooplankton, cb_zoo_v, v_lb_zoo, mf_p_phytoplankton, cb_phytoplankton_v, v_lb_phytoplankton):
    cbmf_mf = (cb_mf_v / v_lb_mf) / ((mf_p_small_fish * cb_sf_v / v_lb_sf) + (mf_p_filter_feeders * cb_ff_v / v_lb_ff) + (mf_p_benthic_invertebrates * cb_beninv_v / v_lb_beninv) + (mf_p_zooplankton * cb_zoo_v / v_lb_zoo) + (mf_p_phytoplankton * cb_phytoplankton_v / v_lb_phytoplankton)) 
    return cbmf_mf    
###########################################################################################
############ large fish
## ventilation rate     
def gv_lf_f(wb_lf, c_ox):  
    wb_lf = float(wb_lf)
    c_ox = float(c_ox)
    gv_lf = (1400.0 * ((wb_lf**0.65)/c_ox))
    return gv_lf

# rate constant for elimination through the gills for large fish
def ew_lf_f(k_ow):
    ew_lf = (1.0/(1.85+(155.0/k_ow)))           
    return ew_lf

#uptake rate constant through respiratory area for large fish  
def k1_lf_f(k_ow, wb_lf, c_ox):
    ew_lf = ew_lf_f(k_ow)    
    gv_lf = gv_lf_f(wb_lf, c_ox) 
    k1_lf = ((ew_lf * gv_lf) / wb_lf)   
    return k1_lf
# large fish water partition coefficient
def k_bw_lf_f(v_lb_lf, k_ow, v_nb_lf, v_wb_lf):
    v_lb_lf = float(v_lb_lf)
    v_nb_lf = float(v_nb_lf)
    v_wb_lf = float(v_wb_lf)
    k_bw_lf = (v_lb_lf * k_ow) + (v_nb_lf * 0.035 * k_ow) + v_wb_lf
    return k_bw_lf    
# elimination rate constant through the gills for large fish   
def k2_lf_f(k1_lf, k_bw_lf):
    k2_lf = k1_lf / k_bw_lf
    return k2_lf 
 # large fish dietary pesticide transfer efficiency
def ed_lf_f(k_ow):
    ed_lf = 1 / (.0000003 * k_ow + 2.0)
    return ed_lf
# large fish feeding rate
def gd_lf_f(wb_lf, w_t): 
    gd_lf = 0.022 * wb_lf **0.85 * math.exp(0.06*w_t)
    return gd_lf
# large fish rate constant pesticide uptake by food ingestion
def kd_lf_f(k_ow, wb_lf, w_t, c_ss, c_ox):
    ed_lf = ed_lf_f(k_ow)
    gd_lf = gd_lf_f(wb_lf, w_t)
    kd_lf = ed_lf * gd_lf / wb_lf  
    return kd_lf
# medium fish growth rate constant
def kg_lf_f(wb_lf, w_t):
    if w_t < 17.5:
        kg_lf = 0.0005 * wb_lf **-0.2
    else:
        kg_lf = 0.00251 * wb_lf **-0.2
    return kg_lf   

#overall lipid content of diet
def v_ld_lf_f(lf_p_sediment, s_lipid, lf_p_phytoplankton, v_lb_phytoplankton, lf_p_benthic_invertebrates, v_lb_beninv, lf_p_zooplankton, v_lb_zoo, lf_p_filter_feeders, v_lb_ff, lf_p_small_fish, v_lb_sf, lf_p_medium_fish, v_lb_mf):
    v_ld_lf = lf_p_sediment * s_lipid + lf_p_phytoplankton * v_lb_phytoplankton + lf_p_benthic_invertebrates * v_lb_beninv + lf_p_zooplankton * v_lb_zoo + lf_p_filter_feeders * v_lb_ff + lf_p_small_fish * v_lb_sf + lf_p_medium_fish * v_lb_mf
    return v_ld_lf
# overall nonlipid content of diet
def v_nd_lf_f(lf_p_sediment, s_NLOM, lf_p_phytoplankton, v_nb_phytoplankton, lf_p_benthic_invertebrates, v_nb_beninv, lf_p_zooplankton, v_nb_zoo, lf_p_filter_feeders, v_nb_ff, lf_p_small_fish, v_nb_sf, lf_p_medium_fish, v_nb_mf):
    v_nd_lf = lf_p_sediment * s_NLOM + lf_p_phytoplankton * v_nb_phytoplankton + lf_p_benthic_invertebrates * v_nb_beninv + lf_p_zooplankton * v_nb_zoo + lf_p_filter_feeders * v_nb_ff + lf_p_small_fish * v_nb_sf + lf_p_medium_fish * v_nb_mf
    return v_nd_lf
# overall water content of diet 
def v_wd_lf_f(lf_p_sediment, s_water, lf_p_phytoplankton, v_wb_phytoplankton, lf_p_benthic_invertebrates, v_wb_beninv, lf_p_zooplankton, v_wb_zoo, lf_p_filter_feeders, v_wb_ff, lf_p_small_fish, v_wb_sf, lf_p_medium_fish, v_wb_mf):   
    v_wd_lf = lf_p_sediment * s_water + lf_p_phytoplankton * v_wb_phytoplankton + lf_p_benthic_invertebrates * v_wb_beninv + lf_p_zooplankton * v_wb_zoo + lf_p_filter_feeders * v_wb_ff + lf_p_small_fish * v_wb_sf + lf_p_medium_fish * v_wb_mf
    return v_wd_lf   

def gf_lf_f(wb_lf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, lf_p_sediment, s_water, lf_p_phytoplankton, v_wb_phytoplankton, lf_p_benthic_invertebrates, v_wb_beninv, lf_p_zooplankton, v_wb_zoo, lf_p_filter_feeders, v_wb_ff, lf_p_small_fish, v_wb_sf, v_lb_mf, v_nb_mf, v_wb_mf, lf_p_medium_fish):
    v_ld_lf = v_ld_lf_f(lf_p_sediment, s_lipid, lf_p_phytoplankton, v_lb_phytoplankton, lf_p_benthic_invertebrates, v_lb_beninv, lf_p_zooplankton, v_lb_zoo, lf_p_filter_feeders, v_lb_ff, lf_p_small_fish, v_lb_sf, lf_p_medium_fish, v_lb_mf)    
    v_nd_lf = v_nd_lf_f(lf_p_sediment, s_NLOM, lf_p_phytoplankton, v_nb_phytoplankton, lf_p_benthic_invertebrates, v_nb_beninv, lf_p_zooplankton, v_nb_zoo, lf_p_filter_feeders, v_nb_ff, lf_p_small_fish, v_nb_sf, lf_p_medium_fish, v_nb_mf)
    v_wd_lf = v_wd_lf_f(lf_p_sediment, s_water, lf_p_phytoplankton, v_wb_phytoplankton, lf_p_benthic_invertebrates, v_wb_beninv, lf_p_zooplankton, v_wb_zoo, lf_p_filter_feeders, v_wb_ff, lf_p_small_fish, v_wb_sf, lf_p_medium_fish, v_wb_mf )
    gd_lf = gd_lf_f(wb_lf, w_t)
    gf_lf = ((1-0.92)*v_ld_lf+(1-0.6)*v_nd_lf+(1-0.25)*v_wd_lf)*gd_lf
    return gf_lf

#lipid content in gut 
def vlg_lf_f(lf_p_sediment, wb_lf, wb_mf, w_t, s_lipid, v_lb_phytoplankton, lf_p_phytoplankton, v_lb_beninv, lf_p_benthic_invertebrates, v_lb_zoo, lf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, v_lb_ff, v_lb_sf, s_NLOM, lf_p_medium_fish, v_lb_mf, v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_nb_mf, v_wb_phytoplankton, v_wb_mf, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf):
    v_ld_lf = v_ld_lf_f(lf_p_sediment, s_lipid, lf_p_phytoplankton, v_lb_phytoplankton, lf_p_benthic_invertebrates, v_lb_beninv, lf_p_zooplankton, v_lb_zoo, lf_p_filter_feeders, v_lb_ff, lf_p_small_fish, v_lb_sf, lf_p_medium_fish, v_lb_mf)
    gd_lf = gd_lf_f(wb_lf, w_t)
    gf_lf = gf_lf_f(wb_lf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, lf_p_sediment, s_water, lf_p_phytoplankton, v_wb_phytoplankton, lf_p_benthic_invertebrates, v_wb_beninv, lf_p_zooplankton, v_wb_zoo, lf_p_filter_feeders, v_wb_ff, lf_p_small_fish, v_wb_sf, v_lb_mf, v_nb_mf, v_wb_mf, lf_p_medium_fish)
    vlg_lf = (1-0.92) * v_ld_lf * gd_lf / gf_lf
    return vlg_lf
# non lipid content in gut    
def vng_lf_f(wb_lf, s_lipid, lf_p_sediment, v_lb_phytoplankton, lf_p_phytoplankton, v_lb_beninv, v_lb_zoo, lf_p_benthic_invertebrates, lf_p_zooplankton, lf_p_filter_feeders, v_lb_ff, v_lb_sf, lf_p_small_fish, s_water, lf_p_medium_fish, v_nb_mf, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_wb_sf, wb_mf, w_t, mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, v_lb_mf, v_wb_mf, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf):
    v_nd_lf = v_nd_lf_f(lf_p_sediment, s_NLOM, lf_p_phytoplankton, v_nb_phytoplankton, lf_p_benthic_invertebrates, v_nb_beninv, lf_p_zooplankton, v_nb_zoo, lf_p_filter_feeders, v_nb_ff, lf_p_small_fish, v_nb_sf, lf_p_medium_fish, v_nb_mf)    
    gd_lf = gd_lf_f(wb_lf, w_t)
    gf_lf = gf_lf_f(wb_lf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, lf_p_sediment, s_water, lf_p_phytoplankton, v_wb_phytoplankton, lf_p_benthic_invertebrates, v_wb_beninv, lf_p_zooplankton, v_wb_zoo, lf_p_filter_feeders, v_wb_ff, lf_p_small_fish, v_wb_sf, v_lb_mf, v_nb_mf, v_wb_mf, lf_p_medium_fish)
    vng_lf = (1 - 0.6) * v_nd_lf * gd_lf / gf_lf
    return vng_lf
# water content in the gut
def vwg_lf_f(wb_lf, wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, lf_p_phytoplankton, v_lb_zoo, lf_p_benthic_invertebrates, v_lb_ff, v_lb_sf, lf_p_zooplankton, s_NLOM, lf_p_filter_feeders, lf_p_sediment, lf_p_small_fish, v_lb_mf, v_nb_mf, lf_p_medium_fish, v_wb_mf, v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf):
    v_wd_lf = v_wd_lf_f(lf_p_sediment, s_water, lf_p_phytoplankton, v_wb_phytoplankton, lf_p_benthic_invertebrates, v_wb_beninv, lf_p_zooplankton, v_wb_zoo, lf_p_filter_feeders, v_wb_ff, lf_p_small_fish, v_wb_sf, lf_p_medium_fish, v_wb_mf)
    gd_lf = gd_lf_f(wb_lf, w_t)
    gf_lf = gf_lf_f(wb_lf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, lf_p_sediment, s_water, lf_p_phytoplankton, v_wb_phytoplankton, lf_p_benthic_invertebrates, v_wb_beninv, lf_p_zooplankton, v_wb_zoo, lf_p_filter_feeders, v_wb_ff, lf_p_small_fish, v_wb_sf, v_lb_mf, v_nb_mf, v_wb_mf, lf_p_medium_fish)
    vwg_lf = (1 - 0.25) * v_wd_lf * gd_lf / gf_lf
    return vwg_lf  

def kgb_lf_f(k_ow, v_lb_lf, v_nb_lf, v_wb_lf, wb_lf, s_lipid, lf_p_sediment, v_lb_phytoplankton, lf_p_phytoplankton, v_lb_beninv, v_lb_zoo, lf_p_benthic_invertebrates, lf_p_zooplankton, lf_p_filter_feeders, v_lb_ff, v_lb_sf, lf_p_small_fish, s_water, lf_p_medium_fish, v_nb_mf, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_wb_sf, wb_mf, w_t, mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, v_lb_mf, v_wb_mf, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf):
    vlg_lf = vlg_lf_f(lf_p_sediment, wb_lf, wb_mf, w_t, s_lipid, v_lb_phytoplankton, lf_p_phytoplankton, v_lb_beninv, lf_p_benthic_invertebrates, v_lb_zoo, lf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, v_lb_ff, v_lb_sf, s_NLOM, lf_p_medium_fish, v_lb_mf, v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_nb_mf, v_wb_phytoplankton, v_wb_mf, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
    vng_lf = vng_lf_f(wb_lf, s_lipid, lf_p_sediment, v_lb_phytoplankton, lf_p_phytoplankton, v_lb_beninv, v_lb_zoo, lf_p_benthic_invertebrates, lf_p_zooplankton, lf_p_filter_feeders, v_lb_ff, v_lb_sf, lf_p_small_fish, s_water, lf_p_medium_fish, v_nb_mf, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_wb_sf, wb_mf, w_t, mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, v_lb_mf, v_wb_mf, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf)
    vwg_lf = vwg_lf_f(wb_lf, wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, lf_p_phytoplankton, v_lb_zoo, lf_p_benthic_invertebrates, v_lb_ff, v_lb_sf, lf_p_zooplankton, s_NLOM, lf_p_filter_feeders, lf_p_sediment, lf_p_small_fish, v_lb_mf, v_nb_mf, lf_p_medium_fish, v_wb_mf, v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
    kgb_lf = (vlg_lf * k_ow + vng_lf * 0.035 * k_ow + vwg_lf) / (v_lb_lf * k_ow + v_nb_lf * 0.035 * k_ow + v_wb_lf) 
    return kgb_lf 

def ke_lf_f(k_ow, v_lb_lf, v_nb_lf, v_wb_lf, wb_lf, s_lipid, lf_p_sediment, v_lb_phytoplankton, lf_p_phytoplankton, v_lb_beninv, v_lb_zoo, lf_p_benthic_invertebrates, lf_p_zooplankton, lf_p_filter_feeders, v_lb_ff, v_lb_sf, lf_p_small_fish, s_water, lf_p_medium_fish, v_nb_mf, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_wb_sf, wb_mf, w_t, mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, v_lb_mf, v_wb_mf, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf):
    ed_lf = ed_lf_f(k_ow) 
    gf_lf = gf_lf_f(wb_lf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, lf_p_sediment, s_water, lf_p_phytoplankton, v_wb_phytoplankton, lf_p_benthic_invertebrates, v_wb_beninv, lf_p_zooplankton, v_wb_zoo, lf_p_filter_feeders, v_wb_ff, lf_p_small_fish, v_wb_sf, v_lb_mf, v_nb_mf, v_wb_mf, lf_p_medium_fish)
    kgb_lf = kgb_lf_f(k_ow, v_lb_lf, v_nb_lf, v_wb_lf, wb_lf, s_lipid, lf_p_sediment, v_lb_phytoplankton, lf_p_phytoplankton, v_lb_beninv, v_lb_zoo, lf_p_benthic_invertebrates, lf_p_zooplankton, lf_p_filter_feeders, v_lb_ff, v_lb_sf, lf_p_small_fish, s_water, lf_p_medium_fish, v_nb_mf, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_wb_sf, wb_mf, w_t, mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, v_lb_mf, v_wb_mf, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf)
    ke_lf = gf_lf * ed_lf * (kgb_lf / wb_lf)
    return ke_lf

def diet_lf_f(wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):  
    cb_phytoplankton = cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)
    c_s = c_s_f(c_wdp, k_oc, oc)  
    cb_zoo = cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment)    
    cb_beninv = cb_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv)    
    cb_ff = cb_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)    
    cb_sf = cb_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    cb_mf = cb_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)    
    diet_mf = c_s * lf_p_sediment + cb_phytoplankton * lf_p_phytoplankton + cb_zoo * lf_p_zooplankton + cb_beninv * lf_p_benthic_invertebrates + cb_ff * lf_p_filter_feeders + cb_sf * lf_p_small_fish + cb_mf * lf_p_medium_fish
    return diet_mf

 # large fish pesticide tissue residue
def cb_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_lf = diet_lf_f(wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_lf = kg_lf_f(wb_lf, w_t)
    cb_lf = (k1_lf * (1.0 * phi * c_wto + 0.00 * c_wdp) + kd_lf * diet_lf) / (k2_lf + ke_lf + kg_lf + 0)
    return cb_lf
# large fish lipid normalized pesticide tissue residue
def cbl_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, v_lb_lf, k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders, v_lb_mf):
    cb_lf = cb_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    cbl_lf = cb_lf / v_lb_lf
    return cbl_lf
# large fish pesticide concentration originating from uptake through diet k1=0     
def cbd_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_lf = diet_lf_f(wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_lf = kg_lf_f(wb_lf, w_t)
    k1_lf = 0   
    cbd_lf = (k1_lf * (1.0 * phi * c_wto + 0.0 * c_wdp) + kd_lf * diet_lf) / (k2_lf + ke_lf + kg_lf + 0)
    return cbd_lf
# large fish pesticide concentration originating from uptake through respiration (kd=0)    
def cbr_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_lf = diet_lf_f(wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_lf = kg_lf_f(wb_lf, w_t)
    kd_lf = 0
    cbr_lf = (k1_lf * (1.0 * phi * c_wto + 0.0 * c_wdp) + kd_lf * diet_lf) / (k2_lf + ke_lf + kg_lf + 0)
    return cbr_lf  
# large fish total bioconcentration factor
def cbf_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_lf = diet_lf_f(wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kd_lf = 0
    ke_lf = 0    
    #km_lf = 0    
    kg_lf = 0
    cbf_lf = ((k1_lf * (1.0 * phi * c_wto + 0.00 * c_wdp) + kd_lf * diet_lf) / (k2_lf + ke_lf + kg_lf + 0)) / c_wto
    return cbf_lf
# large fish lipid normalized total bioconcentration factor
def cbfl_lf_f(v_lb_lf, kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_lf = diet_lf_f(wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kd_lf = 0
    ke_lf = 0    
    #km_lf = 0    
    kg_lf = 0
    cbfl_lf = (((k1_lf * (1.0 * phi * c_wto + 0.00 * c_wdp) + kd_lf * diet_lf) / (k2_lf + ke_lf + kg_lf + 0)) / v_lb_lf) / (c_wto * phi)
    return cbfl_lf
# large fish bioaccumulation factor
def cbaf_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_lf = diet_lf_f(wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_lf = kg_lf_f(wb_lf, w_t)
    cbaf_lf = ((k1_lf * (1.0 * phi * c_wto + 0.00 * c_wdp) + kd_lf * diet_lf) / (k2_lf + ke_lf + kg_lf + 0)) / c_wto
    return cbaf_lf
# large fish lipid normalized bioaccumulation factor
def cbafl_lf_f(v_lb_lf, kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_lf = diet_lf_f(wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_lf = kg_lf_f(wb_lf, w_t)
    cbafl_lf = (((k1_lf * (1.0 * phi * c_wto + 0.00 * c_wdp) + kd_lf * diet_lf) / (k2_lf + ke_lf + kg_lf + 0)) / v_lb_lf) / (c_wto * phi)
    return cbafl_lf  
# large fish biota-sediment accumulation factors    
def cbsafl_lf_f(v_lb_lf, kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_lf = diet_lf_f(wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_lf = kg_lf_f(wb_lf, w_t)
    c_soc = c_soc_f(c_wdp, k_oc)
    cbsafl_lf = (((k1_lf * (1.0 * phi * c_wto + 0.00 * c_wdp) + kd_lf * diet_lf) / (k2_lf + ke_lf + kg_lf + 0)) / v_lb_lf) / (c_soc)
    return cbsafl_lf  
# large fish biomagnification factor
def cbmf_lf_f(v_lb_lf, v_lb_mf, v_lb_sf, v_lb_ff, cb_mf_v, cb_sf_v, cb_ff_v, cb_beninv_v, cb_zoo_v, cb_phytoplankton_v, kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders):
    phi = phi_f(x_poc, x_doc, k_ow)    
    diet_lf = diet_lf_f(wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
    kg_lf = kg_lf_f(wb_lf, w_t)
    cbmf_lf = (((k1_lf * (1.0 * phi * c_wto + 0.00 * c_wdp) + kd_lf * diet_lf) / (k2_lf + ke_lf + kg_lf + 0)) / v_lb_lf) / ((lf_p_medium_fish * cb_mf_v / v_lb_mf) + (lf_p_small_fish * cb_sf_v / v_lb_sf) + (lf_p_filter_feeders *cb_ff_v / v_lb_ff) + (lf_p_benthic_invertebrates * cb_beninv_v / v_lb_beninv) + (lf_p_zooplankton * cb_zoo_v / v_lb_zoo) + (lf_p_phytoplankton * cb_phytoplankton_v / v_lb_phytoplankton))
    return cbmf_lf

    
class KabamOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
  
        chemical_name = form.getvalue('name')
        l_kow = form.getvalue('lkow')
        k_oc = form.getvalue('Koc')
        c_wdp_2 = float(form.getvalue('beec'))
        c_wdp = float(form.getvalue('beec')) / 1000000
        water_column_EEC = float(form.getvalue('weec'))
        c_wto = float(water_column_EEC) / 1000000
        chemical_specific_mineau_scaling_factor = float(form.getvalue('sf'))
        x_poc = form.getvalue('cpoc')
        x_doc = form.getvalue('cdoc')
        c_ox = form.getvalue('cox')
        w_t = float(form.getvalue('wt'))
        c_ss = form.getvalue('css')
        oc = float(form.getvalue('oc'))/100
        k_ow = 10**(float(l_kow))
        species_of_the_tested_bird = form.getvalue('b_species')
        body_weight_of_the_tested_bird_quail = form.getvalue('bw_quail')
        body_weight_of_the_tested_bird_duck = form.getvalue('bw_duck')
        body_weight_of_the_tested_bird_other = form.getvalue('bwb_other')
        avian_ld50 = float(form.getvalue('ald50'))
        avian_lc50 = float(form.getvalue('alc50'))
        avian_noaec = float(form.getvalue('aNOAEC'))
        species_of_the_tested_mamm = form.getvalue('m_species')
        body_weight_of_the_tested_mamm_rat=float(form.getvalue('bw_rat'))
        body_weight_of_the_tested_mamm_other=float(form.getvalue('bwm_other'))
#        print 'weight=', body_weight_of_the_tested_mamm_other
        mammalian_ld50 = float(form.getvalue('mld50'))
        mammalian_lc50 = float(form.getvalue('mlc50'))
        mammalian_chronic_endpoint = float(form.getvalue('m_chronic'))
#        body_weight_of_the_assessed_mamm = float(form.getvalue('bw_assess_m'))
        diet_for_large_fish = form.getvalue('Diet_lfish')
        lf_p_sediment = float(form.getvalue('lfish_p_sediment'))/100
        lf_p_phytoplankton = float(form.getvalue('lfish_p_phyto'))/100
        lf_p_zooplankton = float(form.getvalue('lfish_p_zoo'))/100
        lf_p_benthic_invertebrates = float(form.getvalue('lfish_p_beninv'))/100
        lf_p_filter_feeders = float(form.getvalue('lfish_p_ff'))/100
        lf_p_small_fish = float(form.getvalue('lfish_p_sfish'))/100
        lf_p_medium_fish = float(form.getvalue('lfish_p_mfish'))/100
        diet_for_medium_fish = form.getvalue('Diet_mfish')
        mf_p_sediment = form.getvalue('mfish_p_sediment') 
        #print type(mf_p_sediment)
        mf_p_sediment = float(mf_p_sediment)
        mf_p_phytoplankton = float(form.getvalue('mfish_p_phyto'))
        mf_p_zooplankton = float(form.getvalue('mfish_p_zoo'))
        mf_p_benthic_invertebrates = float(form.getvalue('mfish_p_beninv'))/100
        mf_p_filter_feeders = float(form.getvalue('mfish_p_ff'))
        mf_p_small_fish = float(form.getvalue('mfish_p_sfish'))/100
        diet_for_small_fish = form.getvalue('Diet_sfish')
        sf_p_sediment = float(form.getvalue('sfish_p_sediment'))
        sf_p_phytoplankton = float(form.getvalue('sfish_p_phyto'))
        sf_p_zooplankton = float(form.getvalue('sfish_p_zoo'))/100
        sf_p_benthic_invertebrates = float(form.getvalue('sfish_p_beninv'))/100
        sf_p_filter_feeders = float(form.getvalue('sfish_p_ff'))
        diet_for_filter_feeder = form.getvalue('Diet_ff')
        ff_p_sediment = float(form.getvalue('ff_p_sediment'))/100
        ff_p_phytoplankton = float(form.getvalue('ff_p_phyto'))/100
        ff_p_zooplankton = float(form.getvalue('ff_p_zoo'))/100
        ff_p_benthic_invertebrates = float(form.getvalue('ff_p_beninv'))
        diet_for_invertebrates = form.getvalue('Diet_invert')
        beninv_p_sediment = float(form.getvalue('beninv_p_sediment'))/100
        beninv_p_phytoplankton = float(form.getvalue('beninv_p_phyto'))/100
        beninv_p_zooplankton = float(form.getvalue('beninv_p_zoo'))/100
        diet_for_zooplankton = form.getvalue('Diet_zoo')
        zoo_p_sediment = float(form.getvalue('zoo_p_sediment'))
        zoo_p_phyto = float(form.getvalue('zoo_p_phyto'))/100
        characteristics_sediment = form.getvalue('char_s')
        s_lipid = float(form.getvalue('s_lipid'))/100
        s_NLOM = float(form.getvalue('s_NLOM'))/100
        s_water = float(form.getvalue('s_water'))/100
        sediment_respire = form.getvalue('s_respire')
        characteristics_phytoplankton = form.getvalue('char_phyto')
        v_lb_phytoplankton = float(form.getvalue('phyto_lipid'))/100
        v_nb_phytoplankton = float(form.getvalue('phyto_NLOM'))/100
        v_wb_phytoplankton = float(form.getvalue('phyto_water'))/100
        phytoplankton_respire = form.getvalue('phyto_respire')
        characteristics_zooplankton = form.getvalue('char_zoo')
        wb_zoo = float(form.getvalue('zoo_ww'))
        v_lb_zoo = float(form.getvalue('zoo_lipid'))/100
        v_nb_zoo = float(form.getvalue('zoo_NLOM'))/100
        v_wb_zoo = float(form.getvalue('zoo_water'))/100
        zoo_respire = form.getvalue('zoo_respire')
        characteristics_benthic_invertebrates = form.getvalue('char_beninv')
        wb_beninv = float(form.getvalue('beninv_ww'))
        v_lb_beninv = float(form.getvalue('beninv_lipid'))/100
        v_nb_beninv = float(form.getvalue('beninv_NLOM'))/100
        v_wb_beninv = float(form.getvalue('beninv_water'))/100
        beninv_respire = form.getvalue('beninv_respire')
        characteristics_ff = form.getvalue('char_ff')
        wb_ff = float(form.getvalue('ff_ww'))
        v_lb_ff = float(form.getvalue('ff_lipid'))/100
        v_nb_ff = float(form.getvalue('ff_NLOM'))/100
        v_wb_ff = float(form.getvalue('ff_water'))/100
        ff_respire = form.getvalue('ff_respire')
        characteristics_smfish = form.getvalue('char_sfish')
        wb_sf = float(form.getvalue('sfish_ww'))
        v_lb_sf = float(form.getvalue('sfish_lipid'))/100
        v_nb_sf = float(form.getvalue('sfish_NLOM'))/100
        v_wb_sf = float(form.getvalue('sfish_water'))/100
        smfish_respire = form.getvalue('sfish_respire')
        characteristics_medfish = form.getvalue('char_mfish')
        wb_mf = float(form.getvalue('mfish_ww'))
        v_lb_mf = float(form.getvalue('mfish_lipid'))/100
        v_nb_mf = float(form.getvalue('mfish_NLOM'))/100
        v_wb_mf = float(form.getvalue('mfish_water'))/100
        medfish_respire = form.getvalue('mfish_respire')
        characteristics_larfish = form.getvalue('char_lfish')
        wb_lf = float(form.getvalue('lfish_ww'))
        v_lb_lf = float(form.getvalue('lfish_lipid'))/100
        v_nb_lf = float(form.getvalue('lfish_NLOM'))/100
        v_wb_lf = float(form.getvalue('lfish_water'))/100
        larfish_respire = form.getvalue('lfish_respire')
        rate_constants = form.getvalue('rate_c')
        # phytoplankton growth rate constant
        kg_phytoplankton = 0.1
        # phytoplankton diet uptake rate constant
        kd_phytoplankton=0
        #phytoplankton fecal elimination rate constant  
        ke_phytoplankton=0
        # fraction of respiratory ventilation involving overlying water
        mo_phytoplankton = 1
        # fraction of respiratory ventilation involving pore water
        mp_phytoplankton = 0    
        # rate constant for pesticide metabolic transformation
        km_phytoplankton = 0
         # rate constant for pesticide metabolic transformation
        km_zoo = 0
       
        if rate_constants == 'b': # use input values for rate constants           
            k1_phytoplankton = form.getvalue('phyto_k1')
            k2_phytoplankton = form.getvalue('phyto_k2')
            kd_phytoplankton = form.getvalue('phyto_kd')
            ke_phytoplankton = form.getvalue('phyto_ke')
            km_phytoplankton = form.getvalue('phyto_km')
            k1_zoo = form.getvalue('zoo_k1')
            k2_zoo = form.getvalue('zoo_k2')
            kd_zoo = form.getvalue('zoo_kd')
            ke_zoo = form.getvalue('zoo_ke')
            km_zoo = form.getvalue('zoo_km')
            k1_beninv = form.getvalue('beninv_k1')
            k2_beninv = form.getvalue('beninv_k2')
            kd_beninv = form.getvalue('beninv_kd')
            ke_beninv = form.getvalue('beninv_ke')
            km_beninv = form.getvalue('beninv_km')
            k1_ff = form.getvalue('ff_k1')
            k2_ff = form.getvalue('ff_k2')
            kd_ff = form.getvalue('ff_kd')
            ke_ff = form.getvalue('ff_ke')
            km_ff = form.getvalue('ff_km')
            k1_sf = form.getvalue('sfish_k1')
            k2_sf = form.getvalue('sfish_k2')
            kd_sf = form.getvalue('sfish_kd')
            ke_sf = form.getvalue('sfish_ke')
            km_sf = form.getvalue('sfish_km')
            k1_mf = form.getvalue('mfish_k1')
            k2_mf = form.getvalue('mfish_k2')
            kd_mf = form.getvalue('mfish_kd')
            ke_mf = form.getvalue('mfish_ke')
            km_mf = form.getvalue('mfish_km')
            k1_lf = form.getvalue('lfish_k1')
            k2_lf = form.getvalue('lfish_k2')
            kd_lf = form.getvalue('lfish_kd')
            ke_lf = form.getvalue('lfish_ke')
            km_lf = form.getvalue('lfish_km')

        else: # calculate values for rate constants
                k_bw_phytoplankton = k_bw_phytoplankton_f(v_lb_phytoplankton, v_nb_phytoplankton, k_ow, v_wb_phytoplankton)
                k1_phytoplankton = k1_phytoplankton_f(k_ow)
                k2_phytoplankton = k2_phytoplankton_f(k_ow, k1_phytoplankton, k_bw_phytoplankton)
                k_bw_zoo = k_bw_zoo_f(v_lb_zoo, k_ow, v_nb_zoo, v_wb_zoo)
                k1_zoo = k1_zoo_f(k_ow, wb_zoo, c_ox)
                k2_zoo = k2_zoo_f(k_bw_zoo, k1_zoo)
                kd_zoo = kd_zoo_f(k_ow, wb_zoo, w_t)               
                ke_zoo = ke_zoo_f(k_ow, wb_zoo, v_lb_zoo, v_nb_zoo, zoo_p_sediment, s_lipid, s_NLOM, zoo_p_phyto, v_lb_phytoplankton, v_nb_phytoplankton, s_water, v_wb_phytoplankton, w_t, v_wb_zoo)
                k_bw_beninv = k_bw_beninv_f(v_lb_beninv, k_ow, v_nb_beninv, v_wb_beninv)                
                k1_beninv = k1_beninv_f(k_ow, wb_beninv, c_ox)        
                k2_beninv = k2_beninv_f(k1_beninv, k_bw_beninv)                
                kd_beninv = kd_beninv_f(k_ow, wb_beninv, w_t)                
                ke_beninv = ke_beninv_f(k_ow, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t, v_lb_beninv, v_nb_beninv, v_wb_beninv)
                k_bw_ff = k_bw_ff_f(v_lb_ff, k_ow, v_nb_ff, v_wb_ff)                
                k1_ff = k1_ff_f(k_ow, wb_ff, c_ox)
                k2_ff = k2_ff_f(k1_ff, k_bw_ff)                
                kd_ff = kd_ff_f(k_ow, wb_ff, w_t, c_ss, c_ox)
                ke_ff = ke_ff_f(k_ow, ff_p_sediment, v_lb_ff, v_nb_ff, v_wb_ff, ff_p_phytoplankton,  c_ss, c_ox, s_lipid, v_lb_phytoplankton, ff_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_ff, w_t)
                k_bw_sf = k_bw_sf_f(v_lb_sf, k_ow, v_nb_sf, v_wb_sf)                
                k1_sf = k1_sf_f(k_ow, wb_sf, c_ox)
                k2_sf = k2_sf_f(k1_sf, k_bw_sf)
                kd_sf = kd_sf_f(k_ow, wb_sf, w_t, c_ss, c_ox)
                ke_sf = ke_sf_f(k_ow, v_lb_sf, v_nb_sf, v_wb_sf, c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, ff_p_zooplankton, s_NLOM, v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, c_ss, wb_ff,  wb_sf, w_t, v_nb_beninv, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, v_wb_beninv, v_wb_ff, sf_p_filter_feeders, v_lb_ff)
                k_bw_mf = k_bw_mf_f(v_lb_mf, k_ow, v_nb_mf, v_wb_mf)                
                k1_mf = k1_mf_f(k_ow, wb_mf, c_ox)
                k2_mf = k2_mf_f(k1_mf, k_bw_mf) 
                kd_mf = kd_mf_f(k_ow, wb_mf, w_t, c_ss, c_ox)
                ke_mf = ke_mf_f(k_ow, v_lb_mf, v_nb_mf, v_wb_mf, wb_mf, w_t, s_lipid, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo,  v_lb_ff, v_lb_sf, s_NLOM,  v_nb_phytoplankton, v_nb_beninv,  v_nb_zoo,  v_nb_ff, v_nb_sf, mf_p_sediment, s_water, mf_p_phytoplankton, v_wb_phytoplankton, mf_p_benthic_invertebrates, v_wb_beninv, mf_p_zooplankton, v_wb_zoo, mf_p_filter_feeders, v_wb_ff, mf_p_small_fish, v_wb_sf)
                k_bw_lf = k_bw_lf_f(v_lb_lf, k_ow, v_nb_lf, v_wb_lf)
                k1_lf = k1_lf_f(k_ow, wb_lf, c_ox)
                k2_lf = k2_lf_f(k1_lf, k_bw_lf)
                kd_lf = kd_lf_f(k_ow, wb_lf, w_t, c_ss, c_ox)
                ke_lf = ke_lf_f(k_ow, v_lb_lf, v_nb_lf, v_wb_lf, wb_lf, s_lipid, lf_p_sediment, v_lb_phytoplankton, lf_p_phytoplankton, v_lb_beninv, v_lb_zoo, lf_p_benthic_invertebrates, lf_p_zooplankton, lf_p_filter_feeders, v_lb_ff, v_lb_sf, lf_p_small_fish, s_water, lf_p_medium_fish, v_nb_mf, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_wb_sf, wb_mf, w_t, mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, v_lb_mf, v_wb_mf, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf)
        cb_phytoplankton_v = cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)   
        cb_zoo_v = cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment)
        cb_beninv_v = cb_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv)
        cb_ff_v = cb_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
        cb_sf_v = cb_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
        cb_mf_v = cb_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
        cb_lf_v = cb_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)

##########################################################################
################################## Mammals EECs     
        cb_a = np.array([[cb_phytoplankton_v, cb_zoo_v, cb_beninv_v, cb_ff_v, cb_sf_v, cb_mf_v, cb_lf_v]])
#        print cb_a       
        cb_a2 = cb_a * 1000000
#        print cb_a2
        #array of mammal weights       
        mweight= np.array([[0.018, 0.085, 0.45, 1.8, 5, 15]]) 
#        print mweight[:,0]      
        dfir = (0.0687*mweight**0.822)/mweight
#        print dfir.shape
#        print dfir[:,0]
         #creation of array for mammals of dry food ingestion rate
#        for i in mweight:
#            dfir = (.0687*i**0.822)/i
#            return dfir
#array of percent water in biota
        v_wb_a = np.array([[v_wb_phytoplankton, v_wb_zoo, v_wb_beninv, v_wb_ff, v_wb_sf, v_wb_mf, v_wb_lf]])
#array of % diet of food web for each mammal
        diet_mammal = np.array([[0, 0, 1, 0, 0, 0, 0], [0, 0, .34, .33, .33, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0,0,0,0,0,1,0], [0,0,0,0,0,1,0], [0,0,0,0,0,0,1]])
#        print type(diet_mammal)
        denom1 = diet_mammal * v_wb_a 
        denom1 = ([[ 0., 0., 0.76, 0., 0., 0., 0. ], [ 0., 0., 0.2584, 0.2805, 0.2409, 0., 0. ], [ 0., 0., 0., 0., 0., 0.73, 0. ], [ 0., 0., 0., 0., 0., 0.73, 0. ], [ 0., 0., 0., 0., 0., 0.73, 0. ], [ 0., 0., 0., 0., 0., 0., 0.73 ]])     
        denom2 = np.cumsum(denom1, axis = 1)
        denom3 =denom2[:,6] # selects out seventh row of array which is the cumulative sums of the products      
        denom4 = 1 - denom3
        #wet food ingestion rate for mammals
        wet_food_ingestion_m = dfir / denom4 
        #array of drinking water intake rate for mammals
        drinking_water_intake_m = .099 * mweight**0.9
        db1 = cb_a2 * diet_mammal
        db2 = np.cumsum(db1, axis = 1)
        db3 = db2[:,6]
        #dose based  EEC
        db4 = (db3/1000) * wet_food_ingestion_m + (water_column_EEC / 1000)*(drinking_water_intake_m/mweight)
        #dietary based EEC
        db5 = db3/1000
##########################################################################
################################## Avian EECs        
        aweight= np.array([[0.02, 6.7, 0.07, 2.9, 1.25, 7.5]]) 
        dfir_a = (0.0582*aweight**0.651)/aweight
        v_wb_a = np.array([[v_wb_phytoplankton, v_wb_zoo, v_wb_beninv, v_wb_ff, v_wb_sf, v_wb_mf, v_wb_lf]])
  
        diet_avian = np.array([[0, 0, .33, 0.33, 0.34, 0, 0], [0, 0, .33, .33, 0, 0.34, 0], [0, 0, 0.5, 0, 0.5,0,0], [0,0,0.5,0,0,0.5,0], [0,0,0,0,0,1,0], [0,0,0,0,0,0,1]])
        denom1a = diet_avian * v_wb_a  
        denom2a = np.cumsum(denom1a, axis = 1)     
        denom3a =denom2a[:,6] # selects out seventh row of array which is the cumulative sums of the products
        denom4a = 1 - denom3a
        wet_food_ingestion_a = dfir_a / denom4a
        drinking_water_intake_a = .059 * mweight**0.67
        db1a = cb_a2 * diet_avian
        db2a = np.cumsum(db1a, axis = 1)
        db3a = db2a[:,6]
        #dose based  EEC
        db4a = (db3a/1000) * wet_food_ingestion_a + (water_column_EEC / 1000)*(drinking_water_intake_a/aweight)
        #dietary based EEC
        db5a = (db3a/1000)
 
##################################### toxicity values
#################################### mammal
#dose based acute toxicity for mammals
        if species_of_the_tested_mamm == '350':
            acute_dose_based_m = mammalian_ld50 * (0.35 / mweight)**0.25
   #         return acute_dose_based_m
        else:
            acute_dose_based_m = mammalian_ld50 * (body_weight_of_the_tested_mamm_other / mweight)**0.25          
  #              return acute_dose_based_m
        #print type(acute_dose_based_m)
#dose based chronic toxicity for mammals        
        if species_of_the_tested_mamm == '350':
            chronic_dose_based_m = (mammalian_chronic_endpoint/20) * ((0.35 / mweight)**0.25)
        else:
#            body_weight_of_the_tested_mamm_other = float(body_weight_of_the_tested_mamm_other)
            chronic_dose_based_m = (mammalian_chronic_endpoint/20) * (body_weight_of_the_tested_mamm_other / mweight)**0.25
  #              return chronic_dose_based_m
#################################### avian
#dose based acute toxicity for birds
        if species_of_the_tested_bird == '178':
            acute_dose_based_a = avian_ld50 * (aweight/0.178)**(chemical_specific_mineau_scaling_factor-1)
        elif species_of_the_tested_bird == '1580':
            acute_dose_based_a = avian_ld50 * (aweight/1.58)**(chemical_specific_mineau_scaling_factor-1)
        else: 
            acute_dose_based_a = avian_ld50 * (aweight/float(body_weight_of_the_tested_bird_other))**(chemical_specific_mineau_scaling_factor-1)
  #          return acute_dose_based_a

##################################### RQ Values
################################# mammal
#RQ dose based for mammals
        acute_rq_dose_m = db4 / acute_dose_based_m
        chronic_rq_dose_m = db4 / chronic_dose_based_m
#RQ diet based for mammals
        acute_rq_diet_m = db5 / mammalian_lc50
        chronic_rq_diet_m = db5 / mammalian_chronic_endpoint
#RQ dose based for birds
        acute_rq_dose_a = db4a / acute_dose_based_a
        
#RQ diet based for birds
        acute_rq_diet_a = db5a / avian_ld50
        chronic_rq_diet_a = db5a / avian_noaec
        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'kabam','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'kabam',
                'model_attributes':'Kabam Output'})

        cb_phytoplankton_v = cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)   
        print cb_phytoplankton_v


        html = html + """
        <table border="1">
        <tr><H3>User Inputs</H3></tr>
        <tr>
        <td>Chemical Name</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Log Kow</td>
        <td>%s</td>
        <td></td>
        </tr>
        <tr>
        <td>Koc</td>
        <td>%s</td>
        <td>L/kg OC</td>
        </tr>
        <tr>
        <td>Pore water EEC</td>
        <td>%s</td>
        <td>&#956;g/L</td>
        </tr>
        <tr>
        <td>Water Column EEC</td>
        <td>%s</td>
        <td>&#956;g/L</td>
        </tr>
        <tr>
        </table>
        """ % (chemical_name, l_kow, k_oc, c_wdp_2, water_column_EEC)
        html = html + """
        <table border="1">
        <tr><H3>Ecosystem components</H3></tr>
        <tr>
        <td>Ecosystem component</td>
        <td>Total concentration</td>
        <td>Lipid normalized concentration</td> 
        <td>Contribution due to diet</td>
        <td>Contribution due to respiration</td>
        </tr>
        <tr>
        <td>Water total</td> 
        <td>%s</td>
        <td>NA</td>
        <td>NA</td>
        <td>NA</td>
        </tr>
        <tr>
        <td>Water freely dissolved</td>
        <td>%s</td>
        <td>NA</td>
        <td>NA</td>
        <td>NA</td>
        </tr>
        <tr>
        <td>Sediment pore water</td>
        <td>%.3f</td>
        <td>NA</td>
        <td>NA</td>
        <td>NA</td>
        </tr>
        <td>Sediment in solid</td>
        <td>%.3f</td>
        <td>NA</td>
        <td>NA</td>
        <td>NA</td>
        </tr>
        <tr>
        <td>Phytoplankton</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>NA</td>
        <td>%.5f</td>
        </tr>
        <tr>
        <td>Zooplankton</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        </tr>
        <tr>
        <td>Benthic invertebrates</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        </tr>
        <tr>
        <td>Filter feeders</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        </tr>
        <tr>
        <td>Small Fish</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        </tr>
        <tr>
        <td>Medium Fish</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        </tr>
        <tr>
        <td>Large Fish</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        <td>%.3f</td>
        </tr>
        </table>
        """ % (water_column_EEC, water_d(x_poc, x_doc, k_ow, c_wto), c_wdp_2, c_s_f(c_wdp, k_oc, oc), cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc), cbl_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton), cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc), cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment), cbl_zoo_f(k_ow, wb_zoo, c_ox, w_t, k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, v_nb_zoo, v_wb_zoo, v_lb_zoo, zoo_p_sediment, s_lipid, zoo_p_phyto, s_NLOM, s_water), cbd_zoo_f(k_ow, wb_zoo, c_ox, w_t, k1_phytoplankton, kd_zoo, c_wdp, c_wto, k2_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, ke_zoo), cbr_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k1_zoo, k2_zoo, ke_zoo, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto), cb_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv), cbl_beninv_f(k_ow, wb_zoo, c_ox, w_t, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, v_nb_zoo, v_wb_zoo, v_lb_zoo, zoo_p_sediment, s_lipid, zoo_p_phyto, s_NLOM, s_water, v_lb_beninv, beninv_p_zooplankton, beninv_p_phytoplankton, beninv_p_sediment, v_nb_beninv, v_wb_beninv, wb_beninv, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k1_beninv, k2_beninv, kd_beninv, ke_beninv), cbd_beninv_f(x_poc, x_doc, k_ow, wb_beninv, c_ox, k1_beninv, k2_beninv, ke_beninv, kd_beninv, w_t, k1_phytoplankton, c_wdp, v_wb_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo), cbr_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, k1_zoo, k2_zoo, kd_zoo, ke_zoo), cb_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates), cbl_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, v_lb_ff), cbd_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates), cbr_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates), cb_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbl_sf_f(v_lb_sf, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbd_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbr_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cb_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbl_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders, v_lb_mf), cbd_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbr_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cb_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbl_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, v_lb_lf, k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders, v_lb_mf), cbd_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbr_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders))       
        




        html = html + """        
        <table border="1">
        <tr><H3>Total BCF and BAF levels in aquatic trophic levels</H3></tr>
        <tr>
        <td>Trophic level</td>
        <td>Total BCF (&#956g/kg-ww)/(&#956g/L)</td>
        <td>Total BAF (&#956g/kg-ww)/(&#956g/L)</td>
        </tr>
        <tr>
        <td>Phytoplankton</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>Zooplankton</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>Benthic Invertebrates</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>Filter feeders</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>Small fish</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>Medium fish</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>Large fish</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        </table>
        """ % (cbcf_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc), cbaf_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc), cbf_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment), cbaf_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment), cbf_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv), cbaf_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv), cbf_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates), cbaf_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates), cbf_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbaf_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbf_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbaf_mf_f(k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbf_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbaf_lf_f(kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders))






        html = html + """        
        <table border="1">
        <tr><H3>Lipid normalized BCF, BAF, BMF, and BSAF, values of in aquatic trophic levels.</H3></tr> 
        <tr>
        <td>Trophic levels</td>
        <td>BCF (&#956g/kg-lipid)/(&#956g/L)</td>
        <td>BAF (&#956g/kg-lipid)/(&#956g/L)</td>
        <td>BMF (&#956g/kg-lipid)/(&#956g/kg-lipid)</td>
        <td>BSAF (&#956g/kg-lipid)/(&#956g/kg-OC)</td>
        </tr>
        <tr>
        <td>phytoplankton</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>zooplankton</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>Benthic invertebrates</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>Filter feeders</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>Small fish</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>Medium fish</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>Large fish</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        </table>
        """ % (cbcfl_phytoplankton_f(v_lb_phytoplankton, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc), cbafl_phytoplankton_f(v_lb_phytoplankton, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc), cbsafl_phytoplankton_f(k_oc, v_lb_phytoplankton, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc), cbfl_zoo_f(v_lb_zoo, k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment), cbafl_zoo_f(v_lb_zoo, k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment), bmf_zoo_f(cb_zoo_v, v_lb_zoo, zoo_p_phyto, cb_phytoplankton_v, v_lb_phytoplankton), cbsafl_zoo_f(v_lb_zoo, k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment), cbfl_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv), cbafl_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv), bmf_beninv_f(cb_beninv_v, v_lb_beninv, beninv_p_zooplankton, cb_zoo_v, v_lb_zoo, beninv_p_phytoplankton, cb_phytoplankton_v, v_lb_phytoplankton), cbsafl_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv), cbfl_ff_f(v_lb_ff, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates), cbafl_ff_f(v_lb_ff, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates), bmf_ff_f(cb_ff_v, v_lb_ff, ff_p_benthic_invertebrates, cb_beninv_v, v_lb_beninv, ff_p_zooplankton, cb_zoo_v, v_lb_zoo, ff_p_phytoplankton, cb_phytoplankton_v, v_lb_phytoplankton), cbsafl_ff_f(v_lb_ff, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates), cbfl_sf_f(v_lb_sf, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbafl_sf_f(v_lb_sf, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), bmf_sf_f(cb_sf_v, v_lb_sf, sf_p_filter_feeders, cb_ff_v, v_lb_ff, sf_p_benthic_invertebrates, cb_beninv_v,v_lb_beninv, sf_p_zooplankton, cb_zoo_v, v_lb_zoo, sf_p_phytoplankton, cb_phytoplankton_v, v_lb_phytoplankton), cbsafl_sf_f(v_lb_sf, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbfl_mf_f(v_lb_mf, k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbafl_mf_f(v_lb_mf, k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbmf_mf_f(cb_mf_v, v_lb_mf, mf_p_small_fish, cb_sf_v, v_lb_sf, mf_p_filter_feeders, cb_ff_v, v_lb_ff, mf_p_benthic_invertebrates, cb_beninv_v, v_lb_beninv, mf_p_zooplankton, cb_zoo_v, v_lb_zoo, mf_p_phytoplankton, cb_phytoplankton_v, v_lb_phytoplankton), cbsafl_mf_f(v_lb_mf, k1_mf, k2_mf, kd_mf, ke_mf, wb_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbfl_lf_f(v_lb_lf, kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbafl_lf_f(v_lb_lf, kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbmf_lf_f(v_lb_lf, v_lb_mf, v_lb_sf, v_lb_ff, cb_mf_v, cb_sf_v, cb_ff_v, cb_beninv_v, cb_zoo_v, cb_phytoplankton_v, kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders), cbsafl_lf_f(v_lb_lf, kd_lf, k2_lf, ke_lf, k1_lf, wb_lf, wb_mf, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, k1_mf, k2_mf, kd_mf, ke_mf, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders))



        html = html + """        
        <table border="1">
        <tr><H3>Calculation of EECs for mammals and birds consuming fish contaminated by %s</H3></tr> 
        <tr>
        <td>Wildlife Species</td>
        <td>Body weight (kg)</td>
        <td>Dry food ingestion rate (kg-dry food/kg-bw/day)</td>
        <td>Wet food ingestion rate (kg-wet food/kg-bw/day)</td>
        <td>Drinking water intake (L/d)</td>
        <td>Dose based (mg/kg-bw/d)</td>
        <td>Dietary based (ppm)</td>
        </tr>
        <tr>
        <td>fog/water shrew</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>rice rate/star nosed mole</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>small mink</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>large mink</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>small river otter</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>large river otter</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>sandpipers</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>cranes</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>rails</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>herons</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>small osprey</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>white pelican</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        </table>
        """ % (chemical_name, mweight[:,0], dfir[:,0], wet_food_ingestion_m[:,0],drinking_water_intake_m[:,0],db4[:,0], db5[0], mweight[:,1], dfir[:,1], wet_food_ingestion_m[:,1],drinking_water_intake_m[:,1],db4[:,1], db5[1], mweight[:,2], dfir[:,2], wet_food_ingestion_m[:,2],drinking_water_intake_m[:,2],db4[:,2], db5[2], mweight[:,3], dfir[:,3], wet_food_ingestion_m[:,3],drinking_water_intake_m[:,3],db4[:,3], db5[3], mweight[:,4], dfir[:,4], wet_food_ingestion_m[:,4],drinking_water_intake_m[:,4],db4[:,4], db5[4], mweight[:,5], dfir[:,5], wet_food_ingestion_m[:,5],drinking_water_intake_m[:,5],db4[:,5], db5[5], aweight[:,0], dfir_a[:,0], wet_food_ingestion_a[:,0],drinking_water_intake_a[:,0],db4a[:,0], db5a[0], aweight[:,1], dfir_a[:,1], wet_food_ingestion_a[:,1],drinking_water_intake_a[:,1],db4a[:,1], db5a[1], aweight[:,2], dfir_a[:,2], wet_food_ingestion_a[:,2],drinking_water_intake_a[:,2],db4a[:,2], db5a[2], aweight[:,3], dfir_a[:,3], wet_food_ingestion_a[:,3],drinking_water_intake_a[:,3],db4a[:,3], db5a[3], aweight[:,4], dfir_a[:,4], wet_food_ingestion_a[:,4],drinking_water_intake_a[:,4],db4a[:,4], db5a[4], aweight[:,5], dfir_a[:,5], wet_food_ingestion_a[:,5],drinking_water_intake_a[:,5],db4a[:,5], db5a[5])




        html = html + """        
        <table border="1">
        <tr><H3>Calculation of toxicity values for mammals and birds consuming fish contaminated by %s</H3></tr> 
        <table border="1">
        <tr>
        <th rowspan="3">WildlifeSpecies</th>
        <th colspan="4">Toxicity values</th>
        </tr>
        <tr>
        <td colspan="2">Acute</td>
        <td colspan="2">Chronic</td>
        </tr>
        <tr>
        <td>Dose Based (mg/kg-bw)</td>
        <td>Dietary Based (mg/kg-diet)</td>
        <td>Dose Based (mg/kg-bw)</td>
        <td>Dietary Based (mg/kg-diet)</td>
        </tr>
        <tr>        
        <td colspan="5">Mammalian</td>
        </tr>
        <tr>
        <td>fog/water shrew</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>rice rate/star nosed mole</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>small mink</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>large mink</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>small river otter</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>large river otter</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td colspan="5">Avian</td>
        </tr>
        <tr>
        <td>sandpipers</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>cranes</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>rails</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>herons</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>small osprey</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>white pelican</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
         </table>  
        """% (chemical_name, acute_dose_based_m[:,0], mammalian_ld50, chronic_dose_based_m[:,0], mammalian_chronic_endpoint, acute_dose_based_m[:,1], mammalian_ld50, chronic_dose_based_m[:,1], mammalian_chronic_endpoint, acute_dose_based_m[:,2], mammalian_ld50, chronic_dose_based_m[:,2], mammalian_chronic_endpoint, acute_dose_based_m[:,3], mammalian_ld50, chronic_dose_based_m[:,3], mammalian_chronic_endpoint,  acute_dose_based_m[:,4], mammalian_ld50, chronic_dose_based_m[:,4], mammalian_chronic_endpoint, acute_dose_based_m[:,5], mammalian_ld50, chronic_dose_based_m[:,5], mammalian_chronic_endpoint, acute_dose_based_a[:,0], avian_ld50, avian_lc50, acute_dose_based_a[:,1], avian_ld50, avian_lc50, acute_dose_based_a[:,2], avian_ld50, avian_lc50, acute_dose_based_a[:,3], avian_ld50, avian_lc50, acute_dose_based_a[:,4], avian_ld50, avian_lc50, acute_dose_based_a[:,5], avian_ld50, avian_lc50)



        html = html + """        
        <table border="1">
        <tr><H3>Calculation of RQ values for mammals and birds consuming fish contaminated by %s</H3></tr> 
        <table border="1">
        <tr>
        <th rowspan="3">WildlifeSpecies</th>
        </tr>
        <tr>
        <td colspan="2">Acute</td>
        <td colspan="2">Chronic</td>
        </tr>
        <tr>
        <td>Dose Based</td>
        <td>Dietary Based</td>
        <td>Dose Based</td>
        <td>Dietary Based</td>
        </tr>
        <tr>        
        <td colspan="5">Mammalian</td>
        </tr>
        <tr>
        <td>fog/water shrew</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>rice rate/star nosed mole</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>small mink</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>large mink</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>small river otter</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>large river otter</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td colspan="5">Avian</td>
        </tr>
        <tr>
        <td>sandpipers</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>cranes</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>rails</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>herons</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>small osprey</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        <tr>
        <td>white pelican</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>NA</td>
        <td>%.2f</td>
        </tr>
        </table>  
        """% (chemical_name, acute_rq_dose_m[:,0], acute_rq_diet_m[0], chronic_rq_dose_m[:,0], chronic_rq_diet_m[0], acute_rq_dose_m[:,1], acute_rq_diet_m[1], chronic_rq_dose_m[:,1], chronic_rq_diet_m[1], acute_rq_dose_m[:,2], acute_rq_diet_m[2], chronic_rq_dose_m[:,2], chronic_rq_diet_m[2], acute_rq_dose_m[:,3], acute_rq_diet_m[3], chronic_rq_dose_m[:,3], chronic_rq_diet_m[3], acute_rq_dose_m[:,4], acute_rq_diet_m[4], chronic_rq_dose_m[:,4], chronic_rq_diet_m[4], acute_rq_dose_m[:,5], acute_rq_diet_m[5], chronic_rq_dose_m[:,5], chronic_rq_diet_m[5], acute_rq_dose_a[:,0], acute_rq_diet_a[0], chronic_rq_diet_a[0], acute_rq_dose_a[:,1], acute_rq_diet_a[1], chronic_rq_diet_a[1], acute_rq_dose_a[:,2], acute_rq_diet_a[2], chronic_rq_diet_a[2], acute_rq_dose_a[:,3], acute_rq_diet_a[3], chronic_rq_diet_a[3], acute_rq_dose_a[:,4], acute_rq_diet_a[4], chronic_rq_diet_a[4], acute_rq_dose_a[:,5], acute_rq_diet_a[5], chronic_rq_diet_a[5])



        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        #print 'cb_phyto=', cb_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, x_doc, x_poc)
        #print 'cbl_phyto=', cbl_phytoplankton_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton)
        #print 'cb_zoo=', cb_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_phyto, zoo_p_sediment)
        #print 'cbr_zoo=', cbr_zoo_f(k_ow, wb_zoo, w_t, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k1_zoo, k2_zoo, ke_zoo, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto)        
        #print 'k1_zoo=', k1_zoo_f(k_ow, wb_zoo, c_ox)        
        #print 'k2_zoo=', k2_zoo_f(k_bw_zoo, k1_zoo) 
#        print 'kd_zoo=', kd_zoo_f(k_ow, wb_zoo, w_t)               
#        print 'ke_zoo=', ke_zoo_f(k_ow, wb_zoo, v_lb_zoo, v_nb_zoo, zoo_p_sediment, s_lipid, s_NLOM, zoo_p_phyto, v_lb_phytoplankton, v_nb_phytoplankton, s_water, v_wb_phytoplankton, w_t, v_wb_zoo)
#        print 'kg_zoo=', kg_zoo_f(wb_zoo, w_t)        
#        print 'diet_zoo=', diet_zoo_f(k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto)                
#        print 'ed_zoo=', ed_zoo_f(k_ow)
#        print 'gd_zoo=', gd_zoo_f(wb_zoo, w_t)
#        print 'ed_zoo=', ed_zoo_f(k_ow)
#        print 'gf_zoo=', gf_zoo_f(zoo_p_sediment, s_lipid, zoo_p_phyto, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, s_water, v_wb_phytoplankton, wb_zoo, w_t)
#        print 'kgb_zoo=', kgb_zoo_f(k_ow, v_lb_zoo, v_nb_zoo, wb_zoo, zoo_p_sediment, s_water, zoo_p_phyto, v_wb_phytoplankton, w_t, s_lipid, v_lb_phytoplankton, s_NLOM, v_nb_phytoplankton, v_wb_zoo)
#        print 'wb_zoo =', wb_zoo
#        print 'w_t=', w_t
#        print 'cb_beninv=', cb_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv)
#        print 'cbd_beninv=', cbd_beninv_f(x_poc, x_doc, k_ow, wb_beninv, c_ox, k1_beninv, k2_beninv, ke_beninv, kd_beninv, w_t, k1_phytoplankton, c_wdp, v_wb_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo)     
#        print 'cbr_beninv=',cbr_beninv_f(x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, k1_zoo, k2_zoo, kd_zoo, ke_zoo)        
#        print 'gv_beninv=', gv_beninv_f(wb_beninv, c_ox)  
#        print 'ew_beninv=', ew_beninv_f(k_ow)
#        print 'k1_beninv=', k1_beninv_f(k_ow, wb_beninv, c_ox)
#        print 'k_bw_beninv=', k_bw_beninv_f(v_lb_beninv, k_ow, v_nb_beninv, v_wb_beninv)
#        print 'k2_beninv=', k2_beninv_f(k1_beninv, k_bw_beninv)
#        print 'ed_beninv=', ed_beninv_f(k_ow)
 #       print 'gd_beninv=', gd_beninv_f(wb_beninv, w_t)
#        print 'kd_beninv=', kd_beninv_f(k_ow, wb_beninv, w_t)
#        print 'kg_beninv=', kg_beninv_f(wb_beninv, w_t)
#        print 'v_ld_beninv=', v_ld_beninv_f(beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo)
#        print 'v_nd_beninv=', v_nd_beninv_f(beninv_p_sediment, s_NLOM, beninv_p_phytoplankton, v_nb_phytoplankton, beninv_p_zooplankton, v_nb_zoo)
#        print 'v_wd_beninv=', v_wd_beninv_f(beninv_p_sediment, s_water, beninv_p_phytoplankton, v_wb_phytoplankton, beninv_p_zooplankton, v_wb_zoo)
#        print 'gf_beninv=', gf_beninv_f(beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t)
#        print 'vlg_beninv=', vlg_beninv_f(wb_beninv, w_t, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo)
#        print 'vng_beninv=', vng_beninv_f(beninv_p_sediment, s_NLOM, beninv_p_phytoplankton, v_nb_phytoplankton, beninv_p_zooplankton, v_nb_zoo, wb_beninv, w_t, s_lipid, v_lb_phytoplankton, v_lb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo)
#        print 'vwg_beninv=', vwg_beninv_f(beninv_p_sediment, s_water, beninv_p_phytoplankton, v_wb_phytoplankton, beninv_p_zooplankton, v_wb_zoo, s_lipid, v_lb_phytoplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, wb_beninv, w_t)
#        print 'kgb_beninv=', kgb_beninv_f(wb_beninv, w_t, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, k_ow, v_lb_beninv, v_nb_beninv, v_wb_beninv)
#        print 'ke_beninv=', ke_beninv_f(k_ow, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, wb_beninv, w_t, v_lb_beninv, v_nb_beninv, v_wb_beninv)
#        print 'diet_beninv=', diet_beninv_f(k1_phytoplankton, c_wdp, c_wto, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_ow, k_oc, oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, c_ox, w_t, v_nb_zoo, v_wb_zoo, v_lb_zoo, s_lipid, s_NLOM, s_water, beninv_p_phytoplankton, beninv_p_zooplankton, beninv_p_sediment)
#        print 'cb_ff=', cb_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
#        print 'cbl_ff=', cbl_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, v_lb_ff)
#        print 'cbd_ff=', cbd_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
#        print 'cbr_ff=', cbr_ff_f(k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, w_t, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates)
#        print 'k1_sf=', k1_sf_f(k_ow, wb_sf, c_ox)
#        print 'k2_sf=', k2_sf_f(k1_sf, k_bw_sf)
#        print 'gd_sf=', gd_sf_f(wb_sf, w_t)
#        print 'kd_sf=', kd_sf_f(k_ow, wb_sf, w_t, c_ss, c_ox)
#        print 'kbw_sf=', k_bw_sf_f(v_lb_sf, k_ow, v_nb_sf, v_wb_sf)        
#        print 'ed_sf=', ed_sf_f(k_ow)
#        print 'wb_sf=', wb_sf
#        print 'cb_sf=', cb_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
#        print 'cbl_sf=', cbl_sf_f(v_lb_sf, wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
#        print 'cbd_sf=', cbd_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
#        print 'cbr_sf=', cbr_sf_f(wb_sf, k1_sf, k2_sf, kd_sf, ke_sf, sf_p_benthic_invertebrates, ff_p_phytoplankton, ff_p_sediment, ff_p_zooplankton, k1_ff, k2_ff, kd_ff, ke_ff, wb_ff, sf_p_phytoplankton, sf_p_sediment, sf_p_zooplankton, x_poc, x_doc, k_ow, k1_beninv, k2_beninv, kd_beninv, ke_beninv, wb_beninv, c_ox, w_t, k1_phytoplankton, c_wdp, k1_zoo, k2_zoo, kd_zoo, ke_zoo, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km_phytoplankton, mo_phytoplankton, mp_phytoplankton, k_oc, v_wb_beninv, oc, k_bw_phytoplankton, zoo_p_sediment, zoo_p_phyto, wb_zoo, beninv_p_sediment, s_lipid, beninv_p_phytoplankton, v_lb_phytoplankton, beninv_p_zooplankton, v_lb_zoo, s_NLOM,  v_nb_phytoplankton, v_nb_zoo, s_water, v_wb_phytoplankton, v_wb_zoo, v_lb_beninv, v_nb_beninv, ff_p_benthic_invertebrates, sf_p_filter_feeders)
#        print 'gf_sf=', gf_sf_f(s_lipid, s_NLOM, wb_sf, w_t, s_water, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff)
#        print 'vlg_sf=', vlg_sf_f(s_NLOM, s_lipid, wb_sf, w_t, s_water, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff,  v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff)
#        print 'vng_sf=', vng_sf_f(c_ox, ff_p_sediment, s_lipid, ff_p_phytoplankton, ff_p_zooplankton, s_NLOM,  v_nb_phytoplankton, v_nb_zoo,  v_wb_phytoplankton, v_wb_zoo, c_ss, wb_ff,  wb_sf, w_t, s_water, v_nb_beninv, v_nb_ff, sf_p_sediment, sf_p_phytoplankton, v_lb_phytoplankton, sf_p_benthic_invertebrates, v_lb_beninv, sf_p_zooplankton, v_lb_zoo, sf_p_filter_feeders, v_lb_ff, v_wb_ff, v_wb_beninv)
#        print 'vwg_sf=', vwg_sf_f(s_lipid, s_water, s_NLOM, v_nb_phytoplankton, v_nb_beninv, v_nb_zoo, v_nb_ff, v_lb_phytoplankton, v_lb_beninv, v_lb_zoo, v_lb_ff, wb_sf, w_t, sf_p_sediment, sf_p_phytoplankton, v_wb_phytoplankton, sf_p_benthic_invertebrates, v_wb_beninv, v_wb_zoo, sf_p_zooplankton,  sf_p_filter_feeders, v_wb_ff)
#        print 'k1_lf=', k1_lf_f(k_ow, wb_lf, c_ox)
#        print 'k2_lf=', k2_lf_f(k1_lf, k_bw_lf)
#        print 'kd_lf=', kd_lf_f(k_ow, wb_lf, w_t, c_ss, c_ox)
#        print 'ke_lf=', ke_lf_f(k_ow, v_lb_lf, v_nb_lf, v_wb_lf, wb_lf, s_lipid, lf_p_sediment, v_lb_phytoplankton, lf_p_phytoplankton, v_lb_beninv, v_lb_zoo, lf_p_benthic_invertebrates, lf_p_zooplankton, lf_p_filter_feeders, v_lb_ff, v_lb_sf, lf_p_small_fish, s_water, lf_p_medium_fish, v_nb_mf, v_wb_phytoplankton, v_wb_beninv, v_wb_zoo, v_wb_ff, v_wb_sf, wb_mf, w_t, mf_p_sediment, s_NLOM, mf_p_phytoplankton, v_nb_phytoplankton, v_lb_mf, v_wb_mf, mf_p_benthic_invertebrates, v_nb_beninv, mf_p_zooplankton, v_nb_zoo, mf_p_filter_feeders, v_nb_ff, mf_p_small_fish, v_nb_sf)
#        print denom4
        self.response.out.write(html)
        
        #update 
#        conn = MySQLdb.connect("localhost", "root", "th339933ht", "kabam")
#        cursor = conn.cursor()
#        cursor.execute('UPDATE input SET aw_bird=%s WHERE aw_bird=%s', (aw_bird,Kabamdb.aw_bird_p))
#        conn.commit()
#        conn.close()

#        conn = MySQLdb.connect("localhost", "root", "th339933ht", "kabam")
#        cursor = conn.cursor()
#        cursor.execute('INSERT INTO input (aw_bird, mf_w_bird) VALUES(%s, %s)', (aw_bird, mf_w_bird))
#        conn.commit()
#        conn.close()


        
#        if aw_bird != Kabamdb.aw_bird_p:
#            conn = MySQLdb.connect("localhost", "root", "th339933ht", "kabam")
#            cursor = conn.cursor()
#            cursor.execute('UPDATE input SET aw_bird=%s WHERE aw_bird=%s', (aw_bird, Kabamdb.aw_bird_p))
#            conn.close()
#           
#        else: pass
    
#        conn = MySQLdb.connect("localhost", "root", "th339933ht", "kabam")
#        cursor = conn.cursor()    
#        cursor.execute('INSERT INTO ouput (para_out) VALUES (%s)', (fi_bird(aw_bird, mf_w_bird)))
#        conn.commit()
#        conn.close()
#        
app = webapp.WSGIApplication([('/.*', KabamOutputPage)], debug=True)
        

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    