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
from es_mapping_openlayer import es_mapping_openlayer_model, es_mapping_openlayer_tables


import logging
logger = logging.getLogger('ES Model')

class ESOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()   

        args={}
        for key in form:
            args[key] = form.getvalue(key)
        es_obj = es_mapping_openlayer_model.es_mapping_openlayer(args)
        logger.info(vars(es_obj))

        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "Endangered Species Mapper Output")    
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'es_mapping_openlayer','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
            'model':'es_mapping_openlayer', 
            'model_attributes':'Endangered Species Mapper Output'})
        html = html + es_mapping_openlayer_tables.table_all(es_obj)
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', ESOutputPage)], debug=True)
        

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()                                                                                                         




    

