import numpy as np
import logging
import sys
import math
import time, datetime


class dust(object):
    def __init__(self, set_variables=True, run_methods=True, run_type='single', chemical_name='', label_epa_reg_no='', ar_lb=1, frac_pest_surface=1, dislodge_fol_res=1,  bird_acute_oral_study="", bird_study_add_comm="",
              low_bird_acute_ld50=1, test_bird_bw=1, mineau_scaling_factor=1, mamm_acute_derm_study='', mamm_study_add_comm='',  mam_acute_derm_ld50=1, mam_acute_oral_ld50=1, test_mam_bw=1, vars_dict=None):
        self.set_default_variables()
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
                self.set_variables(run_type, chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res,  bird_acute_oral_study, bird_study_add_comm,
              low_bird_acute_ld50, test_bird_bw, mineau_scaling_factor, mamm_acute_derm_study, mamm_study_add_comm,  mam_acute_derm_ld50, mam_acute_oral_ld50, test_mam_bw)

            if run_methods:
                self.run_methods()

    def set_default_variables(self):
 #Currently used variables
        self.run_type = "single"
        self.chemical_name=''
        self.label_epa_reg_no=''
        self.ar_lb=1
        self.frac_pest_surface=1
        self.dislodge_fol_res=1
        self.bird_acute_oral_study=1
        self.bird_study_add_comm=''
        self.low_bird_acute_ld50=1
        self.test_bird_bw=1
        self.mineau_scaling_factor=1
        self.mamm_acute_derm_study=''
        self.mamm_study_add_comm=''
        #self.aviandermaltype=1
        self.mam_acute_derm_ld50=1
        self.mam_acute_oral_ld50=1
        self.test_mam_bw=1
        #result variables
        self.ar_mg=-1
        self.bird_reptile_dermal_ld50=-1
        self.gran_bird_ex_derm_dose=-1
        self.gran_repamp_ex_derm_dose=-1
        self.gran_mam_ex_derm_dose=-1
        self.fol_bird_ex_derm_dose=-1
        self.fol_repamp_ex_derm_dose=-1
        self.fol_mam_ex_derm_dose=-1
        self.bgs_bird_ex_derm_dose=-1
        self.bgs_repamp_ex_derm_dose=-1
        self.bgs_mam_ex_derm_dose=-1
        self.amp_derm_ld50=-1
        self.birdrep_derm_ld50=-1
        self.mam_derm_ld50=-1
        self.ratio_gran_bird=-1
        self.LOC_gran_bird=-1
        self.ratio_gran_rep=-1
        self.LOC_gran_rep=-1
        self.ratio_gran_amp=-1
        self.LOC_gran_amp=-1
        self.ratio_gran_mam=-1
        self.LOC_gran_mam=-1
        self.ratio_fol_bird=-1
        self.LOC_fol_bird=-1
        self.ratio_fol_rep=-1
        self.LOC_fol_rep=-1
        self.ratio_fol_amp=-1
        self.LOC_fol_amp=-1
        self.ratio_fol_mam=-1
        self.LOC_fol_mam=-1
        self.ratio_bgs_bird=-1
        self.LOC_bgs_bird=-1
        self.ratio_bgs_rep=-1
        self.LOC_bgs_rep=-1
        self.ratio_bgs_amp=-1
        self.LOC_bgs_amp=-1
        self.ratio_bgs_mam=-1
        self.LOC_bgs_mam=-1

    def set_variables(self, run_type, chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res, bird_acute_oral_study, bird_study_add_comm,
              low_bird_acute_ld50, test_bird_bw, mineau_scaling_factor, mamm_acute_derm_study, mamm_study_add_comm, mam_acute_derm_ld50, mam_acute_oral_ld50, test_mam_bw):
        self.run_type = run_type
        self.chemical_name=chemical_name
        self.label_epa_reg_no=label_epa_reg_no
        self.ar_lb=ar_lb
        self.frac_pest_surface=frac_pest_surface
        self.dislodge_fol_res=dislodge_fol_res
        self.bird_acute_oral_study=bird_acute_oral_study
        self.bird_study_add_comm=bird_study_add_comm
        self.low_bird_acute_ld50=low_bird_acute_ld50
        self.test_bird_bw=test_bird_bw
        self.mineau_scaling_factor=mineau_scaling_factor
        self.mamm_acute_derm_study=mamm_acute_derm_study
        self.mamm_study_add_comm=mamm_study_add_comm
        #self.aviandermaltype=aviandermaltype
        self.mam_acute_derm_ld50=mam_acute_derm_ld50
        self.mam_acute_oral_ld50 = mam_acute_oral_ld50
        self.test_mam_bw=test_mam_bw
        self.run_methods()

    def run_methods(self):
        self.ar_mg_f()
        self.bird_reptile_dermal_ld50_f()
        self.gran_bird_ex_derm_dose_f()
        self.gran_repamp_ex_derm_dose_f()
        self.gran_mam_ex_derm_dose_f()
        self.fol_bird_ex_derm_dose_f()
        self.fol_repamp_ex_derm_dose_f()
        self.fol_mam_ex_derm_dose_f()
        self.bgs_bird_ex_derm_dose_f()
        self.bgs_repamp_ex_derm_dose_f()
        self.bgs_mam_ex_derm_dose_f()
        self.amp_derm_ld50_f()
        self.birdrep_derm_ld50_f()
        self.mam_derm_ld50_f()
        self.ratio_gran_bird_f()
        self.LOC_gran_bird_f()
        self.ratio_gran_rep_f()
        self.LOC_gran_rep_f()
        self.ratio_gran_amp_f()
        self.LOC_gran_amp_f()
        self.ratio_gran_mam_f()
        self.LOC_gran_mam_f()
        self.ratio_fol_bird_f()
        self.LOC_fol_bird_f()
        self.ratio_fol_rep_f()
        self.LOC_fol_rep_f()
        self.ratio_fol_amp_f()
        self.LOC_fol_amp_f()
        self.ratio_fol_mam_f()
        self.LOC_fol_mam_f()
        self.ratio_bgs_bird_f()
        self.LOC_bgs_bird_f()
        self.ratio_bgs_rep_f()
        self.LOC_bgs_rep_f()
        self.ratio_bgs_amp_f()
        self.LOC_bgs_amp_f()
        self.ratio_bgs_mam_f()
        self.LOC_bgs_mam_f()

    #Application rate conversion to mg/cm2
    def ar_mg_f(self):
        if self.ar_mg == -1:
            self.ar_mg = float(self.ar_lb) * 0.011208511
            return self.ar_mg

    def bird_reptile_dermal_ld50_f(self):
        self.low_bird_acute_ld50 = float(self.low_bird_acute_ld50)
        self.mam_acute_oral_ld50 = float(self.mam_acute_oral_ld50)
        self.mam_acute_derm_ld50 = float(self.mam_acute_derm_ld50)
        if self.bird_reptile_dermal_ld50 == -1:
           # if self.aviandermaltype == 'With DTI':
            #    self.bird_reptile_dermal_ld50 = 10**(1.7822+0.8199 *(math.log(self.low_bird_acute_ld50))-0.4874 * (math.log(self.mam_acute_oral_ld50/self.mam_acute_derm_ld50*1000)))
            #elif self.aviandermaltype == 'With DTI 90% CI':
				 # rmse1<-0.5361976
				 # var_b1<-0.1038**2
				 # var_b2<-0.1210**2
				 # b1_mean<-0.6379028
				 # b2_mean<-2.432222
				 # no.samples<-72
				 # self.bird_reptile_dermal_ld50 = 10**(1.7822+0.8199 *(math.log(self.low_bird_acute_ld50))-0.4874 * (math.log(self.mam_acute_oral_ld50/self.mam_acute_derm_ld50*1000)))
     #         	-((math.sqrt(2)/2)*2.38*math.sqrt((rmse1**2/(no.samples)) + ((self.low_bird_acute_ld50-b1_mean)**2*var_b1)+(((math.log(self.mam_acute_oral_ld50/self.mam_acute_derm_ld50*1000)-b2_mean)**2*var_b2)+rmse1**2 ))
            self.bird_reptile_dermal_ld50 = 10**(1.7822+0.8199 *(math.log(self.low_bird_acute_ld50))-0.4874 * (math.log(self.mam_acute_oral_ld50/self.mam_acute_derm_ld50*1000)))
            -((math.sqrt(2)/2)*2.38*math.sqrt((0.5361976**2/(72)) + ((self.low_bird_acute_ld50-0.6379028)**2*0.1038**2)+(((math.log(self.mam_acute_oral_ld50/self.mam_acute_derm_ld50*1000)-2.432222)**2*0.1210**2)+0.5361976**2)))
            #else:
             #   self.bird_reptile_dermal_ld50 = 10**(0.84+(0.62*(math.log(self.low_bird_acute_ld50))))
            return self.bird_reptile_dermal_ld50
    

    #------Granular Application------

    def gran_bird_ex_derm_dose_f(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.gran_bird_ex_derm_dose == -1:
            self.gran_bird_ex_derm_dose = (((self.ar_mg*self.frac_pest_surface)/1300)*0.958*(10*(20**0.667)))/(20.0/1000.0)
        return self.gran_bird_ex_derm_dose

    #Reptile/Amphibian External Dermal Dose
    def gran_repamp_ex_derm_dose_f(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.gran_repamp_ex_derm_dose == -1:    
            self.gran_repamp_ex_derm_dose = ((self.ar_mg*self.frac_pest_surface/1300)*0.958*(8.42*(20**0.694)))/(20.0/1000.0)
        return self.gran_repamp_ex_derm_dose

    #Mammal External Dermal Dose
    def gran_mam_ex_derm_dose_f(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.gran_mam_ex_derm_dose == -1:    
            self.gran_mam_ex_derm_dose = ((self.ar_mg*self.frac_pest_surface/1300)*0.958*(12.3*(15**0.65)))/(15.0/1000.0)
        return self.gran_mam_ex_derm_dose

    #------Foliar Spray Application-------

    #Bird External Dermal Dose
    def fol_bird_ex_derm_dose_f(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.dislodge_fol_res = float(self.dislodge_fol_res)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.fol_bird_ex_derm_dose == -1:    
            self.fol_bird_ex_derm_dose = ((self.ar_mg*6.01*6*0.158*0.2*(10*(20**0.667)))+(self.ar_mg*((10*(20**0.667)*0.1))))/(20.0/1000.0)
        return self.fol_bird_ex_derm_dose

    #Reptile/Amphibian External Dermal Dose
    def fol_repamp_ex_derm_dose_f(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.dislodge_fol_res = float(self.dislodge_fol_res)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.fol_repamp_ex_derm_dose == -1:    
            self.fol_repamp_ex_derm_dose = ((self.ar_mg*6.01*6*0.158*0.2*(8.42*(20**0.694)))+(self.ar_mg*((8.42*(20**0.694))*0.1)))/(20.0/1000.0)
        return self.fol_repamp_ex_derm_dose
        
    #Mammal External Dermal Dose
    def fol_mam_ex_derm_dose_f(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.dislodge_fol_res = float(self.dislodge_fol_res)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.fol_mam_ex_derm_dose == -1:    
            self.fol_mam_ex_derm_dose = ((self.ar_mg*6.01*0.158*0.2*(12.3*(15**0.65)))+(self.ar_mg*((12.3*(15**0.65))*0.1))/(15.0/1000.0))
        return self.fol_mam_ex_derm_dose
        
    #------Bare Ground Spray Application-------

    #Bird External Dermal Dose
    def bgs_bird_ex_derm_dose_f(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.bgs_bird_ex_derm_dose == -1:    
            self.bgs_bird_ex_derm_dose = (((self.ar_mg*self.frac_pest_surface/1300.0)*0.958*(10*(20**0.667)))+(self.ar_mg*((10*(20**0.667))/2.0)))/(20.0/1000.0)
        return self.bgs_bird_ex_derm_dose

    #Reptile/Amphibian External Dermal Dose
    def bgs_repamp_ex_derm_dose_f(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.bgs_repamp_ex_derm_dose == -1:    
            self.bgs_repamp_ex_derm_dose = (((self.ar_mg*self.frac_pest_surface/1300.0)*0.958*(8.42*(20**0.694)))+(self.ar_mg*((8.42*(20**0.694))/2.0)))/(20.0/1000.0)
        return self.bgs_repamp_ex_derm_dose
        
    #Mammal External Dermal Dose
    def bgs_mam_ex_derm_dose_f(self):
        try:
            self.ar_mg = float(self.ar_mg)
            self.frac_pest_surface = float(self.frac_pest_surface)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.bgs_mam_ex_derm_dose == -1:    
            self.bgs_mam_ex_derm_dose = (((self.ar_mg*self.frac_pest_surface/1300.0)*0.958*(12.3*(20**0.65)))+(self.ar_mg*((12.3*(20**0.65))/2.0)))/(15.0/1000.0)
        return self.bgs_mam_ex_derm_dose


    #------Dermal Toxicity Calculation (ADJ LD50)------

    #Estimate 20g Amphibian Dermal LD50 (mg a.i./kg-bw)
    def amp_derm_ld50_f(self):
        try:
            self.low_bird_acute_ld50 = float(self.low_bird_acute_ld50)
            self.test_bird_bw = float(self.test_bird_bw)
            self.mineau_scaling_factor = float(self.mineau_scaling_factor)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.amp_derm_ld50 == -1:    
            self.amp_derm_ld50 = self.low_bird_acute_ld50*((20.0/self.test_bird_bw)**(self.mineau_scaling_factor-1.0))
        return self.amp_derm_ld50
   
    #Estimate 20g Bird/Reptile Dermal LD50 (mg a.i./kg-bw)
    def birdrep_derm_ld50_f(self):
        try:
            self.bird_reptile_dermal_ld50 = float(self.bird_reptile_dermal_ld50)
            self.test_bird_bw = float(self.test_bird_bw)
            self.mineau_scaling_factor = float(self.mineau_scaling_factor)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.birdrep_derm_ld50 == -1:
            self.birdrep_derm_ld50 = self.bird_reptile_dermal_ld50*((20/self.test_bird_bw)**(self.mineau_scaling_factor-1))
        return self.birdrep_derm_ld50

    #Estimate 15g Mammal Dermal LD50 (mg a.i./kg-bw)
    def mam_derm_ld50_f(self):
        try:
            self.mam_acute_derm_ld50 = float(self.mam_acute_derm_ld50)
            self.test_mam_bw = float(self.test_mam_bw)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('')
        if self.mam_derm_ld50 == -1:    
            self.mam_derm_ld50 = self.mam_acute_derm_ld50*((self.test_mam_bw/15.0)**0.25)
        return self.mam_derm_ld50

    #------RATIO OF EXPOSURE TO TOXICITY------


    #______Granular

    #Bird
    def ratio_gran_bird_f(self):
        if self.ratio_gran_bird == -1:
            self.ratio_gran_bird = self.gran_bird_ex_derm_dose/self.birdrep_derm_ld50
        return self.ratio_gran_bird

    def LOC_gran_bird_f(self):
        if self.LOC_gran_bird == -1:
            if self.ratio_gran_bird < 0.01:
                self.LOC_gran_bird ='Exposure Not Likely Significant'
                return self.LOC_gran_bird
            else:
                self.LOC_gran_bird = 'Potentially Significant Pathway'
                return self.LOC_gran_bird

    #Reptile
    def ratio_gran_rep_f(self):
        if self.ratio_gran_rep == -1:
            self.ratio_gran_rep = self.gran_repamp_ex_derm_dose/self.birdrep_derm_ld50
            return self.ratio_gran_rep

    def LOC_gran_rep_f(self):
        if self.LOC_gran_rep == -1:
            if self.ratio_gran_rep < 0.01:
                self.LOC_gran_rep = 'Exposure Not Likely Significant'
                return self.LOC_gran_rep
            else:
                self.LOC_gran_rep = 'Potentially Significant Pathway'
                return self.LOC_gran_rep
        
    #Amphibian
    def ratio_gran_amp_f(self):
        if self.ratio_gran_amp == -1:
            self.ratio_gran_amp = self.gran_repamp_ex_derm_dose/self.amp_derm_ld50
            return self.ratio_gran_amp

    def LOC_gran_amp_f(self):
        if self.LOC_gran_amp == -1:
            if self.ratio_gran_amp < 0.01:
                self.LOC_gran_amp = 'Exposure Not Likely Significant'
                return self.LOC_gran_amp
            else:
                self.LOC_gran_amp = 'Potentially Significant Pathway'
                return self.LOC_gran_amp
        
        
    #Mammal
    def ratio_gran_mam_f(self):
        if self.ratio_gran_mam == -1:
            self.ratio_gran_mam = self.gran_mam_ex_derm_dose/self.mam_derm_ld50
            return self.ratio_gran_mam

    def LOC_gran_mam_f(self):
        if self.LOC_gran_mam == -1:
            if self.ratio_gran_mam < 0.01:
                self.LOC_gran_mam = 'Exposure Not Likely Significant'
                return self.LOC_gran_mam
            else:
                self.LOC_gran_mam = 'Potentially Significant Pathway'
                return self.LOC_gran_mam

    #_______Foliar Spray

    #Bird
    def ratio_fol_bird_f(self):
        if self.ratio_fol_bird == -1:
            self.ratio_fol_bird = self.fol_bird_ex_derm_dose/self.birdrep_derm_ld50
            return self.ratio_fol_bird

    def LOC_fol_bird_f(self):
        if self.LOC_fol_bird == -1:
            if self.ratio_fol_bird < 0.01:
                self.LOC_fol_bird = 'Exposure Not Likely Significant'
                return self.LOC_fol_bird
            else:
                self.LOC_fol_bird = 'Potentially Significant Pathway'
                return self.LOC_fol_bird


    #Reptile
    def ratio_fol_rep_f(self):
        if self.ratio_fol_rep == -1:
            self.ratio_fol_rep = self.fol_repamp_ex_derm_dose/self.birdrep_derm_ld50
            return self.ratio_fol_rep

    def LOC_fol_rep_f(self):
        if self.LOC_fol_rep == -1:
            if self.ratio_fol_rep < 0.01:
                self.LOC_fol_rep = 'Exposure Not Likely Significant'
                return self.LOC_fol_rep
            else:
                self.LOC_fol_rep = 'Potentially Significant Pathway'
                return self.LOC_fol_rep

    #Amphibian
    def ratio_fol_amp_f(self):
        if self.ratio_fol_amp == -1:
            self.ratio_fol_amp = self.fol_repamp_ex_derm_dose/self.amp_derm_ld50
            return self.ratio_fol_amp

    def LOC_fol_amp_f(self):
        if self.LOC_fol_amp == -1:
            if self.ratio_fol_amp < 0.01:
                self.LOC_fol_amp = 'Exposure Not Likely Significant'
                return self.LOC_fol_amp
            else:
                self.LOC_fol_amp = 'Potentially Significant Pathway'
                return self.LOC_fol_amp

    #Mammal
    def ratio_fol_mam_f(self):
        if self.ratio_fol_mam == -1:
            self.ratio_fol_mam = self.fol_mam_ex_derm_dose/self.mam_derm_ld50
            return self.ratio_fol_mam
        
    def LOC_fol_mam_f(self):
        if self.LOC_fol_mam == -1:
            if self.ratio_fol_mam < 0.01:
                self.LOC_fol_mam = 'Exposure Not Likely Significant'
                return self.LOC_fol_mam
            else:
                self.LOC_fol_mam = 'Potentially Significant Pathway'
                return self.LOC_fol_mam

    #_______Bare Ground Spray

    #Bird
    def ratio_bgs_bird_f(self):
        if self.ratio_bgs_bird == -1:
            self.ratio_bgs_bird = self.bgs_bird_ex_derm_dose/self.birdrep_derm_ld50
            return self.ratio_bgs_bird
        
    def LOC_bgs_bird_f(self):
        if self.LOC_bgs_bird == -1:
            if self.ratio_bgs_bird < 0.01:
                self.LOC_bgs_bird = 'Exposure Not Likely Significant'
                return self.LOC_bgs_bird
            else:
                self.LOC_bgs_bird = 'Potentially Significant Pathway'
                return self.LOC_bgs_bird

    #Reptile
    def ratio_bgs_rep_f(self):
        if self.ratio_bgs_rep == -1:
            self.ratio_bgs_rep = self.bgs_repamp_ex_derm_dose/self.birdrep_derm_ld50
            return self.ratio_bgs_rep

    def LOC_bgs_rep_f(self):
        if self.LOC_bgs_rep == -1:
            if self.ratio_bgs_rep < 0.01:
                self.LOC_bgs_rep = 'Exposure Not Likely Significant'
                return self.LOC_bgs_rep
            else:
                self.LOC_bgs_rep = 'Potentially Significant Pathway'
                return self.LOC_bgs_rep

    #Amphibian
    def ratio_bgs_amp_f(self):
        if self.ratio_bgs_amp == -1:
            self.ratio_bgs_amp = self.bgs_repamp_ex_derm_dose/self.amp_derm_ld50
            return self.ratio_bgs_amp

    def LOC_bgs_amp_f(self):
        if self.LOC_bgs_amp == -1:
            if self.ratio_bgs_amp < 0.01:
                self.LOC_bgs_amp = 'Exposure Not Likely Significant'
                return self.LOC_bgs_amp
            else:
                self.LOC_bgs_amp = 'Potentially Significant Pathway'    
                return self.LOC_bgs_amp

    #Mammal
    def ratio_bgs_mam_f(self):
        if self.ratio_bgs_mam == -1:
            self.ratio_bgs_mam = self.bgs_mam_ex_derm_dose/self.mam_derm_ld50
            return self.ratio_bgs_mam

    def LOC_bgs_mam_f(self):
        if self.LOC_bgs_mam == -1:
            if self.ratio_bgs_mam < 0.01:
                self.LOC_bgs_mam = 'Exposure Not Likely Significant'
                return self.LOC_bgs_mam
            else:
                self.LOC_bgs_mam = 'Potentially Significant Pathway'
                return self.LOC_bgs_mam
    
    
    
  
