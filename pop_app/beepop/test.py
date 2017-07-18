# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 09:20:08 2012

@author: msnyde02
"""
import numpy as np
import random
import math
#S=4
#n_f=np.zeros(shape=(S,S))
#
#
#n_f[0,0]=500
#print n_f
#for i in range(0,S-1):
#    j=0
#    while (i>=0):
#        n_f[i+1,i+1]=n_f[i,i]
#        i=i-1
#    n_f[0,0]=random.randint(0, 100)
#    print n_f
# 
#import csv   
##data = csv.reader(open('\\AA.AD.EPA.GOV\\ATH\\USERS\\A-M\\msnyde02\\Net MyDocuments\\Dropbox\\AppPest\\beepop\\athens_weather.csv'))
#data = csv.reader(open('C:/temp/athens_weather.csv'))
#
#jday = []
#precip = []
#temp = []
#wspeed = []
#day_light = []
#for row in data:
    #jday.append(float(row[0]))
    #precip.append(float(row[1]))  
    #temp.append(float(row[2]))
    #wspeed.append(float(row[3]))
    #day_light.append(float(row[4]))
#
#print wspeed


#N = (math.log((7 * .001) + 1)) * 0.672
#print N

adults = np.zeros((5, 5))
adults[0,1] = 20
adults[1,2] = 30
#print adults
#adults = np.roll(adults, 1, axis = 1)
#adults = np.roll(adults, 1, axis = 0)
#print adults
adults[1:5, 1:5] = adults[0:4, 0:4]

drones = np.zeros((5, 5))
drones[0,0] = 2
drones[0,1] = 3
drones[:,4] = 100
print drones

drones_t=np.roll(drones, 1, axis = 1)
drones_t=np.roll(drones_t, 1, axis = 0)
drones_t[:,0]=0
drones_t[0,:]=0
print drones_t
drones = drones_t
#
#drones_t[0,i]=adults[9,i]
#print drones_t

#for i in range(1,365,1):
#    if i == 1:
#        nt = 7
#        print nt
#    else:
#        nt = 3
#        print nt
#    pop_size = nt * 2
#    print pop_size
#        





