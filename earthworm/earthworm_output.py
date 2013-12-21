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
#from earthworm import earthworm_model, earthworm_tables
#import sys
#sys.path.append("../earthworm")

class earthwormOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        k_ow = form.getvalue('k_ow')
        l_f_e = form.getvalue('l_f_e')
        c_s = form.getvalue('c_s')
        k_d = form.getvalue('k_d')
        p_s = form.getvalue('p_s')
        c_w = form.getvalue('c_w')
        m_w = form.getvalue('m_w')
        p_e = form.getvalue('p_e')
        
        c_e = k_ow*l_f_e*(c_s/(k_d*p_s)+c_w)*m_w/p_e



        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie)   
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'earthworm','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'earthworm', 
                'model_attributes':'Earthworm Output'})
        html = html + """
        <table width="600" border="1">
          
        </table>
        <p>&nbsp;</p>                     
        
        <table width="600" border="1">
        
        </table>
        """
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', earthwormOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    