# -*- coding: utf-8 -*-

# TREX
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from trex2 import trex2_model
from trex2 import trex2_tables


class TRexOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        chem_name = form.getvalue('chemical_name')
        use = form.getvalue('Use')
        formu_name = form.getvalue('Formulated_product_name')
        a_i = form.getvalue('percent_ai')
        a_i = float(a_i)/100
        Application_type = form.getvalue('Application_type')
        seed_crop = form.getvalue('seed_crop')
        p_i = form.getvalue('percent_incorporated')
        p_i = float(p_i)/100
        seed_treatment_formulation_name = form.getvalue('seed_treatment_formulation_name')
        den = form.getvalue('density_of_product')
        den = float(den)
        m_s_r_p = form.getvalue('maximum_seedling_rate_per_use')
        m_s_r_p = float(m_s_r_p)
        r_s = form.getvalue('row_sp') 
        r_s=float(r_s)
        b_w = form.getvalue('bandwidth')   #convert to ft
        b_w = float(b_w)/12
        n_a = float(form.getvalue('noa'))

        rate_out = []
        day_out = []

        for i in range(int(n_a)):
            j=i+1
            rate_temp = form.getvalue('rate'+str(j))
            rate_out.append(float(rate_temp))
            day_temp = form.getvalue('day'+str(j))
            day_out.append(day_temp)  

        if Application_type=='Seed Treatment':
           a_r_p=rate_out[0]       #coefficient used to estimate initial conc.
        else:
           a_r_p=0

        h_l = form.getvalue('Foliar_dissipation_half_life')
        ld50_bird = form.getvalue('avian_ld50')
        lc50_bird = form.getvalue('avian_lc50')
        NOAEC_bird = form.getvalue('avian_NOAEC')
        NOAEC_bird = float(NOAEC_bird)
        NOAEL_bird = form.getvalue('avian_NOAEL')
        NOAEL_bird = float(NOAEL_bird)
        
        Species_of_the_tested_bird = form.getvalue('Species_of_the_tested_bird')
        aw_bird_sm = form.getvalue('body_weight_of_the_assessed_bird_small')
        aw_bird_sm = float(aw_bird_sm)  
        aw_bird_md = form.getvalue('body_weight_of_the_assessed_bird_medium')
        aw_bird_md = float(aw_bird_md) 
        aw_bird_lg = form.getvalue('body_weight_of_the_assessed_bird_large')
        aw_bird_lg = float(aw_bird_lg)       
        if Species_of_the_tested_bird == 'Bobwhite quail':
            tw_bird = form.getvalue('bw_quail')
        elif  Species_of_the_tested_bird == 'Mallard duck':
            tw_bird = form.getvalue('bw_duck')  
        else:
            tw_bird = form.getvalue('bwb_other')      

        tw_bird = float(tw_bird)        
        x = form.getvalue('mineau_scaling_factor')
        ld50_mamm = form.getvalue('mammalian_ld50')
        lc50_mamm = form.getvalue('mammalian_lc50')
        lc50_mamm=float(lc50_mamm)        
        NOAEC_mamm = form.getvalue('mammalian_NOAEC')
        NOAEC_mamm = float(NOAEC_mamm)
        NOAEL_mamm = form.getvalue('mammalian_NOAEL')

        aw_mamm_sm = form.getvalue('body_weight_of_the_assessed_mammal_small')
        aw_mamm_sm = float(aw_mamm_sm)  
        aw_mamm_md = form.getvalue('body_weight_of_the_assessed_mammal_medium')
        aw_mamm_md = float(aw_mamm_md) 
        aw_mamm_lg = form.getvalue('body_weight_of_the_assessed_mammal_large')
        aw_mamm_lg = float(aw_mamm_lg)               
        tw_mamm = form.getvalue('body_weight_of_the_tested_mammal')
        tw_mamm = float(tw_mamm) 

        text_file = open('trex2/trex2_description.txt','r')
        x1 = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'trex2','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'trex2', 
                'model_attributes':'T-Rex 1.5.1 Output'})

        html = html + trex2_tables.table_1(chem_name, use, formu_name, 100*a_i, Application_type, r_s, 12*b_w, 100*p_i, den, h_l)
        html = html + trex2_tables.table_2(n_a, rate_out, day_out)
        html = html + trex2_tables.table_3(ld50_bird, lc50_mamm, NOAEC_bird, NOAEL_mamm, aw_bird_sm, aw_bird_md, 
                                           aw_bird_lg, Species_of_the_tested_bird, tw_bird, x)
        html = html + trex2_tables.table_4(ld50_mamm, lc50_mamm, NOAEC_mamm, NOAEL_mamm, aw_mamm_sm, aw_mamm_md, 
                                           aw_mamm_lg, tw_mamm)


        if Application_type == 'Seed Treatment':

            html = html + trex2_tables.table_5(Application_type, a_r_p, a_i, den, ld50_bird, aw_bird_sm, tw_bird, x, m_s_r_p, 
                                               NOAEC_bird, ld50_mamm, aw_mamm_sm, tw_mamm, NOAEL_mamm, aw_bird_md, aw_mamm_md, aw_bird_lg, aw_mamm_lg)

        else:

            html = html + trex2_tables.table_6(Application_type, n_a, rate_out, a_i, h_l, day_out)
            html = html + trex2_tables.table_7(aw_bird_sm, aw_bird_md, aw_bird_lg, n_a, rate_out, a_i, h_l, day_out)
            html = html + trex2_tables.table_8(lc50_bird, NOAEC_bird, n_a, rate_out, a_i, h_l, day_out)  
            html = html + trex2_tables.table_9(aw_mamm_sm, aw_mamm_md, aw_mamm_lg, n_a, rate_out, a_i, h_l, day_out)
            html = html + trex2_tables.table_10(aw_mamm_sm, aw_mamm_md, aw_mamm_lg, ld50_mamm, NOAEL_mamm, tw_mamm, n_a, rate_out, a_i, h_l, day_out)
            html = html + trex2_tables.table_11(lc50_mamm, NOAEC_bird, n_a, rate_out, a_i, h_l, day_out)


        if Application_type == 'Row/Band/In-furrow-Granular':

            html = html + trex2_tables.table_12(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_bird_sm, aw_mamm_sm, aw_bird_md, aw_mamm_md, aw_bird_lg, aw_mamm_lg, ld50_bird, ld50_mamm, tw_bird, tw_mamm, x)


        elif Application_type == 'Row/Band/In-furrow-Liquid':

            html = html + trex2_tables.table_13(Application_type, rate_out, a_i, p_i, b_w, aw_bird_sm, aw_mamm_sm, aw_bird_md, aw_mamm_md, aw_bird_lg, aw_mamm_lg, ld50_bird, ld50_mamm, tw_bird, tw_mamm, x)

        elif Application_type == 'Broadcast-Granular':

            html = html + trex2_tables.table_14(Application_type, rate_out, a_i, p_i, aw_bird_sm, aw_mamm_sm, aw_bird_md, aw_mamm_md, aw_bird_lg, aw_mamm_lg, ld50_bird, ld50_mamm, tw_bird, tw_mamm, x)

        elif Application_type == 'Broadcast-Liquid':

            html = html + trex2_tables.table_15(Application_type, rate_out, a_i, p_i, aw_bird_sm, aw_mamm_sm, aw_bird_md, aw_mamm_md, aw_bird_lg, aw_mamm_lg, ld50_bird, ld50_mamm, tw_bird, tw_mamm, x)          

        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TRexOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    