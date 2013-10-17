'''
Created on May 17, 2012

@author: th
'''
import os
import csv
#data = csv.reader(open('C:/Users/th/Dropbox/AppPest/PRZM/scenario_new.csv'))
#scenario = []
#station = []
#met = []
#inp = []
#run = []
#
#for row in data:
#    scenario_temp=row[0]
#    station_temp=row[1]  
#    met_temp=row[2]  
#    inp_temp=row[9]
#        
#    scenario.append(scenario_temp)
#    station.append(station_temp)
#    met.append(met_temp+'.DVF')
#    inp.append(inp_temp+'-P.INP')
#    run.append(inp_temp+'-P.RUN')
        
#sce_sce=tuple(zip(scenario,scenario))
#sce_stat=dict(zip(scenario,station))
#sce_met=dict(zip(scenario,met))
#sce_inp=dict(zip(scenario,inp))
#sce_run=dict(zip(scenario,run))
#print "type(sce_stat)=", (type(sce_stat))
#print "sce_sce=", (sce_sce)
#print "sce_stat=", (sce_stat)   
#print "sce_met=", (sce_met)
#print "sce_inp=", (sce_inp)
#print "sce_run=", (sce_run)

#read dates from 

#scan all the files names in a directory
#import glob
#a=glob.glob("C:/Users/th/Desktop/pool/*.INP")

data = csv.reader(open('C:/Users/th/Desktop/scenario_new.csv'))
scenario = []
station = []
met = []
inp = []
run = []
EMergence = []
MAturation = []
HArvest = []
PLanting = []

for row in data:
    scenario_temp=row[0]
    station_temp=row[1]  
    met_temp=row[2]  
    inp_temp=row[9]
        
    scenario.append(scenario_temp)
    station.append(station_temp)
    met.append(met_temp+'.DVF')
    inp.append(inp_temp+'-P.INP')
    run.append(inp_temp+'-P.RUN')
    

    file_name='C:/Users/th/Desktop/pool/'+row[9]+'-P.INP'
    lines = open(file_name, 'r').readlines()
    
    EMergence.append(lines[51][2:6])
    MAturation.append(lines[51][10:14])
    HArvest.append(lines[51][18:22])
    PLanting.append(lines[95][2:6])

sce_PLanting=dict(zip(scenario,PLanting))
sce_EMergence=dict(zip(scenario,EMergence))
sce_MAturation=dict(zip(scenario,MAturation))
sce_HArvest=dict(zip(scenario,HArvest))

print sce_PLanting
print sce_EMergence
print sce_MAturation
print sce_HArvest




#data = csv.reader(open('C:/Users/th/Desktop/NS.csv'))
#sc_name = []
#co_name = []
#co_num = []
#
#for row in data:
#    sc_name_temp=row[5]   
#    co_name_temp=row[6]  
#    co_num_temp=row[7]
#    
#    sc_name.append(sc_name_temp+' ('+co_name_temp+')')
#    co_num.append(co_num_temp)
#    
#sc_co=tuple(zip(co_num,sc_name))
#
#print sc_co

#sce_all=(zip(scenario,station,met,inp))



#####link station numbers and 


#for line in file("C:\Program Files (x86)\EXPRESS\stdmet\Full list of station.txt"):
#for line in file("C:/Users/th/Dropbox/AppPest/przm/Scenario.txt"):
#
#   line_s = line.split()
#   x_number1 = line_s[0]
#   #x_name1 = line[11:43]
#   x_number.append(x_number1)
  
   #x_number.append('w'+x_number1+'.txt')
   
   #x_name.append(str.strip(x_name1))
   
   #x_name1.append(x_name2)
   
#x=tuple(zip(x_number,x_name))

#f = open("ban.txt", "w")
#f.write(str(x))
#f.close()
#City_select = (('Select a city','Select a city'),('MS Cotton','MS Cotton'))

#print(type(City_select))

#print(type(x))
#print(x_number)



#print(mergedlist)   
#for i in range(len(x_number)):
#   print x[i]

#print (x_number)
#print (x_name)

####scan filenames in a folder######
#import glob
#import os
#os.chdir("C:\Program Files (x86)\EXPRESS\stdmet")
#for files in glob.glob("*.txt"):
#    print files
    
    
 
