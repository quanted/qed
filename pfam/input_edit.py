'''
Created on May 22, 2012

@author: th
'''
import os
import string
import operator

def update(wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
           noa,dd_out,mm_out,ma_out,sr_out,weather, wea_l,nof,date_f1,nod_out,fl_out,wl_out,ml_out,to_out,
           zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
           ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10):
   
    file_name = str(os.getcwd())+'\\pfam\\pfam_input1.PFA' 
    lines = open(file_name, 'r').readlines() 
    lines[0]=wat_hl+'\n'
    lines[1]=ben_hl+'\n'
    lines[2]=unf_hl+'\n'
    lines[3]=aqu_hl+'\n'
    lines[4]=hyd_hl+'\n'
    lines[5]=mw+'\n'
    lines[6]=vp+'\n'
    lines[7]=sol+'\n'
    lines[8]=koc+'\n'
    lines[9]=wat_t+'\n'
    lines[10]=ben_t+'\n'
    lines[11]=unf_t+'\n'
    lines[12]=aqu_t+'\n'
    lines[13]=hea_h+'\n'
    lines[14]=hea_r_t+'\n'
    lines[15]=noa+'\n'
#####applications#############
    lines16_old=lines[16].split(",")[int(noa):]
    lines[16]=", ".join("".join(map(str,l)) for l in dd_out)+', '+', '.join(map(str, lines16_old))
    lines17_old=lines[17].split(",")[int(noa):]
    lines[17]=", ".join("".join(map(str,l)) for l in mm_out)+', '+', '.join(map(str, lines17_old))    
    lines18_old=lines[18].split(",")[int(noa):]
    lines[18]=", ".join("".join(map(str,l)) for l in ma_out)+', '+', '.join(map(str, lines18_old))     
    lines19_old=lines[19].split(",")[int(noa):]
    lines[19]=", ".join("".join(map(str,l)) for l in sr_out)+', '+', '.join(map(str, lines19_old))      
#####location##############
    lines[20]=weather+'\n'
    lines[21]=wea_l+'\n'
#####floods##############
    lines[22]=str(int(nof))+'\n'
    lines[23]=str(int(date_f1[3:5]))+'\n'
    lines[24]=str(int(date_f1[0:2]))+'\n'
    lines25_old=lines[25].split(",")[int(nof):]
    lines[25]=", ".join("".join(map(str,l)) for l in nod_out)+', '+', '.join(map(str, lines25_old)) 
    lines26_old=lines[26].split(",")[int(nof):]
    lines[26]=", ".join("".join(map(str,l)) for l in fl_out)+', '+', '.join(map(str, lines26_old)) 
    lines27_old=lines[27].split(",")[int(nof):]
    lines[27]=", ".join("".join(map(str,l)) for l in wl_out)+', '+', '.join(map(str, lines27_old))     
    lines28_old=lines[28].split(",")[int(nof):]
    lines[28]=", ".join("".join(map(str,l)) for l in ml_out)+', '+', '.join(map(str, lines28_old))     
    lines29_old=lines[29].split(",")[int(nof):]
    lines[29]=", ".join("".join(map(str,l)) for l in to_out)+', '+', '.join(map(str, lines29_old))      
#####crop##############
    lines[30]=str(int(zero_height_ref[3:5]))+'\n'
    lines[31]=str(int(zero_height_ref[0:2]))+'\n'
    lines[32]=str(int(days_zero_full))+'\n'
    lines[33]=str(int(days_zero_removal))+'\n'
    lines[34]=max_frac_cov+'\n'
#####crop##############
    lines[35]=mas_tras_cof+'\n'
    lines[36]=ref_d+'\n'
    lines[37]=ben_d+'\n'
    lines[38]=ben_por+'\n'
    lines[39]=dry_bkd+'\n'
    lines[40]=foc_wat+'\n'
    lines[41]=foc_ben+'\n'
    lines[42]=ss+'\n'
    lines[43]=chl+'\n'
    lines[44]=wat_c_doc+'\n'
    lines[48]=q10+'\n'
    lines[49]=dfac+'\n'
    lines[51]=leak+'\n'
    
    
    return lines
#    out = open(file_name, 'w')
#    out.writelines(lines)
#    out.close()    
    
    
    



