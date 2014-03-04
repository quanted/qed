# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi, cgitb
cgitb.enable()
from exams import exams_model,exams_tables
from uber import uber_lib
import sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
import keys_Picloud_S3
import rest_funcs
import logging

class examsOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()   
        chem_name = form.getvalue('chemical_name')
        scenarios =form.getvalue('scenarios')
        farm =form.getvalue('farm_pond')
        mw = form.getvalue('molecular_weight')
        sol = form.getvalue('solubility')
        koc = form.getvalue('Koc')
        vp = form.getvalue('vapor_pressure')
        aem = form.getvalue('aerobic_aquatic_metabolism')
        anm = form.getvalue('anaerobic_aquatic_metabolism')
        aqp = form.getvalue('aquatic_direct_photolysis')
        tmper = form.getvalue('temperature')
        n_ph = float(form.getvalue('n_ph'))
        ph_out = []
        hl_out = []
        for i in range(int(n_ph)):
            j=i+1
            ph_temp = form.getvalue('ph'+str(j))
            ph_out.append(float(ph_temp))
            hl_temp = float(form.getvalue('hl'+str(j)))
            hl_out.append(hl_temp)  

        exams_obj = exams_model.exams(chem_name, scenarios, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out)
        # logging.info(vars(exams_obj))

        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "EXAMS Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'exams','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'exams', 
                'model_attributes':'EXAMS Output'})
        html = html + exams_tables.timestamp(exams_obj)
        html = html + exams_tables.table_all(exams_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, exams_obj.__dict__, 'exams', 'single')
        self.response.out.write(html)
app = webapp.WSGIApplication([('/.*', examsOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
