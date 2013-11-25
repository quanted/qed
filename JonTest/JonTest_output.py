# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
from time import sleep

def testFunc(body_weight_of_bird):
    sleep(5)
    body_weight_of_bird = body_weight_of_bird * 2
    return body_weight_of_bird

class genericOutputPage(webapp.RequestHandler):
    def post(self):

        form = cgi.FieldStorage() 
        chemical_name = form.getvalue('chemical_name')
        body_weight_of_bird = float(form.getvalue('body_weight_of_bird'))

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheaderJon.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html',  {'model':'JonTest','page':'output'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'JonTest', 
                'model_attributes':'generic hh Output'})
        html = html + """
        <table width="600" border="1">
            <tr>
                <td>%s</td>
            </tr>  
        </table>
        <p>&nbsp;</p>
        
        """%testFunc(body_weight_of_bird)
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', genericOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    