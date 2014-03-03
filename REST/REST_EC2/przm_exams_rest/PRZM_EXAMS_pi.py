#!/usr/bin/python
#
def PRZM_EXAMS_pi(chem_name, noa, scenarios, unit, met, inp, run, exam, MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft, 
                  farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out):

    import os
    import stat
    import shutil
    import glob
    import subprocess
    import zipfile
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key
    from boto.s3.bucket import Bucket
    import string
    import random
    import keys_Picloud_S3
##########################################################################################
#####AMAZON KEY, store output files. You might have to write your own import approach#####
##########################################################################################
    key = keys_Picloud_S3.amazon_s3_key
    secretkey = keys_Picloud_S3.amazon_s3_secretkey
##### Generate a folder with random name to store files
    def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))
    name_temp=id_generator()

##################################################################################
######Create a folder if it does not existed, where holds calculations' output.###
##################################################################################
    cwd='/home/ubuntu/Rest_EC2/przm_exams_rest'
    # print("cwd1="+cwd)

    src=cwd
    src1=cwd+'/'+name_temp
    if not os.path.exists(src1):
        os.makedirs(src1)
    else:
        shutil.rmtree(src1)
        os.makedirs(src1)
    ##
    os.chdir(src1)

    # inp = inp.encode('ascii','ignore')
    # met = met.encode('ascii','ignore')
    # run = run.encode('ascii','ignore')
    # print(run)
    # print(met)
    # print(inp)

########Copy common files########~#############
    shutil.copy(src+"/inpsrc1/"+met, src1)
    # shutil.copy(src+"/GO_lin.BAT", src1)
########PRZM files#############################
    shutil.copy(src+"/inpsrc1/"+run, src1)
    shutil.copy(src+"/inpsrc1/"+inp, src1)
    shutil.copy(src+"/przm3123_lin.exe", src1)
########EXAMS files############################
    shutil.copy(src+"/inpsrc1/"+exam, src1)
    shutil.copy(src+"/exams_lin.exe", src1)
    shutil.copy(src+"/POND298.EXV", src1)
    shutil.copy(src+"/exams.daf",src1)
    shutil.copy(src+"/OZONE.DAF",src1)


    # print(os.getcwd())
    # print('files_included=', os.listdir(src1))   #check what files are copied

#######################################################
#######Modify the GO.BAT file##########################
#######################################################

    # def update_go(run, exam):
    #     file_name = str(os.getcwd())+'/GO_lin.BAT'
    #     lines = open(file_name, 'r').readlines() 

    #     scenario_name = run.split(".")[0]
    #     scenario_name_new = "C"+scenario_name[0:-2]+"P1"
    #     lines[0] = "cp " + run + " PRZM3.RUN" + '\n'
    #     lines[2] = "./exams_lin.exe " + exam + " " + scenario_name + ".PEX " + scenario_name + ".ERR " + scenario_name + ".WRN " + '\n'
    #     lines[3] = "cp report.xms " + scenario_name + ".XMS" + '\n'
    #     lines[4] = "cp ecoriskc.xms " + scenario_name + ".YMS" + '\n'
    #     lines[5] = "cp ecotoxc.xms " + scenario_name + ".ZMS" + '\n'
    #     lines[6] = "cp cprzm31.hyd " + scenario_name_new + ".HYD" + '\n'
    #     lines[7] = "cp cprzm31.cnc " + scenario_name_new + ".CNC" + '\n'
    #     lines[8] = "cp cprzm31.msb " + scenario_name_new + ".MSB" + '\n'

    #     out = open(file_name, 'w')
    #     out.writelines(lines)
    #     out.close()            
    #     return lines

    # os.chdir(src1)
    # go_update=update_go(run, exam)
    # print('GO_lin.BAT is modified')

