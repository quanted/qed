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
sys.path.append("../therps")
from agdrift import agdrift_model,agdrift_tables
from therps import therps_model,therps_tables
from uber import uber_lib
from django.template import Context, Template
from django.utils import simplejson
import logging

#logger = logging.getLogger('trex2 Model')

class agdrift_therpsOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        #print form
       # args={}
        #for keys in form:
        #    args[keys]=form.getvalue(keys)
        drop_size = form.getvalue('drop_size')
        ecosystem_type = form.getvalue('ecosystem_type')
        application_method = form.getvalue('application_method')
        boom_height = form.getvalue('boom_height')
        orchard_type = form.getvalue('orchard_type')
        # application_rate = form.getvalue('application_rate')
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

        chem_name = form.getvalue('chemical_name')
        use = form.getvalue('Use')
        formu_name = form.getvalue('Formulated_product_name')
        a_i = form.getvalue('percent_ai')
        a_i = float(a_i)/100
        a_r = form.getvalue('application_rate')
        a_r = float(a_r)         
        n_a = form.getvalue('number_of_applications')
        n_a = float(n_a)

        i_a = form.getvalue('interval_between_applications')
        i_a = float(i_a)
        h_l = form.getvalue('Foliar_dissipation_half_life')
        h_l = float(h_l)        
        avian_ld50 = float(form.getvalue('avian_ld50'))
        avian_lc50 = float(form.getvalue('avian_lc50'))
        avian_NOAEC = float(form.getvalue('avian_NOAEC'))
        avian_NOAEL = float(form.getvalue('avian_NOAEL'))

        Species_of_the_tested_bird_avian_ld50 = form.getvalue('Species_of_the_tested_bird_avian_ld50')
        Species_of_the_tested_bird_avian_lc50 = form.getvalue('Species_of_the_tested_bird_avian_lc50')
        Species_of_the_tested_bird_avian_NOAEC = form.getvalue('Species_of_the_tested_bird_avian_NOAEC')
        Species_of_the_tested_bird_avian_NOAEL = form.getvalue('Species_of_the_tested_bird_avian_NOAEL')

        bw_avian_ld50 = float(form.getvalue('bw_avian_ld50'))
        bw_avian_lc50 = float(form.getvalue('bw_avian_lc50'))
        bw_avian_NOAEC = float(form.getvalue('bw_avian_NOAEC'))
        bw_avian_NOAEL = float(form.getvalue('bw_avian_NOAEL'))

        mineau_scaling_factor = form.getvalue('mineau_scaling_factor')
        mineau_scaling_factor = float(mineau_scaling_factor)
        c_mamm_a = form.getvalue('body_weight_of_the_consumed_mammal_a')
        c_mamm_a = float(c_mamm_a)
        c_herp_a = form.getvalue('body_weight_of_the_consumed_herp_a')
        c_herp_a = float(c_herp_a)    

        bw_herp_a_sm = form.getvalue('BW_herptile_a_sm')
        bw_herp_a_sm = float(bw_herp_a_sm)
        bw_herp_a_md = form.getvalue('BW_herptile_a_md')
        bw_herp_a_md = float(bw_herp_a_md)
        bw_herp_a_lg = form.getvalue('BW_herptile_a_lg')
        bw_herp_a_lg = float(bw_herp_a_lg)

        wp_herp_a_sm = form.getvalue('W_p_a_sm')
        wp_herp_a_sm = float(wp_herp_a_sm)/100      
        wp_herp_a_md = form.getvalue('W_p_a_md')
        wp_herp_a_md = float(wp_herp_a_md)/100   
        wp_herp_a_lg = form.getvalue('W_p_a_lg')
        wp_herp_a_lg = float(wp_herp_a_lg)/100   
        
        #print rate_out
        agdrift_obj = agdrift_model.agdrift(True, True, drop_size, ecosystem_type, application_method, boom_height, orchard_type, a_r, distance, aquatic_type, calculation_input)
        #logger.info(type(agdrift_obj.init_avg_dep_foa))
        therps_obj = therps_model.therps(chem_name, use, formu_name, a_i, h_l, n_a, i_a, a_r, avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, 
                                         Species_of_the_tested_bird_avian_ld50, Species_of_the_tested_bird_avian_lc50, Species_of_the_tested_bird_avian_NOAEC, Species_of_the_tested_bird_avian_NOAEL,
                                         bw_avian_ld50, bw_avian_lc50, bw_avian_NOAEC, bw_avian_NOAEL,
                                         mineau_scaling_factor, bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, 
                                         wp_herp_a_lg, c_mamm_a, c_herp_a)
        # trex_obj = trex2_model.trex2('single', chem_name, use, formu_name, a_i, Application_type, seed_treatment_formulation_name, seed_crop, seed_crop_v, r_s, b_w, p_i, den, h_l, n_a, [agdrift_obj.init_avg_dep_foa*i for i in rate_out], day_out,
        #               ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, aw_bird_sm, aw_bird_md, aw_bird_lg, 
        #               Species_of_the_tested_bird_avian_ld50, Species_of_the_tested_bird_avian_lc50, Species_of_the_tested_bird_avian_NOAEC, Species_of_the_tested_bird_avian_NOAEL,
        #               tw_bird_ld50, tw_bird_lc50, tw_bird_NOAEC, tw_bird_NOAEL, x, ld50_mamm, lc50_mamm, NOAEC_mamm, NOAEL_mamm, aw_mamm_sm, aw_mamm_md, aw_mamm_lg, tw_mamm,
        #               m_s_r_p)
        text_file = open('agdrift/agdrift_description.txt','r')
        x = text_file.read()
        text_file = open('therps/therps_description.txt','r')
        x1 = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "AgDrift-T-Herps Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'agdrift','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'agdrift_therps', 
                'model_attributes':'AgDrift-T-Herps Output'})

        #html = html + therps_tables.timestamp(therps_obj, '')
        html = html + agdrift_tables.table_all(agdrift_obj)
        # html = html + trex2_tables.timestamp()
        html = html + therps_tables.table_all(therps_obj)[0]
        

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
        self.response.out.write(html)
          
app = webapp.WSGIApplication([('/.*', agdrift_therpsOutputPage)], debug=True)
        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()