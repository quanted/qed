# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from uber import uber_lib
import numpy as np
import cgi
import cgitb
cgitb.enable()
from earthworm import earthworm_model, earthworm_tables
import sys
sys.path.append("../earthworm")
from uber import uber_lib

import logging
logger = logging.getLogger('earthworm')

class earthwormOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        k_ow = float(form.getvalue('k_ow'))
        l_f_e = float(form.getvalue('l_f_e'))
        c_s = float(form.getvalue('c_s'))
        k_d = float(form.getvalue('k_d'))
        p_s = float(form.getvalue('p_s'))
        c_w = float(form.getvalue('c_w'))
        m_w = float(form.getvalue('m_w'))
        p_e = float(form.getvalue('p_e'))
        
        earthworm_obj = earthworm_model.earthworm(True,True,k_ow,l_f_e,c_s,k_d,p_s,c_w,m_w,p_e)
        logger.info(vars(earthworm_obj))
        
        # text_file = open('earthworm/earthworm_description.txt','r')
        # x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "Earthworm Output")   
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'earthworm','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'earthworm', 
                'model_attributes':'Earthworm Output'})
        
        html = html + earthworm_tables.timestamp()
        html = html + earthworm_tables.table_all(earthworm_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', earthwormOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    