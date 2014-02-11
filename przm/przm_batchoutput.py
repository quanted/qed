import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from StringIO import StringIO
import csv
from przm import przm_batchmodel, przm_tables
import json
import base64
import urllib
from google.appengine.api import urlfetch
import keys_Picloud_S3
import logging
logger = logging.getLogger('PRZM Batch Model')
from uber import uber_lib
from threading import Thread
import Queue
# import multiprocessing
from collections import OrderedDict
import rest_funcs

chem_name = []
NOA = []
Scenarios = []
Unit = []
appdate = []
apm = []
apr = []
cam = []
depi = []

####### Outputs ########
jid_all = []
przm_obj_all = []
jid_batch = []
all_threads = []
out_html_all = {}
job_q = Queue.Queue()
thread_count = 10


def html_table(row_inp_all):
    while True:
        row_inp_temp_all = row_inp_all.get()
        if row_inp_temp_all is None:
            break
        else:
            row = row_inp_temp_all[0]
            iter = row_inp_temp_all[1]
            logger.info("iteration: " + str(iter))

            chem_name_temp = str(row[0])
            chem_name.append(chem_name_temp)
            NOA_temp = str(row[1])
            NOA.append(NOA_temp)
            Scenarios_temp = str(row[2])
            Scenarios.append(Scenarios_temp)
            Unit_temp = str(row[3])
            Unit.append(Unit_temp)
            appdate_temp = str(row[4]).split(',')
            appdate.append(appdate_temp)
            apm_temp = str(row[5]).split(',')
            apm.append(apm_temp)
            apr_temp = str(row[6]).split(',')
            apr.append(apr_temp)
            cam_temp = str(row[7]).split(',')
            cam.append(cam_temp)
            depi_temp = str(row[8]).split(',')
            depi.append(depi_temp)
            przm_obj = przm_batchmodel.przm_batch(chem_name_temp, NOA_temp, Scenarios_temp, Unit_temp, appdate_temp, apm_temp, apr_temp, cam_temp, depi_temp)
            setattr(przm_obj, 'iter_index', iter)

            jid_all.append(przm_obj.jid)
            przm_obj_all.append(przm_obj)
            if iter == 0:
                jid_batch.append(przm_obj.jid)

            batch_header = """
                <div class="out_">
                    <br><H3>Batch Calculation of Iteration %s:</H3>
                </div>
                """%(iter+1)
            out_html_temp = batch_header + przm_tables.table_all(przm_obj)
            out_html_all[iter]=out_html_temp


def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()

    i=0
    iter_html=""
    for row in reader:
        job_q.put([row, i])
        i=i+1

    all_threads = [Thread(target=html_table, args=(job_q, )) for j in range(thread_count)]
    for x in all_threads:
        x.start()
    for x in all_threads:
        job_q.put(None)
    for x in all_threads:
        x.join()
    html_timestamp = przm_tables.timestamp("", jid_batch[0])
    out_html_all_sort = OrderedDict(sorted(out_html_all.items()))

    return html_timestamp + "".join(out_html_all_sort.values())


class przmBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['file-0']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = template.render(templatepath + '04uberoutput_start.html', {
                'model':'przm',
                'model_attributes':'PRZM Batch Output'})
        # html = html + przm_tables.timestamp()
        html = html + iter_html
        logger.info(out_html_all)
        # html = html + template.render(templatepath + 'export_fortran.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        # html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.batch_save_dic(html, [x.__dict__ for x in przm_obj_all], 'przm', 'batch', jid_batch[0], ChkCookie, templatepath)
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', przmBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
