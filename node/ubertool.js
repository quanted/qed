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

    exports.getAllAquaConfigNames = function(callback)
    {
      db.collection('AquaticToxicity', function(err,collection){
        collection.find().toArray(function(err,all_aqua_data) {
          var aqua_config_names = [];
          for(i = 0; i < all_aqua_data.length; i++)
          {
            aqua_config_names.push(all_aqua_data[i].config_name);
          }
          callback(null,aqua_config_names);
        });
      });
    }

    exports.getAquaConfigData = function(aqua_config,callback)
    { 
      db.collection('AquaticToxicity', function(err,collection){
        collection.findOne({'config_name':aqua_config},function(err,aqua_config_data) {
          console.log(aqua_config_data);
          callback(null,aqua_config_data);
        });
      });
    }