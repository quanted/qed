import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from uber import uber_lib

class webiceQaqcPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'webice','page':'qaqc'})
        html = html + template.render (templatepath + '03pop_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'webice',
                'model_attributes':'Web-ICE QAQC'})
#        html = html =
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', webiceQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
