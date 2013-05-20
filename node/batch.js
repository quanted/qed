var restify = require('restify');
var rabbitmq = require('./rabbitmq.js');
var mongodb = require('./mongodb.js');
var cas = require('./cas_mongo.js');
var ubertool = require('./ubertool.js');
var flow = require('nimble');

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

server.post('/ubertool/batch/:config', function(req, res, next){
    var config_type = req.params.config_type;
    var config = req.params.config;
    var body = '';
    var json = '';
    req.on('data', function (data)
    {
        body += data;
    });
    req.on('end', function ()
    {
        json = JSON.parse(body);
        console.log("POST for Configuration Name: " + config + " config type: " + config_type + " json data: " + json);
    });
});

//Ubertool Services
server.get('/ubertool/:config_type/config_names', function(req, res, next){
    var config_type = req.params.config_type;
    ubertool.getAllConfigNames(config_type,function(error,config_names){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.send(config_names);
    });
});

server.get('/ubertool/:config_type/:config', function(req, res, next){
    var config_type = req.params.config_type;
    var config = req.params.config;
    console.log("GET for Configuration Name: " + config);
    ubertool.getConfigData(config_type,config, function(error,config_data){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.send(config_data);
    });
});

server.post('/ubertool/:config_type/:config', function(req, res, next){
    var config_type = req.params.config_type;
    var config = req.params.config;
    var body = '';
    var json = '';
    req.on('data', function (data)
    {
        body += data;
    });
    req.on('end', function ()
    {
        json = JSON.parse(body);
        console.log("POST for Configuration Name: " + config + " config type: " + config_type + " json data: " + json);
        ubertool.addUpdateConfig(config_type,config,json, function(error, results)
        {
            res.send(results);
        });
    });
});

server.listen(8887, function() {
  console.log('%s listening at %s', server.name, server.url);
});
