# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os

class genericJonDescriptionPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('genericJon/genericJon_description.txt','r')
        x = text_file1.read()
        text_file2 = open('genericJon/genericJon_text.txt','r')
        xx = text_file2.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheaderJon.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinksJon.html', {'model':'genericJon','page':'description'})
        html = html + template.render(templatepath + '03hh_ubertext_links_leftJon.html', {})                       
        html = html + template.render(templatepath + '04ubertext_startJon.html', {
                'model_page':'#',
                'model_attributes':"Jon's Testing Domain", 
                'text_paragraph':xx})
        html = html + template.render(templatepath + '04ubertext_endJon.html', {})
        html = html + template.render(templatepath + '05hh_ubertext_links_rightJon.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', genericJonDescriptionPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
 