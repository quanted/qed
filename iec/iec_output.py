# -*- coding: utf-8 -*-

# IEC
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
#from iec import iec_input      <---- HAS THIS BEEN DONE?  (I JUST CHANGED THE NAME)
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
from iec import iec_model

class IecOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        LC50 = float(form.getvalue('LC50'))
        threshold = float(form.getvalue('threshold'))
        dose_response = float(form.getvalue('dose_response'))
        text_file = open('iec/iec_description.txt','r')
        x1 = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'iec','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'iec', 
                'model_attributes':'IEC Output'})
        html = html + """
        <table width="400" border="1" class="out_1">
          <tr>
            <th width="200" scope="col">User Inputs</th>
            <th width="200" scope="col">Values</th>
          </tr>
          <tr>
            <td>LC50 or LD50</td>
            <td>%.2f</td>
          </tr>          
          <tr>
           <td>Threshold</td>
           <td>%.2f</td>
          </tr>          
          <tr>
           <td>Slope</td>
           <td>%.2f</td>
          </tr>
        </table>
        <p>&nbsp;</p>                     
        """%(LC50, threshold, dose_response)                   
        html = html + """
        <table width="400" border="1" class="out_2">
          <tr>
            <th width="200" scope="col">IEC Outputs</th>
            <th width="200" scope="col">Values</th>
          </tr>
          <tr>
            <td>Z Score</td>
            <td>%.2f</td>
          </tr>           
          <tr>
            <td>"F8"</td>
            <td>%.8f</td>
          </tr>           
          <tr>
            <td>Chance of Individual Effect</td>
            <td>%.2f</td>
          </tr>          
        </table>
        """%(iec_model.z_score_f(dose_response, LC50, threshold), iec_model.F8_f(dose_response, LC50, threshold), iec_model.chance_f(dose_response, LC50, threshold))
        html = html + template.render(templatepath + 'getpdf_jon.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', IecOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

     