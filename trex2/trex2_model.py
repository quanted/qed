import numpy as np
import logging
import sys
import time, datetime
logger = logging.getLogger('trex2 model')


#food intake for birds
class trex2(object):
    def __init__(self, run_type, chem_name, use, formu_name, a_i, Application_type, seed_treatment_formulation_name, seed_crop, seed_crop_v, r_s, b_w, p_i, den, h_l, n_a, ar_lb, day_out,
              ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, aw_bird_sm, aw_bird_md, aw_bird_lg, 
              Species_of_the_tested_bird_avian_ld50, Species_of_the_tested_bird_avian_lc50, Species_of_the_tested_bird_avian_NOAEC, Species_of_the_tested_bird_avian_NOAEL, 
              tw_bird_ld50, tw_bird_lc50, tw_bird_NOAEC, tw_bird_NOAEL, x, ld50_mamm, lc50_mamm, NOAEC_mamm, NOAEL_mamm, aw_mamm_sm, aw_mamm_md, aw_mamm_lg, tw_mamm,
              m_s_r_p):
        ts = datetime.datetime.now()
        if(time.daylight):
            ts1 = datetime.timedelta(hours=-4)+ts
        else:
            ts1 = datetime.timedelta(hours=-5)+ts
        self.jid = ts1.strftime('%Y%m%d%H%M%S%f')

        self.run_type=run_type
        self.chem_name=chem_name
        self.use=use
        self.formu_name=formu_name
        self.a_i=a_i
        self.a_i_t1=100*float(a_i)
        self.Application_type=Application_type
        self.seed_treatment_formulation_name=seed_treatment_formulation_name
        self.seed_crop=seed_crop
        self.seed_crop_v=seed_crop_v
        self.r_s=r_s
        self.b_w=b_w
        self.b_w_t1=12*float(b_w)
        self.p_i=p_i
        try:
            self.p_i_t1=100*float(p_i)
        except:
            self.p_i_t1='N/A'
        self.den=den
        self.h_l=h_l
        self.n_a=n_a
        self.ar_lb=ar_lb
        self.day_out=day_out
        self.ld50_bird=ld50_bird
        self.lc50_bird=lc50_bird
        self.NOAEC_bird=NOAEC_bird
        self.NOAEL_bird=NOAEL_bird
        self.aw_bird_sm=aw_bird_sm
        self.aw_bird_md=aw_bird_md
        self.aw_bird_lg=aw_bird_lg

        self.Species_of_the_tested_bird_avian_ld50=Species_of_the_tested_bird_avian_ld50
        self.Species_of_the_tested_bird_avian_lc50=Species_of_the_tested_bird_avian_lc50
        self.Species_of_the_tested_bird_avian_NOAEC=Species_of_the_tested_bird_avian_NOAEC
        self.Species_of_the_tested_bird_avian_NOAEL=Species_of_the_tested_bird_avian_NOAEL

        self.tw_bird_ld50=tw_bird_ld50
        self.tw_bird_lc50=tw_bird_lc50
        self.tw_bird_NOAEC=tw_bird_NOAEC
        self.tw_bird_NOAEL=tw_bird_NOAEL
        self.x=x
        self.ld50_mamm=ld50_mamm
        self.lc50_mamm=lc50_mamm
        self.NOAEC_mamm=NOAEC_mamm
        self.NOAEL_mamm=NOAEL_mamm
        self.aw_mamm_sm=aw_mamm_sm
        self.aw_mamm_md=aw_mamm_md
        self.aw_mamm_lg=aw_mamm_lg
        self.tw_mamm=tw_mamm
        self.m_s_r_p=m_s_r_p

        #Table5
        self.sa_bird_1_s = self.sa_bird_1(ar_lb[0], a_i, den, self.at_bird, self.fi_bird, 0.1, ld50_bird, aw_bird_sm, tw_bird_ld50, x, 0.02) 
        self.sa_bird_2_s = self.sa_bird_2(ar_lb[0], a_i, den, m_s_r_p, self.at_bird, ld50_bird, aw_bird_sm, tw_bird_ld50, x, 0.02) 
        self.sc_bird_s = self.sc_bird(ar_lb[0], a_i, den, NOAEC_bird)
        self.sa_mamm_1_s = self.sa_mamm_1(ar_lb[0], a_i, den, self.at_mamm, self.fi_mamm, 0.1, ld50_mamm, aw_mamm_sm, tw_mamm, 0.015)
        self.sa_mamm_2_s = self.sa_mamm_2(ar_lb[0], a_i, den, m_s_r_p, self.at_mamm, ld50_mamm, aw_mamm_sm, tw_mamm, 0.015)
        self.sc_mamm_s = self.sc_mamm(ar_lb[0], a_i, den, NOAEL_mamm, aw_mamm_sm, self.fi_mamm, 0.1, tw_mamm, self.ANOAEL_mamm, 0.015)

        self.sa_bird_1_m = self.sa_bird_1(ar_lb[0], a_i, den, self.at_bird, self.fi_bird, 0.1, ld50_bird, aw_bird_md, tw_bird_ld50, x, 0.1) 
        self.sa_bird_2_m = self.sa_bird_2(ar_lb[0], a_i, den, m_s_r_p, self.at_bird, ld50_bird, aw_bird_md, tw_bird_ld50, x, 0.1) 
        self.sc_bird_m = self.sc_bird(ar_lb[0], a_i, den, NOAEC_bird)
        self.sa_mamm_1_m = self.sa_mamm_1(ar_lb[0], a_i, den, self.at_mamm, self.fi_mamm, 0.1, ld50_mamm, aw_mamm_md, tw_mamm, 0.035)
        self.sa_mamm_2_m = self.sa_mamm_2(ar_lb[0], a_i, den, m_s_r_p, self.at_mamm, ld50_mamm, aw_mamm_md, tw_mamm, 0.035)
        self.sc_mamm_m = self.sc_mamm(ar_lb[0], a_i, den, NOAEL_mamm,aw_mamm_md, self.fi_mamm, 0.1, tw_mamm, self.ANOAEL_mamm, 0.035)

        self.sa_bird_1_l = self.sa_bird_1(ar_lb[0], a_i, den, self.at_bird, self.fi_bird, 0.1, ld50_bird, aw_bird_lg, tw_bird_ld50, x, 1.0) 
        self.sa_bird_2_l = self.sa_bird_2(ar_lb[0], a_i, den, m_s_r_p, self.at_bird, ld50_bird, aw_bird_lg, tw_bird_ld50, x, 1.0) 
        self.sc_bird_l = self.sc_bird(ar_lb[0], a_i, den, NOAEC_bird)
        self.sa_mamm_1_l = self.sa_mamm_1(ar_lb[0], a_i, den, self.at_mamm, self.fi_mamm, 0.1, ld50_mamm, aw_mamm_lg, tw_mamm, 1)
        self.sa_mamm_2_l = self.sa_mamm_2(ar_lb[0], a_i, den, m_s_r_p, self.at_mamm, ld50_mamm, aw_mamm_lg, tw_mamm, 1)
        self.sc_mamm_l = self.sc_mamm(ar_lb[0], a_i, den, NOAEL_mamm,aw_mamm_lg, self.fi_mamm, 0.1, tw_mamm, self.ANOAEL_mamm, 1)

        #Table 6
        self.EEC_diet_SG = self.EEC_diet(self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.EEC_diet_TG = self.EEC_diet(self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.EEC_diet_BP = self.EEC_diet(self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.EEC_diet_FR = self.EEC_diet(self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.EEC_diet_AR = self.EEC_diet(self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)

        #Table 7
        self.EEC_dose_bird_SG_sm = self.EEC_dose_bird(self.EEC_diet, aw_bird_sm, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.EEC_dose_bird_SG_md = self.EEC_dose_bird(self.EEC_diet, aw_bird_md, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.EEC_dose_bird_SG_lg = self.EEC_dose_bird(self.EEC_diet, aw_bird_lg, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.EEC_dose_bird_TG_sm = self.EEC_dose_bird(self.EEC_diet, aw_bird_sm, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.EEC_dose_bird_TG_md = self.EEC_dose_bird(self.EEC_diet, aw_bird_md, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.EEC_dose_bird_TG_lg = self.EEC_dose_bird(self.EEC_diet, aw_bird_lg, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.EEC_dose_bird_BP_sm = self.EEC_dose_bird(self.EEC_diet, aw_bird_sm, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.EEC_dose_bird_BP_md = self.EEC_dose_bird(self.EEC_diet, aw_bird_md, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.EEC_dose_bird_BP_lg = self.EEC_dose_bird(self.EEC_diet, aw_bird_lg, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.EEC_dose_bird_FP_sm = self.EEC_dose_bird(self.EEC_diet, aw_bird_sm, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.EEC_dose_bird_FP_md = self.EEC_dose_bird(self.EEC_diet, aw_bird_md, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.EEC_dose_bird_FP_lg = self.EEC_dose_bird(self.EEC_diet, aw_bird_lg, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.EEC_dose_bird_AR_sm = self.EEC_dose_bird(self.EEC_diet, aw_bird_sm, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.EEC_dose_bird_AR_md = self.EEC_dose_bird(self.EEC_diet, aw_bird_md, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.EEC_dose_bird_AR_lg = self.EEC_dose_bird(self.EEC_diet, aw_bird_lg, self.fi_bird, 0.9, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.EEC_dose_bird_SE_sm = self.EEC_dose_bird(self.EEC_diet, aw_bird_sm, self.fi_bird, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.EEC_dose_bird_SE_md = self.EEC_dose_bird(self.EEC_diet, aw_bird_md, self.fi_bird, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.EEC_dose_bird_SE_lg = self.EEC_dose_bird(self.EEC_diet, aw_bird_lg, self.fi_bird, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)

        #Table 7_add
        self.ARQ_bird_SG_sm = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_sm, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.ARQ_bird_SG_md = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_md, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.ARQ_bird_SG_lg = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_lg, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.ARQ_bird_TG_sm = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_sm, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.ARQ_bird_TG_md = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_md, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.ARQ_bird_TG_lg = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_lg, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.ARQ_bird_BP_sm = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_sm, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.ARQ_bird_BP_md = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_md, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.ARQ_bird_BP_lg = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_lg, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.ARQ_bird_FP_sm = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_sm, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.ARQ_bird_FP_md = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_md, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.ARQ_bird_FP_lg = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_lg, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.ARQ_bird_AR_sm = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_sm, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.ARQ_bird_AR_md = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_md, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.ARQ_bird_AR_lg = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_lg, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.ARQ_bird_SE_sm = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_sm, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.ARQ_bird_SE_md = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_md, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.ARQ_bird_SE_lg = self.ARQ_dose_bird(self.EEC_dose_bird, self.EEC_diet, aw_bird_lg, self.fi_bird, self.at_bird, ld50_bird, tw_bird_ld50, x, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)

        #Table 8
        self.ARQ_diet_bird_SG_A = self.ARQ_diet_bird(self.EEC_diet, lc50_bird, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.ARQ_diet_bird_SG_C = self.CRQ_diet_bird(self.EEC_diet, NOAEC_bird, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l,day_out)
        self.ARQ_diet_bird_TG_A = self.ARQ_diet_bird(self.EEC_diet, lc50_bird, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l,day_out)
        self.ARQ_diet_bird_TG_C = self.CRQ_diet_bird(self.EEC_diet, NOAEC_bird, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l,day_out)
        self.ARQ_diet_bird_BP_A = self.ARQ_diet_bird(self.EEC_diet, lc50_bird, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.ARQ_diet_bird_BP_C = self.CRQ_diet_bird(self.EEC_diet, NOAEC_bird, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.ARQ_diet_bird_FP_A = self.ARQ_diet_bird(self.EEC_diet, lc50_bird, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.ARQ_diet_bird_FP_C = self.CRQ_diet_bird(self.EEC_diet, NOAEC_bird, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.ARQ_diet_bird_AR_A = self.ARQ_diet_bird(self.EEC_diet, lc50_bird, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.ARQ_diet_bird_AR_C = self.CRQ_diet_bird(self.EEC_diet, NOAEC_bird, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
                      
        #Table 9
        self.EEC_dose_mamm_SG_sm=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_sm, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.EEC_dose_mamm_SG_md=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_md, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.EEC_dose_mamm_SG_lg=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_lg, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.EEC_dose_mamm_TG_sm=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_sm, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.EEC_dose_mamm_TG_md=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_md, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.EEC_dose_mamm_TG_lg=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_lg, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.EEC_dose_mamm_BP_sm=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_sm, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.EEC_dose_mamm_BP_md=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_md, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.EEC_dose_mamm_BP_lg=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_lg, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.EEC_dose_mamm_FP_sm=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_sm, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.EEC_dose_mamm_FP_md=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_md, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.EEC_dose_mamm_FP_lg=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_lg, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.EEC_dose_mamm_AR_sm=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_sm, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.EEC_dose_mamm_AR_md=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_md, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.EEC_dose_mamm_AR_lg=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_lg, self.fi_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.EEC_dose_mamm_SE_sm=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_sm, self.fi_mamm, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.EEC_dose_mamm_SE_md=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_md, self.fi_mamm, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.EEC_dose_mamm_SE_lg=self.EEC_dose_mamm(self.EEC_diet, aw_mamm_lg, self.fi_mamm, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)

        #Table 10
        self.ARQ_dose_mamm_SG_sm=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_sm, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.CRQ_dose_mamm_SG_sm=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.ARQ_dose_mamm_SG_md=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_md, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.CRQ_dose_mamm_SG_md=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.ARQ_dose_mamm_SG_lg=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_lg, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.CRQ_dose_mamm_SG_lg=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)

        self.ARQ_dose_mamm_TG_sm=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_sm, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.CRQ_dose_mamm_TG_sm=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.ARQ_dose_mamm_TG_md=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_md, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.CRQ_dose_mamm_TG_md=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.ARQ_dose_mamm_TG_lg=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_lg, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.CRQ_dose_mamm_TG_lg=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)

        self.ARQ_dose_mamm_BP_sm=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_sm, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.CRQ_dose_mamm_BP_sm=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.ARQ_dose_mamm_BP_md=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_md, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.CRQ_dose_mamm_BP_md=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.ARQ_dose_mamm_BP_lg=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_lg, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.CRQ_dose_mamm_BP_lg=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)

        self.ARQ_dose_mamm_FP_sm=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_sm, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.CRQ_dose_mamm_FP_sm=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.ARQ_dose_mamm_FP_md=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_md, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.CRQ_dose_mamm_FP_md=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.ARQ_dose_mamm_FP_lg=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_lg, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.CRQ_dose_mamm_FP_lg=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)

        self.ARQ_dose_mamm_AR_sm=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_sm, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.CRQ_dose_mamm_AR_sm=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.ARQ_dose_mamm_AR_md=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_md, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.CRQ_dose_mamm_AR_md=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.ARQ_dose_mamm_AR_lg=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_lg, self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        self.CRQ_dose_mamm_AR_lg=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, self.fi_mamm, tw_mamm, 0.8, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)

        self.ARQ_dose_mamm_SE_sm=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_sm, self.fi_mamm, ld50_mamm, tw_mamm, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.CRQ_dose_mamm_SE_sm=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, self.fi_mamm, tw_mamm, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.ARQ_dose_mamm_SE_md=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_md, self.fi_mamm, ld50_mamm, tw_mamm, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.CRQ_dose_mamm_SE_md=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, self.fi_mamm, tw_mamm, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.ARQ_dose_mamm_SE_lg=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet, self.at_mamm, aw_mamm_lg, self.fi_mamm, ld50_mamm, tw_mamm, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.CRQ_dose_mamm_SE_lg=self.CRQ_dose_mamm(self.EEC_diet, self.EEC_dose_mamm, self.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, self.fi_mamm, tw_mamm, 0.1, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)

        #table 11
        if self.lc50_mamm != 'N/A':
            self.ARQ_diet_mamm_SG=self.ARQ_diet_mamm(self.EEC_diet, lc50_mamm, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
            self.ARQ_diet_mamm_TG=self.ARQ_diet_mamm(self.EEC_diet, lc50_mamm, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
            self.ARQ_diet_mamm_BP=self.ARQ_diet_mamm(self.EEC_diet, lc50_mamm, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
            self.ARQ_diet_mamm_FP=self.ARQ_diet_mamm(self.EEC_diet, lc50_mamm, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
            self.ARQ_diet_mamm_AR=self.ARQ_diet_mamm(self.EEC_diet, lc50_mamm, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
        else:
            self.ARQ_diet_mamm_SG='N/A'
            self.ARQ_diet_mamm_TG='N/A'
            self.ARQ_diet_mamm_BP='N/A'
            self.ARQ_diet_mamm_FP='N/A'
            self.ARQ_diet_mamm_AR='N/A'

        self.CRQ_diet_mamm_SG=self.CRQ_diet_mamm(self.EEC_diet, NOAEC_mamm, self.C_0, self.C_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.CRQ_diet_mamm_TG=self.CRQ_diet_mamm(self.EEC_diet, NOAEC_mamm, self.C_0, self.C_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.CRQ_diet_mamm_BP=self.CRQ_diet_mamm(self.EEC_diet, NOAEC_mamm, self.C_0, self.C_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.CRQ_diet_mamm_FP=self.CRQ_diet_mamm(self.EEC_diet, NOAEC_mamm, self.C_0, self.C_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.CRQ_diet_mamm_AR=self.CRQ_diet_mamm(self.EEC_diet, NOAEC_mamm, self.C_0, self.C_t, n_a, ar_lb, a_i, 94, h_l, day_out)
  
        #Table12
        self.LD50_rg_bird_sm=self.LD50_rg_bird(Application_type, ar_lb, a_i, p_i, r_s, b_w, aw_bird_sm, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_rg_mamm_sm=self.LD50_rg_mamm(Application_type, ar_lb, a_i, p_i, r_s, b_w, aw_mamm_sm, self.at_mamm, ld50_mamm, tw_mamm)
        self.LD50_rg_bird_md=self.LD50_rg_bird(Application_type, ar_lb, a_i, p_i, r_s, b_w, aw_bird_md, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_rg_mamm_md=self.LD50_rg_mamm(Application_type, ar_lb, a_i, p_i, r_s, b_w, aw_mamm_md, self.at_mamm, ld50_mamm, tw_mamm)
        self.LD50_rg_bird_lg=self.LD50_rg_bird(Application_type, ar_lb, a_i, p_i, r_s, b_w, aw_bird_lg, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_rg_mamm_lg=self.LD50_rg_mamm(Application_type, ar_lb, a_i, p_i, r_s, b_w, aw_mamm_lg, self.at_mamm, ld50_mamm, tw_mamm)

        #Table13
        self.LD50_rl_bird_sm=self.LD50_rl_bird(Application_type, ar_lb, a_i, p_i, b_w, aw_bird_sm, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_rl_mamm_sm=self.LD50_rl_mamm(Application_type, ar_lb, a_i, p_i, b_w, aw_mamm_sm, self.at_mamm, ld50_mamm, tw_mamm)
        self.LD50_rl_bird_md=self.LD50_rl_bird(Application_type, ar_lb, a_i, p_i, b_w, aw_bird_md, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_rl_mamm_md=self.LD50_rl_mamm(Application_type, ar_lb, a_i, p_i, b_w, aw_mamm_md, self.at_mamm, ld50_mamm, tw_mamm)
        self.LD50_rl_bird_lg=self.LD50_rl_bird(Application_type, ar_lb, a_i, p_i, b_w, aw_bird_lg, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_rl_mamm_lg=self.LD50_rl_mamm(Application_type, ar_lb, a_i, p_i, b_w, aw_mamm_lg, self.at_mamm, ld50_mamm, tw_mamm)

        #Table14
        self.LD50_bg_bird_sm=self.LD50_bg_bird(Application_type, ar_lb, a_i, p_i, aw_bird_sm, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_bg_mamm_sm=self.LD50_bg_mamm(Application_type, ar_lb, a_i, p_i, aw_mamm_sm, self.at_mamm, ld50_mamm, tw_mamm)
        self.LD50_bg_bird_md=self.LD50_bg_bird(Application_type, ar_lb, a_i, p_i, aw_bird_md, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_bg_mamm_md=self.LD50_bg_mamm(Application_type, ar_lb, a_i, p_i, aw_mamm_md, self.at_mamm, ld50_mamm, tw_mamm)
        self.LD50_bg_bird_lg=self.LD50_bg_bird(Application_type, ar_lb, a_i, p_i, aw_bird_lg, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_bg_mamm_lg=self.LD50_bg_mamm(Application_type, ar_lb, a_i, p_i, aw_mamm_lg, self.at_mamm, ld50_mamm, tw_mamm)

        #Table15
        self.LD50_bl_bird_sm=self.LD50_bl_bird(Application_type, ar_lb, a_i, aw_bird_sm, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_bl_mamm_sm=self.LD50_bl_mamm(Application_type, ar_lb, a_i, aw_mamm_sm, self.at_mamm, ld50_mamm, tw_mamm)
        self.LD50_bl_bird_md=self.LD50_bl_bird(Application_type, ar_lb, a_i, aw_bird_md, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_bl_mamm_md=self.LD50_bl_mamm(Application_type, ar_lb, a_i, aw_mamm_md, self.at_mamm, ld50_mamm, tw_mamm)
        self.LD50_bl_bird_lg=self.LD50_bl_bird(Application_type, ar_lb, a_i, aw_bird_lg, self.at_bird, ld50_bird, tw_bird_ld50, x)
        self.LD50_bl_mamm_lg=self.LD50_bl_mamm(Application_type, ar_lb, a_i, aw_mamm_lg, self.at_mamm, ld50_mamm, tw_mamm)

    #food intake for birds

    def fi_bird(self, aw_bird, mf_w_bird):
        try:
            aw_bird = float(aw_bird)
            mf_w_bird = float(mf_w_bird)           
        except IndexError:
            raise IndexError\
            ('The body weight of the assessed bird, and/or the mass fraction of '\
            'water in the food must be supplied on the command line.')
        except ValueError:
            raise ValueError\
            ('The body weight of the assessed bird must be a real number, not "%g"' % aw_bird)
        except ValueError:
            raise ValueError\
            ('The mass fraction of water in the food for bird must be a real number, not "%g"' % mf_w_bird)
        if aw_bird < 0:
            raise ValueError\
            ('The body weight of the assessed bird=%g is a non-physical value.' % aw_bird)
        if mf_w_bird < 0:
            raise ValueError\
            ('The fraction of water in the food for bird=%g is a non-physical value.' % mf_w_bird)        
        if mf_w_bird >= 1:
            raise ValueError\
            ('The fraction of water in the food for bird=%g must be less than 1.' % mf_w_bird)   
        return (0.648 * (aw_bird**0.651))/(1-mf_w_bird)

    # food intake for mammals

    def fi_mamm(self, aw_mamm, mf_w_mamm):
        try:
            aw_mamm = float(aw_mamm)
            mf_w_mamm = float(mf_w_mamm)           
        except IndexError:
            raise IndexError\
            ('The body weight of mammal, and/or the mass fraction of water in the '\
             'food must be supplied on the command line.')
        except ValueError:
            raise ValueError\
            ('The body weight of mammal must be a real number, not "%g"' % aw_mamm)
        except ValueError:
            raise ValueError\
            ('The mass fraction of water in the food for mammals must be a real number, not "%"' % mf_w_mamm)
        if aw_mamm < 0:
            raise ValueError\
            ('The body weight of mammal=%g is a non-physical value.' % aw_mamm)
        if mf_w_mamm < 0:
            raise ValueError\
            ('The fraction of water in the food for mammals=%g is a non-physical value.' % mf_w_mamm)        
        if mf_w_mamm >= 1:
            raise ValueError\
            ('The fraction of water in the food for mammals=%g must be less than 1.' % mf_w_mamm)  
        return (0.621 * (aw_mamm**0.564))/(1-mf_w_mamm)

    #Acute adjusted toxicity value for birds

    def at_bird(self, ld50_bird, aw_bird, tw_bird, x):
        try:
            ld50_bird = float(ld50_bird)
            aw_bird = float(aw_bird)
            tw_bird = float(tw_bird)
            x = float(x)
        except IndexError:
            raise IndexError\
            ('The lethal dose, body weight of assessed bird, body weight of tested'\
            ' bird, and/or Mineau scaling factor for birds must be supplied on'\
            ' the command line.')
        except ValueError:
            raise ValueError\
            ('The lethal dose must be a real number, not "%mg/kg"' %ld50_bird)
        except ValueError:
            raise ValueError\
            ('The body weight of assessed bird must be a real number, not "%g"' %aw_bird)
        except ValueError:
            raise ValueError\
            ('The body weight of tested bird must be a real number, not "%g"' %tw_bird)
        except ValueError:
            raise ValueError\
            ('The Mineau scaling factor for birds must be a real number' % x)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The body weight of tested bird must be non-zero.')
        if ld50_bird < 0:
            raise ValueError\
            ('ld50=%g is a non-physical value.' % ld50_bird)
        if aw_bird < 0:
            raise ValueError\
            ('aw_bird=%g is a non-physical value.' % aw_bird)
        if tw_bird < 0:
            raise ValueError\
            ('tw_bird=%g is a non-physical value.' % tw_bird)
        if x < 0:
            raise ValueError\
            ('x=%g is non-physical value.' %x)
        return (ld50_bird) * ((aw_bird/tw_bird)**(x-1))

    # Acute adjusted toxicity value for mammals

    def at_mamm(self, ld50_mamm, aw_mamm, tw_mamm):
        try:
            ld50_mamm = float(ld50_mamm)
            aw_mamm = float(aw_mamm)
            tw_mamm = float(tw_mamm)
        except IndexError:
            raise IndexError\
            ('The lethal dose, body weight of assessed mammal, and body weight of tested'\
            ' mammal must be supplied on'\
            ' the command line.')
        except ValueError:
            raise ValueError\
            ('The lethal dose must be a real number, not "%mg/kg"' %ld50_mamm)
        except ValueError:
            raise ValueError\
            ('The body weight of assessed mammals must be a real number, not "%g"' %aw_mamm)
        except ValueError:
            raise ValueError\
            ('The body weight of tested mammals must be a real number, not "%g"' %tw_mamm)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The body weight of tested mammals must be non-zero.')
        if ld50_mamm < 0:
            raise ValueError\
            ('ld50_mamm=%g is a non-physical value.' % ld50_mamm)
        if aw_mamm < 0:
            raise ValueError\
            ('aw_mamm=%g is a non-physical value.' % aw_mamm)
        if tw_mamm < 0:
            raise ValueError\
            ('tw_mamm=%g is a non-physical value.' % tw_mamm)
        return (ld50_mamm) * ((tw_mamm/aw_mamm)**(0.25))

    # Adjusted chronic toxicity (NOAEL) value for mammals

    def ANOAEL_mamm(self, NOAEL_mamm, aw_mamm, tw_mamm):
        try:
            NOAEL_mamm = float(NOAEL_mamm)
            aw_mamm = float(aw_mamm)
            tw_mamm = float(tw_mamm)
        except IndexError:
            raise IndexError\
            ('The NOAEL, body weight of assessed mammal, and body weight of tested'\
            ' mammal must be supplied on'\
            ' the command line.')
        except ValueError:
            raise ValueError\
            ('The NOAEL must be a real number, not "%mg/kg"' %NOAEL_mamm)
        except ValueError:
            raise ValueError\
            ('The body weight of assessed mammals must be a real number, not "%g"' %aw_mamm)
        except ValueError:
            raise ValueError\
            ('The body weight of tested mammals must be a real number, not "%g"' %tw_mamm)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The body weight of tested mammals must be non-zero.')
        if NOAEL_mamm < 0:
            raise ValueError\
            ('NOAEL_mamm=%g is a non-physical value.' % NOAEL_mamm)
        if aw_mamm < 0:
            raise ValueError\
            ('aw_mamm=%g is a non-physical value.' % aw_mamm)
        if tw_mamm < 0:
            raise ValueError\
            ('tw_mamm=%g is a non-physical value.' % tw_mamm)
        return (NOAEL_mamm) * ((tw_mamm/aw_mamm)**(0.25))

    #Dietary based EECs

    #Initial concentration
     
    def C_0(self, a_r, a_i, para):
        try:
            a_r = float(a_r)
            a_i = float(a_i)           
        except IndexError:
            raise IndexError\
            ('The application rate, and/or the percentage of active ingredient '\
             'must be supplied on the command line.')
        except ValueError:
            raise ValueError\
            ('The application rate must be a real number, not "%g"' % a_r)
        except ValueError:
            raise ValueError\
            ('The percentage of active ingredient must be a real number, not "%"' % a_i)
        if a_r < 0:
            raise ValueError\
            ('The application rate=%g is a non-physical value.' % a_r)
        if a_i < 0:
            raise ValueError\
            ('The percentage of active ingredient=%g is a non-physical value.' % a_i)        
        return (a_r*a_i*para)

    #Concentration over time

    def C_t(self, C_ini, h_l):    
        try:
            h_l = float(h_l)      
        except IndexError:
            raise IndexError\
            ('The initial concentration, and/or the foliar dissipation half life, '\
             'must be supplied on the command line.')
        except ValueError:
            raise ValueError\
            ('The foliar dissipation half life must be a real number, not "%g"' % h_l)      
        if h_l < 0:
            raise ValueError\
            ('The foliar dissipation half life=%g is a non-physical value.' % h_l)        
        return (C_ini*np.exp(-(np.log(2)/h_l)*1))
        
    # concentration over time if application rate or time interval is variable

    #Dietary based EECs

    def EEC_diet(self, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out):
    #new in trex1.5.1
        if n_a == 1:
            C_temp = C_0(a_r[0], a_i, para)
            return C_temp
        else:
            C_temp = np.ones((371,1)) #empty array to hold the concentrations over days       
            a_p_temp = 0  #application period temp  
            n_a_temp = 0  #number of existing applications
            dayt = 0
            day_out_l=len(day_out)
            for i in range (0,371):
                if i==0:  #first day of application
                    C_temp[i] = C_0(a_r[0], a_i, para)
                    a_p_temp = 0
                    n_a_temp = n_a_temp + 1
                    dayt = dayt + 1
                elif dayt<=day_out_l-1 and n_a_temp<=n_a: # next application day
                    if i==day_out[dayt]:
                        C_temp[i] = C_t(C_temp[i-1], h_l) + C_0(a_r[dayt], a_i, para)
                        n_a_temp = n_a_temp + 1
                        dayt = dayt + 1        
                    else :
                        C_temp[i]=C_t(C_temp[i-1], h_l) 
            return (max(C_temp))


    # Dose based EECs for birds

    def EEC_dose_bird(self, EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out):
        n_a = float(n_a)
     #   i_a = float(i_a)      
        aw_bird = float(aw_bird)
        mf_w_bird = float(mf_w_bird)
      #  a_r = float(a_r)
        a_i = float(a_i)
        para = float(para)
        h_l = float(h_l)
            
        fi_bird = fi_bird(aw_bird, mf_w_bird)
        EEC_diet=EEC_diet(C_0, C_t, n_a, a_r, a_i, para, h_l, day_out)
        return (EEC_diet*fi_bird/aw_bird)

    # Dose based EECs for granivores birds

    # def EEC_dose_bird_g(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, n_a, a_r, a_i, para, h_l):
    #     if para==15:
    #         n_a = float(n_a)
    #       #  i_a = float(i_a)      
    #         aw_bird = float(aw_bird)
    #         mf_w_bird = float(mf_w_bird)
    #         a_r = float(a_r)
    #         a_i = float(a_i)
    #         para = float(para)
    #         h_l = float(h_l)        
    #         fi_bird = fi_bird(aw_bird, mf_w_bird)
    #         EEC_diet=EEC_diet(C_0, n_a, a_r, a_i, para, h_l, day)
    #         return (EEC_diet*fi_bird/aw_bird)
    #     else:
    #         return(0)
            
    # Dose based EECs for mammals

    def EEC_dose_mamm(self, EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out):
        aw_mamm = float(aw_mamm)
        EEC_diet=EEC_diet(C_0, C_t, n_a, a_r, a_i, para, h_l, day_out)
        fi_mamm = fi_mamm(aw_mamm, mf_w_mamm)
        return (EEC_diet*fi_mamm/aw_mamm)

    # Dose based EECs for granivores mammals

    # def EEC_dose_mamm_g(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l):
    #     if para==15:    
    #         aw_mamm = float(aw_mamm)
    #         EEC_diet=EEC_diet(C_0, n_a, a_r, a_i, para, h_l, day)
    #         fi_mamm = fi_mamm(aw_mamm, mf_w_mamm)
    #         return (EEC_diet*fi_mamm/aw_mamm)
    #     else:
    #         return(0)
            
    # Acute dose-based risk quotients for birds

    def ARQ_dose_bird(self, EEC_dose_bird, EEC_diet, aw_bird, fi_bird, at_bird, ld50_bird, tw_bird, x, mf_w_bird, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out):
        EEC_dose_bird = EEC_dose_bird(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out)
        at_bird = at_bird(ld50_bird,aw_bird,tw_bird,x)
        return (EEC_dose_bird/at_bird)

    # Acute dose-based risk quotients for granivores birds

    # def ARQ_dose_bird_g(EEC_dose_bird, EEC_diet, aw_bird, fi_bird, at_bird, ld50_bird, tw_bird, x, mf_w_bird, C_0, n_a, a_r, a_i, para, h_l):
    #     if para==15:
    #         EEC_dose_bird = EEC_dose_bird(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, n_a, a_r, a_i, para, h_l)
    #         at_bird = at_bird(ld50_bird,aw_bird,tw_bird,x)
    #         return (EEC_dose_bird/at_bird)
    #     else:
    #         return (0)
        
    # Acute dose-based risk quotients for mammals

    def ARQ_dose_mamm(self, EEC_dose_mamm, EEC_diet, at_mamm, aw_mamm, fi_mamm, ld50_mamm, tw_mamm, mf_w_mamm, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out):
        EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out)
        at_mamm = at_mamm(ld50_mamm,aw_mamm,tw_mamm)
        return (EEC_dose_mamm/at_mamm)

    # Acute dose-based risk quotients for granivores mammals

    # def ARQ_dose_mamm_g(EEC_dose_mamm, at_mamm, aw_mamm, ld50_mamm, tw_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l):
    #     if para==15:    
    #         EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l)
    #         at_mamm = at_mamm(ld50_mamm,aw_mamm,tw_mamm)
    #         return (EEC_dose_mamm/at_mamm)
    #     else:
    #         return(0)
            
    # Acute dietary-based risk quotients for birds

    def ARQ_diet_bird(self, EEC_diet, lc50_bird, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out):
        EEC_diet=EEC_diet(C_0, C_t, n_a, a_r, a_i, para, h_l, day_out)    
        try:
            lc50_bird = float(lc50_bird)      
        except IndexError:
            raise IndexError\
            ('The Avian LC50 must be supplied on the command line.')
        if lc50_bird < 0:
            raise ValueError\
            ('The Avian LC50=%g is a non-physical value.' % lc50_bird)        
        return (EEC_diet/lc50_bird)


    # Acute dietary-based risk quotients for mammals

    def ARQ_diet_mamm(self, EEC_diet, lc50_mamm, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out):
        EEC_diet=EEC_diet(C_0, C_t, n_a, a_r, a_i, para, h_l, day_out)    
        return (EEC_diet/lc50_mamm)

    # Chronic dietary-based risk quotients for birds

    def CRQ_diet_bird(self, EEC_diet, NOAEC_bird, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out):
        EEC_diet=EEC_diet(C_0, C_t, n_a, a_r, a_i, para, h_l, day_out)    
        try:
            NOAEC_bird = float(NOAEC_bird)      
        except IndexError:
            raise IndexError\
            ('The avian NOAEC must be supplied on the command line.')
        if NOAEC_bird < 0:
            raise ValueError\
            ('The avian NOAEC=%g is a non-physical value.' % NOAEC_bird)        
        return (EEC_diet/NOAEC_bird)

    # Chronic dietary-based risk quotients for mammals

    def CRQ_diet_mamm(self, EEC_diet, NOAEC_mamm, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out):
        EEC_diet=EEC_diet(C_0, C_t, n_a, a_r, a_i, para, h_l, day_out)
        try:
            NOAEC_mamm = float(NOAEC_mamm)      
        except IndexError:
            raise IndexError\
            ('The mammlian NOAEC must be supplied on the command line.')
        if NOAEC_mamm < 0:
            raise ValueError\
            ('The mammlian NOAEC=%g is a non-physical value.' % NOAEC_mamm)        
        return (EEC_diet/NOAEC_mamm)

    # Chronic dose-based risk quotients for mammals

    def CRQ_dose_mamm(self, EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm, fi_mamm, tw_mamm, mf_w_mamm, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out):
        ANOAEL_mamm=ANOAEL_mamm(NOAEL_mamm,aw_mamm,tw_mamm)
        EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, C_t, n_a, a_r, a_i, para, h_l, day_out)     
        return (EEC_dose_mamm/ANOAEL_mamm)

    # Chronic dose-based risk quotients for granviores mammals

    # def CRQ_dose_mamm_g(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm, tw_mamm, mf_w_mamm, n_a, a_r, a_i, para, h_l):
    #     if para==15:    
    #         ANOAEL_mamm=ANOAEL_mamm(NOAEL_mamm,aw_mamm,tw_mamm)
    #         EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l)     
    #         return (EEC_dose_mamm/ANOAEL_mamm)
    #     else:
    #         return (0)
            
    # LD50ft-2 for row/band/in-furrow granular birds

    def LD50_rg_bird(self, Application_type, a_r, a_i, p_i, r_s, b_w, aw_bird, at_bird, ld50_bird, tw_bird, x): 
        if Application_type=='Row/Band/In-furrow-Granular':     
            at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)
            # print 'r_s', r_s
            n_r=(43560**0.5)/(r_s)
            # print 'n_r=', n_r
            # print 'a_r=', a_r
            # print 'b_w=', b_w
            # print 'p_i=', p_i
            # print 'a_i', a_i
            # print 'class a_r', type(a_r)
            expo_rg_bird=(max(a_r)*a_i*453590.0)/(n_r*(43560.0**0.5)*b_w)*(1-p_i)
            return (expo_rg_bird/(at_bird*(aw_bird/1000.0)))
        else:
            return(0)
            
    # LD50ft-2 for row/band/in-furrow liquid birds

    def LD50_rl_bird(self, Application_type, a_r, a_i, p_i, b_w, aw_bird, at_bird, ld50_bird, tw_bird, x):
        if Application_type=='Row/Band/In-furrow-Liquid':    
            at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)    
            expo_rl_bird=((max(a_r)*28349*a_i)/(1000*b_w))*(1-p_i)
            return (expo_rl_bird/(at_bird*(aw_bird/1000.0)))
        else:
            return(0)
            
    # LD50ft-2 for row/band/in-furrow granular mammals

    def LD50_rg_mamm(self, Application_type, a_r, a_i, p_i, r_s, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
        if Application_type=='Row/Band/In-furrow-Granular':  
           # a_r = max(ar_lb)  
            at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)
            n_r=(43560**0.5)/(r_s)
            expo_rg_mamm=(max(a_r)*a_i*453590)/(n_r*(43560**0.5)*b_w)*(1-p_i)
            return (expo_rg_mamm/(at_mamm*(aw_mamm/1000.0)))
        else:
            return(0)
            
    # LD50ft-2 for row/band/in-furrow liquid mammals

    def LD50_rl_mamm(self, Application_type, a_r, a_i, p_i, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
        if Application_type=='Row/Band/In-furrow-Liquid':    
            at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)    
            expo_rl_bird=((max(a_r)*28349*a_i)/(1000*b_w))*(1-p_i)
            return (expo_rl_bird/(at_mamm*(aw_mamm/1000.0)))
        else:
            return(0)
            
    # LD50ft-2 for broadcast granular birds

    def LD50_bg_bird(self, Application_type, a_r, a_i, p_i, aw_bird, at_bird, ld50_bird, tw_bird, x):
        if Application_type=='Broadcast-Granular':    
            at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)
            expo_bg_bird=((max(a_r)*a_i*453590)/43560)
            return (expo_bg_bird/(at_bird*(aw_bird/1000.0)))
        else:
            return(0)
            
    # LD50ft-2 for broadcast liquid birds

    def LD50_bl_bird(self, Application_type, a_r, a_i, aw_bird, at_bird, ld50_bird, tw_bird, x):
        if Application_type=='Broadcast-Liquid':   
            at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)
            # expo_bl_bird=((max(a_r)*28349*a_i)/43560)*(1-p_i)
            expo_bl_bird=((max(a_r)*453590*a_i)/43560)
            return (expo_bl_bird/(at_bird*(aw_bird/1000.0)))    
        else:
            return(0)
            
    # LD50ft-2 for broadcast granular mammals

    def LD50_bg_mamm(self, Application_type, a_r, a_i, p_i, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
        if Application_type=='Broadcast-Granular':    
            at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm) 
            expo_bg_mamm=((max(a_r)*a_i*453590)/43560)
            return (expo_bg_mamm/(at_mamm*(aw_mamm/1000.0)))
        else:
            return(0)
            
    # LD50ft-2 for broadcast liquid mammals

    def LD50_bl_mamm(self, Application_type, a_r, a_i, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
        if Application_type=='Broadcast-Liquid':    
            at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)
            # expo_bl_mamm=((max(a_r)*28349*a_i)/43560)*(1-p_i)
            expo_bl_mamm=((max(a_r)*a_i*453590)/43560)
            return (expo_bl_mamm/(at_mamm*(aw_mamm/1000.0)))     
        else:
            return(0)
            
    # Seed treatment acute RQ for birds method 1

    def sa_bird_1(self, a_r_p, a_i, den, at_bird, fi_bird, mf_w_bird, ld50_bird, aw_bird, tw_bird, x, nagy_bird_coef):
        at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)    
        # fi_bird=fi_bird(20, 0.1)    
        fi_bird = fi_bird(aw_bird, mf_w_bird)
        m_s_a_r=((a_r_p*a_i)/128)*den*10000    #maximum seed application rate=application rate*10000
        nagy_bird=fi_bird*0.001*m_s_a_r/nagy_bird_coef
        return (nagy_bird/at_bird)      


    # Seed treatment acute RQ for birds method 2

    def sa_bird_2(self, a_r_p, a_i, den, m_s_r_p, at_bird, ld50_bird, aw_bird, tw_bird, x, nagy_bird_coef):
        at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)    
        m_a_r=(m_s_r_p*((a_i*a_r_p)/128)*den)/100    #maximum application rate
        av_ai=m_a_r*1e6/(43560*2.2)
        return (av_ai/(at_bird*nagy_bird_coef))     
        
    # Seed treatment chronic RQ for birds

    def sc_bird(self, a_r_p, a_i, den, NOAEC_bird):    
        m_s_a_r=((a_r_p*a_i)/128)*den*10000    #maximum seed application rate=application rate*10000
        return (m_s_a_r/NOAEC_bird)       
        
    # Seed treatment acute RQ for mammals method 1

    def sa_mamm_1(self, a_r_p, a_i, den, at_mamm, fi_mamm, mf_w_bird, ld50_mamm, aw_mamm, tw_mamm, nagy_mamm_coef):
        at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)     
        fi_mamm=fi_mamm(aw_mamm, mf_w_bird)    
        m_s_a_r=((a_r_p*a_i)/128)*den*10000    #maximum seed application rate=application rate*10000
        nagy_mamm=fi_mamm*0.001*m_s_a_r/nagy_mamm_coef
        return (nagy_mamm/at_mamm)       
        
    # Seed treatment acute RQ for mammals method 2

    def sa_mamm_2(self, a_r_p, a_i, den, m_s_r_p, at_mamm, ld50_mamm, aw_mamm, tw_mamm, nagy_mamm_coef):
        at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)
        m_a_r=(m_s_r_p*((a_r_p*a_i)/128)*den)/100    #maximum application rate
        av_ai=m_a_r*1000000/(43560*2.2)
        return (av_ai/(at_mamm*nagy_mamm_coef))     
          
    # Seed treatment chronic RQ for mammals

    def sc_mamm(self, a_r_p, a_i, den, NOAEL_mamm, aw_mamm, fi_mamm, mf_w_bird, tw_mamm, ANOAEL_mamm, nagy_mamm_coef):
        ANOAEL_mamm = ANOAEL_mamm(NOAEL_mamm, aw_mamm, tw_mamm)
        fi_mamm=fi_mamm(aw_mamm, mf_w_bird)    
        m_s_a_r=((a_r_p*a_i)/128)*den*10000    #maximum seed application rate=application rate*10000
        nagy_mamm=fi_mamm*0.001*m_s_a_r/nagy_mamm_coef
        return (nagy_mamm/ANOAEL_mamm)          
