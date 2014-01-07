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
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <table class="out_">
                <tr>
                    <th colspan="2">Inputs: Chemical Identity</th>
                </tr>
                <tr>
                    <td>Application method</td>
                    <td id="app_method_val">%s</td>
                </tr>
                <tr id="Orc_type">
                    <td>Orchard type</td>
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
            </table>
        </div>
        """ % (application_method, orchard_type, drop_size, ecosystem_type)
        html = html +  """
        <table style="display:none;">
            <tr>
                <td>distance</td>
                <td id="distance">%s</td>
            </tr>
            <tr>
                <td>deposition</td>
                <td id="deposition">%s</td>
            </tr>
        </table>
        <br>
        <h3 class="out_2 collapsible" id="section2"><span></span>Results</h3>
        <div>
        """%(results[0], results[1])
        html = html + template.render(templatepath + 'agdrift-output-jqplot.html', {})
        html = html +  """
        </div>
        """
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)
          
app = webapp.WSGIApplication([('/.*', agdriftOutputPage)], debug=True)
        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()