# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

@author: pascact1
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgi
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import django
from django import forms
from ubertool import select_chemical_db
import sys
import logging

UBERTOOL_MONGO_SERVER = os.environ['UBERTOOL_MONGO_SERVER']

class SelectChemicalInputPage(webapp.RequestHandler):

    def get(self):
        logger = logging.getLogger(__name__)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_nomodellinks.html', {'title2':'Select Chemical'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {'model':'select_chemical'})
        html = html + template.render(templatepath + 'chemical_selection_jqueryui.html', {'UBERTOOL_MONGO_SERVER':UBERTOOL_MONGO_SERVER})
        html = html + str(select_chemical_db.SelectChemicalInp())
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)


app = webapp.WSGIApplication([('/.*', SelectChemicalInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    
