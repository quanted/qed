#*********************************************************#
# @@ScriptName: orehe_model.py
# @@Author: Tao Hong
# @@Create Date: 2013-08-28
# @@Modify Date: 2013-09-06
#*********************************************************#
import numpy as np
import logging
import sys

#Inputs used by all scenarios, area is not included##
class orehe_chem(object):
    def __init__(self, actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                 inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm):
        self.actv_cm = actv_cm
        self.exdu_cm = exdu_cm
        self.der_pod_cm= float(der_pod_cm)
        self.der_pod_sor_cm = der_pod_sor_cm
        self.der_abs_cm = float(der_abs_cm)
        self.der_abs_sor_cm = der_abs_sor_cm
        self.der_loc_cm = float(der_loc_cm)

        self.inh_pod_cm = float(inh_pod_cm)
        self.inh_pod_sor_cm = inh_pod_sor_cm
        self.inh_abs_cm = float(inh_abs_cm)
        self.inh_loc_cm = float(inh_loc_cm)
        self.der_wt_cm = float(der_wt_cm)
        self.inh_wt_cm = float(inh_wt_cm)
        self.chd_wt_cm = float(chd_wt_cm)
        self.comb_cm = comb_cm

class orehe_ge(orehe_chem):
    def __init__(self, actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                 inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                 scna_gh, form_gh, apmd_gh, type_gh, aprt_gh, area_gh, deru_gh, inhu_gh):
        super (orehe_ge, self).__init__(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                       inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm)
        self.scna_gh = scna_gh
        self.form_gh = form_gh
        self.apmd_gh = apmd_gh
        self.type_gh = type_gh
        self.aprt_gh = float(aprt_gh)
        self.area_gh = float(area_gh)
        self.deru_gh = float(deru_gh)
        self.inhu_gh = float(inhu_gh)

        self.exp_ge_out = self.exp_ge(self.aprt_gh, self.area_gh, self.deru_gh, self.inhu_gh, self.der_abs_cm, self.der_wt_cm, self.inh_abs_cm, 
                                      self.inh_wt_cm, self.der_pod_cm, self.inh_pod_cm, self.comb_cm, self.der_loc_cm, self.inh_loc_cm)

    def exp_ge(self, aprt_gh, area_gh, deru_gh, inhu_gh, der_abs_cm, der_wt_cm, inh_abs_cm, 
            inh_wt_cm, der_pod_cm, inh_pod_cm, comb_cm, der_loc_cm, inh_loc_cm):
        der_exp = aprt_gh*area_gh*deru_gh
        inh_exp = aprt_gh*area_gh*inhu_gh
        der_abs_exp = der_exp*der_abs_cm/der_wt_cm
        inh_abs_exp = inh_exp*inh_abs_cm/inh_wt_cm
        der_moe = der_pod_cm/der_abs_exp
        inh_moe = inh_pod_cm/inh_abs_exp

        if comb_cm == 'No':
            comb_moe = 'N/A'
            ari = 'N/A'
        elif comb_cm == 'Combined (same LOCs)':
            comb_moe = 1.0/((1.0/der_moe)+(1.0/inh_moe))
            ari = 'N/A'
        elif comb_cm == 'ARI (different LOCs)':
            comb_moe = 'N/A'
            ari = 1.0/((der_loc_cm/der_moe)+(inh_loc_cm/inh_moe))

        return {'der_exp':der_exp, 'inh_exp':inh_exp, 'der_abs_exp':der_abs_exp, 
                'inh_abs_exp':inh_abs_exp, 'der_moe':der_moe, 'inh_moe':inh_moe, 
                'comb_moe':comb_moe, 'ari':ari}

