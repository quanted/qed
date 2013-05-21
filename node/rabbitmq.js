var flow = require('nimble');
var http = require('http');
var amqp = require('amqp');
var URL = require('url');
var rabbitUrl = "localhost";
console.log("Starting ... AMQP URL: " + rabbitUrl);
var conn = amqp.createConnection({host: rabbitUrl});
conn.on('ready', setup);
var mongodb = require('./mongodb.js');

var port = process.env.VCAP_APP_PORT || 3000;

function setup() {
    console.log("Node.js connected to RabbitMQ!");
    exchange = conn.exchange('UbertoolBatchSubmissionExchange',options={type:'topic',durable:true});
}

exports.submitUbertoolBatchRequest = function (msg)
{
    var ubertools = msg['ubertools'];
    var batchId = msg['id'];
    console.log("SubmitUbertoolBatchRequest");
    console.log(msg);
    mongodb.createNewBatch(batchId,ubertools, function(error,batchId,ubertools){
        if(error == null)
        {
            submitNextUbertoolRun(ubertools,batchId,0,submitNextUbertoolRun); 
        }
    });
}

function submitNextUbertoolRun(ubertools,batchId,index,callback){
    if(index < ubertools.length)
    {
        console.log("Ubertools index: " + index);
        var ubertoolRunData = ubertools[index];
        ubertoolRunData['batchId'] = batchId;
        var config_name = ubertoolRunData['config_name'];
        mongodb.addEmptyUbertoolRun(config_name,batchId,ubertoolRunData,function(ubertoolRunData){ 
            exchange.publish('UbertoolBatchSubmissionQueue',{message:JSON.stringify(ubertoolRunData)});
            if(index + 1 < ubertools.length)
            {
                index++;
                callback(ubertools,batchId,index,callback);
            }
        });
    }
}

conn.addListener('ready', function () {
    var q = conn.queue('UbertoolBatchResultsQueue', {
        durable: true,
        autoDelete: false
    });

    // bind to a route
    q.bind('#');

    var messageHandler = function (body, headers, deliveryInfo) {
        // process message here
        var config_name = body.config_name;
        delete body.config_name;
        var batch_id = body.batchId;
        delete body.batchId;
        mongodb.updateUbertoolRun(config_name,batch_id,body, function(error, batch_data){
          console.log(batch_data);
        });
    };

    // subscribe to the queue
    q.subscribe({ack: true}, function(message) {
        messageHandler(message);
        q.shift();
    });
});
