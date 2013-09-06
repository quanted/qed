#!/usr/bin/env python
# -*- coding:utf-8 -*-
#*********************************************************#
# @@ScriptName: orehe_input.py
# @@Author: Tao Hong
# @@Create Date: 2013-06-19
# @@Modify Date: 2013-09-05
#*********************************************************#
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
from orehe import orehe_parameters

class oreheInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})
        html = html + template.render (templatepath + 'orehe-jquery.html', {})
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'orehe','page':'input'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start_tabbed.html', {
                'model':'orehe', 
                'model_attributes':'ORE Inputs'})
        html = html + """
        <div id="input_nav">
            <ul>
                <li class="uutab scenario" style="color:#A31E39; font-weight:bold">Chemical</li>
                <li class="uutab ie" style="font-weight:bold; display:none"> | Indoor Environment</li>
                <li class="uutab pp" style="font-weight:bold; display:none"> | Paints / Preservatives</li>
                <li class="uutab tp" style="font-weight:bold; display:none"> | Treated Pets</li>
                <li class="uutab oa" style="font-weight:bold; display:none"> | Outdoor Aerosol Space Sprays</li>
                <li class="uutab or" style="font-weight:bold; display:none"> | Outdoor Residential Misting Systems</li>
                <li class="uutab ab" style="font-weight:bold; display:none"> | Animal Barn Misting Systems</li>
            </ul>
        </div>
        """
        html = html + """<br><table class="tab tab_scenario" border="0">"""
        html = html + str(orehe_parameters.oreheInp_cm())
        html = html + """</table><table class="tab tab_ie" border="0" style="display:none">"""
        html = html + str(orehe_parameters.oreheInp_gh())
        html = html + """</table><table class="tab tab_pp" border="0" style="display:none">"""
        html = html + str(orehe_parameters.oreheInp_pp_ac())
        html = html + """</table><table class="tab tab_tp" border="0" style="display:none">"""
        html = html + str(orehe_parameters.oreheInp_tp_dp())
        html = html + """</table><table class="tab tab_oa" border="0" style="display:none">"""
        html = html + str(orehe_parameters.oreheInp_oa())
        html = html + """</table><table class="tab tab_or" border="0" style="display:none">"""
        html = html + str(orehe_parameters.oreheInp_or())
        html = html + """</table><table class="tab tab_ab" border="0" style="display:none">"""
        html = html + str(orehe_parameters.oreheInp_ab())



        html = html + template.render(templatepath + '04uberinput_tabbed_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05hh_ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', oreheInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

