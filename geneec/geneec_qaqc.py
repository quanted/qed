import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from StringIO import StringIO
import csv
from geneec import geneec_model, geneec_tables
from uber import uber_lib
import rest_funcs

cwd= os.getcwd()
data = csv.reader(open(cwd+'/geneec/geneec_qaqc.csv'))
chem_name = []
application_target = []
application_rate = []
number_of_applications = []
interval_between_applications = []
Koc = []
aerobic_soil_metabolism = []
wet_in = []
application_method = []
application_method_label = []
aerial_size_dist = []
ground_spray_type = []
airblast_type = []
spray_quality = []
no_spray_drift = []
incorporation_depth = []
solubility = []
aerobic_aquatic_metabolism = []
hydrolysis = []
photolysis_aquatic_half_life = []
####### Outputs ########
GEEC_peak = []
GEEC_4avg = []
GEEC_21avg = []
GEEC_60avg = []
GEEC_90avg = []


data.next()
for row in data:
    chem_name.append(row[0])
    application_target.append(row[1])
    application_rate.append(float(row[2]))
    number_of_applications.append(float(row[3]))
    interval_between_applications.append(float(row[4]))
    Koc.append(float(row[5]))
    aerobic_soil_metabolism.append(float(row[6]))
    wet_in.append(row[7])
    application_method.append(row[8])
    aerial_size_dist.append(row[9])
    ground_spray_type.append(row[10])
    airblast_type.append(row[11])
    spray_quality.append(row[12])
    no_spray_drift.append(float(row[13]))
    incorporation_depth.append(float(row[14]))
    solubility.append(float(row[15]))
    aerobic_aquatic_metabolism.append(float(row[16]))
    hydrolysis.append(float(row[17]))
    photolysis_aquatic_half_life.append(float(row[18]))
    GEEC_peak.append(float(row[19]))
    GEEC_4avg.append(float(row[20]))
    GEEC_21avg.append(float(row[21]))
    GEEC_60avg.append(float(row[22]))
    GEEC_90avg.append(float(row[23]))

geneec_obj = geneec_model.geneec("qaqc", chem_name[0], application_target[0], application_rate[0], number_of_applications[0], interval_between_applications[0], Koc[0], aerobic_soil_metabolism[0], wet_in[0], application_method[0], application_method_label, aerial_size_dist[0], ground_spray_type[0], airblast_type[0], spray_quality[0], no_spray_drift[0], incorporation_depth[0], solubility[0], aerobic_aquatic_metabolism[0], hydrolysis[0], photolysis_aquatic_half_life[0])
geneec_obj.chem_name_exp = chem_name[0]
geneec_obj.GEEC_peak_exp = GEEC_peak[0]
geneec_obj.GEEC_4avg_exp = GEEC_4avg[0]
geneec_obj.GEEC_21avg_exp = GEEC_21avg[0]
geneec_obj.GEEC_60avg_exp = GEEC_60avg[0]
geneec_obj.GEEC_90avg_exp = GEEC_90avg[0]


class geneecQaqcPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "GENEEC QA/QC")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'geneec','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'geneec',
                'model_attributes':'GENEE QAQC'})
        html = html + geneec_tables.timestamp(geneec_obj)
        html = html + geneec_tables.table_all_qaqc(geneec_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, geneec_obj.__dict__, 'geneec', 'qaqc')
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', geneecQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
