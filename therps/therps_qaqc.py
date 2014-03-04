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
sys.path.append("../therps")
from therps import therps_model,therps_tables
from uber import uber_lib
import logging

logger = logging.getLogger('TherpsQaqcPage')

cwd= os.getcwd()
data = csv.reader(open(cwd+'/therps/therps_qaqc.csv'))

chem_name=[]
use=[]
formu_name=[]
a_i=[]
a_i_disp=[]
a_r=[]
n_a=[]
i_a=[]
h_l=[]
ld50_bird=[]
Species_of_the_tested_bird_avian_ld50=[]
bw_avian_ld50=[]
lc50_bird=[]
Species_of_the_tested_bird_avian_lc50=[]
bw_avian_lc50=[]
NOAEC_bird=[]
Species_of_the_tested_bird_avian_NOAEC=[]
bw_avian_NOAEC=[]
NOAEL_bird=[]
Species_of_the_tested_bird_avian_NOAEL=[]
bw_avian_NOAEL=[]
x=[]
c_mamm_a=[]
c_herp_a=[]
bw_herp_a_sm=[]
bw_herp_a_md=[]
bw_herp_a_lg=[]
wp_herp_a_sm=[]
wp_herp_a_md=[]
wp_herp_a_lg=[]

######Pre-defined outputs########
EEC_diet_herp_BL_exp=[]
EEC_ARQ_herp_BL_exp=[]
EEC_CRQ_herp_BL_exp=[]
EEC_diet_herp_FR_exp=[]
EEC_ARQ_herp_FR_exp=[]
EEC_CRQ_herp_FR_exp=[]
EEC_diet_herp_HM_exp=[]
EEC_ARQ_herp_HM_exp=[]
EEC_CRQ_herp_HM_exp=[]
EEC_diet_herp_IM_exp=[]
EEC_ARQ_herp_IM_exp=[]
EEC_CRQ_herp_IM_exp=[]
EEC_diet_herp_TP_exp=[]
EEC_ARQ_herp_TP_exp=[]
EEC_CRQ_herp_TP_exp=[]
LD50_AD_sm_exp=[]
LD50_AD_md_exp=[]
LD50_AD_lg_exp=[]
EEC_dose_BP_sm_exp=[]
EEC_dose_BP_md_exp=[]
EEC_dose_BP_lg_exp=[]
ARQ_dose_BP_sm_exp=[]
ARQ_dose_BP_md_exp=[]
ARQ_dose_BP_lg_exp=[]
EEC_dose_FR_sm_exp=[]
EEC_dose_FR_md_exp=[]
EEC_dose_FR_lg_exp=[]
ARQ_dose_FR_sm_exp=[]
ARQ_dose_FR_md_exp=[]
ARQ_dose_FR_lg_exp=[]
EEC_dose_HM_md_exp=[]
EEC_dose_HM_lg_exp=[]
ARQ_dose_HM_md_exp=[]
ARQ_dose_HM_lg_exp=[]
EEC_dose_IM_md_exp=[]
EEC_dose_IM_lg_exp=[]
ARQ_dose_IM_md_exp=[]
ARQ_dose_IM_lg_exp=[]
EEC_dose_TP_md_exp=[]
EEC_dose_TP_lg_exp=[]
ARQ_dose_TP_md_exp=[]
ARQ_dose_TP_lg_exp=[]

