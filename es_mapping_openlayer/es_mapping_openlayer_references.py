# -*- coding: utf-8 -*-


import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os

class ESReferencesPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('es_mapping/es_mapping_references.txt','r')
        x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'es_mapping','page':'references'})
        html = html + template.render(templatepath + '03ubertext_links_left.html', {})                      
        html = html + template.render(templatepath + '04uberreferences_start.html', {
                'model':'es_mapping', 
                'model_attributes':'Endangered Species Mapper References', 
                'text_paragraph':x})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', ESReferencesPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    