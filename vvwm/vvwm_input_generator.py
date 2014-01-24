# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:18:30 2013

@author: Jon F
"""
# from vvwm_parameters_transfer import *
import os
import datetime

def makevvwmTransfer(working_dir, nchem,
					koc_check, Koc, soilHalfLifeBox, soilTempBox1, foliarHalfLifeBox,
					wc_hl, w_temp, bm_hl, ben_temp, ap_hl, p_ref, h_hl, mwt, vp, sol, Q10Box,
					totalApp,
					SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, Rela_a, app_date_type, DepthIncorp, PestAppyRate, localEff, localSpray,
					scenID,
					buried, D_over_dx, PRBEN, benthic_depth, porosity, bulk_density, FROC2, DOC2, BNMAS,
					DFAC, SUSED, CHL, FROC1, DOC1, PLMAS,
					vvwmSimType,
					afield, area, depth_0, depth_max,
					ReservoirFlowAvgDays):

	####################Start writing input file###################
	myfile = open('vvwmTransfer.txt','w')                                #Name of transfer file created
	#Chemical Tab
	myfile.write(working_dir + "\n")                                     #Line 1  Output file name
	myfile.write("" + "\n")                                              #Line 2  Blank Line
	myfile.write(nchem + "\n")                                           #Line 3  Number of Chemicals (degradates?)
	myfile.write(koc_check + "\n")                                       #Line 4  Koc or Kd?
	myfile.write("{0},{1},{2},".format(*Koc) + "\n")                     #Line 5  Koc value(mg/L)
	myfile.write("{0},{1},{2},".format(*wc_hl) + "\n")                   #Line 6  aerobic aquatic halflife(days)
	myfile.write("{0},{1},{2},".format(*w_temp) + "\n")                  #Line 7  ref temperature of aerobic(C)
	myfile.write("{0},{1},{2},".format(*bm_hl) + "\n")                   #Line 8  anaerobic aquatic halflife(days)
	myfile.write("{0},{1},{2},".format(*ben_temp) + "\n")                #Line 9  ref temperature of anaerobic(C)
	myfile.write("{0},{1},{2},".format(*ap_hl) + "\n")                   #Line 10 photolysis halflife(days)
	myfile.write("{0},{1},{2},".format(*p_ref) + "\n")                   #Line 11 latitude of photo study  
	myfile.write("{0},{1},{2},".format(*h_hl) + "\n")                    #Line 12 hydrolysis halflife (days)
	myfile.write("{0},{1},{2},".format(*soilHalfLifeBox) + "\n")         #Line 13 soil halflife
	myfile.write("{0},{1},{2},".format(*soilTempBox1) + "\n")            #Line 14 soil ref temp
	myfile.write("{0},{1},{2},".format(*foliarHalfLifeBox) + "\n")       #Line 15 foliar halflife
	myfile.write("{0},{1},{2},".format(*mwt) + "\n")                     #Line 16 molecular wt
	myfile.write("{0},{1},{2},".format(*vp) + "\n")                      #Line 17 vapor pressure (torr)
	myfile.write("{0},{1},{2},".format(*sol) + "\n")                     #Line 18 solubilty (mg/L)
	                                                                     #        Molar Conversion Factors
	# myfile.write("{0},{1},".format(*wc_mcf) + "\n")                      #Line 19 water column metabolism
	# myfile.write("{0},{1},".format(*ben_mcf) + "\n")                     #Line 20 benthic metabolism
	# myfile.write("{0},{1},".format(*p_mcf) + "\n")                       #Line 21 Photolysis
	# myfile.write("{0},{1},".format(*h_mcf) + "\n")                       #Line 22 Hydrolysis
	# myfile.write("{0},{1},".format(*s_mcf) + "\n")                       #Line 23 soil
	# myfile.write("{0},{1},".format(*f_mcf) + "\n")                       #Line 24 foliar

	myfile.write("0,0" + "\n")                      #Line 19 water column metabolism TEMPORARILY NOT USED
	myfile.write("0,0" + "\n")                      #Line 20 benthic metabolism TEMPORARILY NOT USED
	myfile.write("0,0" + "\n")                      #Line 21 Photolysis TEMPORARILY NOT USED
	myfile.write("0,0" + "\n")                      #Line 22 Hydrolysis TEMPORARILY NOT USED
	myfile.write("0,0" + "\n")                      #Line 23 soil TEMPORARILY NOT USED
	myfile.write("0,0" + "\n")                      #Line 24 foliar TEMPORARILY NOT USED

	myfile.write('' + "\n")                                              #Line 25 
	myfile.write('' + "\n")                                              #Line 26
	myfile.write('' + "\n")                                              #Line 27
	myfile.write(Q10Box + "\n")                                          #Line 28 Q10 (EXAMS)
	#Crop/Land Tab                                 
	myfile.write(scenID + "\n")                                          #Line 29 identifier for scenario, used for output file naming
	dvf_path = "test.dvf"               # TEMPORARY FIXED VALUE
	myfile.write(dvf_path + "\n")                                        #Line 30 met file name
	myfile.write("0" + "\n")                                             #Line 31 Unused in VVWM (radio button for water body type; 0=EPA Res & Pond, 1=Varying Vol, 2=Cons. Vol. w/o Flowthrough, 3=Cons. Vol. w/ Flowthrough, 4=EPA Res Only, 5=EPA Pond Only, 6,n=Res w/ user avg, n=?)
	myfile.write("" + "\n")                                              #Line 32
	#Water Body Tab                                 
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
	mon = PestAppyMon             #From user input (6 = default)
	day = PestAppyDay             #From user input (1 = default)
	firstYear = "1961"            #From weather file   (Hard-coded for now)
	lastYear = "1990"             #From weather file   (Hard-coded for now)

	noofyears = (int(lastYear) - int(firstYear)) + 1
	
	napp = totalApp * noofyears
	myfile.write(napp + "\n")                                            #Line 55 Number of applications -> Number of applications * number of years in weather file
	############################# Accumulative Day of the Year of applications Generator #############################

	dayOfYearList = []
	currentYear = firstYear
	count = 0
	while (count < noofyears):
		monPlusDayYr = str(currentYear) + "," + mon + "," + day
		covertStr2Date = datetime.datetime.strptime(monPlusDayYr, "%Y,%m,%d")
		dayOfYear = covertStr2Date.timetuple().tm_yday
		if (count == 0):
			dayOfYearList.append(dayOfYear)
		else:
			# Calc number of days bw applications (accounts for leap years)
			currDate = monPlusDayYr.split(",")
			currDateYr = int(currDate[0])
			currDateMon = int(currDate[1])
			currDateDay = int(currDate[2])
			prevDateYr = int(prevDate[0])
			prevDateMon = int(prevDate[1])
			prevDateDay = int(prevDate[2])
			d0 = date(currDateYr,currDateMon,currDateDay)
			d1 = date(prevDateYr,prevDateMon,prevDateDay)
			delta = d0 - d1
			dayOfYearListPrevIndex = (count - (count + 1))
			# Add number of days bw applications to prev application's day-of-year
			covertStr2Date = dayOfYearList[dayOfYearListPrevIndex] + delta.days
			dayOfYearList.append(covertStr2Date)
		count = count + 1
		prevDate = monPlusDayYr.split(",")
		currentYear = int(currentYear) + 1

	myfile.write(dayOfYearList + "\n")                                   #Line 56 Day-of-year of application
	##################################################################################################################
	myfile.write(vvwmSimType + "\n")                                     #Line 57 vvwmSimType
	myfile.write(afield + "\n")                                          #Line 58 Field Area ***Dependant on vvwmSimType 
	myfile.write(area + "\n")                                            #Line 59 Water Body Area ***Dependant on vvwmSimType 
	myfile.write(depth_0 + "\n")                                         #Line 60 Initial Depth ***Dependant on vvwmSimType 
	myfile.write(depth_max + "\n")                                       #Line 61 Max Depth ***Dependant on vvwmSimType 
	##################################### ffList Generator ###########################################################
	ffList = []
	i = 0
	localWaterArea = area / 10000
	while (i < noofyears):
		ff = localSpray * PestAppyRate * localWaterArea
		ff = float(format(ff,'.3f'))
		ffList.append(ff)
		i = i + 1

	myfile.write(ffList + "\n")                                          #Line 62 (Drift/T * Amount(rate) * localWaterArea)      where: localWaterArea = Water Body Area (Line 59) / 10000          (Line 955 in Form1.vb)
	##################################################################################################################
	myfile.write(ReservoirFlowAvgDays + "\n")                            #Line 63 "0", unless User Avg Flow is selected sim type, it is the value in the TextBox
	myfile.close()             