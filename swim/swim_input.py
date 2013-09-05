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
from swim import swim_parameters

class swimInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})
        html = html + template.render (templatepath + 'swim-jquery.html', {})
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'swim','page':'input'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start_tabbed.html', {
                'model':'swim', 
                'model_attributes':'SWIM Inputs'})
        html = html + """
        <div class="input_nav">
            <ul>
                <li class="chem" style="color:#A31E39; font-weight:bold">Chemical</li>
                |<li class="ad" style="font-weight:bold"> Adult</li>
                |<li class="c1" style="font-weight:bold"> Children 6-11</li>
                |<li class="c2" style="font-weight:bold"> Children 11-16</li>
            </ul>
        </div>
        """
        html = html + """<br><table class="tab tab_chem" border="0">"""
        html = html + str(swim_parameters.swimInp_chem())
        html = html + """</table><table class="tab tab_ad" border="0" style="display:none">"""
        html = html + str(swim_parameters.swimInp_ad())
        html = html + """</table><table class="tab tab_c1" border="0" style="display:none">"""
        html = html + str(swim_parameters.swimInp_c1())
        html = html + """</table><table class="tab tab_c2" border="0" style="display:none">"""
        html = html + str(swim_parameters.swimInp_c2())
        html = html + template.render(templatepath + '04uberinput_tabbed_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05hh_ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', swimInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()