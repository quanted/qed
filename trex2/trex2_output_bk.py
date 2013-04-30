# -*- coding: utf-8 -*-

# TREX
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
#from trex import trex_input
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
      #  a_r = form.getvalue('application_rate')
     #   a_r = float(a_r)        
     #   a_r_l = form.getvalue('application_rate_l')
     #   a_r_l=float(a_r_l)        
        seed_treatment_formulation_name = form.getvalue('seed_treatment_formulation_name')
        den = form.getvalue('density_of_product')
        den = float(den)
        m_s_r_p = form.getvalue('maximum_seedling_rate_per_use')
        m_s_r_p = float(m_s_r_p)
        #a_r_p = form.getvalue('application_rate_per_use')
        #a_r_p = float(a_r_p)
        r_s = form.getvalue('row_sp') 
        r_s=float(r_s)
        b_w = form.getvalue('bandwidth')   #convert to ft
        b_w = float(b_w)/12
        n_a = float(form.getvalue('noa'))

        # rate_out = np.zeros(shape=(int(n_a),1))
        # day_out = np.zeros(shape=(int(n_a),1))
        

        # for i in range(int(n_a)):
        #     j=i+1
        #     rate_temp = form.getvalue('rate'+str(j))
        #     rate_out[i,] = int(rate_temp) 
        #     day_temp = form.getvalue('day'+str(j))
        #     day_out[i,] = int(day_temp)         
            
        rate_out = []
        day_out = []
        

        for i in range(int(n_a)):
            j=i+1
            rate_temp = form.getvalue('rate'+str(j))
            rate_out.append(float(rate_temp))
            day_temp = form.getvalue('day'+str(j))
            day_out.append(day_temp)  

        # a_t = form.getvalue('Application_target')
        # if a_t=='Short grass':
        #    para=240       #coefficient used to estimate initial conc.
        # elif a_t=='Tall grass':
        #    para=110
        # elif a_t=='Broad-leafed plants/small insects':
        #    para=135
        # elif a_t=='Fruits/pods/seeds/large insects':
        #    para=15
        # elif a_t=='Arthropods': #new coefficient for Arthropods
        #    para=94
        #i_a = form.getvalue('interval_between_applications')
        if Application_type=='Seed Treatment':
           a_r_p=rate_out[0]       #coefficient used to estimate initial conc.
        else:
           a_r_p=0
     #   print 'a_r_p', a_r_p
        h_l = form.getvalue('Foliar_dissipation_half_life')
        ld50_bird = form.getvalue('avian_ld50')
        lc50_bird = form.getvalue('avian_lc50')
        NOAEC_bird = form.getvalue('avian_NOAEC')
        NOAEC_bird = float(NOAEC_bird)
        NOAEL_bird = form.getvalue('avian_NOAEL')
        NOAEL_bird = float(NOAEL_bird)
        
#        bird_type = form.getvalue('Bird_type')    
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

        #tw_bird = form.getvalue('body_weight_of_the_tested_bird')
        tw_bird = float(tw_bird)        
        x = form.getvalue('mineau_scaling_factor')
        ld50_mamm = form.getvalue('mammalian_ld50')
        lc50_mamm = form.getvalue('mammalian_lc50')
        lc50_mamm=float(lc50_mamm)        
        NOAEC_mamm = form.getvalue('mammalian_NOAEC')
        NOAEC_mamm = float(NOAEC_mamm)
        NOAEL_mamm = form.getvalue('mammalian_NOAEL')
