import numpy as np
import logging
import sys
import math


class dust(object):

    def __init__(self, chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res, bird_acute_oral_study, bird_study_add_comm,
              low_bird_acute_ld50, test_bird_bw, mineau, mamm_acute_derm_study, mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw):
        self.chemical_name=chemical_name
        self.label_epa_reg_no=label_epa_reg_no
        self.ar_lb=ar_lb
        self.frac_pest_surface=frac_pest_surface
        self.dislodge_fol_res=dislodge_fol_res
        self.bird_acute_oral_study=bird_acute_oral_study
        self.bird_study_add_comm=bird_study_add_comm
        self.low_bird_acute_ld50=low_bird_acute_ld50
        self.test_bird_bw=test_bird_bw
        self.mineau=mineau
        self.mamm_acute_derm_study=mamm_acute_derm_study
        self.mamm_study_add_comm=mamm_study_add_comm
        self.mam_acute_derm_ld50=mam_acute_derm_ld50
        self.test_mam_bw=test_mam_bw
        self.run_methods()

    def run_methods(self):
        self.ar_mg()
        self.bird_reptile_dermal_ld50()
        self.gran_bird_ex_derm_dose()
        self.gran_repamp_ex_derm_dose()
        self.gran_mam_ex_derm_dose()
        self.fol_bird_ex_derm_dose()
        self.fol_repamp_ex_derm_dose()
        self.fol_mam_ex_derm_dose()
        self.bgs_bird_ex_derm_dose()
        self.bgs_repamp_ex_derm_dose()
        self.bgs_mam_ex_derm_dose()
        self.amp_derm_ld50()
        self.birdrep_derm_ld50()
        self.mam_derm_ld50()
        self.ratio_gran_bird()
        self.LOC_gran_bird()
        self.ratio_gran_rep()
        self.LOC_gran_rep()
        self.ratio_gran_amp()
        self.LOC_gran_amp()
        self.ratio_gran_mam()
        self.LOC_gran_mam()
        self.ratio_fol_bird()
        self.LOC_fol_bird()
        self.ratio_fol_rep()
        self.LOC_fol_rep()
        self.ratio_fol_amp()
        self.LOC_fol_amp()
        self.ratio_fol_mam()
        self.LOC_fol_mam()
        self.ratio_bgs_bird()
        self.LOC_bgs_bird()
        self.ratio_bgs_rep()
        self.LOC_bgs_rep()
        self.ratio_bgs_amp()
        self.LOC_bgs_amp()
        self.ratio_bgs_mam()
        self.LOC_bgs_mam()

    #Application rate conversion to mg/cm2
    def ar_mg(self):
        self.ar_mg = float(self.ar_lb) * 0.011208511
        return self.ar_mg

    def bird_reptile_dermal_ld50(self):
        self.low_bird_acute_ld50 = float(self.low_bird_acute_ld50)
        self.bird_reptile_dermal_ld50 = 10**(0.84+(0.62*(math.log(self.low_bird_acute_ld50))))
        return self.bird_reptile_dermal_ld50

    #------Granular Application------

    def gran_bird_ex_derm_dose(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.gran_bird_ex_derm_dose = (((self.ar_mg*self.frac_pest_surface)/1300)*0.958*(10*(20**0.667)))/(20.0/1000.0)
        return self.gran_bird_ex_derm_dose

    #Reptile/Amphibian External Dermal Dose
    def gran_repamp_ex_derm_dose(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.gran_repamp_ex_derm_dose = ((self.ar_mg*self.frac_pest_surface/1300)*0.958*(8.42*(20**0.694)))/(20.0/1000.0)
        return self.gran_repamp_ex_derm_dose

    #Mammal External Dermal Dose
    def gran_mam_ex_derm_dose(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.gran_mam_ex_derm_dose = ((self.ar_mg*self.frac_pest_surface/1300)*0.958*(12.3*(15**0.65)))/(15.0/1000.0)
        return self.gran_mam_ex_derm_dose

    #------Foliar Spray Application-------

    #Bird External Dermal Dose
    def fol_bird_ex_derm_dose(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.dislodge_fol_res = float(self.dislodge_fol_res)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.fol_bird_ex_derm_dose = ((self.dislodge_fol_res*6.01*12*(10*(20**0.667)))+(self.ar_mg*((10*(20**0.667))/2)))/(20.0/1000.0)
        return self.fol_bird_ex_derm_dose

    #Reptile/Amphibian External Dermal Dose
    def fol_repamp_ex_derm_dose(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.dislodge_fol_res = float(self.dislodge_fol_res)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.fol_repamp_ex_derm_dose = ((self.dislodge_fol_res*6.01*12*(8.42*(20**0.694)))+(self.ar_mg*((8.42*(20**0.694))/2)))/(20.0/1000.0)
        return self.fol_repamp_ex_derm_dose
        
    #Mammal External Dermal Dose
    def fol_mam_ex_derm_dose(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.dislodge_fol_res = float(self.dislodge_fol_res)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.fol_mam_ex_derm_dose = ((self.dislodge_fol_res*6.01*12*(12.3*(15**0.65)))+(self.ar_mg*((12.3*(15**0.65))/2)))/(15.0/1000.0)
        return self.fol_mam_ex_derm_dose
        
    #------Bare Ground Spray Application-------

    #Bird External Dermal Dose
    def bgs_bird_ex_derm_dose(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.bgs_bird_ex_derm_dose = (((self.ar_mg*self.frac_pest_surface/1300.0)*0.958*(10*(20**0.667)))+(self.ar_mg*((10*(20**0.667))/2.0)))/(20.0/1000.0)
        return self.bgs_bird_ex_derm_dose

    #Reptile/Amphibian External Dermal Dose
    def bgs_repamp_ex_derm_dose(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.bgs_repamp_ex_derm_dose = (((self.ar_mg*self.frac_pest_surface/1300.0)*0.958*(8.42*(20**0.694)))+(self.ar_mg*((8.42*(20**0.694))/2.0)))/(20.0/1000.0)
        return self.bgs_repamp_ex_derm_dose
        
    #Mammal External Dermal Dose
    def bgs_mam_ex_derm_dose(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.bgs_mam_ex_derm_dose = (((self.ar_mg*self.frac_pest_surface/1300.0)*0.958*(12.3*(20**0.65)))+(self.ar_mg*((12.3*(20**0.65))/2.0)))/(15.0/1000.0)
        return self.bgs_mam_ex_derm_dose


    #------Dermal Toxicity Calculation (ADJ LD50)------

    #Estimate 20g Amphibian Dermal LD50 (mg a.i./kg-bw)
    def amp_derm_ld50(self):
        try:
            self.low_bird_acute_ld50 = float(self.low_bird_acute_ld50)
            self.test_bird_bw = float(self.test_bird_bw)
            self.mineau = float(self.mineau)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.amp_derm_ld50 = self.low_bird_acute_ld50*((20.0/self.test_bird_bw)**(self.mineau-1.0))
        return self.amp_derm_ld50


    #Estimate 20g Bird/Reptile Dermal LD50 (mg a.i./kg-bw)
    def birdrep_derm_ld50(self):
        try:
            self.bird_reptile_dermal_ld50 = float(self.bird_reptile_dermal_ld50)
            self.test_bird_bw = float(self.test_bird_bw)
            self.mineau = float(self.mineau)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.birdrep_derm_ld50 = self.bird_reptile_dermal_ld50*((20/self.test_bird_bw)**(self.mineau-1))
        return self.birdrep_derm_ld50

    #Estimate 15g Mammal Dermal LD50 (mg a.i./kg-bw)
    def mam_derm_ld50(self):
        try:
            self.mam_acute_derm_ld50 = float(self.mam_acute_derm_ld50)
            self.test_mam_bw = float(self.test_mam_bw)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        self.mam_derm_ld50 = self.mam_acute_derm_ld50*((self.test_mam_bw/15.0)**0.25)
        return self.mam_derm_ld50

    #------RATIO OF EXPOSURE TO TOXICITY------


    #______Granular

    #Bird
    def ratio_gran_bird(self):
        self.ratio_gran_bird = self.gran_bird_ex_derm_dose/self.birdrep_derm_ld50
        return self.ratio_gran_bird

    def LOC_gran_bird(self):
        if self.ratio_gran_bird < 0.01:
            self.LOC_gran_bird ='Exposure Not Likely Significant'
            return self.LOC_gran_bird
        else:
            self.LOC_gran_bird = 'Potentially Significant Pathway'
            return self.LOC_gran_bird

    #Reptile
    def ratio_gran_rep(self):
        self.ratio_gran_rep = self.gran_repamp_ex_derm_dose/self.birdrep_derm_ld50
        return self.ratio_gran_rep

    def LOC_gran_rep(self):
        if self.ratio_gran_rep < 0.01:
            self.LOC_gran_rep = 'Exposure Not Likely Significant'
            return self.LOC_gran_rep
        else:
            self.LOC_gran_rep = 'Potentially Significant Pathway'
            return self.LOC_gran_rep
        
    #Amphibian
    def ratio_gran_amp(self):
        self.ratio_gran_amp = self.gran_repamp_ex_derm_dose/self.amp_derm_ld50
        return self.ratio_gran_amp

    def LOC_gran_amp(self):
        if self.ratio_gran_amp < 0.01:
            self.LOC_gran_amp = 'Exposure Not Likely Significant'
            return self.LOC_gran_amp
        else:
            self.LOC_gran_amp = 'Potentially Significant Pathway'
            return self.LOC_gran_amp
        
        
    #Mammal
    def ratio_gran_mam(self):
        self.ratio_gran_mam = self.gran_mam_ex_derm_dose/self.mam_derm_ld50
        return self.ratio_gran_mam

    def LOC_gran_mam(self):
        if self.ratio_gran_mam < 0.01:
            self.LOC_gran_mam = 'Exposure Not Likely Significant'
            return self.LOC_gran_mam
        else:
            self.LOC_gran_mam = 'Potentially Significant Pathway'
            return self.LOC_gran_mam

    #_______Foliar Spray

    #Bird
    def ratio_fol_bird(self):
        self.ratio_fol_bird = self.fol_bird_ex_derm_dose/self.birdrep_derm_ld50
        return self.ratio_fol_bird

    def LOC_fol_bird(self):
        if self.ratio_fol_bird < 0.01:
            self.LOC_fol_bird = 'Exposure Not Likely Significant'
            return self.LOC_fol_bird
        else:
            self.LOC_fol_bird = 'Potentially Significant Pathway'
            return self.LOC_fol_bird


    #Reptile
    def ratio_fol_rep(self):
        self.ratio_fol_rep = self.fol_repamp_ex_derm_dose/self.birdrep_derm_ld50
        return self.ratio_fol_rep

    def LOC_fol_rep(self):
        if self.ratio_fol_rep < 0.01:
            self.LOC_fol_rep = 'Exposure Not Likely Significant'
            return self.LOC_fol_rep
        else:
            self.LOC_fol_rep = 'Potentially Significant Pathway'
            return self.LOC_fol_rep

    #Amphibian
    def ratio_fol_amp(self):
        self.ratio_fol_amp = self.fol_repamp_ex_derm_dose/self.amp_derm_ld50
        return self.ratio_fol_amp

    def LOC_fol_amp(self):
        if self.ratio_fol_amp < 0.01:
            self.LOC_fol_amp = 'Exposure Not Likely Significant'
            return self.LOC_fol_amp
        else:
            self.LOC_fol_amp = 'Potentially Significant Pathway'
            return self.LOC_fol_amp

    #Mammal
    def ratio_fol_mam(self):
        self.ratio_fol_mam = self.fol_mam_ex_derm_dose/self.mam_derm_ld50
        return self.ratio_fol_mam
        
    def LOC_fol_mam(self):
        if self.ratio_fol_mam < 0.01:
            self.LOC_fol_mam = 'Exposure Not Likely Significant'
            return self.LOC_fol_mam
        else:
            self.LOC_fol_mam = 'Potentially Significant Pathway'
            return self.LOC_fol_mam

    #_______Bare Ground Spray

    #Bird
    def ratio_bgs_bird(self):
        self.ratio_bgs_bird = self.bgs_bird_ex_derm_dose/self.birdrep_derm_ld50
        return self.ratio_bgs_bird
        
    def LOC_bgs_bird(self):
        if self.ratio_bgs_bird < 0.01:
            self.LOC_bgs_bird = 'Exposure Not Likely Significant'
            return self.LOC_bgs_bird
        else:
            self.LOC_bgs_bird = 'Potentially Significant Pathway'
            return self.LOC_bgs_bird

    #Reptile
    def ratio_bgs_rep(self):
        self.ratio_bgs_rep = self.bgs_repamp_ex_derm_dose/self.birdrep_derm_ld50
        return self.ratio_bgs_rep

    def LOC_bgs_rep(self):
        if self.ratio_bgs_rep < 0.01:
            self.LOC_bgs_rep = 'Exposure Not Likely Significant'
            return self.LOC_bgs_rep
        else:
            self.LOC_bgs_rep = 'Potentially Significant Pathway'
            return self.LOC_bgs_rep

    #Amphibian
    def ratio_bgs_amp(self):
        self.ratio_bgs_amp = self.bgs_repamp_ex_derm_dose/self.amp_derm_ld50
        return self.ratio_bgs_amp

    def LOC_bgs_amp(self):
        if self.ratio_bgs_amp < 0.01:
            self.LOC_bgs_amp = 'Exposure Not Likely Significant'
            return self.LOC_bgs_amp
        else:
            self.LOC_bgs_amp = 'Potentially Significant Pathway'    
            return self.LOC_bgs_amp

    #Mammal
    def ratio_bgs_mam(self):
        self.ratio_bgs_mam = self.bgs_mam_ex_derm_dose/self.mam_derm_ld50
        return self.ratio_bgs_mam

    def LOC_bgs_mam(self):
        if self.ratio_bgs_mam < 0.01:
            self.LOC_bgs_mam = 'Exposure Not Likely Significant'
            return self.LOC_bgs_mam
        else:
            self.LOC_bgs_mam = 'Potentially Significant Pathway'
            return self.LOC_bgs_mam
    
    
    
sys.path.append('C:\Python27\Lib\site-packages')

import pymongo
from django.utils import simplejson
import json

dust_obj = dust("Chem 1", "", 2, 0.2, 2, 2, 2, 2, 2, 0.5, 2, 2, 2, 2)


client = pymongo.MongoClient()
print client

# print dust_json
db = client.test_database
posts = db.posts
# print dust_obj.__dict__
posts.save(dust_obj.__dict__)

# print db
# print posts

print posts.find_one({"LOC_bgs_amp": "Potentially Significant Pathway"})

for post in posts.find():
    print post