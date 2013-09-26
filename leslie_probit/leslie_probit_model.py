import math
import logging
import sys
import numpy as np

class leslie_probit(object):
    def __init__(self, a_n, c_n, app_target, ai, hl, sol, t, n_a, rate_out, day_out, b, test_species, ld50_test, bw_test, ass_species, bw_ass, x, c, s, l_m, n_o):
        self.a_n = a_n
        self.c_n = c_n
        self.app_target = app_target
        self.ai = float(ai)/100
        self.hl = float(hl)
        self.sol = float(sol)
        self.t = int(t)
        self.n_a = float(n_a)
        self.rate_out = (rate_out)
        self.day_out = (day_out)
        self.b = float(b)
        self.test_species = test_species
        self.ld50_test = float(ld50_test)
        self.bw_test = float(bw_test)
        self.ass_species = ass_species
        self.bw_ass = float(bw_ass)
        self.x = float(x)
        self.c = float(c)
        self.s = int(s)
        self.l_m = l_m
        self.n_o = n_o
        if app_target == "Short Grass":
            para = 240
            self.para = para
        elif app_target == "Tall Grass":
            para = 110
            self.para = para

        self.conc_out=self.conc(self.C_0, self.C_t, self.n_a, self.rate_out, self.ai, self.para, self.hl, self.day_out, self.t)
        self.out = self.dose_bird(self.bw_ass, self.bw_test, self.ld50_test, self.x, self.sol, self.t, self.b, self.c, self.l_m, self.n_o, self.conc_out)
        self.out_no = self.no_dose_bird(self.l_m, self.n_o, self.t)

    def C_0(self, rate_out, ai, para):
        return (rate_out*ai*para)

    #Concentration over time
    def C_t(self, C_ini, hl):    
        return (C_ini*np.exp(-(np.log(2)/hl)*1))

    def conc(self, C_0, C_t, n_a, rate_out, ai, para, hl, day_out, t):
        if n_a == 1:
            C_temp = C_0(rate_out[0], ai, para)
            return C_temp
        else:
            C_temp = [] #empty array to hold the concentrations over days       
            n_a_temp = 0  #number of existing applications
            dayt = 0
            day_out_l=len(day_out)
            for i in range (0,t):
                if i==0:  #first day of application
                    C_temp.append(C_0(rate_out[0], ai, para))
                    n_a_temp = n_a_temp + 1
                    dayt = dayt + 1
                elif dayt<=day_out_l-1 and n_a_temp<=n_a: # next application day
                    if i==day_out[dayt]:
                        C_temp.append(C_t(C_temp[i-1], hl) + C_0(rate_out[dayt], ai, para))
                        n_a_temp = n_a_temp + 1
                        dayt = dayt + 1        
                    else :
                        C_temp.append(C_t(C_temp[i-1], hl))
                else:
                    C_temp.append(C_t(C_temp[i-1], hl) )
            return C_temp

    # def conc(self, C_0, C_t, n_a, rate_out, ai, para, hl, day_out, t):
    #     if n_a == 1:
    #         C_temp = C_0(rate_out[0], ai, para)
    #         return C_temp
    #     else:
    #         C_temp = np.zeros((t,1)) #empty array to hold the concentrations over days       
    #         n_a_temp = 0  #number of existing applications
    #         dayt = 0
    #         day_out_l=len(day_out)
    #         for i in range (0,t):
    #             if i==0:  #first day of application
    #                 C_temp[i] = C_0(rate_out[0], ai, para)
    #                 n_a_temp = n_a_temp + 1
    #                 dayt = dayt + 1
    #             elif dayt<=day_out_l-1 and n_a_temp<=n_a: # next application day
    #                 if i==day_out[dayt]:
    #                     C_temp[i] = C_t(C_temp[i-1], hl) + C_0(rate_out[dayt], ai, para)
    #                     n_a_temp = n_a_temp + 1
    #                     dayt = dayt + 1        
    #                 else :
    #                     C_temp[i]=C_t(C_temp[i-1], hl) 
    #             else:
    #                 C_temp[i]=C_t(C_temp[i-1], hl) 
    #         return C_temp


    def dose_bird(self, aw_bird, bw_bird, ld50_a, x, sol, t, b, c, l_m, n_o, conc_all):
        ####Initial Leslie Matrix and pesticide conc###########
        S = l_m.shape[1]
        n_f=np.zeros(shape=(S,t))

        l_m_temp=np.zeros(shape=(S,S), dtype=float)
        n_csum=np.sum(n_o)
        n_f[:,0]=n_o.squeeze()

        fw_bird = (1.180 * (aw_bird**0.874))/1000.0
        m=[]
        dose_out = []
        z_out = []

        for i in range(t):
            # C_temp = C_temp*np.exp(-(np.log(2)/h_l)*1)
            C_temp = conc_all[i]
            if C_temp >= sol:
                dose_bird = (fw_bird * C_temp)/(aw_bird / 1000)
            else:
                dose_bird = (fw_bird * C_temp[0])/(aw_bird / 1000)
            at_bird = (ld50_a) * ((aw_bird/bw_bird)**(x-1))
            # print at_bird
            z = b*(np.log10(dose_bird)-np.log10(at_bird))
            m_temp = 1-0.5*(1+math.erf(z/1.4142))

            for j in range(0, S):
                l_m_temp[0,j]=l_m[0,j]*np.exp(-c*n_csum)
                if j-1>=0:
                    l_m_temp[j,j-1]=l_m[j,j-1]*m_temp
                    l_m_temp[S-1,S-1]=l_m[S-1,S-1]*m_temp

            n=np.dot(l_m_temp, n_o)
            n_csum=np.sum(n)
            n_o=n
            n_f[:,i]=n.squeeze()

            m.append(m_temp)
            dose_out.append(dose_bird)
            z_out.append(z)

        return fw_bird, dose_out, at_bird, m, n_f.tolist(), z_out


    def no_dose_bird(self, l_m, n_o, t):
        ####Initial Leslie Matrix and pesticide conc###########
        S = l_m.shape[1]
        n_f=np.zeros(shape=(S,t))
        n_f[:,0]=n_o.squeeze()
        for i in range(t):
            n=np.dot(l_m, n_o)
            n_o=n
            n_f[:,i]=n.squeeze()
        return n_f.tolist()

# ld50_test_t = 783 
# bw_test_t = 178
# sol_t = 70
# bw_ass_t = 4500
# hl_t = 30        #day-1
# rate_out_t = [4, 10, 20]  #(lb ai/acre)
# ai_t = 0.419
# b_t = 4.5
# c_t = 0.00548
# t_t = 365
# n_a_t = 3
# para_t = 240
# day_out_t = [0, 10, 20]
# x_t = 1.15
# s_t = 3

# n_o_t = np.asarray([300, 400, 200])
# l_m_t = np.asarray([[0, 0.880, 1.860], [0.445, 0, 0], [0, 0.616, 0.610]])


# test_obj=leslie_probit('animal_1', 'chem_1', "Short Grass", ai_t, hl_t, sol_t, t_t, n_a_t, rate_out_t, day_out_t, b_t, 'test_species', ld50_test_t, bw_test_t, 'ass_species', bw_ass_t, x_t, c_t, s_t, l_m_t, n_o_t)

# print test_obj.b[2]




