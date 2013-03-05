# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
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
from terrplant import terrplant_db


class TerrPlantInputPage(webapp.RequestHandler):
    def get(self):
        text_file = open('terrplant/terrplant_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'terrplant','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render (templatepath + '04uberinput_start.html', {
                'model':'terrplant', 
                'model_attributes':'TerrPlant Inputs'})
        html = html + str(terrplant_db.TerrPlantInp())
        html = html + template.render (templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render (templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TerrPlantInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

