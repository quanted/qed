# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

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

class UserLoginInputPage(webapp.RequestHandler):
    def get(self):
        mongo_service_url = os.environ['UBERTOOL_MONGO_SERVER']
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + 'user_login_jquery.html', {'ubertool_service_url':mongo_service_url})
        html = html + template.render(templatepath + '02uberintroblock_nomodellinks.html', {'model':'user_login'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render (templatepath + 'user_login.html', {})                
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', UserLoginInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    