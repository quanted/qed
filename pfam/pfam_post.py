'''
Created on Mar 13, 2013

@author: th
'''
import os
import re

cwd='C:/Users/th/Desktop/pfam_PN3YIC'
os.chdir(cwd)

searchfile = open("pfam_out_ProcessedOutput.txt", "r")
i=0
for line in searchfile:
    if "Event#" in line: 
        line_start1=i+2
    if "Maximum released" in line:
        line_end1=i-2
    if "chemical id" in line: 
        line_start2=i+2
    if " ********" in line: 
        line_end2=i-1
    i=i+1
searchfile.close()

x_water=[]
x_water_level=[]
x_ben_tot=[]
x_ben_por=[]
x_date1=[]
x_date2=[]
x_re_v=[]
x_re_c=[]


fp = open("pfam_out_ProcessedOutput.txt")
for i, line in enumerate(fp):
    if (i >= line_start1) and (i <= line_end1):
        line = re.match("(.{5})(.{1})(.{10})(.{17})(.{13})(.{12})", line).groups()
        x_date1_temp = line[2]
        x_date1.append(x_date1_temp)
        x_re_v_temp = line[4]
        x_re_v.append(x_re_v_temp)
        x_re_c_temp = line[5]
        x_re_c.append(x_re_c_temp)
        
    if (i >= line_start2) and (i <= line_end2):
        line = re.match("(.{10})(.{8})(.{8})(.{12})(.{12})(.{12})(.{12})", line).groups()
        x_date2_temp = line[0]
        x_date2.append(x_date2_temp)
        x_water_level_temp = line[1]
        x_water_level.append(x_water_level_temp)
        x_ben_tot_temp = line[4]
        x_ben_tot.append(x_ben_tot_temp)
        x_ben_por_temp = line[5]
        x_ben_por.append(x_ben_por_temp)
        if line[3]=='   ---------':
            x_water_temp = '0'
        else:
            x_water_temp = line[3]
        x_water.append(x_water_temp)
fp.close()

x_date2_len = len(x_date2)
x_re_v_f = [0] * x_date2_len
x_re_c_f = [0] * x_date2_len

for i in x_date1:
    try:
        x_re_v_f[x_date2.index(i)] = x_re_v[x_date1.index(i)]
        x_re_c_f[x_date2.index(i)] = x_re_c[x_date1.index(i)]        
    except:
        x_re_v_f.append(x_re_v[x_date1.index(i)])
        x_re_c_f.append(x_re_c[x_date1.index(i)])
        


#print x_date1
#print x_re_v
#print x_re_c
#print x_date2
#print x_water_level
#print x_ben_tot
#print x_ben_por
#print x_re_v_f
#print x_re_c_f

print [float(i) for i in x_re_v_f]
#print [float(i) for i in x_re_c_f]

print len(x_re_v_f)
#print len(x_re_c_f)

