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
        text_file1 = open('hh_description.txt','r')
        x = text_file1.read()
        text_file2 = open('hh_text.txt','r')
        xx = text_file2.read()
        templatepath = os.path.dirname(__file__) + '/templates/'                     
        html = template.render(templatepath+'01hh_uberheader_main.html', {'title':'Ubertool'})
        html = html + template.render(templatepath+'02hh_uberintroblock_nomodellinks.html', {'title2':'Ecological Risk Web Applications','title3':x})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                        
        html = html + template.render (templatepath+'04ubertext_start_index.html', {'text_paragraph':xx})
        html = html + template.render (templatepath+'04ubertext_end.html',{})
        html = html + template.render (templatepath+'05hh_ubertext_links_right.html', {})
        html = html + template.render(templatepath+'06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', defaultPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()  