# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012
@author: thong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from trex2 import trex2_parameters
from agdrift_trex import agdrift_trex_parameters
from django import forms
from uber import uber_lib

class agdrift_trexInputPage(webapp.RequestHandler):
    def get(self):
        text_file = open('agdrift_trex/agdrift_trex_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "AgDrift-TREX Inputs")
        html = html + template.render (templatepath + 'agdrift_trex_jquery.html', {})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'agdrift_trex','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})        
        html = html + template.render (templatepath + '04uberinput_start_tabbed.html', {
                'model':'agdrift_trex', 
                'model_attributes':'Agdrift and Trex Inputs'})
        html = html + """
        <div class="input_nav">
            <ul>
                <li class="Agdrift tabSel">Agdrift</li>
                |<li class="Chemical tabUnsel">Chemical</li>
                |<li class="Avian tabUnsel"> Avian</li>
                |<li class="Mammal tabUnsel"> Mammal</li>
            </ul>
        </div>
        """
        html = html + """<br><table class="tab tab_Agdrift" border="0">"""
        html = html + str(agdrift_trex_parameters.agdriftInp())
        html = html + """<br><table class="tab tab_Chemical" border="0" style="display:none">"""
        html = html + str(trex2_parameters.trexInp_chem())
        html = html + """</table><table class="tab tab_Application tab_Chemical" border="0" style="display:none">
                                    <tr><th colspan="2" scope="col"><label for="id_noa">Number of Applications:</label></th>
                                        <td colspan="3" scope="col"><select name="noa" id="id_noa">
                                            <option value="1"  selected>1</option></select>
                                        </td>
                                    </tr>
                                    <tr id="noa_header"><th width="18%">App#</th>
                                                                             <th width="18%" id="rate_head">Rate (lb ai/acre)</th>
                                                                             <th width="18%">Day of Application</th>
                                    </tr>
                                    <tr class="tab_noa1"><td><input name="jm1" type="text" size="5" value="1"/></td>
                                                         <td><input type="text" size="5" name="rate1" id="id_rate1" value="4"/></td>
                                                         <td><input type="text" size="5" name="day1" id="id_day1" value="0" disabled/></td>
                                    </tr>""" 
        html = html + """</table><table class="tab tab_Avian" border="0" style="display:none">"""
        html = html + str(trex2_parameters.trexInp_bird())
        html = html + """</table><table class="tab tab_Mammal" border="0" style="display:none">"""
        html = html + str(trex2_parameters.trexInp_mammal())
        html = html + template.render(templatepath + '04uberinput_tabbed_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', agdrift_trexInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    
    