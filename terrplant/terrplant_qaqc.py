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
sys.path.append("../terrplant")
from terrplant import terrplant_model
from terrplant import terrplant_tables
import logging

logger = logging.getLogger('TerrplantQaqcPage')

cwd= os.getcwd()
data = csv.reader(open(cwd+'/terrplant/terrplant_qaqc_inputs.csv'))
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

data.next()
for row in data:
    A.append(float(row[0]))
    I.append(float(row[1]))  
    R.append(float(row[2]))
    rundry_out.append(float(row[3])) 
    runsemi_out.append(float(row[4]))
    D.append(float(row[5]))
    spray_out.append(float(row[6])) 
    totaldry_out.append(float(row[7]))
    totalsemi_out.append(float(row[8]))
    nms.append(float(row[9]))
    nmsRQdry_out.append(float(row[10])) 
    LOCnmsdry_out.append(str(row[11]))
    nmsRQsemi_out.append(float(row[12]))
    LOCnmssemi_out.append(str(row[13])) 
    nmsRQspray_out.append(float(row[14]))
    LOCnmsspray_out.append(str(row[15]))
    lms.append(float(row[16]))
    lmsRQdry_out.append(float(row[17])) 
    LOClmsdry_out.append(str(row[18]))
    lmsRQsemi_out.append(float(row[19]))
    LOClmssemi_out.append(str(row[20])) 
    lmsRQspray_out.append(float(row[21]))
    LOClmsspray_out.append(str(row[22]))
    nds.append(float(row[23]))
    ndsRQdry_out.append(float(row[24])) 
    LOCndsdry_out.append(str(row[25]))
    ndsRQsemi_out.append(float(row[26]))
    LOCndssemi_out.append(str(row[27])) 
    ndsRQspray_out.append(float(row[28]))
    LOCndsspray_out.append(str(row[29]))
    lds.append(float(row[30]))
    ldsRQdry_out.append(float(row[31])) 
    LOCldsdry_out.append(str(row[32]))
    ldsRQsemi_out.append(float(row[33]))
    LOCldssemi_out.append(str(row[34])) 
    ldsRQspray_out.append(float(row[35]))
    LOCldsspray_out.append(str(row[36]))
    
out_fun_rundry = []
out_fun_runsemi = []
out_fun_spray = []
out_fun_totaldry = []
out_fun_totalsemi = []
out_fun_nmsRQdry = []
out_fun_LOCnmsdry = []
out_fun_nmsRQsemi = []
out_fun_LOCnmssemi = []
out_fun_nmsRQspray = []
out_fun_LOCnmsspray = []
out_fun_lmsRQdry = []
out_fun_LOClmsdry = []
out_fun_lmsRQsemi = []
out_fun_LOClmssemi = []
out_fun_lmsRQspray = []
out_fun_LOClmsspray = []
out_fun_ndsRQdry = []
out_fun_LOCndsdry = []
out_fun_ndsRQsemi = []
out_fun_LOCndssemi = []
out_fun_ndsRQspray = []
out_fun_LOCndsspray = []
out_fun_ldsRQdry = []
out_fun_LOCldsdry = []
out_fun_ldsRQsemi = []
out_fun_LOCldssemi = []
out_fun_ldsRQspray = []
out_fun_LOCldsspray = []

def set_globals(**kwargs):
    for argname in kwargs:
        globals()['%s_in' % argname] = kwargs[argname]
           
class TestCase_rundry_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.rundry_out_in=rundry_out_in
    def testRundry_out_in(self):
            fun = self.terr.rundry()
            out_fun_rundry.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("rundry",self.rundry_out_in,fun)
            self.assertEqual(round(fun,3),round(self.rundry_out_in,3),testFailureMessage)
           
class TestCase_runsemi_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.runsemi_out_in=runsemi_out_in
    def testRundry_out_in(self):
            fun = self.terr.runsemi()
            out_fun_runsemi.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("runsemi",self.runsemi_out_in,fun)
            self.assertEqual(round(fun,3),round(self.runsemi_out_in,3),testFailureMessage)
           
