import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgi
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import django
from django import forms
from leslie_probit import leslie_probit_parameters

class leslie_probit_InputPage(webapp.RequestHandler):
    def get(self):       
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'leslie_probit','page':'input'})
        html = html + template.render (templatepath + '03pop_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start_tabbed.html', {
                'model':'leslie_probit', 
                'model_attributes':'Leslie Model with Probit Dose Response Inputs'})
        html = html + """
        <div class="input_nav">
            <ul>
                <li class="chem" style="color:#FFA500; font-weight:bold">Chemical</li>
                |<li class="dose" style="font-weight:bold"> Dose Response</li>
                |<li class="popu" style="font-weight:bold"> Leslie Matrix</li>
            </ul>
        </div>
        """
        html = html + """<br><table class="tab tab_chem" border="0">"""
        html = html + str(leslie_probit_parameters.leslie_probit_chem())
        html = html + """</table><table class="tab tab_app tab_chem" border="0">
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
        html = html + """</table><table class="tab tab_dose" border="0" style="display:none">"""
        html = html + str(leslie_probit_parameters.leslie_probit_dose())

        html = html + """</table><table class="tab tab_popu" border="0" style="display:none">"""
        html = html + str(leslie_probit_parameters.leslie_probit_popu())
        
        html = html + """<table class="tab tab_popu leslie" border="0" style="display:none">"""      
        html = html + """<table class="tab tab_popu no" border="0" style="display:none">"""             
        html = html + template.render(templatepath + 'leslie_probit_input_jquery.html', {})
        html = html + template.render(templatepath + '04uberinput_tabbed_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05pop_ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', leslie_probit_InputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
