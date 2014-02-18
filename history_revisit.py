# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import cgi, cgitb
cgitb.enable()
import logging
logger = logging.getLogger('historyoutputPage')
import rest_funcs


class historyoutputPage(webapp.RequestHandler):
    def get(self):
        form = cgi.FieldStorage() 
        jid = form.getvalue('jid')
        model_name = form.getvalue('model_name')
        html = rest_funcs.get_output_html(jid, model_name)
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', historyoutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    

