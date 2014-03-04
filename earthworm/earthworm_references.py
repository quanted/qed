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

class earthwormReferencesPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('earthworm/earthworm_references.txt','r')
        x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "Earthworm References")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'earthworm','page':'references'})
        html = html + template.render(templatepath + '03ubertext_links_left.html', {})                        
        html = html + template.render(templatepath + '04uberreferences_start.html', {
                'model':'earthworm', 
                'model_attributes':'Earthworm References', 
                'text_paragraph':x})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', earthwormReferencesPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()