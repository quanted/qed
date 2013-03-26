var Db = require('mongodb').Db,
  Connection = require('mongodb').Connection,
  Server = require('mongodb').Server,
  ObjectId = require('mongodb').ObjectId,
  Timestamp = require('mongodb').Timestamp;

var host = process.env['MONGO_NODE_DRIVER_HOST'] != null ? process.env['MONGO_NODE_DRIVER_HOST'] : 'localhost';
var port = process.env['MONGO_NODE_DRIVER_PORT'] != null ? process.env['MONGO_NODE_DRIVER_PORT'] : Connection.DEFAULT_PORT;

console.log("Connecting to " + host + ":" + port);
var db = new Db('ubertool', new Server(host, port, {}), {native_parser:true});

db.open(function(err, db) {
  console.log('Opened MongoDb connection.');
});

exports.createNewBatch = function(batch_id, data)
{
  db.collection('Batch', function(err,collection){
    collection.insert({batchId:batch_id,ubertool_runs:{}});
  });
}

exports.updateUbertoolRun = function(config_name,batch_id,data)
{
  db.collection('Batch', function(err,collection){
    collection.findOne({batchId:batch_id}, function(err, batch) {
      if(batch != null) {
        var isCompleted = true;
        var ubertool_runs = batch.ubertool_runs;
        if(ubertool_runs != null && Object.keys(ubertool_runs).length != 0)
        {
          for(var ubertool_run in ubertool_runs)
          {
            var tempIsCompleted = updateUbertoolRun(batch,ubertool_runs[ubertool_run],config_name,data);
            isCompleted = isCompleted ? tempIsCompleted: isCompleted;
          }
        } else {
          addNewUbertoolRunToBatch(batch,collection,config_name);
          var ubertool_runs = batch.ubertool_runs;
          var isCompleted = true;
          if(ubertool_runs != null)
          {
            for(var ubertool_run in ubertool_runs)
            {
              var tempIsCompleted = updateUbertoolRun(batch,ubertool_run,config_name,data);
              isCompleted = isCompleted ? tempIsCompleted: isCompleted;
            }
          }
        }
        if(isCompleted)
        {
          var objId = batch._id;
          var createdTimestamp = objId.getTimestamp();
          batch.completed = createdTimestamp;
        }
        collection.save(batch);
      } else {
        createBatch(batch_id,collection);
        collection.findOne({batchId:batch_id}, function(err, batch) {
          addNewUbertoolRunToBatch(batch,collection,config_name);
        });
      }
    });
  });
}

function updateUbertoolRun(batch,ubertool_run,config_name,data )
{
  var isCompleted = true;
  var ubertool_run_config_name = ubertool_run['config_name'];
  if(ubertool_run_config_name == config_name)
  {
    var ubertoolRunData = {};
    var objId = batch._id;
    var ubertoolCompleted = objId.getTimestamp();
    ubertoolRunData.config_name = config_name;
    if(data != null)
    {
      ubertoolRunData.data = data;
      ubertoolRunData.completed = ubertoolCompleted;
    }
    else {
      ubertoolRunData.data = null;
      ubertoolRunData.completed = false;
      isCompleted = false;
    }
    ubertool_run[config_name] = ubertoolRunData;
  } else {
    var ubertoolRunCompleted = ubertool_run.completed;
    if(ubertoolRunCompleted == null || ubertoolRunCompleted == false)
    {
      isCompleted = false;
    }
  }
  return isCompleted;
}

function createBatch(batch_id,collection)
{
  collection.insert({batchId:batch_id,ubertool_runs:{}});
  collection.findOne({batchId:batch_id}, function(err, batch) {
    if(batch != null) {
      var objId = batch._id;
      var createdTimestamp = objId.getTimestamp();
      batch.created = createdTimestamp;
      collection.save(batch);
    }
  });
}

function addNewUbertoolRunToBatch(batch,collection,config_name)
{
  var ubertool_run = {}
  var objId = batch._id;
  var createdTimestamp = objId.getTimestamp();
  ubertool_run.created = createdTimestamp;
  ubertool_run.config_name = config_name;
  var ubertool_runs = {};
  ubertool_runs[config_name] = ubertool_run;
  batch.ubertool_runs = ubertool_runs;
  collection.save(batch);
}
