# Screening Tool for Inhalation Risk (STIR)
#  Estimates inhalation-type exposure based on pesticide specific information
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
sys.path.append("../dust")
from stir import stir_model,stir_tables
from uber import uber_lib
from django.template import Context, Template

class STIRExecutePage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        chemical_name = form.getvalue('chemical_name')
        application_rate = form.getvalue('application_rate')
        column_height = form.getvalue('column_height')
        spray_drift_fraction = form.getvalue('spray_drift_fraction')
        direct_spray_duration = form.getvalue('direct_spray_duration')
        molecular_weight = form.getvalue('molecular_weight')
        vapor_pressure = form.getvalue('vapor_pressure')
        avian_oral_ld50 = form.getvalue('avian_oral_ld50')
        body_weight_assessed_bird = form.getvalue('body_weight_assessed_bird')
        body_weight_tested_bird = form.getvalue('body_weight_tested_bird')
        mineau_scaling_factor = form.getvalue('mineau_scaling_factor')
        mammal_inhalation_lc50 = form.getvalue('mammal_inhalation_lc50')
        duration_mammal_inhalation_study = form.getvalue('duration_mammal_inhalation_study')
        body_weight_assessed_mammal = form.getvalue('body_weight_assessed_mammal')
        body_weight_tested_mammal = form.getvalue('body_weight_tested_mammal')
        mammal_oral_ld50 = form.getvalue('mammal_oral_ld50')
        
        text_file = open('stir/stir_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "STIR Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'stir','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'stir', 
                'model_attributes':'STIR Output'})   
              
        pvuheadings = stir_tables.getheaderpvu()
        pvrheadings = stir_tables.getheaderpvr()
        djtemplate = stir_tables.getdjtemplate()
        tmpl = Template(djtemplate)
        
        #instantiate stir model object
        sm = stir_model.StirModel(True,True,chemical_name,application_rate,column_height,spray_drift_fraction,direct_spray_duration, 
            molecular_weight,vapor_pressure,avian_oral_ld50, body_weight_assessed_bird, body_weight_tested_bird, mineau_scaling_factor, 
            mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal, body_weight_tested_mammal, 
            mammal_oral_ld50)

        html = html + stir_tables.timestamp()
        html = html + stir_tables.table_1(pvuheadings,tmpl,sm)
        html = html + stir_tables.table_2(pvuheadings,tmpl,sm)
        html = html + stir_tables.table_3(pvuheadings,tmpl,sm)['html']
        html = html + stir_tables.table_4(pvuheadings,tmpl,sm)['html']
        html = html + stir_tables.table_5(pvrheadings,tmpl,sm)['html']
        
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', STIRExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

