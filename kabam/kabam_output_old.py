# -*- coding: utf-8 -*-


import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from kabam import Kabamdb
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
#import cloud

#import MySQLdb

cgitb.enable()

#food intake for birds
import json
import base64
import urllib2
from google.appengine.api import urlfetch
api_key='3355'
api_secretkey='212ed160e3f416fdac8a3b71c90f3016722856b9'

#def post(self,aaa):
    base64string = base64.standard_b64decode('%s:%s' % (api_key,api_secretkey))[:-1]
    http_headers = {'Authorization' : 'Basic %s' % base64string}
#    request =urllib2.Request('https://api.picloud.com/r/3303/square_func', data='aaa', headers=http_headers)
#    response = urllib2.urlopen(request)
    response = urlfetch.fetch(url='https://api.picloud.com/r/3303/square_func', payload={aaa}, method=urlfetch.GET, headers=http_headers)    
    data = json.load(response)
    
def fi_bird(aw_bird, mf_w_bird):
    return (0.648 * (aw_bird**0.651))/(1-mf_w_bird)

    
 

k_ow = exp(l_kow)

# calculate Fraction of freely dissolved in water column
def phi(x_poc, x_doc, k_ow):
    x_poc=float(x_poc)
    x_doc=float(x_doc)
    k_ow=float(k_ow)
    return 1 / (1 + (x_poc*0.35*k_ow) + (x_doc*0.08*k_ow))

#calculate concentration of chemical in sediment    
def cs(c_soc, oc, c_wdp, k_oc):
    c_soc=float(c_soc)
    oc=float(oc)
    c_wdp=float(c_wdp)
    k_oc=float(k_oc)
    c_soc=c_soc(c_wdp, k_oc)
    return c_sco*oc
#normalized pesticide concentration in sediment    
def c_soc(c_wdp, k_oc):
    c_wdp=float(c_wdp)
    k_oc=float(k_oc)
    return c_wdp*k_oc    

#determine input for rate constants user input or calculated
if rate_constants == b:
    # use input values
    k1_phytoplankton = forms.getvalue('phytoplankton_k1')
    k2_phytoplankton = forms.getvalue('phytoplankton_k2')
    kd_phytoplankton = forms.getvalue('phytoplankton_kd')
    ke_phytoplankton = forms.getvalue('phytoplankton_ke')
    km_phytoplankton = forms.getvalue('phytoplankton_km')
    k1_zoo = forms.getvalue('zooplankton_k1')
    k2_zoo = forms.getvalue('zooplankton_k2')
    kd_zoo = forms.getvalue('zooplankton_kd')
    ke_zoo = forms.getvalue('zooplankton_ke')
    km_zoo = forms.getvalue('zooplankton_km')
    k1_beninv = forms.getvalue('benthic_invertebrates_k1')
    k2_beninv = forms.getvalue('benthic_invertebrates_k2')
    kd_beninv = forms.getvalue('benthic_invertebrates_kd')
    ke_beninv = forms.getvalue('benthic_invertebrates_ke')
    km_beninv = forms.getvalue('benthic_invertebrates_km')
    k1_ff = forms.getvalue('filter_feeders_k1')
    k2_ff = forms.getvalue('filter_feeders_k2')
    kd_ff = forms.getvalue('filter_feeders_kd')
    ke_ff = forms.getvalue('filter_feeders_ke')
    km_ff = forms.getvalue('filter_feeders_km')
    k1_smfish = forms.getvalue('small_fish_k1')
    k2_smfish = forms.getvalue('small_fish_k2')
    kd_smfish = forms.getvalue('small_fish_kd')
    ke_smfish = forms.getvalue('small_fish_ke')
    km_smfish = forms.getvalue('small_fish_km')
    k1_medfish = forms.getvalue('medium_fish_k1')
    k2_medfish = forms.getvalue('medium_fish_k2')
    kd_medfish = forms.getvalue('medium_fish_kd')
    ke_medfish = forms.getvalue('medium_fish_ke')
    km_medfish = forms.getvalue('medium_fish_kd')
    k1_larfish = forms.getvalue('large_fish_k1')
    k2_larfish = forms.getvalue('large_fish_k2')
    kd_larfish = forms.getvalue('large_fish_kd')
    ke_larfish = forms.getvalue('large_fish_ke')
    km_larfish = forms.getvalue('large_fish_km')
    
