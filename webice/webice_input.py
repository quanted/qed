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
from uber import uber_lib

class webiceInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie)
        html = html + template.render (templatepath + 'webice-jquery.html', {})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'webice','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04ubertext_start.html', {
                'model':'webice', 
                'model_attributes':'Web-ICE v3.2.1'})
        html = html + template.render (templatepath + 'webice.html', {})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', webiceInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()