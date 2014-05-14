# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
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
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'}) 
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'es_mapping_openlayer','page':'output'})
        html = html + template.render (templatepath + '03pop_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
            'model':'es_mapping_openlayer', 
            'model_attributes':'Endangered Species Mapper Output'})
        html = html + es_mapping_openlayer_tables.table_all(es_obj)
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        # self.response.headers['Content-Type'] = 'application/x-javascript'
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', ESOutputPage)], debug=True)
        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()