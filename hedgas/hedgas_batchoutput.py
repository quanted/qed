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
from hedgas import hedgas_model,hedgas_tables
import logging

logger = logging.getLogger('hedgasBatchPage')

run_acuteNonOcc=[]
mw_acuteNonOcc=[]
noael_acuteNonOcc=[]
noaelunit_acuteNonOcc=[]
hrs_animal_acuteNonOcc=[]
hrs_human_acuteNonOcc=[]
dow_animal_acuteNonOcc=[]
dow_human_acuteNonOcc=[]
b0_acuteNonOcc=[]
b1_acuteNonOcc=[]
SAa_acuteNonOcc=[]
tb_acuteNonOcc=[]
pu_acuteNonOcc=[]
run_stitNonOcc=[]
mw_stitNonOcc=[]
noael_stitNonOcc=[]
noaelunit_stitNonOcc=[]
hrs_animal_stitNonOcc=[]
hrs_human_stitNonOcc=[]
BWa_stitNonOcc=[]
dow_animal_stitNonOcc=[]
dow_human_stitNonOcc=[]
b0_stitNonOcc=[]
b1_stitNonOcc=[]
SAa_stitNonOcc=[]
tb_stitNonOcc=[]
pu_stitNonOcc=[]
run_ltNonOcc=[]
mw_ltNonOcc=[]
noael_ltNonOcc=[]
noaelunit_ltNonOcc=[]
hrs_animal_ltNonOcc=[]
hrs_human_ltNonOcc=[]
BWa_ltNonOcc=[]
dow_animal_ltNonOcc=[]
dow_human_ltNonOcc=[]
b0_ltNonOcc=[]
b1_ltNonOcc=[]
SAa_ltNonOcc=[]
tb_ltNonOcc=[]
pu_ltNonOcc=[]
run_acuteOcc=[]
mw_acuteOcc=[]
noael_acuteOcc=[]
noaelunit_acuteOcc=[]
hrs_animal_acuteOcc=[]
hrs_human_acuteOcc=[]
BWa_acuteOcc=[]
dow_animal_acuteOcc=[]
dow_human_acuteOcc=[]
b0_acuteOcc=[]
b1_acuteOcc=[]
SAa_acuteOcc=[]
tb_acuteOcc=[]
pu_acuteOcc=[]
run_stitOcc=[]
mw_stitOcc=[]
noael_stitOcc=[]
noaelunit_stitOcc=[]
hrs_animal_stitOcc=[]
hrs_human_stitOcc=[]
BWa_stitOcc=[]
dow_animal_stitOcc=[]
dow_human_stitOcc=[]
b0_stitOcc=[]
b1_stitOcc=[]
SAa_stitOcc=[]
tb_stitOcc=[]
pu_stitOcc=[]
run_ltOcc=[]
mw_ltOcc=[]
noael_ltOcc=[]
noaelunit_ltOcc=[]
hrs_animal_ltOcc=[]
hrs_human_ltOcc=[]
BWa_ltOcc=[]
dow_animal_ltOcc=[]
dow_human_ltOcc=[]
b0_ltOcc=[]
b1_ltOcc=[]
SAa_ltOcc=[]
tb_ltOcc=[]
pu_ltOcc=[]

