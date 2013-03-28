'''
Created on May 17, 2012

@author: th
'''
import os
import csv


data = csv.reader(open('C:/Users/th/Desktop/trex2.csv'))
crop_type = []
max_rate = []


for row in data:
    crop_type_temp=row[0].lstrip()
    max_rate_temp=row[1]  
        
    crop_type.append(crop_type_temp)
    max_rate.append(max_rate_temp)

final_dict=zip(crop_type,max_rate)


print final_dict

