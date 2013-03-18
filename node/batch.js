var restify = require('restify');

function sayHello(req, res, next) {
  res.send('hello ');
}

function getAvailableBatchNames(req, res, next)
{
    console.log(req);
    res.send("Getting Available Batch Names.\n");
    return next();
}

function submitBatch(req, res, next)
{
    var body = '';
    req.on('data', function (data)
    {
        body += data;
    });
    //console.log(body);
    req.on('end', function ()
    {
        var json = JSON.parse(body);
        console.log(JSON.stringify(json)); 
    });
    res.send("Submitting Batch.\n");
}

function getBatchResults(req, res, next)
{
    console.log(req);
    res.send("Getting Batch Results.\n");
    return next();
}

var server = restify.createServer();
server.get('/batch_configs', getAvailableBatchNames);
server.post('/batch',submitBatch);
server.get('/batch_results',getBatchResults);

server.listen(8887, function() {
  console.log('%s listening at %s', server.name, server.url);
});