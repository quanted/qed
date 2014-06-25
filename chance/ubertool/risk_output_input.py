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
from ubertool import use_db
import logging


class UseInputPage(webapp.RequestHandler):
    def get(self):
        ubertool_service_url = os.environ['UBERTOOL_MONGO_SERVER']
        logger = logging.getLogger(__name__)
        cookies = self.request.cookies
        #logger.info(cookies)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        #html = template.render(templatepath + '01uberheaderchance.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + 'ubertool_use_jquery.html', {'ubertool_service_url':ubertool_service_url})
        html = html + template.render(templatepath + '02uberintroblock_nomodellinks.html', {'title2':'Use/Label/Site Data', 'model':'use'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_use_start.html', {'model':'use'})
        html = html + str(use_db.UseInp())
        html = html + template.render(templatepath + '04uberinput_use_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', UseInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    