import numpy as np
import logging
import sys

import math

#Application rate conversion to mg/cm2
def ar_mg(ar_lb):
    ar_lb = float(ar_lb)
    return ar_lb * 0.011208511


#Calculated Bird/Reptile Dermal LD50 (mg a.i./kg-bw)    
def bird_reptile_dermal_ld50(low_bird_acute_ld50):
    low_bird_acute_ld50 = float(low_bird_acute_ld50)
    return 10**(0.84+(0.62*(math.log(low_bird_acute_ld50))))
    

#------Granular Application------

#Bird External Dermal Dose
def gran_bird_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return (((ar_mg*frac_pest_surface)/1300)*0.958*(10*(20**0.667)))/(20.0/1000.0)
    

#Reptile/Amphibian External Dermal Dose
def gran_repamp_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return ((ar_mg*frac_pest_surface/1300)*0.958*(8.42*(20**0.694)))/(20.0/1000.0)
    

#Mammal External Dermal Dose
def gran_mam_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return ((ar_mg*frac_pest_surface/1300)*0.958*(12.3*(15**0.65)))/(15.0/1000.0)
    

#------Foliar Spray Application-------

#Bird External Dermal Dose
def fol_bird_ex_derm_dose(dislodge_fol_res,ar_mg):
    try:
        ar_mg = float(ar_mg)
        dislodge_fol_res = float(dislodge_fol_res)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return ((dislodge_fol_res*6.01*12*(10*(20**0.667)))+(ar_mg*((10*(20**0.667))/2)))/(20.0/1000.0)
    

#Reptile/Amphibian External Dermal Dose
def fol_repamp_ex_derm_dose(dislodge_fol_res,ar_mg):
    try:
        ar_mg = float(ar_mg)
        dislodge_fol_res = float(dislodge_fol_res)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return ((dislodge_fol_res*6.01*12*(8.42*(20**0.694)))+(ar_mg*((8.42*(20**0.694))/2)))/(20.0/1000.0)
    
    
#Mammal External Dermal Dose
def fol_mam_ex_derm_dose(dislodge_fol_res,ar_mg):
    try:
        ar_mg = float(ar_mg)
        dislodge_fol_res = float(dislodge_fol_res)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return ((dislodge_fol_res*6.01*12*(12.3*(15**0.65)))+(ar_mg*((12.3*(15**0.65))/2)))/(15.0/1000.0)
    
    
#------Bare Ground Spray Application-------

#Bird External Dermal Dose
def bgs_bird_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return (((ar_mg*frac_pest_surface/1300.0)*0.958*(10*(20**0.667)))+(ar_mg*((10*(20**0.667))/2.0)))/(20.0/1000.0)
    

#Reptile/Amphibian External Dermal Dose
def bgs_repamp_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return (((ar_mg*frac_pest_surface/1300.0)*0.958*(8.42*(20**0.694)))+(ar_mg*((8.42*(20**0.694))/2.0)))/(20.0/1000.0)
    
    
#Mammal External Dermal Dose
def bgs_mam_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return (((ar_mg*frac_pest_surface/1300.0)*0.958*(12.3*(20**0.65)))+(ar_mg*((12.3*(20**0.65))/2.0)))/(15.0/1000.0)
    


#------Dermal Toxicity Calculation (ADJ LD50)------

#Estimate 20g Amphibian Dermal LD50 (mg a.i./kg-bw)
def amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau):
    try:
        low_bird_acute_ld50 = float(low_bird_acute_ld50)
        test_bird_bw = float(test_bird_bw)
        mineau = float(mineau)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return low_bird_acute_ld50*((20.0/test_bird_bw)**(mineau-1.0))
    

#Estimate 20g Bird/Reptile Dermal LD50 (mg a.i./kg-bw)
def birdrep_derm_ld50(bird_reptile_dermal_ld50,test_bird_bw,mineau):
    try:
        bird_reptile_dermal_ld50 = float(bird_reptile_dermal_ld50)
        test_bird_bw = float(test_bird_bw)
        mineau = float(mineau)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return bird_reptile_dermal_ld50*((20/test_bird_bw)**(mineau-1))
    

