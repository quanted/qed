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


class STIRExecutePage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        chemical_name = form.getvalue('chemical_name')
        select_receptor = form.getvalue('select_receptor')
        ar2 = form.getvalue('application_rate')
        f_inhaled = form.getvalue('spray_drift')
        mw = form.getvalue('molecular_weight')
        vp = form.getvalue('vapor_pressure')
        ld50ao = form.getvalue('avian_oral_ld50')
        aw_avian = form.getvalue('body_weight_of_the_assessed_bird')
        tw_avian = form.getvalue('body_weight_of_the_tested_bird')
        mineau = form.getvalue('chemical_specific_mineau_scaling_factor')
        aw_mammal = form.getvalue('body_weight_of_the_assessed_mammal')
        tw_mammal = form.getvalue('body_weight_of_the_tested_mammal')
        h = form.getvalue('height_of_direct_spray_column')
        ddsi = form.getvalue('ddsi')
        lc50 = form.getvalue('mammalian_inhalation_lc50')
        dur = form.getvalue('duration_of_rat_inhalation_study')
        ld50ri = form.getvalue('rat_inhalation_ld50')
        ld50ro = form.getvalue('rat_oral_ld50')
        
        text_file = open('stir/stir_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'stir','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'stir', 
                'model_attributes':'STIR Output'})    
        html = html + """
        <table border="1" class="out_1>
            <tr>
                <th colspan="3">User Inputs</th>
            </tr>
            <tr>
                <td>Chemical Name</td>
                <td>%s</td>
                <td></td>
            </tr>
            <tr>
                <td>Receptor Selected</td>
                <td>%s</td>
                <td></td>
            </tr>
            <tr>
                <td>Pesticide Application Rate</td>
                <td>%s</td>
                <td>lbs ai/A</td>
            </tr>
            <tr>
                <td>Height of Sirect Spray Column</td>
                <td>%s</td>
                <td>m</td>
            </tr>
            <tr>
                <td>Fraction of Spray Inhaled</td>
                <td>%s</td>
                <td></td>
            </tr>
            <tr>
                <td>Duration of Direct Spray Inhalation</td>
                <td>%s</td>
                <td>minutes</td>
            </tr>
            <tr>
                <td>Molecular Weight</td>
                <td>%s</td>
                <td>g/mol</td>
            </tr>
            <tr>
                <td>Vapor Pressure</td>
                <td>%s</td>
                <td>torr</td>
            </tr>
            <tr>
                <td>Avian Oral LD<sub>50</sub></td>
                <td>%s</td>
                <td>mg/kg-bw</td>
            </tr>
            <tr>
                <td>Body Weight of Assessed Bird</td>
                <td>%s</td>
                <td>kg</td>
            </tr>
            <tr>
                <td>Chemical Specific Mineau Scaling Factor</td>
                <td>%s</td>
                <td></td>
            </tr>
            <tr>
                <td>Mammalian LC<sub>50</sub></td>
                <td>%s</td>
                <td>mg/kg-bw</td>
            </tr>
            <tr>
                <td>Duration of Rat Inhalation Study</td>
                <td>%s</td>
                <td>hrs</td>
            </tr>
            <tr>
                <td>Body Weight of Assessed Mammal</td>
                <td>%s</td>
                <td>kg</td>
            </tr>
            <tr>
                <td>Rat Inhalation LD<sub>50</sub></td>
                <td>%s</td>
                <td>mg/kg-bw</td>
            </tr>
            <tr>
                <td>Rat Oral LD<sub>50</sub></td>
                <td>%s</td>
                <td>mg/kg-bw</td>
            </tr>
        </table><br>
        """ % (chemical_name, select_receptor, ar2, h, f_inhaled, ddsi, mw, vp, ld50ao, aw_avian, mineau, lc50, dur, aw_mammal, ld50ri, ld50ro)

        html = html + """
        <table border="1" class="out_2">
            <tr>
                <th colspan="3">STIR Outputs</th>
            </tr>
            <tr>
                <th colspan="3">Avian (%s kg)</th>
            </tr>
            <tr>
                <td>Saturated Air Concentration of Pesticide</td>
                <td>%0.2E</td>
                <td>mg/m<sup>3</sup></td>
            </tr>
            <tr>
                <td>Avian Inhalation Rate</td>
                <td>%0.2E</td>
                <td>cm<sup>3</sup>/hr</td>
            </tr>
            <tr>
                <td>Maximum 1-hour Avian Vapor Inhalation Dose</td>
                <td>%0.2E</td>
                <td>mg/kg-bw</td>
            </tr>
            <tr>
                <td>Estimated Avian Inhalation LD<sub>50</sub></td>
                <td>%0.2E</td>
                <td>mg/kg-bw</td>
            </tr>
            <tr>
                <td>Adjusted Avian Inhalation LD<sub>50</sub></td>
                <td>%0.2E</td>
                <td>mg/kg-bw</td>
            </tr>
            <tr>
                <td>Ratio of Vapor Dose to Adjusted Inhalation LD<sub>50</sub></td>
                <td>%0.2E</td>
                <td><H5><font color="red">%s</font></H5></td>
            </tr>
            <tr>
                <td>Spray Droplet Inhalation Dose of Assessed Bird</td>
                <td>%0.2E</td>
                <td>mg/kg-bw</td>
            </tr>
            <tr>
                <td>Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD<sub>50</sub></td>
                <td>%0.2E</td>
                <td><H5><font color="red">%s</font></H5></td>
            </tr>
            <tr>
                <th colspan="3">Mammalian (%s kg)</th>
            </tr>
            <tr>
                <td>Saturated Air Concentration of Pesticide</td>
                <td>%0.2E</td>
                <td>mg/m<sup>3</sup></td>
            </tr>
            <tr>
                <td>Mammalian Inhalation Rate</td>
                <td>%0.2E</td>
                <td>cm<sup>3</sup>/hr</td>
            </tr>
            <tr>
                <td>Maximum 1-hour Mammalian Vapor Inhalation Dose</td> 
                <td>%0.2E</td>
                <td>mg/kg</td>
            </tr>
            <tr>
                <td>Conversion of Mammalian Inhalation LC<sub>50</sub> to LD<sub>50</sub></td>
                <td>%0.2E</td>
                <td>mg/kg-bw</td>
            </tr>
            <tr>
                <td>Adjusted Mammalian Inhalation LD<sub>50</sub></td>
                <td>%0.2E</td>
                <td>mg/kg-bw</td>
            </tr>
            <tr>
                <td>Ratio of Vapor Dose to Adjusted Inhalation LD<sub>50</sub></td>
                <td>%0.2E</td>
                <td><H5><font color="red">%s</font></H5></td>
            </tr>
            <tr>
                <td>Spray Droplet Inhalation Dose of Assessed Mammal</td>
                <td>%0.2E</td>
                <td>mg/kg-bw</td>
            </tr>
            <tr>
                <td>Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD<sub>50</sub></td>
                <td>%0.2E</td>
                <td><H5><font color="red">%s</font></H5></td>
            </tr>
        </table>
        """ % (aw_avian, 
               cs(vp,mw), 
ir_avian(aw_avian), 
vid_avian(cs(vp,mw),ir_avian(aw_avian),aw_avian), 
ld50est(ld50ao,ld50ri,ld50ro), 
ld50adj_avian(ld50est(ld50ao,ld50ri,ld50ro),aw_avian,tw_avian,mineau), 
ratio_vd_avian(vid_avian(cs(vp,mw),ir_avian(aw_avian),aw_avian),ld50adj_avian(ld50est(ld50ao,ld50ri,ld50ro),aw_avian,tw_avian,mineau)), 
LOC_vd_avian(ratio_vd_avian(vid_avian(cs(vp,mw),ir_avian(aw_avian),aw_avian),ld50adj_avian(ld50est(ld50ao,ld50ri,ld50ro),aw_avian,tw_avian,mineau))), 
sid_avian(c_air(ar2,h),ir_avian(aw_avian),ddsi,f_inhaled,aw_avian), 
ratio_sid_avian(sid_avian(c_air(ar2,h),ir_avian(aw_avian),ddsi,f_inhaled,aw_avian),ld50adj_avian(ld50est(ld50ao,ld50ri,ld50ro),aw_avian,tw_avian,mineau)), 
LOC_sid_avian(ratio_sid_avian(sid_avian(c_air(ar2,h),ir_avian(aw_avian),ddsi,f_inhaled,aw_avian),ld50adj_avian(ld50est(ld50ao,ld50ri,ld50ro),aw_avian,tw_avian,mineau))), 
               aw_mammal, 
               cs(vp,mw), 
ir_mammal(aw_mammal), 
vid_mammal(cs(vp,mw),ir_mammal(aw_mammal),aw_mammal), 
ld50(lc50,cf(ir_mammal, aw_mammal),dur), 
ld50adj_mammal(ld50(lc50,cf(ir_mammal, aw_mammal),dur),tw_mammal,aw_mammal), 
ratio_vd_mammal(vid_mammal(cs(vp,mw),ir_mammal(aw_mammal),aw_mammal),ld50adj_mammal(ld50(lc50,cf(ir_mammal, aw_mammal),dur),tw_mammal,aw_mammal)), 
LOC_vd_mammal(ratio_vd_mammal(vid_mammal(cs(vp,mw),ir_mammal(aw_mammal),aw_mammal),ld50adj_mammal(ld50(lc50,cf(ir_mammal, aw_mammal),dur),tw_mammal,aw_mammal))), 
sid_mammal(c_air(ar2,h),ir_mammal(aw_mammal),ddsi,f_inhaled,aw_mammal),
ratio_sid_mammal(sid_mammal(c_air(ar2,h),ir_mammal(aw_mammal),ddsi,f_inhaled,aw_mammal),ld50adj_mammal(ld50(lc50,cf(ir_mammal, aw_mammal),dur),tw_mammal,aw_mammal)),
LOC_sid_mammal(ratio_sid_mammal(sid_mammal(c_air(ar2,h),ir_mammal(aw_mammal),ddsi,f_inhaled,aw_mammal),ld50adj_mammal(ld50(lc50,cf(ir_mammal, aw_mammal),dur),tw_mammal,aw_mammal))))

        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', STIRExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

