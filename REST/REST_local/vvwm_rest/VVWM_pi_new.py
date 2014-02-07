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
    cwd = 'C:/Users/Jon/Documents/GitHub/ubertool_src/REST/REST_local/vvwm_rest/'
    # cwd='/home/picloud/vvwm/'
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
    met = "test.dvf"
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

    src2="vvwm.exe vvwmTransfer.txt"

    ##call vvwm.exe w/ transfer file
    os.chdir(src1)
    fname_before = os.listdir(src1)
    print 'Before running VVWM', fname_before

    a=subprocess.Popen(src2, shell=0)
    print('done')
    a.wait()

    fname=os.listdir(src1)
    print 'After running VVWM', fname
    print "++++++++++++++++++++++++++"
    
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
    EWCH_washout = [0]
    EWCH_metabolism = []
    EWCH_hydrolysis = [0]
    EWCH_photolysis = []
    EWCH_volatilization = []
    EWCH_total = []
    EBH_burial = [0]
    EBH_metabolism = []
    EBH_hydrolysis = [0]
    EBH_total = []
    RT_runoff = []
    RT_erosion = []
    RT_drift = []

    peak_li = []
    ben_peak_li = []

    years = 0

    print vvwmSimType
    # if (vvwmSimType == "0" or  vvwmSimType == "5"):
    #     vvwmSimType = "2"
    # elif (vvwmSimType == "4" or vvwmSimType == "6"):
    #     vvwmSimType = "3"
    # elif (vvwmSimType == "1" or vvwmSimType == "2" or vvwmSimType == "3"):
    #     vvwmSimType = "1"

    vvwm_outputFilePond = przm5_outputChk + '_' + scenID + '_Pond_Parent.txt'
    vvwm_outputFileReservoir = 'test_'+scenID+'_Reservoir_Parent.txt'
    with open(vvwm_outputFilePond, 'r') as f:
        for line in f:
            line = line.split()
            if (line):
                if "******* Inputs *******" in line:
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
                        if 'water col metab halflife (days)' in li:
                            EWCH_metabolism.append(float(li[1]))
                        if 'photolysis halflife (days)' in li:
                            EWCH_photolysis.append(float(li[1]))
                        if 'volatile halflife (days)' in li:
                            EWCH_volatilization.append(float(li[1]))
                        if 'total water col halflife (days)' in li:
                            EWCH_total.append(float(li[1]))
                        if 'benthic metab halflife (days)' in li:
                            EBH_metabolism.append(float(li[1]))
                        if 'total benthic halflife (days)' in li:
                            EBH_total.append(float(li[1]))
                        if 'Due to Runoff' in li:
                            RT_runoff.append(float(li[1]))
                        if 'Due to Erosion' in li:
                            RT_erosion.append(float(li[1]))
                        if 'Due to Drift' in li:
                            RT_drift.append(float(li[1]))
                        
                        # Deal with "ZERO" blah blah blahs in output file (list[0] = blah)      <-- They don't have "="
                    if (years == 1):
                        # Append Peak and Benthic Peak to lists
                        if (len(line) == 1):
                            years = 0
                        else:
                            peak_li.append(float(line[1]))
                            ben_peak_li.append(float(line[7]))
                    if (line[0] == 'YEAR'):
                        # Set years flag to begin list appending above
                        years = 1


    #zip all the file
    zout=zipfile.ZipFile("test.zip","w", zipfile.ZIP_DEFLATED)
    for name in fname:
        if name !='vvwm.exe' and name !='test.dvf' and name != przm5_output:
            zout.write(name)
    zout.close()

    name1='VVWM_'+name_temp+'.zip'
    link='https://s3.amazonaws.com/vvwm/'+name1
    # print link

    return link, WC_peak, WC_chronic, WC_simavg, WC_4dayavg, WC_21dayavg, WC_60dayavg, WC_90dayavg, Ben_peak, Ben_21dayavg, Ben_convfact, Ben_massfract, EWCH_washout, EWCH_metabolism, EWCH_hydrolysis, EWCH_photolysis, EWCH_volatilization, EWCH_total, EBH_burial, EBH_metabolism, EBH_hydrolysis, EBH_total, RT_runoff, RT_erosion, RT_drift, peak_li, ben_peak_li, src1, name1