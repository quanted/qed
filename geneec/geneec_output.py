# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
from geneec import geneec_model, geneec_tables
import sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
from uber import uber_lib
import logging
logger = logging.getLogger('Geneec Model')
import rest_funcs

class GENEECOutputPage(webapp.RequestHandler):
    def post(self):     
        form = cgi.FieldStorage() 
        chem_name = form.getvalue('chemical_name')
        application_target = form.getvalue('application_target')
        application_rate = form.getvalue('application_rate')
        number_of_applications = form.getvalue('number_of_applications')
        interval_between_applications = form.getvalue('interval_between_applications')
        Koc = form.getvalue('Koc')  
        aerobic_soil_metabolism = form.getvalue('aerobic_soil_metabolism')   
        wet_in = form.getvalue('wet_in')              
        application_method = form.getvalue('application_method')
        #A1
        aerial_size_dist = form.getvalue('aerial_size_dist')
        #B1
        ground_spray_type = form.getvalue('ground_spray_type')                                          
        #C1
        airblast_type = form.getvalue('airblast_type')  
        #B2    
        spray_quality = form.getvalue('spray_quality')
        
        no_spray_drift = form.getvalue('no_spray_drift')    
        incorporation_depth = form.getvalue('incorporation_depth')   
        solubility = form.getvalue('solubility')
        aerobic_aquatic_metabolism = form.getvalue('aerobic_aquatic_metabolism')
        hydrolysis = form.getvalue('hydrolysis')
        photolysis_aquatic_half_life = form.getvalue('photolysis_aquatic_half_life')
        
        if (application_method=='a' or application_method=='c'):
            incorporation_depth=0
        if (application_method=='d'):
            no_spray_drift=0     
        if  aerobic_aquatic_metabolism>0:
            hydrolysis_label='NA'
        else:
            hydrolysis_label=hydrolysis
               
################label selection###################################                    
        if application_method=='a':
            application_method_label='Aerial Spray'
            if aerial_size_dist=='a':
               aerial_size_dist_label='Very Fine to Fine'
               ground_spray_type_label='NA'
               spray_quality_label='NA'
               airblast_type_label='NA' 
            elif aerial_size_dist=='b':
               aerial_size_dist_label='Fine to Medium (EFED Default)'
               ground_spray_type_label='NA'
               spray_quality_label='NA'
               airblast_type_label='NA'
            elif aerial_size_dist=='c':
               aerial_size_dist_label='Medium to Coarse'
               ground_spray_type_label='NA'
               spray_quality_label='NA'
               airblast_type_label='NA'
            else:
               aerial_size_dist_label='Coarse to Very Coarse' 
               ground_spray_type_label='NA'
               spray_quality_label='NA'
               airblast_type_label='NA'
              
        elif application_method=='b':        
            application_method_label='Ground Spray'
            if ground_spray_type=='a':
                if spray_quality=='a':
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='Low Boom Ground Spray (20" or less)'
                    spray_quality_label='Fine (EFED Default)'
                    airblast_type_label='NA'
                else:
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='Low Boom Ground Spray (20" or less)'
                    spray_quality_label='Medium-Coarse'
                    airblast_type_label='NA'
            else:
                if spray_quality=='a':
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='High Boom Ground Spray (20-50"; EFED Default)'
                    spray_quality_label='Fine (EFED Default)'
                    airblast_type_label='NA'
                else:
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='High Boom Ground Spray (20-50"; EFED Default)'
                    spray_quality_label='Medium-Coarse'
                    airblast_type_label='NA'
        elif application_method=='c':
            application_method_label='Airblast Spray (Orchard & Vineyard)'
            if airblast_type=='a':
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='NA'
                    spray_quality_label='NA'
                    airblast_type_label='Orchards and Dormant Vineyards'
            else:
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='NA'
                    spray_quality_label='NA'
                    airblast_type_label='Foliated Vineyards'
        else:
            application_method_label='NA'
            aerial_size_dist_label='NA' 
            ground_spray_type_label='NA'
            spray_quality_label='NA'
            airblast_type_label='NA'
##########################################################################################                                        

        geneec_obj = geneec_model.geneec('single', chem_name, application_target, application_rate, number_of_applications, interval_between_applications, Koc, aerobic_soil_metabolism, wet_in, application_method, application_method_label, aerial_size_dist, ground_spray_type, airblast_type, spray_quality, no_spray_drift, incorporation_depth, solubility, aerobic_aquatic_metabolism, hydrolysis, photolysis_aquatic_half_life)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "GENEEC Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'geneec','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'geneec', 
                'model_attributes':'GENEEC Output'})
        html = html + geneec_tables.timestamp(geneec_obj)
        html = html + geneec_tables.table_all(geneec_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, geneec_obj.__dict__, 'geneec', 'single')
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', GENEECOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
