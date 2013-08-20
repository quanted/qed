import numpy as np
import logging
import sys

class resexposure(object):
    def __init__(self, model, ar_hd, ai_hd, den_hd, cf1_hd, cf2_hd, fr_hd, tf_hd, sa_hd, da_hd, bw_hd, sa_h_hd, fq_hd, et_hd, se_hd,
                 wf_vl, den_vl, vt_vl, cf1_vl, af_vl, tf_vl, cf2_vl, bw_vl, sa_vl, da_vl, sa_h_vl, fq_vl, et_vl, se_vl):
        self.model = model
        #Hard Surface Floor Cleaner###
        self.ar_hd = float(ar_hd)
        self.ai_hd = float(ai_hd)
        self.den_hd = float(den_hd)
        self.cf1_hd = float(cf1_hd)
        self.cf2_hd = float(cf2_hd)
        self.fr_hd = float(fr_hd)
        self.tf_hd = float(tf_hd)
        self.sa_hd = float(sa_hd)
        self.da_hd = float(da_hd)
        self.bw_hd = float(bw_hd)
        self.sa_h_hd = float(sa_h_hd)
        self.fq_hd = float(fq_hd)
        self.et_hd = float(et_hd)
        self.se_hd = float(se_hd)

#######Vinyl Floor ########
        self.wf_vl = float(wf_vl)
        self.den_vl = float(den_vl)
        self.vt_vl = float(vt_vl)
        self.cf1_vl = float(cf1_vl)
        self.af_vl = float(af_vl)
        self.tf_vl = float(tf_vl)
        self.cf2_vl = float(cf2_vl)
        self.bw_vl = float(bw_vl)
        self.sa_vl = float(sa_vl)
        self.da_vl = float(da_vl)
        self.sa_h_vl = float(sa_h_vl)
        self.fq_vl = float(fq_vl)
        self.et_vl = float(et_vl)
        self.se_vl = float(se_vl)

########Hard Surface Floor Cleaner
        self.hdflr_der = self.hdflr(self.ar_hd, self.ai_hd, self.den_hd, self.cf1_hd, self.cf2_hd, self.fr_hd, self.tf_hd, self.sa_hd, self.da_hd, self.bw_hd, self.sa_h_hd, self.fq_hd, self.et_hd, self.se_hd)[0]
        self.hdflr_ora = self.hdflr(self.ar_hd, self.ai_hd, self.den_hd, self.cf1_hd, self.cf2_hd, self.fr_hd, self.tf_hd, self.sa_hd, self.da_hd, self.bw_hd, self.sa_h_hd, self.fq_hd, self.et_hd, self.se_hd)[1]

#######Vinyl Floor ########
        self.vlflr_der = self.vlflr(self.wf_vl, self.den_vl, self.vt_vl, self.cf1_vl, self.af_vl, self.tf_vl, self.cf2_vl, self.bw_vl, self.sa_vl, self.da_vl, self.sa_h_vl, self.fq_vl, self.et_vl, self.se_vl)[0]
        self.vlflr_ora = self.vlflr(self.wf_vl, self.den_vl, self.vt_vl, self.cf1_vl, self.af_vl, self.tf_vl, self.cf2_vl, self.bw_vl, self.sa_vl, self.da_vl, self.sa_h_vl, self.fq_vl, self.et_vl, self.se_vl)[1]




#######Hard Surface Floor Cleaner########
    def hdflr(self, ar, ai, den, cf1, cf2, fr, tf, sa, da, bw, sa_h, fq, et, se):
        ar_adj = ((ai/100)*den/ar)*cf1*cf2
        exp_der = ar_adj*fr*tf*sa*da
        dose_der = exp_der/bw
        exp_ora = ar_adj*fr*tf*sa_h*fq*et*se
        dose_ora = exp_ora/bw
        return dose_der, dose_ora

#######Vinyl Floor ########
    def vlflr(self, wf_vl, den_vl, vt_vl, cf1_vl, af_vl, tf_vl, cf2_vl, bw_vl, sa_vl, da_vl, sa_h_vl, fq_vl, et_vl, se_vl):
        exp_der = wf_vl*den_vl*vt_vl*cf1_vl*af_vl*tf_vl*sa_vl*cf2_vl*da_vl
        dose_der = exp_der/bw_vl
        exp_ora = wf_vl*den_vl*vt_vl*cf1_vl*af_vl*tf_vl*sa_h_vl*fq_vl*se_vl*et_vl*cf2_vl
        dose_ora = exp_ora/bw_vl
        return dose_der, dose_ora

ss=resexposure('hdflr', 1000, 0.1, 8.35, 454000, 1.08e-3, 0.25, 1, 6600, 1, 15, 20, 20, 4, 0.5,
               0.001, 1.3, 3, 0.001, 0.005, 1, 1000, 15, 6600, 1, 20, 20, 4, 0.5)

print ss.hdflr_der
print ss.hdflr_ora

print ss.vlflr_der
print ss.vlflr_ora