class TestCase_spray_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.spray_out_in=spray_out_in
    def testRundry_out_in(self):
            fun = self.terr.spray()
            out_fun_spray.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.spray_out_in,fun)
            self.assertEqual(round(fun,3),round(self.spray_out_in,3),testFailureMessage)
           
class TestCase_totaldry_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.totaldry_out_in=totaldry_out_in
    def testRundry_out_in(self):
            fun = self.terr.totaldry()
            out_fun_totaldry.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.totaldry_out_in,fun)
            self.assertEqual(round(fun,3),round(self.totaldry_out_in,3),testFailureMessage)
           
class TestCase_totalsemi_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.totalsemi_out_in=totalsemi_out_in
    def testRundry_out_in(self):
            fun = self.terr.totalsemi()
            out_fun_totalsemi.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.totalsemi_out_in,fun)
            self.assertEqual(round(fun,3),round(self.totalsemi_out_in,3),testFailureMessage)
           
class TestCase_nmsRQdry_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.nmsRQdry_out_in=nmsRQdry_out_in
    def testRundry_out_in(self):
            fun = self.terr.nmsRQdry()
            out_fun_nmsRQdry.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.nmsRQdry_out_in,fun)
            self.assertEqual(round(fun,3),round(self.nmsRQdry_out_in,3),testFailureMessage)
           
class TestCase_LOCnmsdry_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOCnmsdry_out_in=LOCnmsdry_out_in
    def testRundry_out_in(self):
            fun = self.terr.LOCnmsdry()
            out_fun_LOCnmsdry.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCnmsdry_out_in,fun)
            self.assertEqual(fun,self.LOCnmsdry_out_in,testFailureMessage)
           
class TestCase_nmsRQsemi_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.nmsRQsemi_out_in=nmsRQsemi_out_in
    def testRunsemi_out_in(self):
            fun = self.terr.nmsRQsemi()
            out_fun_nmsRQsemi.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.nmsRQsemi_out_in,fun)
            self.assertEqual(round(fun,3),round(self.nmsRQsemi_out_in,3),testFailureMessage)
           
class TestCase_LOCnmssemi_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOCnmssemi_out_in=LOCnmssemi_out_in
    def testRunsemi_out_in(self):
            fun = self.terr.LOCnmssemi()
            out_fun_LOCnmssemi.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCnmssemi_out_in,fun)
            self.assertEqual(fun,self.LOCnmssemi_out_in,testFailureMessage)
           
class TestCase_nmsRQspray_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.nmsRQspray_out_in=nmsRQspray_out_in
    def testRunspray_out_in(self):
            fun = self.terr.nmsRQspray()
            out_fun_nmsRQspray.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.nmsRQspray_out_in,fun)
            self.assertEqual(round(fun,3),round(self.nmsRQspray_out_in,3),testFailureMessage)
           
class TestCase_LOCnmsspray_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOCnmsspray_out_in=LOCnmsspray_out_in
    def testRunspray_out_in(self):
            fun = self.terr.LOCnmsspray()
            out_fun_LOCnmsspray.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCnmsspray_out_in,fun)
            self.assertEqual(fun,self.LOCnmsspray_out_in,testFailureMessage)
     
class TestCase_lmsRQdry_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.lmsRQdry_out_in=lmsRQdry_out_in
    def testRundry_out_in(self):
            fun = self.terr.lmsRQdry()
            out_fun_lmsRQdry.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.lmsRQdry_out_in,fun)
            self.assertEqual(round(fun,3),round(self.lmsRQdry_out_in,3),testFailureMessage)
           
class TestCase_LOClmsdry_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOClmsdry_out_in=LOClmsdry_out_in
    def testRundry_out_in(self):
            fun = self.terr.LOClmsdry()
            out_fun_LOClmsdry.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOClmsdry_out_in,fun)
            self.assertEqual(fun,self.LOClmsdry_out_in,testFailureMessage)
           
class TestCase_lmsRQsemi_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.lmsRQsemi_out_in=lmsRQsemi_out_in
    def testRunsemi_out_in(self):
            fun = self.terr.lmsRQsemi()
            out_fun_lmsRQsemi.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.lmsRQsemi_out_in,fun)
            self.assertEqual(round(fun,3),round(self.lmsRQsemi_out_in,3),testFailureMessage)
           