##########################################################
#######Modify the PRZM input file##########################
##########################################################

    def PRZM_pi(noa, met, inp, run, MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft):
        # print 'MM=', MM
        # print 'DD=', DD
        # print 'CAM_f=', CAM_f
        # print 'DEPI_text=', DEPI_text
        # print 'Ar_text=', Ar_text
        # print 'EFF=', EFF
        # print 'Drft=', Drft    
    #############text replacement#############################
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

        new3=noa*30
        
        if new3>100:
            replace_line(src1+'/'+inp, 87, 5,8, str(new3))
        else:
            replace_line(src1+'/'+inp, 87, 6,8, str(new3))
            
        index_del=0
        for l in CAM_f:
            if l=='1' or l=='4' or l=='5' or l=='6' or l=='7' or l=='8':
                index_del=index_del+1
            else:
                index_del=index_del
        
        if index_del>0:
            del_line(src1+'/'+inp, 129,132)
        
        copy_line(src1+'/'+inp, noa, 95, 125)
        
        new=[]
        new1=[]
        j=range(95, 95+30*noa)
        
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
    ########upper case file name######################
        os.rename(src1+'/'+inp, inp.upper())
        # print inp.upper()
        # print('PRZM input updated')

    PRZM_update = PRZM_pi(noa, met, inp, run, MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft)


##########################################################
#######Modify the PRZM input file##########################
##########################################################
    def EXAMS_pi(exam, chem_name, scenarios, met, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out):
        
        import numpy as np
        from scipy.optimize import leastsq

        file_name = str(os.getcwd())+'/'+exam
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

        if farm == "No":
            # lines[33]="set evap(*,*)=0.0 \n"
            # lines[34]="set rain(*)=0.0 \n"
            # lines[35]="set npsfl(*,*)=0.0 \n"
            # lines[36]="set npsed(*,*)=0.0 \n"
            # lines[37]="set stflo(1,*)=0.0 \n"
            str_pond_1 = "set evap(*,*)=0.0"
            str_pond_2 = "set rain(*)=0.0"
            str_pond_3 = "set npsfl(*,*)=0.0"
            str_pond_4 = "set npsed(*,*)=0.0"
            str_pond_5 = "set stflo(1,*)=0.0"

            for i, line in enumerate(lines):
                if str_pond_1 in line:
                    lines[i-2] = "read przm " + lines[i-2].split(" ")[2].upper()
                    lines[i] = "!"+str_pond_1+'\n'
                if str_pond_2 in line:
                    lines[i] = "!"+str_pond_2+'\n'
                if str_pond_3 in line:
                    lines[i] = "!"+str_pond_3+'\n'
                if str_pond_4 in line:
                    lines[i] = "!"+str_pond_4+'\n'
                if str_pond_5 in line:
                    lines[i] = "!"+str_pond_5+'\n'
                # print i, line

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
    # print('EXAMS input updated')

    file_update=EXAMS_pi(exam, chem_name, scenarios, met, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out)    

#############RUN PRZM-EXAM#####################################
    os.chdir(src1)
    os.rename(src1+'/'+run,'PRZM3.RUN')
    src2=src1+"/przm3123_lin.exe"
    run_przm=subprocess.Popen(src2, shell=1)
    while (run_przm.poll() != 0):
        run_przm.wait()
    # print('PRZM run finished')

    os.chdir(src1)
    # print os.listdir(src1)
    scenario_name = run.split(".")[0]
    command_exams = "./exams_lin.exe " + exam + " " + scenario_name + ".PEX " + scenario_name + ".ERR " + scenario_name + ".WRN "
    run_exams=subprocess.Popen(command_exams, shell=1)
    while (run_exams.poll() != 0):
        run_exams.wait()
    # print('EXAMS run finished')

    # run_prog=subprocess.Popen("./GO_lin.BAT", shell=1)
    # run_prog.wait()
    # print('PRZM-EXAMS run finished!')