class orehe_pp_ac(orehe_chem):
    def __init__(self, actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                 inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                 scna_pp_ac, form_pp_ac, apmd_pp_ac, wf_pp_ac, vl_pp_ac, pd_pp_ac, area_pp_ac, deru_pp_ac, inhu_pp_ac):
        super (orehe_pp_ac, self).__init__(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                       inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm)
        self.scna_pp_ac = scna_pp_ac
        self.form_pp_ac = form_pp_ac
        self.apmd_pp_ac = apmd_pp_ac
        self.wf_pp_ac = float(wf_pp_ac)
        self.vl_pp_ac = float(vl_pp_ac)
        self.pd_pp_ac = float(pd_pp_ac)
        self.area_pp_ac = float(area_pp_ac)
        self.deru_pp_ac = float(deru_pp_ac)
        self.inhu_pp_ac = float(inhu_pp_ac)

        self.exp_pp_ac_out = self.exp_pp_ac(self.wf_pp_ac, self.vl_pp_ac, self.pd_pp_ac, self.area_pp_ac, self.deru_pp_ac, self.inhu_pp_ac,
                                            self.der_abs_cm, self.inh_abs_cm, self.der_wt_cm, self.inh_wt_cm, self.der_pod_cm, self.inh_pod_cm, self.comb_cm, self.der_loc_cm, self.inh_loc_cm)

    def exp_pp_ac(self, wf_pp_ac, vl_pp_ac, pd_pp_ac, area_pp_ac, deru_pp_ac, inhu_pp_ac,
               der_abs_cm, inh_abs_cm, der_wt_cm, inh_wt_cm, der_pod_cm, inh_pod_cm, comb_cm, der_loc_cm, inh_loc_cm):
        aprt_pp_ac = wf_pp_ac*vl_pp_ac*pd_pp_ac*2.2*1e-3
        der_exp = aprt_pp_ac*deru_pp_ac*area_pp_ac
        inh_exp = aprt_pp_ac*inhu_pp_ac*area_pp_ac
        der_abs_exp = der_exp*der_abs_cm/der_wt_cm
        inh_abs_exp = inh_exp*inh_abs_cm/inh_wt_cm
        der_moe = der_pod_cm/der_abs_exp
        inh_moe = inh_pod_cm/inh_abs_exp
        inh_exp_cd = der_exp*der_abs_exp*der_moe

        if comb_cm == 'No':
            comb_moe = 'N/A'
            ari = 'N/A'
        elif comb_cm == 'Combined (same LOCs)':
            comb_moe = 1.0/((1.0/der_moe)+(1.0/inh_moe))
            ari = 'N/A'
        elif comb_cm == 'ARI (different LOCs)':
            comb_moe = 'N/A'
            ari = 1.0/((der_loc_cm/der_moe)+(inh_loc_cm/inh_moe))

        return {'der_exp':der_exp, 'inh_exp':inh_exp, 'der_abs_exp':der_abs_exp, 
                'inh_abs_exp':inh_abs_exp, 'der_moe':der_moe, 'inh_moe':inh_moe, 
                'inh_exp_cd':inh_exp_cd, 'comb_moe':comb_moe, 'ari':ari, 'aprt_pp_ac':aprt_pp_ac}

class orehe_tp_dp(orehe_chem):
    def __init__(self, actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                 inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                 scna_tp_dp, form_tp_dp, apmd_tp_dp, aai_tp_dp, aa_tp_dp, area_tp_dp, deru_tp_dp, inhu_tp_dp):
        super (orehe_tp_dp, self).__init__(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                       inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm)
        self.scna_tp_dp = scna_tp_dp
        self.form_tp_dp = form_tp_dp
        self.apmd_tp_dp = apmd_tp_dp
        self.aai_tp_dp = float(aai_tp_dp)/100.0
        self.aa_tp_dp = float(aa_tp_dp)
        self.area_tp_dp = float(area_tp_dp)
        self.deru_tp_dp = float(deru_tp_dp)
        self.inhu_tp_dp = float(inhu_tp_dp)

        self.exp_tp_dp_out = self.exp_tp_dp(self.aai_tp_dp, self.aa_tp_dp, self.area_tp_dp, self.deru_tp_dp, self.inhu_tp_dp,
                                            self.der_abs_cm, self.inh_abs_cm, self.der_wt_cm, self.inh_wt_cm, self.der_pod_cm, self.inh_pod_cm, self.comb_cm, self.der_loc_cm, self.inh_loc_cm)

    def exp_tp_dp(self, aai_tp_dp, aa_tp_dp, area_tp_dp, deru_tp_dp, inhu_tp_dp,
               der_abs_cm, inh_abs_cm, der_wt_cm, inh_wt_cm, der_pod_cm, inh_pod_cm, comb_cm, der_loc_cm, inh_loc_cm):
        aprt_tp_dp = (aai_tp_dp)*(aa_tp_dp/454.0)
        der_exp = aprt_tp_dp*deru_tp_dp*area_tp_dp
        inh_exp = aprt_tp_dp*inhu_tp_dp*area_tp_dp
        der_abs_exp = der_exp*der_abs_cm/der_wt_cm
        inh_abs_exp = inh_exp*inh_abs_cm/inh_wt_cm
        der_moe = der_pod_cm/der_abs_exp
        inh_moe = inh_pod_cm/inh_abs_exp
        inh_exp_cd = der_exp*der_abs_exp*der_moe

        if comb_cm == 'No':
            comb_moe = 'N/A'
            ari = 'N/A'
        elif comb_cm == 'Combined (same LOCs)':
            comb_moe = 1.0/((1.0/der_moe)+(1.0/inh_moe))
            ari = 'N/A'
        elif comb_cm == 'ARI (different LOCs)':
            comb_moe = 'N/A'
            ari = 1.0/((der_loc_cm/der_moe)+(inh_loc_cm/inh_moe))

        return {'der_exp':der_exp, 'inh_exp':inh_exp, 'der_abs_exp':der_abs_exp, 
                'inh_abs_exp':inh_abs_exp, 'der_moe':der_moe, 'inh_moe':inh_moe, 
                'inh_exp_cd':inh_exp_cd, 'comb_moe':comb_moe, 'ari':ari, 'aprt_tp_dp':aprt_tp_dp}