class TestCase_LOClmssemi_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOClmssemi_out_in=LOClmssemi_out_in
    def testRunsemi_out_in(self):
            fun = self.terr.LOClmssemi()
            out_fun_LOClmssemi.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOClmssemi_out_in,fun)
            self.assertEqual(fun,self.LOClmssemi_out_in,testFailureMessage)
           
class TestCase_lmsRQspray_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.lmsRQspray_out_in=lmsRQspray_out_in
    def testRunspray_out_in(self):
            fun = self.terr.lmsRQspray()
            out_fun_lmsRQspray.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.lmsRQspray_out_in,fun)
            self.assertEqual(round(fun,3),round(self.lmsRQspray_out_in,3),testFailureMessage)
           
class TestCase_LOClmsspray_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOClmsspray_out_in=LOClmsspray_out_in
    def testRunspray_out_in(self):
            fun = self.terr.LOClmsspray()
            out_fun_LOClmsspray.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOClmsspray_out_in,fun)
            self.assertEqual(fun,self.LOClmsspray_out_in,testFailureMessage)
     
class TestCase_ndsRQdry_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.ndsRQdry_out_in=ndsRQdry_out_in
    def testRundry_out_in(self):
            fun = self.terr.ndsRQdry()
            out_fun_ndsRQdry.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ndsRQdry_out_in,fun)
            self.assertEqual(round(fun,3),round(self.ndsRQdry_out_in,3),testFailureMessage)
           
class TestCase_LOCndsdry_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOCndsdry_out_in=LOCndsdry_out_in
    def testRundry_out_in(self):
            fun = self.terr.LOCndsdry()
            out_fun_LOCndsdry.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCndsdry_out_in,fun)
            self.assertEqual(fun,self.LOCndsdry_out_in,testFailureMessage)
           
class TestCase_ndsRQsemi_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.ndsRQsemi_out_in=ndsRQsemi_out_in
    def testRunsemi_out_in(self):
            fun = self.terr.ndsRQsemi()
            out_fun_ndsRQsemi.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ndsRQsemi_out_in,fun)
            self.assertEqual(round(fun,3),round(self.ndsRQsemi_out_in,3),testFailureMessage)
           
class TestCase_LOCndssemi_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOCndssemi_out_in=LOCndssemi_out_in
    def testRunsemi_out_in(self):
            fun = self.terr.LOCndssemi()
            out_fun_LOCndssemi.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCndssemi_out_in,fun)
            self.assertEqual(fun,self.LOCndssemi_out_in,testFailureMessage)
           
class TestCase_ndsRQspray_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.ndsRQspray_out_in=ndsRQspray_out_in
    def testRunspray_out_in(self):
            fun = self.terr.ndsRQspray()
            out_fun_ndsRQspray.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ndsRQspray_out_in,fun)
            self.assertEqual(round(fun,3),round(self.ndsRQspray_out_in,3),testFailureMessage)
           
class TestCase_LOCndsspray_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOCndsspray_out_in=LOCndsspray_out_in
    def testRunspray_out_in(self):
            fun = self.terr.LOCndsspray()
            out_fun_LOCndsspray.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCndsspray_out_in,fun)
            self.assertEqual(fun,self.LOCndsspray_out_in,testFailureMessage)
     
class TestCase_ldsRQdry_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.ldsRQdry_out_in=ldsRQdry_out_in
    def testRundry_out_in(self):
            fun = self.terr.ldsRQdry()
            out_fun_ldsRQdry.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ldsRQdry_out_in,fun)
            self.assertEqual(round(fun,3),round(self.ldsRQdry_out_in,3),testFailureMessage)
           
class TestCase_LOCldsdry_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOCldsdry_out_in=LOCldsdry_out_in
    def testRundry_out_in(self):
            fun = self.terr.LOCldsdry()
            out_fun_LOCldsdry.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCldsdry_out_in,fun)
            self.assertEqual(fun,self.LOCldsdry_out_in,testFailureMessage)
           
