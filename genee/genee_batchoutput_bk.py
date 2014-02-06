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
from genee import genee_model, genee_tables
import json
import base64
from google.appengine.api import urlfetch
import keys_Picloud_S3
import logging
logger = logging.getLogger('Geneec Batch')
from threading import Thread
from collections import OrderedDict

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}

###########################################################################
def update_dic(output_html, model_object_dict, model_name):
    all_dic = {"model_name":model_name, "_id":model_object_dict['jid'], "output_html":output_html, "model_object_dict":model_object_dict}
    data = json.dumps(all_dic)
    url='http://localhost:7777/update_history'
    # url=keys_Picloud_S3.amazon_ec2_ip+'/update_history'
    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   

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
genee_obj_all = []
all_threads = []
out_html_all = {}

def create_jid(row_inp,iter):
    chem_name.append(row_inp[0])
    application_target.append(row_inp[1])
    application_rate.append(float(row_inp[2]))
    number_of_applications.append(float(row_inp[3]))
    interval_between_applications.append(float(row_inp[4]))
    Koc.append(float(row_inp[5]))
    aerobic_soil_metabolism.append(float(row_inp[6]))
    wet_in.append(row_inp[7])
    application_method.append(row_inp[8])
    aerial_size_dist.append(row_inp[9])
    ground_spray_type.append(row_inp[10])
    airblast_type.append(row_inp[11])
    spray_quality.append(row_inp[12])
    no_spray_drift.append(float(row_inp[13]))
    incorporation_depth.append(float(row_inp[14]))
    solubility.append(float(row_inp[15]))
    aerobic_aquatic_metabolism.append(float(row_inp[16]))
    hydrolysis.append(float(row_inp[17]))
    photolysis_aquatic_half_life.append(float(row_inp[18]))

    genee_obj = genee_model.genee('batch', chem_name[iter], application_target[iter], application_rate[iter], number_of_applications[iter], interval_between_applications[iter], Koc[iter], aerobic_soil_metabolism[iter], wet_in[iter], application_method[iter], application_method_label, aerial_size_dist[iter], ground_spray_type[iter], airblast_type[iter], spray_quality[iter], no_spray_drift[iter], incorporation_depth[iter], solubility[iter], aerobic_aquatic_metabolism[iter], hydrolysis[iter], photolysis_aquatic_half_life[iter])
    logger.info(genee_obj)
    jid_all.append(genee_obj.jid)
    genee_obj_all.append(genee_obj)
    # genee_dict_list_all.append(genee_obj.__dict__)

    # genee_obj_temp =  genee_obj_all[j]
    # setattr(genee_obj_temp, 'output_val', output_val)
    # logger.info(genee_obj_temp)
    batch_header = """
        <div class="out_">
            <br><H3>Batch Calculation of Iteration %s:</H3>
        </div>
        """%(iter + 1)
    out_html_temp = batch_header + genee_tables.table_all(genee_obj)
    # out_html_all.append(out_html_temp)
    out_html_all[iter]=out_html_temp
    update_dic(out_html_temp, genee_obj.__dict__, 'geneec')

def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    i=0
    out_html=""
    for row in reader:
        p=Thread(target = create_jid, args = (row, i))
        all_threads.append(p)
        # create_jid(row, i)
        i=i+1
    # Start all threads
    [x.start() for x in all_threads]
    # Wait for all of them to finish
    [x.join() for x in all_threads]
    out_html_all_sort = OrderedDict(sorted(out_html_all.items()))
    return out_html_all_sort

    # out_html_all_sort = OrderedDict(sorted(out_html_all.items()))

    # logger.info(len(jid_all))
    # for j in range(len(jid_all)):

        # output_st = ""
        # url_st='http://localhost:7777/ubertool_history/'+ 'geneec/' + jid_all[j]
        # while output_st!="done":
        #     response_st = urlfetch.fetch(url=url_st, method=urlfetch.GET, headers=http_headers, deadline=60)
        #     output_st = json.loads(response_st.content)['status']

        # output_val = json.loads(response_st.content)['output']
        # print j

        # genee_obj_temp =  genee_obj_all[j]
        # setattr(genee_obj_temp, 'output_val', output_val)
        # logger.info(genee_obj_temp)
        # batch_header = """
        #     <div class="out_">
        #         <br><H3>Batch Calculation of Iteration %s:</H3>
        #     </div>
        #     """%(j + 1)

        # out_html = out_html + batch_header + genee_tables.table_all(genee_obj_temp)
        # logger.info(genee_obj_temp.__dict__)
        # update_dic(batch_header + genee_tables.table_all(genee_obj_temp), genee_obj_temp.__dict__, 'geneec')

    # return genee_tables.timestamp(genee_obj_temp) + out_html


class geneeBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['file-0']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '04uberoutput_start.html', {
                'model':'genee',
                'model_attributes':'Genee Batch Output'})
        html = html + "".join(iter_html.values())
        logger.info(iter_html.keys())
        html = html + template.render(templatepath + 'export_fortran.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', geneeBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
