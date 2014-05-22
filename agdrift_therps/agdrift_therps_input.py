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
from therps import therps_parameters
from agdrift_therps import agdrift_therps_parameters
from django import forms
from uber import uber_lib

class agdrift_therpsInputPage(webapp.RequestHandler):
    def get(self):
        text_file = open('agdrift_therps/agdrift_therps_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "AgDrift-T-Herps Inputs")
        html = html + template.render (templatepath + 'agdrift_therps_jquery.html', {})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'agdrift_therps','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})        
        html = html + template.render (templatepath + '04uberinput_start_tabbed.html', {
                'model':'agdrift_therps', 
                'model_attributes':'Agdrift and Therps Inputs'})
        html = html + """
        <div class="input_nav">
            <ul>
                <li class="Agdrift tabSel">Agdrift</li>
                |<li class="Chemical tabUnsel">Chemical</li>
                |<li class="Avian tabUnsel"> Avian</li>
                |<li class="Herptile tabUnsel"> Herptile</li>
            </ul>
        </div>
        """
        html = html + """<br><table class="tab tab_Agdrift" border="0">"""
        html = html + str(agdrift_therps_parameters.agdriftInp())
        html = html + """<br><table class="tab tab_Chemical" border="0" style="display:none">"""
        html = html + str(agdrift_therps_parameters.trexInp_chem())
        html = html + """</table><table class="tab tab_Avian" border="0" style="display:none">"""
        html = html + str(agdrift_therps_parameters.trexInp_bird())
        html = html + """</table><table class="tab tab_Herptile" border="0" style="display:none">"""
        html = html + str(agdrift_therps_parameters.trexInp_herp())
        html = html + template.render(templatepath + '04uberinput_tabbed_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', agdrift_therpsInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    
    