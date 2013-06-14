var restify = require('restify');
var rabbitmq = require('./rabbitmq.js');
var mongodb = require('./mongodb.js');
var cas = require('./cas_mongo.js');
var ubertool = require('./ubertool.js');
var utils = require('./utils.js');
var flow = require('nimble');
var user = require('./user.js');
var fs = require('fs');
var Cookies = require('cookies');

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

var credentials = {certificate: fs.readFileSync('certs/server-cert.pem'),key: fs.readFileSync('certs/server-key.pem')};
var server = restify.createServer(credentials);
server.listen(9443, function() {
  console.log('%s listening at %s', server.name, server.url);
});
server.use(restify.CORS());
server.use(restify.fullResponse());

server.post('/user/login/:userid', function(req, res, next){
    var user_id = req.params.userid;
    console.log('user id: ' + user_id);
    var body = '';
    req.on('data', function (data)
    {
        body += data;
    });
    req.on('end', function ()
    {
        json = JSON.parse(body);
        console.log(json);
        console.log('json: ' + json);
        console.log('password' + json.pswrd);
        user.getLoginDecision(user_id,json.pswrd,function(err, decision_data){
            res.header("Access-Control-Allow-Origin", "*");
            res.header("Access-Control-Allow-Headers", "X-Requested-With");
            res.header('Access-Control-Allow-Methods', "POST");
            if(decision_data.decision)
            {
                var acsid_string = "test="+decision_data.sid;
                console.log("acsid_string: " + acsid_string);
                res.header('Set-Cookie',acsid_string);
            }
            res.send(decision_data);
        });
    });
});

server.post('/user/registration/:user_id', function(req, res, next){
    var user_id = req.params.user_id;
    console.log('user id: ' + user_id);
    var body = '';
    req.on('data', function (data)
    {
        body += data;
    });
    req.on('end', function ()
    {
        json = JSON.parse(body);
        console.log(json);
        console.log('password: ' + json.pswrd);
        console.log('email address: ' + json.email_address);
        user.registerUser(user_id,json.pswrd,json.email_address,function(err, sid_data){
            res.header("Access-Control-Allow-Origin", "*");
            res.header("Access-Control-Allow-Headers", "X-Requested-With");
            res.header('Access-Control-Allow-Methods', "POST");
            res.send(sid_data);
        });
    });
});

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
        if(batch_data != null)
        {
            res.send(batch_data);
        } else {
            res.send("Problem returning results");
        }
    });
});

server.post('/batch_results/:batchId', function(req, res, next){
    var batchId = req.params.batchId;
    console.log("BatchId: " + batchId);
    var body = '';
    req.on('data', function (data)
    {
        body += data;
    });
    req.on('end', function ()
    {
        console.log("body: " + body);
        var json = JSON.parse(body);
        var user_id = json.user_id;
        var user_api_key = json.api_key;
        console.log("json user_id: " + user_id + " user_api_key: " + user_api_key);
        user.authenticateRestAccess(user_id,user_api_key,function(err,authenticated){
            console.log("authenticated: " + authenticated);
            if(authenticated){
                mongodb.getBatchResults(batchId, function(error, batch_data){
                    res.header("Access-Control-Allow-Origin", "*");
                    res.header("Access-Control-Allow-Headers", "X-Requested-With");
                    if(batch_data != null)
                    {
                        res.send(batch_data);
                    } else {
                        res.send("Problem returning results");
                    }
                });
            } else {
                console.log('User API Authentication failed');
                res.send("User: " + user_id + " passed an incorrect api key and cannot call this method.");
            }
        });
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

server.get('/api-key', function(req, res, next){
    console.log("GET for API Key");
    apiKey = utils.generateNewAPIKey();
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.send(apiKey);
});

server.on('MethodNotAllowed', unknownMethodHandler);

function unknownMethodHandler(req, res) {
  if (req.method.toLowerCase() === 'options') {
    var allowHeaders = ['Accept', 'Accept-Version', 'Content-Type', 'Api-Version'];

    if (res.methods.indexOf('OPTIONS') === -1) res.methods.push('OPTIONS');

    res.header('Access-Control-Allow-Credentials', true);
    res.header('Access-Control-Allow-Headers', allowHeaders.join(', '));
    res.header('Access-Control-Allow-Methods', res.methods.join(', '));
    res.header('Access-Control-Allow-Origin', req.headers.origin);

    return res.send(204);
  }
  else
    return res.send(new restify.MethodNotAllowedError());
}


