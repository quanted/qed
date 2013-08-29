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
# from iec import iec_output
from pprint import pprint
import csv
from hedgas import hedgas_model,hedgas_tables

cwd=os.getcwd()
data=csv.reader(open(cwd+'/hedgas/hedgas_qaqc.csv'))
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


data.next()
for row in data:
    run_acuteNonOcc.append(str(row[0]))
    mw_acuteNonOcc.append(float(row[1]))
    noael_acuteNonOcc.append(float(row[2]))
    noaelunit_acuteNonOcc.append(float(row[3]))
    if noaelunit_acuteNonOcc == [0]:
        noaelunit_acuteNonOccTemp = noael_acuteNonOcc[0] * (mw_acuteNonOcc[0] / 24.45)
        noael_acuteNonOcc.insert(0, noaelunit_acuteNonOccTemp)
    hrs_animal_acuteNonOcc.append(float(row[4]))
    hrs_human_acuteNonOcc.append(float(row[5]))
    dow_animal_acuteNonOcc.append(float(row[6]))
    dow_human_acuteNonOcc.append(float(row[7]))
    b0_acuteNonOcc.append(float(row[8]))
    b1_acuteNonOcc.append(float(row[9]))
    SAa_acuteNonOcc.append(float(row[10]))
    tb_acuteNonOcc.append(float(row[11]))
    pu_acuteNonOcc.append(float(row[12]))
    run_stitNonOcc.append(str(row[13]))
    mw_stitNonOcc.append(float(row[14]))
    noael_stitNonOcc.append(float(row[15]))
    noaelunit_stitNonOcc.append(float(row[16]))
    if noaelunit_stitNonOcc == [0]:
        noaelunit_stitNonOccTemp = noael_stitNonOcc[0] * (mw_stitNonOcc[0] / 24.45)
        noael_stitNonOcc.insert(0, noaelunit_stitNonOccTemp)
    hrs_animal_stitNonOcc.append(float(row[17]))
    hrs_human_stitNonOcc.append(float(row[18]))
    BWa_stitNonOcc.append(float(row[19]))
    dow_animal_stitNonOcc.append(float(row[20]))
    dow_human_stitNonOcc.append(float(row[21]))
    b0_stitNonOcc.append(float(row[22]))
    b1_stitNonOcc.append(float(row[23]))
    SAa_stitNonOcc.append(float(row[24]))
    tb_stitNonOcc.append(float(row[25]))
    pu_stitNonOcc.append(float(row[26]))
    run_ltNonOcc.append(str(row[27]))
    mw_ltNonOcc.append(float(row[28]))
    noael_ltNonOcc.append(float(row[29]))
    noaelunit_ltNonOcc.append(float(row[30]))
    if noaelunit_ltNonOcc == [0]:
        noaelunit_ltNonOccTemp = noael_ltNonOcc[0] * (mw_ltNonOcc[0] / 24.45)
        noael_ltNonOcc.insert(0, noaelunit_ltNonOccTemp)
    hrs_animal_ltNonOcc.append(float(row[31]))
    hrs_human_ltNonOcc.append(float(row[32]))
    BWa_ltNonOcc.append(float(row[33]))
    dow_animal_ltNonOcc.append(float(row[34]))
    dow_human_ltNonOcc.append(float(row[35]))
    b0_ltNonOcc.append(float(row[36]))
    b1_ltNonOcc.append(float(row[37]))
    SAa_ltNonOcc.append(float(row[38]))
    tb_ltNonOcc.append(float(row[39]))
    pu_ltNonOcc.append(float(row[40]))
    run_acuteOcc.append(str(row[41]))
    mw_acuteOcc.append(float(row[42]))
    noael_acuteOcc.append(float(row[43]))
    noaelunit_acuteOcc.append(float(row[44]))
    if noaelunit_acuteOcc == [0]:
        noaelunit_acuteOccTemp = noael_acuteOcc[0] * (mw_acuteOcc[0] / 24.45)
        noael_acuteOcc.insert(0, noaelunit_acuteOccTemp)
    hrs_animal_acuteOcc.append(float(row[45]))
    hrs_human_acuteOcc.append(float(row[46]))
    BWa_acuteOcc.append(float(row[47]))
    dow_animal_acuteOcc.append(float(row[48]))
    dow_human_acuteOcc.append(float(row[49]))
    b0_acuteOcc.append(float(row[50]))
    b1_acuteOcc.append(float(row[51]))
    SAa_acuteOcc.append(float(row[52]))
    tb_acuteOcc.append(float(row[53]))
    pu_acuteOcc.append(float(row[54]))
    run_stitOcc.append(str(row[55]))
    mw_stitOcc.append(float(row[56]))
    noael_stitOcc.append(float(row[57]))
    noaelunit_stitOcc.append(float(row[58]))
    if noaelunit_stitOcc == [0]:
        noaelunit_stitOccTemp = noael_stitOcc[0] * (mw_stitOcc[0] / 24.45)
        noael_stitOcc.insert(0, noaelunit_stitOccTemp)
    hrs_animal_stitOcc.append(float(row[59]))
    hrs_human_stitOcc.append(float(row[60]))
    BWa_stitOcc.append(float(row[61]))
    dow_animal_stitOcc.append(float(row[62]))
    dow_human_stitOcc.append(float(row[63]))
    b0_stitOcc.append(float(row[64]))
    b1_stitOcc.append(float(row[65]))
    SAa_stitOcc.append(float(row[66]))
    tb_stitOcc.append(float(row[67]))
    pu_stitOcc.append(float(row[68]))
    run_ltOcc.append(str(row[69]))
    mw_ltOcc.append(float(row[70]))
    noael_ltOcc.append(float(row[71]))
    noaelunit_ltOcc.append(float(row[72]))
    if noaelunit_ltOcc == [0]:
        noaelunit_ltOccTemp = noael_ltOcc[0] * (mw_ltOcc[0] / 24.45)
        noael_ltOcc.insert(0, noaelunit_ltOccTemp)
    hrs_animal_ltOcc.append(float(row[73]))
    hrs_human_ltOcc.append(float(row[74]))
    BWa_ltOcc.append(float(row[75]))
    dow_animal_ltOcc.append(float(row[76]))
    dow_human_ltOcc.append(float(row[77]))
    b0_ltOcc.append(float(row[78]))
    b1_ltOcc.append(float(row[79]))
    SAa_ltOcc.append(float(row[80]))
    tb_ltOcc.append(float(row[81]))
    pu_ltOcc.append(float(row[82]))
    noael_adj_acuteNonOccET.append(float(row[83]))
    mv_a_acuteNonOccET.append(float(row[84]))
    rgdr_acuteNonOccET.append(float(row[85]))
    hec_acuteNonOccET.append(float(row[86]))
    hec_acuteNonOccET_ppm.append(float(row[87]))
    rgdr_acuteNonOccTB.append(float(row[88]))
    hec_acuteNonOccTB.append(float(row[89]))
    hec_acuteNonOccTB_ppm.append(float(row[90]))
    rgdr_acuteNonOccPU.append(float(row[91]))
    hec_acuteNonOccPU.append(float(row[92]))
    hec_acuteNonOccPU_ppm.append(float(row[93]))
    hec_acuteNonOccSYS.append(float(row[94]))
    hec_acuteNonOccSYS_ppm.append(float(row[95]))
    noael_adj_stitNonOccET.append(float(row[96]))
    mv_a_stitNonOccET.append(float(row[97]))
    rgdr_stitNonOccET.append(float(row[98]))
    hec_stitNonOccET.append(float(row[99]))
    hec_stitNonOccET_ppm.append(float(row[100]))
    rgdr_stitNonOccTB.append(float(row[101]))
    hec_stitNonOccTB.append(float(row[102]))
    hec_stitNonOccTB_ppm.append(float(row[103]))
    rgdr_stitNonOccPU.append(float(row[104]))
    hec_stitNonOccPU.append(float(row[105]))
    hec_stitNonOccPU_ppm.append(float(row[106]))
    hec_stitNonOccSYS.append(float(row[107]))
    hec_stitNonOccSYS_ppm.append(float(row[108]))
    noael_adj_ltNonOccET.append(float(row[109]))
    mv_a_ltNonOccET.append(float(row[110]))
    rgdr_ltNonOccET.append(float(row[111]))
    hec_ltNonOccET.append(float(row[112]))
    hec_ltNonOccET_ppm.append(float(row[113]))
    rgdr_ltNonOccTB.append(float(row[114]))
    hec_ltNonOccTB.append(float(row[115]))
    hec_ltNonOccTB_ppm.append(float(row[116]))
    rgdr_ltNonOccPU.append(float(row[117]))
    hec_ltNonOccPU.append(float(row[118]))
    hec_ltNonOccPU_ppm.append(float(row[119]))
    hec_ltNonOccSYS.append(float(row[120]))
    hec_ltNonOccSYS_ppm.append(float(row[121]))
    noael_adj_acuteOccET.append(float(row[122]))
    mv_a_acuteOccET.append(float(row[123]))
    rgdr_acuteOccET.append(float(row[124]))
    hec_acuteOccET.append(float(row[125]))
    hec_acuteOccET_ppm.append(float(row[126]))
    rgdr_acuteOccTB.append(float(row[127]))
    hec_acuteOccTB.append(float(row[128]))
    hec_acuteOccTB_ppm.append(float(row[129]))
    rgdr_acuteOccPU.append(float(row[130]))
    hec_acuteOccPU.append(float(row[131]))
    hec_acuteOccPU_ppm.append(float(row[132]))
    hec_acuteOccSYS.append(float(row[133]))
    hec_acuteOccSYS_ppm.append(float(row[134]))
    noael_adj_stitOccET.append(float(row[135]))
    mv_a_stitOccET.append(float(row[136]))
    rgdr_stitOccET.append(float(row[137]))
    hec_stitOccET.append(float(row[138]))
    hec_stitOccET_ppm.append(float(row[139]))
    rgdr_stitOccTB.append(float(row[140]))
    hec_stitOccTB.append(float(row[141]))
    hec_stitOccTB_ppm.append(float(row[142]))
    rgdr_stitOccPU.append(float(row[143]))
    hec_stitOccPU.append(float(row[144]))
    hec_stitOccPU_ppm.append(float(row[145]))
    hec_stitOccSYS.append(float(row[146]))
    hec_stitOccSYS_ppm.append(float(row[147]))
    noael_adj_ltOccET.append(float(row[148]))
    mv_a_ltOccET.append(float(row[149]))
    rgdr_ltOccET.append(float(row[150]))
    hec_ltOccET.append(float(row[151]))
    hec_ltOccET_ppm.append(float(row[152]))
    rgdr_ltOccTB.append(float(row[153]))
    hec_ltOccTB.append(float(row[154]))
    hec_ltOccTB_ppm.append(float(row[155]))
    rgdr_ltOccPU.append(float(row[156]))
    hec_ltOccPU.append(float(row[157]))
    hec_ltOccPU_ppm.append(float(row[158]))
    hec_ltOccSYS.append(float(row[159]))
    hec_ltOccSYS_ppm.append(float(row[160]))


