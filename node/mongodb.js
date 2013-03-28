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

exports.getBatchNames = function(callback)
{ 
  var completedBatchNames = {};
  db.collection('Batch', function(err,collection){
    collection.find({completed:{$exists:true}}).toArray(function(err,items) {
      for(var i=0; i < items.length; i++)
      {
        var item = items[i];
        completedBatchNames[item.batchId]=item.completed.toString();
      }
      callback(null,completedBatchNames);
    });
  });
}

exports.getBatchResults = function(batch_id,callback)
{ 
  db.collection('Batch', function(err,collection){
    collection.findOne({batchId:batch_id},function(err,batch) {
      //console.log(batch);
      var new_batch = {};
      new_batch.completed = batch.completed;
      new_batch.ubertool_data = batch.ubertool_data;
      new_batch.batchId = batch.batchId;
      callback(null,new_batch);
    });
  });
}

exports.createNewBatch = function(batch_id, data)
{
  db.collection('Batch', function(err,collection){
    collection.insert({batchId:batch_id,ubertool_data:{}});
    collection.findOne({batchId:batch_id}, function(err, batch) {
      var objId = batch._id;
      var createdTimestamp = objId.getTimestamp();
      batch.created = createdTimestamp;
      collection.save(batch);
    });
  });
}

exports.addEmptyUbertoolRun = function(config_name,batch_id)
{
  db.collection('Batch', function(err,collection){
    collection.findOne({batchId:batch_id}, function(err, batch) {
      console.log("addEmptyUbertoolRun  ");
      var ubertool_run = {};
      var objId = batch._id;
      var createdTimestamp = objId.getTimestamp();
      ubertool_run.created = createdTimestamp;
      ubertool_run.config_name = config_name;
      var ubertool_data = batch.ubertool_data;
      if(ubertool_data == null)
      {
        ubertool_data = {};
      }
      ubertool_data[config_name] = ubertool_run;
      batch.ubertool_data = ubertool_data;
      collection.save(batch);
    });
  });
}

exports.updateUbertoolRun = function(config_name,batch_id,data)
{

  db.collection('Batch', function(err,collection){
    collection.findOne({batchId:batch_id}, function(err, batch) {
      var isCompleted = true;
      var ubertool_data = batch.ubertool_data;
      for(var ubertool_run in ubertool_data)
      {
        var tempIsCompleted = updateUbertoolRun(collection,batch,ubertool_data[ubertool_run],config_name,data)
        isCompleted = isCompleted ? tempIsCompleted: isCompleted;
      }
      if(isCompleted)
      {
        var objId = batch._id;
        var createdTimestamp = objId.getTimestamp();
        batch.completed = createdTimestamp;
      }
      collection.save(batch);
    });
  });
}

function updateUbertoolRun(collection,batch,ubertool_run,config_name,data )
{
  var isCompleted = true;
  var ubertool_run_config_name = ubertool_run.config_name;
  console.log("updateUbertoolRun: " + ubertool_run_config_name);
  if(ubertool_run_config_name == config_name)
  {
    var objId = batch._id;
    var ubertoolCompleted = objId.getTimestamp();
    for(var datum in data)
    {
      ubertool_run[datum] = data[datum];
    }
//    ubertool_run.data = data;
    ubertool_run.completed = ubertoolCompleted;
    collection.save(batch);
  } else {
    var ubertoolRunCompleted = ubertool_run.completed;
    if(ubertoolRunCompleted == null || ubertoolRunCompleted == false)
    {
      isCompleted = false;
    }
  }
  return isCompleted;
}
