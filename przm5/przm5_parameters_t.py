# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 23:18:30 2012

@author: tao
"""
import os
import datetime

dvf_file = "test.dvf"
out_file = "test.zts"

#Record 1
pfac = 0.79
snowmelt = 0
evapDepth = 17.5

#Record 3
uslek = 0.37
uslels = 1.34
uslep = 0.5
fieldSize = 10
ireg = 1
slope = 6
hydlength = 356.8

#Record 5
# crop_ID = 1
canopyHoldup = 0.25
rootDepth = 12
canopyCover = 90
# WFMAX = 0
canopyHeight = 30

#Record 6
NumberOfFactors = 26
useYears = 1

##Record 7-10
USLE_day = [16,1,16,1,16,1,16,1,16,1,10,16,1,16,1,16,1,16,1,16,1,10,16,1,16,1]
USLE_mon = [2,3,3,4,4,5,5,6,6,7,7,7,8,8,9,9,10,10,11,11,12,12,12,1,1,2]
USLE_c = [0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011]
USLE_n = [0.188,0.190,0.191,0.527,0.558,0.569,0.572,0.574,0.575,0.634,0.796,0.750,0.602,0.302,0.176,0.176,0.177,0.178,0.505,0.560,0.634,0.803,0.767,0.632,0.318,0.186]
USLE_cn = [89,89,89,89,89,89,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94]
USLE_year = [1972,1971,1975,1976,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1972,1992]

#Record 11
dvf_file_read = open(dvf_file,'r')
content = dvf_file_read.readlines()
firstyear = int(content[0][5:7])
lastyear = int(content[-1][5:7])


#Record 12
dayEmerge_text = 16
monthEmerge_text = 2
dateEmerge_text = datetime.datetime.strptime(str(dayEmerge_text)+str(monthEmerge_text), "%d%m") 
dayMature_text = 5
monthMature_text = 5
dateMature_text = datetime.datetime.strptime(str(dayMature_text)+str(monthMature_text), "%d%m") 
dayHarvest_text = 12
monthHarvest_text = 5
dateHarvest_text = datetime.datetime.strptime(str(dayHarvest_text)+str(monthHarvest_text), "%d%m") 
if dateEmerge_text.date()>dateMature_text.date():
    addYearM = 1
else:
    addYearM = 0

if dateMature_text.date()>dateHarvest_text.date():
    addYearH = 1
else:
    addYearH = 0


#Record 13
noIrrigation_Checked = 1
if noIrrigation_Checked == 0:
    irflag = 0
else:
    irflag = 2
tempflag = 0

#Record 14
overCanopy = 1
fleach = 0.45
depletion = 0.46
rateIrrig= 0.47

#Record 15-17
simTemperature = 1
albedo = 0.4
bcTemp = 23
Q10Box = 2.00 #fixed for EFED
soilTempBox1 = 25

#Record 18
numHoriz = 5

#Record 19
SoilProperty_thick = [10, 22, 40, 77, 22]
SoilProperty_compartment = [100, 11, 8, 77, 11]
# SoilProperty_disp = [0, 0, 0, 0, 0]
SoilProperty_bulkden = [1.575, 1.575, 1.475, 1.725, 1.75]
SoilProperty_maxcap = [0.295, 0.295, 0.347, 0.224, 0.214]
SoilProperty_mincap = [0.17, 0.17, 0.242, 0.139, 0.089]
SoilProperty_oc = [0.725, 0.725, 0.058, 0.058, 0.058]
SoilProperty_sand = [0.1, 0.1, 0.1, 0.1, 0.1]
SoilProperty_clay = [0.1, 0.1, 0.1, 0.1, 0.1]
# SoilProperty_thcond = [0, 0, 0, 0, 0]

#Record 20
rDepthBox = 2.0
rDeclineBox = 1.55
rBypassBox = 0.266

#Record 21
eDepthBox = 0.1
eDeclineBox = 0

#Record C1
appNumber_year = 5
totalApp = (lastyear - firstyear + 1)*appNumber_year

#Record C2
SpecifyYears = 1
ApplicationTypes = [1,2,4,8,7]
DepthIncorp = [4,4,5,6,7]
PestAppyDay = [1,2,3,4,5]
PestAppyMon = [6,7,8,9,10]
PestAppyYear = [70,71,72,73,75]
PestAppyRate = [1.12,1.13,1.14,1.15,1.16]
localEff = [0.95,0.99,0.98,0.97,0.96]
localSpray = [0.05,0.1,0.2,0.3,0.4]

#Record C3
post_harvest_foliage=1
if post_harvest_foliage == 1:
    PestDispHarvest = 1
elif post_harvest_foliage == 2:
    PestDispHarvest = 2
else:
    PestDispHarvest = 3

#Record C4
Deg1CheckBox = 1
Deg2CheckBox = 0
if Deg1CheckBox == 1:
    nchem = 2
elif Deg2CheckBox == 1:
    nchem = 3
else:
    nchem = 1

foliarHalfLifeBox = [23, 50]

#Record C5
convert_Foliar1 = 0.6
parentTo3=0
deg1To2=0

#Record C7
koc_check=1
Koc1=200
Koc2=201
Koc3=202

#Record C8
soilHalfLifeBox=[100,101,102]
soilRate=[0,0,0]

#Record C9
convertSoil1=0.5
convert1to3=0
convert2to3=0
convertSoil2=0.51

if nchem == 2:
    convert1to3 = 0
    convert2to3 = 0
elif nchem == 2:
    convert1to3 = 0
    convert2to3 = 0
else:
    convert1to3 = 0
    convert2to3 = convertSoil2




