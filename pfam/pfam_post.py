'''
Created on Mar 13, 2013

@author: th
'''
import os

cwd='C:/Users/th/Desktop/pfam_30OQOW'
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
fp = open("pfam_out_ProcessedOutput.txt")
for i, line in enumerate(fp):
    if (i >= line_start) and (i <= line_end):
        line = line.split('  ')
#        print line[3]
        if line[3]==' ---------':
            x_water_temp = '0'
        else:
            x_water_temp = line[3]
        x_water.append(x_water_temp)
fp.close()

print x_water


print [float(i) for i in x_water]



