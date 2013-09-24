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
from geneec import geneec_model,geneec_tables
import json
import base64
import urllib
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
GEEC_peak = []
GEEC_4avg = []
GEEC_21avg = []
GEEC_60avg = []
GEEC_90avg = []


def get_jid(geneec_obj):

    url='https://api.picloud.com/r/3303/geneec_fortran_s1' 

    APPRAT = geneec_obj.application_rate
    APPNUM = geneec_obj.number_of_applications
    APSPAC = geneec_obj.interval_between_applications
    KOC = geneec_obj.Koc
    METHAF = geneec_obj.aerobic_soil_metabolism
    WETTED = json.dumps(geneec_obj.wet_in)
    METHOD = json.dumps(geneec_obj.application_method)
    AIRFLG = json.dumps(geneec_obj.aerial_size_dist)
    YLOCEN = geneec_obj.no_spray_drift
    GRNFLG = json.dumps(geneec_obj.ground_spray_type)
    GRSIZE = json.dumps(geneec_obj.spray_quality)
    ORCFLG = json.dumps(geneec_obj.airblast_type)
    INCORP = geneec_obj.incorporation_depth
    SOL = geneec_obj.solubility
    METHAP = geneec_obj.aerobic_aquatic_metabolism
    HYDHAP = geneec_obj.hydrolysis
    FOTHAP = geneec_obj.photolysis_aquatic_half_life

    data = urllib.urlencode({"APPRAT":APPRAT, "APPNUM":APPNUM, "APSPAC":APSPAC, "KOC":KOC, "METHAF":METHAF, "WETTED":WETTED,
                             "METHOD":METHOD, "AIRFLG":AIRFLG, "YLOCEN":YLOCEN, "GRNFLG":GRNFLG, "GRSIZE":GRSIZE,
                             "ORCFLG":ORCFLG, "INCORP":INCORP, "SOL":SOL, "METHAP":METHAP, "HYDHAP":HYDHAP, "FOTHAP":FOTHAP})
    
    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers)    
    jid= json.loads(response.content)['jid']
    output_st = ''
    
    while output_st!="done":
        response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid, headers=http_headers)
        output_st = json.loads(response_st.content)['info']['%s' %jid]['status']

    url_val = 'https://api.picloud.com/job/result/?jid='+str(jid)
    response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
    output_val = json.loads(response_val.content)['result']
    return(jid, output_st, output_val)

def html_table(row_inp,iter):
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


    geneec_obj = geneec_model.geneec(chem_name[iter], application_target[iter], application_rate[iter], number_of_applications[iter], interval_between_applications[iter], Koc[iter], aerobic_soil_metabolism[iter], wet_in[iter], application_method[iter], application_method_label, aerial_size_dist[iter], ground_spray_type[iter], airblast_type[iter], spray_quality[iter], no_spray_drift[iter], incorporation_depth[iter], solubility[iter], aerobic_aquatic_metabolism[iter], hydrolysis[iter], photolysis_aquatic_half_life[iter])
    final_res=get_jid(geneec_obj)

    GEEC_peak.append(final_res[2][0])
    GEEC_4avg.append(final_res[2][1])
    GEEC_21avg.append(final_res[2][2])
    GEEC_60avg.append(final_res[2][3])
    GEEC_90avg.append(final_res[2][4])

    batch_header = """
        <div class="out_">
            <br><H3>Batch Calculation of Iteration %s:</H3>
        </div>
        """%(iter + 1)

    html = batch_header + geneec_tables.table_all(geneec_obj, final_res)
    return html

def loop_html(thefile):
    
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    i=0
    iter_html=""
    for row in reader:
        iter_html = iter_html +html_table(row,i)
        i=i+1

    # sum_html = geneec_tables.table_all_sum(geneec_tables.sumheadings, geneec_tables.tmpl, chem_name, application_target, application_rate, number_of_applications, interval_between_applications, Koc, aerobic_soil_metabolism, wet_in, application_method, application_method_label, aerial_size_dist, ground_spray_type, airblast_type, spray_quality, no_spray_drift, incorporation_depth, solubility, aerobic_aquatic_metabolism, hydrolysis, photolysis_aquatic_half_life,
    #             GEEC_peak, GEEC_4avg, GEEC_21avg, GEEC_60avg, GEEC_90avg)

    # return sum_html+iter_html
    return iter_html

def html_table_temp():
    sum_html = geneec_tables.table_all_sum(geneec_tables.sumheadings, geneec_tables.tmpl, chem_name, application_target, application_rate, number_of_applications, interval_between_applications, Koc, aerobic_soil_metabolism, wet_in, application_method, application_method_label, aerial_size_dist, ground_spray_type, airblast_type, spray_quality, no_spray_drift, incorporation_depth, solubility, aerobic_aquatic_metabolism, hydrolysis, photolysis_aquatic_half_life,
                GEEC_peak, GEEC_4avg, GEEC_21avg, GEEC_60avg, GEEC_90avg)    
    return sum_html

class geneecBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['upfile']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'geneec','page':'batchinput'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'geneec',
                'model_attributes':'GENEEC Batch Output'})
        html = html + geneec_tables.timestamp()
        html = html + iter_html
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', geneecBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
