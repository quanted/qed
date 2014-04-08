import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import unittest
from StringIO import StringIO
import sys
sys.path.append("../rice")
from rice import rice_model,rice_tables
import csv
import logging
from uber import uber_lib

logger = logging.getLogger('RICEQaqcPage')

cwd= os.getcwd()
# data = csv.reader(open(cwd+'/rice/rice_unittest_inputs.csv'))
data = csv.reader(open(cwd+'/rice/rice_qaqc_inputs.csv'))
chemical_name=[]
mai=[]
a=[]
dsed=[]
pb=[]
dw=[]
osed=[]
kd=[]
#####Pre-defined outputs########
msed=[]
vw=[]
mai1=[]
cw=[]

data.next()
for row in data:
    chemical_name.append(str(row[0]))
    mai.append(float(row[1]))
    a.append(float(row[2]))  
    dsed.append(float(row[3]))
    pb.append(float(row[4]))
    dw.append(float(row[5]))
    osed.append(float(row[6]))        
    kd.append(float(row[7]))    
    msed.append(float(row[8]))
    vw.append(float(row[9]))
    mai1.append(float(row[10]))
    cw.append(float(row[11])) 

out_fun_Msed=[]
out_fun_Vw=[]
out_fun_Mai1=[]            
out_fun_Cw=[]            

rice_obj = rice_model.rice(True,True,chemical_name[0], mai[0], dsed[0], a[0], pb[0], dw[0], osed[0], kd[0])

rice_obj.chemical_name_expected=chemical_name[0]
rice_obj.msed_expected=msed[0]
rice_obj.vw_expected=vw[0]
rice_obj.mai1_expected=mai1[0]
rice_obj.cw_expected=cw[0]

                
class RiceQaqcPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "Rice QA/QC")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'rice','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'rice',
                'model_attributes':'Rice Model QAQC'})
        html = html + rice_tables.timestamp()
        html = html + rice_tables.table_all_qaqc(rice_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, rice_obj.__dict__, 'rice', 'qaqc')
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', RiceQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
