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
sys.path.append("../sip")
from sip import sip_model,sip_tables
from uber import uber_lib
import logging

logger = logging.getLogger('SIPBatchPage')

chemical_name=[]
b_species=[]
m_species=[]
bw_quail=[]
bw_duck=[]
bwb_other=[]
bw_rat=[]
bwm_other=[]
avian_ld50=[]
mammalian_ld50=[]
sol=[]
aw_bird=[]
mineau=[]
aw_mamm=[]
noaec_d=[]
noaec_q=[]
noaec_o=[]
noael=[]
Species_of_the_bird_NOAEC_CHOICES=[]
noaec=[]

######Pre-defined outputs########
dose_bird_out = []
dose_mamm_out = []
at_bird_out = []
at_mamm_out = []
det_out = []
act_out = []
acute_bird_out = []
acuconb_out = []
acute_mamm_out = []
acuconm_out = []
chron_bird_out = []
chronconb_out = []
chron_mamm_out = []
chronconm_out = []

logger = logging.getLogger("SIPBatchOutput")

def html_table(row_inp,iter):
    logger.info("iteration: " + str(iter))
    chemical_name.append(str(row_inp[0]))
    b_species.append(float(row_inp[1]))
    m_species.append(float(row_inp[2]))
    bw_quail.append(float(row_inp[3]))
    bw_duck.append(float(row_inp[4]))
    bwb_other.append(float(row_inp[5])) 
    bw_rat.append(float(row_inp[6]))
    bwm_other.append(float(row_inp[7]))
    sol.append(float(row_inp[8]))
    avian_ld50.append(float(row_inp[9])) 
    mammalian_ld50.append(float(row_inp[10]))
    aw_bird.append(float(row_inp[11]))
    mineau.append(float(row_inp[12]))
    aw_mamm.append(float(row_inp[13]))
    noaec_d.append(float(row_inp[14]))
    noaec_q.append(float(row_inp[15]))
    noaec_o.append(float(row_inp[16]))
    noael.append(float(row_inp[17]))
    Species_of_the_bird_NOAEC_CHOICES.append(str(row_inp[18]))
    if Species_of_the_bird_NOAEC_CHOICES[iter] == '1':
        noaec.append(float(row_inp[14]))
    elif Species_of_the_bird_NOAEC_CHOICES[iter] == '2':
        noaec.append(float(row_inp[15]))
    elif Species_of_the_bird_NOAEC_CHOICES[iter] == '3':
        noaec.append(float(row_inp[16]))

    logger.info(chemical_name)
    logger.info(b_species)
    logger.info(m_species)
    logger.info(bw_quail)
    logger.info(bw_duck)
    logger.info(bwb_other)
    logger.info(bw_rat)
    logger.info(bwm_other)
    logger.info(sol)
    logger.info(avian_ld50)
    logger.info(mammalian_ld50)
    logger.info(aw_bird)
    logger.info(mineau)
    logger.info(aw_mamm)
    logger.info(noaec_d)
    logger.info(noaec_q)
    logger.info(noaec_o)
    logger.info(noael)
    logger.info(Species_of_the_bird_NOAEC_CHOICES)

    sip_obj = sip_model.sip(True,True,chemical_name[iter], b_species[iter], m_species[iter], bw_quail[iter],
                    bw_duck[iter], bwb_other[iter], bw_rat[iter], bwm_other[iter], sol[iter], avian_ld50[iter],
                    mammalian_ld50[iter], aw_bird[iter], mineau[iter], aw_mamm[iter], noaec_d[iter], noaec_q[iter], noaec_o[iter], Species_of_the_bird_NOAEC_CHOICES[iter], noael[iter])

    dose_bird_out.append(sip_obj.dose_bird_out)
    dose_mamm_out.append(sip_obj.dose_mamm_out)
    at_bird_out.append(sip_obj.at_bird_out)
    at_mamm_out.append(sip_obj.at_mamm_out)
    det_out.append(sip_obj.det_out)
    act_out.append(sip_obj.act_out)
    acute_bird_out.append(sip_obj.acute_bird_out)
    acuconb_out.append(sip_obj.acuconb_out)
    acute_mamm_out.append(sip_obj.acute_mamm_out)
    acuconm_out.append(sip_obj.acuconm_out)
    chron_bird_out.append(sip_obj.chron_bird_out)
    chronconb_out.append(sip_obj.chronconb_out)
    chron_mamm_out.append(sip_obj.chron_mamm_out)
    chronconm_out.append(sip_obj.chronconm_out)

    batch_header = """
        <div class="out_">
            <br><H3>Batch Calculation of Iteration %s:</H3>
        </div>
        """%(iter + 1)

    html = batch_header + sip_tables.table_all(sip_obj)
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

    sum_html = sip_tables.table_all_sum(sip_tables.sumheadings, sip_tables.tmpl, bw_quail,bw_duck,bwb_other,bw_rat,bwm_other,sol,
                    avian_ld50,mammalian_ld50,aw_bird,mineau,aw_mamm,noaec,noael,
                    dose_bird_out, dose_mamm_out, at_bird_out, 
                    at_mamm_out, det_out, act_out, acute_bird_out, acute_mamm_out, 
                    chron_bird_out, chron_mamm_out)

    return sum_html+iter_html
    # return iter_html


              
class SIPBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['file-0']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        # html = uber_lib.SkinChk(ChkCookie)
        # html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'sip','page':'batchinput'})
        # html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = template.render(templatepath + '04uberbatch_start.html', {
                'model':'sip',
                'model_attributes':'SIP Batch Output'})
        html = html + sip_tables.timestamp()
        html = html + iter_html
        # html = html + template.render(templatepath + 'sip-batchoutput-jqplot.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        # html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', SIPBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

