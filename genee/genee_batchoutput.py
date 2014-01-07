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

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string}
###########################################################################


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
    jid_all.append(genee_obj.jid)
    genee_obj_all.append(genee_obj)




def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    i=0
    out_html=""
    for row in reader:
        create_jid(row, i)
        i=i+1

    for j in range(len(jid_all)):
        output_st = ""
        while output_st!="done":
        response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid_all[j], headers=http_headers)
        output_st = json.loads(response_st.content)['info']['%s' %jid_all[j]]['status']

        url_val = 'https://api.picloud.com/job/result/?jid='+str(jid_all[j])
        response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
        output_val = json.loads(response_val.content)['result']
        # print j

        genee_obj_temp =  genee_obj_all[j]
        setattr(genee_obj_temp, 'output_val', output_val)

        batch_header = """
            <div class="out_">
                <br><H3>Batch Calculation of Iteration %s:</H3>
            </div>
            """%(j + 1)

        out_html = out_html + batch_header + genee_tables.table_all(genee_obj_temp)

    return out_html


class geneeBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['file-0']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '04uberoutput_start.html', {
                'model':'genee',
                'model_attributes':'genee Batch Output'})
        html = html + genee_tables.timestamp()
        html = html + iter_html
        html = html + template.render(templatepath + 'export_fortran.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', geneeBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
