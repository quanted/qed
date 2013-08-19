import logging
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client['ubertool']
chemicals = db.chemicals

file = open('../csvs/formulakeys.csv')


for line in file:
	line = line.rstrip("\n")
	line_data = line.split(',')
	regnum=line_data[0]
	pccode=line_data[1]
	pcpct=line_data[2]
	prodname=line_data[3]
	formula = {'regnum':regnum,'pccode':pccode,'pcpct':pcpct,'prodname':prodname}
	formula_id = chemicals.insert(formula)
	print formula_id
