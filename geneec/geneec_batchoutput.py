import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from uber import uber_lib
import csv
from geneec import geneec_model, geneec_tables
import logging
logger = logging.getLogger('Geneec Batch')
from threading import Thread
import Queue
from collections import OrderedDict
import rest_funcs


chem_name = []
application_target = []
application_rate = []
number_of_applications = []
interval_between_applications = []
Koc = []
aerobic_soil_metabolism = []
wet_in = []
application_method = []
application_method_label = []
aerial_size_dist = []
ground_spray_type = []
airblast_type = []
spray_quality = []
no_spray_drift = []
incorporation_depth = []
solubility = []
aerobic_aquatic_metabolism = []
hydrolysis = []
photolysis_aquatic_half_life = []
####### Outputs ########
jid_all = []
jid_batch = []
geneec_obj_all = []
geneec_obj_all_dict = []
all_threads = []
out_html_all = {}
job_q = Queue.Queue()
thread_count = 10

def create_jid(row_inp):
    while True:
        row_inp_temp_all = row_inp.get()
        if row_inp_temp_all is None:
            break
        else:
            row_inp_temp = row_inp_temp_all[0]
            iter = row_inp_temp_all[1]

            chem_name_temp = row_inp_temp[0]
            application_target_temp = row_inp_temp[1]
            application_rate_temp = float(row_inp_temp[2])
            number_of_applications_temp = float(row_inp_temp[3])
            interval_between_applications_temp = float(row_inp_temp[4])
            Koc_temp = float(row_inp_temp[5])
            aerobic_soil_metabolism_temp = float(row_inp_temp[6])
            wet_in_temp = row_inp_temp[7]
            application_method_temp = row_inp_temp[8]
            aerial_size_dist_temp = row_inp_temp[9]
            ground_spray_type_temp = row_inp_temp[10]
            airblast_type_temp = row_inp_temp[11]
            spray_quality_temp = row_inp_temp[12]
            no_spray_drift_temp = float(row_inp_temp[13])
            incorporation_depth_temp = float(row_inp_temp[14])
            solubility_temp = float(row_inp_temp[15])
            aerobic_aquatic_metabolism_temp = float(row_inp_temp[16])
            hydrolysis_temp = float(row_inp_temp[17])
            photolysis_aquatic_half_life_temp = float(row_inp_temp[18])

            geneec_obj = geneec_model.geneec('batch', chem_name_temp, application_target_temp, application_rate_temp, number_of_applications_temp, interval_between_applications_temp, Koc_temp, aerobic_soil_metabolism_temp, wet_in_temp, application_method_temp, application_method_label, aerial_size_dist_temp, ground_spray_type_temp, airblast_type_temp, spray_quality_temp, no_spray_drift_temp, incorporation_depth_temp, solubility_temp, aerobic_aquatic_metabolism_temp, hydrolysis_temp, photolysis_aquatic_half_life_temp)
            # logger.info(genee_obj)
            jid_all.append(geneec_obj.jid)
            geneec_obj_all.append(geneec_obj)
            if iter == 0:
                jid_batch.append(geneec_obj.jid)

            batch_header = """
                <div class="out_">
                    <br><H3>Batch Calculation of Iteration %s:</H3>
                </div>
                """%(iter + 1)
            out_html_temp = batch_header + geneec_tables.table_all(geneec_obj)
            out_html_all[iter]=out_html_temp
            # save_dic(out_html_temp, genee_obj.__dict__, 'geneec')


def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    indx = 0
    for row in reader:
        job_q.put([row, indx])
        indx = indx + 1
    logger.info(job_q.qsize())

    # Start all threads
    all_threads = [Thread(target=create_jid, args=(job_q, )) for j in range(thread_count)]
    for x in all_threads:
        x.start()
    for x in all_threads:
        job_q.put(None)
    for x in all_threads:
        x.join()

    out_html_all_sort = OrderedDict(sorted(out_html_all.items()))
    return out_html_all_sort



class geneecBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['file-0']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")

        html = template.render(templatepath + '04uberoutput_start.html', {
                'model':'geneec',
                'model_attributes':'Geneec Batch Output'})
        html= html + """
                <div class="out_">
                    <b>GENEEC Version 2.0 (Beta)<br>
                </div>"""
        html = html + "".join(iter_html.values())
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        # logger.info(iter_html.keys())
        # logger.info(len(iter_html.keys()))

        rest_funcs.batch_save_dic(html, [x.__dict__ for x in geneec_obj_all], 'geneec', 'batch', jid_batch[0], ChkCookie, templatepath)
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', geneecBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
