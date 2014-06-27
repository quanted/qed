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

    exports.getAllFormulaData = function(callback)
    {
    	db.collection('chemicals', function(err,collection){
    		collection.find().toArray(function(err,all_formulas) {
    			var formula_data = [];
    			for(i = 0; i < all_formulas.length; i++)
    			{
    				formula_data.push({"Registration Number":all_formulas[i].regnum.substring(0,20),
                                      "PC Percentage":all_formulas[i].pcpct,
                                      "Product Name":all_formulas[i].prodname,
                                      "PC Code":all_formulas[i].pccode})
    			}
    			callback(null,formula_data);
    		});
    	});
    }

    exports.getAllProductNames = function(callback)
    {
      getAllFormulaData( function(err,all_formulas){
        var prodname_data = [];
        for(i = 0; i < all_formulas.length; i++)
        {
          prodname_data.push(all_formulas[i].prodname.substring(0,20));
        }
        callback(null,prodname_data);
      })
    }

    exports.getFormulaDataFromPCCode = function(pc_code,callback)
    { 
      db.collection('chemicals', function(err,collection){
        collection.find({pccode:pc_code}).toArray(function(err,all_formulas) {
          var formula_data = [];
          for(i = 0; i < all_formulas.length; i++)
          {
            formula_data.push({"Registration Number":all_formulas[i].regnum.substring(0,20),
                                      "PC Percentage":all_formulas[i].pcpct,
                                      "Product Name":all_formulas[i].prodname,
                                      "PC Code":all_formulas[i].pccode})
          }
          callback(null,formula_data);
        });
      });
    }

    exports.getFormulaData = function(registration_num,callback)
    { 
      db.collection('chemicals', function(err,collection){
        collection.findOne({regnum:registration_num},function(err,chemical) {
          callback(null,chemical);
        });
      });
    }