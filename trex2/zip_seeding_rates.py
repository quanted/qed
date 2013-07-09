import csv

data = csv.reader(open('D:/Dropbox/ubertool_src/trex2/trex2_seeding.csv'))
crop = []
rate = []


for row in data:
    crop_temp=row[0]#.strip()
    rate_temp=row[1]  
        
    crop.append(crop_temp)
    rate.append(rate_temp)

final=tuple(zip(rate, crop))
print final