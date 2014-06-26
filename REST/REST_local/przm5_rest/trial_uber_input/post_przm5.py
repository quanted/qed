Year = []
Mon = []
Day = []
IRRG = []
PRCP = []
IRRG_sum = []
PRCP_sum = []

with open('test.zts') as f:
    next(f)
    next(f)
    next(f)
    for line in f:
        line = line.split()
        Year.append(int(line[0]))
        Mon.append(int(line[1]))
        Day.append(int(line[2]))
        IRRG.append(float(line[13]))
        PRCP.append(float(line[14]))

year_ind = [Year.index(i) for i in list(set(Year))]
year_ind.append(len(Year))

# print len(Year)
# print list(set(Year))
# print year_ind

for jj in range(len(year_ind)-1):
    # print jj
    # print year_ind[jj], year_ind[jj+1]
    PRCP_sum.append(sum(PRCP[year_ind[jj]:year_ind[jj+1]]))
    IRRG_sum.append(sum(IRRG[year_ind[jj]:year_ind[jj+1]]))
    PRCP_IRRG_sum = [x+y for (x, y) in zip(PRCP_sum, IRRG_sum)]

print len(PRCP_sum)
print (PRCP_sum)

# print IRRG_sum
# print PRCP_IRRG_sum

