# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os

class genericDescriptionPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheaderJon.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinksJon.html', {'model':'genericJon'})
        html = html + template.render(templatepath + '03ubertext_links_leftJon.html', {})                       
        html = html + template.render(templatepath + '04ubertext_startJon.html', {'text_paragraph':
            "<h1>Jon's Testing Domain!</h1><br><img src=http://1.bp.blogspot.com/-xaeAJytK8Bc/T5gVt3dMKqI/AAAAAAAALj8/2x4y-laiqb8/s1600/rock.jpg>"})
        html = html + template.render(templatepath + '04ubertext_endJon.html', {})
        html = html + template.render(templatepath + '05ubertext_links_rightJon.html', {})
        html = html + template.render(templatepath + '06uberfooterJon.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', genericDescriptionPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
 