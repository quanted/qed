import arcpy
import re
import csv

# set workspace environment
arcpy.env.workspace = "F:\\EPA_ES_Mapper\\NatureServe\\Fish\\Shapefiles\\"

featureclasses = arcpy.ListFeatureClasses()


f = open("NSF.txt", "wb")

for fc in featureclasses:
    varname = fc[:-4]
    nameSplit1 = re.split('_',fc[:-4])[0]
    nameSplit2 = re.split('_',fc[:-4])[1]
    name = fc[:-4]+','+nameSplit1+','+nameSplit2
    w = csv.writer(f,delimiter = ',')
    w.writerows([name.split(',')])
f.close()

print "done!"
    

    
    
    
