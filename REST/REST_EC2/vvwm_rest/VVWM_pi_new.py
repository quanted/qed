#!/usr/bin/python
#
def VVWM_pi(working_dir,
            koc_check, Koc, soilHalfLifeBox, soilTempBox1, foliarHalfLifeBox,
            wc_hl, w_temp, bm_hl, ben_temp, ap_hl, p_ref, h_hl, mwt, vp, sol, Q10Box,
            convertSoil, convert_Foliar, convertWC, convertBen, convertAP, convertH,
            deg_check, totalApp,
            SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, appNumber_year, app_date_type, DepthIncorp, PestAppyRate, localEff, localSpray,
            scenID,
            buried, D_over_dx, PRBEN, benthic_depth, porosity, bulk_density, FROC2, DOC2, BNMAS,
            DFAC, SUSED, CHL, FROC1, DOC1, PLMAS,
            firstYear, lastyear, vvwmSimType,
            afield, area, depth_0, depth_max,
            ReservoirFlowAvgDays):
    import os
    import stat
    import shutil
    import subprocess
    import zipfile
    # import cloud
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key
    from boto.s3.bucket import Bucket
    import string
    import random
    import sys
    import vvwm_input_generator

    print os.getcwd()
    import keys_Picloud_S3

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
    cwd='/home/ubuntu/Rest_EC2/vvwm_rest/'
    print("cwd="+cwd)

    src=cwd
    src1=cwd+name_temp
    if not os.path.exists(src1):
        os.makedirs(src1)
    else:
        shutil.rmtree(src1)
        os.makedirs(src1)
    ##
    os.chdir(src1)
    # Set working_dir for vvwmTransfer file:
    working_dir = src1

################################################################################
#####Write the vvwmTransfer file################
    vvwm_input_generator.makevvwmTransfer(working_dir,
                                    koc_check, Koc, soilHalfLifeBox, soilTempBox1, foliarHalfLifeBox,
                                    wc_hl, w_temp, bm_hl, ben_temp, ap_hl, p_ref, h_hl, mwt, vp, sol, Q10Box,
                                    convertSoil, convert_Foliar, convertWC, convertBen, convertAP, convertH,
                                    deg_check, totalApp,
                                    SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, appNumber_year, app_date_type, DepthIncorp, PestAppyRate, localEff, localSpray,
                                    scenID,
                                    buried, D_over_dx, PRBEN, benthic_depth, porosity, bulk_density, FROC2, DOC2, BNMAS,
                                    DFAC, SUSED, CHL, FROC1, DOC1, PLMAS,
                                    firstYear, lastyear, vvwmSimType,
                                    afield, area, depth_0, depth_max,
                                    ReservoirFlowAvgDays)



