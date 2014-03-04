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

class Agdrift_therps_DescriptionPage(webapp.RequestHandler):
    def get(self):
        text_file2 = open('agdrift_therps/agdrift_therps_description.txt','r')
        xx = text_file2.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "AgDrift-T-Herps Description")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'agdrift_therps','page':'description'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})               
        html = html + template.render(templatepath + '04ubertext_start.html', {
            'model_attributes':'AgDrift and T-Herps Overview',
            'model_page':'http://www.agdrift.com/',
            'text_paragraph':xx})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', Agdrift_therps_DescriptionPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    