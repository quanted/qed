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
from JonTest import JonTest_parameters

class genericInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheaderJon.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'generic_hh','page':'input'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'JonTest', 
                'model_attributes':'JonTest Inputs'})
        html = html + str(JonTest_parameters.JonTestInp())
        html = html + template.render(templatepath + '04uberinput_endJon.html', {'sub_title': 'Submit'})
        html = html + """
        <script type="text/javascript" src="/stylesheets/style_JonTest.js"></script>"""
        html = html + template.render(templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', genericInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()