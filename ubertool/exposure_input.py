# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

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
from ubertool import exposure_db

class ECInputPage(webapp.RequestHandler):
    def get(self):
        mongo_service_url = os.environ['UBERTOOL_MONGO_SERVER']
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render (templatepath + 'ubertool_expoconc_jquery.html', {'ubertool_service_url':mongo_service_url})
        html = html + template.render(templatepath + '02uberintroblock_nomodellinks.html', {'title2':'Exposure', 'model':'exposure'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_expo_start.html', {'model':'exposure'})
        html = html + str(exposure_db.ECInp())
        html = html + template.render(templatepath + '04uberinput_expo_end.html', {'sub_title': 'submit'})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', ECInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    