#!/usr/bin/env python
# -*- coding:utf-8 -*-
#*********************************************************#
# @@ScriptName: orehe_description.py
# @@Author: Tao
# @@Create Date: 2013-06-19
# @@Modify Date: 2013-08-28
#*********************************************************#
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os

class oreheDescriptionPage(webapp.RequestHandler):
    def get(self):
        text_file2 = open('orehe/orehe_text.txt','r')
        xx = text_file2.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'orehe','page':'description'})
        html = html + template.render(templatepath + '03hh_ubertext_links_left.html', {})                       
        html = html + template.render(templatepath + '04ubertext_start.html', {
                'model_page':'#', 
                'model_attributes':'ORE Overview', 
                'text_paragraph':xx})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05hh_ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', oreheDescriptionPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
 
