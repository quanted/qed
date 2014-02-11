#!/usr/bin/python
#
def PRZM_pi(met, inp, run):
    import os
    import stat
    import shutil
    import subprocess
    import zipfile
    import send_email
    import cloud
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

    cwd=os.getcwd()+'/PRZM_lin_test'
    print("cwd="+cwd)
#    if isinstance(cwd, unicode):
#        print "cwd unicode"
#    src=cwd+'/inpsrc'
    src=cwd
    
    src1=cwd+'/'+name_temp
    
    if not os.path.exists(src1):
        os.makedirs(src1)
    else:
        shutil.rmtree(src1)
        os.makedirs(src1)
    ##
    os.chdir(src1)
    inp = inp.encode('ascii','ignore')
    met = met.encode('ascii','ignore')
    run = run.encode('ascii','ignore')

#    test = src+"/"+inp
#    if isinstance(test, unicode):
#        print test
#    else:
#        print "OK"
        
#    shutil.copy(unicode.decode(test),src1)
#    shutil.copy(os.path.join(src,"/",inp),src1)
    
    print(os.listdir(src+"/inpsrc"))   

    shutil.copy(src+"/inpsrc/"+run,src1)

    shutil.copy(src+"/przm3123-3.exe",src1)
    #met=string.capitalize(met)
#    print(met)
#    met=met.upper()
#    print(met)
    shutil.copy(src+"/inpsrc/"+met,src1)
    src2=src1+"/przm3123-3.exe"
    
    ##call the PRZM file
    os.chdir(src1)
    print(os.listdir(src1))
    os.rename(src1+'/'+run,'PRZM3.RUN')
    a=subprocess.Popen(src2, shell=0)
    print('done')
    a.wait()

    #os.remove(src+"/PRZM3.RUN")
    #os.remove(src+"/MS1CTT-R.INP")
    #os.remove(src+"/przm3123-1.exe")
    #os.remove(src+"/W03940.DVF")
    ##
    fname=os.listdir(src1)
    zout=zipfile.ZipFile("test.zip","w")
    ##
    ##zip all the file
    for name in fname:
        if name !='przm3123-3.exe':
            zout.write(name)
    zout.close()
    
    ##
    ##send email with attachment
    #to='purucker.tom@gmail.com, hongtao510@gmail.com' #, 
    #filename=src1+"/test.zip"

    ###
    #save the zipfile to amazon server
    conn = S3Connection(key, secretkey)
#    bucket = conn.create_bucket('przm1')
    bucket = Bucket(conn, 'przm')
    k=Key(bucket)



    name1='PRZM_'+name_temp+'.zip'
    k.key=name1
    k.set_contents_from_filename('test.zip')
    link='https://s3.amazonaws.com/przm/'+name1
    k.set_acl('public-read-write')

    ##
    #msg='Run on Picloud x64, shell=0'+link
    #send_email.sendemail(to,filename,msg)

    os.chdir(src)
    #shutil.rmtree(src1)

    ##
    #print('Done')

    return(link)