#        mammal_type = form.getvalue('Mammal_type')                
#        if mammal_type =='Herbivores and insectivores':
#           mf_w_mamm=0.8       #coefficient used to estimate initial conc.
#        elif mammal_type=='Granivores':
#           mf_w_mamm=0.1 
#        if bird_type =='Herbivores and insectivores':
#           mf_w_bird=0.8       #coefficient used to estimate initial conc.
#        elif bird_type=='Granivores':
#           mf_w_bird=0.1            
        aw_mamm_sm = form.getvalue('body_weight_of_the_assessed_mammal_small')
        aw_mamm_sm = float(aw_mamm_sm)  
        aw_mamm_md = form.getvalue('body_weight_of_the_assessed_mammal_medium')
        aw_mamm_md = float(aw_mamm_md) 
        aw_mamm_lg = form.getvalue('body_weight_of_the_assessed_mammal_large')
        aw_mamm_lg = float(aw_mamm_lg)               
        tw_mamm = form.getvalue('body_weight_of_the_tested_mammal')
        tw_mamm = float(tw_mamm) 
        
        #mf_w_mamm = form.getvalue('mass_fraction_of_water_in_the_mammal_food')
        #mf_w_bird = form.getvalue('mass_fraction_of_water_in_the_bird_food')
        
        text_file = open('trex2/trex2_description.txt','r')
        x1 = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'trex2','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'trex2', 
                'model_attributes':'T-Rex 1.5.1 Output'})

        html = html + trex2_tables.table_1(chem_name, use, formu_name, 100*a_i, Application_type, 100*p_i)

        html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Inputs</div></th>
                            <th scope="col">Value</div></th>
                            <th scope="col">Inputs</div></th>
                            <th scope="col">Value</div></th>                            
                          </tr>
                          <tr>
                            <td>Chemical name</td>
                            <td>%s</td>
                            <td>Use</td>
                            <td>%s</td>                          
                          </tr>
                          <tr>
                            <td>Formulated product name</td>
                            <td>%s</td>
                            <td>Percentage active ingredient</td>
                            <td>%s%%</td>  
                          </tr>
                          <tr>
                            <td>Application type</td>
                            <td>%s</td>
                            <td>Percentage incorporated</td>
                            <td>%s%%</td>
                          </tr>
                          <tr>
                            <td>Density of product (lbs/gal)</td>
                            <td>%s</td>
                          </tr>                                                    
                          <tr>
                            <td>Number of applications</td>
                            <td>%s</td>
                          </tr>                              
                          <tr>                            
                            <td>Foliar dissipation half-life (days)</td>
                            <td>%s</td>
                          </tr>                              
                          <tr>                            
                            <td>Avian LD50 (mg/kg-bw)</td>
                            <td>%s</td>
                            <td>Avian LC50 (mg/kg-diet)</td>
                            <td>%s</td>
                          </tr>    
                          <tr>                            
                            <td>Avian NOAEC (mg/kg-diet)</td>
                            <td>%s</td>
                            <td>Avian NOAEL (mg/kg-bw)</td>
                            <td>%s</td>
                          </tr>    
                          <tr>                            
                            <td>Body weight of assessed bird (g)</td>
                            <td>%s</td>
                            <td>Body weight of tested bird (g)</td>
                            <td>%s</td>                                                   
                          </tr>    
                          <tr>
                            <td>Mineau scaling factor</td>
                            <td>%s</td>
                            <td>Mammalian LD50 (mg/kg-bw)</td>
                            <td>%s</td>                                                    
                          </tr>    
                          <tr>                            
                            <td>Mammalian LC50 (mg/kg-diet)</td>
                            <td>%s</td>
                            <td>Mammalian NOAEC (mg/kg-diet)</td>
                            <td>%s</td>                                                                             
                          </tr>    
                          <tr>
                            <td>Mammalian NOAEL (mg/kg-bw)</td>
                            <td>%s</td>
                            <td>Body weight of assessed mammal (g)</td>
                            <td>%s</td>
                          </tr>                           
                          <tr>
                            <td>Body weight of tested mammal (g)</td>
                            <td>%s</td>
                            <td>&nbsp;</td>
                            <td>&nbsp;</td>                            
                          </tr>                                                              
                        </table>
                        <br>                     
                        """%(chem_name, use, formu_name, 100*a_i, Application_type, 100*p_i, den, 
                            n_a, h_l, ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, aw_bird_sm, tw_bird, x, ld50_mamm, 
                               lc50_mamm, NOAEC_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm)         
        if Application_type == 'Seed Treatment':
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Size</div></th>
                            <th scope="col">Acute #1</div></th> 
                            <th scope="col">Acute #2</div></th>                          
                            <th scope="col">Chronic</div></th>
                            <th scope="col">Acute #1</div></th> 
                            <th scope="col">Acute #2</div></th>                          
                            <th scope="col">Chronic</div></th>  
                          </tr>
                          <tr>
                            <td>Small</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>   
                          <tr>
                            <td>Medium</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>  
                          <tr>
                            <td>Large</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          """%(trex2_model.sa_bird_1(a_r_p, a_i, den, trex2_model.at_bird,trex2_model.fi_bird, ld50_bird, aw_bird_sm, tw_bird, x), 
                               trex2_model.sa_bird_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_bird, ld50_bird, aw_bird_sm, tw_bird, x), 
                               trex2_model.sc_bird(a_r_p, a_i, den, NOAEC_bird),
                               trex2_model.sa_mamm_1(a_r_p, a_i, den, trex2_model.at_mamm, trex2_model.fi_mamm, ld50_mamm, aw_mamm_sm, tw_mamm),
                               trex2_model.sa_mamm_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_mamm, ld50_mamm, aw_mamm_sm, tw_mamm),
                               trex2_model.sc_mamm(a_r_p, a_i, den, NOAEL_mamm,aw_mamm_sm,tw_mamm, trex2_model.ANOAEL_mamm),
                               trex2_model.sa_bird_1(a_r_p, a_i, den, trex2_model.at_bird,trex2_model.fi_bird, ld50_bird, aw_bird_md, tw_bird, x), 
                               trex2_model.sa_bird_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_bird, ld50_bird, aw_bird_md, tw_bird, x), 
                               trex2_model.sc_bird(a_r_p, a_i, den, NOAEC_bird),
                               trex2_model.sa_mamm_1(a_r_p, a_i, den, trex2_model.at_mamm, trex2_model.fi_mamm, ld50_mamm, aw_mamm_md, tw_mamm),
                               trex2_model.sa_mamm_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_mamm, ld50_mamm, aw_mamm_md, tw_mamm),
                               trex2_model.sc_mamm(a_r_p, a_i, den, NOAEL_mamm,aw_mamm_md,tw_mamm, trex2_model.ANOAEL_mamm),
                               trex2_model.sa_bird_1(a_r_p, a_i, den, trex2_model.at_bird,trex2_model.fi_bird, ld50_bird, aw_bird_lg, tw_bird, x), 
                               trex2_model.sa_bird_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_bird, ld50_bird, aw_bird_lg, tw_bird, x), 
                               trex2_model.sc_bird(a_r_p, a_i, den, NOAEC_bird),
                               trex2_model.sa_mamm_1(a_r_p, a_i, den, trex2_model.at_mamm, trex2_model.fi_mamm, ld50_mamm, aw_mamm_lg, tw_mamm),
                               trex2_model.sa_mamm_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_mamm, ld50_mamm, aw_mamm_lg, tw_mamm),
                               trex2_model.sc_mamm(a_r_p, a_i, den, NOAEL_mamm,aw_mamm_lg,tw_mamm, trex2_model.ANOAEL_mamm)) 
        else:    
            html = html + """<table width="600" border=                          <tr>
                            <th scope="col">Dietary based EECs (ppm)</div></th>
                            <th scope="col">Value</div></th>                          
                          </tr>
                          <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                          </tr>                           
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                          </tr>                           
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                          </tr>                           
                          <tr>
                            <td>Fruits/Pods/Seeds</td>
                            <td>%.2f</td>   
                          </tr>                           
                          <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>                        
                          </tr>
                        """%(trex2_model.EEC_diet(trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out),trex2_model.EEC_diet(trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out),trex2_model.EEC_diet(trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out),trex2_model.EEC_diet(trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out),trex2_model.EEC_diet(trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out))                        
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Avian Dosed Based EECs</div></th>
                            <th scope="col">Small</div></th>       
                            <th scope="col">Mid</div></th> 
                            <th scope="col">Large</div></th>                    
                          </tr>
                          <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>   
                            <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                           <tr>
                            <td>Fruits/Pods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                           <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                            <tr>
                            <td>Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                        """%(trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out), trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out),trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out),trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out))                      
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Avian Dosed Based RQs</div></th>
                            <th scope="col">Small</div></th>       
                            <th scope="col">Mid</div></th> 
                            <th scope="col">Large</div></th>                    
                          </tr>
                          <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>   
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>   
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Fruits/Pods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                        """%(trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out),
                            trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out),
                            trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out),
                            trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out),
                            trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out),
                            trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out),trex2_model.ARQ_dose_bird(trex2_model.EEC_dose_bird, trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, trex2_model.at_bird, ld50_bird, tw_bird, x, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out))
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Avian Diet Based RQs</div></th>
                            <th scope="col">Acute</div></th>       
                            <th scope="col">Chronic</div></th>                  
                          </tr>
                           <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Fruits/Pods/Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                           <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                        """%(trex2_model.ARQ_diet_bird(trex2_model.EEC_diet, lc50_bird, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out),
                            trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l,day_out),
                            trex2_model.ARQ_diet_bird(trex2_model.EEC_diet, lc50_bird, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l,day_out),
                            trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l,day_out),
                            trex2_model.ARQ_diet_bird(trex2_model.EEC_diet, lc50_bird, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out),
                            trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out),
                            trex2_model.ARQ_diet_bird(trex2_model.EEC_diet, lc50_bird, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out) ,
                            trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out),
                            trex2_model.ARQ_diet_bird(trex2_model.EEC_diet, lc50_bird, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out) ,
                            trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)) 
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Mammalian Dose Based EECs (mg/kg-bw)</div></th>
                            <th scope="col">Small</div></th>       
                            <th scope="col">Medium</div></th> 
                            <th scope="col">Large</div></th>                  
                          </tr>
                           <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Fruits/Pods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                        """%(trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out),
                            trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out),
                            trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out),
                            trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out),
                            trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out),
                            trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out))
            html = html + """<table width="600" border="1">
                          <tr>
                            <th rowspan="2">Mammalian Dose Based EECs (mg/kg-bw)</div></th>
                            <td colspan="2">Small</td>
                            <td colspan="2">Medium</td>
                            <td colspan="2">Large</td>
                            </tr>
                            <tr>
                            <th scope="col">Acute</div></th>       
                            <th scope="col">Chronic</div></th> 
                            <th scope="col">Acute</div></th> 
                            <th scope="col">Chronic</div></th>  
                            <th scope="col">Acute</div></th> 
                            <th scope="col">Chronic</div></th>                  
                          </tr>
                          <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Fruits/Pods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                        """%(trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 240, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 240, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 240, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 110, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 110, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 110, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 135, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 135, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 135, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 15, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 15, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 15, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 94, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 94, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 94, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.1, n_a, rate_out, a_i, 15, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.1, n_a, rate_out, a_i, 15, h_l, day_out),
                            trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.1, n_a, rate_out, a_i, 15, h_l, day_out))
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Mammalian Dietary Based RQs (mg/kg-bw)</div></th>
                            <th scope="col">Acute</div></th>       
                            <th scope="col">Chronic</div></th>               
                          </tr>
                            <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Fruits/Pods/Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                        """%(trex2_model.ARQ_diet_mamm(trex2_model.EEC_diet, lc50_mamm, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out), trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out),
                            trex2_model.ARQ_diet_mamm(trex2_model.EEC_diet, lc50_mamm, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out), trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out),
                            trex2_model.ARQ_diet_mamm(trex2_model.EEC_diet, lc50_mamm, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out), trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out),
                            trex2_model.ARQ_diet_mamm(trex2_model.EEC_diet, lc50_mamm, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out), trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out),
                            trex2_model.ARQ_diet_mamm(trex2_model.EEC_diet, lc50_mamm, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out), trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out))
        if Application_type == 'Row/Band/In-furrow-Granular':
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">LD50ft-2(mg/kg-bw)</div></th>
                            <th scope="col">Avian</div></th>       
                            <th scope="col">Mammal</div></th>    
                            </tr>
                          <tr>
                            <td>Small</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>  
                          <tr>
                            <td>Medium</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          <tr>
                            <td>Large</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>            
                          """%(trex2_model.LD50_rg_bird(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_bird_sm, at_bird, ld50_bird, tw_bird, x), trex2_model.LD50_rg_mamm(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_mamm_sm, at_mamm, ld50_mamm, tw_mamm),
                               trex2_model.LD50_rg_bird(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_bird_md, at_bird, ld50_bird, tw_bird, x), trex2_model.LD50_rg_mamm(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_mamm_md, at_mamm, ld50_mamm, tw_mamm),
                               trex2_model.LD50_rg_bird(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_bird_lg, at_bird, ld50_bird, tw_bird, x), trex2_model.LD50_rg_mamm(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_mamm_lg, at_mamm, ld50_mamm, tw_mamm))
        elif Application_type == 'Row/Band/In-furrow-Liquid':
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">LD50ft-2(mg/kg-bw)</div></th>
                            <th scope="col">Avian</div></th>       
                            <th scope="col">Mammal</div></th>    
                            </tr>
                          <tr>
                            <td>Small</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>  
                          <tr>
                            <td>Medium</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          <tr>
                            <td>Large</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>                      
                          """%(trex2_model.LD50_rl_bird(Application_type, rate_out, a_i, p_i, b_w, aw_bird_sm, at_bird, ld50_bird, tw_bird, x), trex2_model.LD50_rl_mamm(Application_type, rate_out, a_i, p_i, b_w, aw_mamm_sm, at_mamm, ld50_mamm, tw_mamm),     
                               trex2_model.LD50_rl_bird(Application_type, rate_out, a_i, p_i, b_w, aw_bird_md, at_bird, ld50_bird, tw_bird, x), trex2_model.LD50_rl_mamm(Application_type, rate_out, a_i, p_i, b_w, aw_mamm_md, at_mamm, ld50_mamm, tw_mamm),     
                               trex2_model.LD50_rl_bird(Application_type, rate_out, a_i, p_i, b_w, aw_bird_lg, at_bird, ld50_bird, tw_bird, x), trex2_model.LD50_rl_mamm(Application_type, rate_out, a_i, p_i, b_w, aw_mamm_lg, at_mamm, ld50_mamm, tw_mamm))     

        elif Application_type == 'Broadcast-Granular':
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">LD50ft-2(mg/kg-bw)</div></th>
                            <th scope="col">Avian</div></th>       
                            <th scope="col">Mammal</div></th>    
                            </tr>
                          <tr>
                            <td>Small</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>  
                          <tr>
                            <td>Medium</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          <tr>
                            <td>Large</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>                       
                          """%(trex2_model.LD50_bg_bird(Application_type, rate_out, a_i, p_i, aw_bird_sm, trex2_model.at_bird, ld50_bird, tw_bird,x), trex2_model.LD50_bg_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_sm, trex2_model.at_mamm, ld50_mamm, tw_mamm),
                              trex2_model.LD50_bg_bird(Application_type, rate_out, a_i, p_i, aw_bird_md, trex2_model.at_bird, ld50_bird, tw_bird,x), trex2_model.LD50_bg_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_md, trex2_model.at_mamm, ld50_mamm, tw_mamm),
                              trex2_model.LD50_bg_bird(Application_type, rate_out, a_i, p_i, aw_bird_lg, trex2_model.at_bird, ld50_bird, tw_bird,x), trex2_model.LD50_bg_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_lg, trex2_model.at_mamm, ld50_mamm, tw_mamm))
        elif Application_type == 'Broadcast-Liquid':
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">LD50ft-2(mg/kg-bw)</div></th>
                            <th scope="col">Avian</div></th>       
                            <th scope="col">Mammal</div></th>    
                            </tr>
                          <tr>
                            <td>Small</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>  
                          <tr>
                            <td>Medium</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          <tr>
                            <td>Large</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>                      
                          """%(trex2_model.LD50_bl_bird(Application_type, rate_out, a_i, p_i, aw_bird_sm, at_bird, ld50_bird, tw_bird,x), trex2_model.LD50_bl_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_sm, at_mamm, ld50_mamm, tw_mamm),
                               trex2_model.LD50_bl_bird(Application_type, rate_out, a_i, p_i, aw_bird_md, at_bird, ld50_bird, tw_bird,x), trex2_model.LD50_bl_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_md, at_mamm, ld50_mamm, tw_mamm),
                               trex2_model.LD50_bl_bird(Application_type, rate_out, a_i, p_i, aw_bird_lg, at_bird, ld50_bird, tw_bird,x), trex2_model.LD50_bl_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_lg, at_mamm, ld50_mamm, tw_mamm))
        
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TRexOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    