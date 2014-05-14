# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 09:20:08 2012

@author: msnyde02
"""
import numpy as np
import random
import os
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
import csv   
path0=os.path.dirname(__file__)
print path0

data = csv.reader(open(path0+'\\athens_weather.csv'))

jday = []
precip = []
temp = []
wspeed = []
day_light = []
for row in data:
    jday.append(float(row[0]))
    precip.append(float(row[1]))  
    temp.append(float(row[2]))
    wspeed.append(float(row[3]))
    day_light.append(float(row[4]))

print wspeed

