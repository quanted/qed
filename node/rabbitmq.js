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
  mongodb.createNewBatch(batchId,ubertools);
  var results = [];
  for(var index = 0; index < ubertools.length; index++)
  {
    var ubertoolRunData = ubertools[index];
    ubertoolRunData['batchId'] = batchId;
    var config_name = ubertoolRunData['config_name'];
    mongodb.updateUbertoolRun(config_name,batchId,null);
    exchange.publish('UbertoolBatchSubmissionQueue',{message:JSON.stringify(ubertools[index])});
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
        mongodb.updateUbertoolRun(config_name,batch_id,body);
    };

    // subscribe to the queue
    q.subscribe({ack: true}, function(message) {
        messageHandler(message);
        q.shift();
    });
});
