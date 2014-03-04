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
sys.path.append("../terrplant")
from terrplant import terrplant_model,terrplant_tables
from uber import uber_lib
from django.template import Context, Template
import logging
logger = logging.getLogger('TerrplantQaqcPage')
import rest_funcs

cwd= os.getcwd()
data = csv.reader(open(cwd+'/terrplant/terrplant_qaqc_inputs.csv'))
version_terrplant = '1.2.2'
A=[]
I=[]
R=[]
D=[]
nms=[]
lms=[]
nds=[]
lds=[]
chemical_name = []
pc_code = []
use = []
application_method = []
application_form = []
solubility = []

######Pre-defined outputs########
# rundry_out = []
# runsemi_out = []
# spray_out = []
# totaldry_out = []
# totalsemi_out = []
# nmsRQdry_out = []
# LOCnmsdry_out = []
# nmsRQsemi_out = []
# LOCnmssemi_out = []
# nmsRQspray_out = []
# LOCnmsspray_out = []
# lmsRQdry_out = []
# LOClmsdry_out = []
# lmsRQsemi_out = []
# LOClmssemi_out = []
# lmsRQspray_out = []
# LOClmsspray_out = []
# ndsRQdry_out = []
# LOCndsdry_out = []
# ndsRQsemi_out = []
# LOCndssemi_out = []
# ndsRQspray_out = []
# LOCndsspray_out = []
# ldsRQdry_out = []
# LOCldsdry_out = []
# ldsRQsemi_out = []
# LOCldssemi_out = []
# ldsRQspray_out = []
# LOCldsspray_out = []
nms = []
nds = []
lms = []
lds = []
nmv = []
ndv = []
lmv = []
ldv = []
nmsRQdry_results = []
lmsRQdry_results = []
ndsRQdry_results = []
ldsRQdry_results = []
nmsRQsemi_results = []
lmsRQsemi_results = []
ndsRQsemi_results = []
ldsRQsemi_results = []
nmsRQspray_results = []
lmsRQspray_results = []
ndsRQspray_results = []
ldsRQspray_results = []


data.next()
for row in data:
    chemical_name.append(str(row[0]))
    pc_code.append(str(row[1]))
    use.append(str(row[2]))
    application_method.append(str(row[3]))
    application_form.append(str(row[4]))
    solubility.append(float(row[5]))
    I.append(float(row[6]))
    A.append(float(row[7]))
    D.append(float(row[8]))
    R.append(float(row[9]))
    nms.append(float(row[10]))
    nds.append(float(row[11]))
    lms.append(float(row[12]))
    lds.append(float(row[13]))
    nmv.append(float(row[14]))
    ndv.append(float(row[15]))
    lmv.append(float(row[16]))
    ldv.append(float(row[17]))
    nmsRQdry_results.append(float(row[18]))
    lmsRQdry_results.append(float(row[19]))
    ndsRQdry_results.append(float(row[20]))
    ldsRQdry_results.append(float(row[21]))
    nmsRQsemi_results.append(float(row[22]))
    lmsRQsemi_results.append(float(row[23]))
    ndsRQsemi_results.append(float(row[24]))
    ldsRQsemi_results.append(float(row[25]))
    nmsRQspray_results.append(float(row[26]))
    lmsRQspray_results.append(float(row[27]))
    ndsRQspray_results.append(float(row[28]))
    ldsRQspray_results.append(float(row[29]))

    # rundry_out.append(float(row[4])) 
    # runsemi_out.append(float(row[5]))
    # spray_out.append(float(row[7])) 
    # totaldry_out.append(float(row[8]))
    # totalsemi_out.append(float(row[9]))
    # nms.append(float(row[10]))
    # nmsRQdry_out.append(float(row[11])) 
    # LOCnmsdry_out.append(str(row[12]))
    # nmsRQsemi_out.append(float(row[13]))
    # LOCnmssemi_out.append(str(row[14])) 
    # nmsRQspray_out.append(float(row[15]))
    # LOCnmsspray_out.append(str(row[16]))
    # lms.append(float(row[17]))
    # lmsRQdry_out.append(float(row[18])) 
    # LOClmsdry_out.append(str(row[19]))
    # lmsRQsemi_out.append(float(row[20]))
    # LOClmssemi_out.append(str(row[21])) 
    # lmsRQspray_out.append(float(row[22]))
    # LOClmsspray_out.append(str(row[23]))
    # nds.append(float(row[24]))
    # ndsRQdry_out.append(float(row[25])) 
    # LOCndsdry_out.append(str(row[26]))
    # ndsRQsemi_out.append(float(row[27]))
    # LOCndssemi_out.append(str(row[28])) 
    # ndsRQspray_out.append(float(row[29]))
    # LOCndsspray_out.append(str(row[30]))
    # lds.append(float(row[31]))
    # ldsRQdry_out.append(float(row[32])) 
    # LOCldsdry_out.append(str(row[33]))
    # ldsRQsemi_out.append(float(row[34]))
    # LOCldssemi_out.append(str(row[35])) 
    # ldsRQspray_out.append(float(row[36]))
    # LOCldsspray_out.append(str(row[37]))