EEC_diet_herp_BL_exp_mean=[]
EEC_ARQ_herp_BL_exp_mean=[]
EEC_CRQ_herp_BL_exp_mean=[]
EEC_diet_herp_FR_exp_mean=[]
EEC_ARQ_herp_FR_exp_mean=[]
EEC_CRQ_herp_FR_exp_mean=[]
EEC_diet_herp_HM_exp_mean=[]
EEC_ARQ_herp_HM_exp_mean=[]
EEC_CRQ_herp_HM_exp_mean=[]
EEC_diet_herp_IM_exp_mean=[]
EEC_ARQ_herp_IM_exp_mean=[]
EEC_CRQ_herp_IM_exp_mean=[]
EEC_diet_herp_TP_exp_mean=[]
EEC_ARQ_herp_TP_exp_mean=[]
EEC_CRQ_herp_TP_exp_mean=[]
LD50_AD_sm_exp_mean=[]
LD50_AD_md_exp_mean=[]
LD50_AD_lg_exp_mean=[]
EEC_dose_BP_sm_exp_mean=[]
EEC_dose_BP_md_exp_mean=[]
EEC_dose_BP_lg_exp_mean=[]
ARQ_dose_BP_sm_exp_mean=[]
ARQ_dose_BP_md_exp_mean=[]
ARQ_dose_BP_lg_exp_mean=[]
EEC_dose_FR_sm_exp_mean=[]
EEC_dose_FR_md_exp_mean=[]
EEC_dose_FR_lg_exp_mean=[]
ARQ_dose_FR_sm_exp_mean=[]
ARQ_dose_FR_md_exp_mean=[]
ARQ_dose_FR_lg_exp_mean=[]
EEC_dose_HM_md_exp_mean=[]
EEC_dose_HM_lg_exp_mean=[]
ARQ_dose_HM_md_exp_mean=[]
ARQ_dose_HM_lg_exp_mean=[]
EEC_dose_IM_md_exp_mean=[]
EEC_dose_IM_lg_exp_mean=[]
ARQ_dose_IM_md_exp_mean=[]
ARQ_dose_IM_lg_exp_mean=[]
EEC_dose_TP_md_exp_mean=[]
EEC_dose_TP_lg_exp_mean=[]
ARQ_dose_TP_md_exp_mean=[]
ARQ_dose_TP_lg_exp_mean=[]

data.next()
for row in data:
    chem_name.append(str(row[0]))
    use.append(str(row[1]))
    formu_name.append(str(row[2]))
    a_i.append(float(row[3])/100)
    a_i_disp.append(100*float(row[3]))
    a_r.append(float(row[4]))
    n_a.append(float(row[5]))
    i_a.append(float(row[6]))
    h_l.append(float(row[7]))
    ld50_bird.append(float(row[8]))
    Species_of_the_tested_bird_avian_ld50.append(str(row[9]))
    bw_avian_ld50.append(float(row[10]))
    lc50_bird.append(float(row[11]))
    Species_of_the_tested_bird_avian_lc50.append(str(row[12]))
    bw_avian_lc50.append(float(row[13]))
    NOAEC_bird.append(float(row[14]))
    Species_of_the_tested_bird_avian_NOAEC.append(str(row[15]))
    bw_avian_NOAEC.append(float(row[16]))
    NOAEL_bird.append(float(row[17]))
    Species_of_the_tested_bird_avian_NOAEL.append(str(row[18]))
    bw_avian_NOAEL.append(float(row[19]))
    x.append(float(row[20]))
    c_mamm_a.append(float(row[21]))
    c_herp_a.append(float(row[22]))
    bw_herp_a_sm.append(float(row[23]))
    bw_herp_a_md.append(float(row[25]))
    bw_herp_a_lg.append(float(row[27]))
    wp_herp_a_sm.append(float(row[24])/100)
    wp_herp_a_md.append(float(row[26])/100)
    wp_herp_a_lg.append(float(row[28])/100)
