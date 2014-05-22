# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi, cgitb
cgitb.enable()
import logging
logger = logging.getLogger('historyoutputPage')
import rest_funcs
from przm import przm_tables
from uber import uber_lib



class historyoutputPage(webapp.RequestHandler):
    def get(self):
        form = cgi.FieldStorage() 
        jid = form.getvalue('jid')
        model_name = form.getvalue('model_name')
        results = rest_funcs.create_batchoutput_html(jid, model_name)
        iter_html=""
        for single_obj in results:

            batch_header = """
                <div class="out_">
                    <br><H3>Batch Calculation of Iteration %s:</H3>
                </div>
                """%(single_obj.iter_index+1)
            iter_html = iter_html + batch_header + przm_tables.table_all(single_obj)

        ####Finally, assemble batchout page############ 
        templatepath = os.path.dirname(__file__) + '/templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, 'Batch')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'przm','page':'output'})


        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'przm',
                'model_attributes':'PRZM Batch Output'})
        html = html + przm_tables.timestamp("", jid)
        html = html + iter_html
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})


        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', historyoutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    