class TestCase_ldsRQsemi_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.ldsRQsemi_out_in=ldsRQsemi_out_in
    def testRunsemi_out_in(self):
            fun = self.terr.ldsRQsemi()
            out_fun_ldsRQsemi.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ldsRQsemi_out_in,fun)
            self.assertEqual(round(fun,3),round(self.ldsRQsemi_out_in,3),testFailureMessage)
           
class TestCase_LOCldssemi_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOCldssemi_out_in=LOCldssemi_out_in
    def testRunsemi_out_in(self):
            fun = self.terr.LOCldssemi()
            out_fun_LOCldssemi.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCldssemi_out_in,fun)
            self.assertEqual(fun,self.LOCldssemi_out_in,testFailureMessage)
           
class TestCase_ldsRQspray_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.ldsRQspray_out_in=ldsRQspray_out_in
    def testRunspray_out_in(self):
            fun = self.terr.ldsRQspray()
            out_fun_ldsRQspray.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.ldsRQspray_out_in,fun)
            self.assertEqual(round(fun,3),round(self.ldsRQspray_out_in,3),testFailureMessage)
           
class TestCase_LOCldsspray_out(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.terr = terrplant_model.terrplant(True,False,A_in,I_in,R_in,D_in,nms_in,lms_in,nds_in,lds_in)
        #####Pre-defined outputs########
        self.LOCldsspray_out_in=LOCldsspray_out_in
    def testRunspray_out_in(self):
            fun = self.terr.LOCldsspray()
            out_fun_LOCldsspray.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("spray",self.LOCldsspray_out_in,fun)
            self.assertEqual(fun,self.LOCldsspray_out_in,testFailureMessage)

def suite(TestCaseName, **kwargs):
    suite = unittest.TestSuite()
    set_globals(**kwargs)
    suite.addTest(unittest.makeSuite(TestCaseName))
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    stream.seek(0)
    test_out=stream.read()
    return test_out

test_suite_rundry_out = suite(TestCase_rundry_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], rundry_out=rundry_out[0])
test_suite_runsemi_out = suite(TestCase_runsemi_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], runsemi_out=runsemi_out[0])
test_suite_spray_out = suite(TestCase_spray_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], spray_out=spray_out[0])
test_suite_totaldry_out = suite(TestCase_totaldry_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], totaldry_out=totaldry_out[0])
test_suite_totalsemi_out = suite(TestCase_totalsemi_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], totalsemi_out=totalsemi_out[0])
test_suite_nmsRQdry_out = suite(TestCase_nmsRQdry_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], nmsRQdry_out=nmsRQdry_out[0])
test_suite_LOCnmsdry_out = suite(TestCase_LOCnmsdry_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOCnmsdry_out=LOCnmsdry_out[0])
test_suite_nmsRQsemi_out = suite(TestCase_nmsRQsemi_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], nmsRQsemi_out=nmsRQsemi_out[0])
test_suite_LOCnmssemi_out = suite(TestCase_LOCnmssemi_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOCnmssemi_out=LOCnmssemi_out[0])
test_suite_nmsRQspray_out = suite(TestCase_nmsRQspray_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], nmsRQspray_out=nmsRQspray_out[0])
test_suite_LOCnmsspray_out = suite(TestCase_LOCnmsspray_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOCnmsspray_out=LOCnmsspray_out[0])
test_suite_lmsRQdry_out = suite(TestCase_lmsRQdry_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], lmsRQdry_out=lmsRQdry_out[0])
test_suite_LOClmsdry_out = suite(TestCase_LOClmsdry_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOClmsdry_out=LOClmsdry_out[0])
test_suite_lmsRQsemi_out = suite(TestCase_lmsRQsemi_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], lmsRQsemi_out=lmsRQsemi_out[0])
test_suite_LOClmssemi_out = suite(TestCase_LOClmssemi_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOClmssemi_out=LOClmssemi_out[0])
test_suite_lmsRQspray_out = suite(TestCase_lmsRQspray_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], lmsRQspray_out=lmsRQspray_out[0])
test_suite_LOClmsspray_out = suite(TestCase_LOClmsspray_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOClmsspray_out=LOClmsspray_out[0])
test_suite_ndsRQdry_out = suite(TestCase_ndsRQdry_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], ndsRQdry_out=ndsRQdry_out[0])
test_suite_LOCndsdry_out = suite(TestCase_LOCndsdry_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOCndsdry_out=LOCndsdry_out[0])
test_suite_ndsRQsemi_out = suite(TestCase_ndsRQsemi_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], ndsRQsemi_out=ndsRQsemi_out[0])
test_suite_LOCndssemi_out = suite(TestCase_LOCndssemi_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOCndssemi_out=LOCndssemi_out[0])
test_suite_ndsRQspray_out = suite(TestCase_ndsRQspray_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], ndsRQspray_out=ndsRQspray_out[0])
test_suite_LOCndsspray_out = suite(TestCase_LOCndsspray_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOCndsspray_out=LOCndsspray_out[0])
test_suite_ldsRQdry_out = suite(TestCase_ldsRQdry_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], ldsRQdry_out=ldsRQdry_out[0])
test_suite_LOCldsdry_out = suite(TestCase_LOCldsdry_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOCldsdry_out=LOCldsdry_out[0])
test_suite_ldsRQsemi_out = suite(TestCase_ldsRQsemi_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], ldsRQsemi_out=ldsRQsemi_out[0])
test_suite_LOCldssemi_out = suite(TestCase_LOCldssemi_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOCldssemi_out=LOCldssemi_out[0])
test_suite_ldsRQspray_out = suite(TestCase_ldsRQspray_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], ldsRQspray_out=ldsRQspray_out[0])
test_suite_LOCldsspray_out = suite(TestCase_LOCldsspray_out, A=A[0], I=I[0], R=R[0], D=D[0],nms=nms[0],lms=lms[0],nds=nds[0],lds=lds[0], LOCldsspray_out=LOCldsspray_out[0])

class TerrplantQaqcPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('terrplant/terrplant_description.txt','r')
        x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'terrplant','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'terrplant',
                'model_attributes':'IEC QAQC'})
        html = html + """
        <table border="1">
        <tr><H3>Model Validation Inputs</H3></tr><br>
        <tr>
        <td>Input Name</td>
        <td>Test value1</td>
        <td>Unit</td>
        </tr>      
        <tr>
        <td>Application Rate</td>
        <td>%s</td>
        <td>&nbsp</td>
        </tr>
        <tr>
        <td>Incorporation Rate</td>
        <td>%s</td>
        <td>&nbsp</td>
        </tr>
        <tr>
        <td>Runoff Fraction</td>
        <td>%s</td>       
        <td>&nbsp</td>
        </tr>
        <tr>
        <td>Drift Fraction</td>
        <td>%s</td>       
        <td>&nbsp</td>
        </tr>
        <tr>
        <td>EC25 (Non-listed) Monocot Seedling</td>
        <td>%s</td>
        <td>&nbsp</td>
        </tr>
        <tr>
        <td>NOAEC (Listed) Monocot Seedling</td>
        <td>%s</td>
        <td>&nbsp</td>
        </tr>
        <tr>
        <td>EC25 (Non-listed) Dicot Seedling</td>
        <td>%s</td>       
        <td>&nbsp</td>
        </tr>
        <tr>
        <td>NOAEC (Listed) Dicot Seedling</td>
        <td>%s</td>       
        <td>&nbsp</td>
        </tr>
        </table>
        """  % (A[0], I[0], R[0], D[0], nms[0], lms[0], nds[0], lds[0])      
        html = html + """
        <table width="500" border="1">
            <br>
            <tr><H3>Model Validation Outputs<H3></tr><br>
            <tr>
                <td>Model Name</td>
                <td>Simulated value</td>
                <td>Expected value</td>
                <td>Test output</td>       
            </tr>
            <tr>
                <td>rundry</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>runsemi</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>spray</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>totaldry</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>totalsemi</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>      
            <tr>
                <td>nmsRQdry</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOCnmsdry</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>       
            <tr>
                <td>nmsRQsemi</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOCnmssemi</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>        
            <tr>
                <td>nmsRQspray</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOCnmsspray</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>      
            <tr>
                <td>lmsRQdry</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOClmsdry</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>       
            <tr>
                <td>lmsRQsemi</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOClmssemi</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>        
            <tr>
                <td>lmsRQspray</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOCndsspray</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>      
            <tr>
                <td>ndsRQdry</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOCndsdry</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>       
            <tr>
                <td>ndsRQsemi</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOCndssemi</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>        
            <tr>
                <td>ndsRQspray</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOCndsspray</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>       
            <tr>
                <td>ldsRQdry</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOCldsdry</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>       
            <tr>
                <td>ldsRQsemi</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOCldssemi</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>        
            <tr>
                <td>ldsRQspray</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>LOCldsspray</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>   
        </table>
        """ % (round(out_fun_rundry[0],3), round(rundry_out[0],3), test_suite_rundry_out,
            round(out_fun_runsemi[0],3), round(runsemi_out[0],3), test_suite_runsemi_out,
            round(out_fun_spray[0],3), round(spray_out[0],3), test_suite_spray_out,
            round(out_fun_totaldry[0],3), round(totaldry_out[0],3), test_suite_totaldry_out,
            round(out_fun_totalsemi[0],3), round(totalsemi_out[0],3), test_suite_totalsemi_out,
            round(out_fun_nmsRQdry[0],3), round(nmsRQdry_out[0],3), test_suite_nmsRQdry_out,
            out_fun_LOCnmsdry[0], LOCnmsdry_out[0], test_suite_LOCnmsdry_out,
            round(out_fun_nmsRQsemi[0],3), round(nmsRQsemi_out[0],3), test_suite_nmsRQsemi_out,
            out_fun_LOCnmssemi[0], LOCnmssemi_out[0], test_suite_LOCnmssemi_out,
            round(out_fun_nmsRQspray[0],3), round(nmsRQspray_out[0],3), test_suite_nmsRQspray_out,
            out_fun_LOCnmsspray[0], LOCnmsspray_out[0], test_suite_LOCnmsspray_out,
            round(out_fun_lmsRQdry[0],3), round(lmsRQdry_out[0],3), test_suite_lmsRQdry_out,
            out_fun_LOClmsdry[0], LOClmsdry_out[0], test_suite_LOClmsdry_out,
            round(out_fun_lmsRQsemi[0],3), round(lmsRQsemi_out[0],3), test_suite_lmsRQsemi_out,
            out_fun_LOClmssemi[0], LOClmssemi_out[0], test_suite_LOClmssemi_out,
            round(out_fun_lmsRQspray[0],3), round(lmsRQspray_out[0],3), test_suite_lmsRQspray_out,
            out_fun_LOClmsspray[0], LOClmsspray_out[0], test_suite_LOClmsspray_out,
            round(out_fun_ndsRQdry[0],3), round(ndsRQdry_out[0],3), test_suite_ndsRQdry_out,
            out_fun_LOCndsdry[0], LOCndsdry_out[0], test_suite_LOCndsdry_out,
            round(out_fun_ndsRQsemi[0],3), round(ndsRQsemi_out[0],3), test_suite_ndsRQsemi_out,
            out_fun_LOCndssemi[0], LOCndssemi_out[0], test_suite_LOCndssemi_out,
            round(out_fun_ndsRQspray[0],3), round(ndsRQspray_out[0],3), test_suite_ndsRQspray_out,
            out_fun_LOCndsspray[0], LOCndsspray_out[0], test_suite_LOCndsspray_out,
            round(out_fun_ldsRQdry[0],3), round(ldsRQdry_out[0],3), test_suite_ldsRQdry_out,
            out_fun_LOCldsdry[0], LOCldsdry_out[0], test_suite_LOCldsdry_out,
            round(out_fun_ldsRQsemi[0],3), round(ldsRQsemi_out[0],3), test_suite_ldsRQsemi_out,
            out_fun_LOCldssemi[0], LOCldssemi_out[0], test_suite_LOCldssemi_out,
            round(out_fun_ldsRQspray[0],3), round(ldsRQspray_out[0],3), test_suite_ldsRQspray_out,
            out_fun_LOCldsspray[0], LOCldsspray_out[0], test_suite_LOCldsspray_out)
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TerrplantQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
