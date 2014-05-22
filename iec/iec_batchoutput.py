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
import Queue
from collections import OrderedDict
import rest_funcs

logger = logging.getLogger('IECBatchPage')
dose_response = []
LC50 = []
threshold = []

######Pre-defined outputs########
z_score_f_out = []
F8_f_out = []
chance_f_out = []
jid_all = []
jid_batch = []
iec_obj_all = []
iec_obj_temp = []

def html_table(row_inp,iter):
    logger.info("iteration: " + str(iter))
    dose_response.append(float(row_inp[0]))
    LC50.append(float(row_inp[1]))
    threshold.append(float(row_inp[2]))

    Input_header="""<div class="out_">
                        <br><H3>Batch Calculation of Iteration %s</H3>
                    </div>"""%(iter)

    iec_obj_temp = iec_model.iec(True,True, 'batch',dose_response[iter-1],LC50[iter-1],threshold[iter-1])
    iec_obj_temp.loop_indx = str(iter)

    z_score_f_out.append(iec_obj_temp.z_score_f_out)
    F8_f_out.append(iec_obj_temp.F8_f_out)
    chance_f_out.append(iec_obj_temp.chance_f_out)


    #html = iec_tables.table_all(iec_obj)

    jid_all.append(iec_obj_temp.jid)
    iec_obj_all.append(iec_obj_temp)    
    if iter == 1:
        jid_batch.append(iec_obj_temp.jid)
    
    table_all_out = iec_tables.table_all(iec_obj_temp)

    html_table_temp = Input_header + table_all_out + "<br>"

    return html_table_temp
    #return html
                
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    logger.info(header)
    i=1
    #iter_html=""
    iter_html_temp=""
    for row in reader:
        #iter_html = iter_html +html_table(row,i)
        iter_html_temp = iter_html_temp +html_table(row,i)
        i=i+1

    sum_html = iec_tables.table_all_sum(dose_response,LC50,threshold,
                    z_score_f_out, F8_f_out, chance_f_out)
    return sum_html+iter_html_temp

    #return sum_html+iter_html
    # return iter_html


              
class IECBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['file-0']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        # html = uber_lib.SkinChk(ChkCookie)
        # html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'iec','page':'batchinput'})
        # html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = template.render(templatepath + '04uberbatch_start.html', {
                'model':'iec',
                'model_attributes':'IEC Batch Output'})
        html = html + iec_tables.timestamp("",jid_batch[0])
        html = html + iter_html
        # html = html + template.render(templatepath + 'sip-batchoutput-jqplot.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        # html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.batch_save_dic(html, [x.__dict__ for x in iec_obj_all], 'iec', 'batch', jid_batch[0], ChkCookie, templatepath)
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', IECBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

