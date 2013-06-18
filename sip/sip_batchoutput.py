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
from iec import iec_output
from pprint import pprint
import csv
import sys
sys.path.append("../sip")
from sip import sip_model_new,sip_tables
import logging

logger = logging.getLogger('SIPBatchPage')

bw_bird=[]
bw_mamm=[]
avian_ld50=[]
mammalian_ld50=[]
sol = []
aw_bird=[]
tw_bird=[]
mineau=[]
aw_mamm=[]
tw_mamm=[]
avian_noaec=[]
avian_noael=[]
mammalian_noaec=[]
mammalian_noael=[]

######Pre-defined outputs########
fw_bird_out = []
fw_mamm_out = []
dose_bird_out = []
dose_mamm_out = []
at_bird_out = []
at_mamm_out = []
fi_bird_out = []
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
    bw_bird_temp=float(row_inp[0])
    bw_bird.append(bw_bird_temp)
    bw_mamm_temp=float(row_inp[1])
    bw_mamm.append(bw_mamm_temp)
    sol_temp=float(row_inp[2])
    sol.append(sol_temp)
    avian_ld50_temp=float(row_inp[3])
    avian_ld50.append(avian_ld50_temp)
    mammalian_ld50_temp=float(row_inp[4])
    mammalian_ld50.append(mammalian_ld50_temp)
    aw_bird_temp=float(row_inp[5])        
    aw_bird.append(aw_bird_temp)
    tw_bird_temp=float(row_inp[6])   
    tw_bird.append(tw_bird_temp)
    mineau_temp=float(row_inp[7])
    mineau.append(mineau_temp)
    aw_mamm_temp=float(row_inp[8])
    aw_mamm.append(aw_mamm_temp)
    tw_mamm_temp=float(row_inp[9])   
    tw_mamm.append(tw_mamm_temp)
    avian_noaec_temp=float(row_inp[10])   
    avian_noaec.append(avian_noaec_temp)
    avian_noael_temp=float(row_inp[11])   
    avian_noael.append(avian_noael_temp)
    mammalian_noaec_temp=float(row_inp[12])   
    mammalian_noaec.append(mammalian_noaec_temp)
    mammalian_noael_temp=float(row_inp[13])   
    mammalian_noael.append(mammalian_noael_temp)

    sip_obj = sip_model_new.sip(True,True,'', bw_bird[0], bw_mamm[0], sol[0], avian_ld50[0], mammalian_ld50[0], aw_bird[0], tw_bird[0], mineau[0], aw_mamm[0], tw_mamm[0], avian_noaec[0], avian_noael[0])    

    fw_bird_out.append(sip_obj.fw_bird_out)
    fw_mamm_out.append(sip_obj.fw_mamm_out)
    dose_bird_out.append(sip_obj.dose_bird_out)
    dose_mamm_out.append(sip_obj.dose_mamm_out)
    at_bird_out.append(sip_obj.at_bird_out)
    at_mamm_out.append(sip_obj.at_mamm_out)
    fi_bird_out.append(sip_obj.fi_bird_out)
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

    html = sip_tables.table_all(sip_obj)
               
    return html  
                
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    logger.info(header)
    i=1
    iter_html=""
    for row in reader:
        iter_html = iter_html +html_table(row,i)
        i=i+1

    sum_html = sip_tables.table_all_sum(sip_tables.sumheadings, sip_tables.tmpl, bw_bird, 
                    bw_mamm, avian_ld50, mammalian_ld50, sol, aw_bird, tw_bird, mineau,
                    aw_mamm, tw_mamm, avian_noaec, avian_noael, mammalian_noaec, mammalian_noael,
                    fw_bird_out, fw_mamm_out, dose_bird_out, dose_mamm_out, at_bird_out, 
                    at_mamm_out, fi_bird_out, det_out, 
                    act_out, acute_bird_out, acute_mamm_out, 
                    chron_bird_out, chron_mamm_out)

    return sum_html+iter_html



              
class SIPBatchOutputPage(webapp.RequestHandler):
    def post(self):
        text_file1 = open('sip/sip_description.txt','r')
        x = text_file1.read()
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['upfile']
        iter_html=loop_html(thefile)        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'sip','page':'batchinput'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {})
        html = html + iter_html
        html = html + template.render(templatepath + 'sip-batchoutput-jqplot.html', {})                
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        #html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', SIPBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

