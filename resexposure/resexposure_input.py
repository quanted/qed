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
from resexposure import resexposure_parameters

class resexposureInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})
        html = html + template.render (templatepath + 'resexposure-jquery.html', {})
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'resexposure','page':'input'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start_tabbed.html', {
                'model':'resexposure', 
                'model_attributes':'Residential Exposure Model Inputs'})
        html = html + """
        <div id="input_nav">
            <ul>
                <li class="model" style="color:#FFA500; font-weight:bold">Select model</li>
                <li class="hdflr" style="font-weight:bold; display:none"> | Hard Surface Floor Cleaner</li>
                <li class="vlflr" style="font-weight:bold; display:none"> | Vinyl Floor</li>
                <li class="cpcln" style="font-weight:bold; display:none"> | Carpet Cleaner</li>
            </ul>
        </div>
        """
        #
        html = html + """<br><table class="tab tab_model" border="0">"""
        html = html + str(resexposure_parameters.resexposureInp_model())
        html = html + """</table><table class="tab tab_hdflr" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_hdflr())
        html = html + """</table><table class="tab tab_vlflr" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_vlflr())
        html = html + """</table><table class="tab tab_cpcln" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_cpcln())
        html = html + template.render(templatepath + '04uberinput_tabbed_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05hh_ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', resexposureInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()