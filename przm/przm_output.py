# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
from przm import przm_model,przm_tables
from uber import uber_lib
import logging
logger = logging.getLogger('PRZM Model')
import rest_funcs

class PRZMOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        # print form
        args={}
        for key in form:
            args[key] = form.getvalue(key)
        args["run_type"] = "single"

        przm_obj = przm_model.przm(args)
        # logger.info(vars(przm_obj))

        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "PRZM Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'przm','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'przm', 
                'model_attributes':'PRZM Output'})
        html = html + przm_tables.timestamp(przm_obj)
        html = html + przm_tables.table_all(przm_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, przm_obj.__dict__, 'przm', 'single')
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', PRZMOutputPage)], debug=True)
        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()



