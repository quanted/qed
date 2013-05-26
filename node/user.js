var flow = require('nimble');
var crypto = require('crypto');
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

exports.getLoginDecision = function(user_id, password, callback)
{ 
  db.collection('user', function(err,collection){
    collection.findOne({user_id:user_id},function(err,user_data) {
      if(user_data != null)
      {
        var crypted_password = user_data.password;
        var salt = user_data.salt;
        console.log("crypted_password: " + crypted_password + " salt: " + salt);
        callback(null,authenticate(password,crypted_password,salt));
      } else {
        callback(null,false);
      }
    });
  });
}

exports.registerUser = function(user_id, password, email_address, callback)
{ 
  console.log("Registering User");
  var salt = makeSalt();
  console.log("salt: " + salt);
  var encrypted_password = encryptPassword(password,salt);
  console.log("encrypted password: " + encrypted_password);
  var registration_data = {'email_address':email_address,'user_id':user_id,'salt':salt,'password':encrypted_password};
  db.collection('user', function(err,collection){
    collection.findAndModify({ubertool_username:user_id}, {created: 1},
      registration_data , {new:true, upsert:true, w:1},function(err,doc){
        callback(null,true);
      });
  });
}

makeSalt = function() 
{
  return Math.round((new Date().valueOf() * Math.random())) + '';
}

encryptPassword = function(password,salt) 
{
  console.log("password: " + password + "salt: " + salt);
  var encrypted_password = crypto.createHmac('sha1', salt).update(password).digest('hex');
  console.log('encrypted password: ' + encrypted_password);
  return encrypted_password;
}

authenticate = function(plainText,hashed_password,salt) 
{
  var corrected_password = (encryptPassword(plainText,salt) === hashed_password);
  return corrected_password;
}