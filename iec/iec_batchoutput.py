# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import unittest
from StringIO import StringIO
from pprint import pprint
import csv
import sys
sys.path.append("../iec")
from iec import iec_model,iec_tables
from uber import uber_lib
import logging

logger = logging.getLogger('IECBatchPage')
dose_response = []
LC50 = []
threshold = []

######Pre-defined outputs########
z_score_f_out = []
F8_f_out = []
chance_f_out = []

def html_table(row_inp,iter):
    logger.info("iteration: " + str(iter))
    dose_response.append(float(row_inp[0]))
    LC50.append(float(row_inp[1]))
    threshold.append(float(row_inp[2]))

    iec_obj = iec_model.iec(True,True, dose_response[iter],LC50[iter],threshold[iter])

    z_score_f_out.append(iec_obj.z_score_f_out)
    F8_f_out.append(iec_obj.F8_f_out)
    chance_f_out.append(iec_obj.chance_f_out)


    html = iec_tables.table_all(iec_obj)

    return html
                
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    logger.info(header)
    i=0
    iter_html=""
    for row in reader:
        iter_html = iter_html +html_table(row,i)
        i=i+1

    sum_html = iec_tables.table_all_sum(dose_response,LC50,threshold,
                    z_score_f_out, F8_f_out, chance_f_out)

    return sum_html+iter_html
    # return iter_html


              
class IECBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['upfile']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie)
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'iec','page':'batchinput'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {
                'model':'iec',
                'model_attributes':'IEC Batch Output'})
        html = html + iec_tables.timestamp()
        html = html + iter_html
        # html = html + template.render(templatepath + 'sip-batchoutput-jqplot.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', IECBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

