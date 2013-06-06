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
from user import userdb


class UserInputPage(webapp.RequestHandler):
    def get(self):
        ubertool_batch_server = os.environ['UBERTOOL_MONGO_SERVER']
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'User'})
        html = html + template.render(templatepath + '02uberintroblock_nomodellinks.html', {'title2':'Update User Ubertool Configurations'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {'model':'user'})
        html = html + str(userdb.UserInp())
        html = html + template.render (templatepath + '04user_assessment_history.html', {})  
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + 'user_jquery.html', {'ubertool_server':ubertool_batch_server})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', UserInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()