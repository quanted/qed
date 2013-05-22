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

exports.getAllConfigNames = function(config_type,callback)
{
  var config_collection = '';
  if(config_type == 'aqua')
  {
    config_collection = 'AquaticToxicity';
  } else if(config_type == 'eco')
  {
    config_collection = 'EcosystemInputs';
  } else if(config_type == 'expo')
  {
    config_collection = 'ExposureConcentrations';
  } else if(config_type == 'pest')
  {
    config_collection = 'PesticideProperties';
  } else if(config_type == 'terre')
  {
    config_collection = 'TerrestrialToxicity';
  } else if(config_type == 'use')
  {
    config_collection = 'Use';
  } else if(config_type == 'ubertool')
  {
    config_collection = 'Ubertool';
  } 
  db.collection(config_collection, function(err,collection){
    collection.find().toArray(function(err,all_data) {
      var config_names = [];
      for(i = 0; i < all_data.length; i++)
      {
        config_names.push(all_data[i].config_name);
      }
      callback(null,config_names);
    });
  });
}

exports.getConfigData = function(config_type,config,callback)
{ 
  var config_collection = '';
  if(config_type == 'aqua')
  {
    config_collection = 'AquaticToxicity';
  } else if(config_type == 'eco')
  {
    config_collection = 'EcosystemInputs';
  } else if(config_type == 'expo')
  {
    config_collection = 'ExposureConcentrations';
  } else if(config_type == 'pest')
  {
    config_collection = 'PesticideProperties';
  } else if(config_type == 'terre')
  {
    config_collection = 'TerrestrialToxicity';
  } else if(config_type == 'use')
  {
    config_collection = 'Use';
  } else if(config_type == 'ubertool')
  {
    config_collection = 'Ubertool';
  } 
  db.collection(config_collection, function(err,collection){
    collection.findOne({'config_name':config},function(err,config_data) {
      callback(null,config_data);
    });
  });
}

exports.addUpdateConfig = function(config_type,config,json_data,callback)
{
  var config_collection = '';
  if(config_type == 'aqua')
  {
    config_collection = 'AquaticToxicity';
  } else if(config_type == 'eco')
  {
    config_collection = 'EcosystemInputs';
  } else if(config_type == 'expo')
  {
    config_collection = 'ExposureConcentrations';
  } else if(config_type == 'pest')
  {
    config_collection = 'PesticideProperties';
  } else if(config_type == 'terre')
  {
    config_collection = 'TerrestrialToxicity';
  } else if(config_type == 'use')
  {
    config_collection = 'Use';
  } else if(config_type == 'ubertool')
  {
    config_collection = 'Ubertool';
  }
  console.log(config_collection);
  console.log(config);
  //console.log(json_data);
  db.collection(config_collection, function(err,collection){
    collection.findAndModify({config_name:config}, {created: 1},
      json_data, {new:true, upsert:true, w:1},function(err,doc){
        console.log("added document");
        console.log(doc);
        callback(null,doc);
      });
  });
}