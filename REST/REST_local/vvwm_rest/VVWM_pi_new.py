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
        przm5_output = "test1.zts"
    elif (deg_check == 2):
        przm5_output = "test2.zts"
    elif (deg_check == 3):
        przm5_output = "test3.zts"

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
    


    ##zip all the file
    # zout=zipfile.ZipFile("test.zip","w")
    # for name in fname:
    #     if name !='przm5.exe' and name !='test.dvf':
    #         zout.write(name)
    # zout.close()

    ##upload file to S3
    # conn = S3Connection(key, secretkey)
    # bucket = Bucket(conn, 'przm5')
    # k=Key(bucket)

    # name1='PRZM5_'+name_temp+'.zip'
    # k.key=name1
    # link='https://s3.amazonaws.com/przm5/'+name1
    # print link

    # return link, PRCP_IRRG_sum, RUNF_sum, CEVP_TETD_sum, src1, name1

    return src1

    # k.set_contents_from_filename('test.zip')

    # k.set_acl('public-read-write')
    # print 'upload finished'
    # os.chdir(src)

    # return link, PRCP_IRRG_sum, RUNF_sum, CEVP_TETD_sum

    # return 'done'
