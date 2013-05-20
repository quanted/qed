import numpy as np
import logging
import sys
import math

class StirModel:
    def __init__(self,chemical_name, ar2, h, f_inhaled, ddsi, mw, vp,ld50ao, assessed_bw_avian, mineau, lc50, dur, 
        assessed_bw_mammal, ld50ri, ld50ro):
        #inputs
        self.GetInputs(chemical_name, ar2, h, f_inhaled, ddsi, mw, vp,ld50ao, assessed_bw_avian, mineau, lc50, dur, 
        assessed_bw_mammal, ld50ri, ld50ro)
        #outputs
        self.GetOutputs()

    def GetInputs(self,chemical_name, ar2, h, f_inhaled, ddsi, mw, vp,ld50ao, assessed_bw_avian, mineau, lc50, dur, 
        assessed_bw_mammal, ld50ri, ld50ro):
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

    def GetOutputs(self):
        self.sat_air_conc = self.CalcSatAirConc(self.vp,self.mw)
        self.inh_rate_avian = self.InhRateAvian(self.assessed_bw_avian)
        self.vid_avian = self.VidAvian(self.sat_air_conc,self.inh_rate_avian,self.assessed_bw_avian)
        self.ld50est = self.LD50Est(self.ld50ao,self.ld50ri,self.ld50ro)
        #self.ld50adj
        #self.ratio_vd_avian
        #self.sid_avian
        #self.ratio_sid_avian

        self.inh_rate_mammal = self.InhRateMammal(self.assessed_bw_mammal)

    #eq. 1 saturated air concentration in mg/m^3
    def CalcSatAirConc(self,vp,mw):
        self.vp = float(vp)
        self.mw = float(mw)
        air_vol = 24.45
        pressure = 760.0
        conv = 1000000.0
        sat_air_conc = (vp * mw * conv)/(pressure * air_vol)
        return sat_air_conc

    #eq. 2 Avian inhalation rate
    def InhRateAvian(self,assessed_bw_avian):
        self.assessed_bw_avian = float(assessed_bw_avian)
        magic1 = 284.
        magic2 = 0.77
        conversion = 60.
        activity_factor = 3.
        inh_rate_avian = magic1 * (assessed_bw_avian**magic2) * conversion * activity_factor
        return inh_rate_avian

    #eq. 3  Maximum avian vapor inhalation dose
    def VidAvian(self,sat_air_conc,inh_rate_avian,assessed_bw_avian):
        self.sat_air_conc = float(sat_air_conc)
        self.inh_rate_avian = float(inh_rate_avian)
        self.assessed_bw_avian = float(assessed_bw_avian)
        duration_hours = 1.
        conversion_factor = 1000000. # cm3/m3
        vid_avian = (sat_air_conc * inh_rate_avian * duration_hours)/(conversion_factor * assessed_bw_avian) # 1 (hr) is duration of exposure
        return vid_avian

    #eq. 4 Mammalian inhalation rate
    def InhRateMammal(self,assessed_bw_mammal):
        self.assessed_bw_mammal = float(assessed_bw_mammal)
        magic1 = 379.0
        magic2 = 0.8
        minutes_conversion = 60.
        activity_factor = 3
        inh_rate_mammal = magic1 * (assessed_bw_mammal**magic2) * minutes_conversion * activity_factor
        return inh_rate_mammal

    #eq. 5 Maximum mammalian vapor inhalation dose
    def VidMammal(self,cs,ir_mammal,aw_mammal):
        self.cs = float(cs)
        self.ir_mammal = float(ir_mammal)
        self.aw_mammal = float(aw_mammal)
        duration_hours = 1.
        conversion_factor = 1000000.
        vid_mammal = (cs * ir_mammal * duration_hours)/(conversion_factor * aw_mammal) # 1 hr = duration of exposure
        return vid_mammal

    #eq. 6 Air column concentration after spray
    def ConcAir(self,ar1,h):
        self.ar1 = float(ar1)
        self.h = float(h)
        conversion_factor = 100. #cm/m
        self.ar2 = PARConversion(ar1)
        air_conc = self.ar2/(h * conversion_factor)
        return air_conc

    # conversion of application rate from lbs/acre to mg/cm2
    def PARConversion(self, ar1):
        cf_g_lbs = 453.59237
        cf_mg_g = 1000.
        cf_cm2_acre = 40468564.2
        self.ar2 = (ar1*cf_g_lbs*cf_mg_g)/cf_cm2_acre
        return ar2

    #eq. 7 Avian spray droplet inhalation dose
    def SidAvian(self,c_air,ir_avian,ddsi,f_inhaled,aw_avian):
        self.c_air = float(c_air)
        self.ir_avian = float(ir_avian)
        self.ddsi = float(ddsi)
        self.f_inhaled = float(f_inhaled)
        self.aw_avian = float(aw_avian)
        sid_avian = (c_air * ir_avian * ddsi * f_inhaled)/(60.0 * aw_avian)
        return sid_avian

    #eq. 8 Mammalian spray droplet inhalation dose
    def SidMammal(self,c_air,ir_mammal,ddsi,f_inhaled,aw_mammal):
        self.c_air = float(c_air)
        self.ir_mammal = float(ir_mammal)
        self.ddsi = float(ddsi)
        self.f_inhaled = float(f_inhaled)
        self.aw_mammal = float(aw_mammal)
        sid_mammal = (c_air * ir_mammal * ddsi * f_inhaled)/(60.0 * aw_mammal)
        return sid_mammal

    # Conversion Factor
    def CF(self,ir_mammal, aw_mammal):
        self.ir_mammal = float(ir_mammal)
        self.aw_mammal = float(aw_mammal)
        cf = ((ir_mammal * 0.001)/aw_mammal)
        return cf

    #eq. 9 Conversion of mammalian LC50 to LD50
    def LD50 (self,lc50,cf,dur):
        self.lc50 = float(lc50)
        self.cf = float(cf)
        self.dur = float(dur)
        ld50 = lc50 * 1 * cf * dur * 1 # Absorption is assumed to be 100% = 1 -- Activity Factor = 1 (reflects the rat at rest in the experimental conditions)
        return ld50

    #eq. 10 Adjusted mammalian inhalation LD50
    def LD50AdjMammal(self,ld50,tw_mammal,aw_mammal):
        self.ld50 = float(ld50)
        self.tw_mammal = float(tw_mammal)
        self.aw_mammal = float(aw_mammal)
        ld50adj_mammal = ld50 * (tw_mammal/aw_mammal)**0.25
        return ld50adj_mammal


    #eq. 11 Estimated avian inhalation LD50
    def LD50Est(self,ld50ao,ld50ri,ld50ro):
        self.ld50ao = float(ld50ao)
        self.ld50ri = float(ld50ri)
        self.ld50ro = float(ld50ro)
        ld50_est = (ld50ao * ld50ri)/(3.5 * ld50ro) 
        return ld50_est

    #eq. 12 Adjusted avian inhalation LD50
    def LD50AdjAvian(self,ld50est,aw_avian,tw_avian,mineau):
        self.ld50est = float(ld50est)
        self.aw_avian = float(aw_avian)
        self.tw_avian = float(tw_avian)
        self.mineau = float(mineau)
        ld50adj_avian = ld50est * (aw_avian/tw_avian)**(mineau - 1)
        return ld50adj_avian

    # ----------------------------------------------
    # Ratio of avian vapor dose to adjusted inhalation LD50
    def RatioVdAvian(self,vid_avian,ld50adj_avian):
        self.vid_avian = float(vid_avian)
        self.ld50adj_avian = float(ld50adj_avian)
        ratio_vd_avian = vid_avian/ld50adj_avian
        return ratio_vd_avian

    # Level of Concern for avian vapor phase risk
    def LocVdAvian(self,ratio_vd_avian):
        if ratio_vd_avian < 0.1:
            return ('Exposure not Likely Significant')
        else:
            return ('Proceed to Refinements')

    # Ratio of avian droplet inhalation dose to adjusted inhalation LD50
    def RatioSidAvian(self,sid_avian,ld50adj_avian):
        self.sid_avian = float(sid_avian)
        self.ld50adj_avian = float(ld50adj_avian)
        ratio_sid_avian = sid_avian/ld50adj_avian
        return ratio_sid_avian

    # Level of Concern for avian droplet inhalation risk
    def LocSidAvian(self,ratio_sid_avian):
        if ratio_sid_avian < 0.1:
            return ('Exposure not Likely Significant')
        else:
            return ('Proceed to Refinements')

    # Ratio of mammalian vapor dose to adjusted inhalation LD50
    def RatioVdMammal(self,vid_mammal,ld50adj_mammal):
        self.vid_mammal = float(vid_mammal)
        self.ld50adj_mammal = float(ld50adj_mammal)
        ratio_vd_mammal = vid_mammal/ld50adj_mammal
        return vid_mammal/ld50adj_mammal

    # Level of Concern for mammalian vapor phase risk
    def LocVdMammal(self,ratio_vd_mammal):
        if ratio_vd_mammal < 0.1:
            return ('Exposure not Likely Significant')
        else:
            return ('Proceed to Refinements')

    # Ratio of mammalian droplet inhalation dose to adjusted inhalation LD50
    def RatioSidMammal(self,sid_mammal,ld50adj_mammal):
        self.sid_mammal = float(sid_mammal)
        self.ld50adj_mammal = float(ld50adj_mammal)
        ratio_sid_mammal = sid_mammal/ld50adj_mammal
        return ratio_sid_mammal

    # Level of Concern for mammaliam droplet inhalation risk
    def LocSidMammal(self,ratio_sid_mammal):
        if ratio_sid_mammal < 0.1:
            return ('Exposure not Likely Significant')
        else:
            return ('Proceed to Refinements')