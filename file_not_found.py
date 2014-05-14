# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
from uber import uber_lib

class defaultPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "404 Error")
        html = html + template.render(templatepath + '02uberintroblock_nomodellinks.html', {'title2':'File not found'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                                
        html = html + template.render (templatepath + '04ubertext_start.html', {
                'text_paragraph': '<h3>File not found.</h3>'})
        html = html + """ <img src="../images/404error.png" width="300" height="300">"""
        html = html + template.render (templatepath + '04ubertext_end.html', {})
        html = html + template.render (templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', defaultPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