# I CREATED THIS
# out_nms = []
# out_nds = []
# out_lms = []
# out_lds = []
# out_nmv = []
# out_ndv = []
# out_lmv = []
# out_ldv = []
# out_nmsRQdry_results = []
# out_lmsRQdry_results = []
# out_ndsRQdry_results = []
# out_ldsRQdry_results = []
# out_nmsRQsemi_results = []
# out_lmsRQsemi_results = []
# out_ndsRQsemi_results = []
# out_ldsRQsemi_results = []
# out_nmsRQspray_results = []
# out_lmsRQspray_results = []
# out_ndsRQspray_results = []
# out_ldsRQspray_results = []
  
# out_fun_rundry = []
# out_fun_runsemi = []
# out_fun_spray = []
# out_fun_totaldry = []
# out_fun_totalsemi = []
# out_fun_nmsRQdry = []
# out_fun_LOCnmsdry = []
# out_fun_nmsRQsemi = []
# out_fun_LOCnmssemi = []
# out_fun_nmsRQspray = []
# out_fun_LOCnmsspray = []
# out_fun_lmsRQdry = []
# out_fun_LOClmsdry = []
# out_fun_lmsRQsemi = []
# out_fun_LOClmssemi = []
# out_fun_lmsRQspray = []
# out_fun_LOClmsspray = []
# out_fun_ndsRQdry = []
# out_fun_LOCndsdry = []
# out_fun_ndsRQsemi = []
# out_fun_LOCndssemi = []
# out_fun_ndsRQspray = []
# out_fun_LOCndsspray = []
# out_fun_ldsRQdry = []
# out_fun_LOCldsdry = []
# out_fun_ldsRQsemi = []
# out_fun_LOCldssemi = []
# out_fun_ldsRQspray = []
# out_fun_LOCldsspray = []





# def set_globals(**kwargs):
#     for argname in kwargs:
#         globals()['%s_in' % argname] = kwargs[argname]
           
# class TestCase_rundry_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.rundry_out_in=rundry_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.rundry()
#             out_fun_rundry.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("rundry",self.rundry_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.rundry_out_in,3),testFailureMessage)
           
# class TestCase_runsemi_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.runsemi_out_in=runsemi_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.runsemi()
#             out_fun_runsemi.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("runsemi",self.runsemi_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.runsemi_out_in,3),testFailureMessage)
           
# class TestCase_spray_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.spray_out_in=spray_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.spray()
#             out_fun_spray.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.spray_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.spray_out_in,3),testFailureMessage)
           
# class TestCase_totaldry_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.totaldry_out_in=totaldry_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.totaldry()
#             out_fun_totaldry.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.totaldry_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.totaldry_out_in,3),testFailureMessage)
           
# class TestCase_totalsemi_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.totalsemi_out_in=totalsemi_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.totalsemi()
#             out_fun_totalsemi.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.totalsemi_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.totalsemi_out_in,3),testFailureMessage)
           
# class TestCase_nmsRQdry_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.nmsRQdry_out_in=nmsRQdry_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.nmsRQdry()
#             out_fun_nmsRQdry.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.nmsRQdry_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.nmsRQdry_out_in,3),testFailureMessage)
           
# class TestCase_LOCnmsdry_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOCnmsdry_out_in=LOCnmsdry_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.LOCnmsdry()
#             out_fun_LOCnmsdry.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCnmsdry_out_in,fun)
#             self.assertEqual(fun,self.LOCnmsdry_out_in,testFailureMessage)
           
