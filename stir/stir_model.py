import numpy as np
import logging
import sys
import math
from django.utils import simplejson

def toJSON(stir_object):
    stir_vars = vars(stir_object)
    stir_json = simplejson.dumps(stir_vars)
    return stir_json

def fromJSON(json_string):
    stir_vars = simplejson.loads(json_string)
    new_stir = stir(True,False,vars_dict=stir_vars)
    return new_stir

class StirModel:
    #inputs
    chemical_name = ''
    ar2 = 1
    h = 1
    f_inhaled = 1
    ddsi = 1
    mw = 1
    vp = 1
    ld50ao = 1
    assessed_bw_avian = 1
    mineau = 1
    lc50 = 1
    dur = 1
    assessed_bw_mammal = 1
    ld50ri = 1
    ld50ro = 1

    #outputs

    def __init__(self,set_variables=TRUE, run_methods=TRUE,
            chemical_name=None, ar2=None, h=None, f_inhaled=None, ddsi=None, mw=None, vp=None,ld50ao=None, assessed_bw_avian=None, 
            mineau=None, lc50=None, dur=None, assessed_bw_mammal=None, ld50ri=None, ld50ro=None):
        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.set_variables(chemical_name,ar2,h,f_inhaled,ddsi,mw,vp,ld50ao,assessed_bw_avian,mineau,lc50,dur,
                    assessed_bw_mammal,ld50ri,ld50ro)
            if run_methods:
                self.run_methods()

    def __str__(self):
        string_rep = ''
        string_rep = string_rep + self.chemical_name
        string_rep = string_rep + "ar2 = %.2e \n" % self.ar2
        string_rep = string_rep + "h = %.2e \n" % self.h
        string_rep = string_rep + "f_inhaled = %.2e \n" % self.f_inhaled
        string_rep = string_rep + "ddsi = %.2e \n" % self.ddsi
        string_rep = string_rep + "mw = %.2e \n" % self.mw
        string_rep = string_rep + "vp = %.2e \n" % self.vp
        string_rep = string_rep + "ld50ao = %.2e \n" % self.ld50ao
        string_rep = string_rep + "assessed_bw_avian = %.2e \n" % self.assessed_bw_avian
        string_rep = string_rep + "mineau = %.2e \n" % self.mineau
        string_rep = string_rep + "lc50 = %.2e \n" % self.lc50
        string_rep = string_rep + "dur = %.2e \n" % self.dur
        string_rep = string_rep + "assessed_bw_mammal = %.2e \n" % self.assessed_bw_mammal
        string_rep = string_rep + "ld50ri = %.2e \n" % self.ld50ri
        string_rep = string_rep + "ld50ro = %.2e \n" % self.ld50ro
        string_rep = string_rep + "rundry_results = %.2e \n" % self.rundry_results
        string_rep = string_rep + "runsemi_results = %.2e \n" % self.runsemi_results
        string_rep = string_rep + "totaldry_results = %.2e \n" % self.totaldry_results
        string_rep = string_rep + "totalsemi_results = %.2e \n" % self.totalsemi_results
        string_rep = string_rep + "spray_results = %.2e \n" % self.spray_results
        string_rep = string_rep + "nmsRQdry_results = %.2e \n" % self.nmsRQdry_results
        string_rep = string_rep + "nmsRQsemi_results = %.2e \n" % self.nmsRQsemi_results
        string_rep = string_rep + "nmsRQspray_results = %.2e \n" % self.nmsRQspray_results
        string_rep = string_rep + "lmsRQdry_results = %.2e \n" % self.lmsRQdry_results
        string_rep = string_rep + "lmsRQsemi_results = %.2e \n" % self.lmsRQsemi_results
        string_rep = string_rep + "lmsRQspray_results = %.2e \n" % self.lmsRQspray_results
        string_rep = string_rep + "ndsRQdry_results = %.2e \n" % self.ndsRQdry_results
        string_rep = string_rep + "ndsRQsemi_results = %.2e \n" % self.ndsRQsemi_results
        string_rep = string_rep + "ndsRQspray_results = %.2e \n" % self.ndsRQspray_results
        string_rep = string_rep + "ldsRQdry_results = %.2e \n" % self.ldsRQdry_results
        string_rep = string_rep + "ldsRQsemi_results = %.2e \n" % self.ldsRQsemi_results
        string_rep = string_rep + "ldsRQspray_results = %.2e \n" % self.ldsRQspray_results
        return string_rep

    def set_variables(self,chemical_name,ar2,h,f_inhaled,ddsi,mw,vp,ld50ao,assessed_bw_avian, 
            mineau,lc50,dur,assessed_bw_mammal,ld50ri,ld50ro):
        self.chemical_name = chemical_name
        self.ar2 = ar2
        self.h = h
        self.f_inhaled = f_inhaled
        self.ddsi = ddsi
        self.mw = mw
        self.vp = vp
        self.ld50ao = ld50ao
        self.assessed_bw_avian = assessed_bw_avian
        self.mineau = mineau
        self.lc50 = lc50
        self.dur = dur
        self.assessed_bw_mammal = assessed_bw_mammal
        self.ld50ri = ld50ri
        self.ld50ro = ld50ro

    def run_methods(self):
        try:
            self.CalcSatAirConc() #eq. 1
            self.CalcInhRateAvian() #eq. 2
            self.CalcVidAvian() #eq. 3
            self.CalcInhRateMammal() #eq. 4
            self.CalcVidMammal() #eq. 5
            self.CalcConcAir() #eq. 6
            self.CalcSidAvian() #eq. 7
            self.CalcSidMammal() #eq. 8
            self.CalcLD50() #eq. 9
            self.CalcLD50AdjMammal() #eq. 10
            self.CalcLD50Est() #eq. 11
            self.CalcLD50AdjAvian() #eq. 12
            self.ReturnRatioVdAvian() #results #1
            self.ReturnLocVdAvian() #results #2
            self.ReturnRatioSidAvian() #results #3
            self.ReturnLocSidAvian() #results #4
            self.ReturnRatioVdMammal() #results #5
            self.ReturnLocVdMammal() #results #6
            self.ReturnRatioSidMammal() #results #7
            self.ReturnLocSidMammal() #results #8
        except TypeError:
            print "Type Error: Your variables are not set correctly."

    #eq. 1 saturated air concentration in mg/m^3
    def CalcSatAirConc(self):
        self.vp = float(vp)
        self.mw = float(mw)
        air_vol = 24.45
        pressure = 760.0
        conv = 1000000.0
        sat_air_conc = (vp * mw * conv)/(pressure * air_vol)
        return sat_air_conc

    #eq. 2 Avian inhalation rate
    def CalcInhRateAvian(self):
        self.assessed_bw_avian = float(assessed_bw_avian)
        magic1 = 284.
        magic2 = 0.77
        conversion = 60.
        activity_factor = 3.
        inh_rate_avian = magic1 * (assessed_bw_avian**magic2) * conversion * activity_factor
        return inh_rate_avian

    #eq. 3  Maximum avian vapor inhalation dose
    def CalcVidAvian(self):
        self.sat_air_conc = float(sat_air_conc)
        self.inh_rate_avian = float(inh_rate_avian)
        self.assessed_bw_avian = float(assessed_bw_avian)
        duration_hours = 1.
        conversion_factor = 1000000. # cm3/m3
        vid_avian = (sat_air_conc * inh_rate_avian * duration_hours)/(conversion_factor * assessed_bw_avian) # 1 (hr) is duration of exposure
        return vid_avian

    #eq. 4 Mammalian inhalation rate
    def CalcInhRateMammal(self):
        self.assessed_bw_mammal = float(assessed_bw_mammal)
        magic1 = 379.0
        magic2 = 0.8
        minutes_conversion = 60.
        activity_factor = 3
        inh_rate_mammal = magic1 * (assessed_bw_mammal**magic2) * minutes_conversion * activity_factor
        return inh_rate_mammal

    #eq. 5 Maximum mammalian vapor inhalation dose
    def CalcVidMammal(self):
        self.cs = float(cs)
        self.ir_mammal = float(ir_mammal)
        self.aw_mammal = float(aw_mammal)
        duration_hours = 1.
        conversion_factor = 1000000.
        vid_mammal = (cs * ir_mammal * duration_hours)/(conversion_factor * aw_mammal) # 1 hr = duration of exposure
        return vid_mammal

    #eq. 6 Air column concentration after spray
    def CalcConcAir(self):
        self.ar1 = float(ar1)
        self.h = float(h)
        conversion_factor = 100. #cm/m
        self.ar2 = PARConversion(ar1)
        air_conc = self.ar2/(h * conversion_factor)
        return air_conc

    # conversion of application rate from lbs/acre to mg/cm2
    def CalcPARConversion(self):
        cf_g_lbs = 453.59237
        cf_mg_g = 1000.
        cf_cm2_acre = 40468564.2
        self.ar2 = (ar1*cf_g_lbs*cf_mg_g)/cf_cm2_acre
        return ar2

    #eq. 7 Avian spray droplet inhalation dose
    def CalcSidAvian(self):
        self.c_air = float(c_air)
        self.ir_avian = float(ir_avian)
        self.ddsi = float(ddsi)
        self.f_inhaled = float(f_inhaled)
        self.aw_avian = float(aw_avian)
        sid_avian = (c_air * ir_avian * ddsi * f_inhaled)/(60.0 * aw_avian)
        return sid_avian

    #eq. 8 Mammalian spray droplet inhalation dose
    def CalcSidMammal(self):
        self.c_air = float(c_air)
        self.ir_mammal = float(ir_mammal)
        self.ddsi = float(ddsi)
        self.f_inhaled = float(f_inhaled)
        self.aw_mammal = float(aw_mammal)
        sid_mammal = (c_air * ir_mammal * ddsi * f_inhaled)/(60.0 * aw_mammal)
        return sid_mammal

    # Conversion Factor
    def CF(self):
        self.ir_mammal = float(ir_mammal)
        self.aw_mammal = float(aw_mammal)
        cf = ((ir_mammal * 0.001)/aw_mammal)
        return cf

    #eq. 9 Conversion of mammalian LC50 to LD50
    def CalcLD50 (self):
        self.lc50 = float(lc50)
        self.cf = float(cf)
        self.dur = float(dur)
        ld50 = lc50 * 1 * cf * dur * 1 # Absorption is assumed to be 100% = 1 -- Activity Factor = 1 (reflects the rat at rest in the experimental conditions)
        return ld50

    #eq. 10 Adjusted mammalian inhalation LD50
    def CalcLD50AdjMammal(self):
        self.ld50 = float(ld50)
        self.tw_mammal = float(tw_mammal)
        self.aw_mammal = float(aw_mammal)
        ld50adj_mammal = ld50 * (tw_mammal/aw_mammal)**0.25
        return ld50adj_mammal

    #eq. 11 Estimated avian inhalation LD50
    def CalcLD50Est(self):
        self.ld50ao = float(ld50ao)
        self.ld50ri = float(ld50ri)
        self.ld50ro = float(ld50ro)
        ld50_est = (ld50ao * ld50ri)/(3.5 * ld50ro) 
        return ld50_est

    #eq. 12 Adjusted avian inhalation LD50
    def CalcLD50AdjAvian(self):
        self.ld50est = float(ld50est)
        self.aw_avian = float(aw_avian)
        self.tw_avian = float(tw_avian)
        self.mineau = float(mineau)
        ld50adj_avian = ld50est * (aw_avian/tw_avian)**(mineau - 1)
        return ld50adj_avian

    # ----------------------------------------------
    # results
    # ----------------------------------------------
    # results #1: Ratio of avian vapor dose to adjusted inhalation LD50
    def ReturnRatioVdAvian(self):
        self.vid_avian = float(vid_avian)
        self.ld50adj_avian = float(ld50adj_avian)
        ratio_vd_avian = vid_avian/ld50adj_avian
        return ratio_vd_avian

    # results #2: Level of Concern for avian vapor phase risk
    def ReturnLocVdAvian(self):
        if ratio_vd_avian < 0.1:
            return ('Exposure not Likely Significant')
        else:
            return ('Proceed to Refinements')

    # results #3: Ratio of avian droplet inhalation dose to adjusted inhalation LD50
    def ReturnRatioSidAvian(self):
        self.sid_avian = float(sid_avian)
        self.ld50adj_avian = float(ld50adj_avian)
        ratio_sid_avian = sid_avian/ld50adj_avian
        return ratio_sid_avian

    # results #4: Level of Concern for avian droplet inhalation risk
    def ReturnLocSidAvian(self):
        if ratio_sid_avian < 0.1:
            return ('Exposure not Likely Significant')
        else:
            return ('Proceed to Refinements')

    # results #5: Ratio of mammalian vapor dose to adjusted inhalation LD50
    def ReturnRatioVdMammal(self):
        self.vid_mammal = float(vid_mammal)
        self.ld50adj_mammal = float(ld50adj_mammal)
        ratio_vd_mammal = vid_mammal/ld50adj_mammal
        return vid_mammal/ld50adj_mammal

    # results #6: Level of Concern for mammalian vapor phase risk
    def ReturnLocVdMammal(self):
        if ratio_vd_mammal < 0.1:
            return ('Exposure not Likely Significant')
        else:
            return ('Proceed to Refinements')

    # results #7: Ratio of mammalian droplet inhalation dose to adjusted inhalation LD50
    def ReturnRatioSidMammal(self):
        self.sid_mammal = float(sid_mammal)
        self.ld50adj_mammal = float(ld50adj_mammal)
        ratio_sid_mammal = sid_mammal/ld50adj_mammal
        return ratio_sid_mammal

    # results #8: Level of Concern for mammaliam droplet inhalation risk
    def ReturnLocSidMammal(self):
        if ratio_sid_mammal < 0.1:
            return ('Exposure not Likely Significant')
        else:
            return ('Proceed to Refinements')

def main():
    test_stir = stir(True,True,1,1,1,1,1,1,1,1)
    print vars(test_stir)
    stir_json = toJSON(test_stir)
    new_stir = fromJSON(stir_json)
    print vars(new_stir)

if __name__ == '__main__':
    main()