class orehe_oa(orehe_chem):
    def __init__(self, actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                 inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                 lab_oa, ai_oa, at_oz_oa, at_g_oa, at_ml_oa, den_oa, deru_oa, inhu_oa):
        super (orehe_oa, self).__init__(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                       inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm)
        self.lab_oa = lab_oa
        self.ai_oa = float(ai_oa)/100.0
        try:
            self.at_oz_oa = float(at_oz_oa)
        except:
            self.at_oz_oa = at_oz_oa
        try:
            self.at_g_oa = float(at_g_oa)
        except:
            self.at_g_oa = at_g_oa
        try:
            self.at_ml_oa = float(at_ml_oa)
            self.den_oa = float(den_oa)
        except:
            self.at_ml_oa = at_ml_oa
            self.den_oa = den_oa
        self.deru_oa = float(deru_oa)
        self.inhu_oa = float(inhu_oa)

        self.exp_oa_out = self.exp_oa(self.lab_oa, self.ai_oa, self.at_oz_oa, self.at_g_oa, self.at_ml_oa, self.den_oa, self.deru_oa, self.inhu_oa,
                                      self.der_abs_cm, self.inh_abs_cm, self.der_wt_cm, self.inh_wt_cm, self.der_pod_cm, self.inh_pod_cm, self.comb_cm, self.der_loc_cm, self.inh_loc_cm)

    def exp_oa(self, lab_oa, ai_oa, at_oz_oa, at_g_oa, at_ml_oa, den_oa, deru_oa, inhu_oa, 
               der_abs_cm, inh_abs_cm, der_wt_cm, inh_wt_cm, der_pod_cm, inh_pod_cm, comb_cm, der_loc_cm, inh_loc_cm):
        if lab_oa == 'oz':
            aprt_oa = at_oz_oa*ai_oa*(1.0/16)*1
        elif lab_oa == 'g':
            aprt_oa = at_g_oa*ai_oa*(1.0/454)*1
        elif lab_oa == 'ml':
            aprt_oa = at_ml_oa*ai_oa*(1.0/454)*den_oa*1
        der_exp = aprt_oa*deru_oa
        inh_exp = aprt_oa*inhu_oa
        der_abs_exp = der_exp*der_abs_cm/der_wt_cm
        inh_abs_exp = inh_exp*inh_abs_cm/inh_wt_cm
        der_moe = der_pod_cm/der_abs_exp
        inh_moe = inh_pod_cm/inh_abs_exp

        if comb_cm == 'No':
            comb_moe = 'N/A'
            ari = 'N/A'
        elif comb_cm == 'Combined (same LOCs)':
            comb_moe = 1.0/((1.0/der_moe)+(1.0/inh_moe))
            ari = 'N/A'
        elif comb_cm == 'ARI (different LOCs)':
            comb_moe = 'N/A'
            ari = 1.0/((der_loc_cm/der_moe)+(inh_loc_cm/inh_moe))

        return {'der_exp':der_exp, 'inh_exp':inh_exp, 'der_abs_exp':der_abs_exp, 
                'inh_abs_exp':inh_abs_exp, 'der_moe':der_moe, 'inh_moe':inh_moe, 
                'comb_moe':comb_moe, 'ari':ari, 'aprt_oa':aprt_oa}

