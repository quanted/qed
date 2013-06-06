# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from therps import therps_model
from therps import therps_tables


class THerpsOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
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
        ld50_bird = form.getvalue('avian_ld50')
        ld50_bird = float(ld50_bird)
        lc50_bird = form.getvalue('avian_lc50')
        lc50_bird = float(lc50_bird)
        NOAEC_bird = form.getvalue('avian_NOAEC')
        NOAEC_bird = float(NOAEC_bird)
        NOAEL_bird = form.getvalue('avian_NOAEL')    
        NOAEL_bird = float(NOAEL_bird)
        Species_of_the_tested_bird = form.getvalue('Species_of_the_tested_bird')    

        tw_bird = form.getvalue('body_weight_of_the_tested_bird')
        tw_bird = float(tw_bird)        
        x = form.getvalue('mineau_scaling_factor')
        x = float(x)
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
        
        text_file = open('therps/therps_description.txt','r')
        x1 = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'therps','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                        
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'therps', 
                'model_attributes':'T-Herps Output'})

        html = html + therps_tables.table_all(chem_name, use, formu_name, a_i, h_l, n_a, i_a, a_r, ld50_bird, 
                                              lc50_bird, NOAEC_bird, NOAEL_bird, Species_of_the_tested_bird, tw_bird,
                                              x, bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, 
                                              wp_herp_a_lg, c_mamm_a, c_herp_a)[0]
 
        html = html + template.render(templatepath + 'export.html', {})       
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', THerpsOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    