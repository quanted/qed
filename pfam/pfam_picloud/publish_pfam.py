import cloud
import sys 
import os
lib_path = os.path.abspath('../../..')
sys.path.append(lib_path)
from ubertool_src import keys_Picloud_S3

cloud.setkey(keys_Picloud_S3.picloud_api_key, keys_Picloud_S3.picloud_api_secretkey)   

def pfam(input_list): 
    import os, sys
    lib_path = os.path.abspath('/home/picloud/pfam_picloud')
    sys.path.append(lib_path)
    
    wat_hl=input_list[0]
    wat_t=input_list[1]
    ben_hl=input_list[2]
    ben_t=input_list[3]
    unf_hl=input_list[4]
    unf_t=input_list[5]
    aqu_hl=input_list[6]
    aqu_t=input_list[7]
    hyd_hl=input_list[8]
    mw=input_list[9]
    vp=input_list[10]
    sol=input_list[11]
    koc=input_list[12]
    hea_h=input_list[13]
    hea_r_t=input_list[14]
    noa=input_list[15]
    dd_out=input_list[16]
    mm_out=input_list[17]
    ma_out=input_list[18]
    sr_out=input_list[19]
    weather=input_list[20]
    wea_l=input_list[21]
    nof=input_list[22]
    date_f1=input_list[23]
    nod_out=input_list[24]
    fl_out=input_list[25]
    wl_out=input_list[26]
    ml_out=input_list[27]
    to_out=input_list[28]
    zero_height_ref=input_list[29]
    days_zero_full=input_list[30]
    days_zero_removal=input_list[31]
    max_frac_cov=input_list[32]
    mas_tras_cof=input_list[33]
    leak=input_list[34]
    ref_d=input_list[35]
    ben_d=input_list[36]
    ben_por=input_list[37]
    dry_bkd=input_list[38]
    foc_wat=input_list[39]
    foc_ben=input_list[40]
    ss=input_list[41]
    wat_c_doc=input_list[42]
    chl=input_list[43]
    dfac=input_list[44]
    q10=input_list[45] 
    area_app=input_list[46] 
    
    import pfam_pi
    ff=pfam_pi.pfam_pi(wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
           noa,dd_out,mm_out,ma_out,sr_out,weather,wea_l,nof,date_f1,nod_out,fl_out,wl_out,ml_out,to_out,
           zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
           ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10,area_app)
   
    return ff
 
cloud.rest.publish(func=pfam, label='pfam_s1', _env='t-fortran77-test', _type='s1', _profile=True )

print 'Done'


