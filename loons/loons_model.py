import math
import logging
import sys
import numpy as np
import copy

class loons(object):
    def __init__(self, b, m, r, pa, sj, t, no1, no2, no3, no4):
        self.b = float(b)
        self.m = float(m)
        self.r = float(r)
        self.pa = float(pa)
        self.sj = float(sj)
        self.t = int(t)
        self.no1 = float(no1)
        self.no2 = float(no2)
        self.no3 = float(no3)
        self.no4 = float(no4)
        self.b_mu = 0.80
        self.b_v = 0.02**2

        self.sj_mu = 0.45
        self.sj_v = 0.2**2

        self.pa_mu = 0.92
        self.pa_v = 0.013**2

        self.m_mu = 0.58
        self.m_v = 0.03**2

        n_o = np.zeros(shape=(4,1))
        n_o[0] = no1
        n_o[1] = no2
        n_o[2] = no3
        n_o[3] = no4
        self.n_o = n_o


        # n_o =[no1, no2, no3, no4]
        # self.n_o = np.asarray(n_o)

        self.fa = (self.pa**(10.0/12.0))*self.b*self.m*self.r

        l_m = np.zeros(shape=(4,4))
        l_m[1,0] = self.sj
        l_m[2,1] = self.sj
        l_m[3,2] = self.sj
        l_m[0,3] = self.fa
        l_m[3,3] = self.pa
        self.l_m = l_m

        self.eig_dom = self.eigdom(self.l_m)
        self.rj = (self.sj/self.eig_dom)**2/(1+(self.sj/self.eig_dom)+(self.sj/self.eig_dom)**2)
        self.gj = self.sj*self.rj
        self.pj = self.sj*(1-self.rj)

        l_s = np.zeros(shape=(2,2))
        l_s[0,0] = self.pj
        l_s[0,1] = self.fa
        l_s[1,0] = self.gj
        l_s[1,1] = self.pa
        self.l_s = l_s

        self.sen_gj = self.elastic(self.eigdom, self.l_s, 1,0)[0]
        self.sen_pj = self.elastic(self.eigdom, self.l_s, 0,0)[0]
        self.sen_fa = self.elastic(self.eigdom, self.l_s, 0,1)[0]
        self.sen_b = self.elastic_low(self.eigdom, self.l_s, "b")[0]
        self.sen_m = self.elastic_low(self.eigdom, self.l_s, "m")[0]
        self.sen_sj = self.elastic_low(self.eigdom, self.l_s, "sj")[0]
        self.sen_rj = self.elastic_low(self.eigdom, self.l_s, "rj")[0]
        self.sen_pa = self.elastic_low(self.eigdom, self.l_s, "pa")[0]

        self.ela_gj = self.elastic(self.eigdom, self.l_s, 1,0)[1]
        self.ela_pj = self.elastic(self.eigdom, self.l_s, 0,0)[1]
        self.ela_fa = self.elastic(self.eigdom, self.l_s, 0,1)[1]
        self.ela_b = self.elastic_low(self.eigdom, self.l_s, "b")[1]
        self.ela_m = self.elastic_low(self.eigdom, self.l_s, "m")[1]
        self.ela_sj = self.elastic_low(self.eigdom, self.l_s, "sj")[1]
        self.ela_rj = self.elastic_low(self.eigdom, self.l_s, "rj")[1]
        self.ela_pa = self.elastic_low(self.eigdom, self.l_s, "pa")[1]

        self.lamda_ci_out = self.lamda_ci(self.eigdom, 10000)
        self.lamda_ci_out_025 = self.lamda_ci_out[1]
        self.lamda_ci_out_975 = self.lamda_ci_out[2]

        self.leslie_out = self.leslie(self.l_m, self.n_o, self.t)

    def leslie(self, l_m, n_o, t):
        ####Initial Leslie Matrix and pesticide conc###########
        S = l_m.shape[1]
        n_f=np.zeros(shape=(S,t))
        n_f[:,0]=n_o.squeeze()
        for i in range(t):
            n=np.dot(l_m, n_o)
            n_o=n
            n_f[:,i]=n.squeeze()
        return n_f.tolist()

    def eigdom(self, l_m):
        eig_pool = np.linalg.eigvals(l_m)
        eig_pool = eig_pool.tolist()
        eig_pool_abs = [abs(k) for k in eig_pool]
        return max(eig_pool_abs)

    def elastic(self, eigdom, l_m, ind_1, ind_2):
        chg = l_m[ind_1, ind_2]*0.1
        eig_old = eigdom(l_m)
        l_m_temp = copy.deepcopy(l_m)
        l_m_temp[ind_1, ind_2] = l_m[ind_1, ind_2]-chg
        eig_new = eigdom(l_m_temp)
        sen = abs(eig_new-eig_old)/chg
        ela = sen*((l_m_temp[ind_1, ind_2]+chg)/eig_old)
        return sen, ela

    def lamda_ci(self, eigdom, n):
        self.b_a = ((1-self.b_mu)/self.b_v-1/self.b_mu)*self.b_mu**2
        self.b_b = self.b_a*(1/self.b_mu-1)
        self.b_rand = np.random.beta(self.b_a, self.b_b, n)

        self.sj_a = ((1-self.sj_mu)/self.sj_v-1/self.sj_mu)*self.sj_mu**2
        self.sj_b = self.sj_a*(1/self.sj_mu-1)
        self.sj_rand = np.random.beta(self.sj_a, self.sj_b, n)

        self.pa_a = ((1-self.pa_mu)/self.pa_v-1/self.pa_mu)*self.pa_mu**2
        self.pa_b = self.pa_a*(1/self.pa_mu-1)
        self.pa_rand = np.random.beta(self.pa_a, self.pa_b, n)

        self.m_mu_n = np.log(self.m_mu**2/(self.m_mu**2+self.m_v)**0.5)
        self.m_v_n = (np.log((self.m_v/self.m_mu**2)+1))**0.5
        self.m_rand = np.random.lognormal(self.m_mu_n, self.m_v_n, n)
        l_s_eig_dom_rand = np.zeros(shape=(n,1))

        for i in range(n):
            fa_temp = (self.pa_rand[i]**(10.0/12.0))*self.b_rand[i]*self.m_rand[i]*self.r
            l_m_temp = np.zeros(shape=(4,4))
            l_m_temp[1,0] = self.sj_rand[i]
            l_m_temp[2,1] = self.sj_rand[i]
            l_m_temp[3,2] = self.sj_rand[i]
            l_m_temp[0,3] = fa_temp
            l_m_temp[3,3] = self.pa_rand[i]
            eig_dom_temp = eigdom(l_m_temp)

            rj_temp = (self.sj_rand[i]/eig_dom_temp)**2/(1+(self.sj_rand[i]/eig_dom_temp)+(self.sj_rand[i]/eig_dom_temp)**2)
            gj_temp = self.sj_rand[i]*rj_temp
            pj_temp = self.sj_rand[i]*(1-rj_temp)

            l_s_temp = np.zeros(shape=(2,2))
            l_s_temp[0,0] = pj_temp
            l_s_temp[0,1] = fa_temp
            l_s_temp[1,0] = gj_temp
            l_s_temp[1,1] = self.pa_rand[i]
            l_s_eig_dom_rand[i] = eigdom(l_s_temp)
        l_s_eig_dom_025 = np.percentile(l_s_eig_dom_rand, 2.5)
        l_s_eig_dom_975 = np.percentile(l_s_eig_dom_rand, 97.5)
        return l_s_eig_dom_rand, l_s_eig_dom_025, l_s_eig_dom_975

    def elastic_low(self, eigdom, l_m, var):
        eig_old = eigdom(l_m)
        l_m_temp = copy.deepcopy(l_m)
        if var== "b":
            b_new = self.b*0.9
            fa_new = (self.pa**(10.0/12.0))*b_new*self.m*self.r
            l_m_temp[0, 1] = fa_new
            eig_new = eigdom(l_m_temp)
            sen = abs(eig_new-eig_old)/(self.b-b_new)
            ela = sen*(self.b/eig_old)
        if var== "m":
            m_new = self.m*0.9
            fa_new = (self.pa**(10.0/12.0))*self.b*m_new*self.r
            l_m_temp[0, 1] = fa_new
            eig_new = eigdom(l_m_temp)
            sen = abs(eig_new-eig_old)/(self.m-m_new)
            ela = sen*(self.m/eig_old)
        if var== "sj":
            sj_new = self.sj*0.9
            l_m_new = np.zeros(shape=(4,4))
            l_m_new[1,0] = sj_new
            l_m_new[2,1] = sj_new
            l_m_new[3,2] = sj_new
            l_m_new[0,3] = self.fa
            l_m_new[3,3] = self.pa
            l_m_new_eig = eigdom(l_m_new)
            rj_new = (sj_new/l_m_new_eig)**2/(1+(sj_new/l_m_new_eig)+(sj_new/l_m_new_eig)**2)
            gj_new = sj_new*rj_new
            pj_new = sj_new*(1-rj_new)
            l_m_temp[0, 0] = pj_new
            l_m_temp[1, 0] = gj_new
            eig_new = eigdom(l_m_temp)
            sen = abs(eig_new-eig_old)/(self.sj-sj_new)
            ela = sen*(self.sj/eig_old)
        if var== "rj":
            rj_new = self.rj*0.90
            gj_new = self.sj*rj_new
            pj_new = self.sj*(1-rj_new)
            l_m_temp[0, 0] = pj_new
            l_m_temp[1, 0] = gj_new
            eig_new = eigdom(l_m_temp)
            sen = abs(eig_new-eig_old)/(self.rj-rj_new)
            ela = sen*(self.rj/eig_old)
        if var== "pa":
            pa_new = self.pa*0.90
            fa_new = (pa_new**(10.0/12.0))*self.b*self.m*self.r
            l_m_temp[0, 1] = fa_new
            l_m_temp[1, 1] = pa_new
            eig_new = eigdom(l_m_temp)
            sen = abs(eig_new-eig_old)/(self.pa-pa_new)
            ela = sen*(self.pa/eig_old)
        return sen, ela

# test = loons(0.80, 0.58, 0.50, 0.92, 0.75, 10, 3, 0, 1, 2)

# print test.leslie_out
# print 'sen_fa', test.sen_fa, test.ela_fa
# print 'sen_pj', test.sen_pj, test.ela_pj
# print 'sen_gj', test.sen_gj, test.ela_gj
# print 'sen_b', test.sen_b, test.ela_b
# print 'sen_m', test.sen_m, test.ela_m
# print 'sen_sj', test.sen_sj, test.ela_sj
# print 'sen_rj', test.sen_rj, test.ela_rj
# print 'sen_pa', test.sen_pa, test.ela_pa

# print test.b_mu, test.b_v, test.b_a, test.b_b
# print test.sj_mu, test.sj_v, test.sj_a, test.sj_b
# print test.pa_mu, test.pa_v, test.pa_a, test.pa_b
# print test.m_mu, test.m_v, test.m_mu_n, test.m_v_n

# print test.lamda_ci_out_025
# print test.lamda_ci_out_975