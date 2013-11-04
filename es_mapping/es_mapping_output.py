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
        IUCN_Mammals = form.getvalue('IUCN_Mammals')
        IUCN_Mammals_Marine = form.getvalue('IUCN_Mammals_Marine')
        IUCN_Coral = form.getvalue('IUCN_Coral')
        IUCN_Reptiles = form.getvalue('IUCN_Reptiles')
        IUCN_Seagrasses = form.getvalue('IUCN_Seagrasses')
        IUCN_SeaCucumbers = form.getvalue('IUCN_SeaCucumbers')        
        IUCN_Mangrove = form.getvalue('IUCN_Mangrove')
        IUCN_MarineFish = form.getvalue('IUCN_MarineFish')

        USFWS_p = form.getvalue('USFWS_p')
        USFWS_l = form.getvalue('USFWS_l')

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
                    <tr>
                        <th id="iucn_mammals">IUCN_Mammals</th>
                        <td id="IUCN_Mammals">%s<td>
                    </tr>
                    <tr>
                        <th id="iucn_mammals_marine">IUCN_Mammals_Marine</th>
                        <td id="IUCN_Mammals_Marine">%s<td>
                    </tr>            
                    <tr>
                        <th id="iucn_coral">IUCN_Coral</th>
                        <td id="IUCN_Coral">%s<td>
                    </tr>
                    <tr>
                        <th id="iucn_reptiles">IUCN_Reptiles</th>
                        <td id="IUCN_Reptiles">%s<td>
                    </tr>
                    <tr>
                        <th id="iucn_seagrasses">IUCN_Seagrasses</th>
                        <td id="IUCN_Seagrasses">%s<td>
                    </tr> 
                    <tr>
                        <th id="iucn_seacucumbers">IUCN_SeaCucumbers</th>
                        <td id="IUCN_SeaCucumbers">%s<td>
                    </tr>
                    <tr>
                        <th id="iucn_mangrove">IUCN_Mangrove</th>
                        <td id="IUCN_Mangrove">%s<td>
                    </tr>
                    <tr>
                        <th id="iucn_marinefish">IUCN_MarineFish</th>
                        <td id="IUCN_MarineFish">%s<td>
                    </tr>
                    <tr>
                        <th id="usfws_p">USFWS_p</th>
                        <td id="USFWS_p">%s<td>
                    </tr>
                    <tr>
                        <th id="usfws_l">USFWS_l</th>
                        <td id="USFWS_l">%s<td>
                    </tr>                                                                                                                                                                                                                                         
                </table>
        """%(NSF, NSP, NSM, Crop, IUCN_Amphibians, IUCN_Birds, IUCN_Mammals,IUCN_Mammals_Marine, IUCN_Coral,IUCN_Reptiles,IUCN_Seagrasses,IUCN_SeaCucumbers,IUCN_Mangrove,IUCN_MarineFish,USFWS_p,USFWS_l)
        html = html + template.render(templatepath+'ManykmlDropbox_test.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', ESOutputPage)], debug=True)
        

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()                                                                                                         




    

