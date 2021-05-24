import requests
import json

baseUrl="http://restdemo.chemaxon.com/rest-v0/"
searchUrl=baseUrl+"data/sample/table/ChEBI_lite_3star/search"
detailUrl=baseUrl+"data/sample/table/ChEBI_lite_3star/detail/"
searchOptions = {
	"searchOptions": {
		"queryStructure": "c1ccccc1",
		"searchMode": "SUBSTRUCTURE"
	},
	"filter": {
		"simpleConditions": "cd_molweight;lt;500",
		"orderBy": "cd_id"
	},
	"paging": {
		"offset": 0,
		"limit": 10
	},
	"display": {

		"include": ["cd_id", "cd_molweight", "logp", "don", "acc"],

		"additionalFields": {
                    "logp": "chemicalTerms(logp)",
                    "don": "chemicalTerms(donorCount)",
                    "acc": "chemicalTerms(acceptorCount)"
		}
	}
}
detailOptions = {
	"include": ["cd_id", "cd_molweight", "format", "hbda"],
       "pluginParameters":{
#		"logP": {
#    "showIncrements": True,
#    "method": "WEIGHTED",
#    "wVG": 1.0,
#    "wKLOP": 1.0,
#    "wPHYS": 1.0,
#    "CI": 0.1,
#    "NaK": 0.1,
#    "considerTautomerization": False
#},
"hbda":
{
    "pHLower": 0,
    "pHUpper": 14, 
    "pHStep": 0.1, 
    "excludeSulfur": True, 
    "excludeHalogens": True, 
    "displayMajorMicrospecies": False, 
    "pH": 7.4
}
	}
}
headers = {'content-type': 'application/json'}
resultRaw = requests.post(searchUrl, data=json.dumps(searchOptions), headers=headers)
result=resultRaw.json()
for row in result["data"]:
    print(row)
    if (row["acc"]<=2) and (row["don"]<=3) and (row["logp"]<=5):
        detailRaw = requests.post(detailUrl+str(row["cd_id"]), data=json.dumps(detailOptions), headers=headers)
        detail=detailRaw.json()
        print("OK: "+detail["format"]["smiles"])
    else:
        print("Failed")
            
