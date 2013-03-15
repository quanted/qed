'''
Created on Mar 13, 2013

@author: th
'''
import os
import re

cwd='C:/Users/tao/Desktop/pfam_UI4YFR'
os.chdir(cwd)

searchfile = open("pfam_out_ProcessedOutput.txt", "r")
i=0
for line in searchfile:
    if "chemical id" in line: 
        line_start=i+2
    if " ********" in line: 
        line_end=i-1
    i=i+1
searchfile.close()

x_water=[]
x_date=[]
fp = open("pfam_out_ProcessedOutput.txt")
for i, line in enumerate(fp):
    if (i >= line_start) and (i <= line_end):
#        line = line.split('  ')
        line = re.match("(.{10})(.{8})(.{8})(.{12})(.{12})(.{12})(.{12})", line).groups()
        x_date_temp = line[0]
        x_date.append(x_date_temp)
        
        if line[3]=='   ---------':
            x_water_temp = '0'
        else:
            x_water_temp = line[3]
        x_water.append(x_water_temp)
fp.close()


    
#fp = open("pfam_out_ProcessedOutput.txt")
#for i, line in enumerate(fp):
#    if (i >= line_start) and (i <= line_end):
#        line = line.split()
#        x_date_temp = line[0]
#        x_date.append(x_date_temp)
#
#fp.close()

print x_water

print [float(i) for i in x_water]



