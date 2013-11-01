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
import cStringIO
import logging
import sys
sys.path.append("../terrplant")
from terrplant import terrplant_model,terrplant_tables
from uber import uber_lib
import csv
import numpy

A=[]
I=[]
R=[]
D=[]
nms=[]
lms=[]
nds=[]
lds=[]

######Pre-defined outputs########
rundry_out = []
runsemi_out = []
spray_out = []
totaldry_out = []
totalsemi_out = []
nmsRQdry_out = []
LOCnmsdry_out = []
nmsRQsemi_out = []
LOCnmssemi_out = []
nmsRQspray_out = []
LOCnmsspray_out = []
lmsRQdry_out = []
LOClmsdry_out = []
lmsRQsemi_out = []
LOClmssemi_out = []
lmsRQspray_out = []
LOClmsspray_out = []
ndsRQdry_out = []
LOCndsdry_out = []
ndsRQsemi_out = []
LOCndssemi_out = []
ndsRQspray_out = []
LOCndsspray_out = []
ldsRQdry_out = []
LOCldsdry_out = []
ldsRQsemi_out = []
LOCldssemi_out = []
ldsRQspray_out = []
LOCldsspray_out = []

logger = logging.getLogger("TerrPlantBatchOutput")

def html_table(row_inp,iter):
    A_temp=float(row_inp[0])
    A.append(A_temp)
    I_temp=float(row_inp[1])
    I.append(I_temp)
    R_temp=float(row_inp[2])
    R.append(R_temp)
    D_temp=float(row_inp[3])
    D.append(D_temp)
    nms_temp=float(row_inp[4])
    nms.append(nms_temp)
    lms_temp=float(row_inp[5])        
    lms.append(lms_temp)
    nds_temp=float(row_inp[6])   
    nds.append(nds_temp)
    lds_temp=float(row_inp[7])
    lds.append(lds_temp)
    terr = terrplant_model.terrplant(True,True,A_temp,I_temp,R_temp,D_temp,nms_temp,lms_temp,nds_temp,lds_temp)
    rundry_temp=terr.rundry_results
    rundry_out.append(rundry_temp)
    runsemi_temp=terr.runsemi_results
    runsemi_out.append(runsemi_temp)
    spray_temp=terr.spray_results
    spray_out.append(spray_temp)
    totaldry_temp=terr.totaldry_results
    totaldry_out.append(totaldry_temp)
    totalsemi_temp=terr.totalsemi_results
    totalsemi_out.append(totalsemi_temp)
    nmsRQdry_temp=terr.nmsRQdry_results
    nmsRQdry_out.append(nmsRQdry_temp)
    LOCnmsdry_temp=terr.LOCnmsdry_results
    LOCnmsdry_out.append(LOCnmsdry_temp)
    nmsRQsemi_temp=terr.nmsRQsemi_results
    nmsRQsemi_out.append(nmsRQsemi_temp)
    LOCnmssemi_temp=terr.LOCnmssemi_results
    LOCnmssemi_out.append(LOCnmssemi_temp)
    nmsRQspray_temp=terr.nmsRQspray_results
    nmsRQspray_out.append(nmsRQspray_temp)
    LOCnmsspray_temp=terr.LOCnmsspray_results
    LOCnmsspray_out.append(LOCnmsspray_temp)
    lmsRQdry_temp=terr.lmsRQdry_results
    lmsRQdry_out.append(lmsRQdry_temp)
    LOClmsdry_temp=terr.LOClmsdry_results
    LOClmsdry_out.append(LOClmsdry_temp)
    lmsRQsemi_temp=terr.lmsRQsemi_results
    lmsRQsemi_out.append(lmsRQsemi_temp)
    LOClmssemi_temp=terr.LOClmssemi_results
    LOClmssemi_out.append(LOClmssemi_temp)
    lmsRQspray_temp=terr.lmsRQspray_results
    lmsRQspray_out.append(lmsRQspray_temp)
    LOClmsspray_temp=terr.LOClmsspray_results
    LOClmsspray_out.append(LOClmsspray_temp)
    ndsRQdry_temp=terr.ndsRQdry_results
    ndsRQdry_out.append(ndsRQdry_temp)
    LOCndsdry_temp=terr.LOCndsdry_results
    LOCndsdry_out.append(LOCndsdry_temp)
    ndsRQsemi_temp=terr.ndsRQsemi_results
    ndsRQsemi_out.append(ndsRQsemi_temp)
    LOCndssemi_temp=terr.LOCndssemi_results
    LOCndssemi_out.append(LOCndssemi_temp)
    ndsRQspray_temp=terr.ndsRQspray_results
    ndsRQspray_out.append(ndsRQspray_temp)
    LOCndsspray_temp=terr.LOCndsspray_results
    LOCndsspray_out.append(LOCndsspray_temp)
    ldsRQdry_temp=terr.ldsRQdry_results
    ldsRQdry_out.append(ldsRQdry_temp)
    LOCldsdry_temp=terr.LOCldsdry_results
    LOCldsdry_out.append(LOCldsdry_temp)
    ldsRQsemi_temp=terr.ldsRQsemi_results
    ldsRQsemi_out.append(ldsRQsemi_temp)
    LOCldssemi_temp=terr.LOCldssemi_results
    LOCldssemi_out.append(LOCldssemi_temp)
    ldsRQspray_temp=terr.ldsRQspray_results
    ldsRQspray_out.append(ldsRQspray_temp)
    LOCldsspray_temp=terr.LOCldsspray_results
    LOCldsspray_out.append(LOCldsspray_temp)

    html = terrplant_tables.table_all(terrplant_tables.pvheadings, terrplant_tables.pvuheadings,terrplant_tables.deheadings,
                                        terrplant_tables.plantec25noaecheadings,terrplant_tables.plantecdrysemisprayheadings, 
                                        terrplant_tables.sumheadings, terrplant_tables.tmpl, terr)
    
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

    sum_html = terrplant_tables.table_all_sum(terrplant_tables.sumheadings, terrplant_tables.tmpl, A, I, R, D, nms, lms, nds, lds, 
                    rundry_out, runsemi_out, spray_out, totaldry_out, totalsemi_out, 
                    nmsRQdry_out, nmsRQsemi_out, nmsRQspray_out, 
                    lmsRQdry_out, lmsRQsemi_out, lmsRQspray_out, 
                    ndsRQdry_out, ndsRQsemi_out, ndsRQspray_out, 
                    ldsRQdry_out, ldsRQsemi_out, ldsRQspray_out)

    return sum_html+iter_html



              
class TerrPlantBatchOutputPage(webapp.RequestHandler):
    def post(self):
        text_file1 = open('terrplant/terrplant_description.txt','r')
        x = text_file1.read()
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['upfile']
        iter_html=loop_html(thefile)        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie)
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'terrplant','page':'batchinput'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {
                'model':'terrplant',
                'model_attributes':'TerrPlant Batch Output'})
        html = html + terrplant_tables.timestamp()
        html = html + iter_html
        # html = html + template.render(templatepath + 'terrplant-batchoutput-jqplot.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TerrPlantBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

