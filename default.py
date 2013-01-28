# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""

from google.appengine.ext import webapp

from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import db

from google.appengine.ext.webapp import template

from google.appengine.ext.db import djangoforms

class defaultPage(webapp.RequestHandler):
    def get(self):
        html = template.render('templates/01uberheader.html', {'title':'TITLE'})
        html = html + template.render('templates/02uberintroblock.html', {'title2':'TITLE2'})
        html = html + template.render ('templates/03aubertext_start.html', {'text_paragraph':'Text goes here.'})
        html = html + template.render ('templates/03bubertext_add.html', {'text_paragraph':'More text goes here.'})
        html = html + template.render ('templates/03dubertext_end.html',{})
        html = html + template.render ('templates/03cubertext_links.html', {})
        html = html + template.render('templates/04uberform_end.html', {'sub_title': 'Submit Input'})
        html = html + template.render('templates/05uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', defaultPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    