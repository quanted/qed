# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import http_check_pages
from django.utils.safestring import mark_safe
import datetime

class aboutPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/templates/'                     
        html = template.render(templatepath+'01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath+'02uberintroblock_nomodellinks.html', {'title2':'Ecological Risk Web Applications','title3':''})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {}) 

        #check to see if all web pages are serving
        http_html = http_check_pages.check_pages("eco")

        html = html + template.render(templatepath + '04ubertext_start.html', {
                'model_page':'',
                'model_attributes':'Ecological Web Page Integration Testing','text_paragraph':http_html})
        #html = html + http_html
        html = html + template.render(templatepath+'04uberoutput_end.html',{})
        html = html + template.render(templatepath+'06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', aboutPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()  