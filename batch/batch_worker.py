import pika
import sys
import json
import pickle
import logging
sys.path.append("terrplant")
import terrplant_model
from terrplant_batch_runner import TerrPlantBatchRunner
terrPlantRunner = TerrPlantBatchRunner()
#sys.path.append("sip")
#import sip_model
#from sip_batch_runner import SIPBatchRunner
#sipRunner = SIPBatchRunner()

logger = logging.getLogger("BatchWorker")

# Create a global channel variable to hold our channel object in
channel = None
    
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

# Step #2
def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    # Open a channel
    connection.channel(on_channel_open)
    logger.info("On Connected")

# Step #3
def on_channel_open(new_channel):
    """Called when our channel has opened"""
    logger.info("On Channel Open")
    global channel,results_channel
    channel = new_channel
    channel.queue_declare(queue="UbertoolBatchSubmissionQueue", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)
    results_channel = new_channel
    results_channel.queue_declare(queue="UbertoolBatchResultsQueue", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)

# Step #4
def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
    logger.info("On Queue Declare")
    channel.basic_consume(handle_delivery, queue='UbertoolBatchSubmissionQueue')

# Step #5
def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    logger.info("Handling message delivery")
    print body
    channel.basic_ack(delivery_tag = method.delivery_tag)
    data = json.loads(body, object_hook=ascii_encode_dict)
    messageData = data['message']
    messageData = convert(messageData)
    messageData = json.loads(messageData)
    results_data = None
    #print messageData
    ubertool_config_name = messageData['config_name']
    if 'batchId' in messageData:
        batch_id = messageData['batchId']
        results = processUbertoolBatchRunsIntoBatchModelRun(messageData)
        results['config_name'] = ubertool_config_name
        results['batchId'] = batch_id
        print results
        results_data = json.dumps(results)
    msg_props = pika.BasicProperties()
    msg_props.content_type = "application/json"
    msg_props.durable = False
    results_channel.basic_publish(exchange="UbertoolBatchResultsExchange",routing_key='#',body=results_data,properties=msg_props)
    
# Step #1: Connect to RabbitMQ using the default parameters
parameters = pika.ConnectionParameters()
connection = pika.SelectConnection(parameters, on_connected)

try:
    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()