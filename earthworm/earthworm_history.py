# -*- coding: utf-8 -*-
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
from uber import uber_lib
import rest_funcs
import history_tables

class earthwormAlgorithmPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('earthworm/earthworm_history.txt','r')
        x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "Earthworm User History")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'earthworm','page':'history'})
        html = html + template.render(templatepath + '03ubertext_links_left.html', {})                       
        html = html + template.render(templatepath + '04uberalgorithm_start.html', {
                'model':'earthworm', 
                'model_attributes':'Earthworm User History', 
                'text_paragraph':x})
        html = html + template.render (templatepath + 'history_pagination.html', {})                
        hist_obj = rest_funcs.user_hist('admin', 'earthworm')
        html = html + history_tables.table_all(hist_obj)
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', earthwormAlgorithmPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    