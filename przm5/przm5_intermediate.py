# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from uber import uber_lib
import json
import logging
logger = logging.getLogger('PRZM5_int_Model')
import sys
import rest_funcs


class przm5IntermediatePage(webapp.RequestHandler):
    def post(self):
        data_all = json.load(sys.stdin)
        data_html = data_all["data_html"]
        jid = str(data_all["jid"])
        logger.info(data_all)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "")    
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'przm5','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {})
        html = html + data_html
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.update_html(html, jid, 'przm5')
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', przm5IntermediatePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    

