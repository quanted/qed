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
from pfam import PFAMdb

class PFAMInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'pfam','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'pfam', 
                'model_attributes':'PFAM Inputs'})

        html = html + """<table><H4  align="center" id="id_tab">
            |<a href="#" class="Chemical"> Chemical </a>|
             <a href="#" class="Application"> Application </a>|
             <a href="#" class="Location"> Location </a>|
             <a href="#" class="Floods"> Floods </a>|
             <a href="#" class="Crop"> Crop </a>|
             <a href="#" class="Physical"> Physical </a>|
             <a href="#" class="Output"> Output </a>|
            </H4>"""
        html = html + """</table><br><table class="tab tab_Chemical" border="0">"""
        html = html + str(PFAMdb.PFAMInp_chem())
        html = html + """</table><table class="tab tab_Application" border="0" style="display:none">
                                    <tr><th colspan="2" scope="col"><label for="id_noa">Number of Applications:</label></th>
                                        <td colspan="3" scope="col"><select name="noa" id="id_noa">
                                            <option value="">Make a selection</option>
                                            <option value="1">1</option>
                                            <option value="2">2</option>
                                            <option value="3">3</option></select>
                                        </td>
                                    </tr>"""        
                
        html = html + """</table><table class="tab tab_Location" border="0" style="display:none">"""    
        html = html + str(PFAMdb.PFAMInp_loc())
        html = html + """</table><table class="tab tab_Floods" border="0" style="display:none">
                                    <tr><th></th><th colspan="2" scope="col"><label for="id_nof">Number of Floods Events:</label></th>
                                        <td colspan="2" scope="col"><select name="nof" id="id_nof">
                                            <option value="">Make a selection</option>
                                            <option value="1">1</option>
                                            <option value="2">2</option>
                                            <option value="3">3</option>
                                            </select>
                                        </td>
                                    </tr>
                                    <tr><th></th><th colspan="2"><label for="id_date_f1">Date for Event 1:</label></th>
                                        <td colspan="2"><input type="text" name="date_f1" value="MM/DD" id="id_date_f1" /></td>
                                    </tr>"""    
                         
        html = html + """</table><table class="tab tab_Crop" border="0" style="display:none">"""      
        html = html + str(PFAMdb.PFAMInp_cro())                
        html = html + """</table><table class="tab tab_Physical" border="0" style="display:none">"""      
        html = html + str(PFAMdb.PFAMInp_phy())
        html = html + """</table><table class="tab tab_Output" border="0" style="display:none">"""    
        html = html + str(PFAMdb.PFAMInp_out())     
                
        html = html + template.render(templatepath + 'pfam-jquery.html', {})
        html = html + template.render(templatepath + 'pfam_input_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', PFAMInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    