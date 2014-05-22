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
from geneec import geneec_parameters
from uber import uber_lib

class GENEECInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "GENEEC Inputs")
        html = html + template.render(templatepath + 'geneec-jQuery.html', {})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'geneec','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'geneec', 
                'model_attributes':'GENEEC Inputs'})
        html = html + str(geneec_parameters.GENEECInp())
        html = html + """<br><table class="tab_input_html" style="display:none">"""
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', GENEECInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

