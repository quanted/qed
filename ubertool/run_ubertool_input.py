# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

@author: jharston
"""

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from ubertool import run_ubertool_db

class UbertoolInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + 'ubertool_config_jquery.html', {})
        html = html + template.render(templatepath + '02uberintroblock_nomodellinks.html', {'title2':'Ubertool Inputs', 'model':'run_ubertool'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_batch_start.html', {'model':'run_ubertool'})
        html = html + template.render (templatepath + 'ubertool_multiple_runs.html', {})
        #html = html + str(run_ubertool_db.RunUbertoolInp())
        #html = html + template.render(templatepath + '04ubertext_checkbox.html', {})
        html = html + template.render(templatepath + '04ubertoolinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', UbertoolInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
