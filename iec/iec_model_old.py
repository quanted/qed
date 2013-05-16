import math

def z_score_f(dose_response, LC50, threshold):
    z_score = dose_response * (math.log10(LC50 * threshold) - math.log10(LC50))
    return z_score
    
def F8_f(dose_response, LC50, threshold):
    z_score = z_score_f(dose_response, LC50, threshold)
    F8 = 0.5 * math.erfc(-z_score/math.sqrt(2))
    if F8 == 0:
        F8 = 10^-16
    else:
        F8 = F8
    return F8
    
def chance_f(dose_response, LC50, threshold):    
    chance = 1 / F8_f(dose_response, LC50, threshold)
    return chance