# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
from przm import przm_model
from przm import przm_tables

import logging
logger = logging.getLogger('PRZM Model')

class PRZMOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        # print form
        args={}
        for key in form:
            args[key] = form.getvalue(key)

        przm_obj = przm_model.przm(args)
        logger.info(vars(przm_obj))

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'przm','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'przm', 
                'model_attributes':'PRZM Output'})
        html = html + przm_tables.timestamp()
        html = html + przm_tables.table_all(przm_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', PRZMOutputPage)], debug=True)
        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()



