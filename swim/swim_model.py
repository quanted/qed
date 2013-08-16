import numpy as np
import logging
import sys


#food intake for birds
class swim(object):
    def __init__(self, chemical_name, log_kow, mw, hlc, r, T, cw, noael, 
                 bw_aa, bw_fa, sa_a_c, sa_a_nc, et_a_c, et_a_nc, ir_a_c, ir_a_nc, igr_a_c, igr_a_nc, 
                 bw_c1, sa_c1_c, sa_c1_nc, et_c1_c, et_c1_nc, ir_c1_c, ir_c1_nc, igr_c1_c, igr_c1_nc, 
                 bw_c2, sa_c2_c, sa_c2_nc, et_c2_c, et_c2_nc, ir_c2_c, ir_c2_nc, igr_c2_c, igr_c2_nc):
        self.chemical_name = chemical_name
        self.log_kow = float(log_kow)
        self.mw = float(mw)
        self.hlc = float(hlc)
        self.r = float(r)
        self.T = float(T)
        self.cw = float(cw)
        self.noael = float(noael)

        self.bw_aa = float(bw_aa)
        self.bw_fa = float(bw_fa)
        self.sa_a_c = float(sa_a_c)
        self.sa_a_nc = float(sa_a_nc)
        self.et_a_c = float(et_a_c)
        self.et_a_nc = float(et_a_nc)
        self.ir_a_c = float(ir_a_c)
        self.ir_a_nc = float(ir_a_nc)
        self.igr_a_c = float(igr_a_c)
        self.igr_a_nc = float(igr_a_nc)

        self.bw_c1 = float(bw_c1)
        self.sa_c1_c = float(sa_c1_c)
        self.sa_c1_nc = float(sa_c1_nc)
        self.et_c1_c = float(et_c1_c)
        self.et_c1_nc = float(et_c1_nc)
        self.ir_c1_c = float(ir_c1_c)
        self.ir_c1_nc = float(ir_c1_nc)
        self.igr_c1_c = float(igr_c1_c)
        self.igr_c1_nc = float(igr_c1_nc)

        self.bw_c2 = float(bw_c2)
        self.sa_c2_c = float(sa_c2_c)
        self.sa_c2_nc = float(sa_c2_nc)
        self.et_c2_c = float(et_c2_c)
        self.et_c2_nc = float(et_c2_nc)
        self.ir_c2_c = float(ir_c2_c)
        self.ir_c2_nc = float(ir_c2_nc)
        self.igr_c2_c = float(igr_c2_c)
        self.igr_c2_nc = float(igr_c2_nc)

        #Inhalation
        self.inh_c_aa = self.inh(self.hlc, self.r, self.T, self.cw, self.et_a_c, self.ir_a_c, self.bw_aa, self.noael)[0]
        self.inh_c_fa = self.inh(self.hlc, self.r, self.T, self.cw, self.et_a_c, self.ir_a_c, self.bw_fa, self.noael)[0]
        self.inh_c_c1 = self.inh(self.hlc, self.r, self.T, self.cw, self.et_c1_c, self.ir_c1_c, self.bw_c1, self.noael)[0]
        self.inh_c_c2 = self.inh(self.hlc, self.r, self.T, self.cw, self.et_c2_c, self.ir_c2_c, self.bw_c2, self.noael)[0]
        self.inh_nc_aa = self.inh(self.hlc, self.r, self.T, self.cw, self.et_a_nc, self.ir_a_nc, self.bw_aa, self.noael)[0]
        self.inh_nc_fa = self.inh(self.hlc, self.r, self.T, self.cw, self.et_a_nc, self.ir_a_nc, self.bw_fa, self.noael)[0]
        self.inh_nc_c1 = self.inh(self.hlc, self.r, self.T, self.cw, self.et_c1_nc, self.ir_c1_nc, self.bw_c1, self.noael)[0]
        self.inh_nc_c2 = self.inh(self.hlc, self.r, self.T, self.cw, self.et_c2_nc, self.ir_c2_nc, self.bw_c2, self.noael)[0]

        self.inh_c_aa_moe = self.inh(self.hlc, self.r, self.T, self.cw, self.et_a_c, self.ir_a_c, self.bw_aa, self.noael)[1]
        self.inh_c_fa_moe = self.inh(self.hlc, self.r, self.T, self.cw, self.et_a_c, self.ir_a_c, self.bw_fa, self.noael)[1]
        self.inh_c_c1_moe = self.inh(self.hlc, self.r, self.T, self.cw, self.et_c1_c, self.ir_c1_c, self.bw_c1, self.noael)[1]
        self.inh_c_c2_moe = self.inh(self.hlc, self.r, self.T, self.cw, self.et_c2_c, self.ir_c2_c, self.bw_c2, self.noael)[1]
        self.inh_nc_aa_moe = self.inh(self.hlc, self.r, self.T, self.cw, self.et_a_nc, self.ir_a_nc, self.bw_aa, self.noael)[1]
        self.inh_nc_fa_moe = self.inh(self.hlc, self.r, self.T, self.cw, self.et_a_nc, self.ir_a_nc, self.bw_fa, self.noael)[1]
        self.inh_nc_c1_moe = self.inh(self.hlc, self.r, self.T, self.cw, self.et_c1_nc, self.ir_c1_nc, self.bw_c1, self.noael)[1]
        self.inh_nc_c2_moe = self.inh(self.hlc, self.r, self.T, self.cw, self.et_c2_nc, self.ir_c2_nc, self.bw_c2, self.noael)[1]


        #Ingestion
        self.ing_c_aa = self.ing(self.cw, self.igr_a_c, self.et_a_c, self.bw_aa, self.noael)[0]
        self.ing_c_fa = self.ing(self.cw, self.igr_a_c, self.et_a_c, self.bw_fa, self.noael)[0]
        self.ing_c_c1 = self.ing(self.cw, self.igr_c1_c, self.et_c1_c, self.bw_c1, self.noael)[0]
        self.ing_c_c2 = self.ing(self.cw, self.igr_c2_c, self.et_c2_c, self.bw_c2, self.noael)[0]
        self.ing_nc_aa = self.ing(self.cw, self.igr_a_nc, self.et_a_nc, self.bw_aa, self.noael)[0]
        self.ing_nc_fa = self.ing(self.cw, self.igr_a_nc, self.et_a_nc, self.bw_fa, self.noael)[0]
        self.ing_nc_c1 = self.ing(self.cw, self.igr_c1_nc, self.et_c1_nc, self.bw_c1, self.noael)[0]
        self.ing_nc_c2 = self.ing(self.cw, self.igr_c2_nc, self.et_c2_nc, self.bw_c2, self.noael)[0]

        self.ing_c_aa_moe = self.ing(self.cw, self.igr_a_c, self.et_a_c, self.bw_aa, self.noael)[1]
        self.ing_c_fa_moe = self.ing(self.cw, self.igr_a_c, self.et_a_c, self.bw_fa, self.noael)[1]
        self.ing_c_c1_moe = self.ing(self.cw, self.igr_c1_c, self.et_c1_c, self.bw_c1, self.noael)[1]
        self.ing_c_c2_moe = self.ing(self.cw, self.igr_c2_c, self.et_c2_c, self.bw_c2, self.noael)[1]
        self.ing_nc_aa_moe = self.ing(self.cw, self.igr_a_nc, self.et_a_nc, self.bw_aa, self.noael)[1]
        self.ing_nc_fa_moe = self.ing(self.cw, self.igr_a_nc, self.et_a_nc, self.bw_fa, self.noael)[1]
        self.ing_nc_c1_moe = self.ing(self.cw, self.igr_c1_nc, self.et_c1_nc, self.bw_c1, self.noael)[1]
        self.ing_nc_c2_moe = self.ing(self.cw, self.igr_c2_nc, self.et_c2_nc, self.bw_c2, self.noael)[1]

        #Dermal
        self.der_c_aa = self.der(self.cw, self.log_kow, self.mw, self.sa_a_c, self.et_a_c, self.bw_aa, self.noael)[0]
        self.der_c_fa = self.der(self.cw, self.log_kow, self.mw, self.sa_a_c, self.et_a_c, self.bw_fa, self.noael)[0]
        self.der_c_c1 = self.der(self.cw, self.log_kow, self.mw, self.sa_c1_c, self.et_c1_c, self.bw_c1, self.noael)[0]
        self.der_c_c2 = self.der(self.cw, self.log_kow, self.mw, self.sa_c2_c, self.et_c2_c, self.bw_c2, self.noael)[0]
        self.der_nc_aa = self.der(self.cw, self.log_kow, self.mw, self.sa_a_nc, self.et_a_nc, self.bw_aa, self.noael)[0]
        self.der_nc_fa = self.der(self.cw, self.log_kow, self.mw, self.sa_a_nc, self.et_a_nc, self.bw_fa, self.noael)[0]
        self.der_nc_c1 = self.der(self.cw, self.log_kow, self.mw, self.sa_c1_nc, self.et_c1_nc, self.bw_c1, self.noael)[0]
        self.der_nc_c2 = self.der(self.cw, self.log_kow, self.mw, self.sa_c2_nc, self.et_c2_nc, self.bw_c2, self.noael)[0]

        self.der_c_aa_moe = self.der(self.cw, self.log_kow, self.mw, self.sa_a_c, self.et_a_c, self.bw_aa, self.noael)[1]
        self.der_c_fa_moe = self.der(self.cw, self.log_kow, self.mw, self.sa_a_c, self.et_a_c, self.bw_fa, self.noael)[1]
        self.der_c_c1_moe = self.der(self.cw, self.log_kow, self.mw, self.sa_c1_c, self.et_c1_c, self.bw_c1, self.noael)[1]
        self.der_c_c2_moe = self.der(self.cw, self.log_kow, self.mw, self.sa_c2_c, self.et_c2_c, self.bw_c2, self.noael)[1]
        self.der_nc_aa_moe = self.der(self.cw, self.log_kow, self.mw, self.sa_a_nc, self.et_a_nc, self.bw_aa, self.noael)[1]
        self.der_nc_fa_moe = self.der(self.cw, self.log_kow, self.mw, self.sa_a_nc, self.et_a_nc, self.bw_fa, self.noael)[1]
        self.der_nc_c1_moe = self.der(self.cw, self.log_kow, self.mw, self.sa_c1_nc, self.et_c1_nc, self.bw_c1, self.noael)[1]
        self.der_nc_c2_moe = self.der(self.cw, self.log_kow, self.mw, self.sa_c2_nc, self.et_c2_nc, self.bw_c2, self.noael)[1]
 

##Inhalation###
    def inh(self, hlc, r, T, cw, et, ir, bw, noael):
        henry_ulss = hlc/(r*(T+273))
        cf = 1000 #conversion factor 
        cvp = cw*henry_ulss*cf
        prd_inh = cvp*et*ir/bw
        prd_inh_moe = noael/prd_inh
        return prd_inh, prd_inh_moe

##Ingestion########
    def ing(self, cw, igr, et, bw, noael):
        prd_ing = cw*igr*et/bw
        prd_ing_moe = noael/prd_ing
        return prd_ing, prd_ing_moe

##Dermal########
    def der(self, cw, log_kow, mw, sa, et, bw, noael):
        log_kp = -2.72+(0.71*log_kow)-(0.0061*mw)
        kp = 10**log_kp
        cf_der=0.001    #conversion factor (L/cm3)
        prd_der = cw*sa*et*kp*cf_der/bw
        prd_der_moe = noael/prd_der
        return prd_der, prd_der_moe


# ss=swim('test', 1, 10, 1, 1, 1, 1, 1, 
#            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
#            1, 1, 1, 1, 1, 1, 1, 1, 1, 
#            1, 1, 1, 1, 1, 1, 1, 1, 1)

# print ss.der_c_aa