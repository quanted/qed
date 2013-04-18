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
        a_t = form.getvalue('Application_target')
        if a_t=='Short grass':
           para=240       #coefficient used to estimate initial conc.
        elif a_t=='Tall grass':
           para=110
        elif a_t=='Broad-leafed plants/small insects':
           para=135
        elif a_t=='Fruits/pods/seeds/large insects':
           para=15
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
        tw_bird = form.getvalue('body_weight_of_the_tested_bird')
        tw_bird = float(tw_bird)        
        x = form.getvalue('mineau_scaling_factor')
        x = float(x)
        c_mamm_a = form.getvalue('body_weight_of_the_consumed_mammal_a')
        c_mamm_a = float(c_mamm_a)
        c_herp_a = form.getvalue('body_weight_of_the_consumed_herp_a')
        c_herp_a = float(c_herp_a)        
        bw_range_a = form.getvalue('BW_range_a')
        bw_herp_a = form.getvalue('BW_herptile_a')
        bw_herp_a = float(bw_herp_a)
        wp_herp_a = form.getvalue('W_p_a')
        wp_herp_a = float(wp_herp_a)/100        
        wp_mamm_a = form.getvalue('W_p_m_a')        
        wp_mamm_a = float(wp_mamm_a)/100                

        c_mamm_r = form.getvalue('body_weight_of_the_consumed_mammal_r')
        c_mamm_r = float(c_mamm_r)
        c_herp_r = form.getvalue('body_weight_of_the_consumed_herp_r')
        c_herp_r = float(c_herp_r)        
        bw_range_r = form.getvalue('BW_range_r')
        bw_herp_r = form.getvalue('BW_herptile_r')
        bw_herp_r = float(bw_herp_r)
        wp_herp_r = form.getvalue('W_p_r')
        wp_herp_r = float(wp_herp_r)/100        
        wp_mamm_r = form.getvalue('W_p_m_r')        
        wp_mamm_r = float(wp_mamm_r)/100               

        
        
        text_file = open('therps/therps_description.txt','r')
        x1 = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'therps','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                        
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'therps', 
                'model_attributes':'T-Herps Output'})

        html = html + """<table width="600" border="1">
                          <tr>
                            <th width="240" scope="col">Inputs</div></th>
                            <th width="60" scope="col">Value</div></th>
                            <th width="240" scope="col">Inputs</div></th>
                            <th width="60" scope="col">Value</div></th>                            
                          </tr>
                          <tr>
                            <td>Chemical name</td>
                            <td>%s</td>
                            <td>Use</td>
                            <td>%s</td>                          
                          </tr>
                          <tr>
                            <td>Formulated procuct name</td>
                            <td>%s</td>
                            <td>Percentage active ingredient</td>
                            <td>%s%%</td>  
                          </tr>
                          <tr>
                            <td>Application rate (lbs a.i./A)</td>
                            <td>%s</td>                          
                            <td>Number of applications</td>
                            <td>%s</td> 
                          </tr>
                          <tr>                                                         
                            <td>Interval between applications (days)</td>
                            <td>%s</td>                                                                            
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
                            <td>Body weight of tested bird (g)</td>
                            <td>%s</td>                                                      
                            <td>Mineau scaling factor</td>
                            <td>%s</td>  
                          </tr>    
                          <tr>                                                     
                            <td>Weight of the mammal consumed by amphibian (g)</td>
                            <td>%s</td>                                                      
                            <td>Body weight range of the assessed amphibian</td>
                            <td>%s</td>       
                          </tr>    
                          <tr>                               
                            <td>Body weight of assessed amphibian (g)</td>
                            <td>%s</td>                                                         
                            <td>Water content of the assessed amphibian's diet</td>
                            <td>%s%%</td>       
                          </tr>    
                          <tr>                              
                            <td>Water content of in mammal's diet (consumed by amphibian)</td>
                            <td>%s%%</td>                                                  
                            <td>Weight of the herptile consumed by amphibian (g)</td>
                            <td>%s</td>
                          </tr>                           
                          <tr>                                                     
                            <td>Weight of the mammal consumed by reptile (g)</td>
                            <td>%s</td>                                                      
                            <td>Body weight range of the assessed reptile</td>
                            <td>%s</td>       
                          </tr>    
                          <tr>                               
                            <td>Body weight of assessed reptile (g)</td>
                            <td>%s</td>                                                         
                            <td>Water content of the assessed reptile's diet</td>
                            <td>%s%%</td>       
                          </tr>    
                          <tr>                              
                            <td>Water content of in mammal's diet (consumed by reptile)</td>
                            <td>%s%%</td>                                                  
                            <td>Weight of the herptile consumed by reptile (g)</td>
                            <td>%s</td>
                          </tr>                                                                     

                                                                                    
                        </table>
                        <p>&nbsp;</p>                     
                        """%(chem_name, use, formu_name, 100*a_i, a_r, n_a, i_a, h_l, ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, tw_bird, x, 
                             c_mamm_a, bw_range_a, bw_herp_a, 100*wp_herp_a, 100*wp_mamm_a, c_herp_a,
                             c_mamm_r, bw_range_r, bw_herp_r, 100*wp_herp_r, 100*wp_mamm_r, c_herp_r)   

        html = html +  """<table width="600" border="1">
                          <tr>
                            <th width="480" scope="col">Outputs</div></th>
                            <th width="120" scope="col">Value</div></th>                            
                          </tr>
                          <tr>
                            <td>Amphibian dietary-based EECs for %s (ppm)</td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Amphibian dietary-based EECs for %s herbivore mammals (ppm)</td>
                            <td>%0.2E</td>
                          </tr>                                                    
                          <tr>
                            <td>Amphibian dietary-based EECs for %s insectivore mammals (ppm)</td>
                            <td>%0.2E</td>
                          </tr>                           
                          <tr>
                            <td>Amphibian dietary-based EECs for %s terrestrial phase amphibians (ppm)</td>
                            <td>%0.2E</td>
                          </tr>                           
                          <tr>
                            <td>Amphibian dose-based acute EECs for %s (mg/kg-bw)</td>
                            <td>%0.2E</td>
                          </tr>                            
                          <tr>
                            <td>Amphibian dose-based acute EECs for %s herbivore mammals (mg/kg-bw)</td>
                            <td>%0.2E</td>
                          </tr> 
                          <tr>
                            <td>Amphibian dose-based acute EECs for %s insectivore mammals (mg/kg-bw)</td>
                            <td>%0.2E</td>
                          </tr>                           
                          <tr>
                            <td>Amphibian dose-based acute EECs for %s terrestrial phase amphibians (mg/kg-bw)</td>
                            <td>%0.2E</td>
                          </tr>                            
                          <tr>
                            <td>Amphibian dose-based acute RQs for %s </td>
                            <td>%0.2E</td>
                          </tr>                             
                          <tr>
                            <td>Amphibian dose-based acute RQs for %s herbivore mammals</td>
                            <td>%0.2E</td>
                          </tr>                          
                          <tr>
                            <td>Amphibian dose-based acute RQs for %s insectivore mammals</td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Amphibian dose-based acute RQs for %s terrestrial phase amphibians</td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Amphibian dietary-based acute RQs for %s </td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Amphibian dietary-based acute RQs for %s herbivore mammals</td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Amphibian dietary-based acute RQs for %s insectivore mammals</td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Amphibian dietary-based acute RQs for %s terrestrial phase amphibians</td>
                            <td>%0.2E</td>
                          </tr>                            
                          <tr>
                            <td>Amphibian dietary-based chronic RQs for %s</td>
                            <td>%0.2E</td>
                          </tr> 
                          <tr>
                            <td>Amphibian dietary-based chronic RQs for %s herbivore mammals</td>
                            <td>%0.2E</td>
                          </tr>                           
                          <tr>
                            <td>Amphibian dietary-based chronic RQs for %s insectivore mammals</td>
                            <td>%0.2E</td>
                          </tr> 
                          <tr>
                            <td>Amphibian dietary-based chronic RQs for %s terrestrial phase amphibians</td>
                            <td>%0.2E</td>
                          </tr>                           

                          <tr>
                            <td>Reptile dietary-based EECs for %s (ppm)</td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Reptile dietary-based EECs for %s herbivore mammals (ppm)</td>
                            <td>%0.2E</td>
                          </tr>                                                    
                          <tr>
                            <td>Reptile dietary-based EECs for %s insectivore mammals (ppm)</td>
                            <td>%0.2E</td>
                          </tr>                           
                          <tr>
                            <td>Reptile dietary-based EECs for %s terrestrial phase amphibians (ppm)</td>
                            <td>%0.2E</td>
                          </tr>                                         
                          <tr>
                            <td>Reptile dose-based acute EECs for %s (mg/kg-bw)</td>
                            <td>%0.2E</td>
                          </tr>                            
                          <tr>
                            <td>Reptile dose-based acute EECs for %s herbivore mammals (mg/kg-bw)</td>
                            <td>%0.2E</td>
                          </tr> 
                          <tr>
                            <td>Reptile dose-based acute EECs for %s insectivore mammals (mg/kg-bw)</td>
                            <td>%0.2E</td>
                          </tr>                           
                          <tr>
                            <td>Reptile dose-based acute EECs for %s terrestrial phase amphibians (mg/kg-bw)</td>
                            <td>%0.2E</td>
                          </tr>                            
                          <tr>
                            <td>Reptile dose-based acute RQs for %s </td>
                            <td>%0.2E</td>
                          </tr>                             
                          <tr>
                            <td>Reptile dose-based acute RQs for %s herbivore mammals</td>
                            <td>%0.2E</td>
                          </tr>                          
                          <tr>
                            <td>Reptile dose-based acute RQs for %s insectivore mammals</td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Reptile dose-based acute RQs for %s terrestrial phase amphibians</td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Reptile dietary-based acute RQs for %s </td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Reptile dietary-based acute RQs for %s herbivore mammals</td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Reptile dietary-based acute RQs for %s insectivore mammals</td>
                            <td>%0.2E</td>
                          </tr>
                          <tr>
                            <td>Reptile dietary-based acute RQs for %s terrestrial phase amphibians</td>
                            <td>%0.2E</td>
                          </tr>                            
                          <tr>
                            <td>Reptile dietary-based chronic RQs for %s</td>
                            <td>%0.2E</td>
                          </tr> 
                          <tr>
                            <td>Reptile dietary-based chronic RQs for %s herbivore mammals</td>
                            <td>%0.2E</td>
                          </tr>                           
                          <tr>
                            <td>Reptile dietary-based chronic RQs for %s insectivore mammals</td>
                            <td>%0.2E</td>
                          </tr> 
                          <tr>
                            <td>Reptile dietary-based chronic RQs for %s terrestrial phase amphibians</td>
                            <td>%0.2E</td>
                          </tr>
                          </table>""" %(a_t, therps_model.EEC_diet(therps_model.C_0, n_a, i_a, a_r, a_i, para, h_l),
                                       bw_range_a, therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, therps_model.fi_mamm, c_mamm_a, wp_mamm_a),
                                       bw_range_a, therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, therps_model.fi_mamm, c_mamm_a, wp_mamm_a),
                                       bw_range_a, therps_model.EEC_diet_tp(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_a, wp_herp_a),
                                       a_t, therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_a, therps_model.fi_herp, wp_herp_a, therps_model.C_0, n_a, i_a, a_r, a_i, para, h_l),
                                       bw_range_a, therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, bw_herp_a, c_mamm_a, wp_mamm_a),
                                       bw_range_a, therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, bw_herp_a, c_mamm_a, wp_mamm_a),
                                       bw_range_a, therps_model.EEC_dose_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, bw_herp_a, c_herp_a, wp_herp_a),
                                       a_t, therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_a, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, wp_herp_a, therps_model.C_0, n_a, i_a, a_r, a_i, para, h_l),
                                       bw_range_a, therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_a, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, c_mamm_a, wp_mamm_a, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l),
                                       bw_range_a, therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_a, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, c_mamm_a, wp_mamm_a, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l),
                                       bw_range_a, therps_model.ARQ_dose_tp(therps_model.EEC_dose_tp, therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_a, wp_herp_a, therps_model.at_bird, ld50_bird, bw_herp_a, tw_bird, x),
                                       a_t, therps_model.ARQ_diet_herp(therps_model.EEC_diet, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, para, h_l),
                                       bw_range_a, therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, therps_model.fi_mamm, c_mamm_a, wp_mamm_a),
                                       bw_range_a, therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, therps_model.fi_mamm, c_mamm_a, wp_mamm_a),
                                       bw_range_a, therps_model.ARQ_diet_tp(therps_model.EEC_diet_tp, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_a, wp_herp_a),
                                       a_t, therps_model.CRQ_diet_herp(therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, para, h_l),
                                       bw_range_a, therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, therps_model.fi_mamm, c_mamm_a, wp_mamm_a),
                                       bw_range_a, therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, therps_model.fi_mamm, c_mamm_a, wp_mamm_a),
                                       bw_range_a, therps_model.CRQ_diet_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_a, wp_herp_a),
                                       
                                       a_t, therps_model.EEC_diet(therps_model.C_0, n_a, i_a, a_r, a_i, para, h_l),
                                       bw_range_r, therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l,therps_model.fi_mamm, c_mamm_r, wp_mamm_r),
                                       bw_range_r, therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l,therps_model.fi_mamm, c_mamm_r, wp_mamm_r),
                                       bw_range_r, therps_model.EEC_diet_tp(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_r, wp_herp_r),
                                       a_t, therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_r, therps_model.fi_herp, wp_herp_r, therps_model.C_0, n_a, i_a, a_r, a_i, para, h_l),
                                       bw_range_r, therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, bw_herp_r, c_mamm_r, wp_mamm_r),
                                       bw_range_r, therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, bw_herp_r, c_mamm_r, wp_mamm_r),
                                       bw_range_r, therps_model.EEC_dose_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, bw_herp_r, c_herp_r, wp_herp_r),
                                       a_t, therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_r, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, wp_herp_r, therps_model.C_0, n_a, i_a, a_r, a_i, para, h_l),
                                       bw_range_r, therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_r, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, c_mamm_r, wp_mamm_r, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l),
                                       bw_range_r, therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_r, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, c_mamm_r, wp_mamm_r, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l),
                                       bw_range_r, therps_model.ARQ_dose_tp(therps_model.EEC_dose_tp, therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_r, wp_herp_r, therps_model.at_bird, ld50_bird, bw_herp_r, tw_bird, x),
                                       a_t, therps_model.ARQ_diet_herp(therps_model.EEC_diet, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, para, h_l),
                                       bw_range_r, therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, therps_model.fi_mamm, c_mamm_r, wp_mamm_r),
                                       bw_range_r, therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, therps_model.fi_mamm, c_mamm_r, wp_mamm_r),
                                       bw_range_r, therps_model.ARQ_diet_tp(therps_model.EEC_diet_tp, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_r, wp_herp_r),
                                       a_t, therps_model.CRQ_diet_herp(therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, para, h_l),
                                       bw_range_r, therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, therps_model.fi_mamm, c_mamm_r, wp_mamm_r),
                                       bw_range_r, therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, therps_model.fi_mamm, c_mamm_r, wp_mamm_r),
                                       bw_range_r, therps_model.CRQ_diet_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_r, wp_herp_r))            
        
#        
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', THerpsOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    