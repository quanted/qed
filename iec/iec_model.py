import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import math


class iec(object):
    # def __init__(self, set_variables=True,run_methods=True,dose_response=1,LC50=1,threshold=1,vars_dict=None):
    #     self.set_default_variables()
    #     if set_variables:
    #         if vars_dict != None:
    #             self.__dict__.update(vars_dict)
    #         else:
    #             self.set_variables(dose_response,LC50,threshold)
    #         if run_methods:
    #             self.run_methods()

    def __init__(self,dose_response,LC50,threshold):
        self.dose_response = dose_response
        self.LC50 = LC50
        self.threshold = threshold
        self.run_methods()

    # def set_variables(self, dose_response,LC50,threshold):
    #     self.dose_response = dose_response
    #     self.LC50 = LC50
    #     self.threshold = threshold

    # def set_default_variables(self):
    #     self.dose_response = -1
    #     self.LC50 = -1
    #     self.threshold = -1
    #     self.z_score_f_out = -1
    #     self.F8_f_out = -1
    #     self.chance_f_out = -1
        #
        #"_out" need to be added to ea. fun. as expection catching
        #

    # def set_unit_testing_variables(self):
    #     z_score_f_out_expected = None
    #     F8_f_out_expected = None
    #     chance_f_out_expected = None


    # def __str__(self):
    #     string_rep = ''
    #     string_rep = string_rep + "dose_response = %.2e" % self.dose_response
    #     string_rep = string_rep + "LC50 = %.2e" % self.LC50
    #     string_rep = string_rep + "threshold = %.2e" % self.threshold
    #     return string_rep


    def run_methods(self):
        self.z_score_f()
        self.F8_f()
        self.chance_f()

    def z_score_f(self):
        if self.dose_response < 0:
            raise ValueError\
            ('self.dose_response=%g is a non-physical value.' % self.dose_response)
        if self.LC50 < 0:
            raise ValueError\
            ('self.LC50=%g is a non-physical value.' % self.LC50)
        if self.threshold < 0:
            raise ValueError\
            ('self.threshold=%g is a non-physical value.' % self.threshold)    
        self.z_score_f_out = self.dose_response * (math.log10(self.LC50 * self.threshold) - math.log10(self.LC50))
        return self.z_score_f_out
        
    def F8_f(self):
        if self.z_score_f_out == None:
            raise ValueError\
            ('z_score_f variable equals None and therefor this function cannot be run.')
        self.F8_f_out = 0.5 * math.erfc(-self.z_score_f_out/math.sqrt(2))
        if self.F8_f_out == 0:
            self.F8_f_out = 10^-16
        else:
            self.F8_f_out = self.F8_f_out
        return self.F8_f_out
        
    def chance_f(self):
        if self.F8_f_out == None:
            raise ValueError\
            ('F8_f variable equals None and therefor this function cannot be run.')
        self.chance_f_out = 1 / self.F8_f_out
        return self.chance_f_out
