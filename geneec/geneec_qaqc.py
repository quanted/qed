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
############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string}
###########################################################################


cwd= os.getcwd()
data = csv.reader(open(cwd+'/geneec/geneec_qaqc.csv'))
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


data.next()
for row in data:
    chem_name.append(row[0])
    application_target.append(row[1])
    application_rate.append(float(row[2]))
    number_of_applications.append(float(row[3]))
    interval_between_applications.append(float(row[4]))
    Koc.append(float(row[5]))
    aerobic_soil_metabolism.append(float(row[6]))
    wet_in.append(row[7])
    application_method.append(row[8])
    aerial_size_dist.append(row[9])
    ground_spray_type.append(row[10])
    airblast_type.append(row[11])
    spray_quality.append(row[12])
    no_spray_drift.append(float(row[13]))
    incorporation_depth.append(float(row[14]))
    solubility.append(float(row[15]))
    aerobic_aquatic_metabolism.append(float(row[16]))
    hydrolysis.append(float(row[17]))
    photolysis_aquatic_half_life.append(float(row[18]))
    GEEC_peak.append(float(row[19]))
    GEEC_4avg.append(float(row[20]))
    GEEC_21avg.append(float(row[21]))
    GEEC_60avg.append(float(row[22]))
    GEEC_90avg.append(float(row[23]))

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


geneec_obj = geneec_model.geneec(chem_name[0], application_target[0], application_rate[0], number_of_applications[0], interval_between_applications[0], Koc[0], aerobic_soil_metabolism[0], wet_in[0], application_method[0], application_method_label, aerial_size_dist[0], ground_spray_type[0], airblast_type[0], spray_quality[0], no_spray_drift[0], incorporation_depth[0], solubility[0], aerobic_aquatic_metabolism[0], hydrolysis[0], photolysis_aquatic_half_life[0])
final_res=get_jid(geneec_obj)

geneec_obj.chem_name_exp = chem_name[0]
geneec_obj.GEEC_peak_exp = GEEC_peak[0]
geneec_obj.GEEC_4avg_exp = GEEC_4avg[0]
geneec_obj.GEEC_21avg_exp = GEEC_21avg[0]
geneec_obj.GEEC_60avg_exp = GEEC_60avg[0]
geneec_obj.GEEC_90avg_exp = GEEC_90avg[0]


class geneecQaqcPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'geneec','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'geneec',
                'model_attributes':'GENEEC QAQC'})
        html = html + geneec_tables.timestamp()
        html = html + geneec_tables.table_all_qaqc(geneec_obj, final_res)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', geneecQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
