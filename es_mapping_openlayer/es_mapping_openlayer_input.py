import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from django import forms
from es_mapping_openlayer import es_mapping_openlayer_parameters


class esInputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + 'mapper_openlayer_jQuery.html', {})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'es_mapping_openlayer','page':'input'})
        html = html + template.render (templatepath + '03pop_ubertext_links_left.html', {})        
        html = html + template.render (templatepath + '04uberinput_start.html', {
                'model':'es_mapping_openlayer', 
                'model_attributes':'Endangered Species Mapper Inputs'})
        html = html + str(es_mapping_openlayer_parameters.esInp())
        html = html + template.render (templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render (templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', esInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

