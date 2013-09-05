var restify = require('restify');
var rabbitmq = require('./rabbitmq.js');
var mongodb = require('./mongodb.js');
var cas = require('./cas_mongo.js');
var formula = require('./formula.js');
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

var server = restify.createServer();
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
        user.getLoginDecision(user_id,json.password,function(err, decision_data){
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

server.post('/user/openid/login', function(req,res,next){
    var body = '';
    req.on('data', function (data)
    {
        body += data;
    });
    req.on('end', function ()
    {
        var json = JSON.parse(body);
        user.openIdLogin(json.openid, function(err, login_data){
            res.header("Access-Control-Allow-Origin", "*");
            res.header("Access-Control-Allow-Headers", "X-Requested-With");
            res.header('Access-Control-Allow-Methods', "GET");
            res.send(login_data);
        });
    });
});


server.post('/user/sessionid', function(req,res,next){
    var body = '';
    req.on('data', function (data)
    {
        body += data;
    });
    req.on('end', function ()
    {
        var json = JSON.parse(body);
        var user_id = json['user_id'];
        var session_id = json['session_id'];
        console.log("User id: " + user_id + " session id: " + session_id);
        user.checkUserSessionId(user_id, session_id, function(err, decision_data){
            res.header("Access-Control-Allow-Origin", "*");
            res.header("Access-Control-Allow-Headers", "X-Requested-With");
            res.header('Access-Control-Allow-Methods', "POST");
            console.log(decision_data);
            res.send(decision_data);
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

server.get('/casdata/:chemical_name', function(req, res, next){
    var chemical_name = req.params.chemical_name;
    console.log("Chemical Name: " + chemical_name);
    cas.getChemicalData(chemical_name, function(error,cas_data){
        if(cas_data != null)
        {
            res.header("Access-Control-Allow-Origin", "*");
            res.header("Access-Control-Allow-Headers", "X-Requested-With");
            res.send(cas_data);
        }
    });
});

server.get('/all-cas', function(req, res, next){
    cas.getAll(function(error,all_cas){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.send(all_cas);
    });
});

//Formula Services
server.get('/formula/:registration_num', function(req, res, next){
    var registration_num = req.params.registration_num;
    console.log("Registration Number: " + registration_num);
    formula.getFormulaData(registration_num, function(error,chemicals){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        console.log(chemicals)
        res.send(chemicals);
    });
});

server.get('/formulas/:pc_code', function(req, res, next){
    var pc_code = req.params.pc_code;
    console.log("PC Code: " + pc_code);
    formula.getFormulaDataFromPCCode(pc_code, function(error,chemical){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.send(chemical);
    });
});

server.get('/all_formula', function(req, res, next){
    formula.getAllFormulaData(function(error,formula_data){
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.send(formula_data);
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

server.get('/api', function(req, res, next){
    console.log("Describe REST API");
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    var apiDescription = "/user/login/:userid<br>"+
    "POST: Decides if the password passed in the json in the body of the request (key password) is valid for the user id as the last part of the url. Returns a json document with the decision(true/false), the sessionId, expiration date time. It adds a value to the passed cookie that tells google appengine that the user is valid to view protected pages.<br>"+
    "/user/registration/:user_id<br>"+
    "POST: registers a user given the user id as the last part of the url and the password and email address passed as arguments in the json request. Returns a json document with the sessionId, expiration date time.<br>"+
    "/user/openid/login<br>"+
    "POST: Using the openId passed in the json request, retrieves the userId, sessionId, and expiration date time for the sessionID. <br>"+
    "/user/sessionid<br>"+
    "POST: Attempts to validate a sessionId for a userId, both passed as arguments in the json request. Returns a json document with the decision(true/false), the sessionId, expiration date time.<br>"+
    "/batch_configs<br>"+
    "GET: Retrieves all the names for batch configurations in the system. No parameters are passed<br>"+
    "/batch<br>"+
    "POST: Submits a batch configuration to the asynchronous batching system via RabbitMQ.<br>"+
    "/batch_results/:batchId <br>"+
    "GET: Retrieves the results of an ubertool batch, based on the batchId passed in the URL. Returns a hierarchical JSON data.<br>"+
    "POST: Similar to GET request, except that it authenticates the userId along with an apiKey (both passed as arguments in the json documents).  If authenticated to a valid user, will retrieve results.<br>"+
    "/cas/:cas_num<br>"+
    "GET: Retrieves the chemical name associated with a CAS number<br>"+
    "/casdata/:chemical_name<br>"+
    "GET: Retrieves the CAS Number and PC Code<br>"+
    "/all-cas<br>"+
    "GET: Retrieves all of the CAS Numbers<br>"+
    "/formula/:registration_num<br>"+
    "GET: Retrieves formulation data based on a registration number. This service returns PC Percentage, Product Name, and PC Code in the json response.<br>"+
    "/formulas/:pc_code<br>"+
    "GET: Retrieves all of the formulations given a PC Code. The return is a json document containing an array of data, each data record contains Registration Number, PC Percentage, Product Name, and PC Code"+
    "/all_formula"+
    "GET: Retrieves all of the formulations available.  The return is a json document containing an array of data, each data record contains Registration Number, PC Percentage, Product Name, and PC Code"+
    "/ubertool/:config_type/config_names"+
    "GET: Retrieves all configurations for a given ubertool configuration (use, pest, aqua, eco, expo, terre, ubertool). Returns a json document, with a variety of properties."+
    "/ubertool/:config_type/:config"+
    "GET:  Retrieves a configuration for a given ubertool configuration (use, pest, aqua, eco, expo, terre, ubertool) based on a specific configuration ID (the last part of the url). Returns a json document, with a variety of properties."+
    "POST: Places an ubertool configuration into the mongo db, which can be referenced by ubertool configurations and is the basis for running an ubertool batch."+
    "/api-key"+
    "GET: Retrieves an API Key, though this is not stored to a user, just a means of generating an API key."+
    res.send(apiDescription);
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

server.listen(8887, function() {
  console.log('%s listening at %s', server.name, server.url);
});

/**
var credentials = {certificate: fs.readFileSync('ubertool_src/node/certs/server-cert.pem'),key: fs.readFileSync('ubertool_src/node/certs/server-key.pem')};
var httpsServer = restify.createServer(credentials);
httpsServer.listen(9443, function() {
  console.log('%s listening at %s', httpsServer.name, httpsServer.url);
});
**/