# class TestCase_nmsRQsemi_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.nmsRQsemi_out_in=nmsRQsemi_out_in
#     def testRunsemi_out_in(self):
#             fun = self.terr.nmsRQsemi()
#             out_fun_nmsRQsemi.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.nmsRQsemi_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.nmsRQsemi_out_in,3),testFailureMessage)
           
# class TestCase_LOCnmssemi_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOCnmssemi_out_in=LOCnmssemi_out_in
#     def testRunsemi_out_in(self):
#             fun = self.terr.LOCnmssemi()
#             out_fun_LOCnmssemi.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCnmssemi_out_in,fun)
#             self.assertEqual(fun,self.LOCnmssemi_out_in,testFailureMessage)
           
# class TestCase_nmsRQspray_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.nmsRQspray_out_in=nmsRQspray_out_in
#     def testRunspray_out_in(self):
#             fun = self.terr.nmsRQspray()
#             out_fun_nmsRQspray.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.nmsRQspray_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.nmsRQspray_out_in,3),testFailureMessage)
           
# class TestCase_LOCnmsspray_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOCnmsspray_out_in=LOCnmsspray_out_in
#     def testRunspray_out_in(self):
#             fun = self.terr.LOCnmsspray()
#             out_fun_LOCnmsspray.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCnmsspray_out_in,fun)
#             self.assertEqual(fun,self.LOCnmsspray_out_in,testFailureMessage)
     
# class TestCase_lmsRQdry_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.lmsRQdry_out_in=lmsRQdry_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.lmsRQdry()
#             out_fun_lmsRQdry.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.lmsRQdry_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.lmsRQdry_out_in,3),testFailureMessage)
           
# class TestCase_LOClmsdry_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOClmsdry_out_in=LOClmsdry_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.LOClmsdry()
#             out_fun_LOClmsdry.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOClmsdry_out_in,fun)
#             self.assertEqual(fun,self.LOClmsdry_out_in,testFailureMessage)
           
# class TestCase_lmsRQsemi_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.lmsRQsemi_out_in=lmsRQsemi_out_in
#     def testRunsemi_out_in(self):
#             fun = self.terr.lmsRQsemi()
#             out_fun_lmsRQsemi.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.lmsRQsemi_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.lmsRQsemi_out_in,3),testFailureMessage)
           
# class TestCase_LOClmssemi_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOClmssemi_out_in=LOClmssemi_out_in
#     def testRunsemi_out_in(self):
#             fun = self.terr.LOClmssemi()
#             out_fun_LOClmssemi.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOClmssemi_out_in,fun)
#             self.assertEqual(fun,self.LOClmssemi_out_in,testFailureMessage)
           
# class TestCase_lmsRQspray_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.lmsRQspray_out_in=lmsRQspray_out_in
#     def testRunspray_out_in(self):
#             fun = self.terr.lmsRQspray()
#             out_fun_lmsRQspray.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.lmsRQspray_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.lmsRQspray_out_in,3),testFailureMessage)
           
# class TestCase_LOClmsspray_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOClmsspray_out_in=LOClmsspray_out_in
#     def testRunspray_out_in(self):
#             fun = self.terr.LOClmsspray()
#             out_fun_LOClmsspray.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOClmsspray_out_in,fun)
#             self.assertEqual(fun,self.LOClmsspray_out_in,testFailureMessage)
     
# class TestCase_ndsRQdry_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.ndsRQdry_out_in=ndsRQdry_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.ndsRQdry()
#             out_fun_ndsRQdry.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ndsRQdry_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.ndsRQdry_out_in,3),testFailureMessage)
           
# class TestCase_LOCndsdry_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOCndsdry_out_in=LOCndsdry_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.LOCndsdry()
#             out_fun_LOCndsdry.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCndsdry_out_in,fun)
#             self.assertEqual(fun,self.LOCndsdry_out_in,testFailureMessage)
           
# class TestCase_ndsRQsemi_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.ndsRQsemi_out_in=ndsRQsemi_out_in
#     def testRunsemi_out_in(self):
#             fun = self.terr.ndsRQsemi()
#             out_fun_ndsRQsemi.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ndsRQsemi_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.ndsRQsemi_out_in,3),testFailureMessage)
           
