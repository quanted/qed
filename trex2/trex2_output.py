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
from trex2 import trex2_model, trex2_tables
from uber import uber_lib
import rest_funcs
import logging
logger = logging.getLogger('trex2 out')

class TRexOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        chem_name = form.getvalue('chemical_name')
        use = form.getvalue('Use')
        formu_name = form.getvalue('Formulated_product_name')
        a_i = form.getvalue('percent_ai')
        a_i = float(a_i)/100
        Application_type = form.getvalue('Application_type')
        seed_crop = float(form.getvalue('seed_crop'))
        seed_crop_v = form.getvalue('seed_crop_v')
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

        if Application_type=='Seed Treatment':
           n_a = 1
        else:
           n_a = float(form.getvalue('noa'))
        
        rate_out = []
        day_out = []
        for i in range(int(n_a)):
           j=i+1
           rate_temp = form.getvalue('rate'+str(j))
           rate_out.append(float(rate_temp))
           day_temp = float(form.getvalue('day'+str(j)))
           day_out.append(day_temp)  

        h_l = form.getvalue('Foliar_dissipation_half_life')
        ld50_bird = form.getvalue('avian_ld50')
        lc50_bird = form.getvalue('avian_lc50')
        NOAEC_bird = float(form.getvalue('avian_NOAEC'))
        try:
            NOAEL_bird = float(form.getvalue('avian_NOAEL'))
        except:
            NOAEL_bird = 'N/A'
        aw_bird_sm = form.getvalue('body_weight_of_the_assessed_bird_small')
        aw_bird_sm = float(aw_bird_sm)  
        aw_bird_md = form.getvalue('body_weight_of_the_assessed_bird_medium')
        aw_bird_md = float(aw_bird_md) 
        aw_bird_lg = form.getvalue('body_weight_of_the_assessed_bird_large')
        aw_bird_lg = float(aw_bird_lg)       
        
        Species_of_the_tested_bird_avian_ld50 = form.getvalue('Species_of_the_tested_bird_avian_ld50')
        Species_of_the_tested_bird_avian_lc50 = form.getvalue('Species_of_the_tested_bird_avian_lc50')
        Species_of_the_tested_bird_avian_NOAEC = form.getvalue('Species_of_the_tested_bird_avian_NOAEC')
        Species_of_the_tested_bird_avian_NOAEL = form.getvalue('Species_of_the_tested_bird_avian_NOAEL')

        tw_bird_ld50 = float(form.getvalue('bw_avian_ld50'))
        tw_bird_lc50 = float(form.getvalue('bw_avian_lc50'))
        tw_bird_NOAEC = float(form.getvalue('bw_avian_NOAEC'))
        tw_bird_NOAEL = float(form.getvalue('bw_avian_NOAEL'))

        x = form.getvalue('mineau_scaling_factor')
        ld50_mamm = form.getvalue('mammalian_ld50')
        try:
            lc50_mamm = float(form.getvalue('mammalian_lc50'))
        except:
            lc50_mamm = 'N/A'
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
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "TREX 1.5.2 Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'trex2','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'trex2', 
                'model_attributes':'T-Rex 1.5.2 Output'})

        trex2_obj = trex2_model.trex2("single", chem_name, use, formu_name, a_i, Application_type, seed_treatment_formulation_name, seed_crop, seed_crop_v, r_s, b_w, p_i, den, h_l, n_a, rate_out, day_out,
                      ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, aw_bird_sm, aw_bird_md, aw_bird_lg, 
                      Species_of_the_tested_bird_avian_ld50, Species_of_the_tested_bird_avian_lc50, Species_of_the_tested_bird_avian_NOAEC, Species_of_the_tested_bird_avian_NOAEL,
                      tw_bird_ld50, tw_bird_lc50, tw_bird_NOAEC, tw_bird_NOAEL, x, ld50_mamm, lc50_mamm, NOAEC_mamm, NOAEL_mamm, aw_mamm_sm, aw_mamm_md, aw_mamm_lg, tw_mamm,
                      m_s_r_p)
        
        html = html + trex2_tables.timestamp(trex2_obj)
        html = html + trex2_tables.table_all(trex2_obj)[0]
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        logger.info(trex2_obj.__dict__)
        rest_funcs.save_dic(html, trex2_obj.__dict__, "trex2", "single")
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TRexOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    