#Estimate 15g Mammal Dermal LD50 (mg a.i./kg-bw)
def mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw):
    try:
        mam_acute_derm_ld50 = float(mam_acute_derm_ld50)
        test_mam_bw = float(test_mam_bw)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return mam_acute_derm_ld50*((test_mam_bw/15.0)**0.25)
    

#------RATIO OF EXPOSURE TO TOXICITY------


#______Granular

#Bird
def ratio_gran_bird(gran_bird_ex_derm_dose,birdrep_derm_ld50):
    return gran_bird_ex_derm_dose/birdrep_derm_ld50
    
def LOC_gran_bird(ratio_gran_bird):
    if ratio_gran_bird < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Reptile
def ratio_gran_rep(gran_repamp_ex_derm_dose,birdrep_derm_ld50):
    return gran_repamp_ex_derm_dose/birdrep_derm_ld50
    
def LOC_gran_rep(ratio_gran_rep):
    if ratio_gran_rep < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
    
#Amphibian
def ratio_gran_amp(gran_repamp_ex_derm_dose,amp_derm_ld50):
    return gran_repamp_ex_derm_dose/amp_derm_ld50
    
def LOC_gran_amp(ratio_gran_amp):
    if ratio_gran_amp < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
    
#Mammal
def ratio_gran_mam(gran_mam_ex_derm_dose,mam_derm_ld50):
    return gran_mam_ex_derm_dose/mam_derm_ld50
    
def LOC_gran_mam(ratio_gran_mam):
    if ratio_gran_mam < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    

#_______Foliar Spray

#Bird
def ratio_fol_bird(fol_bird_ex_derm_dose,birdrep_derm_ld50):
    return fol_bird_ex_derm_dose/birdrep_derm_ld50

def LOC_fol_bird(ratio_fol_bird):
    if ratio_fol_bird < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Reptile
def ratio_fol_rep(fol_repamp_ex_derm_dose,birdrep_derm_ld50):
    return fol_repamp_ex_derm_dose/birdrep_derm_ld50
    
def LOC_fol_rep(ratio_fol_rep):
    if ratio_fol_rep < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Amphibian
def ratio_fol_amp(fol_repamp_ex_derm_dose,amp_derm_ld50):
    return fol_repamp_ex_derm_dose/amp_derm_ld50
    
def LOC_fol_amp(ratio_fol_amp):
    if ratio_fol_amp < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Mammal
def ratio_fol_mam(fol_mam_ex_derm_dose,mam_derm_ld50):
    return fol_mam_ex_derm_dose/mam_derm_ld50
    
def LOC_fol_mam(ratio_fol_mam):
    if ratio_fol_mam < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    

#_______Bare Ground Spray

#Bird
def ratio_bgs_bird(bgs_bird_ex_derm_dose,birdrep_derm_ld50):
    return bgs_bird_ex_derm_dose/birdrep_derm_ld50
    
def LOC_bgs_bird(ratio_bgs_bird):
    if ratio_bgs_bird < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Reptile
def ratio_bgs_rep(bgs_repamp_ex_derm_dose,birdrep_derm_ld50):
    return bgs_repamp_ex_derm_dose/birdrep_derm_ld50
    
def LOC_bgs_rep(ratio_bgs_rep):
    if ratio_bgs_rep < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Amphibian
def ratio_bgs_amp(bgs_repamp_ex_derm_dose,amp_derm_ld50):
    return bgs_repamp_ex_derm_dose/amp_derm_ld50
    
def LOC_bgs_amp(ratio_bgs_amp):
    if ratio_bgs_amp < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Mammal
def ratio_bgs_mam(bgs_mam_ex_derm_dose,mam_derm_ld50):
    return bgs_mam_ex_derm_dose/mam_derm_ld50
    
def LOC_bgs_mam(ratio_bgs_mam):
    if ratio_bgs_mam < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
    
    
    
  
