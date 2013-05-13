# Screening Imbibiton Program v1.0 (SIP)

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import sys
sys.path.append("../sip")
from sip import sip_model
from sip import sip_tables

class SIPExecutePage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        chemical_name = form.getvalue('chemical_name')
        select_receptor = form.getvalue('select_receptor')
        bw_bird = form.getvalue('body_weight_of_bird')
        bw_mamm = form.getvalue('body_weight_of_mammal')
        sol = form.getvalue('solubility')
        ld50 = form.getvalue('ld50')
        aw_bird = form.getvalue('body_weight_of_the_assessed_bird')
        tw_bird = form.getvalue('body_weight_of_the_tested_bird')
        aw_mamm = form.getvalue('body_weight_of_the_assessed_mammal')
        tw_mamm = form.getvalue('body_weight_of_the_tested_mammal')
        mineau = form.getvalue('mineau_scaling_factor')
        noaec = form.getvalue('NOAEC')
        noael = form.getvalue('NOAEL')
            
        text_file = open('sip/sip_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'sip','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'sip', 
                'model_attributes':'SIP Output'})     



        # html = html + sip_tables.table_1(chemical_name, select_receptor, bw_bird, bw_mamm, sol, ld50, aw_bird, tw_bird, aw_mamm, tw_mamm, mineau, noaec, noael)      

        html = html + sip_tables.table_all(chemical_name, select_receptor, bw_bird, bw_mamm, sol, ld50, aw_bird, tw_bird, aw_mamm, tw_mamm, mineau, noaec, noael)

       
        # html = html + """
        #  #pre-table 1
        # <table>
        # <tr><H3>User Inputs: Chemical Identity</H3></tr>
        # <tr><H4>Application and Chemical Information</H4></tr>
        # <tr></tr>
        # </table>
        # """
        # pvuheadings = sip_tables.getheaderpvu()
        # pvrheadings = sip_tables.getheaderpvr()
        # djtemplate = sip_tables.getdjtemplate()
        # tmpl = Template(djtemplate)

        # #table 1
        # t1data = sip_tables.gett1data(chemical_name, select_receptor, bw_bird, bw_mamm, sol, ld50, aw_bird, tw_bird, aw_mamm, tw_mamm, mineau, noaec, noael)
        # t1rows = sip_tables.gethtmlrowsfromcols(t1data,pvuheadings)
        # html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        # html = html + """
        #  #pre-table 2
        # <table>
        # <tr><H3>Outputs: Chemical Identity</H3></tr>
        # <tr><H4>Application and Chemical Information</H4></tr>
        # <tr></tr>
        # </table>
        # """
        # #table 2
        # t2data = sip_tables.gett2data(aw_bird, bw_bird, sol, ld50, tw_bird, mineau, noaec)
        # t2rows = sip_tables.gethtmlrowsfromcols(t1data,pvuheadings)
        # html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', SIPExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

    
    