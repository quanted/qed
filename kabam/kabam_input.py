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
        html = html + template.render(templatepath + '04uberinput_start_tabbed.html', {
                'model':'kabam', 
                'model_attributes':'Kabam Inputs'})
        html = html + """
        <div id="input_nav">
          <ul>
            <li>| <a class="Chemical" style="color:#FFA500; font-weight:bold"> Chemical </a></li>
            <li>| <a class="Avian" style="font-weight:bold"> Avian </a></li>
            <li>| <a class="Mammal" style="font-weight:bold"> Mammal </a></li>
            <li>| <a class="LargeFish" style="font-weight:bold"> Large Fish </a></li>
            <li>| <a class="MediumFish" style="font-weight:bold"> Medium Fish </a></li>
            <li>| <a class="SmallFish" style="font-weight:bold"> Small Fish </a></li>
            <li>| <a class="Filterfeeders" style="font-weight:bold"> Filter feeders </a></li>
            <li>| <a class="Invertebrates" style="font-weight:bold"> Invertebrates </a></li>
            <li>| <a class="Zooplankton" style="font-weight:bold"> Zooplankton </a></li>
            <li>| <a class="Phytoplankton" style="font-weight:bold"> Phytoplankton </a></li>
            <li>| <a class="Sediment" style="font-weight:bold"> Sediment </a></li>
            <li>| <a class="Constants" style="font-weight:bold"> Constants </a>|</li>
          </ul>
        </div>
        """
        html = html + """<br><table class="tab tab_Chemical" border="0">"""
        html = html + str(Kabamdb.KabamInp_chem())
        html = html + """</table><table class="tab tab_Avian" border="0" style="display:none">"""
        html = html + str(Kabamdb.KabamInp_bird())
        html = html + """</table><table class="tab tab_Mammal" border="0" style="display:none">"""
        html = html + str(Kabamdb.KabamInp_mammal())
        html = html + """</table><table class="tab tab_LargeFish" border="0" style="display:none">"""
        html = html + str(Kabamdb.KabamInp_lfish())
        html = html + """</table><table class="tab tab_MediumFish" border="0" style="display:none">"""
        html = html + str(Kabamdb.KabamInp_mfish())
        html = html + """</table><table class="tab tab_SmallFish" border="0" style="display:none">"""
        html = html + str(Kabamdb.KabamInp_sfish())
        html = html + """</table><table class="tab tab_Filterfeeders" border="0" style="display:none">"""
        html = html + str(Kabamdb.KabamInp_ff())
        html = html + """</table><table class="tab tab_Invertebrates" border="0" style="display:none">"""
        html = html + str(Kabamdb.KabamInp_invert())
        html = html + """</table><table class="tab tab_Zooplankton" border="0" style="display:none">"""
        html = html + str(Kabamdb.KabamInp_zoo())
        html = html + """</table><table class="tab tab_Phytoplankton" border="0" style="display:none">"""
        html = html + str(Kabamdb.KabamInp_phyto())
        html = html + """</table><table class="tab tab_Sediment" border="0" style="display:none">"""
        html = html + str(Kabamdb.KabamInp_sed())
        html = html + """</table><table class="tab tab_Constants" border="0" style="display:none">"""
        html = html + str(Kabamdb.KabamInp_constants())
        html = html + template.render(templatepath + 'kabam_input_end.html', {'sub_title': 'Submit'})
      #  html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', KabamInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

