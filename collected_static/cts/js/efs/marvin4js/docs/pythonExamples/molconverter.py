import requests
import json

url="http://restdemo.chemaxon.com/rest-v0/util/calculate/stringMolExport"
conversionOptions = {
    "structure": "aspirin",
    "parameters": "mol"
}
headers = {'content-type': 'application/json'}
resultRaw = requests.post(url, data=json.dumps(conversionOptions), headers=headers)
result=resultRaw.text
print(result)
