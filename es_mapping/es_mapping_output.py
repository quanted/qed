# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import json
import base64
import urllib
from google.appengine.api import urlfetch


class ESOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()   
        
        NSF = form.getvalue('NSF')
        NSP = form.getvalue('NSP')
        NSM = form.getvalue('NSM')
        Crop = form.getvalue('Crop')

        IUCN_Amphibians = form.getvalue('IUCN_Amphibians')
        IUCN_Birds = form.getvalue('IUCN_Birds')


        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'es_mapping','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_esmapping_start.html', {
            'model':'es_mapping', 
            'model_attributes':'Endangered Species Mapper Output'})
        
        html = html + """
                <table class="out_">
                    <tr>
                        <th id="NSF">NSF</th>
                        <td id="nsf">%s<td>
                    </tr>
                    <tr>
                        <th id="NSP">NSP</th>
                        <td id="nsp">%s<td>
                    </tr>
                    <tr>
                        <th id="NSM">NSM</th>
                        <td id="nsm">%s<td>
                    </tr>
                    <tr>
                        <th id="Crop">Crop</th>
                        <td id="crop">%s<td>
                    </tr>
                    <tr>
                        <th id="iucn_amphibians">IUCN_Amphibians</th>
                        <td id="IUCN_Amphibians">%s<td>
                    </tr>   
                    <tr>
                        <th id="iucn_birds">IUCN_Birds</th>
                        <td id="IUCN_Birds">%s<td>
                    </tr>                                       
                </table>
        """%(NSF, NSP, NSM, Crop, IUCN_Amphibians, IUCN_Birds)
        html = html + template.render(templatepath+'ManykmlDropbox_test.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', ESOutputPage)], debug=True)
        

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()                                                                                                         




    

