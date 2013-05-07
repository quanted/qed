# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: tao.hong
"""

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgi
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import django
from django import forms
from therps import therps_parameters


class THerpsInputPage(webapp.RequestHandler):
    def get(self):
        text_file = open('therps/therps_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'therps','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})        
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'therps', 
                'model_attributes':'T-Herps Inputs'})

        html = html + """<table><H4  align="center" id="id_tab">
            |<a class="Chemical" style="color:#FFA500; font-weight:bold"> Chemical </a>|
             <a class="Avian" style="font-weight:bold"> Avian </a>|
             <a class="Herptile" style="font-weight:bold"> Herptile </a>|
            </H4>"""
        html = html + """</table><br><table class="tab tab_Chemical" border="0">"""
        html = html + str(therps_parameters.trexInp_chem())
        html = html + """</table><table class="tab tab_Avian" border="0" style="display:none">"""
        html = html + str(therps_parameters.trexInp_bird())
        html = html + """</table><table class="tab tab_Herptile" border="0" style="display:none">"""
        html = html + str(therps_parameters.trexInp_herp())
        html = html + template.render(templatepath + 'therps_input_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + 'therps-jquery.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', THerpsInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    