else:
    # calculate values
    #############phytoplankton
  
    # phytoplankton water partition coefficient  
    def k_bw_phytoplankton(v_lb_phytoplankton, v_nb_phytoplankton, k_ow, v_wb_phytoplankton):
        v_lb_phytoplankton=float(v_lb_phytoplankton)
        v_nb_phytoplankton=float(v_nb_phytoplankton)
        v_wb_phytoplankton=float(v_wb_phytoplankton)
        return (v_lb_phytoplankton*k_ow)+(v_nb_phytoplankton*0.35*k_ow)+v_wb_phytoplankton
    # rate constant for uptake through respiratory area
    def k1_phytoplankton(k_ow):
        k_ow=float(k_ow)
        return 1/(6.0e-5+(5.5/k_ow))
        
    #rate constant for elimination through the gills for phytoplankton  
    def k2_phytoplankton(k_ow, k1_phytoplankton, v_lb_phytoplankton, v_nb_phytoplankton, k_ow, v_wb_phytoplankton):
        k_bw_phytoplankton = k_bw_phytoplankton(v_lb_phytoplankton, v_nb_phytoplankton, k_ow, v_wb_phytoplankton)
        return k1_phytoplankton/k_bw_phytoplankton
##################zooplankton
    # rate constant for elimination through the gills for zooplankton
    def k2_zoo(k_ow, ew_zoo, gv_zoo, wb_zoo, c_ox, v_lb_zoo, v_nb_zoo, v_wb_zoo):
        k1_zoo = k1_zoo(k_ow, ew_zoo, gv_zoo, wb_zoo, c_ox)
        ew_zoo = ew_zoo(k_ow)
        gv_zoo = gv_zoo(wb_zoo, c_ox)
        k_bw_zoo = k_bw_zoo(v_lb_zoo, k_ow, v_nb_zoo, v_wb_zoo)
        return k1_zoo / k_bw_zoo
    #uptake rate constant through respiratory area    
    def k1_zoo(k_ow, ew_zoo, gv_zoo, wb_zoo, c_ox):
        gv_zoo = gv_zoo(wb_zoo, c_ox)
        ew_zoo = ew_zoo(k_ow)
        return ((ew_zoo*gv_zoo) / wb_zoo)
    # pesticide uptake efficiency by gills
    def ew_zoo(k_ow):          
        return (1/(1.85+(155/k_ow)))         
    # ventilation rate     
    def gv_zoo(wb_zoo, c_ox):  
        wb_zoo = float(wb_zoo)
        c_ox = float(c_ox)
        return (1400 * ((wb_zoo**0.65)/c_ox))
    # zooplankton water partition coefficient
    def k_bw_zoo(v_lb_zoo, k_ow, v_nb_zoo, v_wb_zoo):
        v_lb_zoo = float(v_lb_zoo)
        v_nb_zoo = float(v_nb_zoo)
        v_wb_zoo = float(v_wb_zoo)
        return (v_lb_zoo * k_ow) + (v_nb_zoo * 0.035 * k_ow) + v_wb_zoo
        