# class TestCase_LOCndssemi_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOCndssemi_out_in=LOCndssemi_out_in
#     def testRunsemi_out_in(self):
#             fun = self.terr.LOCndssemi()
#             out_fun_LOCndssemi.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCndssemi_out_in,fun)
#             self.assertEqual(fun,self.LOCndssemi_out_in,testFailureMessage)
           
# class TestCase_ndsRQspray_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.ndsRQspray_out_in=ndsRQspray_out_in
#     def testRunspray_out_in(self):
#             fun = self.terr.ndsRQspray()
#             out_fun_ndsRQspray.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ndsRQspray_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.ndsRQspray_out_in,3),testFailureMessage)
           
# class TestCase_LOCndsspray_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOCndsspray_out_in=LOCndsspray_out_in
#     def testRunspray_out_in(self):
#             fun = self.terr.LOCndsspray()
#             out_fun_LOCndsspray.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCndsspray_out_in,fun)
#             self.assertEqual(fun,self.LOCndsspray_out_in,testFailureMessage)
     
# class TestCase_ldsRQdry_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.ldsRQdry_out_in=ldsRQdry_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.ldsRQdry()
#             out_fun_ldsRQdry.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ldsRQdry_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.ldsRQdry_out_in,3),testFailureMessage)
           
# class TestCase_LOCldsdry_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOCldsdry_out_in=LOCldsdry_out_in
#     def testRundry_out_in(self):
#             fun = self.terr.LOCldsdry()
#             out_fun_LOCldsdry.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCldsdry_out_in,fun)
#             self.assertEqual(fun,self.LOCldsdry_out_in,testFailureMessage)
           
# class TestCase_ldsRQsemi_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.ldsRQsemi_out_in=ldsRQsemi_out_in
#     def testRunsemi_out_in(self):
#             fun = self.terr.ldsRQsemi()
#             out_fun_ldsRQsemi.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ldsRQsemi_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.ldsRQsemi_out_in,3),testFailureMessage)
           
# class TestCase_LOCldssemi_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOCldssemi_out_in=LOCldssemi_out_in
#     def testRunsemi_out_in(self):
#             fun = self.terr.LOCldssemi()
#             out_fun_LOCldssemi.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCldssemi_out_in,fun)
#             self.assertEqual(fun,self.LOCldssemi_out_in,testFailureMessage)
           
# class TestCase_ldsRQspray_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.ldsRQspray_out_in=ldsRQspray_out_in
#     def testRunspray_out_in(self):
#             fun = self.terr.ldsRQspray()
#             out_fun_ldsRQspray.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ldsRQspray_out_in,fun)
#             self.assertEqual(round(fun,3),round(self.ldsRQspray_out_in,3),testFailureMessage)
           
# class TestCase_LOCldsspray_out(unittest.TestCase):
#     def setUp(self):
#         #####Pre-defined inputs########
#         self.terr = terrplant_obj_in
#         #####Pre-defined outputs########
#         self.LOCldsspray_out_in=LOCldsspray_out_in
#     def testRunspray_out_in(self):
#             fun = self.terr.LOCldsspray()
#             out_fun_LOCldsspray.append(fun)
#             testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCldsspray_out_in,fun)
#             self.assertEqual(fun,self.LOCldsspray_out_in,testFailureMessage)

# def suite(TestCaseName, **kwargs):
#     suite = unittest.TestSuite()
#     set_globals(**kwargs)
#     suite.addTest(unittest.makeSuite(TestCaseName))
#     stream = StringIO()
#     runner = unittest.TextTestRunner(stream=stream, verbosity=2)
#     result = runner.run(suite)
#     stream.seek(0)
#     test_out=stream.read()
#     return test_out

