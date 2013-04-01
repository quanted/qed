#!/usr/bin/python
met="wTest.dvf"
run="run_pfam.bat"
inp="pfam_input.PFA"
import os
import stat
import shutil
import subprocess
import zipfile
#import cloud
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucket import Bucket
import string
import random
# Generate a random ID for file save
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
name_temp=id_generator()
#AMAZON KEY
key='AKIAIUYH5XORGJCNDZOQ'
secretkey='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'   
cwd=os.getcwd()
src=cwd
src1=cwd+'/'+name_temp
if not os.path.exists(src1):
    os.makedirs(src1)
else:
    shutil.rmtree(src1)
    os.makedirs(src1)
##
shutil.copy(src+"/"+run,src1)
shutil.copy(src+"/"+met,src1)
shutil.copy(cwd+"/pfam_pi.exe",src1)
shutil.copy(src+"/"+inp,src1)
#
src2=src1+"/run_pfam.bat"
os.chdir(src1)
a=subprocess.Popen(src2, shell=1)
#a=subprocess.Popen(['./run_pfam.bat', 'src1'], shell=1)
#a=subprocess.Popen(['./pfam_pi.exe', 'inp', 'src1'], shell=0)
#
#
a.wait()
#
fname=os.listdir(src1)
zout=zipfile.ZipFile("test.zip","w")
#
##zip all the file
for name in fname:
    if name !='pfam_pi.exe' and name !='run_pfam.bat':
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

print link













#os.remove(src+"/PRZM3.RUN")
