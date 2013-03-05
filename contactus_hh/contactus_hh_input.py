import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class contactusInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02hh_uberintroblock_nomodellinks.html', {'model':'contactus_hh'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render (templatepath + 'contactus_hh.html', {})                
        html = html + template.render(templatepath + '05hh_ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', contactusInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
