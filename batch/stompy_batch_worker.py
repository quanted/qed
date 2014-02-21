from twisted.internet import defer, reactor
from stompest.config import StompConfig
from stompest.async import Stomp
from stompest.async.listener import ReceiptListener,SubscriptionListener
from stompest.protocol import StompSpec

import sys
import json
import pickle
import logging
sys.path.append("terrplant")
import terrplant_model
from terrplant_batch_runner import TerrPlantBatchRunner
terrPlantRunner = TerrPlantBatchRunner()
sys.path.append("sip")
import sip_model
from sip_batch_runner import SIPBatchRunner
sipRunner = SIPBatchRunner()
# sys.path.append("stir")
# import stir_model
# from stir_batch_runner import StirBatchRunner
# stirRunner = STIRBatchRunner()
sys.path.append("dust")
import dust_model
from dust_batch_runner import DUSTBatchRunner
dustRunner = DUSTBatchRunner()
sys.path.append("trex2")
import trex2_model
from trex2_batch_runner import TREX2BatchRunner
trex2Runner = TREX2BatchRunner()
SUBMISSION_QUEUE = '/queue/UbertoolBatchSubmissionQueue'
RESULTS_QUEUE = '/queue/UbertoolBatchResultsQueue'
HOST = 'localhost'
PORT = '61613'

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
    ubertool_result = sipRunner.runSIPModel(ubertool,ubertool_result)
    logger.info("Ubertool Results:")
    logger.info(ubertool_result)
    ubertool_result = stirRunner.runSTIRModel(ubertool,ubertool_result)
    logger.info("Ubertool Results:")
    logger.info(ubertool_result)
    ubertool_result = dustRunner.runDUSTModel(ubertool,ubertool_result)
    logger.info("Ubertool Results:")
    logger.info(ubertool_result)
    ubertool_result = trex2Runner.runTREX2Model(ubertool,ubertool_result)
    logger.info("Ubertool Results:")
    logger.info(ubertool_result)
    #perform on all other eco models
    return ubertool_result
    
# def ioloop():
# 	while continueRunning:
# 		message = stomp.get(block=True)
#         print "we have a message!"
#         data = json.loads(message.body, object_hook=ascii_encode_dict)
#         messageData = data['message']
#         messageData = convert(messageData)
#         messageData = json.loads(messageData)
#         results_data = None
#         ubertool_config_name = messageData['config_name']
#         if 'batchId' in messageData:
#             batch_id = messageData['batchId']
#             results = processUbertoolBatchRunsIntoBatchModelRun(messageData)
#             results['config_name'] = ubertool_config_name
#             results['batchId'] = batch_id
#             print results
#             results_data = json.dumps(results)
#             stomp.put(results_data,"/queue/UbertoolBatchResultsQueue",persistent=True)
#             stomp.ack(message)

def consume(self, client, frame):
    """
    NOTE: you can return a Deferred here
    """
    data = json.loads(frame.body)
    print data
    messageData = data['message']
    print messageData
    # messageData = convert(messageData)
    # messageData = json.loads(messageData)
    results_data = None
    ubertool_config_name = messageData['config_name']
    if 'batchId' in messageData:
        batch_id = messageData['batchId']
        results = processUbertoolBatchRunsIntoBatchModelRun(messageData)
        results['config_name'] = ubertool_config_name
        results['batchId'] = batch_id
        print results
        results_data = json.dumps(results)
        # stomp.put(results_data,"/queue/UbertoolBatchResultsQueue",persistent=True)
        # stomp.ack(message)

@defer.inlineCallbacks
def run():
    while(True):
        client = yield Stomp(config).connect()
        headers = {
            # client-individual mode is necessary for concurrent processing
            # (requires ActiveMQ >= 5.2)
            StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL,
            # the maximal number of messages the broker will let you work on at the same time
            'activemq.prefetchSize': '100',
        }
        client.subscribe(SUBMISSION_QUEUE, headers, listener=SubscriptionListener(consume))

config = StompConfig('tcp://'+HOST+':'+PORT)

print "stuff might be working"

run()

# stomp = Client()
# stomp.connect(username="admin",password="admin")
# stomp.subscribe("/queue/UbertoolBatchSubmissionQueue")
# continueRunning = True

# try:
# 	ioloop()    
# except KeyboardInterrupt:
#     stomp.unsubscribe(QUEUE)
#     stomp.disconnect()