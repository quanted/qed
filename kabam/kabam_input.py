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
from kabam import kabam_parameters
from django import forms
from uber import uber_lib

class KabamInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        text_file = open('kabam/kabam_description.txt','r')
        x = text_file.read()
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "Kabam Inputs")
        html = html + template.render(templatepath + 'kabam-jQuery.html', {})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'kabam','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04uberinput_start_tabbed.html', {
                'model':'kabam', 
                'model_attributes':'Kabam Inputs'})
        html = html + template.render (templatepath + '04uberinput_tabbed_nav.html', {
                'nav_dict': {
                    'class_name': ['Chemical', 'Avian', 'Mammal', 'LargeFish', 'MediumFish', 'SmallFish', 'Filterfeeders', 'Invertebrates', 'Zooplankton', 'Phytoplankton', 'Sediment', 'Constants'],
                    'tab_label': ['Chemical', 'Avian', 'Mammal', 'Large Fish', 'Medium Fish', 'Small Fish', 'Filter feeders', 'Invertebrates', 'Zooplankton', 'Phytoplankton', 'Sediment', 'Constants']
                    }
                })
        html = html + """<br><table class="tab tab_Chemical" border="0">"""
        html = html + str(kabam_parameters.KabamInp_chem())
        html = html + """</table><table class="tab tab_Avian" border="0" style="display:none">"""
        html = html + str(kabam_parameters.KabamInp_bird())
        html = html + """</table><table class="tab tab_Mammal" border="0" style="display:none">"""
        html = html + str(kabam_parameters.KabamInp_mammal())
        html = html + """</table><table class="tab tab_LargeFish" border="0" style="display:none">"""
        html = html + str(kabam_parameters.KabamInp_lfish())
        html = html + """</table><table class="tab tab_MediumFish" border="0" style="display:none">"""
        html = html + str(kabam_parameters.KabamInp_mfish())
        html = html + """</table><table class="tab tab_SmallFish" border="0" style="display:none">"""
        html = html + str(kabam_parameters.KabamInp_sfish())
        html = html + """</table><table class="tab tab_Filterfeeders" border="0" style="display:none">"""
        html = html + str(kabam_parameters.KabamInp_ff())
        html = html + """</table><table class="tab tab_Invertebrates" border="0" style="display:none">"""
        html = html + str(kabam_parameters.KabamInp_invert())
        html = html + """</table><table class="tab tab_Zooplankton" border="0" style="display:none">"""
        html = html + str(kabam_parameters.KabamInp_zoo())
        html = html + """</table><table class="tab tab_Phytoplankton" border="0" style="display:none">"""
        html = html + str(kabam_parameters.KabamInp_phyto())
        html = html + """</table><table class="tab tab_Sediment" border="0" style="display:none">"""
        html = html + str(kabam_parameters.KabamInp_sed())
        html = html + """</table><table class="tab tab_Constants" border="0" style="display:none">"""
        html = html + str(kabam_parameters.KabamInp_constants())
        html = html + template.render(templatepath + '04uberinput_tabbed_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', KabamInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

