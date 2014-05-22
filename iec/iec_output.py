# -*- coding: utf-8 -*-

# IEC
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
#from iec import iec_input      <---- HAS THIS BEEN DONE?  (I JUST CHANGED THE NAME)
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
import logging
import sys
sys.path.append("../utils")
import utils.json_utils
sys.path.append("../iec")
from iec import iec_model,iec_tables
from uber import uber_lib
from django.template import Context, Template
import rest_funcs

class IecOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        LC50 = float(form.getvalue('LC50'))
        threshold = float(form.getvalue('threshold'))
        dose_response = float(form.getvalue('dose_response'))
        iec_obj = iec_model.iec(True,True,'single',dose_response, LC50, threshold, None)
        text_file = open('iec/iec_description.txt','r')
        x1 = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "IEC Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'iec','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'iec', 
                'model_attributes':'IEC Output'})
        html = html + iec_tables.timestamp(iec_obj)
        html = html + iec_tables.table_all(iec_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, iec_obj.__dict__, "iec", "single")
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', IecOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

     
