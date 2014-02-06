# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012
@author: Jon F.
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class ICETabletPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath+'webice_ICETable.html', {'title':'Ubertool'})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', ICETabletPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()  
