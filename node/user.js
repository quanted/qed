var flow = require('nimble');
var crypto = require('crypto');
var utils = require('./utils.js');
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
  var encrypted_password = encryptPassword(password,salt);
  var api_key = utils.generateNewAPIKey();
  var registration_data = {'email_address':email_address,'user_id':user_id,'salt':salt,'password':encrypted_password, 'api_key':api_key};
  db.collection('user', function(err,collection){
    collection.findAndModify({user_id:user_id}, {},
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
  var encrypted_password = crypto.createHmac('sha1', salt).update(password).digest('hex');
  return encrypted_password;
}

authenticate = function(plainText,hashed_password,salt) 
{
  var corrected_password = (encryptPassword(plainText,salt) === hashed_password);
  return corrected_password;
}

exports.authenticateRestAccess = function(userid, api_key, callback)
{
  console.log('user_id: ' + userid + " api key: " + api_key);
  db.collection('user', function(err,collection){
    collection.findOne({'user_id':userid}, function(err, user_data) {
      console.log('mongo stored api_key: ' + user_data.api_key);
      var authenticated = false;
      if( err || !user_data || !user_data.api_key)
      {
        console.log('No user found.');
        callback(null,authenticated);
      }
      else
      {
        authenticated = (api_key === user_data.api_key);
        console.log('API key authentication state: ' + authenticated);
        callback(null,authenticated);
      }
    });
  });
}

