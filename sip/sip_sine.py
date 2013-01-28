# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""

from google.appengine.ext import webapp

from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import db

from google.appengine.ext.webapp import template

from google.appengine.ext.db import djangoforms

import os

from sip import sip_db

from sip import sine

def run_sine3():
    run_sine2 = sine.run_sine()
    return run_sine2

#class SIPInput(djangoforms.ModelForm):
#    class Meta:
#        model = sip_db.SIPInp

class SIPInputPage(webapp.RequestHandler):
    def get(self):
        text_file = open('sip_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock.html', {'title2':'Screening Imbibition Program (SIP) Version 1.0', 'title3':x})
        html = html + template.render(templatepath + '02modellinkblock.html', {'model':'sip'})
        html = html + template.render(templatepath + '03euberinput_start.html', {'model':'sip/sip'})
#        html = html + str(SIPInput())
        html = html + str(run_sine3())
        html = html + template.render(templatepath + '03dubertext_end.html', {})
        html = html + template.render(templatepath + '03cubertext_links.html', {})
        html = html + template.render(templatepath + '04uberform_end.html', {})
        html = html + template.render(templatepath + '05uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', SIPInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
import cgi

import cgitb
cgitb.enable()

form = cgi.FieldStorage()    