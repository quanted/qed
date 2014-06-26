#!/usr/bin/python
def PRZM_pi(noa, met, inp, run, MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft):
    import os
    import stat
    import shutil
    import subprocess
    import zipfile
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key
    from boto.s3.bucket import Bucket
    import string
    import random
    import sys
    import keys_Picloud_S3

    # print 'MM=', MM
    # print 'DD=', DD
    # print 'CAM_f=', CAM_f
    # print 'DEPI_text=', DEPI_text
    # print 'Ar_text=', Ar_text
    # print 'EFF=', EFF
    # print 'Drft=', Drft    
                
    # Generate a random ID for file save
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
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
    cwd='/home/ubuntu/Rest_EC2/przm_rest'
    # cwd='D:/Dropbox/ubertool_src/REST/REST_local/przm_rest/'
    # print("cwd="+cwd)

    src=cwd
    src1=cwd + '/' + name_temp
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
    # print(run)
    # print(met)
    # print(inp)
    przm_exe = "przm3123-3.exe"
########Copy files to the tempt folder#############
    shutil.copy(src+"/inpsrc1/"+run,src1)
    shutil.copy(src+"/inpsrc1/"+inp,src1)
    shutil.copy(src+"/"+przm_exe,src1)
    #met=string.capitalize(met)
#    print(met)
#    met=met.upper()
#    print(met)
    shutil.copy(src+"/inpsrc1/"+met,src1)
    # print(os.getcwd())
    # print(os.listdir(src1))   #check what files are copied

    
    src2=src1+"/"+przm_exe
    
    ##call the PRZM file
    os.chdir(src1)
    #print(os.listdir(src1))
    #text replacement
    def copy_line(file_name, noa, line_s, line_e):
        line = open(file_name, 'r')
        lines = line.readlines()
        line.close()
        
        old_row=len(lines)
        new_row=old_row+(line_e-line_s)*(noa-1)
        
        insert=lines[line_s:line_e]
        insert_1= ''.join(insert)
        new_lines= ['None'] *new_row
        new_lines[0:line_s]=lines[0:line_s]
        
        jj=0
        
        while jj<(line_e-line_s):   #jj indexes rows to be inserted
            j=line_s+(jj)*(noa)
            l=0
            for i in range(noa):
                l=j+i
                new_lines[l]=insert[jj]
            jj=jj+1
        new_lines[l+1:new_row+1]=lines[line_e:]
        out = open(file_name, 'w')
        out.writelines(new_lines)
        out.close()
                
    def replace_line(file_name, line_num, col_s, col_e, text):
        
        lines = open(file_name, 'r').readlines()
        temp=lines[line_num]
        temp = temp.replace(temp[col_s:col_e],text)
        lines[line_num]=temp
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()
    
    
    def del_line(file_name, line_s, line_e):
        line = open(file_name, 'r')
        lines = line.readlines()
        line.close()
        del lines[line_s:line_e]
        
        fout= open(file_name, 'w')
        fout.writelines(lines) 
        fout.close() 

    if inp == "NC1App-P.INP":
        noa_new = 26
        row_num1 = 87 - 4
        row_num2 = 129 - 8
        row_num3 = 132 - 8
        row_num4 = 95 - 4
        row_num5 = 125 - 8
    elif inp == "ND1Cno-P.INP":
        noa_new = 28
        row_num1 = 87 - 2
        row_num2 = 129 - 4
        row_num3 = 132 - 4
        row_num4 = 95 - 2
        row_num5 = 125 - 4
    else:
        noa_new = 30
        row_num1 = 87
        row_num2 = 129
        row_num3 = 132
        row_num4 = 95
        row_num5 = 125

    new3=noa*noa_new
    
    if new3>100:
        replace_line(src1+'/'+inp, row_num1, 5,8, str(new3))
    else:
        replace_line(src1+'/'+inp, row_num1, 6,8, str(new3))
        
    index_del=0
    for l in CAM_f:
        if l=='1' or l=='4' or l=='5' or l=='6' or l=='7' or l=='8':
            index_del=index_del+1
        else:
            index_del=index_del
    
    if index_del>0:
        del_line(src1+'/'+inp, row_num2, row_num3)
    
    copy_line(src1+'/'+inp, noa, row_num4, row_num5)
    
    new=[]
    new1=[]
    j=range(row_num4, row_num4+noa_new*noa)
    
    for i in range(noa):
        new="  "+DD[i]+MM[i]
        new1='0 '+CAM_f[i]+" "+DEPI_text[i]+Ar_text[i]+EFF[i]+Drft[i]+'\r\n'
        # print 'new=', new
        # print 'new1=', new1

        rep=j[i::noa]
        for k in rep:
            replace_line(src1+'/'+inp, k, 0,6, new)
            replace_line(src1+'/'+inp, k, 10,100, new1)
#        YY=YY+1
    lines_test = open(src1+'/'+inp, 'r').readlines()

    # print '95='+lines_test[95]
    # print '96='+lines_test[96]
    # print '97='+lines_test[97]
    # print '98='+lines_test[98]    
    # print '128='+lines_test[128]
    # print '129='+lines_test[129]   
    # print '130='+lines_test[130]        
    os.rename(src1+'/'+run,'PRZM3.RUN')
#    os.rename(src1+'/'+run,run.upper())
#    os.rename(src1+'/'+met,met.upper())
    os.rename(src1+'/'+inp,inp.upper())
#    print(run)
#    print(met)
#    print(inp)    
#    print(os.listdir(src1)) 
    fname_before = os.listdir(src1)
    # print 'Before running PRZM', fname_before

    a=subprocess.Popen(src2, shell=0, stdout=open(os.devnull, 'wb')) #quite version
    # print('done')
    a.wait()
    #os.remove(src+"/PRZM3.RUN")
    #os.remove(src+"/MS1CTT-R.INP")
    #os.remove(src+"/przm3123-1.exe")
    #os.remove(src+"/W03940.DVF")
    fname=os.listdir(src1)
    # print fname
    
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

    # print x_precip
    # print x_runoff
    # print x_et
    # print x_irr
    # print x_leachate
    zout=zipfile.ZipFile("test.zip","w", zipfile.ZIP_DEFLATED)
    ##zip all the file
    for name in fname:
        if name !=przm_exe:
            zout.write(name)
    zout.close()
    #save the zipfile to amazon server
    conn = S3Connection(key, secretkey)
    bucket = Bucket(conn, 'przm')
    k=Key(bucket)
    # print "start upload"
    name1='PRZM_'+name_temp+'.zip'
    k.key=name1
    k.set_contents_from_filename('test.zip')
    # print "done upload"
    link='https://s3.amazonaws.com/przm/'+name1
    k.set_acl('public-read-write')
    src1_up=os.path.abspath(os.path.join(src1, '..'))
    os.chdir(src1_up)
    shutil.rmtree(src1)
    # print('Done')

    return link, x_precip, x_runoff, x_et, x_irr, x_leachate

