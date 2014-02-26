# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:18:30 2013

@author: Jon F
"""
# from vvwm_parameters_transfer import *
import os
import datetime
from datetime import date
import numpy as np

def makevvwmTransfer(working_dir,
					koc_check, Koc, soilHalfLifeBox, soilTempBox1, foliarHalfLifeBox,
					wc_hl, w_temp, bm_hl, ben_temp, ap_hl, p_ref, h_hl, mwt, vp, sol, Q10Box,
					convertSoil, convert_Foliar, convertWC, convertBen, convertAP, convertH,
					deg_check, totalApp,
					SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, appNumber_year, app_date_type, DepthIncorp, PestAppyRate, localEff, localSpray,
					scenID,
					buried, D_over_dx, PRBEN, benthic_depth, porosity, bulk_density, FROC2, DOC2, BNMAS,
					DFAC, SUSED, CHL, FROC1, DOC1, PLMAS,
					firstYear, lastYear, vvwmSimType,
					afield, area, depth_0, depth_max,
					ReservoirFlowAvgDays):

	inputListofLists = [working_dir,
						koc_check, Koc, soilHalfLifeBox, soilTempBox1, foliarHalfLifeBox,
						wc_hl, w_temp, bm_hl, ben_temp, ap_hl, p_ref, h_hl, mwt, vp, sol, Q10Box,
						convertSoil, convert_Foliar, convertWC, convertBen, convertAP, convertH,
						deg_check, totalApp,
						SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, appNumber_year, app_date_type, DepthIncorp, PestAppyRate, localEff, localSpray,
						scenID,
						buried, D_over_dx, PRBEN, benthic_depth, porosity, bulk_density, FROC2, DOC2, BNMAS,
						DFAC, SUSED, CHL, FROC1, DOC1, PLMAS,
						firstYear, lastYear, vvwmSimType,
						afield, area, depth_0, depth_max,
						ReservoirFlowAvgDays]
	# Check is list is empty:
	for x in inputListofLists:
		if (type(x) == list):
			if is_empty(x) and (deg_check == 1):
				x.append('')
			if is_empty(x) and (deg_check == 2):
				i = 0
				while (i < 2):
					x.append('')
					i = i + 1
			if is_empty(x) and (deg_check == 3):
				i = 0
				while (i < 3):
					x.append('')
					i = i + 1

	####################Start writing input file###################
	myfile = open('vvwmTransfer.txt','w')                                   #Name of transfer file created
	#Chemical Tab
	przm5_ouput = "test"
	myfile.write(working_dir + "/" + przm5_ouput + str(deg_check) + "\n")   #Line 1  Output file name
	myfile.write("" + "\n")                                                 #Line 2  Blank Line
	myfile.write(str(deg_check) + "\n")                                     #Line 3  Number of Chemicals (Parent + Degradates)
	if (koc_check == '1'):
		koc_check = "True"
	else:
		koc_check = "False"
	myfile.write(koc_check + "\n")                                          #Line 4  Koc or Kd?

	if (deg_check == 1):
		myfile.write("{0},".format(*Koc) + ",," + "\n")                     #Line 5  Koc value(mg/L)
		myfile.write("{0},".format(*wc_hl) + ",," + "\n")                   #Line 6  aerobic aquatic halflife(days)
		myfile.write("{0},".format(*w_temp) + ",," + "\n")                  #Line 7  ref temperature of aerobic(C)
		myfile.write("{0},".format(*bm_hl) + ",," + "\n")                   #Line 8  anaerobic aquatic halflife(days)
		myfile.write("{0},".format(*ben_temp) + ",," + "\n")                #Line 9  ref temperature of anaerobic(C)
		myfile.write("{0},".format(*ap_hl) + ",," + "\n")                   #Line 10 photolysis halflife(days)
		myfile.write("{0},".format(*p_ref) + ",," + "\n")                   #Line 11 latitude of photo study  
		myfile.write("{0},".format(*h_hl) + ",," + "\n")                    #Line 12 hydrolysis halflife (days)
		myfile.write("{0},".format(*soilHalfLifeBox) + ",," + "\n")         #Line 13 soil halflife
		myfile.write("{0},".format(*soilTempBox1) + ",," + "\n")            #Line 14 soil ref temp
		myfile.write("{0},".format(*foliarHalfLifeBox) + ",," + "\n")       #Line 15 foliar halflife
		myfile.write("{0},".format(*mwt) + ",," + "\n")                     #Line 16 molecular wt
		myfile.write("{0},".format(*vp) + ",," + "\n")                      #Line 17 vapor pressure (torr)
		myfile.write("{0},".format(*sol) + ",," + "\n")                     #Line 18 solubilty (mg/L)
		myfile.write("0,0," + "\n")                                         #Line 19 MCF: water column metabolism
		myfile.write("0,0," + "\n")                                         #Line 20 MCF: benthic metabolism
		myfile.write("0,0," + "\n")                                         #Line 21 MCF: Photolysis
		myfile.write("0,0," + "\n")                                         #Line 22 MCF: Hydrolysis
		myfile.write("0,0," + "\n")                                         #Line 23 MCF: soil
		myfile.write("0,0," + "\n")                                         #Line 24 MCF: foliar
	if (deg_check == 2):
		myfile.write("{0},{1},".format(*Koc) + "," + "\n")                  #Line 5  Koc value(mg/L)
		myfile.write("{0},{1},".format(*wc_hl) + "," + "\n")                #Line 6  aerobic aquatic halflife(days)
		myfile.write("{0},{1},".format(*w_temp) + "," + "\n")               #Line 7  ref temperature of aerobic(C)
		myfile.write("{0},{1},".format(*bm_hl) + "," + "\n")                #Line 8  anaerobic aquatic halflife(days)
		myfile.write("{0},{1},".format(*ben_temp) + "," + "\n")             #Line 9  ref temperature of anaerobic(C)
		myfile.write("{0},{1},".format(*ap_hl) + "," + "\n")                #Line 10 photolysis halflife(days)
		myfile.write("{0},{1},".format(*p_ref) + "," + "\n")                #Line 11 latitude of photo study  
		myfile.write("{0},{1},".format(*h_hl) + "," + "\n")                 #Line 12 hydrolysis halflife (days)
		myfile.write("{0},{1},".format(*soilHalfLifeBox) + "," + "\n")      #Line 13 soil halflife
		myfile.write("{0},{1},".format(*soilTempBox1) + "," + "\n")         #Line 14 soil ref temp
		myfile.write("{0},{1},".format(*foliarHalfLifeBox) + "," + "\n")    #Line 15 foliar halflife
		myfile.write("{0},{1},".format(*mwt) + "," + "\n")                  #Line 16 molecular wt
		myfile.write("{0},{1},".format(*vp) + "," + "\n")                   #Line 17 vapor pressure (torr)
		myfile.write("{0},{1},".format(*sol) + "," + "\n")                  #Line 18 solubilty (mg/L)
		myfile.write("{0},".format(*convertWC) + "0," + "\n")               #Line 19 MCF: water column metabolism
		myfile.write("{0},".format(*convertBen) + "0," + "\n")              #Line 20 MCF: benthic metabolism
		myfile.write("{0},".format(*convertAP) + "0," + "\n")               #Line 21 MCF: Photolysis
		myfile.write("{0},".format(*convertH) + "0," + "\n")                #Line 22 MCF: Hydrolysis
		myfile.write("{0},".format(*convertSoil) + "0," + "\n")             #Line 23 MCF: soil
		myfile.write("{0},".format(*convert_Foliar) + "0," + "\n")          #Line 24 MCF: foliar
	if (deg_check == 3):
		myfile.write("{0},{1},{2},".format(*Koc) + "\n")                    #Line 5  Koc value(mg/L)
		myfile.write("{0},{1},{2},".format(*wc_hl) + "\n")                  #Line 6  aerobic aquatic halflife(days)
		myfile.write("{0},{1},{2},".format(*w_temp) + "\n")                 #Line 7  ref temperature of aerobic(C)
		myfile.write("{0},{1},{2},".format(*bm_hl) + "\n")                  #Line 8  anaerobic aquatic halflife(days)
		myfile.write("{0},{1},{2},".format(*ben_temp) + "\n")               #Line 9  ref temperature of anaerobic(C)
		myfile.write("{0},{1},{2},".format(*ap_hl) + "\n")                  #Line 10 photolysis halflife(days)
		myfile.write("{0},{1},{2},".format(*p_ref) + "\n")                  #Line 11 latitude of photo study  
		myfile.write("{0},{1},{2},".format(*h_hl) + "\n")                   #Line 12 hydrolysis halflife (days)
		myfile.write("{0},{1},{2},".format(*soilHalfLifeBox) + "\n")        #Line 13 soil halflife
		myfile.write("{0},{1},{2},".format(*soilTempBox1) + "\n")           #Line 14 soil ref temp
		myfile.write("{0},{1},{2},".format(*foliarHalfLifeBox) + "\n")      #Line 15 foliar halflife
		myfile.write("{0},{1},{2},".format(*mwt) + "\n")                    #Line 16 molecular wt
		myfile.write("{0},{1},{2},".format(*vp) + "\n")                     #Line 17 vapor pressure (torr)
		myfile.write("{0},{1},{2},".format(*sol) + "\n")                    #Line 18 solubilty (mg/L)
		myfile.write("{0},{1},".format(*convertWC) + "\n")                  #Line 19 MCF: water column metabolism
		myfile.write("{0},{1},".format(*convertBen) + "\n")                 #Line 20 MCF: benthic metabolism
		myfile.write("{0},{1},".format(*convertAP) + "\n")                  #Line 21 MCF: Photolysis
		myfile.write("{0},{1},".format(*convertH) + "\n")                   #Line 22 MCF: Hydrolysis
		myfile.write("{0},{1},".format(*convertSoil) + "\n")                #Line 23 MCF: soil
		myfile.write("{0},{1},".format(*convert_Foliar) + "\n")             #Line 24 MCF: foliar

	myfile.write('' + "\n")                                              #Line 25 
	myfile.write('' + "\n")                                              #Line 26
	myfile.write('' + "\n")                                              #Line 27
	myfile.write(Q10Box + "\n")                                          #Line 28 Q10 (EXAMS)
	#Crop/Land Tab                                 
	myfile.write(scenID + "\n")                                          #Line 29 identifier for scenario, used for output file naming
	dvf_file = "/test.dvf"
	myfile.write(working_dir + dvf_file + "\n") # TEMPORARY FIXED VALUE  #Line 30 met file name
	myfile.write(vvwmSimType + "\n")                                     #Line 31 (Unused in VVWM?) - radio button for water body type; 0=EPA Res & Pond, 1=Varying Vol, 2=Cons. Vol. w/o Flowthrough, 3=Cons. Vol. w/ Flowthrough, 4=EPA Res Only, 5=EPA Pond Only, 6,n=Res w/ user avg, n=?
	if vvwmSimType == '6':
		myfile.write(ReservoirFlowAvgDays + "\n")                        #Line 32 ReservoirFlowAvgDays
	else:
		myfile.write('' + "\n")                                          #Line 32 No ReservoirFlowAvgDays
	#Water Body Tab                                 
	if (buried == "1"):
		buried = "True"
	else:
		buried = "False"
	myfile.write(buried + "\n")                                          #Line 33 Burial Flag (Boolean)
	myfile.write("" + "\n")                                              #Blank Line 34, Not Used by VVWM, but stores custom afield in GUI (area of adjacent runoff-producing field)
	myfile.write("" + "\n")                                              #Blank Line 35, Not Used by VVWM, but stores custom area in GUI
	myfile.write("" + "\n")                                              #Blank Line 36, Not Used by VVWM, but stores custom depth_0 in GUI (initial water body depth)
	myfile.write("" + "\n")                                              #Blank Line 37 
	myfile.write(D_over_dx + "\n")                                       #Line 38 Mass Xfer Coeff.
	myfile.write(PRBEN + "\n")                                           #Line 39 PRBEN
	myfile.write(benthic_depth + "\n")                                   #Line 40 benthic_depth
	myfile.write(porosity + "\n")                                        #Line 41 porosity
	myfile.write(bulk_density + "\n")                                    #Line 42 bulk_density
	myfile.write(FROC2 + "\n")                                           #Line 43 FROC2
	myfile.write(DOC2 + "\n")                                            #Line 44 DOC2
	myfile.write(BNMAS + "\n")                                           #Line 45 BNMAS
	myfile.write(DFAC + "\n")                                            #Line 46 DFAC
	myfile.write(SUSED + "\n")                                           #Line 47 SUSED
	myfile.write(CHL + "\n")                                             #Line 48 CHL
	myfile.write(FROC1 + "\n")                                           #Line 49 FROC1
	myfile.write(DOC1 + "\n")                                            #Line 50 DOC1
	myfile.write(PLMAS + "\n")                                           #Line 51 PLMAS
	myfile.write("False" + "\n")                                         #Line 52 IDK What this is???
	myfile.write("" + "\n")                                              #Line 53 Unused in VVWM
	myfile.write("" + "\n")                                              #Line 54 Unused in VVWM
	############################# Calculate Total Number of Applications #############################################
	# User Input
	firstYear = firstYear         #From weather file   ("1961" - Hard-coded for now)
	lastYear = lastYear           #From weather file   ("1990" - Hard-coded for now)

	noofyears = (int(lastYear) - int(firstYear)) + 1
	
	napp = int(totalApp) * noofyears
	myfile.write(str(napp) + "\n")                                            #Line 55 Number of applications -> Number of applications * number of years in weather file
	############################# Accumulative Day of the Year of applications Generator #############################
	dayOfYearList = []
	currentYear = firstYear
	YearList = []
	mon = PestAppyMon[0]
	day = PestAppyDay[0]
	count = 0
	j = 0
	tempDateList = []
	while (count < noofyears):
		i = 0
		while (i < len(PestAppyMon)):
			monPlusDayYr = str(currentYear) + "," + PestAppyMon[i] + "," + PestAppyDay[i]
			covertStr2Date = datetime.datetime.strptime(monPlusDayYr, "%Y,%m,%d")
			dayOfYear = covertStr2Date.timetuple().tm_yday
			if (count == 0):
				tempDateList.append(monPlusDayYr.split(","))
				dayOfYearList.append(dayOfYear)
			else:
				prevDate = tempDateList[i]
				currDate = monPlusDayYr.split(",")
				tempDateList[i] = (monPlusDayYr.split(","))
				currDateYr = int(currDate[0])
				currDateMon = int(currDate[1])
				currDateDay = int(currDate[2])
				prevDateYr = int(prevDate[0])
				prevDateMon = int(prevDate[1])
				prevDateDay = int(prevDate[2])
				# Calc difference bw currDate and prevDate:
				d0 = date(currDateYr,currDateMon,currDateDay)
				d1 = date(prevDateYr,prevDateMon,prevDateDay)
				delta = d0 - d1
				# Find index of prevDate to add to:
				dayOfYearListPrevIndex = (j - len(PestAppyMon))
				# Add number of days bw applications to prev application's day-of-year:
				covertStr2Date = dayOfYearList[dayOfYearListPrevIndex] + delta.days
				dayOfYearList.append(covertStr2Date)
			i = i + 1
			j = j + 1
		count = count + 1
		currentYear = int(currentYear) + 1

	dayOfYearStrings = ','.join(str(x) for x in dayOfYearList) + ","
	myfile.write(dayOfYearStrings + "\n")                                   #Line 56 Day-of-year of application
	##################################################################################################################
	
	############################ Convert SWC INPUT "SimType" value to vvwmSimType ####################################
	if vvwmSimType == "0" or vvwmSimType == "5": # 0=EPA Reservoir & Pond (writes Pond first, Line 268 writes Reservoir), 5=EPA Pond Only
		vvwmSimType_new = "2"
		myfile.write(vvwmSimType_new + "\n")                                        #Line 57 vvwmSimType
	elif (vvwmSimType == "4" or vvwmSimType == "6"): # 4=EPA Reservoir Only, 6=Reservoir w/ User Avg, 
		vvwmSimType_new = "3"
		myfile.write(vvwmSimType_new + "\n")                                        #Line 57 vvwmSimType
	elif (vvwmSimType == "1" or vvwmSimType == "2" or vvwmSimType == "3"): #1=Varying Volume
		vvwmSimType_new = "1"
		myfile.write(vvwmSimType_new + "\n")                                        #Line 57 vvwmSimType

	myfile.write(afield[0] + "\n")                                          #Line 58 Field Area ***Reservoir
	myfile.write(area[0] + "\n")                                            #Line 59 Water Body Area ***Reservoir
	myfile.write(depth_0[0] + "\n")                                         #Line 60 Initial Depth ***Reservoir
	myfile.write(depth_max[0] + "\n")                                       #Line 61 Max Depth ***Reservoir
	##################################### ffList Generator ###########################################################
	myfile.write(ffListGenerator(area[0], totalApp, noofyears, PestAppyRate, localSpray[0]) + "\n")    #Line 62 (Drift/T * Amount(rate) * localWaterArea), where: localWaterArea = Water Body Area (Line 59) / 10000   (Line 955 in Form1.vb)
	# myfile.write(ffStrings + "\n")                                        
	##################################################################################################################
	myfile.write(ReservoirFlowAvgDays + "\n")                             #Line 63 "0", unless User Avg Flow is selected sim type, it is the value in the TextBox
	myfile.close()
	if vvwmSimType == "0":
		with open('vvwmTransfer.txt', 'r') as file:
			data = file.readlines()
		data[56] = "3" + "\n"   
		data[57] = afield[1] + "\n"                                      #Line 58 Field Area ***Reservoir
		data[58] = area[1] + "\n"                                     #Line 59 Water Body Area ***Reservoir
		data[59] = depth_0[1] + "\n"                                  #Line 60 Initial Depth ***Reservoir
		data[60] = depth_max[1] + "\n"                                #Line 61 Max Depth ***Reservoir
		data[61] = ffListGenerator(area[1], totalApp, noofyears, PestAppyRate, localSpray[1]) + "\n"
		with open('vvwmTransferRes.txt', 'w') as file:
			file.writelines(data)

# ffList Generator
def ffListGenerator(area, totalApp, noofyears, PestAppyRate, localSpray):
	localWaterArea = float(area) / 10000
	totalAppYears = int(totalApp) * int(noofyears)
	# Convert list of strings to floats:
	PestAppyRate = [float(x) for x in PestAppyRate]
	localSpray = [float(x) for x in localSpray]
	# Convert lists to numpy arrays:
	PestAppyRateArray = np.array(PestAppyRate)
	localSprayArray = np.array(localSpray)
	localWaterAreaArray = np.empty(totalAppYears); localWaterAreaArray.fill(localWaterArea)
	ffArrayFinal = np.array([])

	i = 0
	while (i < noofyears):
		ffArray =  np.multiply(PestAppyRateArray, localSprayArray)
		ffArrayFinal = np.append(ffArrayFinal, ffArray)
		i = i + 1
	ffArrayFinal = np.multiply(ffArrayFinal, localWaterAreaArray)
	# Convert array of floats to strings
	ffStrings = ','.join(str(x) for x in ffArrayFinal) + ","
	return ffStrings

# Function to check if tuple is empty:
def is_empty(any_structure):
    if any_structure:
        # Structure is not empty
        return False
    else:
        # Structure is empty
        return True