import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import logging
import sys
sys.path.append("../utils")
import utils.json_utils
sys.path.append("../agdrift")
from agdrift import agdrift_model,agdrift_tables
from uber import uber_lib
from django.template import Context, Template
from django.utils import simplejson
import rest_funcs

class agdriftOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
       # args={}
        #for keys in form:
        #    args[keys]=form.getvalue(keys)
        drop_size = form.getvalue('drop_size')
        ecosystem_type = form.getvalue('ecosystem_type')
        application_method = form.getvalue('application_method')
        boom_height = form.getvalue('boom_height')
        orchard_type = form.getvalue('orchard_type')
        application_rate = form.getvalue('application_rate')
        aquatic_type = form.getvalue('aquatic_type')
        distance = form.getvalue('distance')
        calculation_input = form.getvalue('calculation_input')
        # init_avg_dep_foa = form.getvalue('init_avg_dep_foa')
        # avg_depo_gha = form.getvalue('avg_depo_gha')
        # avg_depo_lbac = form.getvalue('avg_depo_lbac')
        # deposition_ngL = form.getvalue('deposition_ngL')
        # deposition_mgcm = form.getvalue('deposition_mgcm')
        # nasae = form.getvalue('nasae')
        # y = form.getvalue('y')
        # x = form.getvalue('x')
        # express_y = form.getvalue('express_y')
        agdrift_obj = agdrift_model.agdrift(True, True, 'single',drop_size, ecosystem_type, application_method, boom_height, orchard_type, application_rate, distance, aquatic_type, calculation_input, None)
        text_file = open('agdrift/agdrift_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "AgDrift Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'agdrift','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'agdrift', 
                'model_attributes':'AgDrift Output'})

        html = html + agdrift_tables.timestamp(agdrift_obj)
        html = html + agdrift_tables.table_all(agdrift_obj)
        

        # <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        # <div class="out_">
        #     <table class="out_">
        #         <tr>
        #             <th colspan="2">Inputs: Chemical Identity</th>
        #         </tr>
        #         <tr>
        #             <td>Application method</td>
        #             <td id="app_method_val">%s</td>
        #         </tr>
        #         <tr id="Orc_type">
        #             <td>Orchard type</td>
        #             <td>%s</td>
        #         </tr>
        #         <tr>
        #             <td>Drop size</td>
        #             <td>%s</td>
        #         </tr>
        #         <tr>
        #             <td>Ecosystem type</td>
        #             <td>%s</td>
        #         </tr>
        #     </table>
        # </div>
        # """ % (application_method, orchard_type, drop_size, ecosystem_type)
        # html = html +  """
        # <table style="display:none;">
        #     <tr>
        #         <td>distance</td>
        #         <td id="distance">%s</td>
        #     </tr>
        #     <tr>
        #         <td>deposition</td>
        #         <td id="deposition">%s</td>
        #     </tr>
        # </table>
        # <br>
        # <h3 class="out_2 collapsible" id="section2"><span></span>Results</h3>
        #<div>
       # """%(results[0], results[1])

        html = html + template.render(templatepath + 'agdrift-output-jqplot_header.html', {})

        html = html +  """
        </div>
        """
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, agdrift_obj.__dict__, "agdrift", "single")
        self.response.out.write(html)
          
app = webapp.WSGIApplication([('/.*', agdriftOutputPage)], debug=True)
        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()