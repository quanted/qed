import numpy as np
import logging
import sys

########Hard Surface Floor Cleaner###
class resexposure_hd(object):
    def __init__(self, ar_hd, ai_hd, den_hd, cf1_hd, cf2_hd, fr_hd, tf_hd, sa_hd, da_hd, bw_hd, sa_h_hd, fq_hd, et_hd, se_hd):
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
        self.res_hd = self.hd(self.ar_hd, self.ai_hd, self.den_hd, self.cf1_hd, self.cf2_hd, self.fr_hd, self.tf_hd, self.sa_hd, self.da_hd, self.bw_hd, self.sa_h_hd, self.fq_hd, self.et_hd, self.se_hd)
        self.exp_der_hd = self.res_hd[0]
        self.exp_ora_hd = self.res_hd[1]
        self.dose_der_hd = self.res_hd[2]
        self.dose_ora_hd = self.res_hd[3]

    def hd(self, ar, ai, den, cf1, cf2, fr, tf, sa, da, bw, sa_h, fq, et, se):
        ar_adj = ((ai)*den/ar)*cf1*cf2
        exp_der = ar_adj*fr*tf*sa*da
        dose_der = exp_der/bw
        exp_ora = ar_adj*fr*tf*sa_h*fq*et*se
        dose_ora = exp_ora/bw
        return exp_der, exp_ora, dose_der, dose_ora

#######Vinyl Floor ########
class resexposure_vl(object):
    def __init__(self, wf_vl, den_vl, vt_vl, cf1_vl, af_vl, tf_vl, cf2_vl, bw_vl, sa_vl, da_vl, sa_h_vl, fq_vl, et_vl, se_vl):
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
        self.res_vl = self.vl(self.wf_vl, self.den_vl, self.vt_vl, self.cf1_vl, self.af_vl, self.tf_vl, self.cf2_vl, self.bw_vl, self.sa_vl, self.da_vl, self.sa_h_vl, self.fq_vl, self.et_vl, self.se_vl)
        self.exp_der_vl = self.res_vl[0]
        self.exp_ora_vl = self.res_vl[1]
        self.dose_der_vl = self.res_vl[2]
        self.dose_ora_vl = self.res_vl[3]

    def vl(self, wf_vl, den_vl, vt_vl, cf1_vl, af_vl, tf_vl, cf2_vl, bw_vl, sa_vl, da_vl, sa_h_vl, fq_vl, et_vl, se_vl):
        exp_der = wf_vl*den_vl*vt_vl*cf1_vl*af_vl*tf_vl*sa_vl*cf2_vl*da_vl
        dose_der = exp_der/bw_vl
        exp_ora = wf_vl*den_vl*vt_vl*cf1_vl*af_vl*tf_vl*sa_h_vl*fq_vl*se_vl*et_vl*cf2_vl
        dose_ora = exp_ora/bw_vl
        return exp_der, exp_ora, dose_der, dose_ora

########Carpet Cleaner###########
class resexposure_cc(object):
    def __init__(self, ar_cc, ai_cc, den_cc, cf1_cc, cf2_cc, fr_cc, tf_cc, sa_cc, da_cc, bw_cc, sa_h_cc, fq_cc, et_cc, se_cc):
        self.ar_cc = float(ar_cc)
        self.ai_cc = float(ai_cc)
        self.den_cc = float(den_cc)
        self.cf1_cc = float(cf1_cc)
        self.cf2_cc = float(cf2_cc)
        self.fr_cc = float(fr_cc)
        self.tf_cc = float(tf_cc)
        self.sa_cc = float(sa_cc)
        self.da_cc = float(da_cc)
        self.bw_cc = float(bw_cc)
        self.sa_h_cc = float(sa_h_cc)
        self.fq_cc = float(fq_cc)
        self.et_cc = float(et_cc)
        self.se_cc = float(se_cc)
        self.res_cc = self.cc(self.ar_cc, self.ai_cc, self.den_cc, self.cf1_cc, self.cf2_cc, self.fr_cc, self.tf_cc, self.sa_cc, self.da_cc, self.bw_cc, self.sa_h_cc, self.fq_cc, self.et_cc, self.se_cc)
        self.exp_der_cc = self.res_cc[0]
        self.exp_ora_cc = self.res_cc[1]
        self.dose_der_cc = self.res_cc[2]
        self.dose_ora_cc = self.res_cc[3]

    def cc(self, ar_cc, ai_cc, den_cc, cf1_cc, cf2_cc, fr_cc, tf_cc, sa_cc, da_cc, bw_cc, sa_h_cc, fq_cc, et_cc, se_cc):
        ar_adj = ((ai_cc)*den_cc/ar_cc)*cf1_cc*cf2_cc
        exp_der = ar_adj*fr_cc*tf_cc*sa_cc*da_cc
        dose_der = exp_der/bw_cc
        exp_ora = ar_adj*fr_cc*tf_cc*sa_h_cc*fq_cc*et_cc*se_cc
        dose_ora = exp_ora/bw_cc
        return exp_der, exp_ora, dose_der, dose_ora

