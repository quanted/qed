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
from przm import przmdb



class PRZMInputPage(webapp.RequestHandler):
    def get(self):
        #text_file1 = open('geneec/geneec_description.txt','r')
        #x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        #html = html + template.render(templatepath + 'geneec-jQuery.html', {})
        html = html + template.render(templatepath + '02uberintroblock.html', {'title2':'PRZM Input Page', 'title3':''})
        html = html + template.render (templatepath + '03cubertext_links_left.html', {})                
        html = html + template.render(templatepath + '02modellinkblock.html', {'model':'przm'})
        html = html + template.render(templatepath + '03euberinput_start.html', {'model':'przm'})
        html = html + str(przmdb.PRZMInp())
        html = html + template.render(templatepath + '03duberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '03cubertext_links.html', {})
        html = html + template.render(templatepath + '05uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', PRZMInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    