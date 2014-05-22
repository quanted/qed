# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 23:18:30 2012

@author: tao
"""
import os
import stat
import shutil
import subprocess
import zipfile
#import send_email
##
cwd=os.getcwd()
src=cwd
src1=cwd+"/trial1"

if not os.path.exists(src1):
    os.makedirs(src1)
else:
    shutil.rmtree(src1)
    os.makedirs(src1)
##
os.chdir(src1)
shutil.copy(src+"/PRZM3.RUN",src1)
shutil.copy(src+"/MS1CTT-R.INP",src1)
shutil.copy(src+"/przm3123-3.exe",src1)
shutil.copy(src+"/W03940.DVF",src1)
src2=src1+"/przm3123-3.exe"
##
a=subprocess.Popen(src2, shell=0)
a.wait()
##
#msg='Run on Picloud x64 local, shell=0'
###
#os.remove(src1+"/PRZM3.RUN")
#os.remove(src1+"/MS1CTT-R.INP")
#os.remove(src1+"/przm3123-1.exe")
#os.remove(src1+"/W03940.DVF")
###
#fname=os.listdir(src1)
#zout=zipfile.ZipFile("test.zip","w")
###
###zip all the file
#for name in fname:
#    zout.write(name)
#zout.close()
###
###send email with attachment
#to='hongtao510@gmail.com'
#filename=src1+"/test.zip"
#send_email.sendemail(to,filename,msg)
####
#os.chdir(src)
#shutil.rmtree(src1)
##
print('Done')

