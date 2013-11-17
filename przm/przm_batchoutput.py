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

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string}
###########################################################################

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

def create_jid(row):
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

    jid_all.append(przm_obj.jid)
    przm_obj_all.append(przm_obj)


def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()

    out_html=""
    for row in reader:
        create_jid(row)

    for jj in range(len(jid_all)):
        # print jj
        output_st = ""
        while output_st!="done":
            response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid_all[jj], headers=http_headers)
            output_st = json.loads(response_st.content)['info']['%s' %jid_all[jj]]['status']

        url_val = 'https://api.picloud.com/job/result/?jid='+str(jid_all[jj])
        response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
        output_val = json.loads(response_val.content)['result']
        # print j

        przm_obj_temp =  przm_obj_all[jj]
        setattr(przm_obj_temp, 'final_res', output_val)
        setattr(przm_obj_temp, 'link', output_val[0])
        setattr(przm_obj_temp, 'iter_index', jj)
        # print 'przm_obj_temp.iter_index=', przm_obj_temp.iter_index
        logger.info(vars(przm_obj_temp))

        przm_obj_temp.x_precip=[float(i) for i in przm_obj_temp.final_res[1]]
        przm_obj_temp.x_runoff=[float(i) for i in przm_obj_temp.final_res[2]]
        przm_obj_temp.x_et=[float(i) for i in przm_obj_temp.final_res[3]]
        przm_obj_temp.x_irr=[float(i) for i in przm_obj_temp.final_res[4]]
        przm_obj_temp.x_leachate=[float(i) for i in przm_obj_temp.final_res[5]]
        przm_obj_temp.x_pre_irr=[i+j for i,j in zip(przm_obj_temp.x_precip, przm_obj_temp.x_irr)]
        przm_obj_temp.x_leachate=[i/100000 for i in przm_obj_temp.x_leachate]



        batch_header = """
            <div class="out_">
                <br><H3>Batch Calculation of Iteration %s:</H3>
            </div>
            """%(jj+1)

        out_html = out_html + batch_header + przm_tables.table_all(przm_obj_temp)
    return out_html


class przmBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        # thefile = form['upfile']
        thefile = form['file-0']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        # html = template.render(templatepath + '01uberheader.html', 'title')
        # html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'przm','page':'batchinput'})
        # html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = template.render(templatepath + '04uberoutput_start.html', {
                'model':'przm',
                'model_attributes':'PRZM Batch Output'})
        html = html + przm_tables.timestamp()
        html = html + iter_html
        html = html + template.render(templatepath + 'export_fortran.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        # html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', przmBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
