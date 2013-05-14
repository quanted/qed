var restify = require('restify');
var rabbitmq = require('./rabbitmq.js');
var mongodb = require('./mongodb.js');
var cas = require('./cas_mongo.js');
var ubertool = require('./ubertool.js');
var flow = require('nimble');

function sayHello(req, res, next) {
  res.send('hello ');
}

function submitBatch(req, res, next)
{
    console.log("Batch Submitted to Node.js server.");
    var body = '';
    req.on('data', function (data)
    {
        body += data;
    });
    //console.log(body);
    req.on('end', function ()
    {
        var json = JSON.parse(body);
        //console.log(JSON.stringify(json)); 
        var results = rabbitmq.submitUbertoolBatchRequest(json);
    });
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.send("Submitting Batch.\n");
}

function getBatchResults(req, res, next)
{
    //console.log(req);
    res.send("Getting Batch Results.\n");
    return next();
}

var server = restify.createServer();

//Batch REST Services
server.get('/batch_configs', function(req, res, next){
    mongodb.getBatchNames(function(error, batch_ids){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.send(batch_ids);
    });
});
server.post('/batch',submitBatch);
server.get('/batch_results/:batchId', function(req, res, next){
    var batchId = req.params.batchId;
    console.log("BatchId: " + batchId);
    mongodb.getBatchResults(batchId, function(error, batch_data){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.send(batch_data);
    });
});

//CAS Services
server.get('/cas/:cas_num', function(req, res, next){
    var cas_number = req.params.cas_num;
    console.log("Cas Number: " + cas_number);
    cas.getChemicalName(cas_number, function(error,chemical_name){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.send(chemical_name);
    });
});

server.get('/all-cas', function(req, res, next){
    cas.getAll(function(error,all_cas){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.send(all_cas);
    });
});

//Ubertool Services
server.get('/aqua/config_names', function(req, res, next){
    ubertool.getAllAquaConfigNames(function(error,config_names){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.send(config_names);
    });
});

server.get('/aqua/:aqua_config', function(req, res, next){
    var aqua_config = req.params.aqua_config;
    console.log("Aquatic Toxicity Configuration Name: " + aqua_config);
    ubertool.getAquaConfigData(aqua_config, function(error,aqua_config_data){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.send(aqua_config_data);
    });
});

server.listen(8887, function() {
  console.log('%s listening at %s', server.name, server.url);
});
