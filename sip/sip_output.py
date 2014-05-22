# Screening Imbibiton Program v1.0 (SIP)

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
import sys
sys.path.append("../sip")
from sip import sip_model,sip_tables
from uber import uber_lib
import rest_funcs

class SIPExecutePage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        chemical_name = form.getvalue('chemical_name')
       # select_receptor = form.getvalue('select_receptor')
       # bw_bird = form.getvalue('body_weight_of_bird')
       # bw_mamm = form.getvalue('body_weight_of_mammal')
        sol = form.getvalue('solubility')
        ld50_a = form.getvalue('ld50_a')
        ld50_m = form.getvalue('ld50_m')
        aw_bird = form.getvalue('aw_bird')
        # tw_bird = form.getvalue('body_weight_of_the_tested_bird')
        aw_mamm = form.getvalue('aw_mamm')
        # tw_mamm = form.getvalue('body_weight_of_the_tested_mammal')
        mineau = form.getvalue('mineau_scaling_factor')
        noael = form.getvalue('NOAEL')
        noaec_d = form.getvalue('NOAEC_d')
        noaec_q = form.getvalue('NOAEC_q')
        noaec_o = form.getvalue('NOAEC_o')
        # noaec_o2 = form.getvalue('NOAEC_o2')
        Species_of_the_bird_NOAEC_CHOICES = form.getvalue('NOAEC_species')
        bw_quail = form.getvalue('bw_quail')
        bw_duck = form.getvalue('bw_duck')
        bwb_other = form.getvalue('bwb_other')
        bw_rat = form.getvalue('bw_rat')
        bwm_other = form.getvalue('bwm_other')
        b_species = form.getvalue('b_species')
        m_species = form.getvalue('m_species')
        sip_obj = sip_model.sip(True,True,'single',chemical_name, b_species, m_species, bw_quail, bw_duck, bwb_other, bw_rat, bwm_other, sol, ld50_a, ld50_m, aw_bird, mineau, aw_mamm, noaec_d, noaec_q, noaec_o, Species_of_the_bird_NOAEC_CHOICES, noael)
        text_file = open('sip/sip_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "SIP Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'sip','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'sip', 
                'model_attributes':'SIP Output'})     
        html = html + sip_tables.timestamp(sip_obj)
        html = html + sip_tables.table_all(sip_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, sip_obj.__dict__, "sip", "single")
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', SIPExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

    
    