######Pre-defined outputs########
noael_adj_acuteNonOccET=[]
mv_a_acuteNonOccET=[]
rgdr_acuteNonOccET=[]
hec_acuteNonOccET=[]
hec_acuteNonOccET_ppm=[]
rgdr_acuteNonOccTB=[]
hec_acuteNonOccTB=[]
hec_acuteNonOccTB_ppm=[]
rgdr_acuteNonOccPU=[]
hec_acuteNonOccPU=[]
hec_acuteNonOccPU_ppm=[]
hec_acuteNonOccSYS=[]
hec_acuteNonOccSYS_ppm=[]
noael_adj_stitNonOccET=[]
mv_a_stitNonOccET=[]
rgdr_stitNonOccET=[]
hec_stitNonOccET=[]
hec_stitNonOccET_ppm=[]
rgdr_stitNonOccTB=[]
hec_stitNonOccTB=[]
hec_stitNonOccTB_ppm=[]
rgdr_stitNonOccPU=[]
hec_stitNonOccPU=[]
hec_stitNonOccPU_ppm=[]
hec_stitNonOccSYS=[]
hec_stitNonOccSYS_ppm=[]
noael_adj_ltNonOccET=[]
mv_a_ltNonOccET=[]
rgdr_ltNonOccET=[]
hec_ltNonOccET=[]
hec_ltNonOccET_ppm=[]
rgdr_ltNonOccTB=[]
hec_ltNonOccTB=[]
hec_ltNonOccTB_ppm=[]
rgdr_ltNonOccPU=[]
hec_ltNonOccPU=[]
hec_ltNonOccPU_ppm=[]
hec_ltNonOccSYS=[]
hec_ltNonOccSYS_ppm=[]
noael_adj_acuteOccET=[]
mv_a_acuteOccET=[]
rgdr_acuteOccET=[]
hec_acuteOccET=[]
hec_acuteOccET_ppm=[]
rgdr_acuteOccTB=[]
hec_acuteOccTB=[]
hec_acuteOccTB_ppm=[]
rgdr_acuteOccPU=[]
hec_acuteOccPU=[]
hec_acuteOccPU_ppm=[]
hec_acuteOccSYS=[]
hec_acuteOccSYS_ppm=[]
noael_adj_stitOccET=[]
mv_a_stitOccET=[]
rgdr_stitOccET=[]
hec_stitOccET=[]
hec_stitOccET_ppm=[]
rgdr_stitOccTB=[]
hec_stitOccTB=[]
hec_stitOccTB_ppm=[]
rgdr_stitOccPU=[]
hec_stitOccPU=[]
hec_stitOccPU_ppm=[]
hec_stitOccSYS=[]
hec_stitOccSYS_ppm=[]
noael_adj_ltOccET=[]
mv_a_ltOccET=[]
rgdr_ltOccET=[]
hec_ltOccET=[]
hec_ltOccET_ppm=[]
rgdr_ltOccTB=[]
hec_ltOccTB=[]
hec_ltOccTB_ppm=[]
rgdr_ltOccPU=[]
hec_ltOccPU=[]
hec_ltOccPU_ppm=[]
hec_ltOccSYS=[]
hec_ltOccSYS_ppm=[]


logger = logging.getLogger("hedgasBatchOutput")