# phytoplankton growth rate constant
kg_phytoplankton=0.1
# phytoplankton diet uptake rate constant
kd_phytoplankton=0
#phytoplankton fecal elimination rate constant  
ke_phytoplankton=0
# fraction of respiratory ventilation involving overlying water
mo_phytoplankton = 1
# fraction of respiratory ventilation involving pore water
mp_phytoplankton = 0    
# pesticide tissue residue for phytoplankton
# rate constant for pesticide metabolic transformation
km_phytoplankton = 0
def cb_phytoplankton(k1_phytoplankton, c_s, c_wdp, c_wto, k2_phytoplankton, kd_phytoplankton, ke_phytoplankton, kg_phytoplankton, km, mo, mp, phi, k_ow, c_soc, oc, k_oc, x_poc, x_doc, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton):   
    k1_phytoplankton = k1_phytoplankton(k_ow)
    c_s = c_s(c_soc, oc, c_wdp, k_oc)
    phi = phi(x_poc, x_doc, k_ow)
    k2_phytoplankton = k2_phytoplankton(k_ow, k1_phytoplankton, v_lb_phytoplankton, v_nb_phytoplankton, k_ow, v_wb_phytoplankton)
    k_bw_phytoplankton = k_bw_phytoplankton(v_lb_phytoplankton, v_nb_phytoplankton, k_ow, v_wb_phytoplankton)     
    return (k1_phytoplankton * (mo_phytoplankton * phi * c_wto + mp_phytoplankton * c_wdp) + (kd_phytoplankton)) / (k2_phytoplankton + ke_phytoplankton + kg_phytoplankton + km_phytoplankton)
    




class KabamOutputPage(webapp.RequestHandler):
    def get(self):        
        form = cgi.FieldStorage()   
#        chem_name = form.getvalue('chemical_name')
#        Koc = form.getvalue('Koc')
#        aaa = form.getvalue('l_kow')
        
#        aw_bird = float(form.getvalue('body_weight_of_the_assessed_bird'))
#        mf_w_bird = float(form.getvalue('mf_w_bird'))
        