hedgas_obj = hedgas_model.hedgas(True,True,run_acuteNonOcc[0],mw_acuteNonOcc[0],noael_acuteNonOcc[0],hrs_animal_acuteNonOcc[0],hrs_human_acuteNonOcc[0],dow_animal_acuteNonOcc[0],dow_human_acuteNonOcc[0],b0_acuteNonOcc[0],b1_acuteNonOcc[0],SAa_acuteNonOcc[0],tb_acuteNonOcc[0],pu_acuteNonOcc[0],run_stitNonOcc[0],mw_stitNonOcc[0],noael_stitNonOcc[0],hrs_animal_stitNonOcc[0],hrs_human_stitNonOcc[0],BWa_stitNonOcc[0],dow_animal_stitNonOcc[0],dow_human_stitNonOcc[0],b0_stitNonOcc[0],b1_stitNonOcc[0],SAa_stitNonOcc[0],tb_stitNonOcc[0],pu_stitNonOcc[0],run_ltNonOcc[0],mw_ltNonOcc[0],noael_ltNonOcc[0],hrs_animal_ltNonOcc[0],hrs_human_ltNonOcc[0],BWa_ltNonOcc[0],dow_animal_ltNonOcc[0],dow_human_ltNonOcc[0],b0_ltNonOcc[0],b1_ltNonOcc[0],SAa_ltNonOcc[0],tb_ltNonOcc[0],pu_ltNonOcc[0],run_acuteOcc[0],mw_acuteOcc[0],noael_acuteOcc[0],hrs_animal_acuteOcc[0],hrs_human_acuteOcc[0],BWa_acuteOcc[0],dow_animal_acuteOcc[0],dow_human_acuteOcc[0],b0_acuteOcc[0],b1_acuteOcc[0],SAa_acuteOcc[0],tb_acuteOcc[0],pu_acuteOcc[0],run_stitOcc[0],mw_stitOcc[0],noael_stitOcc[0],hrs_animal_stitOcc[0],hrs_human_stitOcc[0],BWa_stitOcc[0],dow_animal_stitOcc[0],dow_human_stitOcc[0],b0_stitOcc[0],b1_stitOcc[0],SAa_stitOcc[0],tb_stitOcc[0],pu_stitOcc[0],run_ltOcc[0],mw_ltOcc[0],noael_ltOcc[0],hrs_animal_ltOcc[0],hrs_human_ltOcc[0],BWa_ltOcc[0],dow_animal_ltOcc[0],dow_human_ltOcc[0],b0_ltOcc[0],b1_ltOcc[0],SAa_ltOcc[0],tb_ltOcc[0],pu_ltOcc[0])

