import numpy as np
import logging
import sys


#food intake for birds
class idream(object):
    def __init__(self, tire, ai_name, prod_re, ai):
        self.tire = tire
        self.ai_name = ai_name
        self.prod_re= prod_re
        self.ai = ai
        self.child_c_1 = 0.00378968423517913
        self.child_c_2 = 0.00270897131609988
        self.adult_c = 0.000974955306407856
        self.fe_c = 0.000921903045649652

        self.child_a_1 = 0.00614293864511702
        self.child_a_2 = 0.00404267442168994
        self.adult_a = 0.00149582015112835
        self.fe_a = 0.00142570664813412

        #Table2
        self.exp_child_c_1 = self.exp_cal(self.prod_re, self.ai, self.child_c_1)
        self.exp_child_c_2 = self.exp_cal(self.prod_re, self.ai, self.child_c_2)
        self.exp_adult_c = self.exp_cal(self.prod_re, self.ai, self.adult_c)
        self.exp_fe_c = self.exp_cal(self.prod_re, self.ai, self.fe_c)

        #Table3
        self.exp_child_a_1 = self.exp_cal(self.prod_re, self.ai, self.child_a_1)
        self.exp_child_a_2 = self.exp_cal(self.prod_re, self.ai, self.child_a_2)
        self.exp_adult_a = self.exp_cal(self.prod_re, self.ai, self.adult_a)
        self.exp_fe_a = self.exp_cal(self.prod_re, self.ai, self.fe_a)

    def exp_cal(self, prod_re, ai, exp_deft):
        prod_re = float(prod_re)
        ai = float(ai)           
        exp_deft = float(exp_deft)           

        return (prod_re*ai/0.001)*exp_deft

