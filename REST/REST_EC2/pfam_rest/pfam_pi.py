#!/usr/bin/python
#
def pfam_pi(wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
           noa,dd_out,mm_out,ma_out,sr_out,weather, wea_l,nof,date_f1,nod_out,fl_out,wl_out,ml_out,to_out,
           zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
           ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10,area_app):
    import os
    import shutil
    import subprocess
    import zipfile
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key
    from boto.s3.bucket import Bucket
    import string
    import random
    import operator
    import re
    import keys_Picloud_S3

    # Generate a random ID for file save
    def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    name_temp=id_generator()

##########################################################################################
#####AMAZON KEY, store output files. You might have to write your own import approach#####
##########################################################################################
    key = keys_Picloud_S3.amazon_s3_key
    secretkey = keys_Picloud_S3.amazon_s3_secretkey

##################################################################################
######Create a folder if it does not existed, where holds calculations' output.#####
##################################################################################
    cwd='/home/ubuntu/Rest_EC2/pfam_rest'
    src=cwd
    src1=src+'/'+name_temp
    if not os.path.exists(src1):
        os.makedirs(src1)
    else:
        shutil.rmtree(src1)
        os.makedirs(src1)
    ##
    os.chdir(src1)
    met="wTest.dvf"
    inp="pfam_input.PFA"
    exe="pfam_pi.exe"
    exe2="pfam_post.exe"   

########Copy files to the tempt folder#############
    shutil.copy(src+"/"+met,src1)
    shutil.copy(cwd+"/"+exe,src1)
    shutil.copy(cwd+"/"+exe2,src1)    
    shutil.copy(src+"/"+inp,src1)
##########Modify input files##########################
    def update(file_name, wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
               noa,dd_out,mm_out,ma_out,sr_out,weather, wea_l,nof,date_f1,nod_out,fl_out,wl_out,ml_out,to_out,
               zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
               ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10,area_app):
       
        file_name = str(os.getcwd())+'/'+file_name
        
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
        dd_out1 = map(str,map(int, reduce(operator.add, dd_out)))
#        dd_out2=", ".join("".join(map(str,l)) for l in dd_out)+', '+', '.join(map(str, lines16_old))
        lines[16]=", ".join("".join(map(str,l)) for l in dd_out1)+', '+', '.join(map(str, lines16_old))
        
        lines17_old=lines[17].split(",")[int(noa):]
        mm_out1 = map(str,map(int, reduce(operator.add, mm_out)))
        lines[17]=", ".join("".join(map(str,l)) for l in mm_out1)+', '+', '.join(map(str, lines17_old))    
        lines18_old=lines[18].split(",")[int(noa):]
        lines[18]=", ".join("".join(map(str,l)) for l in ma_out)+', '+', '.join(map(str, lines18_old))     
        lines19_old=lines[19].split(",")[int(noa):]
        lines[19]=", ".join("".join(map(str,l)) for l in sr_out)+', '+', '.join(map(str, lines19_old))      
    #####location##############
        lines[20]='./'+weather+'.dvf\n'
        lines[21]=wea_l+'\n'
    #####floods##############
        lines[22]=str(int(nof))+'\n'
        lines[23]=str(int(date_f1[3:5]))+'\n'
        lines[24]=str(int(date_f1[0:2]))+'\n'
        lines25_old=lines[25].split(",")[int(nof):]
        nod_out1 = map(str,map(int, reduce(operator.add, nod_out)))
        lines[25]=", ".join("".join(map(str,l)) for l in nod_out1)+', '+', '.join(map(str, lines25_old)) 
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
        lines[50]=area_app+'\n'
        lines[51]=leak+'\n'
        
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()            

    a=update('pfam_input.PFA', wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
               noa,dd_out,mm_out,ma_out,sr_out,weather, wea_l,nof,date_f1,nod_out,fl_out,wl_out,ml_out,to_out,
               zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
               ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10,area_app)

##########################################    
    ##call the pfam file
    os.chdir(src1)
    a=subprocess.Popen("./"+exe+" "+inp, shell=1)
    while (a.poll() != 0):
        a.wait()

    b=subprocess.Popen("./"+exe2+" pfam_out.TXT", shell=1)
    while (b.poll() != 0):
        b.wait()

##########read the post processed file and get water conc.########
    searchfile = open("pfam_out_ProcessedOutput.txt", "r")
    i=0
    for line in searchfile:
        if "Event#" in line: 
            line_start1=i+2
        if "Maximum released" in line:
            line_end1=i-2
        if "chemical id" in line: 
            line_start2=i+2
        if " ********" in line: 
            line_end2=i-1
        i=i+1
    searchfile.close()
    
    x_water=[]
    x_water_level=[]
    x_ben_tot=[]
    x_ben_por=[]
    x_date1=[]
    x_date2=[]
    x_re_v=[]
    x_re_c=[]
    
    fp = open("pfam_out_ProcessedOutput.txt")
    for i, line in enumerate(fp):
        if (i >= line_start1) and (i <= line_end1):
            line = re.match("(.{5})(.{1})(.{10})(.{17})(.{13})(.{12})", line).groups()
            x_date1_temp = line[2]
            x_date1.append(x_date1_temp)
            x_re_v_temp = line[4]
            x_re_v.append(x_re_v_temp)
            x_re_c_temp = line[5]
            x_re_c.append(x_re_c_temp)
            
        if (i >= line_start2) and (i <= line_end2):
            line = re.match("(.{10})(.{8})(.{8})(.{12})(.{12})(.{12})(.{12})", line).groups()
            x_date2_temp = line[0]
            x_date2.append(x_date2_temp)
            x_water_level_temp = line[1]
            x_water_level.append(x_water_level_temp)
            x_ben_tot_temp = line[4]
            x_ben_tot.append(x_ben_tot_temp)
            x_ben_por_temp = line[5]
            x_ben_por.append(x_ben_por_temp)
            if line[3]=='   ---------':
                x_water_temp = '0'
            else:
                x_water_temp = line[3]
            x_water.append(x_water_temp)
    fp.close()
    
    x_date2_len = len(x_date2)
    x_re_v_f = [0] * x_date2_len
    x_re_c_f = [0] * x_date2_len
    
    for i in x_date1:
        try:
            x_re_v_f[x_date2.index(i)] = x_re_v[x_date1.index(i)]
            x_re_c_f[x_date2.index(i)] = x_re_c[x_date1.index(i)]        
        except:
            x_re_v_f.append(x_re_v[x_date1.index(i)])
            x_re_c_f.append(x_re_c[x_date1.index(i)])
    # print len(x_re_v_f)
########################################################
    fname=os.listdir(src1)
    zout=zipfile.ZipFile("test.zip","w", zipfile.ZIP_DEFLATED)
    ##zip all the file
    for name in fname:
        if name not in [exe, exe2, met]:
            zout.write(name)
    zout.close()
    
    conn = S3Connection(key, secretkey)
    bucket = Bucket(conn, 'pfam')
    k=Key(bucket)
    
    name1='pfam_'+name_temp+'.zip'
    k.key=name1
    k.set_contents_from_filename('test.zip')
    link='https://s3.amazonaws.com/pfam/'+name1
    k.set_acl('public-read-write')
    # print (link)
    os.chdir(src)
    shutil.rmtree(src1)
    return link, x_date1, x_re_v_f, x_re_c_f, x_date2, x_water, x_water_level, x_ben_tot, x_ben_por 

