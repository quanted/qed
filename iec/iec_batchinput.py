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
               
class iecBatchInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "IEC Batch")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'iec','page':'batchinput'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatchinput.html', {
                'model':'iec',
                'model_attributes':'IEC Batch Input'}) 
        html = html + template.render(templatepath + '04uberbatchinput_jquery.html', {'model':'iec'}) 
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', iecBatchInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