class idream3(object):
    def __init__(self, tire, ai_name, prod_re, ai, liq_rte, fruit_rte, bread_rte, cheese_rte, veg_rte, meat_rte, pure_rte, piec_rte, powd_rte):
        self.tire = tire
        self.ai_name = ai_name
        self.prod_re= prod_re
        self.ai = ai
        self.liq_rte =  liq_rte
        self.fruit_rte = fruit_rte 
        self.bread_rte = bread_rte 
        self.cheese_rte = cheese_rte
        self.veg_rte = veg_rte
        self.meat_rte = meat_rte
        self.pure_rte = pure_rte
        self.piec_rte = piec_rte
        self.powd_rte = powd_rte

        self.exp_fruit_c_def = [0.00050919587628866, 0.000290160824742268, 0.0000759752577319588, 0.0000719340206185567]
        self.exp_bread_c_def = [0.00176652857142857, 0.000839957142857143, 0.000282, 0.000261857142857143]
        self.exp_cheese_c_def = [0.000245142857142857, 0.000207787755102041, 0.0000677061224489796, 0.0000700408163265306]
        self.exp_veg_c_def = [0.000399407272727273, 0.000175014141414141, 0.000116884444444444, 0.000107508686868687]
        self.exp_meat_c_def = [0.000549213913043478, 0.000524493913043478, 0.000225704347826087, 0.000200984347826087]
        self.exp_pure_c_def = [0.000149908411214953, 0.000150854205607477, 0.0000392504672897196, 0.0000397233644859813]
        self.exp_piec_c_def = [0.0000512233333333334, 0.000371873333333334, 0.000109706666666667, 0.000112126666666667]
        self.exp_powd_c_def = [0.000119064, 0.00014883, 0.000057728, 0.000057728]

        self.fruit_consum_90 = [16.96, 11.15, 3.11, 2.89]
        self.bread_consum_90 = [17.23, 8.15, 2.86, 2.75]
        self.cheese_consum_90 = [3.07, 2.5, 0.81, 0.84]
        self.veg_consum_90 = [15.10, 7.95, 4.52, 4.22]
        self.meat_consum_90 = [11.15, 9.83, 4.21, 3.84]
        self.pure_consum_90 = [9.79, 8.86, 2.47, 2.54]
        self.piec_consum_90 = [4.90, 18.80, 6.10, 6.26]
        self.powd_consum_90 = [3.51, 4.20, 1.51, 1.51]

        self.fruit_consum = [6.3, 3.59, 0.94, 0.89]
        self.bread_consum = [8.77, 4.17, 1.4, 1.3]
        self.cheese_consum = [1.05, 0.89, 0.29, 0.3]
        self.veg_consum = [6.39, 2.8, 1.87, 1.72]
        self.meat_consum = [5.11, 4.88, 2.1, 1.87]
        self.pure_consum = [3.17, 3.19, 0.83, 0.84]
        self.piec_consum = [1.27, 9.22, 2.72, 2.78]
        self.powd_consum = [1.32, 1.65, 0.64, 0.64]

        #Table4
        self.exp_child_c_1 = self.exp_cal_3_c(self.prod_re, self.ai, self.fruit_rte, self.bread_rte, self.cheese_rte, self.veg_rte, self.meat_rte, self.pure_rte, self.piec_rte, self.powd_rte,
                                            self.exp_fruit_c_def[0], self.exp_bread_c_def[0], self.exp_cheese_c_def[0], self.exp_veg_c_def[0], self.exp_meat_c_def[0], self.exp_pure_c_def[0], self.exp_piec_c_def[0], self.exp_powd_c_def[0])
        self.exp_child_c_2 = self.exp_cal_3_c(self.prod_re, self.ai, self.fruit_rte, self.bread_rte, self.cheese_rte, self.veg_rte, self.meat_rte, self.pure_rte, self.piec_rte, self.powd_rte,
                                            self.exp_fruit_c_def[1], self.exp_bread_c_def[1], self.exp_cheese_c_def[1], self.exp_veg_c_def[1], self.exp_meat_c_def[1], self.exp_pure_c_def[1], self.exp_piec_c_def[1], self.exp_powd_c_def[1])
        self.exp_adult_c = self.exp_cal_3_c(self.prod_re, self.ai, self.fruit_rte, self.bread_rte, self.cheese_rte, self.veg_rte, self.meat_rte, self.pure_rte, self.piec_rte, self.powd_rte,
                                            self.exp_fruit_c_def[2], self.exp_bread_c_def[2], self.exp_cheese_c_def[2], self.exp_veg_c_def[2], self.exp_meat_c_def[2], self.exp_pure_c_def[2], self.exp_piec_c_def[2], self.exp_powd_c_def[2])
        self.exp_fe_c = self.exp_cal_3_c(self.prod_re, self.ai, self.fruit_rte, self.bread_rte, self.cheese_rte, self.veg_rte, self.meat_rte, self.pure_rte, self.piec_rte, self.powd_rte,
                                            self.exp_fruit_c_def[3], self.exp_bread_c_def[3], self.exp_cheese_c_def[3], self.exp_veg_c_def[3], self.exp_meat_c_def[3], self.exp_pure_c_def[3], self.exp_piec_c_def[3], self.exp_powd_c_def[3])

        # #Table5
        self.exp_child_a_1 = self.exp_cal_3_a(self.exp_child_c_1, self.fruit_consum[0], self.bread_consum[0], self.cheese_consum[0], self.veg_consum[0], self.meat_consum[0], self.pure_consum[0], self.piec_consum[0], self.powd_consum[0], 
                                              self.fruit_consum_90[0], self.bread_consum_90[0], self.cheese_consum_90[0], self.veg_consum_90[0], self.meat_consum_90[0], self.pure_consum_90[0], self.piec_consum_90[0], self.powd_consum_90[0])
        self.exp_child_a_2 = self.exp_cal_3_a(self.exp_child_c_2, self.fruit_consum[1], self.bread_consum[1], self.cheese_consum[1], self.veg_consum[1], self.meat_consum[1], self.pure_consum[1], self.piec_consum[1], self.powd_consum[1],
                                              self.fruit_consum_90[1], self.bread_consum_90[1], self.cheese_consum_90[1], self.veg_consum_90[1], self.meat_consum_90[1], self.pure_consum_90[1], self.piec_consum_90[1], self.powd_consum_90[1])
        self.exp_adult_a = self.exp_cal_3_a(self.exp_adult_c, self.fruit_consum[2], self.bread_consum[2], self.cheese_consum[2], self.veg_consum[2], self.meat_consum[2], self.pure_consum[2], self.piec_consum[2], self.powd_consum[2],
                                            self.fruit_consum_90[2], self.bread_consum_90[2], self.cheese_consum_90[2], self.veg_consum_90[2], self.meat_consum_90[2], self.pure_consum_90[2], self.piec_consum_90[2], self.powd_consum_90[2])
        self.exp_fe_a = self.exp_cal_3_a(self.exp_fe_c, self.fruit_consum[3], self.bread_consum[3], self.cheese_consum[3], self.veg_consum[3], self.meat_consum[3], self.pure_consum[3], self.piec_consum[3], self.powd_consum[3],
                                         self.fruit_consum_90[3], self.bread_consum_90[3], self.cheese_consum_90[3], self.veg_consum_90[3], self.meat_consum_90[3], self.pure_consum_90[3], self.piec_consum_90[3], self.powd_consum_90[3])

    def exp_cal_3_c(self, prod_re, ai, fruit_rte, bread_rte, cheese_rte, veg_rte, meat_rte, pure_rte, piec_rte, powd_rte,
                  exp_fruit_def, exp_bread_def, exp_cheese_def, exp_veg_def, exp_meat_def, exp_pure_def, exp_piec_def,
                  exp_powd_def):
        prod_re = float(prod_re)
        ai = float(ai)           

        exp_liq_est = 0
        exp_fruit_est = exp_fruit_def*(fruit_rte/0.7)*(prod_re*ai/0.001)
        exp_bread_est = exp_bread_def*(bread_rte/0.2)*(prod_re*ai/0.001)
        exp_cheese_est = exp_cheese_def*(cheese_rte/0.55)*(prod_re*ai/0.001)
        exp_veg_est = exp_veg_def*(veg_rte/0.7)*(prod_re*ai/0.001)
        exp_meat_est = exp_meat_def*(meat_rte/0.8)*(prod_re*ai/0.001)
        exp_pure_est = exp_pure_def*(pure_rte/1.0)*(prod_re*ai/0.001)
        exp_piec_est = exp_piec_def*(piec_rte/0.55)*(prod_re*ai/0.001)
        exp_powd_est = exp_powd_def*(powd_rte/0.2)*(prod_re*ai/0.001)
        exp_list = [exp_liq_est, exp_fruit_est, exp_bread_est, exp_cheese_est, exp_veg_est, exp_meat_est, exp_pure_est, exp_piec_est, exp_powd_est]
        sum_exp_est = sum(exp_list)
        exp_rank = [i[0] for i in sorted(enumerate(exp_list), key=lambda x:x[1])]
        return sum_exp_est, exp_list, exp_rank
