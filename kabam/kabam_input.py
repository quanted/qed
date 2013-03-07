# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012
@author: thong
"""

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from kabam import Kabamdb
from django import forms


class KabamInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        text_file = open('kabam/kabam_description.txt','r')
        x = text_file.read()
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + 'kabam-jQuery.html', {})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'kabam','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'kabam', 
                'model_attributes':'Kabam Inputs'})
        html = html + """<table><H4  align="center" id="id_tab">
            |<a href="#" class="Chemical"> Chemical </a>|
             <a href="#" class="Avian"> Application </a>|
             <a href="#" class="Mammal"> Location </a>|
             <a href="#" class="Large Fish"> Floods </a>|
             <a href="#" class="Medium Fish"> Crop </a>|
             <a href="#" class="Small Fish"> Physical </a>|
             <a href="#" class="Filter feeders"> Output </a>|
             <a href="#" class="Invertebrates"> Output </a>|
             <a href="#" class="Zooplankton"> Output </a>|
             <a href="#" class="Phytoplankton"> Output </a>|
             <a href="#" class="Sediment"> Output </a>|
             <a href="#" class="Constants"> Output </a>|
            </H4>"""
        html = html + """</table><br><table class="tab tab_Chemical" border="0">"""
        html = html + str(Kabamdb.KabamInp_chem())
        html = html + """</table><br><table class="tab tab_Avian" border="0">"""
        html = html + str(Kabamdb.KabamInp_bird())
        html = html + """</table><br><table class="tab tab_Mammal" border="0">"""
        html = html + str(Kabamdb.KabamInp_mammal())
        html = html + """</table><br><table class="tab tab_Large Fish" border="0">"""
        html = html + str(Kabamdb.KabamInp_lfish())
        html = html + """</table><br><table class="tab tab_Medium Fish" border="0">"""
        html = html + str(Kabamdb.KabamInp_mfish())
        html = html + """</table><br><table class="tab tab_Small Fish" border="0">"""
        html = html + str(Kabamdb.KabamInp_sfish())
        html = html + """</table><br><table class="tab tab_Filter feeders" border="0">"""
        html = html + str(Kabamdb.KabamInp_ff())
        html = html + """</table><br><table class="tab tab_Invertebrates" border="0">"""
        html = html + str(Kabamdb.KabamInp_invert())
        html = html + """</table><br><table class="tab tab_Zooplankton" border="0">"""
        html = html + str(Kabamdb.KabamInp_zoo())
        html = html + """</table><br><table class="tab tab_Phytoplankton" border="0">"""
        html = html + str(Kabamdb.KabamInp_phyto())
        html = html + """</table><br><table class="tab tab_Sediment" border="0">"""
        html = html + str(Kabamdb.KabamInp_sed())
        html = html + """</table><br><table class="tab tab_Constants" border="0">"""
        html = html + str(Kabamdb.KabamInp_constants())
        html = html + template.render(templatepath + 'kabam_input_end.html', {'sub_title': 'Submit'})
      #  html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', KabamInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

