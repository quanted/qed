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
import sys
sys.path.append("CAS")
from CAS.CASGql import CASGql
from django.utils import simplejson

class CASService(webapp.RequestHandler):
    
    def get(self,casNumber):
        cas = CASGql()
        results = cas.getChemicalNameFromCASNumber(casNumber)
        chem_json = simplejson.dumps({"chemical_name":results})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(chem_json)

class CASJsonService(webapp.RequestHandler):
    
    def get(self):
        cas = CASGql()
        results = cas.getAllChemNamesCASNumsMongoJson()
        chem_json = simplejson.dumps(results)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(chem_json)

app = webapp.WSGIApplication([('/cas/(.*)', CASService),
								('/cas-all/json', CASJsonService)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