########Impregnated Carpet###########
class resexposure_ic(object):
    def __init__(self, den_ic, wf_ic, tf_ic, bw_ic, sa_ic, da_ic, sa_h_ic, fq_ic, et_ic, se_ic):
        self.den_ic = float(den_ic)
        self.wf_ic = float(wf_ic)
        self.tf_ic = float(tf_ic)
        self.bw_ic = float(bw_ic)
        self.sa_ic = float(sa_ic)
        self.da_ic = float(da_ic)
        self.sa_h_ic = float(sa_h_ic)
        self.fq_ic = float(fq_ic)
        self.et_ic = float(et_ic)
        self.se_ic = float(se_ic)
        self.res_ic = self.ic(self.den_ic, self.wf_ic, self.tf_ic, self.bw_ic, self.sa_ic, self.da_ic, self.sa_h_ic, self.fq_ic, self.et_ic, self.se_ic)
        self.exp_der_ic = self.res_ic[0]
        self.exp_ora_ic = self.res_ic[1]
        self.dose_der_ic = self.res_ic[2]
        self.dose_ora_ic = self.res_ic[3]

    def ic(self, den_ic, wf_ic, tf_ic, bw_ic, sa_ic, da_ic, sa_h_ic, fq_ic, et_ic, se_ic):
        exp_der = den_ic*wf_ic*tf_ic*sa_ic*da_ic
        dose_der = exp_der/bw_ic
        exp_ora = den_ic*wf_ic*tf_ic*sa_h_ic*fq_ic*et_ic*se_ic
        dose_ora = exp_ora/bw_ic
        return exp_der, exp_ora, dose_der, dose_ora

########Mattress###########
class resexposure_mt(object):
    def __init__(self, wf_mt, den_mt, tf_mt, bw_mt, pf_mt, sa_mt, da_mt):
        self.wf_mt = float(wf_mt)
        self.den_mt = float(den_mt)
        self.tf_mt = float(tf_mt)
        self.bw_mt = float(bw_mt)
        self.pf_mt = float(pf_mt)
        self.sa_mt = float(sa_mt)
        self.da_mt = float(da_mt)
        self.res_mt = self.mt(self.wf_mt, self.den_mt, self.tf_mt, self.bw_mt, self.pf_mt, self.sa_mt, self.da_mt)
        self.exp_der_mt = self.res_mt[0]
        self.dose_der_mt = self.res_mt[1]

    def mt(self, wf_mt, den_mt, tf_mt, bw_mt, pf_mt, sa_mt, da_mt):
        exp_der = wf_mt*den_mt*tf_mt*pf_mt*sa_mt*da_mt
        dose_der = exp_der/bw_mt
        return exp_der, dose_der

