import requests
import json
import time
from multiprocessing import Process, Queue

baseUrl="http://restdemo.chemaxon.com/rest-v0/"

monitorUrl=baseUrl+"monitor/"
dataUrl=baseUrl+"data/"

def fileImport(responseChanel, fileName, tableName, monitorID):
    databaseName="sample"
    url=dataUrl+databaseName
    file = {'file': (fileName, open(fileName, 'rb'))}
    formData = {'tableName': tableName, 'monitor':monitorID, 'name':fileName}
    responseChanel.put(requests.post(url, data=formData, files=file).json())
    
if __name__ == "__main__":
    monitorID = requests.post(monitorUrl).json()
    fileName="examples.mrv"
    tableName="probe1"
    responseChanel = Queue()
    proc = Process(target=fileImport, args=(responseChanel, fileName, tableName, monitorID))
    proc.start()
    monRes = requests.get(monitorUrl+monitorID).json()
    state=monRes["state"]
    while state!="FINISHED" and not (state=="CREATED" and not proc.is_alive()):
        monRes = requests.get(monitorUrl+monitorID).json()
        state=monRes["state"]
        if state=="CREATED":
            progress=0
        else:
            progress=monRes["data"]["successful"]
        print(state+" - successful imports:"+str(progress))
        time.sleep(0.2)
    response=responseChanel.get()
    if "errorMessage" in response:
        print("Error: "+response["errorMessage"])
    else:
        print("Successful Import into table: "+response["table"]["tableName"])
    proc.join()
