from stompy.simple import Client
import sys
import json
import pickle
import logging
sys.path.append("terrplant")
import terrplant_model
from terrplant_batch_runner import TerrPlantBatchRunner
terrPlantRunner = TerrPlantBatchRunner()

logger = logging.getLogger("BatchWorker")
    
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
    
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii')
    return dict(map(ascii_encode, pair) for pair in data.items())    

def combineUbertoolProperties(ubertool):
    combined_ubertool_props = {}
    for key in ubertool:
        print key
        if key == "config_name":
            logger.info("Adding config key: " + key)
            combined_ubertool_props["ubertool-config-name"] = ubertool[key]
        elif key == "batchId":
            logger.info("Adding batchId: " + key)
            combined_ubertool_props["batchId"] = ubertool[key]
        else:
            ubertool_config = ubertool[key]
            for config_key in ubertool_config:
                if not config_key == "config_name":
                    logger.info(config_key)
                    combined_ubertool_props[config_key] = ubertool_config[config_key]
    return combined_ubertool_props
    
def processUbertoolBatchRunsIntoBatchModelRun(ubertool):
    logger.info("Starting Ubertool Asynchronous Distributed Batching")
    #combined_ubertool_props = {}
    #combined_ubertool_props = combineUbertoolProperties(ubertool)
    #ubertool_id = combined_ubertool_props["config_name"]
    ubertool_result = {}
    ubertool_result = terrPlantRunner.runTerrPlantModel(ubertool,ubertool_result)
    logger.info("Ubertool Results:")
    logger.info(ubertool_result)
    #ubertool_result = sipRunner.runSIPModel(ubertool,ubertool_result)
    #perform on all other eco models
    return ubertool_result
    
def ioloop():
	while continueRunning:
		message = stomp.get(block=True)
		data = json.loads(message.body, object_hook=ascii_encode_dict)
		messageData = data['message']
		messageData = convert(messageData)
		messageData = json.loads(messageData)
		results_data = None
		ubertool_config_name = messageData['config_name']
		if 'batchId' in messageData:
			batch_id = messageData['batchId']
			results = processUbertoolBatchRunsIntoBatchModelRun(messageData)
			results['config_name'] = ubertool_config_name
			results['batchId'] = batch_id
	    	print results
	    	results_data = json.dumps(results)
	    	stomp.put(results_data,"/queue/UbertoolBatchResultsQueue",persistent=True)
	    	stomp.ack(message)

stomp = Client()
stomp.connect(username="admin",password="admin")
stomp.subscribe("/queue/UbertoolBatchSubmissionQueue")
continueRunning = True

try:
	ioloop()    
except KeyboardInterrupt:
    stomp.unsubscribe("/queue/UbertoolBatchSubmissionQueue")
    stomp.disconnect()