import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()

                
class beekhouryQaqcPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', 'title')
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'beekhoury','page':'qaqc'})
        html = html + template.render (templatepath + '03pop_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'beekhoury',
                'model_attributes':'Khoury QAQC'})
#        html = html =
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '05pop_ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', beekhouryQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
