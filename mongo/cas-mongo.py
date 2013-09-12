import logging
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client['ubertool']
cas_data = db.CAS

file = open('../csvs/chemkeys.csv')


for line in file:
	line = line.rstrip("\n")
	line_data = line.split(',')
	pccode=line_data[0]
	casnum=line_data[1]
	pcname = ''
	if len(line_data) == 3:
		pcname=line_data[2]
	elif len(line_data) > 3:
		for index in range(2,len(line_data)):
			pcname += line_data[index] + " "
		pcname.strip("\n")
	cas = {'PCCode':pccode,'CASNumber':casnum,'ChemicalName':pcname}
	cas_id = cas_data.insert(cas)
	print cas_id