import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import csv
from fdadiet import fdadiet_model,fdadiet_tables

cwd=os.getcwd()
data=csv.reader(open(cwd+'/fdadiet/fdadiet_qaqc.csv'))
chemical_name=[]
trade_name=[]
run_use=[]
atuse_conc=[]
residue=[]
worst_case_est=[]
vol=[]
d=[]
h=[]
sa=[]
intake_avg=[]
intake_90th=[]

######Pre-defined outputs########
sa_cylinder=[]
conc_unit_conv=[]
edi=[]
edi_avg_vol=[]
edi_90th_vol=[]

data.next()
for row in data:
    chemical_name.append(str(row[0]))
    trade_name.append(str(row[1]))
    atuse_conc.append(float(row[2]))
    residue.append(float(row[3]))
    worst_case_est.append(float(row[4]))
    vol.append(float(row[5]))
    d.append(float(row[6]))
    h.append(float(row[7]))
    intake_avg.append(float(row[9]))
    intake_90th.append(float(row[10]))
    sa_cylinder.append(float(row[11]))
    conc_unit_conv.append(float(row[12]))
    edi.append(float(row[13]))
    edi_avg_vol.append(float(row[14]))
    edi_90th_vol.append(float(row[15]))


# Setting the model to run Tank Residue (Volumetric) model
run_use='1'
sa=0

# if run_use == '0':     / Logic used if user is given option of which model type to run on the QAQC page
#     run_use = '0'
# else:
#     run_use = '1'

fdadiet_obj = fdadiet_model.fdadiet(True,True,chemical_name[0],trade_name[0],run_use,atuse_conc[0],residue[0],worst_case_est[0],vol[0],d[0],h[0],sa,intake_avg[0],intake_90th[0])

fdadiet_obj.sa_cylinder_exp=sa_cylinder[0]
fdadiet_obj.conc_unit_conv_exp=conc_unit_conv[0]
fdadiet_obj.edi_exp=edi[0]
fdadiet_obj.edi_avg_vol_exp=edi_avg_vol[0]
fdadiet_obj.edi_90th_vol_exp=edi_90th_vol[0]

                
class fdadietQaqcPageOut(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', 'title')
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'fdadiet','page':'qaqc'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'fdadiet',
                'model_attributes':'FDA Dietary Exposure Model QAQC'})
        html = html + fdadiet_tables.timestamp()
        html = html + fdadiet_tables.table_all_qaqc(fdadiet_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', fdadietQaqcPageOut)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