# terrplant_obj = terrplant_model.terrplant(True,False,A[0],I[0],R[0],D[0],nms[0],lms[0],nds[0],lds[0])
# test_suite_rundry_out = suite(TestCase_rundry_out, terrplant_obj=terrplant_obj, rundry_out=rundry_out[0])
# test_suite_runsemi_out = suite(TestCase_runsemi_out, terrplant_obj=terrplant_obj, runsemi_out=runsemi_out[0])
# test_suite_spray_out = suite(TestCase_spray_out, terrplant_obj=terrplant_obj, spray_out=spray_out[0])
# test_suite_totaldry_out = suite(TestCase_totaldry_out, terrplant_obj=terrplant_obj, totaldry_out=totaldry_out[0])
# test_suite_totalsemi_out = suite(TestCase_totalsemi_out, terrplant_obj=terrplant_obj, totalsemi_out=totalsemi_out[0])
# test_suite_nmsRQdry_out = suite(TestCase_nmsRQdry_out, terrplant_obj=terrplant_obj, nmsRQdry_out=nmsRQdry_out[0])
# test_suite_LOCnmsdry_out = suite(TestCase_LOCnmsdry_out, terrplant_obj=terrplant_obj, LOCnmsdry_out=LOCnmsdry_out[0])
# test_suite_nmsRQsemi_out = suite(TestCase_nmsRQsemi_out, terrplant_obj=terrplant_obj, nmsRQsemi_out=nmsRQsemi_out[0])
# test_suite_LOCnmssemi_out = suite(TestCase_LOCnmssemi_out, terrplant_obj=terrplant_obj, LOCnmssemi_out=LOCnmssemi_out[0])
# test_suite_nmsRQspray_out = suite(TestCase_nmsRQspray_out, terrplant_obj=terrplant_obj, nmsRQspray_out=nmsRQspray_out[0])
# test_suite_LOCnmsspray_out = suite(TestCase_LOCnmsspray_out, terrplant_obj=terrplant_obj, LOCnmsspray_out=LOCnmsspray_out[0])
# test_suite_lmsRQdry_out = suite(TestCase_lmsRQdry_out, terrplant_obj=terrplant_obj, lmsRQdry_out=lmsRQdry_out[0])
# test_suite_LOClmsdry_out = suite(TestCase_LOClmsdry_out, terrplant_obj=terrplant_obj, LOClmsdry_out=LOClmsdry_out[0])
# test_suite_lmsRQsemi_out = suite(TestCase_lmsRQsemi_out, terrplant_obj=terrplant_obj, lmsRQsemi_out=lmsRQsemi_out[0])
# test_suite_LOClmssemi_out = suite(TestCase_LOClmssemi_out, terrplant_obj=terrplant_obj, LOClmssemi_out=LOClmssemi_out[0])
# test_suite_lmsRQspray_out = suite(TestCase_lmsRQspray_out, terrplant_obj=terrplant_obj, lmsRQspray_out=lmsRQspray_out[0])
# test_suite_LOClmsspray_out = suite(TestCase_LOClmsspray_out, terrplant_obj=terrplant_obj, LOClmsspray_out=LOClmsspray_out[0])
# test_suite_ndsRQdry_out = suite(TestCase_ndsRQdry_out, terrplant_obj=terrplant_obj, ndsRQdry_out=ndsRQdry_out[0])
# test_suite_LOCndsdry_out = suite(TestCase_LOCndsdry_out, terrplant_obj=terrplant_obj, LOCndsdry_out=LOCndsdry_out[0])
# test_suite_ndsRQsemi_out = suite(TestCase_ndsRQsemi_out, terrplant_obj=terrplant_obj, ndsRQsemi_out=ndsRQsemi_out[0])
# test_suite_LOCndssemi_out = suite(TestCase_LOCndssemi_out,terrplant_obj=terrplant_obj, LOCndssemi_out=LOCndssemi_out[0])
# test_suite_ndsRQspray_out = suite(TestCase_ndsRQspray_out, terrplant_obj=terrplant_obj, ndsRQspray_out=ndsRQspray_out[0])
# test_suite_LOCndsspray_out = suite(TestCase_LOCndsspray_out, terrplant_obj=terrplant_obj, LOCndsspray_out=LOCndsspray_out[0])
# test_suite_ldsRQdry_out = suite(TestCase_ldsRQdry_out, terrplant_obj=terrplant_obj, ldsRQdry_out=ldsRQdry_out[0])
# test_suite_LOCldsdry_out = suite(TestCase_LOCldsdry_out, terrplant_obj=terrplant_obj, LOCldsdry_out=LOCldsdry_out[0])
# test_suite_ldsRQsemi_out = suite(TestCase_ldsRQsemi_out, terrplant_obj=terrplant_obj, ldsRQsemi_out=ldsRQsemi_out[0])
# test_suite_LOCldssemi_out = suite(TestCase_LOCldssemi_out, terrplant_obj=terrplant_obj, LOCldssemi_out=LOCldssemi_out[0])
# test_suite_ldsRQspray_out = suite(TestCase_ldsRQspray_out, terrplant_obj=terrplant_obj, ldsRQspray_out=ldsRQspray_out[0])
# test_suite_LOCldsspray_out = suite(TestCase_LOCldsspray_out, terrplant_obj=terrplant_obj, LOCldsspray_out=LOCldsspray_out[0])

class TerrplantQaqcPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('terrplant/terrplant_description.txt','r')
        x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "TerrPlant QA/QC")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'terrplant','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'terrplant',
                'model_attributes':'TerrPlant QAQC'})
        terr = terrplant_model.terrplant(True,True,version_terrplant,"qaqc",A[0],I[0],R[0],D[0],nms[0],lms[0],nds[0],lds[0],chemical_name[0],pc_code[0],use[0],application_method[0],application_form[0],solubility[0])
        terr.chemical_name_expected = chemical_name[0]
        terr.pc_code_expected = pc_code[0]
        terr.use_expected = use[0]
        terr.application_method_expected = application_method[0]
        terr.application_form_expected = application_form[0]
        terr.solubility_expected = solubility[0]

        # terr.rundry_results_expected = out_fun_rundry[0]
        # terr.runsemi_results_expected = out_fun_runsemi[0]
        # terr.spray_results_expected = out_fun_spray[0]
        # terr.totaldry_results_expected = out_fun_totaldry[0]
        # terr.totalsemi_results_expected = out_fun_totalsemi[0]

        terr.nms_expected = nms[0]
        terr.nds_expected = nds[0]
        terr.lms_expected = lms[0]
        terr.lds_expected = lds[0]
        terr.nmv_expected = nmv[0]
        terr.ndv_expected = ndv[0]
        terr.lmv_expected = lmv[0]
        terr.ldv_expected = ldv[0]
        terr.nmsRQdry_results_expected = nmsRQdry_results[0]
        terr.lmsRQdry_results_expected = lmsRQdry_results[0]
        terr.ndsRQdry_results_expected = ndsRQdry_results[0]
        terr.ldsRQdry_results_expected = ldsRQdry_results[0]
        terr.nmsRQsemi_results_expected = nmsRQsemi_results[0]
        terr.lmsRQsemi_results_expected = lmsRQsemi_results[0]
        terr.ndsRQsemi_results_expected = ndsRQsemi_results[0]
        terr.ldsRQsemi_results_expected = ldsRQsemi_results[0]
        terr.nmsRQspray_results_expected = nmsRQspray_results[0]
        terr.lmsRQspray_results_expected = lmsRQspray_results[0]
        terr.ndsRQspray_results_expected = ndsRQspray_results[0]
        terr.ldsRQspray_results_expected = ldsRQspray_results[0]

        # terr.nmsRQdry_results_expected = out_fun_nmsRQdry[0]
        # terr.nmsRQsemi_results_expected = out_fun_nmsRQsemi[0]
        # terr.nmsRQspray_results_expected = out_fun_nmsRQspray[0]
        # terr.lmsRQdry_results_expected = out_fun_lmsRQdry[0]
        # terr.lmsRQsemi_results_expected = out_fun_lmsRQsemi[0]
        # terr.lmsRQspray_results_expected = out_fun_lmsRQspray[0]
        # terr.ndsRQdry_results_expected = out_fun_ndsRQdry[0]
        # terr.ndsRQsemi_results_expected = out_fun_ndsRQsemi[0]
        # terr.ndsRQspray_results_expected = out_fun_ndsRQspray[0]
        # terr.ldsRQdry_results_expected = out_fun_ldsRQdry[0]
        # terr.ldsRQsemi_results_expected = out_fun_ldsRQsemi[0]
        # terr.ldsRQspray_results_expected = out_fun_ldsRQspray[0]

        html = html + terrplant_tables.timestamp(terr)
        html = html + terrplant_tables.table_all_qaqc(terrplant_tables.pvheadings, terrplant_tables.pvuheadings,terrplant_tables.deheadingsqaqc,
                                        terrplant_tables.plantec25noaecheadings,terrplant_tables.plantecdrysemisprayheadingsqaqc, 
                                        terrplant_tables.tmpl, terr)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, terr.__dict__, 'terrplant', 'qaqc')
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TerrplantQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
