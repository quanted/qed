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
from ore import ore_parameters

class oreInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})
        html = html + template.render (templatepath + 'ore-jquery.html', {})
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'ore','page':'input'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_ore_start.html', {
                'model':'ore', 
                'model_attributes':'ORE Inputs'})
        html = html + template.render (templatepath + '04uberinput_tabbed_nav.html', {
                'nav_dict': {
                    'class_name': ['ToxInp', 'CropTargetSel', 'OccHandler'],
                    'tab_label': ['Toxicity & Exposure', 'Crop-Target Category Lookup', 'Occupational Handler Exposure']
                    }
                })
        html = html + str(ore_parameters.form())
        html = html + template.render(templatepath + '04uberinput_ore_end.html', {'sub_title': 'Submit'})
        # html = html + template.render(templatepath + '05hh_ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', oreInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()