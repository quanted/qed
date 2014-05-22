# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012
@author: thong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from trex import trexdb
from uber import uber_lib

class trexInputPage(webapp.RequestHandler):
    def get(self):
        text_file = open('trex/trex_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "TREX Inputs")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'trex','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})        
        html = html + template.render (templatepath + '04uberinput_start.html', {
                'model':'trex', 
                'model_attributes':'TREX Inputs'})
        html = html + str(trexdb.trexInp())
        html = html + template.render (templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render (templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', trexInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    