# ########Copy files to the tempt folder#############
    print "++++++++++++++++++++++++++"
    met = "test.dvf"    #This will be changed to allow the user to select a weather file
    if (deg_check == 1):
        przm5_outputChk = "test1"
    elif (deg_check == 2):
        przm5_outputChk = "test2"
    elif (deg_check == 3):
        przm5_outputChk = "test3"
    przm5_output = przm5_outputChk + ".zts"

    shutil.copy(src+"vvwm.exe", src1)
    shutil.copy(src+met,src1)
    shutil.copy(src+przm5_output,src1)
    print(os.getcwd())
    print(os.listdir(src1))   #check what files are copied

    ##call vvwm.exe w/ transfer file
    os.chdir(src1)
    fname_before = os.listdir(src1)
    print 'Before running VVWM', fname_before
    # If EPA Pond & Reservoir is checked, loop through model twice with the two Transfer files:
    if (vvwmSimType == '0'):
        src2=src1+"/vvwm.exe vvwmTransfer.txt"
        a=subprocess.Popen(src2, shell=True)
        print('done 1')
        a.wait()
        os.rename(working_dir+'/vvwmTransfer.txt', working_dir+'/vvwmTransferPond.txt')
        os.rename(working_dir+'/vvwmTransferRes.txt', working_dir+'/vvwmTransfer.txt')
        b=subprocess.Popen(src2, shell=True)
        print('done 2')
        b.wait()
        os.rename(working_dir+'/vvwmTransfer.txt', working_dir+'/vvwmTransferRes.txt')
    else:
        src2=src1+"/vvwm.exe vvwmTransfer.txt"
        a=subprocess.Popen(src2, shell=True)
        print('done')
        a.wait()

    fname=os.listdir(src1)
    print 'After running VVWM', fname
    print "++++++++++++++++++++++++++"
    # Generate Output Variables
    WC_peak = []
    WC_chronic = []
    WC_simavg = []
    WC_4dayavg = []
    WC_21dayavg = []
    WC_60dayavg = []
    WC_90dayavg = []
    Ben_peak = []
    Ben_21dayavg = []
    Ben_convfact = []
    Ben_massfract = []
    EWCH_washout = []
    EWCH_metabolism = []
    EWCH_hydrolysis = []
    EWCH_photolysis = []
    EWCH_volatilization = []
    EWCH_total = []
    EBH_burial = []
    EBH_metabolism = []
    EBH_hydrolysis = []
    EBH_total = []
    RT_runoff = []
    RT_erosion = []
    RT_drift = []
    # Lists to contain graph data
    peak_li1 = []
    ben_peak_li1 = []
    peak_li2 = []
    ben_peak_li2 = []
    # name of output file generated by vvwm
    vvwm_outputFilePond = przm5_outputChk + '_' + scenID + '_Pond_Parent.txt'
    vvwm_outputFileReservoir = przm5_outputChk + '_' + scenID + '_Reservoir_Parent.txt'
    vvwm_outputFileCustom = przm5_outputChk + '_' + scenID + '_Custom_Parent.txt'
    
    # Read output file(s):
    NumOfOutputFiles = 1
    if vvwmSimType == '5':
        vvwm_outputTxt = vvwm_outputFilePond
    elif vvwmSimType == "4":
        vvwm_outputTxt = vvwm_outputFileReservoir
    elif vvwmSimType == "1" or vvwmSimType == "2" or vvwmSimType == "3":
        vvwm_outputTxt = vvwm_outputFileCustom
    elif vvwmSimType == "0":
        vvwm_outputTxt = vvwm_outputFilePond
        NumOfOutputFiles = 2
    x = 0
    while (x < NumOfOutputFiles):
        years = 0
        if x == 1:
            vvwm_outputTxt = vvwm_outputFileReservoir
        with open(vvwm_outputTxt, 'r') as f:
            for line in f:
                line = line.split()
                if (line):
                    if "Inputs" in line:
                        break
                    else:
                        if "=" in line:
                            # Make desired value be index=1 for each line:
                            equalsSignIndex = line.index("=")
                            del line[equalsSignIndex+2:len(line)]
                            s = " ".join(line)
                            li = s.split(" = ", 1)
                            # Assign desired value to variable:
                            if 'Peak 1-in-10' in li:
                                WC_peak.append(float(li[1]))
                            if 'Chronic 1-in-10' in li:
                                WC_chronic.append(float(li[1]))
                            if 'Simulation Avg' in li:
                                WC_simavg.append(float(li[1]))
                            if '4-day avg 1-in-10' in li:
                                WC_4dayavg.append(float(li[1]))
                            if '21-day avg 1-in-10' in li:
                                WC_21dayavg.append(float(li[1]))
                            if '60-day avg 1-in-10' in li:
                                WC_60dayavg.append(float(li[1]))
                            if '90-day avg 1-in-10' in li:
                                WC_90dayavg.append(float(li[1]))
                            if 'Benthic Pore Water Peak 1-in-10' in li:
                                Ben_peak.append(float(li[1]))
                            if 'Benthic Pore Water 21-day avg 1-in-10' in li:
                                Ben_21dayavg.append(float(li[1]))
                            if 'Benthic Conversion Factor' in li:
                                Ben_convfact.append(float(li[1]))
                            if 'Benthic Mass Fraction in Pore Water' in li:
                                Ben_massfract.append(float(li[1]))
                            if 'washout halflife (days)' in li:
                                EWCH_washout.append(float(li[1]))
                            if 'water col metab halflife (days)' in li:
                                EWCH_metabolism.append(float(li[1]))
                            if 'hydrolysis halflife (days)' in li:
                                EWCH_hydrolysis.append(float(li[1]))
                            if 'photolysis halflife (days)' in li:
                                EWCH_photolysis.append(float(li[1]))
                            if 'volatile halflife (days)' in li:
                                EWCH_volatilization.append(float(li[1]))
                            if 'total water col halflife (days)' in li:
                                EWCH_total.append(float(li[1]))
                            if 'burial halflife (days)' in li:
                                EBH_burial.append(float(li[1]))
                            if 'benthic metab halflife (days)' in li:
                                EBH_metabolism.append(float(li[1]))
                            if 'benthic hydrolysis halflife (days)' in li:
                                EBH_hydrolysis.append(float(li[1]))
                            if 'total benthic halflife (days)' in li:
                                EBH_total.append(float(li[1]))
                            if 'Due to Runoff' in li:
                                RT_runoff.append(float(li[1]))
                            if 'Due to Erosion' in li:
                                RT_erosion.append(float(li[1]))
                            if 'Due to Drift' in li:
                                RT_drift.append(float(li[1]))
                        if "zero" in line:
                            li = " ".join(line)
                            if 'washout' in li:
                                EWCH_washout.append(0)
                            if 'zero hydrolysis' in li:
                                EWCH_hydrolysis.append(0)
                            if 'zero burial' in li:
                                EBH_burial.append(0)
                            if 'zero benthic hydrolysis' in li:
                                EBH_hydrolysis.append(0)
                        # Choose which list to append to:
                        if x == 0:
                            # Append Peak and Benthic Peak to lists for graphs:
                            if (years == 1):
                                if (len(line) == 1):
                                    years = 0
                                else:
                                    peak_li1.append(float(line[1]))
                                    ben_peak_li1.append(float(line[7]))
                            if (line[0] == 'YEAR'):
                                # Set years flag to begin list appending above
                                years = 1
                        else:
                            # Append Peak and Benthic Peak to lists for graphs:
                            if (years == 1):
                                if (len(line) == 1):
                                    years = 0
                                else:
                                    peak_li2.append(float(line[1]))
                                    ben_peak_li2.append(float(line[7]))
                            if (line[0] == 'YEAR'):
                                # Set years flag to begin list appending above
                                years = 1
        x = x + 1

    #zip all the file
    zout=zipfile.ZipFile("test.zip","w", zipfile.ZIP_DEFLATED)
    for name in fname:
        if name !='vvwm.exe' and name !='test.dvf' and name != przm5_output:
            zout.write(name)
    zout.close()

    name1='VVWM_'+name_temp+'.zip'
    link='https://s3.amazonaws.com/vvwm/'+name1
    # print link

    return link, WC_peak, WC_chronic, WC_simavg, WC_4dayavg, WC_21dayavg, WC_60dayavg, WC_90dayavg, Ben_peak, Ben_21dayavg, Ben_convfact, Ben_massfract, EWCH_washout, EWCH_metabolism, EWCH_hydrolysis, EWCH_photolysis, EWCH_volatilization, EWCH_total, EBH_burial, EBH_metabolism, EBH_hydrolysis, EBH_total, RT_runoff, RT_erosion, RT_drift, peak_li1, ben_peak_li1, peak_li2, ben_peak_li2, src1, name1