# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:50:49 2013

@author: MSnyder
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
import math
import csv
from agdrift import agdrift_model

cgitb.enable()

class agdriftOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        drop_size = form.getvalue('drop_size')
        ecosystem_type = form.getvalue('ecosystem_type')
        application_method = form.getvalue('application_method')
        boom_height = form.getvalue('boom_height')
        orchard_type = form.getvalue('orchard_type')

        results = agdrift_model.func(ecosystem_type, application_method, drop_size, orchard_type, boom_height)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'agdrift','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'agdrift', 
                'model_attributes':'AgDrift Output'})
        html = html + """
        <table border="1" class="out_1">
        <tr><H3>User Inputs</H3></tr>
        <tr>
        <td>Application method</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Drop size</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Ecosystem type</td>
        <td>%s</td>
        </tr>
        <tr>
        </table>
        """ % (application_method, drop_size, ecosystem_type)
        html = html +  """<table width="400" border="1", style="display:none">
                          <tr><H3>Results</H3></tr>
                          <tr>
                          <td>distance</td>
                          <td id="distance">%s</td>
                          </tr>
                          <tr>
                          <td>deposition</td>
                          <td id="deposition">%s</td>
                          </tr>
                          </table>"""%(results[0], results[1])
        html = html + template.render(templatepath + 'agdrift-output-jqplot.html', {})         
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)
          
app = webapp.WSGIApplication([('/.*', agdriftOutputPage)], debug=True)
        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()