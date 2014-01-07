'''
Created on May 17, 2012

@author: th
'''
import os
import csv


data = csv.reader(open('F:/EPA_ES_Mapper/NatureServe/Fish/NSF.csv'))
code = []
show = []

for row in data:
    code_temp=row[0]
    show_temp_1=row[1]  
    show_temp_2=row[2]  

        
    code.append(code_temp)
    show.append(show_temp_1+' '+show_temp_2)

#print code
#print show

choice=tuple(zip(code,show))

print choice

f = open('F:/EPA_ES_Mapper/NatureServe/Fish/NSF_for_esmapping_db.txt','wb')

f.write(str(choice))

f.close()

print 'cvs to txt is done!'

#reference
# https://s3.amazonaws.com/esmapping_kmz/nsf/Acantharchus_pomotis.kmz

