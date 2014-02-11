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

# przm_exe = "przm3123_win.exe"
przm_exe = "przm3123-3.exe"

RUN_file = "NC1App-P.RUN"
INP_file = "NC1App-P.INP"
DVF_file = "W03812.DVF"

os.chdir(src1)

shutil.copy(src+"/"+RUN_file,src1)
shutil.copy(src+"/"+INP_file,src1)
shutil.copy(src+"/"+przm_exe,src1)
shutil.copy(src+"/"+DVF_file,src1)
src2=src1+"/"+przm_exe

os.rename(src1+'/'+RUN_file,'PRZM3.RUN')
os.rename(src1+'/'+INP_file, INP_file.upper())
fname=os.listdir(src1)
print 'Before running PRZM', fname


##
a=subprocess.Popen(src2, shell=0)
a.wait()
x_precip=[]
x_et=[]
x_runoff=[]
x_irr=[]
x_leachate=[]

for line in file('CPRZM31.hyd'):
    line = line.split()
    x_precip_temp = line[0]
    x_precip.append(x_precip_temp)
    
    x_runoff_temp = line[1]
    x_runoff.append(x_runoff_temp)        
    
    x_et_temp = line[2]
    x_et.append(x_et_temp)    

    x_irr_temp = line[5]
    x_irr.append(x_irr_temp) 
            
for line in file('CPRZM31.cnc'):
    line = line.split()
    x_leachate_temp = line[2]
    x_leachate.append(x_leachate_temp)

    
print x_precip
print x_runoff
print x_et
print x_irr

print x_leachate


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