##############Upper bound#############
    LD50_AD_sm_exp.append(float(row[29]))
    LD50_AD_md_exp.append(float(row[30]))
    LD50_AD_lg_exp.append(float(row[31]))
    EEC_dose_BP_sm_exp.append(float(row[32]))
    EEC_dose_BP_md_exp.append(float(row[33]))
    EEC_dose_BP_lg_exp.append(float(row[34]))
    ARQ_dose_BP_sm_exp.append(float(row[35]))
    ARQ_dose_BP_md_exp.append(float(row[36]))
    ARQ_dose_BP_lg_exp.append(float(row[37]))
    EEC_dose_FR_sm_exp.append(float(row[38]))
    EEC_dose_FR_md_exp.append(float(row[39]))
    EEC_dose_FR_lg_exp.append(float(row[40]))
    ARQ_dose_FR_sm_exp.append(float(row[41]))
    ARQ_dose_FR_md_exp.append(float(row[42]))
    ARQ_dose_FR_lg_exp.append(float(row[43]))
    EEC_dose_HM_md_exp.append(float(row[44]))
    EEC_dose_HM_lg_exp.append(float(row[45]))
    ARQ_dose_HM_md_exp.append(float(row[46]))
    ARQ_dose_HM_lg_exp.append(float(row[47]))
    EEC_dose_IM_md_exp.append(float(row[48]))
    EEC_dose_IM_lg_exp.append(float(row[49]))
    ARQ_dose_IM_md_exp.append(float(row[50]))
    ARQ_dose_IM_lg_exp.append(float(row[51]))
    EEC_dose_TP_md_exp.append(float(row[52]))
    EEC_dose_TP_lg_exp.append(float(row[53]))
    ARQ_dose_TP_md_exp.append(float(row[54]))
    ARQ_dose_TP_lg_exp.append(float(row[55]))

    EEC_diet_herp_BL_exp.append(float(row[56]))
    EEC_ARQ_herp_BL_exp.append(float(row[57]))
    EEC_diet_herp_FR_exp.append(float(row[58]))
    EEC_ARQ_herp_FR_exp.append(float(row[59]))
    EEC_diet_herp_HM_exp.append(float(row[60]))
    EEC_ARQ_herp_HM_exp.append(float(row[61]))

    EEC_diet_herp_IM_exp.append(float(row[62]))
    EEC_ARQ_herp_IM_exp.append(float(row[63]))
    EEC_diet_herp_TP_exp.append(float(row[64]))
    EEC_ARQ_herp_TP_exp.append(float(row[65]))
    EEC_CRQ_herp_BL_exp.append(float(row[66]))
    EEC_CRQ_herp_FR_exp.append(float(row[67]))
    EEC_CRQ_herp_HM_exp.append(float(row[68]))
    EEC_CRQ_herp_IM_exp.append(float(row[69]))
    EEC_CRQ_herp_TP_exp.append(float(row[70]))
