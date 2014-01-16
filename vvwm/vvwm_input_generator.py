# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:18:30 2013

@author: Jon F
"""
from vvwm_parameters_transfer import *
# from vvwm_parameters import *

####################Start writing input file###################
myfile = open('vvwmTransferJon.txt','w')                #Change to "vvwmTransfer.txt" when finished
#Chemical Tab
myfile.write(working_dir + "\n")                        #Line 1  Output file name
myfile.write("" + "\n")                                 #Line 2  Blank Line
myfile.write(nchem + "\n")                              #Line 3  Number of Chemicals (degradates?)
myfile.write(K_unit + "\n")                             #Line 4  Koc or Kd?
myfile.write("{0},{1},{2},".format(*sorp_K) + "\n")     #Line 5  K value(mg/L)
myfile.write("{0},{1},{2},".format(*wc_hl) + "\n")      #Line 6  aerobic aquatic halflife(days)
myfile.write("{0},{1},{2},".format(*w_temp) + "\n")     #Line 7  ref temperature of aerobic(C)
myfile.write("{0},{1},{2},".format(*wc_hl) + "\n")      #Line 8  anaerobic aquatic halflife(days)
myfile.write("{0},{1},{2},".format(*ben_temp) + "\n")   #Line 9  ref temperature of anaerobic(C)
myfile.write("{0},{1},{2},".format(*ap_hl) + "\n")      #Line 10 photolysis halflife(days)
myfile.write("{0},{1},{2},".format(*p_ref) + "\n")      #Line 11 latitude of photo study  
myfile.write("{0},{1},{2},".format(*h_hl) + "\n")       #Line 12 hydrolysis halflife (days)
myfile.write("{0},{1},{2},".format(*s_hl) + "\n")       #Line 13 soil halflife
myfile.write("{0},{1},{2},".format(*s_ref) + "\n")      #Line 14 soil ref temp
myfile.write("{0},{1},{2},".format(*f_hl) + "\n")       #Line 15 foliar halflife
myfile.write("{0},{1},{2},".format(*mwt) + "\n")        #Line 16 molecular wt
myfile.write("{0},{1},{2},".format(*vp) + "\n")         #Line 17 vapor pressure (torr)
myfile.write("{0},{1},{2},".format(*sol) + "\n")        #Line 18 solubilty (mg/L)
                                                        #        Molar Conversion Factors
myfile.write("{0},{1},".format(*wc_mcf) + "\n")         #Line 19 water column metabolism
myfile.write("{0},{1},".format(*ben_mcf) + "\n")        #Line 20 benthic metabolism
myfile.write("{0},{1},".format(*p_mcf) + "\n")          #Line 21 Photolysis
myfile.write("{0},{1},".format(*h_mcf) + "\n")          #Line 22 Hydrolysis
myfile.write("{0},{1},".format(*s_mcf) + "\n")          #Line 23 soil
myfile.write("{0},{1},".format(*f_mcf) + "\n")          #Line 24 foliar

myfile.write('' + "\n")                                 #Line 25 
myfile.write('' + "\n")                                 #Line 26
myfile.write('' + "\n")                                 #Line 27
myfile.write(QT + "\n")                                 #Line 28 Q10
#Crop/Land Tab                    
myfile.write(scenID + "\n")                             #Line 29 identifier for scenario, used for output file naming
myfile.write(dvf_path + "\n")                           #Line 30 met file name
myfile.write("0" + "\n")                                #Line 31 Unused in VVWM (radio button for water body type)
myfile.write("" + "\n")                                 #Line 32
#Water Body Tab                    
myfile.write(buried + "\n")                             #Line 33 Burial Flag (1 = buried)
myfile.write("" + "\n")                                 #Blank Line 34, Not Used by VVWM, but stores custom afield in GUI (area of adjacent runoff-producing field)
myfile.write("" + "\n")                                 #Blank Line 35, Not Used by VVWM, but stores custom area in GUI
myfile.write("" + "\n")                                 #Blank Line 36, Not Used by VVWM, but stores custom depth_0 in GUI (initial water body depth)
myfile.write("" + "\n")                                 #Blank Line 37 
myfile.write("1e-8" + "\n")                             #Line 38 Unused in VVWM, but stores custom depth_max in GUI (maximum water body depth)
myfile.write(PRBEN + "\n")                              #Line 39 PRBEN
myfile.write(benthic_depth + "\n")                      #Line 40 benthic_depth
myfile.write(porosity + "\n")                           #Line 41 porosity
myfile.write(bulk_density + "\n")                       #Line 42 bulk_density
myfile.write(FROC2 + "\n")                              #Line 43 FROC2
myfile.write(DOC2 + "\n")                               #Line 44 DOC2
myfile.write(BNMAS + "\n")                              #Line 45 BNMAS
myfile.write(DFAC + "\n")                               #Line 46 DFAC
myfile.write(SUSED + "\n")                              #Line 47 SUSED
myfile.write(CHL + "\n")                                #Line 48 CHL
myfile.write(FROC1 + "\n")                              #Line 49 FROC1
myfile.write(DOC1 + "\n")                               #Line 50 DOC1
myfile.write(PLMAS + "\n")                              #Line 51 PLMAS
myfile.write("False" + "\n")                            #Line 52 UPDATE THIS VARIABLE IN PARAMETERS!!!
myfile.write("" + "\n")                                 #Line 53 Unused in VVWM
myfile.write("" + "\n")                                 #Line 54 Unused in VVWM
myfile.write(napp + "\n")                               #Line 55 Number of applications -> Number of applications * number of years in weather file
myfile.write(appDayofYear + "\n")                       #Line 56 Day of year of application
myfile.write(vvwmSimType + "\n")                        #Line 56 VVWM Sim Type
myfile.write(afield + "\n")                             #Line 56 ***Dependant on vvwmSimType 
myfile.write(area + "\n")                               #Line 56 ***Dependant on vvwmSimType 
myfile.write(depth_0 + "\n")                            #Line 56 ***Dependant on vvwmSimType 
myfile.write(depth_max + "\n")                          #Line 56 ***Dependant on vvwmSimType 


myfile.close()