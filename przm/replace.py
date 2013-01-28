'''
Created on May 22, 2012

@author: th
'''
import os
import linecache
import fileinput



#old=linecache.getline('C:/Users/th/Dropbox/com/MS1Ctt-P-temp.INP', 96)
#
#print(old)
#old1=old.replace(old[2:8],new)
#print(old1)
#
#f=open('C:/Users/th/Dropbox/com/MS1Ctt-P-temp.INP','w')
#f.write(old1)
#f.close()
#
##print(old)
#print(old)

 

#f=open('C:/Users/th/Dropbox/com/MS1Ctt-P-temp.INP','r+')
#lines=f.readlines()
#x = lines[95]
#print(x)
#f.close()
#
##replace
#f1=open('C:/Users/th/Dropbox/com/MS1Ctt-P-temp.INP')
#con = f1.read()
#print con
#con1 = con.replace(x[2:8],new)
#print con1
#f1.close()
#
#
##write
#f2 = open('C:/Users/th/Dropbox/com/MS1Ctt-P-temp.INP', 'w')
#f2.write(con1)
#f2.close()


#
#with open('C:/Users/th/Dropbox/com/MS1Ctt-P-temp.INP','r+') as f:
#    lines=f.readlines()
#    x = lines[95]
#    x = x.replace(x[2:8],new)
#    f.write(x)
#    f.close()

#    YY1=YY1+1
#    YY=YY+i
#    i=i+1
    
#print(x)
#x=x.replace(x[2:8],new)
#print(x)
#
#f.seek(96,0)
#f.write(x)
#f.close()
#for line in fileinput.FileInput('C:/Users/th/Dropbox/com/MS1Ctt-P-temp.INP', inplace=1):
#    line=line.replace(x,new)

#f.write(x)
#f.close()


#def replace_line(file_name, line_num, col_s, col_e, text):
#    lines = open(file_name, 'r').readlines()
#    temp=lines[line_num]
#    temp = temp.replace(temp[col_s:col_e],text)
#    lines[line_num]=temp
#    out = open(file_name, 'w')
#    out.writelines(lines)
#    out.close()
#
#YY1=61
#MM='04'
#DD='25'
#for i in range (95, 125):
#
#
##    new="  "+MM+DD+str(YY1)+'  0 2 4.001.0000.9500.0500\n'
#    new="  "+MM+DD
#    new1='0 2 4.001.0000.9500.0500\n'
#    replace_line('C:/Users/th/Dropbox/terr_models/EXPRESS/projects/Forchlorfenuron/MS1Ctt-P.INP', i, 0,6, new)
#    replace_line('C:/Users/th/Dropbox/terr_models/EXPRESS/projects/Forchlorfenuron/MS1Ctt-P.INP', i, 10,100, new1)
    
    
def del_line(file_name, line_s, line_e):
    line = open(file_name, 'r')
    lines = line.readlines()
    line.close()
    del lines[line_s:line_e]
    
    fout= open(file_name, 'w')
    fout.writelines(lines) 
    fout.close() 


del_line('C:/Users/th/Desktop/2.INP', 129,132)
    
    
    
    
    
    
    



