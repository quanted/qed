import cloud

api_key='3355'
api_secretkey='212ed160e3f416fdac8a3b71c90f3016722856b9'
cloud.setkey(api_key, api_secretkey) 

def exams(input_list): 
    import os, sys
    lib_path = os.path.abspath('/home/picloud/EXAMS_picloud')
    sys.path.append(lib_path)
    
    chem_name = input_list[0]
    scenarios = input_list[1]
    met = input_list[2]
    farm = input_list[3]
    mw = input_list[4]
    sol = input_list[5]
    koc = input_list[6]
    vp = input_list[7]
    aem = input_list[8]
    anm = input_list[9]
    aqp = input_list[10]
    tmper = input_list[11]
    n_ph = input_list[12]
    ph_out = input_list[13]
    hl_out = input_list[14]


    import exams_pi
    ff=exams_pi.exams_pi(chem_name, scenarios, met, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out)
   
    return ff
 
cloud.rest.publish(func=exams, label='exams_s1', _env='t-fortran77-test', _type='s1', _profile=True )


print 'Done'


