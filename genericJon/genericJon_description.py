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

class genericJonDescriptionPage(webapp.RequestHandler):
    def get(self):
        text_file2 = open('genericJon/genericJon_text.txt','r')
        xx = text_file2.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        # if ChkCookie == 'EPA':
        #     html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        # else:
        #     html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})
        html = uber_lib.SkinChk(ChkCookie)
        # html = webapp.get_request()
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'genericJon','page':'description'})
        html = html + template.render(templatepath + '03hh_ubertext_links_leftJon.html', {})                       
        html = html + template.render(templatepath + '04ubertext_start.html', {
                'model_page':'#',
                'model_attributes':"Jon's Testing Domain", 
                'text_paragraph':xx})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', genericJonDescriptionPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
 