import math

class iec(object):
    def __init__(self, dose_response, LC50, threshold):
        self.dose_response = dose_response
        self.LC50 = LC50
        self.threshold = threshold
        self.run_methods()

    def run_methods(self):
        self.z_score_f()
        self.F8_f()
        self.chance_f()

    def z_score_f(self):
        self.z_score = self.dose_response * (math.log10(self.LC50 * self.threshold) - math.log10(self.LC50))
        return self.z_score
        
    def F8_f(self):
        self.F8 = 0.5 * math.erfc(-self.z_score/math.sqrt(2))
        if self.F8 == 0:
            self.F8 = 10^-16
        else:
            self.F8 = self.F8
        return self.F8
        
    def chance_f(self):    
        self.chance = 1 / self.F8
        return self.chance

