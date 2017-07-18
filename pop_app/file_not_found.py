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

class defaultPage(webapp.RequestHandler):
    def get(self):
        html = template.render('templates/01pop_uberheader.html', {'title':'File not found.'})
        html = html + template.render('templates/02pop_uberintroblock_nomodellinks.html', {'title2':'File not found'})
        html = html + template.render ('templates/03pop_ubertext_links_left.html', {})                                
        html = html + template.render ('templates/04ubertext_start.html', {'text_paragraph':'File not found.'})
        html = html + """ <img src="../images/404error.png" width="300" height="300">"""
        html = html + template.render ('templates/04ubertext_end.html', {})
        html = html + template.render ('templates/05pop_ubertext_links_right.html', {})
        html = html + template.render('templates/06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', defaultPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