class orehe_or(orehe_chem):
    def __init__(self, actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                 inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                 ai_or, ds_or, nd_or, den_or, dr_or, deru_or, inhu_or):
        super (orehe_or, self).__init__(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                       inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm)
        self.ai_or = float(ai_or)/100.0
        self.ds_or = float(ds_or)
        self.nd_or = float(nd_or)
        self.den_or = float(den_or)
        self.dr_or = float(dr_or)
        self.deru_or = float(deru_or)
        self.inhu_or = float(inhu_or)

        self.exp_or_out = self.exp_or(self.ai_or, self.ds_or, self.nd_or, self.den_or, self.dr_or, self.deru_or, self.inhu_or,
                                      self.der_abs_cm, self.inh_abs_cm, self.der_wt_cm, self.inh_wt_cm, self.der_pod_cm, self.inh_pod_cm, self.comb_cm, self.der_loc_cm, self.inh_loc_cm)

    def exp_or(self, ai_or, ds_or, nd_or, den_or, dr_or, deru_or, inhu_or,
               der_abs_cm, inh_abs_cm, der_wt_cm, inh_wt_cm, der_pod_cm, inh_pod_cm, comb_cm, der_loc_cm, inh_loc_cm):
        aprt_or = ds_or*ai_or*nd_or*den_or*dr_or
        der_exp = aprt_or*deru_or
        inh_exp = aprt_or*inhu_or
        der_abs_exp = der_exp*der_abs_cm/der_wt_cm
        inh_abs_exp = inh_exp*inh_abs_cm/inh_wt_cm
        der_moe = der_pod_cm/der_abs_exp
        inh_moe = inh_pod_cm/inh_abs_exp

        if comb_cm == 'No':
            comb_moe = 'N/A'
            ari = 'N/A'
        elif comb_cm == 'Combined (same LOCs)':
            comb_moe = 1.0/((1.0/der_moe)+(1.0/inh_moe))
            ari = 'N/A'
        elif comb_cm == 'ARI (different LOCs)':
            comb_moe = 'N/A'
            ari = 1.0/((der_loc_cm/der_moe)+(inh_loc_cm/inh_moe))

        return {'der_exp':der_exp, 'inh_exp':inh_exp, 'der_abs_exp':der_abs_exp, 
                'inh_abs_exp':inh_abs_exp, 'der_moe':der_moe, 'inh_moe':inh_moe, 
                'comb_moe':comb_moe, 'ari':ari, 'aprt_or':aprt_or}

class orehe_ab(orehe_chem):
    def __init__(self, actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                 inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm, 
                 ai_ab, ds_ab, nd_ab, den_ab, dr_ab, deru_ab, inhu_ab):
        super (orehe_ab, self).__init__(actv_cm, exdu_cm, der_pod_cm, der_pod_sor_cm, der_abs_cm, der_abs_sor_cm, der_loc_cm, 
                                       inh_pod_cm, inh_pod_sor_cm, inh_abs_cm, inh_loc_cm, der_wt_cm, inh_wt_cm, chd_wt_cm, comb_cm)
        self.ai_ab = float(ai_ab)/100.0
        self.ds_ab = float(ds_ab)
        self.nd_ab = float(nd_ab)
        self.den_ab = float(den_ab)
        self.dr_ab = float(dr_ab)
        self.deru_ab = float(deru_ab)
        self.inhu_ab = float(inhu_ab)

        self.exp_ab_out = self.exp_ab(self.ai_ab, self.ds_ab, self.nd_ab, self.den_ab, self.dr_ab, self.deru_ab, self.inhu_ab,
                                      self.der_abs_cm, self.inh_abs_cm, self.der_wt_cm, self.inh_wt_cm, self.der_pod_cm, self.inh_pod_cm, self.comb_cm, self.der_loc_cm, self.inh_loc_cm)

    def exp_ab(self, ai_ab, ds_ab, nd_ab, den_ab, dr_ab, deru_ab, inhu_ab,
               der_abs_cm, inh_abs_cm, der_wt_cm, inh_wt_cm, der_pod_cm, inh_pod_cm, comb_cm, der_loc_cm, inh_loc_cm):
        aprt_ab = ds_ab*ai_ab*nd_ab*den_ab*dr_ab
        der_exp = aprt_ab*deru_ab
        inh_exp = aprt_ab*inhu_ab
        der_abs_exp = der_exp*der_abs_cm/der_wt_cm
        inh_abs_exp = inh_exp*inh_abs_cm/inh_wt_cm
        der_moe = der_pod_cm/der_abs_exp
        inh_moe = inh_pod_cm/inh_abs_exp

        if comb_cm == 'No':
            comb_moe = 'N/A'
            ari = 'N/A'
        elif comb_cm == 'Combined (same LOCs)':
            comb_moe = 1.0/((1.0/der_moe)+(1.0/inh_moe))
            ari = 'N/A'
        elif comb_cm == 'ARI (different LOCs)':
            comb_moe = 'N/A'
            ari = 1.0/((der_loc_cm/der_moe)+(inh_loc_cm/inh_moe))

        return {'der_exp':der_exp, 'inh_exp':inh_exp, 'der_abs_exp':der_abs_exp, 
                'inh_abs_exp':inh_abs_exp, 'der_moe':der_moe, 'inh_moe':inh_moe, 
                'comb_moe':comb_moe, 'ari':ari, 'aprt_ab':aprt_ab}