def html_table(row_inp,iter):
    logger.info("iteration: " + str(iter))
    run_acuteNonOcc.append(str(row_inp[0]))
    mw_acuteNonOcc.append(float(row_inp[1]))
    noael_acuteNonOcc.append(float(row_inp[2]))
    noaelunit_acuteNonOcc.append(float(row_inp[3]))
    if noaelunit_acuteNonOcc == [0]:
        noaelunit_acuteNonOccTemp = noael_acuteNonOcc[0] * (mw_acuteNonOcc[0] / 24.45)
        noael_acuteNonOcc.insert(0, noaelunit_acuteNonOccTemp)
    hrs_animal_acuteNonOcc.append(float(row_inp[4]))
    hrs_human_acuteNonOcc.append(float(row_inp[5]))
    dow_animal_acuteNonOcc.append(float(row_inp[6]))
    dow_human_acuteNonOcc.append(float(row_inp[7]))
    b0_acuteNonOcc.append(float(row_inp[8]))
    b1_acuteNonOcc.append(float(row_inp[9]))
    SAa_acuteNonOcc.append(float(row_inp[10]))
    tb_acuteNonOcc.append(float(row_inp[11]))
    pu_acuteNonOcc.append(float(row_inp[12]))
    run_stitNonOcc.append(str(row_inp[13]))
    mw_stitNonOcc.append(float(row_inp[14]))
    noael_stitNonOcc.append(float(row_inp[15]))
    noaelunit_stitNonOcc.append(float(row_inp[16]))
    if noaelunit_stitNonOcc == [0]:
        noaelunit_stitNonOccTemp = noael_stitNonOcc[0] * (mw_stitNonOcc[0] / 24.45)
        noael_stitNonOcc.insert(0, noaelunit_stitNonOccTemp)
    hrs_animal_stitNonOcc.append(float(row_inp[17]))
    hrs_human_stitNonOcc.append(float(row_inp[18]))
    BWa_stitNonOcc.append(float(row_inp[19]))
    dow_animal_stitNonOcc.append(float(row_inp[20]))
    dow_human_stitNonOcc.append(float(row_inp[21]))
    b0_stitNonOcc.append(float(row_inp[22]))
    b1_stitNonOcc.append(float(row_inp[23]))
    SAa_stitNonOcc.append(float(row_inp[24]))
    tb_stitNonOcc.append(float(row_inp[25]))
    pu_stitNonOcc.append(float(row_inp[26]))
    run_ltNonOcc.append(str(row_inp[27]))
    mw_ltNonOcc.append(float(row_inp[28]))
    noael_ltNonOcc.append(float(row_inp[29]))
    noaelunit_ltNonOcc.append(float(row_inp[30]))
    if noaelunit_ltNonOcc == [0]:
        noaelunit_ltNonOccTemp = noael_ltNonOcc[0] * (mw_ltNonOcc[0] / 24.45)
        noael_ltNonOcc.insert(0, noaelunit_ltNonOccTemp)
    hrs_animal_ltNonOcc.append(float(row_inp[31]))
    hrs_human_ltNonOcc.append(float(row_inp[32]))
    BWa_ltNonOcc.append(float(row_inp[33]))
    dow_animal_ltNonOcc.append(float(row_inp[34]))
    dow_human_ltNonOcc.append(float(row_inp[35]))
    b0_ltNonOcc.append(float(row_inp[36]))
    b1_ltNonOcc.append(float(row_inp[37]))
    SAa_ltNonOcc.append(float(row_inp[38]))
    tb_ltNonOcc.append(float(row_inp[39]))
    pu_ltNonOcc.append(float(row_inp[40]))
    run_acuteOcc.append(str(row_inp[41]))
    mw_acuteOcc.append(float(row_inp[42]))
    noael_acuteOcc.append(float(row_inp[43]))
    noaelunit_acuteOcc.append(float(row_inp[44]))
    if noaelunit_acuteOcc == [0]:
        noaelunit_acuteOccTemp = noael_acuteOcc[0] * (mw_acuteOcc[0] / 24.45)
        noael_acuteOcc.insert(0, noaelunit_acuteOccTemp)
    hrs_animal_acuteOcc.append(float(row_inp[45]))
    hrs_human_acuteOcc.append(float(row_inp[46]))
    BWa_acuteOcc.append(float(row_inp[47]))
    dow_animal_acuteOcc.append(float(row_inp[48]))
    dow_human_acuteOcc.append(float(row_inp[49]))
    b0_acuteOcc.append(float(row_inp[50]))
    b1_acuteOcc.append(float(row_inp[51]))
    SAa_acuteOcc.append(float(row_inp[52]))
    tb_acuteOcc.append(float(row_inp[53]))
    pu_acuteOcc.append(float(row_inp[54]))
    run_stitOcc.append(str(row_inp[55]))
    mw_stitOcc.append(float(row_inp[56]))
    noael_stitOcc.append(float(row_inp[57]))
    noaelunit_stitOcc.append(float(row_inp[58]))
    if noaelunit_stitOcc == [0]:
        noaelunit_stitOccTemp = noael_stitOcc[0] * (mw_stitOcc[0] / 24.45)
        noael_stitOcc.insert(0, noaelunit_stitOccTemp)
    hrs_animal_stitOcc.append(float(row_inp[59]))
    hrs_human_stitOcc.append(float(row_inp[60]))
    BWa_stitOcc.append(float(row_inp[61]))
    dow_animal_stitOcc.append(float(row_inp[62]))
    dow_human_stitOcc.append(float(row_inp[63]))
    b0_stitOcc.append(float(row_inp[64]))
    b1_stitOcc.append(float(row_inp[65]))
    SAa_stitOcc.append(float(row_inp[66]))
    tb_stitOcc.append(float(row_inp[67]))
    pu_stitOcc.append(float(row_inp[68]))
    run_ltOcc.append(str(row_inp[69]))
    mw_ltOcc.append(float(row_inp[70]))
    noael_ltOcc.append(float(row_inp[71]))
    noaelunit_ltOcc.append(float(row_inp[72]))
    if noaelunit_ltOcc == [0]:
        noaelunit_ltOccTemp = noael_ltOcc[0] * (mw_ltOcc[0] / 24.45)
        noael_ltOcc.insert(0, noaelunit_ltOccTemp)
    hrs_animal_ltOcc.append(float(row_inp[73]))
    hrs_human_ltOcc.append(float(row_inp[74]))
    BWa_ltOcc.append(float(row_inp[75]))
    dow_animal_ltOcc.append(float(row_inp[76]))
    dow_human_ltOcc.append(float(row_inp[77]))
    b0_ltOcc.append(float(row_inp[78]))
    b1_ltOcc.append(float(row_inp[79]))
    SAa_ltOcc.append(float(row_inp[80]))
    tb_ltOcc.append(float(row_inp[81]))
    pu_ltOcc.append(float(row_inp[82]))


    hedgas_obj = hedgas_model.hedgas(True,True,run_acuteNonOcc[iter],mw_acuteNonOcc[iter],noael_acuteNonOcc[iter],hrs_animal_acuteNonOcc[iter],hrs_human_acuteNonOcc[iter],dow_animal_acuteNonOcc[iter],dow_human_acuteNonOcc[iter],b0_acuteNonOcc[iter],b1_acuteNonOcc[iter],SAa_acuteNonOcc[iter],tb_acuteNonOcc[iter],pu_acuteNonOcc[iter],run_stitNonOcc[iter],mw_stitNonOcc[iter],noael_stitNonOcc[iter],hrs_animal_stitNonOcc[iter],hrs_human_stitNonOcc[iter],BWa_stitNonOcc[iter],dow_animal_stitNonOcc[iter],dow_human_stitNonOcc[iter],b0_stitNonOcc[iter],b1_stitNonOcc[iter],SAa_stitNonOcc[iter],tb_stitNonOcc[iter],pu_stitNonOcc[iter],run_ltNonOcc[iter],mw_ltNonOcc[iter],noael_ltNonOcc[iter],hrs_animal_ltNonOcc[iter],hrs_human_ltNonOcc[iter],BWa_ltNonOcc[iter],dow_animal_ltNonOcc[iter],dow_human_ltNonOcc[iter],b0_ltNonOcc[iter],b1_ltNonOcc[iter],SAa_ltNonOcc[iter],tb_ltNonOcc[iter],pu_ltNonOcc[iter],run_acuteOcc[iter],mw_acuteOcc[iter],noael_acuteOcc[iter],hrs_animal_acuteOcc[iter],hrs_human_acuteOcc[iter],BWa_acuteOcc[iter],dow_animal_acuteOcc[iter],dow_human_acuteOcc[iter],b0_acuteOcc[iter],b1_acuteOcc[iter],SAa_acuteOcc[iter],tb_acuteOcc[iter],pu_acuteOcc[iter],run_stitOcc[iter],mw_stitOcc[iter],noael_stitOcc[iter],hrs_animal_stitOcc[iter],hrs_human_stitOcc[iter],BWa_stitOcc[iter],dow_animal_stitOcc[iter],dow_human_stitOcc[iter],b0_stitOcc[iter],b1_stitOcc[iter],SAa_stitOcc[iter],tb_stitOcc[iter],pu_stitOcc[iter],run_ltOcc[iter],mw_ltOcc[iter],noael_ltOcc[iter],hrs_animal_ltOcc[iter],hrs_human_ltOcc[iter],BWa_ltOcc[iter],dow_animal_ltOcc[iter],dow_human_ltOcc[iter],b0_ltOcc[iter],b1_ltOcc[iter],SAa_ltOcc[iter],tb_ltOcc[iter],pu_ltOcc[iter])

    noael_adj_acuteNonOccET.append(hedgas_obj.noael_adj_acuteNonOccET)
    mv_a_acuteNonOccET.append(hedgas_obj.mv_a_acuteNonOccET)
    rgdr_acuteNonOccET.append(hedgas_obj.rgdr_acuteNonOccET)
    hec_acuteNonOccET.append(hedgas_obj.hec_acuteNonOccET)
    hec_acuteNonOccET_ppm.append(hedgas_obj.hec_acuteNonOccET_ppm)
    rgdr_acuteNonOccTB.append(hedgas_obj.rgdr_acuteNonOccTB)
    hec_acuteNonOccTB.append(hedgas_obj.hec_acuteNonOccTB)
    hec_acuteNonOccTB_ppm.append(hedgas_obj.hec_acuteNonOccTB_ppm)
    rgdr_acuteNonOccPU.append(hedgas_obj.rgdr_acuteNonOccPU)
    hec_acuteNonOccPU.append(hedgas_obj.hec_acuteNonOccPU)
    hec_acuteNonOccPU_ppm.append(hedgas_obj.hec_acuteNonOccPU_ppm)
    hec_acuteNonOccSYS.append(hedgas_obj.hec_acuteNonOccSYS)
    hec_acuteNonOccSYS_ppm.append(hedgas_obj.hec_acuteNonOccSYS_ppm)
    noael_adj_stitNonOccET.append(hedgas_obj.noael_adj_stitNonOccET)
    mv_a_stitNonOccET.append(hedgas_obj.mv_a_stitNonOccET)
    rgdr_stitNonOccET.append(hedgas_obj.rgdr_stitNonOccET)
    hec_stitNonOccET.append(hedgas_obj.hec_stitNonOccET)
    hec_stitNonOccET_ppm.append(hedgas_obj.hec_stitNonOccET_ppm)
    rgdr_stitNonOccTB.append(hedgas_obj.rgdr_stitNonOccTB)
    hec_stitNonOccTB.append(hedgas_obj.hec_stitNonOccTB)
    hec_stitNonOccTB_ppm.append(hedgas_obj.hec_stitNonOccTB_ppm)
    rgdr_stitNonOccPU.append(hedgas_obj.rgdr_stitNonOccPU)
    hec_stitNonOccPU.append(hedgas_obj.hec_stitNonOccPU)
    hec_stitNonOccPU_ppm.append(hedgas_obj.hec_stitNonOccPU_ppm)
    hec_stitNonOccSYS.append(hedgas_obj.hec_stitNonOccSYS)
    hec_stitNonOccSYS_ppm.append(hedgas_obj.hec_stitNonOccSYS_ppm)
    noael_adj_ltNonOccET.append(hedgas_obj.noael_adj_ltNonOccET)
    mv_a_ltNonOccET.append(hedgas_obj.mv_a_ltNonOccET)
    rgdr_ltNonOccET.append(hedgas_obj.rgdr_ltNonOccET)
    hec_ltNonOccET.append(hedgas_obj.hec_ltNonOccET)
    hec_ltNonOccET_ppm.append(hedgas_obj.hec_ltNonOccET_ppm)
    rgdr_ltNonOccTB.append(hedgas_obj.rgdr_ltNonOccTB)
    hec_ltNonOccTB.append(hedgas_obj.hec_ltNonOccTB)
    hec_ltNonOccTB_ppm.append(hedgas_obj.hec_ltNonOccTB_ppm)
    rgdr_ltNonOccPU.append(hedgas_obj.rgdr_ltNonOccPU)
    hec_ltNonOccPU.append(hedgas_obj.hec_ltNonOccPU)
    hec_ltNonOccPU_ppm.append(hedgas_obj.hec_ltNonOccPU_ppm)
    hec_ltNonOccSYS.append(hedgas_obj.hec_ltNonOccSYS)
    hec_ltNonOccSYS_ppm.append(hedgas_obj.hec_ltNonOccSYS_ppm)
    noael_adj_acuteOccET.append(hedgas_obj.noael_adj_acuteOccET)
    mv_a_acuteOccET.append(hedgas_obj.mv_a_acuteOccET)
    rgdr_acuteOccET.append(hedgas_obj.rgdr_acuteOccET)
    hec_acuteOccET.append(hedgas_obj.hec_acuteOccET)
    hec_acuteOccET_ppm.append(hedgas_obj.hec_acuteOccET_ppm)
    rgdr_acuteOccTB.append(hedgas_obj.rgdr_acuteOccTB)
    hec_acuteOccTB.append(hedgas_obj.hec_acuteOccTB)
    hec_acuteOccTB_ppm.append(hedgas_obj.hec_acuteOccTB_ppm)
    rgdr_acuteOccPU.append(hedgas_obj.rgdr_acuteOccPU)
    hec_acuteOccPU.append(hedgas_obj.hec_acuteOccPU)
    hec_acuteOccPU_ppm.append(hedgas_obj.hec_acuteOccPU_ppm)
    hec_acuteOccSYS.append(hedgas_obj.hec_acuteOccSYS)
    hec_acuteOccSYS_ppm.append(hedgas_obj.hec_acuteOccSYS_ppm)
    noael_adj_stitOccET.append(hedgas_obj.noael_adj_stitOccET)
    mv_a_stitOccET.append(hedgas_obj.mv_a_stitOccET)
    rgdr_stitOccET.append(hedgas_obj.rgdr_stitOccET)
    hec_stitOccET.append(hedgas_obj.hec_stitOccET)
    hec_stitOccET_ppm.append(hedgas_obj.hec_stitOccET_ppm)
    rgdr_stitOccTB.append(hedgas_obj.rgdr_stitOccTB)
    hec_stitOccTB.append(hedgas_obj.hec_stitOccTB)
    hec_stitOccTB_ppm.append(hedgas_obj.hec_stitOccTB_ppm)
    rgdr_stitOccPU.append(hedgas_obj.rgdr_stitOccPU)
    hec_stitOccPU.append(hedgas_obj.hec_stitOccPU)
    hec_stitOccPU_ppm.append(hedgas_obj.hec_stitOccPU_ppm)
    hec_stitOccSYS.append(hedgas_obj.hec_stitOccSYS)
    hec_stitOccSYS_ppm.append(hedgas_obj.hec_stitOccSYS_ppm)
    noael_adj_ltOccET.append(hedgas_obj.noael_adj_ltOccET)
    mv_a_ltOccET.append(hedgas_obj.mv_a_ltOccET)
    rgdr_ltOccET.append(hedgas_obj.rgdr_ltOccET)
    hec_ltOccET.append(hedgas_obj.hec_ltOccET)
    hec_ltOccET_ppm.append(hedgas_obj.hec_ltOccET_ppm)
    rgdr_ltOccTB.append(hedgas_obj.rgdr_ltOccTB)
    hec_ltOccTB.append(hedgas_obj.hec_ltOccTB)
    hec_ltOccTB_ppm.append(hedgas_obj.hec_ltOccTB_ppm)
    rgdr_ltOccPU.append(hedgas_obj.rgdr_ltOccPU)
    hec_ltOccPU.append(hedgas_obj.hec_ltOccPU)
    hec_ltOccPU_ppm.append(hedgas_obj.hec_ltOccPU_ppm)
    hec_ltOccSYS.append(hedgas_obj.hec_ltOccSYS)
    hec_ltOccSYS_ppm.append(hedgas_obj.hec_ltOccSYS_ppm)


    batch_header = """
        <div class="out_">
            <br><H3>Batch Calculation of Iteration %s:</H3>
        </div>
        """%(iter + 1)

    html = batch_header + hedgas_tables.table_all(hedgas_obj)
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

    return iter_html

              
class hedgasBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['upfile']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', 'title')
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'hedgas','page':'batchinput'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {
                'model':'hedgas',
                'model_attributes':'HED Gas Calculator Batch Output'})
        html = html + hedgas_tables.timestamp()
        html = html + iter_html
        # html = html + template.render(templatepath + 'hedgas-batchoutput-jqplot.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', hedgasBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

