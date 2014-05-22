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
        <div class="input_nav">
            <ul>
                <li class="uutab model" style="color:#A31E39; font-weight:bold">Select model</li>
                <li class="uutab model_li" style="font-weight:bold; display:none"> | </li>
                <li class="uutab hdflr" style="font-weight:bold; display:none"> Hard Surface Floor Cleaner</li>
                <li class="uutab hdflr_li" style="font-weight:bold; display:none"> | </li>
                <li class="uutab vlflr" style="font-weight:bold; display:none"> Vinyl Floor</li>
                <li class="uutab vlflr_li" style="font-weight:bold; display:none"> | </li>
                <li class="uutab cpcln" style="font-weight:bold; display:none"> Carpet Cleaner</li>
                <li class="uutab cpcln_li" style="font-weight:bold; display:none"> | </li>
                <li class="uutab ipcap" style="font-weight:bold; display:none"> Impregnated Carpet</li>
                <li class="uutab ipcap_li" style="font-weight:bold; display:none"> | </li>
                <li class="uutab mactk" style="font-weight:bold; display:none"> Mattress Covers and Ticking</li>
                <li class="uutab mactk_li" style="font-weight:bold; display:none"> | </li>
                <li class="uutab ccpst" style="font-weight:bold; display:none"> Clothing/Textile Consumer Product Spray Treatment</li>
                <li class="uutab ccpst_li" style="font-weight:bold; display:none"> | </li>
                <li class="uutab ldtpr" style="font-weight:bold; display:none"> Laundry Detergent Preservative</li>
                <li class="uutab ldtpr_li" style="font-weight:bold; display:none"> | </li>
                <li class="uutab clopr" style="font-weight:bold; display:none"> Clothing/Textile Material Preservative</li>
                <li class="uutab clopr_li" style="font-weight:bold; display:none"> | </li>
                <li class="uutab impdp" style="font-weight:bold; display:none"> Impregnated Diapers</li>
                <li class="uutab impdp_li" style="font-weight:bold; display:none"> | </li>
                <li class="uutab cldst" style="font-weight:bold; display:none"> Sprayed Diapers</li>
                <li class="uutab cldst_li" style="font-weight:bold; display:none"> | </li>
                <li class="uutab impty" style="font-weight:bold; display:none"> Impregnated Toys</li>
                <li class="uutab impty_li" style="font-weight:bold; display:none"> | </li>
            </ul>
        </div>
        """
        html = html + """<br><table class="input_table tab tab_model" border="0">"""
        html = html + str(resexposure_parameters.resexposureInp_model())
        html = html + """</table><table class="input_table tab tab_hdflr" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_hdflr())
        html = html + """</table><table class="input_table tab tab_vlflr" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_vlflr())
        html = html + """</table><table class="input_table tab tab_cpcln" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_cpcln())
        html = html + """</table><table class="input_table tab tab_ipcap" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_ipcap())
        html = html + """</table><table class="input_table tab tab_mactk" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_mactk())
        html = html + """</table><table class="input_table tab tab_ccpst" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_ccpst())
        html = html + """</table><table class="input_table tab tab_ldtpr" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_ldtpr())
        html = html + """</table><table class="input_table tab tab_clopr" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_clopr())
        html = html + """</table><table class="input_table tab tab_impdp" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_impdp())
        html = html + """</table><table class="input_table tab tab_cldst" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_cldst())
        html = html + """</table><table class="input_table tab tab_impty" border="0" style="display:none">"""
        html = html + str(resexposure_parameters.resexposureInp_impty())

        html = html + template.render(templatepath + '04uberinput_tabbed_end_resexposure.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05hh_ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', resexposureInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()