#        c_ss = form.getvalue('c_ss')
#        c_ss = float(c_ss)
#        Species_of_the_tested_bird = form.getvalue('Species_of_the_tested_bird')
#        body_weight_of_the_tested_bird=form.getvalue('body_weight_of_the_tested_bird')
        
        chemical_name = form.getvalue('chemical_name')
        l_kow = form.getvalue('l_kow')
        k_oc = form.getvalue(Koc)
        c_wdp = form.getvalue('pore_water_benthic_EECs')
        water_column_EEC = form.getvalue('water_column_1_in_10_year_EECs')
        chemical_specific_mineau_scaling_factor = form.getvalue('chemical_specific_mineau_scaling_factor')
        x_poc = form.getvalue('c_poc')
        x_doc = form.getvalue('c_doc')
        c_ox = form.getvalue('c_ox')
        w_t = form.getvalue('w_t')
        c_ss = form.getvalue('c_ss')
        oc = form.getvalue('oc')
    
        species_of_the_tested_bird = form.getvalue('Species_of_the_tested_bird')
        body_weight_of_the_tested_bird_quail = form.getvalue('body_weight_of_the_tested_bird_quail')
        body_weight_of_the_tested_bird_duck = form.getvalue('body_weight_of_the_tested_bird_duck')
        body_weight_of_the_tested_bird_other = form.getvalue('body_weight_of_the_tested_bird_other')
        avian_ld50 = form.getvalue('avian_ld50')
        avian_lc50 = form.getvalue('avian_lc50')
        avian_noaec = form.getvalue('avian_NOAEC')
        species_of_the_tested_mamm = form.getvalue('Species_of_the_tested_mamm')
        body_weight_of_the_tested_mamm_rat=form.getvalue('body_weight_of_the_tested_mamm_rat')
        body_weight_of_the_tested_mamm_other=form.getvalue('body_weight_of_the_tested_mamm_other')
        mammalian_ld50 = form.getvalue('mammalian_ld50')
        mammalian_lc50 = form.getvalue('mammalian_lc50')
        mammalian_chronic_endpoint = form.getvalue('mammalian_chronic_endpoint')
        body_weight_of_the_assessed_mamm = form.getvalue('body_weight_of_the_assessed_mamm')
        diet_for_large_fish = form.getvalue('Diet_for_large_fish')
        large_fish_p_sediment = form.getvalue('large_fish_p_sediment')
        large_fish_p_phytoplankton = form.getvalue('large_fish_p_phytoplankton')
        large_fish_p_zooplankton = form.getvalue('large_fish_p_zooplankton')
        large_fish_p_benthic_invertebrates = form.getvalue('large_fish_p_benthic_invertebrates')
        large_fish_p_filter_feeders = form.getvalue('large_fish_p_filter_feeders')
        large_fish_p_small_fish = form.getvalue('large_fish_p_small_fish')
        large_fish_p_fish_medium = form.getvalue('large_fish_p_fish_medium')
        diet_for_medium_fish = form.getvalue('Diet_for_medium_fish')
        medium_fish_p_sediment = form.getvalue('medium_fish_p_sediment')
        medium_fish_p_phytoplankton = form.getvalue('medium_fish_p_phytoplankton')
        medium_fish_p_zooplankton = form.getvalue('medium_fish_p_zooplankton')
        medium_fish_p_benthic_invertebrates = form.getvalue('medium_fish_p_benthic_invertebrates')
        medium_fish_p_filter_feeders = form.getvalue('medium_fish_p_filter_feeders')
        medium_fish_p_small_fish = form.getvalue('medium_fish_p_small_fish')
        Diet_for_small_fish = form.getvalue('diet_for_small_fish')
        small_fish_p_sediment = form.getvalue('small_fish_p_sediment')
        small_fish_p_phytoplankton = form.getvalue('small_fish_p_phytoplankton')
        small_fish_p_zooplankton = form.getvalue('small_fish_p_zooplankton')
        small_fish_p_benthic_invertebrates = form.getvalue('small_fish_p_benthic_invertebrates')
        small_fish_p_filter_feeders = form.getvalue('small_fish_p_filter_feeders')
        Diet_for_filter_feeder = form.getvalue('Diet_for_filter_feeder')
        filter_feeder_p_sediment = form.getvalue('filter_feeder_p_sediment')
        filter_feeder_p_phytoplankton = form.getvalue('filter_feeder_p_phytoplankton')
        filter_feeder_p_zooplankton = form.getvalue('filter_feeder_p_zooplankton')
        filter_feeder_p_benthic_invertebrates = form.getvalue('filter_feeder_p_benthic_invertebrates')
        Diet_for_invertebrates = form.getvalue('Diet_for_invertebrates')
        benthic_invertebrates_p_sediment = form.getvalue('benthic_invertebrates_p_sediment')
        benthic_invertebrates_p_phytoplankton = form.getvalue('benthic_invertebrates_p_phytoplankton')
        benthic_invertebrates_p_zooplankton = form.getvalue('benthic_invertebrates_p_zooplankton')
        Diet_for_zooplankton = form.getvalue('Diet_for_zooplankton')
        zooplankton_p_sediment = form.getvalue('zooplankton_p_sediment')
        zooplankton_p_phytoplankton = form.getvalue('zooplankton_p_phytoplankton')

        characteristics_sediment = form.getvalue('characteristics_sediment')
        sediment_lipid = form.getvalue('sediment_lipid')
        sediment_NLOM = form.getvalue('sediment_NLOM')
        sediment_water = form.getvalue('sediment_water')
        sediment_respire = form.getvalue('sediment_respire')
        characteristics_phytoplankton = form.getvalue('characteristics_phytoplankton')
        v_lb_phytoplankton = form.getvalue('phytoplankton_lipid')
        v_nb_phytoplankton = form.getvalue('phytoplankton_NLOM')
        v_wb_phytoplankton = form.getvalue('phytoplankton_water')
        phytoplankton_respire = form.getvalue('phytoplankton_respire')
        characteristics_zooplankton = form.getvalue('characteristics_zooplankton')
        wb_zoo = form.getvalue('zooplankton_wet_weight')
        v_lb_zoo = form.getvalue('zooplankton_lipid')
        v_nb_zoo = form.getvalue('zooplankton_NLOM')
        v_wb_zoo = form.getvalue('zooplankton_water')
        zoo_respire = form.getvalue('zooplankton_respire')
        characteristics_benthic_invertebrates = form.getvalue('characteristics_benthic_invertebrates')
        wb_beninv = form.getvalue('benthic_invertebrates_wet_weight')
        v_lb_beninv = form.getvalue('benthic_invertebrates_lipid')
        v_nb_beninv = form.getvalue('benthic_invertebrates_NLOM')
        v_wb_beninv = form.getvalue('benthic_invertebrates_water')
        beninv_respire = form.getvalue('benthic_invertebrates_respire')
        characteristics_ff = form.getvalue('characteristics_filter_feeders')
        wb_ff = form.getvalue('filter_feeders_wet_weight')
        v_lb_ff = form.getvalue('filter_feeders_lipid')
        v_nb_ff = form.getvalue('filter_feeders_NLOM')
        v_wb_ff = form.getvalue('filter_feeders_water')
        ff_respire = form.getvalue('filter_feeders_respire')
        characteristics_smfish = form.getvalue('characteristics_small_fish')
        wb_smfish = form.getvalue('small_fish_wet_weight')
        v_lb_smfish = form.getvalue('small_fish_lipid')
        v_nb_smfish = form.getvalue('small_fish_NLOM')
        v_wb_smfish = form.getvalue('small_fish_water')
        smfish_respire = form.getvalue('small_fish_respire')
        characteristics_medfish = form.getvalue('characteristics_medium_fish')
        wb_medfish = form.getvalue('medium_fish_wet_weight')
        v_lb_medfish = form.getvalue('medium_fish_lipid')
        v_nb_medfish = form.getvalue('medium_fish_NLOM')
        v_wb_medfish = form.getvalue('medium_fish_water')
        medfish_respire = form.getvalue('medium_fish_respire')
        characteristics_larfish = form.getvalue('characteristics_large_fish')
        wb_larfish = form.getvalue('large_fish_wet_weight')
        v_lb_larfish = form.getvalue('large_fish_lipid')
        v_nb_larfish = form.getvalue('large_fish_NLOM')
        v_wb_larfish = form.getvalue('large_fish_water')
        larfish_respire = form.getvalue('large_fish_respire')

        rate_constants = form.getvalue('rate_constants')
        k1_phytoplankton = form.getvalue('phytoplankton_k1')
        k2_phytoplankton = form.getvalue('phytoplankton_k2')
        kd_phytoplankton = form.getvalue('phytoplankton_kd')
        ke_phytoplankton = form.getvalue('phytoplankton_ke')
        km_phytoplankton = form.getvalue('phytoplankton_km')
        k1_zoo = form.getvalue('zooplankton_k1')
        k2_zoo = form.getvalue('zooplankton_k2')
        kd_zoo = form.getvalue('zooplankton_kd')
        ke_zoo = form.getvalue('zooplankton_ke')
        km_zoo = form.getvalue('zooplankton_km')
        k1_beninv = form.getvalue('benthic_invertebrates_k1')
        k2_beninv = form.getvalue('benthic_invertebrates_k2')
        kd_beninv = form.getvalue('benthic_invertebrates_kd')
        ke_beninv = form.getvalue('benthic_invertebrates_ke')
        km_beninv = form.getvalue('benthic_invertebrates_km')
        k1_ff = form.getvalue('filter_feeders_k1')
        k2_ff = form.getvalue('filter_feeders_k2')
        kd_ff = form.getvalue('filter_feeders_kd')
        ke_ff = form.getvalue('filter_feeders_ke')
        km_ff = form.getvalue('filter_feeders_km')
        k1_smfish = form.getvalue('small_fish_k1')
        k2_smfish = form.getvalue('small_fish_k2')
        kd_smfish = form.getvalue('small_fish_kd')
        ke_smfish = form.getvalue('small_fish_ke')
        km_smfish = form.getvalue('small_fish_km')
        k1_medfish = form.getvalue('medium_fish_k1')
        k2_medfish = form.getvalue('medium_fish_k2')
        kd_medfish = form.getvalue('medium_fish_kd')
        ke_medfish = form.getvalue('medium_fish_ke')
        km_medfish = form.getvalue('medium_fish_kd')
        k1_larfish = form.getvalue('large_fish_k1')
        k2_larfish = form.getvalue('large_fish_k2')
        kd_larfish = form.getvalue('large_fish_kd')
        ke_larfish = form.getvalue('large_fish_ke')
        km_larfish = form.getvalue('large_fish_km')



        
        
        text_file = open('kabam/kabam_description.txt','r')
        x1 = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'kabam','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {'model':''})
        html = html + """
        <table border="1">
        <tr><H3>User Inputs</H3></tr>
        <tr>
        <td>Chemical Name</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Log Kow</td>
        <td>%s</td>
        <td></td>
        </tr>
        <tr>
        <td>Koc</td>
        <td>%s</td>
        <td>L/kg OC</td>
        </tr>
        <tr>
        <td>Pore water EEC</td>
        <td>%s</td>
        <td>ug/L</td>
        </tr>
        <tr>
        <td>Water Column EEC</td>
        <td>%s</td>
        <td>ug/L</td>
        </tr>
        <tr>
        </table>
        """ % (chemical_name, l_kow, k_oc,c_wdp, water_column_EEC)
      
      
      
      
      
      
      
      # html = html + """<table width="600" border="1">
        #                  <tr>
         #                   <th width="240" scope="col">Inputs</div></th>
          #                  <th width="60" scope="col">Value</div></th>
           #                 <th width="240" scope="col">Inputs</div></th>
            #                <th width="60" scope="col">Value</div></th>                            
             #             </tr>
              #            <tr>
               #             <td>sp</td>
                #            <td>%s</td>
                 #           <td>BW</td>
                  #          <td>%s</td>                          
                   #       </tr>
                                                             
                    #    </table>
                     #   <p>&nbsp;</p>                     
                      #  """%(k_oc)                          
        
       # html = html +  """<table width="600" border="1">
        #                  <tr>
         #                   <th width="480" scope="col">Outputs</div></th>
          #                  <th width="120" scope="col">Value</div></th>                            
           #               </tr>
            #              <tr>
             #               <td>picloud</td>
              #              <td>%s</td></tr>      
               #          </table>"""#%(post(self,aaa))
                         
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)
        
        #update 
