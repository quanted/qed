# -*- coding: utf-8 -*-
import numpy as np
import logging
import sys
import time, datetime
#food intake for birds
class therps(object):
    def __init__(self, run_type, chem_name, use, formu_name, a_i, h_l, n_a, i_a, a_r, avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, 
                 Species_of_the_tested_bird_avian_ld50, Species_of_the_tested_bird_avian_lc50, Species_of_the_tested_bird_avian_NOAEC, Species_of_the_tested_bird_avian_NOAEL,
                 bw_avian_ld50, bw_avian_lc50, bw_avian_NOAEC, bw_avian_NOAEL,
                 mineau_scaling_factor, bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, 
                 wp_herp_a_lg, c_mamm_a, c_herp_a):

        ts = datetime.datetime.now()
        if(time.daylight):
            ts1 = datetime.timedelta(hours=-4)+ts
        else:
            ts1 = datetime.timedelta(hours=-5)+ts
        self.jid = ts1.strftime('%Y%m%d%H%M%S%f')

        self.run_type = run_type
        self.chem_name = chem_name
        self.use = use
        self.formu_name = formu_name
        self.a_i = a_i
        self.a_i_disp = 100*a_i
        self.h_l = h_l
        self.n_a = n_a
        self.i_a = i_a
        self.a_r = a_r
        self.avian_ld50 = avian_ld50
        self.avian_lc50 = avian_lc50
        self.avian_NOAEC = avian_NOAEC
        self.avian_NOAEL = avian_NOAEL
        self.Species_of_the_tested_bird_avian_ld50=Species_of_the_tested_bird_avian_ld50
        self.Species_of_the_tested_bird_avian_lc50=Species_of_the_tested_bird_avian_lc50
        self.Species_of_the_tested_bird_avian_NOAEC=Species_of_the_tested_bird_avian_NOAEC
        self.Species_of_the_tested_bird_avian_NOAEL=Species_of_the_tested_bird_avian_NOAEL
        self.bw_avian_ld50=bw_avian_ld50
        self.bw_avian_lc50=bw_avian_lc50
        self.bw_avian_NOAEC=bw_avian_NOAEC
        self.bw_avian_NOAEL=bw_avian_NOAEL
        self.mineau_scaling_factor = mineau_scaling_factor
        self.bw_herp_a_sm = bw_herp_a_sm
        self.bw_herp_a_md = bw_herp_a_md
        self.bw_herp_a_lg = bw_herp_a_lg
        self.wp_herp_a_sm = wp_herp_a_sm
        self.wp_herp_a_md = wp_herp_a_md
        self.wp_herp_a_lg = wp_herp_a_lg
        self.c_mamm_a = c_mamm_a
        self.c_herp_a = c_herp_a

        #Table 5
        self.LD50_AD_sm=self.at_bird(avian_ld50, bw_herp_a_sm, bw_avian_ld50, mineau_scaling_factor)
        self.LD50_AD_md=self.at_bird(avian_ld50, bw_herp_a_md, bw_avian_ld50, mineau_scaling_factor)
        self.LD50_AD_lg=self.at_bird(avian_ld50, bw_herp_a_lg, bw_avian_ld50, mineau_scaling_factor)

        self.EEC_dose_BP_sm=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_sm, self.fi_herp, wp_herp_a_sm, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.EEC_dose_BP_md=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_md, self.fi_herp, wp_herp_a_md, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.EEC_dose_BP_lg=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_lg, self.fi_herp, wp_herp_a_lg, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.ARQ_dose_BP_sm=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_sm, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_sm, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.ARQ_dose_BP_md=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_md, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_md, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.ARQ_dose_BP_lg=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_lg, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_lg, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l)

        self.EEC_dose_FR_sm=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_sm, self.fi_herp, wp_herp_a_sm, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.EEC_dose_FR_md=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_md, self.fi_herp, wp_herp_a_md, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.EEC_dose_FR_lg=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_lg, self.fi_herp, wp_herp_a_lg, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.ARQ_dose_FR_sm=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_sm, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_sm, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.ARQ_dose_FR_md=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_md, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_md, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.ARQ_dose_FR_lg=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_lg, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_lg, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l)

        self.EEC_dose_HM_md=self.EEC_dose_mamm(self.EEC_diet_mamm, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.EEC_dose_HM_lg=self.EEC_dose_mamm(self.EEC_diet_mamm, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.ARQ_dose_HM_md=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet_mamm, self.EEC_diet, bw_herp_a_md, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm)
        self.ARQ_dose_HM_lg=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet_mamm, self.EEC_diet, bw_herp_a_lg, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm)

        self.EEC_dose_IM_md=self.EEC_dose_mamm(self.EEC_diet_mamm, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.EEC_dose_IM_lg=self.EEC_dose_mamm(self.EEC_diet_mamm, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.ARQ_dose_IM_md=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet_mamm, self.EEC_diet, bw_herp_a_md, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm)
        self.ARQ_dose_IM_lg=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet_mamm, self.EEC_diet, bw_herp_a_lg, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm)

        self.EEC_dose_TP_md=self.EEC_dose_tp(self.EEC_diet_tp, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, bw_herp_a_md, c_herp_a, wp_herp_a_sm, wp_herp_a_md)
        self.EEC_dose_TP_lg=self.EEC_dose_tp(self.EEC_diet_tp, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, bw_herp_a_lg, c_herp_a, wp_herp_a_sm, wp_herp_a_md)
        self.ARQ_dose_TP_md=self.ARQ_dose_tp(self.EEC_dose_tp, self.EEC_diet_tp, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm, wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_md, bw_avian_ld50, mineau_scaling_factor)
        self.ARQ_dose_TP_lg=self.ARQ_dose_tp(self.EEC_dose_tp, self.EEC_diet_tp, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm, wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_lg, bw_avian_ld50, mineau_scaling_factor)

        #Table 6
        self.EEC_diet_herp_BL=self.EEC_diet(self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.EEC_ARQ_herp_BL=self.ARQ_diet_herp(self.EEC_diet, avian_lc50, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.EEC_diet_herp_FR=self.EEC_diet(self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.EEC_ARQ_herp_FR=self.ARQ_diet_herp(self.EEC_diet, avian_lc50, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.EEC_diet_herp_HM=self.EEC_diet_mamm(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_ARQ_herp_HM=self.ARQ_diet_mamm(self.EEC_diet_mamm, self.EEC_diet, avian_lc50, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_diet_herp_IM=self.EEC_diet_mamm(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_ARQ_herp_IM=self.ARQ_diet_mamm(self.EEC_diet_mamm, self.EEC_diet, avian_lc50, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_diet_herp_TP=self.EEC_diet_tp(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.EEC_ARQ_herp_TP=self.ARQ_diet_tp(self.EEC_diet_tp, self.EEC_diet, avian_lc50, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        #Table 7
        self.EEC_diet_herp_BL=self.EEC_diet(self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.EEC_CRQ_herp_BL=self.CRQ_diet_herp(self.EEC_diet, avian_NOAEC, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.EEC_diet_herp_FR=self.EEC_diet(self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.EEC_CRQ_herp_FR=self.CRQ_diet_herp(self.EEC_diet, avian_NOAEC, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.EEC_diet_herp_HM=self.EEC_diet_mamm(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_CRQ_herp_HM=self.CRQ_diet_mamm(self.EEC_diet_mamm, self.EEC_diet, avian_NOAEC, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_diet_herp_IM=self.EEC_diet_mamm(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_CRQ_herp_IM=self.CRQ_diet_mamm(self.EEC_diet_mamm, self.EEC_diet, avian_NOAEC, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_diet_herp_TP=self.EEC_diet_tp(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.EEC_CRQ_herp_TP=self.CRQ_diet_tp(self.EEC_diet_tp, self.EEC_diet, avian_NOAEC, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        #Table 8
        self.EEC_dose_BP_sm_mean=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_sm, self.fi_herp, wp_herp_a_sm, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.EEC_dose_BP_md_mean=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_md, self.fi_herp, wp_herp_a_md, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.EEC_dose_BP_lg_mean=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_lg, self.fi_herp, wp_herp_a_lg, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.ARQ_dose_BP_sm_mean=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_sm, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_sm, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.ARQ_dose_BP_md_mean=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_md, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_md, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.ARQ_dose_BP_lg_mean=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_lg, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_lg, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l)

        self.EEC_dose_FR_sm_mean=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_sm, self.fi_herp, wp_herp_a_sm, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.EEC_dose_FR_md_mean=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_md, self.fi_herp, wp_herp_a_md, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.EEC_dose_FR_lg_mean=self.EEC_dose_herp(self.EEC_diet, bw_herp_a_lg, self.fi_herp, wp_herp_a_lg, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.ARQ_dose_FR_sm_mean=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_sm, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_sm, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.ARQ_dose_FR_md_mean=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_md, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_md, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.ARQ_dose_FR_lg_mean=self.ARQ_dose_herp(self.EEC_dose_herp, self.EEC_diet, bw_herp_a_lg, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, wp_herp_a_lg, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l)

        self.EEC_dose_HM_md_mean=self.EEC_dose_mamm(self.EEC_diet_mamm, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.EEC_dose_HM_lg_mean=self.EEC_dose_mamm(self.EEC_diet_mamm, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.ARQ_dose_HM_md_mean=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet_mamm, self.EEC_diet, bw_herp_a_md, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm)
        self.ARQ_dose_HM_lg_mean=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet_mamm, self.EEC_diet, bw_herp_a_lg, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm)

        self.EEC_dose_IM_md_mean=self.EEC_dose_mamm(self.EEC_diet_mamm, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.EEC_dose_IM_lg_mean=self.EEC_dose_mamm(self.EEC_diet_mamm, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.ARQ_dose_IM_md_mean=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet_mamm, self.EEC_diet, bw_herp_a_md, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm)
        self.ARQ_dose_IM_lg_mean=self.ARQ_dose_mamm(self.EEC_dose_mamm, self.EEC_diet_mamm, self.EEC_diet, bw_herp_a_lg, self.fi_herp, self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm)

        self.EEC_dose_TP_md_mean=self.EEC_dose_tp(self.EEC_diet_tp, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, bw_herp_a_md, c_herp_a, wp_herp_a_sm, wp_herp_a_md)
        self.EEC_dose_TP_lg_mean=self.EEC_dose_tp(self.EEC_diet_tp, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, bw_herp_a_lg, c_herp_a, wp_herp_a_sm, wp_herp_a_md)
        self.ARQ_dose_TP_md_mean=self.ARQ_dose_tp(self.EEC_dose_tp, self.EEC_diet_tp, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm, wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_md, bw_avian_ld50, mineau_scaling_factor)
        self.ARQ_dose_TP_lg_mean=self.ARQ_dose_tp(self.EEC_dose_tp, self.EEC_diet_tp, self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm, wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_lg, bw_avian_ld50, mineau_scaling_factor)

        #Table 9
        self.EEC_diet_herp_BL_mean=self.EEC_diet(self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.EEC_ARQ_herp_BL_mean=self.ARQ_diet_herp(self.EEC_diet, avian_lc50, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.EEC_diet_herp_FR_mean=self.EEC_diet(self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.EEC_ARQ_herp_FR_mean=self.ARQ_diet_herp(self.EEC_diet, avian_lc50, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.EEC_diet_herp_HM_mean=self.EEC_diet_mamm(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_ARQ_herp_HM_mean=self.ARQ_diet_mamm(self.EEC_diet_mamm, self.EEC_diet, avian_lc50, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_diet_herp_IM_mean=self.EEC_diet_mamm(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_ARQ_herp_IM_mean=self.ARQ_diet_mamm(self.EEC_diet_mamm, self.EEC_diet, avian_lc50, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_diet_herp_TP_mean=self.EEC_diet_tp(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.EEC_ARQ_herp_TP_mean=self.ARQ_diet_tp(self.EEC_diet_tp, self.EEC_diet, avian_lc50, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        #Table 10
        self.EEC_diet_herp_BL_mean=self.EEC_diet(self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.EEC_CRQ_herp_BL_mean=self.CRQ_diet_herp(self.EEC_diet, avian_NOAEC, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.EEC_diet_herp_FR_mean=self.EEC_diet(self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.EEC_CRQ_herp_FR_mean=self.CRQ_diet_herp(self.EEC_diet, avian_NOAEC, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.EEC_diet_herp_HM_mean=self.EEC_diet_mamm(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_CRQ_herp_HM_mean=self.CRQ_diet_mamm(self.EEC_diet_mamm, self.EEC_diet, avian_NOAEC, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_diet_herp_IM_mean=self.EEC_diet_mamm(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_CRQ_herp_IM_mean=self.CRQ_diet_mamm(self.EEC_diet_mamm, self.EEC_diet, avian_NOAEC, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.EEC_diet_herp_TP_mean=self.EEC_diet_tp(self.EEC_diet, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.EEC_CRQ_herp_TP_mean=self.CRQ_diet_tp(self.EEC_diet_tp, self.EEC_diet, avian_NOAEC, self.C_0, self.C_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)


    def fi_herp(self, aw_herp, mf_w_herp):
        try:
            aw_herp = float(aw_herp)
            mf_w_herp = float(mf_w_herp)           
        except IndexError:
            raise IndexError\
            ('The body weight of the assessed bird, and/or the mass fraction of '\
            'water in the food must be supplied on the command line.')
        except ValueError:
            raise ValueError\
            ('The body weight of the assessed bird must be a real number, not "%g"' % aw_herp)
        except ValueError:
            raise ValueError\
            ('The mass fraction of water in the food for bird must be a real number, not "%g"' % mf_w_herp)
        if aw_herp < 0:
            raise ValueError\
            ('The body weight of the assessed bird=%g is a non-physical value.' % aw_herp)
        if mf_w_herp < 0:
            raise ValueError\
            ('The fraction of water in the food for bird=%g is a non-physical value.' % mf_w_herp)        
        if mf_w_herp >= 1:
            raise ValueError\
            ('The fraction of water in the food for bird=%g must be less than 1.' % mf_w_herp)   
        return (0.013* (aw_herp**0.773))/(1-mf_w_herp)

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

    def at_bird(self, avian_ld50, bw_herp, tw_bird, mineau_scaling_factor):
        try:
            avian_ld50 = float(avian_ld50)
            bw_herp = float(bw_herp)
            tw_bird = float(tw_bird)
            mineau_scaling_factor = float(mineau_scaling_factor)
        except IndexError:
            raise IndexError\
            ('The lethal dose, body weight of assessed bird, body weight of tested'\
            ' bird, and/or Mineau scaling factor for birds must be supplied on'\
            ' the command line.')
        except ValueError:
            raise ValueError\
            ('The lethal dose must be a real number, not "%mg/kg"' %avian_ld50)
        except ValueError:
            raise ValueError\
            ('The body weight of assessed bird must be a real number, not "%g"' %bw_herp)
        except ValueError:
            raise ValueError\
            ('The body weight of tested bird must be a real number, not "%g"' %tw_bird)
        except ValueError:
            raise ValueError\
            ('The Mineau scaling factor for birds must be a real number' % mineau_scaling_factor)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The body weight of tested bird must be non-zero.')
        if avian_ld50 < 0:
            raise ValueError\
            ('ld50=%g is a non-physical value.' % avian_ld50)
        if bw_herp < 0:
            raise ValueError\
            ('bw_herp=%g is a non-physical value.' % bw_herp)
        if tw_bird < 0:
            raise ValueError\
            ('tw_bird=%g is a non-physical value.' % tw_bird)
        if mineau_scaling_factor < 0:
            raise ValueError\
            ('mineau_scaling_factor=%g is non-physical value.' %mineau_scaling_factor)
        return (avian_ld50) * ((bw_herp/tw_bird)**(mineau_scaling_factor-1))

    # Acute adjusted toxicity value for mammals

    def at_mamm(ld50_mamm,aw_mamm,tw_mamm):
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

    def ANOAEL_mamm(NOAEL_mamm,aw_mamm,tw_mamm):
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
        
    #Dietary based EECs

    def EEC_diet(self, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l):
        C_0=C_0(a_r, a_i, para)
        try:
            n_a = float(n_a)
            i_a = float(i_a)        
        except IndexError:
            raise IndexError\
            ('The number of applications, and/or the interval between applications '\
             'must be supplied on the command line.')
        except ValueError:
            raise ValueError\
            ('The number of applications must be a real number, not "%g"' % n_a)        
        except ValueError:
            raise ValueError\
            ('The interval between applications must be a real number, not "%g"' % i_a)                
        if n_a < 0:
            raise ValueError\
            ('The number of applications=%g is a non-physical value.' % n_a)    
        if i_a < 0:
            raise ValueError\
            ('The interval between applications=%g is a non-physical value.' % i_a)      
        if a_i*n_a > 365:
            raise ValueError\
            ('The schduled application=%g is over the modeling period (1 year).' % i_a*n_a)     

        #C_temp=[1.0]*365 #empty array to hold the concentrations over days   
        C_temp=np.ones((365,1)) #empty array to hold the concentrations over days       
        a_p_temp=0  #application period temp  
        n_a_temp=0  #number of existed applications
        
        for i in range (0,365):
            if i==0: 
                a_p_temp=0
                n_a_temp=n_a_temp+1
                C_temp[i]=C_0
            elif a_p_temp==(i_a-1) and n_a_temp<n_a:
                a_p_temp=0
                n_a_temp=n_a_temp+1
                C_temp[i]=C_t(C_temp[i-1], h_l)+C_0        
            elif a_p_temp<(i_a-1) and n_a_temp<=n_a:
                a_p_temp=a_p_temp+1
                C_temp[i]=C_t(C_temp[i-1], h_l)        
            else :
                C_temp[i]=C_t(C_temp[i-1], h_l) 
        return (max(C_temp))


    #Dietary_mammal based EECs

    def EEC_diet_mamm(self, EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_mamm, c_mamm, wp_mamm):
        EEC_diet=EEC_diet(C_0, C_t, n_a, i_a, a_r, a_i, para, h_l)
        fi_mamm=fi_mamm(c_mamm, wp_mamm)
        return (EEC_diet*fi_mamm/(c_mamm))

    #Dietary terrestrial phase based EECs

    def EEC_diet_tp(self, EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_herp, c_herp, wp_herp):
        EEC_diet=EEC_diet(C_0, C_t, n_a, i_a, a_r, a_i, para, h_l)
        fi_herp=fi_herp(c_herp, wp_herp)
        return (EEC_diet*fi_herp/(c_herp))

    # Amphibian Dose based EECs

    def EEC_dose_herp(self, EEC_diet, bw_herp, fi_herp, wp_herp, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l):        
        fi_herp=fi_herp(bw_herp, wp_herp)
        EEC_diet=EEC_diet(C_0, C_t, n_a, i_a, a_r, a_i, para, h_l)
        return (EEC_diet*fi_herp/bw_herp)

    # Amphibian Dose based EECs for mammals

    def EEC_dose_mamm(self, EEC_diet_mamm, EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_mamm, bw_herp, c_mamm, wp_mamm):
        EEC_diet_mamm=EEC_diet_mamm(EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_mamm, c_mamm, wp_mamm)
        return (EEC_diet_mamm*c_mamm/bw_herp)

    # Amphibian Dose based EECs for terrestrial

    def EEC_dose_tp(self, EEC_diet_tp, EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_herp, bw_herp, c_herp, wp_herp, wp_herp_a):
        EEC_diet_tp=EEC_diet_tp(EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_herp, c_herp, wp_herp)
        fi_herp=fi_herp(bw_herp, wp_herp_a)
        return (EEC_diet_tp*fi_herp/bw_herp)
            
    # Amphibian acute dose-based risk quotients  

    def ARQ_dose_herp(self, EEC_dose_herp, EEC_diet, bw_herp, fi_herp, at_bird, avian_ld50, tw_bird, mineau_scaling_factor, wp_herp, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l):
        EEC_dose_herp=EEC_dose_herp(EEC_diet, bw_herp, fi_herp, wp_herp, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l)
        at_bird=at_bird(avian_ld50,bw_herp,tw_bird,mineau_scaling_factor)
        return (EEC_dose_herp/at_bird)

    # Amphibian acute dose-based risk quotients for mammals

    def ARQ_dose_mamm(self, EEC_dose_mamm, EEC_diet_mamm, EEC_diet, bw_herp, fi_herp, at_bird, avian_ld50, tw_bird, mineau_scaling_factor, c_mamm, wp_mamm, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_mamm):
        EEC_dose_mamm=EEC_dose_mamm(EEC_diet_mamm, EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_mamm, bw_herp, c_mamm, wp_mamm)
        at_bird=at_bird(avian_ld50,bw_herp,tw_bird,mineau_scaling_factor)
        return (EEC_dose_mamm/at_bird)


    # Amphibian acute dose-based risk quotients for tp

    def ARQ_dose_tp(self, EEC_dose_tp, EEC_diet_tp, EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_herp, c_herp, wp_herp, wp_herp_a, at_bird, avian_ld50, bw_herp, tw_bird, mineau_scaling_factor):
        EEC_dose_tp=EEC_dose_tp(EEC_diet_tp, EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_herp, bw_herp, c_herp, wp_herp, wp_herp_a)
        at_bird=at_bird(avian_ld50,bw_herp,tw_bird,mineau_scaling_factor)
        return (EEC_dose_tp/at_bird)
            
    # Amphibian acute dietary-based risk quotients

    def ARQ_diet_herp(self, EEC_diet, avian_lc50, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l):
        EEC_diet=EEC_diet(C_0, C_t, n_a, i_a, a_r, a_i, para, h_l)         
        return (EEC_diet/avian_lc50)

    # Amphibian acute dietary-based risk quotients for mammals

    def ARQ_diet_mamm(self, EEC_diet_mamm, EEC_diet, avian_lc50, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_mamm, c_mamm, wp_mamm):
        EEC_diet_mamm=EEC_diet_mamm(EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_mamm, c_mamm, wp_mamm)
        return (EEC_diet_mamm/avian_lc50)

    # Amphibian acute dietary-based risk quotients for tp

    def ARQ_diet_tp(self, EEC_diet_tp, EEC_diet, avian_lc50, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_herp, c_herp, wp_herp):
        EEC_diet_tp=EEC_diet_tp(EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_herp, c_herp, wp_herp)
        return (EEC_diet_tp/avian_lc50)

    # Amphibian chronic dietary-based risk quotients

    def CRQ_diet_herp(self, EEC_diet, avian_NOAEC, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l):
        EEC_diet=EEC_diet(C_0, C_t, n_a, i_a, a_r, a_i, para, h_l)      
        return (EEC_diet/avian_NOAEC)
            
    # Amphibian chronic dietary-based risk quotients for mammal

    def CRQ_diet_mamm(self, EEC_diet_mamm, EEC_diet, avian_NOAEC, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_mamm, c_mamm, wp_mamm):
        EEC_diet_mamm=EEC_diet_mamm(EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_mamm, c_mamm, wp_mamm)
        return (EEC_diet_mamm/avian_NOAEC)

    # Amphibian chronic dietary-based risk quotients for tp

    def CRQ_diet_tp(self, EEC_diet_tp, EEC_diet, avian_NOAEC, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_herp, c_herp, wp_herp):
        EEC_diet_tp=EEC_diet_tp(EEC_diet, C_0, C_t, n_a, i_a, a_r, a_i, para, h_l, fi_herp, c_herp, wp_herp)
        return (EEC_diet_tp/avian_NOAEC)

