#!/usr/bin/python
#

import exams_model

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
import re
# from ubertool_src import keys_Picloud_S3
import keys_Picloud_S3

exams_obj = exams_model.exams('chem_name_1', 'CA Almonds MLRA-17', 'Yes', 70, 71, 72, 73, 24, 25, 26, 27, 3, [5.0, 7.0, 11.0], [11.0, 12.0, 10.0])


def exams_pi(exams_obj):
    # Generate a random ID for file save
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))
    name_temp=id_generator()

    ##################################################################################
    ######Create a folder if it does not existed, where holds calculations' output.#####
    ##################################################################################
    cwd=os.getcwd()+'/exams_test'
    print("cwd="+cwd)

    src=cwd
    src1=cwd+'/'+name_temp
    if not os.path.exists(src1):
        os.makedirs(src1)
    else:
        shutil.rmtree(src1)
        os.makedirs(src1)

    os.chdir(src1)

    met=exams_obj.met
    inp="exams_inputs.EXA"
    exe="exams.exe"
    pond="pond298.exv"
    daf="exams.daf"

    # ########Copy files to the tempt folder#############
    shutil.copy(src+"/"+met,src1)
    shutil.copy(src+"/"+inp,src1)
    shutil.copy(src+"/"+exe,src1)
    shutil.copy(cwd+"/"+pond,src1)
    shutil.copy(cwd+"/"+daf,src1)

    # print(os.getcwd())
    # print(os.listdir(src1))   #check what files are copied
    # print(os.listdir(cwd))   #check what files are copied

    ##########Modify input files##########################
    def update(exams_obj):
       
        file_name = str(os.getcwd())+'/'+inp
        lines = open(file_name, 'r').readlines() 

        # print vars(exams_obj)
        lines[8] = "chem name is " + exams_obj.chem_name + '\n'
        lines[9] = "set mwt(1)= %10.4E"%float(exams_obj.mw) + '\n'
        lines[10] = "set sol(1,1)= %10.4E"%float(exams_obj.sol) + '\n'
        lines[12] = "set Koc(1)= %10.4E"%float(exams_obj.koc) + '\n'
        lines[13] = "set vapr(1)= %10.4E"%float(exams_obj.vp) + '\n'

        if exams_obj.anm > 0:
            exams_obj.kbacs = np.log(2)/(float(exams_obj.anm)*24.0)
        else:
            exams_obj.kbacs=0
        lines[15]="set kbacs(*,1,1)= %10.4E"%(exams_obj.kbacs) + '\n'

        if exams_obj.aem > 0:
            exams_obj.kbacw = np.log(2)/(float(exams_obj.aem)*24.0)
        else:
            exams_obj.kbacw=0
        lines[19]="set kbacw(*,1,1)= %10.4E"%(exams_obj.kbacw) + '\n'

        if exams_obj.aqp > 0:
            exams_obj.kdp = np.log(2)/(float(exams_obj.aqp)*24.0)
        else:
            exams_obj.kdp=0
        lines[22]="set kdp(1,1)= %10.4E"%(exams_obj.kdp) + '\n'

        if exams_obj.farm == "Yes":
            lines[33]="set evap(*,*)=0.0 \n"
            lines[34]="set rain(*)=0.0 \n"
            lines[35]="set npsfl(*,*)=0.0 \n"
            lines[36]="set npsed(*,*)=0.0 \n"
            lines[37]="set stflo(1,*)=0.0 \n"

        hl_out = np.array(exams_obj.hl_out)
        ph_out = np.array(exams_obj.ph_out)
        k_abn =np.array([1, 0, 0])

        def residuals(k_abn, ph_out, tmper, hl_out):
                hr=np.log(2)/(hl_out*24.0)
                ph_adj=6013.79/(tmper+273.15) + 23.6521*np.log10(tmper + 273.15) - 64.7013
                err = peval(k_abn, ph_out, ph_adj) - hr
                return err

        def peval(k_abn, ph_out, ph_adj):
            temp= k_abn[0]*np.power(10,-ph_out) + k_abn[1] + k_abn[2]*np.power(10,(-ph_adj + ph_out))
            return temp

        exams_obj.k_abn = list(leastsq(residuals, k_abn, args=(ph_out, exams_obj.tmper, hl_out), maxfev=200000)[0])
        print exams_obj.k_abn

        if exams_obj.k_abn[0] < 7.9E-5:
            exams_obj.k_abn[0] = 0
        if exams_obj.k_abn[1] < 7.9E-7:
            exams_obj.k_abn[1] = 0
        if exams_obj.k_abn[2] < 7.9E-5:
            exams_obj.k_abn[2] = 0

        lines[23]="set kah(1,1,1)= %10.4E"%(exams_obj.k_abn[0]) + '\n'
        lines[24]="set knh(1,1,1)= %10.4E"%(exams_obj.k_abn[1]) + '\n'
        lines[25]="set kbh(1,1,1)= %10.4E"%(exams_obj.k_abn[2]) + '\n'
        lines[30]="read meteorology %s"%(exams_obj.met) + '\n'

        print vars(exams_obj)
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()            
        return lines

    file_update=update(exams_obj)    
    a=subprocess.Popen("exams.exe exams_inputs.EXA", shell=1)
    a.wait()
    print('done')

    ##########################################################################################
    #####AMAZON KEY, store output files. You might have to write your own import approach#####
    ##########################################################################################
    key = keys_Picloud_S3.amazon_s3_key
    secretkey = keys_Picloud_S3.amazon_s3_secretkey

    ##################################################################################
    ######Zipping output files########################################################
    ##################################################################################
    fname=os.listdir(src1)
    zout=zipfile.ZipFile("exams_all.zip","w")
    for name in fname:
        if name !='exams.exe':
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

    return link

print exams_pi(exams_obj)