#        conn = MySQLdb.connect("localhost", "root", "th339933ht", "kabam")
#        cursor = conn.cursor()
#        cursor.execute('UPDATE input SET aw_bird=%s WHERE aw_bird=%s', (aw_bird,Kabamdb.aw_bird_p))
#        conn.commit()
#        conn.close()

#        conn = MySQLdb.connect("localhost", "root", "th339933ht", "kabam")
#        cursor = conn.cursor()
#        cursor.execute('INSERT INTO input (aw_bird, mf_w_bird) VALUES(%s, %s)', (aw_bird, mf_w_bird))
#        conn.commit()
#        conn.close()


        
#        if aw_bird != Kabamdb.aw_bird_p:
#            conn = MySQLdb.connect("localhost", "root", "th339933ht", "kabam")
#            cursor = conn.cursor()
#            cursor.execute('UPDATE input SET aw_bird=%s WHERE aw_bird=%s', (aw_bird, Kabamdb.aw_bird_p))
#            conn.close()
#           
#        else: pass
    
#        conn = MySQLdb.connect("localhost", "root", "th339933ht", "kabam")
#        cursor = conn.cursor()    
#        cursor.execute('INSERT INTO ouput (para_out) VALUES (%s)', (fi_bird(aw_bird, mf_w_bird)))
#        conn.commit()
#        conn.close()
#        
app = webapp.WSGIApplication([('/.*', KabamOutputPage)], debug=True)
        

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    