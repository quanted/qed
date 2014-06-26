#!/usr/bin/python
#
import cloud

api_key='3355'
api_secretkey='212ed160e3f416fdac8a3b71c90f3016722856b9'
cloud.setkey(api_key, api_secretkey) 

def PRZM_EXAMS(input_list): 

    import os, sys
    lib_path = os.path.abspath('/home/picloud/PRZM_EXAMS_Picloud')
    sys.path.append(lib_path)

    chem_name = input_list[0]
    noa = input_list[1]
    scenarios = input_list[2]
    unit = input_list[3]
    met = input_list[4]
    inp = input_list[5]
    run = input_list[6]
    exam = input_list[7]
    MM = input_list[8]
    DD = input_list[9]
    YY = input_list[10]
    CAM_f = input_list[11]
    DEPI = input_list[12]
    Ar = input_list[13]
    EFF = input_list[14]
    Drft = input_list[15]
    farm = input_list[16]
    mw = input_list[17]
    sol = input_list[18]
    koc = input_list[19]
    vp = input_list[20]
    aem = input_list[21]
    anm = input_list[22]
    aqp = input_list[23]
    tmper = input_list[24]
    n_ph = input_list[25]
    ph_out = input_list[26]
    hl_out = input_list[27]

    import PRZM_EXAMS_pi
    ff=PRZM_EXAMS_pi.PRZM_EXAMS_pi(chem_name, noa, scenarios, unit, met, inp, run, exam, MM, DD, YY, CAM_f, DEPI, Ar, EFF, Drft, 
                  farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out)
    return ff

cloud.rest.publish(func=PRZM_EXAMS, label='przm_exams_s1', _env='t-fortran77-test', _type='s1', _profile=True )

print 'Done'