########Clothing/Textile Consumer Product Spray Treatment###########
class resexposure_ct(object):
    def __init__(self, wa_ct, wf_ct, bw_ct, tf_ct, sa_ct, da_ct, sa_m_ct, se_ct):
        self.wa_ct = float(wa_ct)
        self.wf_ct = float(wf_ct)
        self.bw_ct = float(bw_ct)
        self.tf_ct = float(tf_ct)
        self.sa_ct = float(sa_ct)
        self.da_ct = float(da_ct)
        self.sa_m_ct = float(sa_m_ct)
        self.se_ct = float(se_ct)
        self.res_ct = self.ct(self.wa_ct, self.wf_ct, self.bw_ct, self.tf_ct, self.sa_ct, self.da_ct, self.sa_m_ct, self.se_ct)
        self.exp_der_ct = self.res_ct[0]
        self.exp_ora_ct = self.res_ct[1]
        self.dose_der_ct = self.res_ct[2]
        self.dose_ora_ct = self.res_ct[3]

    def ct(self, wa_ct, wf_ct, bw_ct, tf_ct, sa_ct, da_ct, sa_m_ct, se_ct):
        exp_der = wa_ct*wf_ct*tf_ct*sa_ct*da_ct
        dose_der = exp_der/bw_ct
        exp_ora = wa_ct*wf_ct*sa_m_ct*se_ct
        dose_ora = exp_ora/bw_ct
        return exp_der, exp_ora, dose_der, dose_ora

########Laundry Detergent Preservative###########
class resexposure_lp(object):
    def __init__(self, ap_lp, wf_lp, den_lp, wfd_lp, tw_lp, bw_lp, sa_lp, tf_cs_lp, tf_r_lp, da_lp, sa_m_lp, se_lp):
        self.ap_lp = float(ap_lp)
        self.wf_lp = float(wf_lp)
        self.den_lp = float(den_lp)
        self.wfd_lp = float(wfd_lp)
        self.tw_lp = float(tw_lp)
        self.bw_lp = float(bw_lp)
        self.sa_lp = float(sa_lp)
        self.tf_cs_lp = float(tf_cs_lp)
        self.tf_r_lp = float(tf_r_lp)
        self.da_lp = float(da_lp)
        self.sa_m_lp = float(sa_m_lp)
        self.se_lp = float(se_lp)
        self.res_lp = self.lp(self.ap_lp, self.wf_lp, self.den_lp, self.wfd_lp, self.tw_lp, self.bw_lp, self.sa_lp, self.tf_cs_lp, self.tf_r_lp, self.da_lp, self.sa_m_lp, self.se_lp)
        self.exp_der_lp = self.res_lp[0]
        self.exp_ora_lp = self.res_lp[1]
        self.dose_der_lp = self.res_lp[2]
        self.dose_ora_lp = self.res_lp[3]

    def lp(self, ap_lp, wf_lp, den_lp, wfd_lp, tw_lp, bw_lp, sa_lp, tf_cs_lp, tf_r_lp, da_lp, sa_m_lp, se_lp):
        exp_der = (ap_lp*wf_lp*den_lp*wfd_lp/tw_lp)*(sa_lp*tf_cs_lp*tf_r_lp*da_lp)
        dose_der = exp_der/bw_lp
        exp_ora = (ap_lp*wf_lp*den_lp*wfd_lp/tw_lp)*(sa_m_lp*se_lp)
        dose_ora = exp_ora/bw_lp
        return exp_der, exp_ora, dose_der, dose_ora

