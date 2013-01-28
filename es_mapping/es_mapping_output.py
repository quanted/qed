# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb

import json
import base64
import urllib
from google.appengine.api import urlfetch



                                   
class ESOutputPage(webapp.RequestHandler):
    def get(self):
        #text_file1 = open('geneec/geneec_description.txt','r')
        #x = text_file1.read()        

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'es_mapping'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {'model':'es_mapping'})
        html = html + template.render(templatepath+'ManykmlDropbox.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', ESOutputPage)], debug=True)
        

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()                                                                                                         




    