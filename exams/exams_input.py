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
from exams import exams_parameters
from uber import uber_lib

class EXAMSInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "EXAMS Inputs")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'exams','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'exams', 
                'model_attributes':'EXAMS Inputs'})
        html = html + str(exams_parameters.EXAMSInp())
        html = html + """</table><table class="n_ph" align="center" border="0">
                                    <tr><th><label for="n_ph">Number of Different pH:</label></th>
                                        <td><select name="n_ph" id="n_ph">
                                            <option value="">Make a selection</option>
                                            <option value="3">3</option>
                                            <option value="4">4</option>
                                            <option value="5">5</option>
                                            <option value="6">6</option>
                                            <option value="7">7</option>
                                            <option value="8">8</option>
                                            <option value="9">9</option>
                                            <option value="10">10</option></select>
                                        </td>
                                    </tr>""" 
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render (templatepath + 'exams_input_jquery.html', {})
        html = html + template.render(templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', EXAMSInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    