hedgas_obj.noael_adj_acuteNonOccET_exp=noael_adj_acuteNonOccET[0]
hedgas_obj.mv_a_acuteNonOccET_exp=mv_a_acuteNonOccET[0]
hedgas_obj.rgdr_acuteNonOccET_exp=rgdr_acuteNonOccET[0]
hedgas_obj.hec_acuteNonOccET_exp=hec_acuteNonOccET[0]
hedgas_obj.hec_acuteNonOccET_ppm_exp=hec_acuteNonOccET_ppm[0]
hedgas_obj.rgdr_acuteNonOccTB_exp=rgdr_acuteNonOccTB[0]
hedgas_obj.hec_acuteNonOccTB_exp=hec_acuteNonOccTB[0]
hedgas_obj.hec_acuteNonOccTB_ppm_exp=hec_acuteNonOccTB_ppm[0]
hedgas_obj.rgdr_acuteNonOccPU_exp=rgdr_acuteNonOccPU[0]
hedgas_obj.hec_acuteNonOccPU_exp=hec_acuteNonOccPU[0]
hedgas_obj.hec_acuteNonOccPU_ppm_exp=hec_acuteNonOccPU_ppm[0]
hedgas_obj.hec_acuteNonOccSYS_exp=hec_acuteNonOccSYS[0]
hedgas_obj.hec_acuteNonOccSYS_ppm_exp=hec_acuteNonOccSYS_ppm[0]
hedgas_obj.noael_adj_stitNonOccET_exp=noael_adj_stitNonOccET[0]
hedgas_obj.mv_a_stitNonOccET_exp=mv_a_stitNonOccET[0]
hedgas_obj.rgdr_stitNonOccET_exp=rgdr_stitNonOccET[0]
hedgas_obj.hec_stitNonOccET_exp=hec_stitNonOccET[0]
hedgas_obj.hec_stitNonOccET_ppm_exp=hec_stitNonOccET_ppm[0]
hedgas_obj.rgdr_stitNonOccTB_exp=rgdr_stitNonOccTB[0]
hedgas_obj.hec_stitNonOccTB_exp=hec_stitNonOccTB[0]
hedgas_obj.hec_stitNonOccTB_ppm_exp=hec_stitNonOccTB_ppm[0]
hedgas_obj.rgdr_stitNonOccPU_exp=rgdr_stitNonOccPU[0]
hedgas_obj.hec_stitNonOccPU_exp=hec_stitNonOccPU[0]
hedgas_obj.hec_stitNonOccPU_ppm_exp=hec_stitNonOccPU_ppm[0]
hedgas_obj.hec_stitNonOccSYS_exp=hec_stitNonOccSYS[0]
hedgas_obj.hec_stitNonOccSYS_ppm_exp=hec_stitNonOccSYS_ppm[0]
hedgas_obj.noael_adj_ltNonOccET_exp=noael_adj_ltNonOccET[0]
hedgas_obj.mv_a_ltNonOccET_exp=mv_a_ltNonOccET[0]
hedgas_obj.rgdr_ltNonOccET_exp=rgdr_ltNonOccET[0]
hedgas_obj.hec_ltNonOccET_exp=hec_ltNonOccET[0]
hedgas_obj.hec_ltNonOccET_ppm_exp=hec_ltNonOccET_ppm[0]
hedgas_obj.rgdr_ltNonOccTB_exp=rgdr_ltNonOccTB[0]
hedgas_obj.hec_ltNonOccTB_exp=hec_ltNonOccTB[0]
hedgas_obj.hec_ltNonOccTB_ppm_exp=hec_ltNonOccTB_ppm[0]
hedgas_obj.rgdr_ltNonOccPU_exp=rgdr_ltNonOccPU[0]
hedgas_obj.hec_ltNonOccPU_exp=hec_ltNonOccPU[0]
hedgas_obj.hec_ltNonOccPU_ppm_exp=hec_ltNonOccPU_ppm[0]
hedgas_obj.hec_ltNonOccSYS_exp=hec_ltNonOccSYS[0]
hedgas_obj.hec_ltNonOccSYS_ppm_exp=hec_ltNonOccSYS_ppm[0]
hedgas_obj.noael_adj_acuteOccET_exp=noael_adj_acuteOccET[0]
hedgas_obj.mv_a_acuteOccET_exp=mv_a_acuteOccET[0]
hedgas_obj.rgdr_acuteOccET_exp=rgdr_acuteOccET[0]
hedgas_obj.hec_acuteOccET_exp=hec_acuteOccET[0]
hedgas_obj.hec_acuteOccET_ppm_exp=hec_acuteOccET_ppm[0]
hedgas_obj.rgdr_acuteOccTB_exp=rgdr_acuteOccTB[0]
hedgas_obj.hec_acuteOccTB_exp=hec_acuteOccTB[0]
hedgas_obj.hec_acuteOccTB_ppm_exp=hec_acuteOccTB_ppm[0]
hedgas_obj.rgdr_acuteOccPU_exp=rgdr_acuteOccPU[0]
hedgas_obj.hec_acuteOccPU_exp=hec_acuteOccPU[0]
hedgas_obj.hec_acuteOccPU_ppm_exp=hec_acuteOccPU_ppm[0]
hedgas_obj.hec_acuteOccSYS_exp=hec_acuteOccSYS[0]
hedgas_obj.hec_acuteOccSYS_ppm_exp=hec_acuteOccSYS_ppm[0]
hedgas_obj.noael_adj_stitOccET_exp=noael_adj_stitOccET[0]
hedgas_obj.mv_a_stitOccET_exp=mv_a_stitOccET[0]
hedgas_obj.rgdr_stitOccET_exp=rgdr_stitOccET[0]
hedgas_obj.hec_stitOccET_exp=hec_stitOccET[0]
hedgas_obj.hec_stitOccET_ppm_exp=hec_stitOccET_ppm[0]
hedgas_obj.rgdr_stitOccTB_exp=rgdr_stitOccTB[0]
hedgas_obj.hec_stitOccTB_exp=hec_stitOccTB[0]
hedgas_obj.hec_stitOccTB_ppm_exp=hec_stitOccTB_ppm[0]
hedgas_obj.rgdr_stitOccPU_exp=rgdr_stitOccPU[0]
hedgas_obj.hec_stitOccPU_exp=hec_stitOccPU[0]
hedgas_obj.hec_stitOccPU_ppm_exp=hec_stitOccPU_ppm[0]
hedgas_obj.hec_stitOccSYS_exp=hec_stitOccSYS[0]
hedgas_obj.hec_stitOccSYS_ppm_exp=hec_stitOccSYS_ppm[0]
hedgas_obj.noael_adj_ltOccET_exp=noael_adj_ltOccET[0]
hedgas_obj.mv_a_ltOccET_exp=mv_a_ltOccET[0]
hedgas_obj.rgdr_ltOccET_exp=rgdr_ltOccET[0]
hedgas_obj.hec_ltOccET_exp=hec_ltOccET[0]
hedgas_obj.hec_ltOccET_ppm_exp=hec_ltOccET_ppm[0]
hedgas_obj.rgdr_ltOccTB_exp=rgdr_ltOccTB[0]
hedgas_obj.hec_ltOccTB_exp=hec_ltOccTB[0]
hedgas_obj.hec_ltOccTB_ppm_exp=hec_ltOccTB_ppm[0]
hedgas_obj.rgdr_ltOccPU_exp=rgdr_ltOccPU[0]
hedgas_obj.hec_ltOccPU_exp=hec_ltOccPU[0]
hedgas_obj.hec_ltOccPU_ppm_exp=hec_ltOccPU_ppm[0]
hedgas_obj.hec_ltOccSYS_exp=hec_ltOccSYS[0]
hedgas_obj.hec_ltOccSYS_ppm_exp=hec_ltOccSYS_ppm[0]

class hedgasQaqcPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', 'title')
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'hedgas','page':'qaqc'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'hedgas',
                'model_attributes':'HED Gas Calculator QAQC'})
        html = html + hedgas_tables.timestamp()
        html = html + hedgas_tables.table_all_qaqc(hedgas_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', hedgasQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
