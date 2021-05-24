import requests
import json

url="http://restdemo.chemaxon.com/rest-v0/data/sample/table/ChEBI_lite_3star/search"

paging = {"offset": 16, "limit": 20}

result=requests.get(url, params=paging)
table=result.json()['data']
for row in table:
	print("("+str(row['cd_id'])+")"+row['c_chebi_id']+": "+row['c_chebi_name'])
	