########Clothing/Textile Material Preservative###########
class resexposure_cp(object):
    def __init__(self, den_cp, wf_cp, bw_cp, tf_cs_cp, sa_cp, da_cp, sa_m_cp, se_cp):
        self.den_cp = float(den_cp)
        self.wf_cp = float(wf_cp)
        self.bw_cp = float(bw_cp)
        self.tf_cs_cp = float(tf_cs_cp)
        self.sa_cp = float(sa_cp)
        self.da_cp = float(da_cp)
        self.sa_m_cp = float(sa_m_cp)
        self.se_cp = float(se_cp)
        self.res_cp = self.cp(self.den_cp, self.wf_cp, self.bw_cp, self.tf_cs_cp, self.sa_cp, self.da_cp, self.sa_m_cp, self.se_cp)
        self.exp_der_cp = self.res_cp[0]
        self.exp_ora_cp = self.res_cp[1]
        self.dose_der_cp = self.res_cp[2]
        self.dose_ora_cp = self.res_cp[3]

    def cp(self, den_cp, wf_cp, bw_cp, tf_cs_cp, sa_cp, da_cp, sa_m_cp, se_cp):
        exp_der = den_cp*wf_cp*tf_cs_cp*sa_cp*da_cp
        dose_der = exp_der/bw_cp
        exp_ora = den_cp*wf_cp*sa_m_cp*se_cp
        dose_ora = exp_ora/bw_cp
        return exp_der, exp_ora, dose_der, dose_ora

########Impregnated Diapers###########
class resexposure_id(object):
    def __init__(self, am_id, wf_id, tf_id, fq_id, da_id, bw_id):
        self.am_id = float(am_id)
        self.wf_id = float(wf_id)
        self.tf_id = float(tf_id)
        self.fq_id = float(fq_id)
        self.da_id = float(da_id)
        self.bw_id = float(bw_id)
        self.res_id = self.id(self.am_id, self.wf_id, self.tf_id, self.fq_id, self.da_id, self.bw_id)
        self.exp_der_id = self.res_id[0]
        self.dose_der_id = self.res_id[1]

    def id(self, am_id, wf_id, tf_id, fq_id, da_id, bw_id):
        cf = 1000 #conversion factor  (mg/g)
        exp_der = am_id*wf_id*tf_id*fq_id*da_id*cf
        dose_der = exp_der/bw_id
        return exp_der, dose_der

########Cloth Diaper Spray Treatment###########
class resexposure_sd(object):
    def __init__(self, ar_sd, wf_sd, tf_sd, sa_sd, fq_sd, da_sd, bw_sd):
        self.ar_sd = float(ar_sd)
        self.wf_sd = float(wf_sd)
        self.tf_sd = float(tf_sd)
        self.sa_sd = float(sa_sd)
        self.fq_sd = float(fq_sd)
        self.da_sd = float(da_sd)
        self.bw_sd = float(bw_sd)
        self.res_sd = self.sd(self.ar_sd, self.wf_sd, self.tf_sd, self.sa_sd, self.fq_sd, self.da_sd, self.bw_sd)
        self.exp_der_sd = self.res_sd[0]
        self.dose_der_sd = self.res_sd[1]

    def sd(self, ar_sd, wf_sd, tf_sd, sa_sd, fq_sd, da_sd, bw_sd):
        exp_der = ar_sd*wf_sd*tf_sd*sa_sd*fq_sd*da_sd
        dose_der = exp_der/bw_sd
        return exp_der, dose_der

########Impregnated Polymer###########
class resexposure_ip(object):
    def __init__(self, wf_ip, wt_ip, fr_sa_ip, sa_ip, sa_m_ip, se_ip, bw_ip):
        self.wf_ip = float(wf_ip)
        self.wt_ip = float(wt_ip)
        self.fr_sa_ip = float(fr_sa_ip)
        self.sa_ip = float(sa_ip)
        self.sa_m_ip = float(sa_m_ip)
        self.se_ip = float(se_ip)
        self.bw_ip = float(bw_ip)
        self.res_ip = self.ip(self.wf_ip, self.wt_ip, self.fr_sa_ip, self.sa_ip, self.sa_m_ip, self.se_ip, self.bw_ip)
        self.exp_der_ip = self.res_ip[0]
        self.dose_der_ip = self.res_ip[1]

    def ip(self, wf_ip, wt_ip, fr_sa_ip, sa_ip, sa_m_ip, se_ip, bw_ip):
        cf = 1000 #conversion factor  (mg/g)
        sr = wf_ip*wt_ip*cf*fr_sa_ip/sa_ip
        exp_der = sr*se_ip*sa_m_ip
        dose_der = exp_der/bw_ip
        return exp_der, dose_der


