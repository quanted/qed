# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: thong
"""
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os

class THerpsDescriptionPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('therps/therps_description.txt','r')
        x = text_file1.read()
        text_file2 = open('therps/therps_text.txt','r')
        xx = text_file2.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'therps','page':'description'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                                  
        html = html + template.render(templatepath + '04ubertext_start.html', {
			'model_page':'http://www.epa.gov/oppefed1/models/terrestrial/therps/t_herps_user_guide.htm',
			'model_attributes':'T-Herps Overview','text_paragraph':xx})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', THerpsDescriptionPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
