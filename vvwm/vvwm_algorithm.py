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

class vvwmAlgorithmPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('vvwm/vvwm_algorithm.txt','r')
        x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "VVWM Algorithms")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'vvwm','page':'algorithm'})
        html = html + template.render(templatepath + '03ubertext_links_left.html', {})                       
        html = html + template.render(templatepath + '04ubertext_start.html', {
                'model':'vvwm', 
                'model_attributes':'VVWM Algorithms', 
                'text_paragraph':x})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', vvwmAlgorithmPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    