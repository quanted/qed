#!/usr/bin/python
#

import os
import stat
import shutil
import subprocess
import numpy as np
from scipy.optimize import leastsq
import zipfile
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucket import Bucket
import string
import random
import operator
import simplejson
import keys_Picloud_S3


def exams_pi(chem_name, scenarios, met, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out):
    # Generate a random ID for file save
    def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))
    name_temp=id_generator()

    ##################################################################################
    ######Create a folder if it does not existed, where holds calculations' output.#####
    ##################################################################################
    cwd='/home/ubuntu/Rest_EC2/exams_rest'
    src=cwd
    src1=cwd+'/'+name_temp
    if not os.path.exists(src1):
        os.makedirs(src1)
    else:
        shutil.rmtree(src1)
        os.makedirs(src1)

    os.chdir(src1)

    met=met
    inp="exams_inputs.EXA"
    exe="exams.exe"
    pond="pond298.exv"
    daf="exams.daf"

    # ########Copy files to the tempt folder#############
    shutil.copy(src+"/dvf_pool/"+met,src1)
    shutil.copy(src+"/"+inp,src1)
    shutil.copy(src+"/"+exe,src1)
    shutil.copy(cwd+"/"+pond,src1)
    shutil.copy(cwd+"/"+daf,src1)

    # print(os.getcwd())
    # print(os.listdir(src1))   #check what files are copied
    # print(os.listdir(cwd))   #check what files are copied

    ##########Modify input files##########################
    def update(chem_name, scenarios, met, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out):
        file_name = str(os.getcwd())+'/'+inp
        lines = open(file_name, 'r').readlines() 
        # print vars(exams_obj)
        lines[8] = "chem name is " + chem_name + '\n'
        lines[9] = "set mwt(1)= %10.4E"%float(mw) + '\n'
        lines[10] = "set sol(1,1)= %10.4E"%float(sol) + '\n'
        lines[12] = "set Koc(1)= %10.4E"%float(koc) + '\n'
        lines[13] = "set vapr(1)= %10.4E"%float(vp) + '\n'

        if anm > 0:
            kbacs = np.log(2)/(float(anm)*24.0)
        else:
            kbacs=0
        lines[15]="set kbacs(*,1,1)= %10.4E"%(kbacs) + '\n'

        if aem > 0:
            kbacw = np.log(2)/(float(aem)*24.0)
        else:
            kbacw=0
        lines[19]="set kbacw(*,1,1)= %10.4E"%(kbacw) + '\n'

        if aqp > 0:
            kdp = np.log(2)/(float(aqp)*24.0)
        else:
            kdp=0
        lines[22]="set kdp(1,1)= %10.4E"%(kdp) + '\n'

        if farm == "Yes":
            lines[33]="set evap(*,*)=0.0 \n"
            lines[34]="set rain(*)=0.0 \n"
            lines[35]="set npsfl(*,*)=0.0 \n"
            lines[36]="set npsed(*,*)=0.0 \n"
            lines[37]="set stflo(1,*)=0.0 \n"

        hl_out = np.array(hl_out)
        ph_out = np.array(ph_out)
        k_abn =np.array([1, 0, 0])

        def residuals(k_abn, ph_out, tmper, hl_out):
                hr=np.log(2)/(hl_out*24.0)
                ph_adj=6013.79/(float(tmper)+273.15) + 23.6521*np.log10(float(tmper) + 273.15) - 64.7013
                err = peval(k_abn, ph_out, ph_adj) - hr
                return err

        def peval(k_abn, ph_out, ph_adj):
            temp= k_abn[0]*np.power(10,-ph_out) + k_abn[1] + k_abn[2]*np.power(10,(-ph_adj + ph_out))
            return temp

        k_abn = list(leastsq(residuals, k_abn, args=(ph_out, tmper, hl_out), maxfev=200000)[0])
        # print k_abn

        if k_abn[0] < 7.9E-5:
            k_abn[0] = 0
        if k_abn[1] < 7.9E-7:
            k_abn[1] = 0
        if k_abn[2] < 7.9E-5:
            k_abn[2] = 0

        lines[23]="set kah(1,1,1)= %10.4E"%(k_abn[0]) + '\n'
        lines[24]="set knh(1,1,1)= %10.4E"%(k_abn[1]) + '\n'
        lines[25]="set kbh(1,1,1)= %10.4E"%(k_abn[2]) + '\n'
        lines[30]="read meteorology %s"%(met) + '\n'

        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()            
        return lines

    file_update=update(chem_name, scenarios, met, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out)    
    os.listdir(src1)
    # print 'src1===', os.listdir(src1)   #check what files are copied
    a=subprocess.Popen("./exams.exe exams_inputs.EXA", shell=1)
    a.wait()
    # print('done')


    ##########################################################################################
    #####AMAZON KEY, store output files. You might have to write your own import approach#####
    ##########################################################################################
    key = keys_Picloud_S3.amazon_s3_key
    secretkey = keys_Picloud_S3.amazon_s3_secretkey

    ##################################################################################
    ######Zipping output files########################################################
    ##################################################################################
    fname=os.listdir(src1)
    zout=zipfile.ZipFile("exams_all.zip","w", zipfile.ZIP_DEFLATED)
    # print('src2===', os.listdir(src1))   #check what files are copied

    for name in fname:
        if name not in [inp, exe, pond, daf]:
            zout.write(name)
    zout.close()

    #save the zipfile to amazon server
    conn = S3Connection(key, secretkey)
    bucket = Bucket(conn, 'epa_exams')
    k=Key(bucket)

    name1='EXAMS_'+name_temp+'.zip'
    k.key=name1
    k.set_contents_from_filename('exams_all.zip')
    link='https://s3.amazonaws.com/epa_exams/'+name1
    k.set_acl('public-read-write')
    src1_up=os.path.abspath(os.path.join(src1, '..'))
    os.chdir(src1_up)
    shutil.rmtree(src1)
    return link





