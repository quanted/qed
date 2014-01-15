import pymongo

client = pymongo.MongoClient()

# --host chancedelphia.com --port 27017 -u tao -p

#show all database
print client.database_names()

#show all collections
# print client.test_database.collection_names()
print client.ubertool.collection_names()
db = client.ubertool
# db.geneec.remove()


# aaa=db['geneec'].find({"user_id": "admin"})
# print type(aaa)

for post in db['geneec'].find({"user_id": "admin"}, {"jid":1}):
	print post

# a= db["geneec"].find({"_id" :"20140113181005545000"}, {"output_html": 1})
# print list(a)
# for post in db.przm5.find({"user_id": "admin"}):
# 	print post

# for post in db.cars.find({"make": "Ford", "$or": [{"color": "red"}, {"color": "blu"}]}):
# 	print post

# jid = '20140103183501689000'

# print db['geneec'].find_one({'jid':jid})



#Drop a database
# client.drop_database('local')


# db = client.test_database
# car = {"make": "Ford" , "model": "Galaxy", "color": "blk"}
# db.cars.insert(car)
# car1 = {"make": "Ford" , "model": "Galaxy1", "color": "red"}
# db.cars.insert(car1)
# car2 = {"make": "Ford" , "model": "Galaxy1", "color": "blu"}
# db.cars.insert(car2)
# car3 = {"make": "Ford" , "model": "Galaxy1", "color": "blu", "misc":{"year":1976}}
# db.cars.insert(car3)

# for post in db.cars.find({"make": "Ford", "$or": [{"color": "red"}, {"color": "blu"}]}):
# 	print post

# for post in db.cars.find({"misc.year": 1976}):
# 	print post

# print db.cars.find()
# print db.cars.count()
# for post in db.cars.find():
# 	print post


# dust_save = dict(dust_obj.__dict__,**user_names)
# posts.insert(dust_save)
# print db
# print posts
# print posts.find_one({"user":"tao"})