############Post Process###########################
    fname=os.listdir(src1)
    # print 'After Simulation=', fname
    
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

    # print "x_precip=", x_precip
    # print "x_runoff=", x_runoff
    # print "x_et=", x_et
    # print "x_irr=", x_irr
    # print "x_leachate=", x_leachate

    Lim_inst=[]
    Lim_24h=[]
    Lim_96h=[]
    Lim_21d=[]
    Lim_60d=[]
    Lim_90d=[]
    Lim_y=[]

    Ben_inst=[]
    Ben_24h=[]
    Ben_96h=[]
    Ben_21d=[]
    Ben_60d=[]
    Ben_90d=[]
    Ben_y=[]

    for i, line in enumerate(file('EcoRiskC.xms')):
        if i>54:
            line = line.split()
            Lim_inst_temp = line[1]
            Lim_inst.append(Lim_inst_temp)
            Lim_24h_temp = line[5]
            Lim_24h.append(Lim_24h_temp)
            Lim_96h_temp = line[9]
            Lim_96h.append(Lim_96h_temp)
            Lim_21d_temp = line[13]
            Lim_21d.append(Lim_21d_temp)
            Lim_60d_temp = line[17]
            Lim_60d.append(Lim_60d_temp)
            Lim_90d_temp = line[21]
            Lim_90d.append(Lim_90d_temp)
            Lim_y_temp = line[25]
            Lim_y.append(Lim_y_temp)

            Ben_inst_temp = line[3]
            Ben_inst.append(Ben_inst_temp)
            Ben_24h_temp = line[7]
            Ben_24h.append(Ben_24h_temp)
            Ben_96h_temp = line[11]
            Ben_96h.append(Ben_96h_temp)
            Ben_21d_temp = line[15]
            Ben_21d.append(Ben_21d_temp)
            Ben_60d_temp = line[19]
            Ben_60d.append(Ben_60d_temp)
            Ben_90d_temp = line[23]
            Ben_90d.append(Ben_90d_temp)
            Ben_y_temp = line[27]
            Ben_y.append(Ben_y_temp)

    # print 'Lim_inst=', Lim_inst
    # print 'Lim_24h=', Lim_24h
    # print 'Lim_96h=', Lim_96h
    # print 'Lim_21d=', Lim_21d
    # print 'Lim_60d=', Lim_60d
    # print 'Lim_90d=', Lim_90d
    # print 'Lim_y=', Lim_y

    ##############Rename files#########################
    os.chdir(src1)
    os.rename(src1+'/report.xms', scenario_name+'.XMS')
    os.rename(src1+'/EcoRiskC.xms', scenario_name+'.YMS')
    os.rename(src1+'/EcoToxC.xms', scenario_name+'.ZMS')
    os.rename(src1+'/CPRZM31.hyd', scenario_name+'.HYD')
    os.rename(src1+'/CPRZM31.cnc', scenario_name+'.CNC')
    os.rename(src1+'/CPRZM31.msb', scenario_name+'.MSB')

    # print 'After file renaming=', os.listdir(src1)

########################################################
###########Save file to AMAZON S3#######################
########################################################
    P2E_list=glob.glob('P2E*.*')
    PRN_list=glob.glob('*.PRN')
    PRZ_list=glob.glob('*.PRZ')
    ZTS_list=glob.glob('*.ZTS')
    MSB_list=glob.glob('*.msb')
    PLT_list=glob.glob('*.PLT')
    DVF_list=glob.glob('*.DVF')

    file_exclud=P2E_list+PRN_list+PRZ_list+ZTS_list+MSB_list+PLT_list+DVF_list+['przm3123_lin.exe', 'przm3123_win.exe', 'exams_lin.exe', 'exams_win.exe', 'exams.daf', 'OZONE.DAF', 'POND298.EXV']
    all_list=os.listdir(src1)
    final_list=list(set(all_list) - set(file_exclud))

    zout=zipfile.ZipFile("PRZM_EXAMS.zip","w", zipfile.ZIP_DEFLATED)
    for name in final_list:
        zout.write(name)
    zout.close()

    #save the zipfile to amazon server
    conn = S3Connection(key, secretkey)
    bucket = Bucket(conn, 'przm_exams')
    k=Key(bucket)

    name1='PRZM_EXAMS_'+name_temp+'.zip'
    k.key=name1
    k.set_contents_from_filename('PRZM_EXAMS.zip')
    link='https://s3.amazonaws.com/przm_exams/'+name1
    k.set_acl('public-read-write')
    os.chdir(src)
    shutil.rmtree(src1)
    # print link
    return link, x_precip, x_runoff, x_et, x_irr, x_leachate, Lim_inst, Lim_24h, Lim_96h, Lim_21d, Lim_60d, Lim_90d, Lim_y,  Ben_inst, Ben_24h, Ben_96h, Ben_21d, Ben_60d, Ben_90d, Ben_y