###################Mean#############
    EEC_dose_BP_sm_exp_mean.append(float(row[71]))
    EEC_dose_BP_md_exp_mean.append(float(row[72]))
    EEC_dose_BP_lg_exp_mean.append(float(row[73]))
    ARQ_dose_BP_sm_exp_mean.append(float(row[74]))
    ARQ_dose_BP_md_exp_mean.append(float(row[75]))
    ARQ_dose_BP_lg_exp_mean.append(float(row[76]))
    EEC_dose_FR_sm_exp_mean.append(float(row[77]))
    EEC_dose_FR_md_exp_mean.append(float(row[78]))
    EEC_dose_FR_lg_exp_mean.append(float(row[79]))
    ARQ_dose_FR_sm_exp_mean.append(float(row[80]))
    ARQ_dose_FR_md_exp_mean.append(float(row[81]))
    ARQ_dose_FR_lg_exp_mean.append(float(row[82]))
    EEC_dose_HM_md_exp_mean.append(float(row[83]))
    EEC_dose_HM_lg_exp_mean.append(float(row[84]))
    ARQ_dose_HM_md_exp_mean.append(float(row[85]))
    ARQ_dose_HM_lg_exp_mean.append(float(row[86]))
    EEC_dose_IM_md_exp_mean.append(float(row[87]))
    EEC_dose_IM_lg_exp_mean.append(float(row[88]))
    ARQ_dose_IM_md_exp_mean.append(float(row[89]))
    ARQ_dose_IM_lg_exp_mean.append(float(row[90]))
    EEC_dose_TP_md_exp_mean.append(float(row[91]))
    EEC_dose_TP_lg_exp_mean.append(float(row[92]))
    ARQ_dose_TP_md_exp_mean.append(float(row[93]))
    ARQ_dose_TP_lg_exp_mean.append(float(row[94]))

    EEC_diet_herp_BL_exp_mean.append(float(row[95]))
    EEC_ARQ_herp_BL_exp_mean.append(float(row[96]))
    EEC_diet_herp_FR_exp_mean.append(float(row[97]))
    EEC_ARQ_herp_FR_exp_mean.append(float(row[98]))
    EEC_diet_herp_HM_exp_mean.append(float(row[99]))
    EEC_ARQ_herp_HM_exp_mean.append(float(row[100]))
    EEC_diet_herp_IM_exp_mean.append(float(row[101]))
    EEC_ARQ_herp_IM_exp_mean.append(float(row[102]))
    EEC_diet_herp_TP_exp_mean.append(float(row[103]))
    EEC_ARQ_herp_TP_exp_mean.append(float(row[104]))

    EEC_CRQ_herp_BL_exp_mean.append(float(row[105]))
    EEC_CRQ_herp_FR_exp_mean.append(float(row[106]))
    EEC_CRQ_herp_HM_exp_mean.append(float(row[107]))
    EEC_CRQ_herp_IM_exp_mean.append(float(row[108]))
    EEC_CRQ_herp_TP_exp_mean.append(float(row[109]))

    therps_obj = therps_model.therps(chem_name[0], use[0], formu_name[0], a_i[0], h_l[0], n_a[0], i_a[0], a_r[0], ld50_bird[0], lc50_bird[0], NOAEC_bird[0], NOAEL_bird[0], 
                                     Species_of_the_tested_bird_avian_ld50[0], Species_of_the_tested_bird_avian_lc50[0], Species_of_the_tested_bird_avian_NOAEC[0], Species_of_the_tested_bird_avian_NOAEL[0],
                                     bw_avian_ld50[0], bw_avian_lc50[0], bw_avian_NOAEC[0], bw_avian_NOAEL[0],
                                     x[0], bw_herp_a_sm[0], bw_herp_a_md[0], bw_herp_a_lg[0], wp_herp_a_sm[0], wp_herp_a_md[0], 
                                     wp_herp_a_lg[0], c_mamm_a[0], c_herp_a[0])

    therps_obj.LD50_AD_sm_exp = LD50_AD_sm_exp[0]
    therps_obj.LD50_AD_md_exp = LD50_AD_md_exp[0]
    therps_obj.LD50_AD_lg_exp = LD50_AD_lg_exp[0]
    therps_obj.EEC_dose_BP_sm_exp = EEC_dose_BP_sm_exp[0]
    therps_obj.EEC_dose_BP_md_exp = EEC_dose_BP_md_exp[0]
    therps_obj.EEC_dose_BP_lg_exp = EEC_dose_BP_lg_exp[0]
    therps_obj.ARQ_dose_BP_sm_exp = ARQ_dose_BP_sm_exp[0]
    therps_obj.ARQ_dose_BP_md_exp = ARQ_dose_BP_md_exp[0]
    therps_obj.ARQ_dose_BP_lg_exp = ARQ_dose_BP_lg_exp[0]
    therps_obj.EEC_dose_FR_sm_exp = EEC_dose_FR_sm_exp[0]
    therps_obj.EEC_dose_FR_md_exp = EEC_dose_FR_md_exp[0]
    therps_obj.EEC_dose_FR_lg_exp = EEC_dose_FR_lg_exp[0]
    therps_obj.ARQ_dose_FR_sm_exp = ARQ_dose_FR_sm_exp[0]
    therps_obj.ARQ_dose_FR_md_exp = ARQ_dose_FR_md_exp[0]
    therps_obj.ARQ_dose_FR_lg_exp = ARQ_dose_FR_lg_exp[0]
    therps_obj.EEC_dose_HM_md_exp = EEC_dose_HM_md_exp[0]
    therps_obj.EEC_dose_HM_lg_exp = EEC_dose_HM_lg_exp[0]
    therps_obj.ARQ_dose_HM_md_exp = ARQ_dose_HM_md_exp[0]
    therps_obj.ARQ_dose_HM_lg_exp = ARQ_dose_HM_lg_exp[0]
    therps_obj.EEC_dose_IM_md_exp = EEC_dose_IM_md_exp[0]
    therps_obj.EEC_dose_IM_lg_exp = EEC_dose_IM_lg_exp[0]
    therps_obj.ARQ_dose_IM_md_exp = ARQ_dose_IM_md_exp[0]
    therps_obj.ARQ_dose_IM_lg_exp = ARQ_dose_IM_lg_exp[0]
    therps_obj.EEC_dose_TP_md_exp = EEC_dose_TP_md_exp[0]
    therps_obj.EEC_dose_TP_lg_exp = EEC_dose_TP_lg_exp[0]
    therps_obj.ARQ_dose_TP_md_exp = ARQ_dose_TP_md_exp[0]
    therps_obj.ARQ_dose_TP_lg_exp = ARQ_dose_TP_lg_exp[0]

    therps_obj.EEC_diet_herp_BL_exp = EEC_diet_herp_BL_exp[0]
    therps_obj.EEC_ARQ_herp_BL_exp = EEC_ARQ_herp_BL_exp[0]
    therps_obj.EEC_diet_herp_FR_exp = EEC_diet_herp_FR_exp[0]
    therps_obj.EEC_ARQ_herp_FR_exp = EEC_ARQ_herp_FR_exp[0]
    therps_obj.EEC_diet_herp_HM_exp = EEC_diet_herp_HM_exp[0]
    therps_obj.EEC_ARQ_herp_HM_exp = EEC_ARQ_herp_HM_exp[0]

    therps_obj.EEC_diet_herp_IM_exp = EEC_diet_herp_IM_exp[0]
    therps_obj.EEC_ARQ_herp_IM_exp = EEC_ARQ_herp_IM_exp[0]
    therps_obj.EEC_diet_herp_TP_exp = EEC_diet_herp_TP_exp[0]
    therps_obj.EEC_ARQ_herp_TP_exp = EEC_ARQ_herp_TP_exp[0]
    therps_obj.EEC_CRQ_herp_BL_exp = EEC_CRQ_herp_BL_exp[0]
    therps_obj.EEC_CRQ_herp_FR_exp = EEC_CRQ_herp_FR_exp[0]
    therps_obj.EEC_CRQ_herp_HM_exp = EEC_CRQ_herp_HM_exp[0]
    therps_obj.EEC_CRQ_herp_IM_exp = EEC_CRQ_herp_IM_exp[0]
    therps_obj.EEC_CRQ_herp_TP_exp = EEC_CRQ_herp_TP_exp[0]
