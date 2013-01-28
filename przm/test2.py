# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:45:53 2012

@author: MSnyder
"""
#import sys
import csv

data = csv.reader(open('/Users/MSnyder/Dropbox/apppest/przm/slope1_csv1.csv'))
id1 = []
distance = []
elevation = []
for row in data:
    id1.append(float(row[0]))
    distance.append(float(row[1]))  
    elevation.append(float(row[2]))

slope=[0]*(len(id1))

for i in range(0,len(id1)-1):
    j=1
    up_ele=elevation[i]
    up_dis=distance[i]
    low_ele=elevation[i+j]
  
    if (up_ele-low_ele)>=0.5:
        while (i+j<len(id1)-1)&(up_ele-elevation[i+j]<3):
            j=j+1
            
        low_dis=distance[i+j]
        low_ele=elevation[i+j]
        slope[i]=float(up_ele-low_ele)/abs(up_dis-low_dis)
   
#print slope  
for i in range(len(slope)-1):
    if slope[i]!=0:
        j=slope[i]
    else:
        slope[i-1]=j
            
#print type(slope)       
#print slope
        
#print row
file2 = open('out1.csv', 'wb')
file1 = csv.writer(file2, dialect='excel')

out_data=zip(id1, distance, elevation, slope)
print out_data
for row in out_data:
    file1.writerow(row)
#    file1.writerow([distance][i])
    #file1.writerow(elevation)
    #file1.writerow(slope)
#file2.close()    
#all =id1+distance+elevation+slope
#print all[1]
#csv_writer = csv.writer(sys.stdout, delimiter='\t')
#csv_writer.writerows(all)
