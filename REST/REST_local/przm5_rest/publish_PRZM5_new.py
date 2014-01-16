import cloud
import sys 
import os
lib_path = os.path.abspath('../../..')
sys.path.append(lib_path)
from ubertool_src import keys_Picloud_S3

cloud.setkey(keys_Picloud_S3.picloud_api_key, keys_Picloud_S3.picloud_api_secretkey)

def PRZM5(input_list): 
    import os, sys
    lib_path = os.path.abspath('/home/picloud/PRZM5')
    sys.path.append(lib_path)
    import PRZM5_pi_new


    pfac = input_list[0]
    snowmelt = input_list[1]
    evapDepth = input_list[2]
    uslek = input_list[3]
    uslels = input_list[4]
    uslep = input_list[5]
    fieldSize = input_list[6]
    ireg = input_list[7]
    slope = input_list[8]
    hydlength = input_list[9]
    canopyHoldup = input_list[10]
    rootDepth = input_list[11]
    canopyCover = input_list[12]
    canopyHeight = input_list[13]
    NumberOfFactors = input_list[14]
    useYears = input_list[15]
    USLE_day = input_list[16]
    USLE_mon = input_list[17]
    USLE_year = input_list[18]
    USLE_c = input_list[19]
    USLE_n = input_list[20]
    USLE_cn = input_list[21]
    firstyear = input_list[22]
    lastyear = input_list[23]
    dayEmerge_text = input_list[24]
    monthEmerge_text = input_list[25]
    dayMature_text = input_list[26]
    monthMature_text = input_list[27]
    dayHarvest_text = input_list[28]
    monthHarvest_text = input_list[29]
    addYearM = input_list[30]
    addYearH = input_list[31]
    irflag = input_list[32]
    tempflag = input_list[33]
    fleach = input_list[34]
    depletion = input_list[35]
    rateIrrig = input_list[36]
    albedo = input_list[37]
    bcTemp = input_list[38]
    Q10Box = input_list[39]
    soilTempBox1 = input_list[40]
    numHoriz = input_list[41]
    SoilProperty_thick = input_list[42]
    SoilProperty_compartment = input_list[43]
    SoilProperty_bulkden = input_list[44]
    SoilProperty_maxcap = input_list[45]
    SoilProperty_mincap = input_list[46]
    SoilProperty_oc = input_list[47]
    SoilProperty_sand = input_list[48]
    SoilProperty_clay = input_list[49]
    rDepthBox = input_list[50]
    rDeclineBox = input_list[51]
    rBypassBox = input_list[52]
    eDepthBox = input_list[53]
    eDeclineBox = input_list[54]
    appNumber_year = input_list[55]
    totalApp = input_list[56]
    SpecifyYears = input_list[57]
    ApplicationTypes = input_list[58]
    PestAppyDay = input_list[59]
    PestAppyMon = input_list[60]
    Rela_a = input_list[61]
    app_date_type = input_list[62]
    DepthIncorp = input_list[63]
    PestAppyRate = input_list[64]
    localEff = input_list[65]
    localSpray = input_list[66]
    PestDispHarvest = input_list[67]
    nchem = input_list[68]
    convert_Foliar1 = input_list[69]
    parentTo3 = input_list[70]
    deg1To2 = input_list[71]
    foliarHalfLifeBox = input_list[72]
    koc_check = input_list[73]
    Koc = input_list[74]
    soilHalfLifeBox = input_list[75]
    convertSoil1 = input_list[76]
    convert1to3 = input_list[77]
    convert2to3 = input_list[78]


    ff=PRZM5_pi_new.PRZM5_pi(pfac, snowmelt, evapDepth, 
          uslek, uslels, uslep, fieldSize, ireg, slope, hydlength,
          canopyHoldup, rootDepth, canopyCover, canopyHeight,
          NumberOfFactors, useYears,
          USLE_day, USLE_mon, USLE_year, USLE_c, USLE_n, USLE_cn,
          firstyear, lastyear,
          dayEmerge_text, monthEmerge_text, dayMature_text, monthMature_text, dayHarvest_text, monthHarvest_text, addYearM, addYearH,
          irflag, tempflag,
          fleach, depletion, rateIrrig,
          albedo, bcTemp, Q10Box, soilTempBox1,
          numHoriz,
          SoilProperty_thick, SoilProperty_compartment, SoilProperty_bulkden, SoilProperty_maxcap, SoilProperty_mincap, SoilProperty_oc, SoilProperty_sand, SoilProperty_clay,
          rDepthBox, rDeclineBox, rBypassBox,
          eDepthBox, eDeclineBox,
          appNumber_year, totalApp,
          SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, Rela_a, app_date_type, DepthIncorp, PestAppyRate, localEff, localSpray,
          PestDispHarvest,
          nchem, convert_Foliar1, parentTo3, deg1To2, foliarHalfLifeBox,
          koc_check, Koc,
          soilHalfLifeBox,
          convertSoil1, convert1to3, convert2to3)

    return ff

cloud.rest.publish(func=PRZM5, label='PRZM5_s1_new', _env='t-fortran77-test', _type='s1', _profile=True)

