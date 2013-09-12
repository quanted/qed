import os
from compiler.pycodegen import EXCEPT
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgi
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import django
from django import forms
from google.appengine.api import rdbms
import logging

google_cloud_instance = "apppest:cas"
google_cloud_database = "CAS"

local_mysql_instance = "localhost"
local_mysql_database = "ubertool"
local_mysql_user = "ubertool"
local_mysql_password = "ubertool"
		
class CASGql:

	def __init__(self, instance=google_cloud_instance, database=google_cloud_database, user=local_mysql_user, password=local_mysql_password):
		self.logger = logging.getLogger(__name__)
		self.conn = None
		try:
			self.conn = rdbms.connect(instance=google_cloud_instance, database=google_cloud_database)
		except:
			try:
				self.logger.error("Trying local MySQL db")
				self.conn = rdbms.connect(instance=local_mysql_instance, database=local_mysql_database,user=local_mysql_user,password=local_mysql_password)
			except:
				self.logger.error("Either not on Google AppEngine or local MySQL db not set-up")
			
	def closeDBConnection(self):
		self.conn.close()
			
	def getAllChemicalNames(self, max=None):
		rows = None
		if not self.conn is None:
			cursor = self.conn.cursor()
			if max is None:
				cursor.execute('SELECT ChemicalName from CAS')
			else:
				cursor.execute('SELECT ChemicalName from CAS limit %s' , (max))
			rows = cursor.fetchall()
		return rows
	
	def getAllChemicalNamesUTF8(self, max=None, maxChars=None):
		unicodeList = self.getAllChemicalNames(max)
		utfList = None
		if not unicodeList is None:
			utfList = self.makeChemicalNamesListUTF8(unicodeList,maxChars)
		#self.logger.info(utfList)
		return utfList

	def getAllChemicalNamesCASNumbers(self, max=None):
		rows = None
		if not self.conn is None:
			cursor = self.conn.cursor()
			if max is None:
				cursor.execute('SELECT ChemicalName,CASNumber from CAS')
			else:
				cursor.execute('SELECT ChemicalName,CASNumber from CAS limit %s' , (max))
			rows = cursor.fetchall()
		return rows

	def getAllChemNamesCASNumsMongoJson(self):
		utfTupleList = self.getAllChemNamesCASNumsUTF8()
		mongoJSON = None
		if not utfTupleList is None:
			mongoJSON = ''
			for utfTuple in utfTupleList:
				mongoJSON += '{\"ChemicalName\":\"%s\",\"CASNumber\":\"%s\"}\n' % (utfTuple[1],utfTuple[0])
			self.logger.info(mongoJSON)
		return mongoJSON

	def getAllChemNamesCASNumsUTF8(self, max=None, macChars=None):
		unicodeList = self.getAllChemicalNamesCASNumbers(max)
		utfList = None
		if not unicodeList is None:
			self.logger.debug(unicodeList)
			utfList = self.makeListUTF8(unicodeList, macChars)
		return utfList

	def getChemicalNameFromCASNumber(self, casNumber):
		chemicalName = None
		if not self.conn is None:
			cursor = self.conn.cursor()
			cursor.execute('SELECT ChemicalName from CAS where CASNumber=%s', (casNumber))
			chemicalName = cursor.fetchone()
			print chemicalName
		return chemicalName

	def getCASNumberFromChemicalName(self, chemicalName):
		casNumber = None
		if not self.conn is None:
			cursor = self.conn.cursor()
			cursor.execute('SELECT CASNumber from CAS where ChemicalName=%s', (chemicalName))
			casNumber = cursor.fetchone()
			print casNumber
		return casNumber
	
	def makeChemicalNamesListUTF8(self, list, maxChars=None):
		utfList = []
		#self.logger.info(list)
		for item in list:
			chemName = item[0]
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
			chemName = item[0]
			casNum = item[1]
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
	