###################Mean#############
    therps_obj.EEC_dose_BP_sm_exp_mean = EEC_dose_BP_sm_exp_mean[0]
    therps_obj.EEC_dose_BP_md_exp_mean = EEC_dose_BP_md_exp_mean[0]
    therps_obj.EEC_dose_BP_lg_exp_mean = EEC_dose_BP_lg_exp_mean[0]
    therps_obj.ARQ_dose_BP_sm_exp_mean = ARQ_dose_BP_sm_exp_mean[0]
    therps_obj.ARQ_dose_BP_md_exp_mean = ARQ_dose_BP_md_exp_mean[0]
    therps_obj.ARQ_dose_BP_lg_exp_mean = ARQ_dose_BP_lg_exp_mean[0]
    therps_obj.EEC_dose_FR_sm_exp_mean = EEC_dose_FR_sm_exp_mean[0]
    therps_obj.EEC_dose_FR_md_exp_mean = EEC_dose_FR_md_exp_mean[0]
    therps_obj.EEC_dose_FR_lg_exp_mean = EEC_dose_FR_lg_exp_mean[0]
    therps_obj.ARQ_dose_FR_sm_exp_mean = ARQ_dose_FR_sm_exp_mean[0]
    therps_obj.ARQ_dose_FR_md_exp_mean = ARQ_dose_FR_md_exp_mean[0]
    therps_obj.ARQ_dose_FR_lg_exp_mean = ARQ_dose_FR_lg_exp_mean[0]
    therps_obj.EEC_dose_HM_md_exp_mean = EEC_dose_HM_md_exp_mean[0]
    therps_obj.EEC_dose_HM_lg_exp_mean = EEC_dose_HM_lg_exp_mean[0]
    therps_obj.ARQ_dose_HM_md_exp_mean = ARQ_dose_HM_md_exp_mean[0]
    therps_obj.ARQ_dose_HM_lg_exp_mean = ARQ_dose_HM_lg_exp_mean[0]
    therps_obj.EEC_dose_IM_md_exp_mean = EEC_dose_IM_md_exp_mean[0]
    therps_obj.EEC_dose_IM_lg_exp_mean = EEC_dose_IM_lg_exp_mean[0]
    therps_obj.ARQ_dose_IM_md_exp_mean = ARQ_dose_IM_md_exp_mean[0]
    therps_obj.ARQ_dose_IM_lg_exp_mean = ARQ_dose_IM_lg_exp_mean[0]
    therps_obj.EEC_dose_TP_md_exp_mean = EEC_dose_TP_md_exp_mean[0]
    therps_obj.EEC_dose_TP_lg_exp_mean = EEC_dose_TP_lg_exp_mean[0]
    therps_obj.ARQ_dose_TP_md_exp_mean = ARQ_dose_TP_md_exp_mean[0]
    therps_obj.ARQ_dose_TP_lg_exp_mean = ARQ_dose_TP_lg_exp_mean[0]

    therps_obj.EEC_diet_herp_BL_exp_mean = EEC_diet_herp_BL_exp_mean[0]
    therps_obj.EEC_ARQ_herp_BL_exp_mean = EEC_ARQ_herp_BL_exp_mean[0]
    therps_obj.EEC_diet_herp_FR_exp_mean = EEC_diet_herp_FR_exp_mean[0]
    therps_obj.EEC_ARQ_herp_FR_exp_mean = EEC_ARQ_herp_FR_exp_mean[0]
    therps_obj.EEC_diet_herp_HM_exp_mean = EEC_diet_herp_HM_exp_mean[0]
    therps_obj.EEC_ARQ_herp_HM_exp_mean = EEC_ARQ_herp_HM_exp_mean[0]
    therps_obj.EEC_diet_herp_IM_exp_mean = EEC_diet_herp_IM_exp_mean[0]
    therps_obj.EEC_ARQ_herp_IM_exp_mean = EEC_ARQ_herp_IM_exp_mean[0]
    therps_obj.EEC_diet_herp_TP_exp_mean = EEC_diet_herp_TP_exp_mean[0]
    therps_obj.EEC_ARQ_herp_TP_exp_mean = EEC_ARQ_herp_TP_exp_mean[0]

    therps_obj.EEC_CRQ_herp_BL_exp_mean = EEC_CRQ_herp_BL_exp_mean[0]
    therps_obj.EEC_CRQ_herp_FR_exp_mean = EEC_CRQ_herp_FR_exp_mean[0]
    therps_obj.EEC_CRQ_herp_HM_exp_mean = EEC_CRQ_herp_HM_exp_mean[0]
    therps_obj.EEC_CRQ_herp_IM_exp_mean = EEC_CRQ_herp_IM_exp_mean[0]
    therps_obj.EEC_CRQ_herp_TP_exp_mean = EEC_CRQ_herp_TP_exp_mean[0]


class TherpsQaqcPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "T-Herps QA/QC")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'therps','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'therps',
                'model_attributes':'T-Herps QAQC'})
        html = html + therps_tables.timestamp()
        html = html + therps_tables.table_all_qaqc(therps_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TherpsQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
