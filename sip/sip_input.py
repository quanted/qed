"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
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
from sip import sip_parameters
from uber import uber_lib

class SIPInputPage(webapp.RequestHandler):
    def get(self):
        text_file = open('sip/sip_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "SIP Inputs")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'sip','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {}) 
        html = html + template.render(templatepath + 'sip-jQuery.html', {})               
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'sip', 
                'model_attributes':'SIP Inputs'})
        html = html + template.render (templatepath + 'sip_ubertool_config_input.html', {})  
        html = html + str(sip_parameters.SIPInp())
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render (templatepath + 'sip_ubertool_config.html', {})
        html = html + template.render(templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', SIPInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