# 
    def exp_cal_3_a(self, c_reults, fruit_consum, bread_consum, cheese_consum, veg_consum, meat_consum, pure_consum, piec_consum, powd_consum,
                    fruit_consum_90, bread_consum_90, cheese_consum_90, veg_consum_90, meat_consum_90, pure_consum_90, piec_consum_90, powd_consum_90):
        exp_list_c = c_reults[1]
        exp_list_c_rank = c_reults[2]

        exp_liq_est = 0
        exp_fruit_est = exp_list_c[1]*(fruit_consum_90/fruit_consum)
        exp_bread_est = exp_list_c[2]*(bread_consum_90/bread_consum)
        exp_cheese_est = exp_list_c[3]*(cheese_consum_90/cheese_consum)
        exp_veg_est = exp_list_c[4]*(veg_consum_90/veg_consum)
        exp_meat_est = exp_list_c[5]*(meat_consum_90/meat_consum)
        exp_pure_est = exp_list_c[6]*(pure_consum_90/pure_consum)
        exp_piec_est = exp_list_c[7]*(piec_consum_90/piec_consum)
        exp_powd_est = exp_list_c[8]*(powd_consum_90/powd_consum)

        exp_list_a_pool = [exp_liq_est, exp_fruit_est, exp_bread_est, exp_cheese_est, exp_veg_est, exp_meat_est, exp_pure_est, exp_piec_est, exp_powd_est]
        exp_list_c[exp_list_c_rank[8]] = exp_list_a_pool[exp_list_c_rank[8]]
        exp_list_c[exp_list_c_rank[7]] = exp_list_a_pool[exp_list_c_rank[7]]
        exp_list_a = exp_list_c
        sum_exp_est = sum(exp_list_a)
        return sum_exp_est

# ss=idream3('test', 'tire 2 ', 0.1, 1, 0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)

# print ss.exp_child_c_1[0]
