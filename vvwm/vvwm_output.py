# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from uber import uber_lib
import cgi
import cgitb
from vvwm import vvwm_model
# , vvwm_tables

import logging
logger = logging.getLogger('vvwm Model')


class vvwmOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        args={}
        for key in form:
            args[key] = form.getvalue(key)
        vvwm_obj = vvwm_model.vvwm(args)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie)
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'vvwm','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'vvwm', 
                'model_attributes':'VVWM Output'})
        # html = html + przm5_tables.table_all(przm5_obj)
        html = html + """
        <table width="600" border="1">
          
        </table>
        <p>&nbsp;</p>                     
        
        <table width="600" border="1">
        
        </table>
        """
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', vvwmOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    