import math

class iec(object):
    def __init__(self, dose_response, LC50, threshold):
        self.dose_response = dose_response
        self.LC50 = LC50
        self.threshold = threshold

        #Result variables
        self.z_score_f_out = -1
        self.F8_f_out = -1
        self.chance_f_out = -1
        self.run_methods()


    def run_methods(self):
        try:
            self.z_score_f()
            self.F8_f()
            self.chance_f()
        except TypeError:
            print "Type Error: Your variables are not set correctly."

    def z_score_f(self):
        if self.dose_response < 0:
            raise ValueError\
            ('self.dose_response=%g is a non-physical value.' % self.dose_response)
        if self.LC50 < 0:
            raise ValueError\
            ('self.LC50=%g is a non-physical value.' % self.LC50)
        if self.threshold < 0:
            raise ValueError
            ('self.threshold=%g is a non-physical value.' % self.threshold)
        if self.z_score_f_out == -1:
            self.z_score_f_out = self.dose_response * (math.log10(self.LC50 * self.threshold) - math.log10(self.LC50))
        return self.z_score_f_out
        
    def F8_f(self):
        if self.z_score_f_out == None:
            raise ValueError\
            ('z_score_f variable equals None and therefor this function cannot be run.')
        if self.F8_f_out == -1:
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
        if self.chance_f_out == -1:
            self.chance_f_out = 1 / self.F8_f_out
        return self.chance_f_out

