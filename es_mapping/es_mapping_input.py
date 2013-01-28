'''
Created on May 23, 2012

@author: th
'''
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
from es_mapping import es_mapping_db


class esInputPage(webapp.RequestHandler):
    def get(self):
#        text_file = open('trex/trex_description.txt','r')
#        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + 'mapper-jQuery.html', {})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'es_mapping'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})        
        html = html + template.render (templatepath + '04uberinput_start.html', {'model':'es_mapping'})
        html = html + str(es_mapping_db.esInp())
        html = html + template.render (templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render (templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', esInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()