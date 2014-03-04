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
from iec import iec_unparameters
from uber import uber_lib

class iecUninputPage(webapp.RequestHandler):
    def get(self):
        text_file = open('iec/iec_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "IEC Uncertainty Inputs")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'iec','page':'un_input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start_un.html', {
                'model':'iec', 
                'model_attributes':'IEC Uncertainty Evaluation Inputs'})
        html = html + str(iec_unparameters.iecInp())
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + 'iec_uninput_jquery.html', {})
        html = html + template.render(templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', iecUninputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()