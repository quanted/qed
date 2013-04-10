# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012
@author: tao.hong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import math 
import cgitb
import json

cgitb.enable()

class pdfLoadingPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()   
        pdf_t = form.getvalue('pdf_t')
        pdf_nop = form.getvalue('pdf_nop')
        pdf_p = json.loads(form.getvalue('pdf_p'))
        print form
        templatepath = os.path.dirname(__file__) + '/../templates/'                                 
        html = template.render(templatepath + 'popup.html', {'title':'Ubertool'})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', pdfLoadingPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()  

