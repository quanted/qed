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

    exports.getAll = function(callback)
    {
    	db.collection('CAS', function(err,collection){
    		collection.find().toArray(function(err,all_cas) {
    			var cas_nums_chem_names = [];
    			for(i = 0; i < all_cas.length; i++)
    			{
    				cas_nums_chem_names.push({"ChemicalName":all_cas[i].ChemicalName.substring(0,20),"CASNumber":all_cas[i].CASNumber})
    			}
    			callback(null,cas_nums_chem_names);
    		});
    	});
    }

    exports.getAllChemicalNames = function(callback)
    {
      getAll( function(err,cas_data){
        var utf8_cas_data = [];
        for(i = 0; i < cas_data.length; i++)
        {
          utf8_cas_data.push(cas_data[i].ChemicalName.substring(0,20));
        }
        callback(null,utf8_cas_data);
      })
    }

    exports.getChemicalName = function(cas_number,callback)
    { 
      db.collection('CAS', function(err,collection){
        collection.findOne({CASNumber:cas_number},function(err,cas) {
          console.log(cas);
          callback(null,cas.ChemicalName.substring(0,20));
        });
      });
    }