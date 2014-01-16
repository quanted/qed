# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 23:18:30 2012

@author: tao
"""

import os
import datetime

def test_przm5(pfac, snowmelt, evapDepth, 
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
               convertSoil1, convert1to3, convert2to3):



    dvf_file = "test.dvf"
    out_file = "test.zts"

    #Record 1
    # pfac = 0.79
    # snowmelt = 0
    # evapDepth = 17.5

    #Record 3
    # uslek = 0.37
    # uslels = 1.34
    # uslep = 0.5
    # fieldSize = 10
    # ireg = 1
    # slope = 6
    # hydlength = 356.8

    #Record 5
    # crop_ID = 1  # WFMAX = 0

    # canopyHoldup = 0.25
    # rootDepth = 12
    # canopyCover = 90
    # canopyHeight = 30

    #Record 6
    # NumberOfFactors = 26
    # useYears = 1

    ##Record 7-10
    # USLE_day = [16,1,16,1,16,1,16,1,16,1,10,16,1,16,1,16,1,16,1,16,1,10,16,1,16,1]
    # USLE_mon = [2,3,3,4,4,5,5,6,6,7,7,7,8,8,9,9,10,10,11,11,12,12,12,1,1,2]
    # USLE_c = [0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011]
    # USLE_n = [0.188,0.190,0.191,0.527,0.558,0.569,0.572,0.574,0.575,0.634,0.796,0.750,0.602,0.302,0.176,0.176,0.177,0.178,0.505,0.560,0.634,0.803,0.767,0.632,0.318,0.186]
    # USLE_cn = [89,89,89,89,89,89,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94]
    # USLE_year = [1972,1971,1975,1976,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1992]

    #Record 11
    # dvf_file_read = open(dvf_file,'r')
    # content = dvf_file_read.readlines()
    # firstyear = int(content[0][5:7])
    # lastyear = int(content[-1][5:7])
    # firstyear = int(61)
    # lastyear = int(90)

    #Record 12
    # dayEmerge_text = 16
    # monthEmerge_text = 2
    # dateEmerge_text = datetime.datetime.strptime(str(dayEmerge_text)+str(monthEmerge_text), "%d%m") 
    # dayMature_text = 5
    # monthMature_text = 5
    # dateMature_text = datetime.datetime.strptime(str(dayMature_text)+str(monthMature_text), "%d%m") 
    # dayHarvest_text = 12
    # monthHarvest_text = 5
    # dateHarvest_text = datetime.datetime.strptime(str(dayHarvest_text)+str(monthHarvest_text), "%d%m") 
    # if dateEmerge_text.date()>dateMature_text.date():
    #     addYearM = 1
    # else:
    #     addYearM = 0

    # if dateMature_text.date()>dateHarvest_text.date():
    #     addYearH = 1
    # else:
    #     addYearH = 0


    #Record 13
    # noIrrigation_Checked = 1
    # if noIrrigation_Checked == 0:
    #     irflag = 0
    # else:
    #     irflag = 2
    # tempflag = 0

    #Record 14
    # overCanopy = 1
    # fleach = 0.45
    # depletion = 0.46
    # rateIrrig= 0.47

    #Record 15-17
    # simTemperature = 1
    # albedo = 0.4
    # bcTemp = 23
    # Q10Box = 2.00 #fixed for EFED
    # soilTempBox1 = 25

    #Record 18
    # numHoriz = 5

    #Record 19
    # SoilProperty_thick = [10, 22, 40, 77, 22]
    # SoilProperty_compartment = [100, 11, 8, 77, 11]
    # SoilProperty_bulkden = [1.575, 1.575, 1.475, 1.725, 1.75]
    # SoilProperty_maxcap = [0.295, 0.295, 0.347, 0.224, 0.214]
    # SoilProperty_mincap = [0.17, 0.17, 0.242, 0.139, 0.089]
    # SoilProperty_oc = [0.725, 0.725, 0.058, 0.058, 0.058]
    # SoilProperty_sand = [0.1, 0.1, 0.1, 0.1, 0.1]
    # SoilProperty_clay = [0.1, 0.1, 0.1, 0.1, 0.1]

    ## SoilProperty_thcond = [0, 0, 0, 0, 0]
    ## SoilProperty_disp = [0, 0, 0, 0, 0]

    #Record 20
    # rDepthBox = 2.0
    # rDeclineBox = 1.55
    # rBypassBox = 0.266

    #Record 21
    # eDepthBox = 0.1
    # eDeclineBox = 0

    #Record C1
    # appNumber_year = 5
    # totalApp = (lastyear - firstyear + 1)*appNumber_year

    #Record C2
    # SpecifyYears = 1
    # ApplicationTypes = [1,2,4,8,7]
    # DepthIncorp = [4,4,5,6,7]
    # PestAppyDay = [1,2,3,4,5]
    # PestAppyMon = [6,7,8,9,10]
    # PestAppyYear = [70,71,72,73,75]
    # PestAppyRate = [1.12,1.13,1.14,1.15,1.16]
    # localEff = [0.95,0.99,0.98,0.97,0.96]
    # localSpray = [0.05,0.1,0.2,0.3,0.4]

    #Record C3
    # post_harvest_foliage=1
    # if post_harvest_foliage == 1:
    #     PestDispHarvest = 1
    # elif post_harvest_foliage == 2:
    #     PestDispHarvest = 2
    # else:
    #     PestDispHarvest = 3

    #Record C4
    # Deg1CheckBox = 1
    # Deg2CheckBox = 0
    # if Deg1CheckBox == 1:
    #     nchem = 2
    # elif Deg2CheckBox == 1:
    #     nchem = 3
    # else:
    #     nchem = 1

    # foliarHalfLifeBox = [23, 50]

    #Record C5
    # convert_Foliar1 = 0.6
    # parentTo3=0
    # deg1To2=0

    #Record C7
    # koc_check=1
    # Koc1=200
    # Koc2=201
    # Koc3=202

    #Record C8
    # soilHalfLifeBox=[100,101,102]
    # soilRate=[0,0,0]

    #Record C9
    # convertSoil1=0.5
    # convert1to3=0
    # convert2to3=0
    # convertSoil2=0.51

    # if nchem == 2:
    #     convert1to3 = 0
    #     convert2to3 = 0
    # elif nchem == 2:
    #     convert1to3 = 0
    #     convert2to3 = 0
    # else:
    #     convert1to3 = 0
    #     convert2to3 = convertSoil2





    # from przm5_parameters_t import *


    ####################Start writing input file###################
    myfile = open('PRZM5.inp','w')
    # myfile = []

    myfile.write("***  " + datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + "\n")
    myfile.write("***  PRZM5 Input File Generator" + "\n")
    myfile.write("***Record A1: Weather File" + "\n")
    myfile.write(dvf_file + "\n")
    myfile.write("***Record A2: PRZM5 Time Series Output File" + "\n")
    myfile.write(out_file + "\n")
    myfile.write("***Record A3: PRZM5 Advanced Options" + "\n")
    myfile.write("True,True,True,True,False " + "\n")

    myfile.write("***Record 1: pfac, sfac, anetd, inicrp " + "\n")
    myfile.write('{0}, {1}, {2}, {3}'.format(*[pfac, snowmelt, evapDepth, 1]) + "\n")

    myfile.write("***Record 2: Erosion Flag 4 = MUSS, 3= MUST, 1= MUSLE " + "\n")
    myfile.write('{0}'.format(4) + "\n")

    myfile.write("***Record 3: uslek, uslels, uslep, FieldSize, ireg, slope, hydraul length " + "\n")
    myfile.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(*[uslek, uslels, uslep, fieldSize, ireg, slope, hydlength]) + "\n")

    myfile.write("***Record 4: Number of Crops in Simulation" + "\n")
    myfile.write(str(1) + "\n")

    myfile.write("***Record 5: Crop ID, canopyHoldup, rootDepth, canopyCover, WFMAX (optional), canopyHeight" + "\n")
    myfile.write('{0}, {1}, {2}, {3}, {4}, {5}'.format(*[1, canopyHoldup, rootDepth, canopyCover, 0, canopyHeight]) + "\n")

    myfile.write("***Record 6: CROPNO, NUSLEC, use_usleyears" + "\n")
    myfile.write('{0}, {1}, {2}'.format(*[1, NumberOfFactors, useYears]) + "\n")

    myfile.write("***Record 7 4DayMon" + "\n")
    Record_7 = ','.join(str(int(x)*100+int(y)) for (x, y) in zip(USLE_day, USLE_mon))
    myfile.write(Record_7 + "\n")

    if useYears == 1:
        myfile.write("***Record 7a Year" + "\n")
        Record_7a = ','.join(str(x) for x in USLE_year)
        myfile.write(Record_7a + "\n")

    myfile.write("***Record 8 Soil loss cover management factors, C value" + "\n")
    Record9Cstring = ','.join(str(x) for x in USLE_c)
    myfile.write(Record9Cstring + "\n")

    myfile.write("***Record 9 Manning’s N" + "\n")
    Record9Dstring = ','.join(str(x) for x in USLE_n)
    myfile.write(Record9Dstring + "\n")

    myfile.write("***Record 10 Runoff curve number" + "\n")
    Record9Estring = ','.join(str(x) for x in USLE_cn)
    myfile.write(Record9Estring + "\n")

    myfile.write("***Record 11: Number of Applications that follow" + "\n")
    myfile.write('{0}'.format(lastyear - firstyear + 1) + "\n")

    myfile.write("***Record 12 EMD, EMM, IYREM, MAD, MAM, IYRAT, HAD, HAM, IYRHAR, INCRP" + "\n")
    for i in range(firstyear, lastyear+1):
        Record_12 = [dayEmerge_text, monthEmerge_text, i, dayMature_text, monthMature_text, (i+addYearM), dayHarvest_text, monthHarvest_text, (i+addYearM+addYearH), 1]
        myfile.write('{0:>2},{1:>2},{2:>2},{3:>4},{4:>2},{5:>2},{6:>4},{7:>2},{8:>2},{9:>8}'.format(*Record_12) + "\n")

    myfile.write("***Record 13: irrflag, Tempflag, thermConducflag" + "\n")
    myfile.write('{0:>2},{1:>2},{1:>2}'.format(*[irflag, tempflag]) + "\n")

    if int(irflag) != 0:
        if int(irflag) == 1:
            irtype = 3
        elif int(irflag) == 2:
            irtype = 4
        myfile.write("***Record 14 IRTYP, FLEACH, PCDEPL, RATEAP" + "\n")
        myfile.write('{0:>1},{1:>5},{2:>5},{3:>5}'.format(*[irtype, fleach, depletion, rateIrrig]) + "\n")

    if int(tempflag) == 1:
        myfile.write("***Record 15 ALBEDO, EMMISS, ZWIND" + "\n")
        myfile.write("{0},{0},{0},{0},{0},{0},{0},{0},{0},{0},{0},{0}, {1}, {2}".format(*[albedo, 0.97, 10.0]) + "\n")

        myfile.write("***Record 16 BBT" + "\n")
        myfile.write("{0},{0},{0},{0},{0},{0},{0},{0},{0},{0},{0},{0}".format(bcTemp) + "\n")

        myfile.write("***Record 17 QFAC(1), ..., QFAC(Nchem) TBASE(1), ... ,TBASE(Nchem)" + "\n")
        myfile.write("{0},{1}".format(*[Q10Box, soilTempBox1]) + "\n")


    myfile.write("***Record 18: Number of horizons" + "\n")
    myfile.write("{0}".format(numHoriz) + "\n")

    myfile.write("*** Record 19" + "\n")
    myfile.write("*** #,thk, Del, Dsp,   bd,  W0,    FC,    WP,    oc, snd, cly, thermcon, tmp " + "\n")

    for i in range(numHoriz):
        if not SoilProperty_sand:
            Record_19 = [i+1, SoilProperty_thick[i], SoilProperty_compartment[i], 0, SoilProperty_bulkden[i],
                         SoilProperty_maxcap[i], SoilProperty_maxcap[i], SoilProperty_mincap[i], SoilProperty_oc[i], 0]
            myfile.write('{0}, {1}, {2}, {3:2.1f}, {4:.3f}, {5:.3f}, {6:.3f}, {7:.3f}, {8:.3f}, , , {9:.1f}, ,'.format(*Record_19) + "\n")
        else:
            Record_19 = [i+1, SoilProperty_thick[i], SoilProperty_compartment[i], 0, SoilProperty_bulkden[i],
                         SoilProperty_maxcap[i], SoilProperty_maxcap[i], SoilProperty_mincap[i], SoilProperty_oc[i], SoilProperty_sand[i],
                         SoilProperty_clay[i], 0, bcTemp]
            myfile.write('{0}, {1}, {2}, {3:2.1f}, {4:.3f}, {5:.3f}, {6:.3f}, {7:.3f}, {8:.3f}, {9}, {10}, {11:.1f}, {12}'.format(*Record_19) + "\n")

    myfile.write("*** Record 20, New Runoff Extraction Parameters: rDepth, rDecline, Bypass" + "\n")
    myfile.write('{0},{1},{2}'.format(*(rDepthBox, rDeclineBox, rBypassBox)) + "\n")

    myfile.write("*** Record 21: New Erosion Extraction Parameters: eDepth, eDecline" + "\n")
    myfile.write('{0},{1}'.format(*(eDepthBox, eDeclineBox)) + "\n")

    myfile.write("************ START OF CHEMICAL INPUTS ***************************" + "\n")
    if SpecifyYears == 1:
        totalApp = appNumber_year
        Record_C1 = [totalApp, nchem]
        myfile.write("***Record C1  Number of Applications, Number of Chemicals" + "\n")
        myfile.write('{0:>8}{1:>8}'.format(*Record_C1) + "\n")
        myfile.write("***Record C2  mm,dd,yy, cam, dep, rate, eff, spry, 1cam, 1dep, 1rate, 1eff, 1spry, 2cam, 2dep, 2rate, 2eff, 2spry, " + "\n")

        for j in range(totalApp):
            if ApplicationTypes[j] == 1:
                cam = 1
                depi = DepthIncorp[j]
            elif ApplicationTypes[j]==2:
                cam = 2
                depi = DepthIncorp[j]
            elif ApplicationTypes[j]==4:
                cam = 4
                depi = DepthIncorp[j]
            elif ApplicationTypes[j]==8:
                cam = 8
                depi = DepthIncorp[j]
            else:
                cam = 7
                depi = DepthIncorp[j]

            if app_date_type == '0':
                Record_C2_temp = [PestAppyDay[j], PestAppyMon[j], PestAppyYear[j], cam, depi, PestAppyRate[j], localEff[j], localSpray[j], 1, 4.0, 0, 0, 0, 1, 4.0, 0, 0, 0]
            else:
                now = datetime(1961, int(2), int(16))
                Later = now + timedelta(days=int(Rela_a[j]))
                Later=str(Later)
                Record_C2_temp = [Later[2:4], Later[5:7], PestAppyYear[j], cam, depi, PestAppyRate[j], localEff[j], localSpray[j], 1, 4.0, 0, 0, 0, 1, 4.0, 0, 0, 0]

            myfile.write('{0},{1},{2},{3},{4},{5},{6},{7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}'.format(*Record_C2_temp) + "\n")
    else:
        totalApp = (lastyear - firstyear + 1)*appNumber_year
        Record_C1 = [totalApp, nchem]
        myfile.write("***Record C1  Number of Applications, Number of Chemicals" + "\n")
        myfile.write('{0:>8}{1:>8}'.format(*Record_C1) + "\n")
        myfile.write("***Record C2  mm,dd,yy, cam, dep, rate, eff, spry, 1cam, 1dep, 1rate, 1eff, 1spry, 2cam, 2dep, 2rate, 2eff, 2spry, " + "\n")
        ll=0
        for k in range(firstyear, lastyear+1):
            for j in range(appNumber_year):
                if ApplicationTypes[j] == 1:
                    cam = 1
                    depi = DepthIncorp[j]
                elif ApplicationTypes[j]==2:
                    cam = 2
                    depi = DepthIncorp[j]
                elif ApplicationTypes[j]==4:
                    cam = 4
                    depi = DepthIncorp[j]
                elif ApplicationTypes[j]==8:
                    cam = 8
                    depi = DepthIncorp[j]
                else:
                    cam = 7
                    depi = DepthIncorp[j]

                PestAppyYear = firstyear + ll

                if app_date_type == '0':
                    Record_C2_temp = [PestAppyDay[j], PestAppyMon[j], PestAppyYear, cam, depi, PestAppyRate[j], localEff[j], localSpray[j], 1, 4.0, 0, 0, 0, 1, 4.0, 0, 0, 0]
                else:
                    now = datetime.datetime(1961, int(2), int(16))
                    Later = now + datetime.timedelta(days=int(Rela_a[j]))
                    Later=str(Later)
                    Record_C2_temp = [Later[8:10], Later[5:7], PestAppyYear, cam, depi, PestAppyRate[j], localEff[j], localSpray[j], 1, 4.0, 0, 0, 0, 1, 4.0, 0, 0, 0]


                myfile.write('{0},{1},{2},{3},{4},{5},{6},{7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}'.format(*Record_C2_temp) + "\n")
            ll=ll+1


    myfile.write("***Record C3: FILTRA,IPSCND,UPTKF,1IPSCND,1UPTKF,2IPSCND,2UPTKF " + "\n")
    Record_C3 = [0, PestDispHarvest, 0]
    myfile.write('{0},{1},{2},{1},{2},{1},{2}'.format(*Record_C3) + "\n")

    foliar_cam= [2,3,9,10]
    if any(x in foliar_cam for x in ApplicationTypes):
        for zz in range(nchem):
            if foliarHalfLifeBox[zz] == 0:
                foliarRate=0
            else:
                foliarRate = 0.69314/foliarHalfLifeBox[zz]
            myfile.write('***Record C4 (Chem #{0} PLVKRT, PLDKRT, FEXTRC)'.format(zz+1) + "\n")
            myfile.write('{0}, {1}, {2}'.format(*[0, foliarRate, 0.5]) + "\n")
        if nchem>1:
            myfile.write('***Record C5 PTRAN12, PTRAN13, PTRAN23' + "\n")
            myfile.write('{0}, {1}, {2}'.format(*[convert_Foliar1, parentTo3, deg1To2]) + "\n")

    myfile.write('***Record C6: volatilization' + "\n")
    myfile.write('{0},{0},{0},{0},{0},{0},{0},{0},{0}'.format(0) + "\n")

    myfile.write('*** Record C7: Kd1, Kd2, Kd3 for each horizon' + "\n")
    for kk in range(numHoriz):
        if koc_check == '1':
            kdfactor = SoilProperty_oc[kk] * 0.01
        else:
            kdfactor = 1

        if nchem == 1:
            kd1 = Koc[0] * kdfactor
            myfile.write('{0}'.format(kd1) + "\n")
        elif nchem == 2:
            kd1 = Koc[0] * kdfactor
            kd2 = Koc[1] * kdfactor
            myfile.write('{0},{1}'.format(*[kd1, kd2]) + "\n")
        else:
            kd1 = Koc[0] * kdfactor
            kd2 = Koc[1] * kdfactor
            kd3 = Koc[2] * kdfactor
            myfile.write('{0},{1},{2}'.format(*[kd1, kd2, kd3]) + "\n")


    myfile.write('*** Record C8: Degradation Rates Aqueous, Sorbed, Gas' + "\n")
    soilRate=[0,0,0]
    for kk in range(numHoriz):
        if nchem == 1:
            if soilHalfLifeBox[0] != 0:
                soilRate[0] = 0.69314 / soilHalfLifeBox[0]

            myfile.write('{0},{0},{1}'.format(*[soilRate[0], 0]) + "\n")
        elif nchem == 2:
            if soilHalfLifeBox[0] != 0:
                soilRate[0] = 0.69314 / soilHalfLifeBox[0]
            if soilHalfLifeBox[1] != 0:
                soilRate[1] = 0.69314 / soilHalfLifeBox[1]
            myfile.write('{0},{0},{1},{2},{2},{1}'.format(*[soilRate[0], 0, soilRate[1]]) + "\n")
        else:
            if soilHalfLifeBox[0] != 0:
                soilRate[0] = 0.69314 / soilHalfLifeBox[0]
            if soilHalfLifeBox[1] != 0:
                soilRate[1] = 0.69314 / soilHalfLifeBox[1]
            if soilHalfLifeBox[2] != 0:
                soilRate[2] = 0.69314 / soilHalfLifeBox[2]
            myfile.write('{0},{0},{1},{2},{2},{1},{3},{3},{1}'.format(*[soilRate[0], 0, soilRate[1], soilRate[2]]) + "\n")


    myfile.write('*** Record C9: Molar Conversions 1 to 2, 1 to 3, 2 to 3' + "\n")
    for kk in range(numHoriz):
        myfile.write('{0},{1},{2}'.format(*[convertSoil1, convert1to3, convert2to3]) + "\n")

###############################Original##################################################
    # myfile.write('********** OUTPUT SPECIFICATIONS ***********************' + "\n")
    # myfile.write('*** Record U1' + "\n")
    # myfile.write('{0}'.format(8 + 2 * nchem) + "\n")

    # myfile.write('*** Record U2' + "\n")
    # myfile.write('RUNF,0,TSER,   0,   0,    1.0' + "\n")
    # myfile.write('ESLS,0,TSER,   0,   0,    1.0' + "\n")

    # mwtBox=[1000, 100, 10]

    # for kk in range(nchem):
    #     myfile.write('RFLX,{0},TSER,   0,   0,{1:8.3f}'.format(*[kk+1, mwtBox[kk]/float(mwtBox[0])]) + "\n")
    #     myfile.write('EFLX,{0},TSER,   0,   0,{1:8.3f}'.format(*[kk+1, mwtBox[kk]/float(mwtBox[0])]) + "\n")

    # myfile.write('TPST,0,TSER,   1,   1,    1.0' + "\n")
    # myfile.write('TPST,0,TSER,   2,   2,    1.0' + "\n")
    # myfile.write('TPST,0,TSER,   3,   3,    1.0' + "\n")
    # myfile.write('TPST,0,TSER,   4,   4,    1.0' + "\n")
    # myfile.write('TPST,0,TSER,   5,   5,    1.0' + "\n")
    # myfile.write('TPST,0,TSER,   1,  30,    1.0' + "\n")
###############################Original##################################################
    myfile.write('********** OUTPUT SPECIFICATIONS ***********************' + "\n")
    myfile.write('*** Record U1' + "\n")
    myfile.write('{0}'.format(5) + "\n")
    myfile.write('IRRG,0,TSER,   0,   0,    1.0' + "\n")
    myfile.write('PRCP,0,TSER,   0,   0,    1.0' + "\n")
    myfile.write('RUNF,0,TSER,   0,   0,    1.0' + "\n")
    myfile.write('CEVP,0,TSER,   0,   0,    1.0' + "\n")
    myfile.write('TETD,0,TSER,   0,   0,    1.0' + "\n")


    myfile.close()
    # return myfile


