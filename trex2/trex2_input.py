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
from django import forms
from uber import uber_lib

class trexInputPage(webapp.RequestHandler):
    def get(self):
        text_file = open('trex/trex_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "TREX 1.5.2 Inputs")
        html = html + template.render (templatepath + 'trex2-jquery.html', {})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'trex2','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})        
        html = html + template.render (templatepath + '04uberinput_start_tabbed.html', {
                'model':'trex2', 
                'model_attributes':'TREX 1.5.2 Inputs'})
        html = html + """<a href="trex_input.html" class="TREX1"> Want to Use TREX 1.4.1?</a>"""
        html = html + """
        <div class="input_nav">
            <ul>
                <li class="Chemical tabSel">Chemical</li>
                |<li class="Avian tabUnsel"> Avian</li>
                |<li class="Mammal tabUnsel"> Mammal</li>
            </ul>
        </div>
        """
        html = html + """<br><table class="tab tab_Chemical">"""
        html = html + str(trex2_parameters.trexInp_chem())
        html = html + """</table><table class="tab tab_Application tab_Chemical">
                                    <tr><th colspan="2" scope="col"><label for="id_noa">Number of Applications:</label></th>
                                        <td colspan="3" scope="col"><select name="noa" id="id_noa">
                                            <option value="1">1</option><option value="2">2</option><option value="3" selected>3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option><option value="11">11</option><option value="12">12</option><option value="13">13</option><option value="14">14</option><option value="15">15</option><option value="16">16</option><option value="17">17</option><option value="18">18</option><option value="19">19</option><option value="20">20</option><option value="21">21</option><option value="22">22</option><option value="23">23</option><option value="24">24</option><option value="25">25</option><option value="26">26</option><option value="27">27</option><option value="28">28</option><option value="29">29</option><option value="30">30</option></select>
                                        </td>
                                    </tr>
                                    <tr id="noa_header"><th width="18%">App#</th>
                                                                             <th width="18%" id="rate_head">Rate (lb ai/acre)</th>
                                                                             <th width="18%">Day of Application</th>
                                    </tr>
                                    <tr class="tab_noa1"><td><input name="jm1" type="text" size="5" value="1"/></td>
                                                         <td><input type="text" size="5" name="rate1" id="id_rate1" value="4"/></td>
                                                         <td><input type="text" size="5" name="day1" id="id_day1" value="0" /></td>
                                    </tr>""" 
        html = html + """</table><table class="tab tab_Avian" style="display:none">"""
        html = html + str(trex2_parameters.trexInp_bird())
        html = html + """</table><table class="tab tab_Mammal" style="display:none">"""
        html = html + str(trex2_parameters.trexInp_mammal())
        html = html + template.render(templatepath + '04uberinput_tabbed_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', trexInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    