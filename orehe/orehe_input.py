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
                <li class="uutab scenario tabSel">Chemical</li>
                <li class="uutab ie tabUnsel" style="display:none"> | Indoor Environment</li>
                <li class="uutab pp tabUnsel" style="display:none"> | Paints / Preservatives</li>
                <li class="uutab tp tabUnsel" style="display:none"> | Treated Pets</li>
                <li class="uutab oa tabUnsel" style="display:none"> | Outdoor Aerosol Space Sprays</li>
                <li class="uutab or tabUnsel" style="display:none"> | Outdoor Residential Misting Systems</li>
                <li class="uutab ab tabUnsel" style="display:none"> | Animal Barn Misting Systems</li>
            </ul>
        </div>
        """
        # html = html + template.render (templatepath + '04uberinput_tabbed_nav.html', {
        #         'nav_dict': {
        #             'class_name': ['scenario', 'ie', 'pp', 'tp', 'oa', 'or', 'ab'],
        #             'tab_label': ['Chemical', 'Indoor Environment', 'Paints / Preservatives', 'Treated Pets', 'Outdoor Aerosol Space Sprays', 'Outdoor Residential Misting Systems', 'Animal Barn Misting Systems']
        #             }
        #         })
        html = html + """<br><table class="input_table tab tab_scenario">"""
        html = html + str(orehe_parameters.oreheInp_cm())
        html = html + """</table><table class="input_table tab tab_ie" style="display:none">"""
        html = html + str(orehe_parameters.oreheInp_gh())
        html = html + """</table><table class="input_table tab tab_pp" style="display:none">"""
        html = html + str(orehe_parameters.oreheInp_pp_ac())
        html = html + """</table><table class="input_table tab tab_tp" style="display:none">"""
        html = html + str(orehe_parameters.oreheInp_tp_dp())
        html = html + """</table><table class="input_table tab tab_oa" style="display:none">"""
        html = html + str(orehe_parameters.oreheInp_oa())
        html = html + """</table><table class="input_table tab tab_or" style="display:none">"""
        html = html + str(orehe_parameters.oreheInp_or())
        html = html + """</table><table class="input_table tab tab_ab" style="display:none">"""
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

