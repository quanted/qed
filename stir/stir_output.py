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
from stir import stir_model
from stir import stir_parameters
from stir import stir_tables
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
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
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

        html = html +stir_tables.timestamp()
        html = html + stir_tables.table_1(pvuheadings,tmpl,sm)
        html = html + stir_tables.table_2(pvuheadings,tmpl,sm)
        html = html + stir_tables.table_3(pvuheadings,tmpl,sm)
        html = html + stir_tables.table_4(pvuheadings,tmpl,sm)
        html = html + stir_tables.table_5(pvrheadings,tmpl,sm)
        # sat_air_conc = sm.sat_air_conc
        # inh_rate_avian = sm.inh_rate_avian
        # vid_avian = sm.vid_avian
        # ld50est = sm.ld50est
        # ld50adj = sm.ld50adj_avian
        # ratio_vd_avian = sm.ratio_vd_avian(stir_model.vid_avian(sat_air_conc,inh_rate_avian,assessed_bw_avian),stir_model.ld50adj_avian(stir_model.ld50est(ld50ao,ld50ri,ld50ro),assessed_bw_avian,tw_avian,mineau))
        # sid_avian = sm.sid_avian(stir_model.c_air(ar2,h),inh_rate_avian,ddsi,f_inhaled,assessed_bw_avian),
        # ratio_sid_avian = sm.ratio_sid_avian(stir_model.sid_avian(stir_model.c_air(ar2,h),inh_rate_avian,ddsi,f_inhaled,assessed_bw_avian),stir_model.ld50adj_avian(stir_model.ld50est(ld50ao,ld50ri,ld50ro),assessed_bw_avian,tw_avian,mineau)), 

        # html = html + stir_tables.table_3(pvuheadings,tmpl,sat_air_conc,inh_rate_avian,vid_avian,ld50est,ld50adj,ratio_vd_avian,sid_avian,ratio_sid_avian)

        # sm.LOC_vd_avian(stir_model.ratio_vd_avian(stir_model.vid_avian(sat_air_conc,inh_rate_avian,assessed_bw_avian),stir_model.ld50adj_avian(stir_model.ld50est(ld50ao,ld50ri,ld50ro),assessed_bw_avian,tw_avian,mineau))), 
        # sm.LOC_sid_avian(stir_model.ratio_sid_avian(stir_model.sid_avian(stir_model.c_air(ar2,h),inh_rate_avian,ddsi,f_inhaled,assessed_bw_avian),stir_model.ld50adj_avian(stir_model.ld50est(ld50ao,ld50ri,ld50ro),assessed_bw_avian,tw_avian,mineau))), 

        # html = html + """
        # <table border="1" class="out_2">
        #     <tr>
        #         <th colspan="3">STIR Outputs</th>
        #     </tr>
        #     <tr>
        #         <th colspan="3">Avian (%s kg)</th>
        #     </tr>
        #     <tr>
        #         <td>Saturated Air Concentration of Pesticide</td>
        #         <td>%0.2E</td>
        #         <td>mg/m<sup>3</sup></td>
        #     </tr>
        #     <tr>
        #         <td>Avian Inhalation Rate</td>
        #         <td>%0.2E</td>
        #         <td>cm<sup>3</sup>/hr</td>
        #     </tr>
        #     <tr>
        #         <td>Maximum 1-hour Avian Vapor Inhalation Dose</td>
        #         <td>%0.2E</td>
        #         <td>mg/kg-bw</td>
        #     </tr>
        #     <tr>
        #         <td>Estimated Avian Inhalation LD<sub>50</sub></td>
        #         <td>%0.2E</td>
        #         <td>mg/kg-bw</td>
        #     </tr>
        #     <tr>
        #         <td>Adjusted Avian Inhalation LD<sub>50</sub></td>
        #         <td>%0.2E</td>
        #         <td>mg/kg-bw</td>
        #     </tr>
        #     <tr>
        #         <td>Ratio of Vapor Dose to Adjusted Inhalation LD<sub>50</sub></td>
        #         <td>%0.2E</td>
        #         <td><H5><font color="red">%s</font></H5></td>
        #     </tr>
        #     <tr>
        #         <td>Spray Droplet Inhalation Dose of Assessed Bird</td>
        #         <td>%0.2E</td>
        #         <td>mg/kg-bw</td>
        #     </tr>
        #     <tr>
        #         <td>Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD<sub>50</sub></td>
        #         <td>%0.2E</td>
        #         <td><H5><font color="red">%s</font></H5></td>
        #     </tr>
        #     <tr>
        #         <th colspan="3">Mammalian (%s kg)</th>
        #     </tr>
        #     <tr>
        #         <td>Saturated Air Concentration of Pesticide</td>
        #         <td>%0.2E</td>
        #         <td>mg/m<sup>3</sup></td>
        #     </tr>
        #     <tr>
        #         <td>Mammalian Inhalation Rate</td>
        #         <td>%0.2E</td>
        #         <td>cm<sup>3</sup>/hr</td>
        #     </tr>
        #     <tr>
        #         <td>Maximum 1-hour Mammalian Vapor Inhalation Dose</td> 
        #         <td>%0.2E</td>
        #         <td>mg/kg</td>
        #     </tr>
        #     <tr>
        #         <td>Conversion of Mammalian Inhalation LC<sub>50</sub> to LD<sub>50</sub></td>
        #         <td>%0.2E</td>
        #         <td>mg/kg-bw</td>
        #     </tr>
        #     <tr>
        #         <td>Adjusted Mammalian Inhalation LD<sub>50</sub></td>
        #         <td>%0.2E</td>
        #         <td>mg/kg-bw</td>
        #     </tr>
        #     <tr>
        #         <td>Ratio of Vapor Dose to Adjusted Inhalation LD<sub>50</sub></td>
        #         <td>%0.2E</td>
        #         <td><H5><font color="red">%s</font></H5></td>
        #     </tr>
        #     <tr>
        #         <td>Spray Droplet Inhalation Dose of Assessed Mammal</td>
        #         <td>%0.2E</td>
        #         <td>mg/kg-bw</td>
        #     </tr>
        #     <tr>
        #         <td>Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD<sub>50</sub></td>
        #         <td>%0.2E</td>
        #         <td><H5><font color="red">%s</font></H5></td>
        #     </tr>
        # </table>
        # """ % (assessed_bw_avian, 
        #       sat_air_conc, 
        #       inh_rate_avian, 
        #       stir_model.vid_avian(sat_air_conc,stir_model.ir_avian(assessed_bw_avian),assessed_bw_avian), 
        #       stir_model.ld50est(ld50ao,ld50ri,ld50ro), 
        #       stir_model.ld50adj_avian(stir_model.ld50est(ld50ao,ld50ri,ld50ro),assessed_bw_avian,tw_avian,mineau), 
        #       stir_model.ratio_vd_avian(stir_model.vid_avian(sat_air_conc,inh_rate_avian,assessed_bw_avian),stir_model.ld50adj_avian(stir_model.ld50est(ld50ao,ld50ri,ld50ro),assessed_bw_avian,tw_avian,mineau)), 
        #       stir_model.LOC_vd_avian(stir_model.ratio_vd_avian(stir_model.vid_avian(sat_air_conc,inh_rate_avian,assessed_bw_avian),stir_model.ld50adj_avian(stir_model.ld50est(ld50ao,ld50ri,ld50ro),assessed_bw_avian,tw_avian,mineau))), 
        #       stir_model.sid_avian(stir_model.c_air(ar2,h),inh_rate_avian,ddsi,f_inhaled,assessed_bw_avian),
        #       stir_model.ratio_sid_avian(stir_model.sid_avian(stir_model.c_air(ar2,h),inh_rate_avian,ddsi,f_inhaled,assessed_bw_avian),stir_model.ld50adj_avian(stir_model.ld50est(ld50ao,ld50ri,ld50ro),assessed_bw_avian,tw_avian,mineau)), 
        #       stir_model.LOC_sid_avian(stir_model.ratio_sid_avian(stir_model.sid_avian(stir_model.c_air(ar2,h),inh_rate_avian,ddsi,f_inhaled,assessed_bw_avian),stir_model.ld50adj_avian(stir_model.ld50est(ld50ao,ld50ri,ld50ro),assessed_bw_avian,tw_avian,mineau))), 
        #       aw_mammal, 
        #       sat_air_conc, 
        #       stir_model.ir_mammal(aw_mammal), 
        #       stir_model.vid_mammal(sat_air_conc,stir_model.ir_mammal(aw_mammal),aw_mammal), 
        #       stir_model.ld50(lc50,stir_model.cf(stir_model.ir_mammal(aw_mammal),aw_mammal),dur), 
        #       stir_model.ld50adj_mammal(stir_model.ld50(lc50,stir_model.cf(stir_model.ir_mammal(aw_mammal), aw_mammal),dur),tw_mammal,aw_mammal), 
        #       stir_model.ratio_vd_mammal(stir_model.vid_mammal(sat_air_conc,stir_model.ir_mammal(aw_mammal),aw_mammal),stir_model.ld50adj_mammal(stir_model.ld50(lc50,stir_model.cf(stir_model.ir_mammal(aw_mammal), aw_mammal),dur),tw_mammal,aw_mammal)), 
        #       stir_model.LOC_vd_mammal(stir_model.ratio_vd_mammal(stir_model.vid_mammal(sat_air_conc,stir_model.ir_mammal(aw_mammal),aw_mammal),stir_model.ld50adj_mammal(stir_model.ld50(lc50,stir_model.cf(stir_model.ir_mammal(aw_mammal), aw_mammal),dur),tw_mammal,aw_mammal))), 
        #       stir_model.sid_mammal(stir_model.c_air(ar2,h),stir_model.ir_mammal(aw_mammal),ddsi,f_inhaled,aw_mammal),
        #       stir_model.ratio_sid_mammal(stir_model.sid_mammal(stir_model.c_air(ar2,h),stir_model.ir_mammal(aw_mammal),ddsi,f_inhaled,aw_mammal),stir_model.ld50adj_mammal(stir_model.ld50(lc50,stir_model.cf(stir_model.ir_mammal(aw_mammal), aw_mammal),dur),tw_mammal,aw_mammal)),
        #       stir_model.LOC_sid_mammal(stir_model.ratio_sid_mammal(stir_model.sid_mammal(stir_model.c_air(ar2,h),stir_model.ir_mammal(aw_mammal),ddsi,f_inhaled,aw_mammal),stir_model.ld50adj_mammal(stir_model.ld50(lc50,stir_model.cf(stir_model.ir_mammal(aw_mammal), aw_mammal),dur),tw_mammal,aw_mammal))))

        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', STIRExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

