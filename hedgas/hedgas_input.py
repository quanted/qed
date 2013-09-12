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
from hedgas import hedgas_parameters

class hedgasInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'hedgas','page':'input'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'hedgas', 
                'model_attributes':'HED Gas Calculator Inputs'})
        html = html + """
        <h3>Acute HEC Non-Occupational:</h3>
        """
        html = html + str(hedgas_parameters.hedgas_acuteNonOcc_Inp())
        html = html + """
        </table><h3>ST-IT HEC Non-Occupational:</h3><table>
        """
        html = html + str(hedgas_parameters.hedgas_stitNonOcc_Inp())
        html = html + """
        </table>
        <p>*Developmental studies are 7 days per week for animal exposure whereas 13-week studies are 5 days a week.</p>
        <h3>LT HEC Non-Occupational:</h3><table>
        """
        html = html + str(hedgas_parameters.hedgas_ltNonOcc_Inp())
        html = html + """
        </table><h3>Acute HEC Occupational:</h3><table>
        """
        html = html + str(hedgas_parameters.hedgas_acuteOcc_Inp())
        html = html + """
        </table><h3>ST-IT HEC Occupational:</h3><table>
        """
        html = html + str(hedgas_parameters.hedgas_stitOcc_Inp())
        html = html + """
        </table><h3>LT HEC Occupational:</h3><table>
        """
        html = html + str(hedgas_parameters.hedgas_ltOcc_Inp())
        html = html + """
        </table>
        """
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05hh_ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', hedgasInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()