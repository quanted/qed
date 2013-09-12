import logging
from pymongo import MongoClient

class CASMongo:

	def __init__(self, mongodb_host='chancedelphia.com', mongodb_port=27017):
		self.client = MongoClient(mongodb_host, mongodb_port)
		self.db = self.client.ubertool

	def getAll(self, max=None):
		results = None
		cas_collection = self.db.CAS
		if max is None:
			results = cas_collection.find()
		else:
			results = cas_collection.find(limit=max)
		return results
	
	def getAllChemicalNamesUTF8(self, max=None, maxChars=None):
		unicodeList = self.getAll(max)
		utfList = self.makeChemicalNamesListUTF8(unicodeList,maxChars)
		self.logger.info(utfList)
		return utfList

	def getAllChemNamesCASNumsMongoJson(self):
		utfTupleList = self.getAllChemNamesCASNumsUTF8()
		mongoJSON = ''
		for utfTuple in utfTupleList:
			mongoJSON += '{\"ChemicalName\":\"%s\",\"CASNumber\":\"%s\"}\n' % (utfTuple[1],utfTuple[0])
		self.logger.info(mongoJSON)
		return mongoJSON

	def getAllChemNamesCASNumsUTF8(self, max=None, maxChars=None):
		unicodeList = self.getAll(max)
		self.logger.debug(unicodeList)
		utfList = self.makeListUTF8(unicodeList, maxChars)
		return utfList

	def getChemicalNameFromCASNumber(self, casNumber):
		chemicalName = None
		cas_collection = self.db.CAS
		results = cas_collection.find_one({"CASNumber":casNumber})
		chemicalName = results["CASNumber"]
		print chemicalName
		return chemicalName

	def getCASNumberFromChemicalName(self, chemicalName):
		casNumber = None
		cas_collection = self.db.CAS
		results = cas_collection.find_one({"ChemicalName":chemicalName})
		casNumber = results["ChemicalName"]
		print casNumber
		return casNumber
	
	def makeChemicalNamesListUTF8(self, list, maxChars=None):
		utfList = []
		#self.logger.info(list)
		for item in list:
			chemName = item["ChemicalName"]
			try:
				utfChemName = chemName.encode('UTF-8')
				if not maxChars is None:
					utfChemName = utfChemName[0:maxChars]
				utfList.append(utfChemName)
			except UnicodeDecodeError:
				# TODO don't just drop these on the floor
				pass
		return utfList

	def makeListUTF8(self, list, maxChars=None):
		utfList = ()
		for item in list:
			self.logger.debug(item)
			chemName = item["ChemicalName"]
			casNum = item["CASNumber"]
			try:
				utfChemName = chemName.encode('UTF-8')
				if not maxChars is None:
					utfChemName = utfChemName[0:maxChars]
				utfCASnum = casNum.encode('UTF-8')
				utfTuple = ((utfCASnum, utfChemName),)
				utfList += utfTuple
			except UnicodeDecodeError:
				# TODO don't just drop these on the floor
				pass
		return utfList