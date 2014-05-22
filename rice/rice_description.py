# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
from uber import uber_lib

class RiceDescriptionPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('rice/rice_description.txt','r')
        x = text_file1.read()
        text_file2 = open('rice/rice_text.txt','r')
        xx = text_file2.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "Rice Description")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'rice','page':'description'})
        html = html + template.render(templatepath + '03ubertext_links_left.html', {})                       
        html = html + template.render(templatepath + '04ubertext_start.html', {
			'model_page':'http://www.epa.gov/oppefed1/models/water/rice_tier_i.htm',
			'model_attributes':'Rice Model Overview', 
			'text_paragraph':xx})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', RiceDescriptionPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    