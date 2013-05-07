# -*- coding: utf-8 -*-

# IEC
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
#from iec import iec_input      <---- HAS THIS BEEN DONE?  (I JUST CHANGED THE NAME)
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
#import numpy as np
import cgi
import math 
import cgitb
cgitb.enable()



 
class genericJonOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheaderJon.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinksJon.html', {'model':'genericJon','page':'output'})
        html = html + template.render (templatepath + '03hh_ubertext_links_leftJon.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'genericJon', 
                'model_attributes':'GenericJon Output'})
        html = html + """
        <h3 class="collapsible" id="section1">User Inputs</h3>
            <div class="container_output">
                <table class="out_">
                    <tr><th colspan="2">Inputs: Testing1</th></tr>
                    <tr>
                        <td>Long string.............................................</td>
                        <td>Long string.............................................</td>
                    </tr>
                    <tr>
                        <td>Long string.............................................</td>
                        <td>Long string.............................................</td>
                    </tr>
                    <tr>
                        <td>Long string.............................................</td>
                        <td>Long string.............................................</td>
                    </tr>
                </table>
            </div>
        <br>

        <h3 class="collapsible" id="section2">Model Input</h3>
            <div class="container_output">
                <table class="out_">
                    <tr><th colspan="2">Inputs: Testing2</th></tr>
                    <tr>
                        <td>Long string.............................................</td>
                        <td>Long string.............................................</td>
                    </tr>
                    <tr>
                        <td>Long string.............................................</td>
                        <td>Long string.............................................</td>
                    </tr>
                    <tr>
                        <td>Long string.............................................</td>
                        <td>Long string.............................................</td>
                    </tr>
                </table>
            </div>
        """
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)
        
        

app = webapp.WSGIApplication([('/.*', genericJonOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    