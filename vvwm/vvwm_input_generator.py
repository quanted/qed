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
myfile.write(nchem + "\n")                              #Line 2  Number of Chemicals (degradates?)
myfile.write(K_unit + "\n")                             #Line 3  Koc or Kd?
myfile.write("{0},{1},{2},".format(*sorp_K) + "\n")     #Line 4  K value(mg/L)
myfile.write("{0},{1},{2},".format(*wc_hl) + "\n")      #Line 5  aerobic aquatic halflife(days)
myfile.write("{0},{1},{2},".format(*w_temp) + "\n")     #Line 6  ref temperature of aerobic(C)
myfile.write("{0},{1},{2},".format(*wc_hl) + "\n")      #Line 7  anaerobic aquatic halflife(days)
myfile.write("{0},{1},{2},".format(*ben_temp) + "\n")   #Line 8  ref temperature of anaerobic(C)
myfile.write("{0},{1},{2},".format(*ap_hl) + "\n")      #Line 9  photolysis halflife(days)
myfile.write("{0},{1},{2},".format(*p_ref) + "\n")      #Line 10 latitude of photo study  
myfile.write("{0},{1},{2},".format(*h_hl) + "\n")       #Line 11 hydrolysis halflife (days)
myfile.write("{0},{1},{2},".format(*s_hl) + "\n")       #Line 12
myfile.write("{0},{1},{2},".format(*s_ref) + "\n")      #Line 13
myfile.write("{0},{1},{2},".format(*f_hl) + "\n")       #Line 14
myfile.write("{0},{1},{2},".format(*mwt) + "\n")        #Line 15 molecular wt
myfile.write("{0},{1},{2},".format(*vp) + "\n")         #Line 16 vapor pressure (torr)
myfile.write("{0},{1},{2},".format(*sol) + "\n")        #Line 17 solubilty (mg/L)
                                                        #        Molar Conversion Factors
myfile.write("{0},{1},".format(*wc_mcf) + "\n")         #Line 18
myfile.write("{0},{1},".format(*ben_mcf) + "\n")        #Line 19
myfile.write("{0},{1},".format(*p_mcf) + "\n")          #Line 20
myfile.write("{0},{1},".format(*h_mcf) + "\n")          #Line 21
myfile.write("{0},{1},".format(*s_mcf) + "\n")          #Line 22
myfile.write("{0},{1},".format(*f_mcf) + "\n")          #Line 23

myfile.write('True' + "\n")         #Line 24 
myfile.write('False' + "\n")        #Line 25
myfile.write('False' + "\n")        #Line 26
myfile.write(QT + "\n")             #Line 27 Q10
#Crop/Land Tab
myfile.write(scenID + "\n")         #Line 28 identifier for scenario, used for output file naming
myfile.write(dvf_path + "\n")       #Line 29 met file name
myfile.write("0" + "\n")            #Line 30 Unused in VVWM (radio button for water body type)
myfile.write("1" + "\n")            #Line 31
myfile.write(buried + "\n")         #Line 32 Burial Flag
myfile.write("" + "\n")             #Blank Line 33, Not Used by VVWM, but stores custom afield in GUI (area of adjacent runoff-producing field)
myfile.write("" + "\n")             #Blank Line 34, Not Used by VVWM, but stores custom area in GUI
myfile.write("" + "\n")             #Blank Line 35, Not Used by VVWM, but stores custom depth_0 in GUI (initial water body depth)
#Water Body Tab
myfile.write("1e-8" + "\n")      #Line 36 Unused in VVWM, but stores custom depth_max in GUI (maximum water body depth)
myfile.write(PRBEN + "\n")          #Line 37
myfile.write(benthic_depth + "\n")  #Line 38
myfile.write(porosity + "\n")       #Line 39
myfile.write(bulk_density + "\n")   #Line 40
myfile.write(FROC2 + "\n")          #Line 41
myfile.write(DOC2 + "\n")           #Line 42
myfile.write(BNMAS + "\n")          #Line 43
myfile.write(DFAC + "\n")           #Line 45
myfile.write(SUSED + "\n")          #Line 46
myfile.write(CHL + "\n")            #Line 47
myfile.write(FROC1 + "\n")          #Line 48
myfile.write(DOC1 + "\n")           #Line 49
myfile.write(PLMAS + "\n")          #Line 50
myfile.write("" + "\n")             #Line 51 Unused in VVWM
myfile.write("" + "\n")             #Line 52 Unused in VVWM
myfile.write("" + "\n")             #Line 53 Unused in VVWM
myfile.write(napp + "\n")           #Line 54



myfile.close()