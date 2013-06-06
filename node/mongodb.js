    var flow = require('nimble');
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
          console.log("Getting Batch Names");
          for(var i=0; i < items.length; i++)
          {
            var item = items[i];
            completedBatchNames[item.batchId]=item.completed.toString();
          }
          console.log(completedBatchNames);
          callback(null,completedBatchNames);
        });
      });
    }


    exports.getBatchResults = function(batch_id,callback)
    { 
      db.collection('Batch', function(err,collection){
        collection.findOne({batchId:batch_id},function(err,batch) {
          console.log("getBatchResults");
          console.log(batch);
          callback(null,batch);
        });
      });
    }

    exports.createNewBatch = function(batch_id, data,callback)
    {
      db.collection('Batch', function(err,collection){
        collection.insert({batchId:batch_id,ubertool_data:{}});
        collection.findOne({batchId:batch_id}, function(err, batch) {
            if(batch != null)
            {
              var createdTime = new Date();
              batch.created = createdTime.toString();
              collection.save(batch);
            }
            callback(null,batch_id,data);
        });
      });
    }

    exports.addEmptyUbertoolRun = function(config_name,batch_id,ubertoolRunData,callback)
    {
        db.collection('Batch', function(err,collection){
            collection.findOne({batchId:batch_id}, function(err, batch) {
                console.log("addEmptyUbertoolRun  ");
                var ubertool_run = {};
                var createdTime = new Date();
                ubertool_run.created = createdTime.toString();
                ubertool_run.config_name = config_name;
                ubertool_run.config_properties = ubertoolRunData;
                var ubertool_data = batch.ubertool_data;
                console.log('Before - ubertool_data: ' + ubertool_data);
                if(ubertool_data == null)
                {
                    ubertool_data = {};
                }
                ubertool_data[config_name] = ubertool_run;
                console.log('After - ubertool_data: ' + ubertool_data);
                batch.ubertool_data = ubertool_data;
                batch.created = createdTime.toString();
                collection.save(batch);
                console.log(batch);
                callback(ubertoolRunData);
            });
        });
    }

    exports.updateUbertoolRun = function(config_name,batch_id,data,callback)
    {
        db.collection('Batch', function(err,collection){
            collection.findOne({batchId:batch_id}, function(err, batch) {
                updateUbertoolBatch(batch,data,config_name,collection, function(err, batch){
                    callback(batch);
                });       
            });
        });
    }

    function updateUbertoolBatch(batch, data, config_name,collection,callback)
    {
        console.log("Finding One batch for update.");
        console.log(batch);
          
        var isCompleted = false;
        if(ubertool_data in batch)
        {
            var ubertool_data = batch.ubertool_data;
            for(var ubertool_run in ubertool_data)
            {
                var tempIsCompleted = updateCompletedUbertoolRun(collection,batch,ubertool_data[ubertool_run],config_name,data)
                if(!isCompleted && tempIsCompleted)
                {
                    isCompleted = true;
                }
            }
            if(isCompleted)
            {
                var completedTime = new Date();
                batch.completed = completedTime.toString();
            }
            collection.save(batch);
            callback(batch);
        }
    }

    function updateCompletedUbertoolRun(collection,batch,ubertool_run,config_name,data )
    {
        var isCompleted = true;
        var ubertool_run_config_name = ubertool_run.config_name;
        console.log("updateUbertoolRun: " + ubertool_run_config_name + " config_name: " + config_name);
        if(ubertool_run_config_name == config_name)
        {
            console.log("Completed ubertool run: " + ubertool_run_config_name);
            for(var datum in data)
            {
                ubertool_run[datum] = data[datum];
            }
            var completedTime = new Date();
            ubertool_run.completed = completedTime.toString();
            collection.save(batch);
        } else {
            var ubertoolRunCompleted = ubertool_run.completed;
            if(ubertoolRunCompleted == null)
            {
                isCompleted = false;
            }
            console.log("Ubertool run: " + ubertool_run_config_name + " completion status: " + isCompleted);
        }
        return isCompleted;
    }
