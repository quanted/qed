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
from pfam import pfam_parameters
from uber import uber_lib

class PFAMInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "PFAM Inputs")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'pfam','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start_tabbed.html', {
                'model':'pfam', 
                'model_attributes':'PFAM Inputs'})
        html = html + """
        <div class="input_nav">
            <ul>
                <li class="Chemical tabSel"> Chemical </li>
                |<li class="Application tabUnsel"> Application </li>
                |<li class="Location tabUnsel"> Location </li>
                |<li class="Floods tabUnsel"> Floods </li>
                |<li class="Crop tabUnsel"> Crop </li>
                |<li class="Physical tabUnsel"> Physical </li>
                |<li class="Output tabUnsel"> Output</li>
            </ul>
        </div>
        """
        html = html + """<br><table class="tab tab_Chemical" border="0">"""
        html = html + str(pfam_parameters.PFAMInp_chem())
        html = html + """</table><table class="tab tab_Application" border="0" style="display:none">
                                    <tr><th colspan="2" scope="col"><label for="id_noa">Number of Applications:</label></th>
                                        <td colspan="3" scope="col"><select name="noa" id="id_noa">
                                            <option value="">Make a selection</option>
                                            <option value="1">1</option>
                                            <option value="2">2</option>
                                            <option value="3">3</option>
                                            <option value="4">4</option>
                                            <option value="5">5</option>
                                            <option value="6">6</option>
                                            <option value="7">7</option>
                                            <option value="8">8</option>
                                            <option value="9">9</option>
                                            <option value="10">10</option>
                                            <option value="11">11</option>
                                            <option value="12">12</option>
                                            <option value="13">13</option>
                                            <option value="14">14</option>
                                            <option value="15">15</option>
                                            <option value="16">16</option>
                                            <option value="17">17</option>
                                            <option value="18">18</option>
                                            <option value="19">19</option>
                                            <option value="20">20</option>
                                            <option value="21">21</option>
                                            <option value="22">22</option>
                                            <option value="23">23</option>
                                            <option value="24">24</option>
                                            <option value="25">25</option>
                                            <option value="26">26</option>
                                            <option value="27">27</option>
                                            <option value="28">28</option>
                                            <option value="29">29</option>
                                            <option value="30">30</option>
                                        </td>
                                    </tr>"""        
                
        html = html + """</table><table class="tab tab_Location" border="0" style="display:none">"""    
        html = html + str(pfam_parameters.PFAMInp_loc())
        html = html + """</table><table class="tab tab_Floods" border="0" style="display:none">
                                    <tr><th></th><th colspan="2" scope="col"><label for="id_nof">Number of Floods Events:</label></th>
                                        <td colspan="2" scope="col"><select name="nof" id="id_nof">
                                            <option value="">Make a selection</option>
                                            <option value="1">1</option>
                                            <option value="2">2</option>
                                            <option value="3">3</option>
                                            <option value="4">4</option>
                                            <option value="5">5</option>
                                            <option value="6">6</option>
                                            <option value="7">7</option>
                                            <option value="8">8</option>
                                            <option value="9">9</option>
                                            <option value="10">10</option>
                                        </td>
                                    </tr>
                                    <tr><th></th><th colspan="2"><label for="id_date_f1">Date for Event 1:</label></th>
                                        <td colspan="2"><input type="text" name="date_f1" value="MM/DD" id="id_date_f1" /></td>
                                    </tr>"""    

        html = html + """</table><table class="tab tab_Crop" border="0" style="display:none">"""      
        html = html + str(pfam_parameters.PFAMInp_cro())                
        html = html + """</table><table class="tab tab_Physical" border="0" style="display:none">"""      
        html = html + str(pfam_parameters.PFAMInp_phy())
        html = html + """</table><table class="tab tab_Output" border="0" style="display:none">"""    
        html = html + str(pfam_parameters.PFAMInp_out())     
                
        html = html + template.render(templatepath + 'pfam-jquery.html', {})
        html = html + template.render(templatepath + '04uberinput_tabbed_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', PFAMInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
