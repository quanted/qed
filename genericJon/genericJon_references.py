# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""

import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os

class genericJonReferencesPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('genericJon/genericJon_references.txt','r')
        x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheaderJon.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinksJon.html', {'model':'genericJon'})
        html = html + template.render(templatepath + '03ubertext_links_left.html', {})                        
        html = html + template.render(templatepath + '04uberreferences_start.html', {
                'model':'genericJon', 
                'model_attributes':'GenericJon References', 
                'text_paragraph':x})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', genericJonReferencesPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()