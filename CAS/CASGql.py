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

google_cloud_instance = "uberdb:cas"
google_cloud_database = "CAS"

local_mysql_instance = "localhost"
local_mysql_database = "ubertool"
local_mysql_user = "ubertool"
local_mysql_password = "ubertool"


class CASGqlPage(webapp.RequestHandler):
	def get(self):
		cas = CASGql()
		results = cas.getAllChemicalNamesCASNumbers(20)
		print results
		print "TEST"
		self.response.out.write("""
		  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		  <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
			<head>
			   <title>My Guestbook!</title>
			</head>
			<body>
			  <table style="border: 1px solid black">
				<tbody>
				  <tr>
					<th width="35%" style="background-color: #CCFFCC; margin: 5px">ChemicalName</th>
					<th style="background-color: #CCFFCC; margin: 5px">CASNumber</th>
				  </tr>""")
		for result in results:
			self.response.out.write('<tr><td>')
			self.response.out.write(cgi.escape(result[0]))
			self.response.out.write('</td><td>')
			self.response.out.write(result[1])
			self.response.out.write('</td></tr>')
		self.response.out.write("""
		  </tbody>
		  </body>
		</html>""")
		cas.closeDBConnection()

class CASGql:

	def __init__(self, instance=google_cloud_instance, database=google_cloud_database, user=local_mysql_user, password=local_mysql_password):
		self.logger = logging.getLogger(__name__)
		try:
			self.conn = rdbms.connect(instance=google_cloud_instance, database=google_cloud_database)
		except rdbms.OperationalError:
			try:
				self.conn = rdbms.connect(instance=local_mysql_instance, database=local_mysql_database,user=local_mysql_user,password=local_mysql_password)
			except:
				self.logger.error("Either not on Google AppEngine or local MySQL db not set-up")
			
	def closeDBConnection(self):
		self.conn.close()
			
	def getAllChemicalNames(self, max=None):
		cursor = self.conn.cursor()
		if max is None:
			cursor.execute('SELECT ChemicalName from CAS')
		else:
			cursor.execute('SELECT ChemicalName from CAS limit %s' , (max))
		rows = cursor.fetchall()
		return rows

	def getAllChemicalNamesCASNumbers(self, max=None):
		cursor = self.conn.cursor()
		if max is None:
			cursor.execute('SELECT ChemicalName,CASNumber from CAS')
		else:
			cursor.execute('SELECT ChemicalName,CASNumber from CAS limit %s' , (max))
		rows = cursor.fetchall()
		return rows

	def getAllChemNamesCASNumsUTF8(self, max=None, macChars=None):
		unicodeList = self.getAllChemicalNamesCASNumbers(max)
		self.logger.debug(unicodeList)
		utfList = self.makeListUTF8(unicodeList, macChars)
		self.logger.debug(utfList)
		return utfList

	def getChemicalNameFromCASNumber(self, casNumber):
		cursor = self.conn.cursor()
		cursor.execute('SELECT ChemicalName from CAS where CASNumber=%s', (casNumber))
		chemicalName = cursor.fetchone()
		print chemicalName
		return chemicalName

	def getCASNumberFromChemicalName(self, chemicalName):
		cursor = self.conn.cursor()
		cursor.execute('SELECT CASNumber from CAS where ChemicalName=%s', (chemicalName))
		casNumber = cursor.fetchone()
		print casNumber
		return casNumber

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
	

app = webapp.WSGIApplication([('/.*', CASGqlPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
