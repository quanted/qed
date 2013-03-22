var http = require('http');
var amqp = require('amqp');
var URL = require('url');
var rabbitUrl = "localhost";
console.log("Starting ... AMQP URL: " + rabbitUrl);
var conn = amqp.createConnection({host: rabbitUrl});
conn.on('ready', setup);

var port = process.env.VCAP_APP_PORT || 3000;

function setup() {
  console.log("Node.js connected to RabbitMQ!");
  exchange = conn.exchange('UbertoolBatchExchange');
  //resultsQueue = conn.queue('UbertoolBatchResultsQueue');
  //resultsQueue.bind(exchange, '#');
}

exports.submitUbertoolBatchRequest = function (msg)
{
  console.info(msg);
  var ubertools = msg['ubertools'];
  var results = [];
  for(var index = 0; index < ubertools.length; index++)
  {
    console.log(JSON.stringify(ubertools[index]));
    exchange.publish('UbertoolBatchSubmissionQueue',{message:JSON.stringify(ubertools[index])});
   /**
    resultsQueue.subscribe(function(msg){
      results.append(msg);
    });
  **/
  }
  return results;
}
