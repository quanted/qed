import cloud
import sys 
import os
lib_path = os.path.abspath('../../..')
sys.path.append(lib_path)
from ubertool_src import keys_Picloud_S3

cloud.setkey(keys_Picloud_S3.picloud_api_key, keys_Picloud_S3.picloud_api_secretkey)    


def PRZM(noa, met, inp, run,  MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft): 
    import os, sys
    lib_path = os.path.abspath('/home/picloud/PRZM_lin_test')
#    lib_path = os.path.abspath('/home/picloud')
    sys.path.append(lib_path)
    import PRZM_pi_new
    ff=PRZM_pi_new.PRZM_pi(noa, met, inp, run, MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft)
#    ff, a, b, c, d=PRZM_pi_new.PRZM_pi(met, inp, run, MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft)    
   
    return ff
 
cloud.rest.publish(func=PRZM, label='PRZM_s1_new', _env='t-fortran77-test', _type='s1', _profile=True)



# , _kill_process=True