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
sys.path.append("../stir")
from stir import stir_model,stir_tables
from uber import uber_lib
from django.template import Context, Template
import logging

logger = logging.getLogger('stirQaqcPage')

cwd= os.getcwd()
data = csv.reader(open(cwd+'/stir/stir_qaqc.csv'))
#inputs
chemical_name = []
application_rate = []
column_height = []
spray_drift_fraction = []
direct_spray_duration = []
molecular_weight = []
vapor_pressure = []
avian_oral_ld50 = []
body_weight_assessed_bird = []
body_weight_tested_bird = []
mineau_scaling_factor = []
mammal_inhalation_lc50 = []
duration_mammal_inhalation_study = []
body_weight_assessed_mammal = []
body_weight_tested_mammal = []
mammal_oral_ld50 = []

#outputs
sat_air_conc = []
inh_rate_avian = []
vid_avian = []
inh_rate_mammal = []
vid_mammal = []
ar2 = []
air_conc = []
sid_avian = []
sid_mammal = []
cf = []
mammal_inhalation_ld50 = []
adjusted_mammal_inhalation_ld50 = []
estimated_avian_inhalation_ld50 = []
adjusted_avian_inhalation_ld50 = []
ratio_vid_avian = []
ratio_sid_avian = []
ratio_vid_mammal = []
ratio_sid_mammal = []
loc_vid_avian = []
loc_sid_avian = []
loc_vid_mammal = []
loc_sid_mammal = []

data.next()
for row in data:
    chemical_name.append(str(row[0]))
    application_rate.append(float(row[1]))
    column_height.append(float(row[2]))
    spray_drift_fraction.append(float(row[3]))
    direct_spray_duration.append(float(row[4]))
    molecular_weight.append(float(row[5]))
    vapor_pressure.append(float(row[6]))
    avian_oral_ld50.append(float(row[7]))
    body_weight_assessed_bird.append(float(row[8]))
    body_weight_tested_bird.append(float(row[9]))
    mineau_scaling_factor.append(float(row[10]))
    mammal_inhalation_lc50.append(float(row[11]))
    duration_mammal_inhalation_study.append(float(row[12]))
    body_weight_assessed_mammal.append(float(row[13]))
    body_weight_tested_mammal.append(float(row[14]))
    mammal_oral_ld50.append(float(row[15]))
    sat_air_conc.append(float(row[16]))
    inh_rate_avian.append(float(row[17]))
    vid_avian.append(float(row[18]))
    inh_rate_mammal.append(float(row[19]))
    vid_mammal.append(float(row[20]))
    ar2.append(str(row[21]))
    air_conc.append(float(row[22]))
    sid_avian.append(float(row[23]))
    sid_mammal.append(float(row[24]))
    cf.append(str(row[25]))
    mammal_inhalation_ld50.append(float(row[26]))
    adjusted_mammal_inhalation_ld50.append(float(row[27]))
    estimated_avian_inhalation_ld50.append(float(row[28]))
    adjusted_avian_inhalation_ld50.append(float(row[29]))
    ratio_vid_avian.append(float(row[30]))
    ratio_sid_avian.append(float(row[31]))
    ratio_vid_mammal.append(float(row[32]))
    ratio_sid_mammal.append(float(row[33]))
    loc_vid_avian.append(str(row[34]))
    loc_sid_avian.append(str(row[35]))
    loc_vid_mammal.append(str(row[36]))
    loc_sid_mammal.append(str(row[37]))


out_fun_sat_air_conc = []
out_fun_inh_rate_avian = []
out_fun_vid_avian = []
out_fun_inh_rate_mammal = []
out_fun_vid_mammal = []
out_fun_ar2 = []
out_fun_air_conc = []
out_fun_sid_avian = []
out_fun_sid_mammal = []
out_fun_cf = []
out_fun_mammal_inhalation_ld50 = []
out_fun_adjusted_mammal_inhalation_ld50 = []
out_fun_estimated_avian_inhalation_ld50 = []
out_fun_adjusted_avian_inhalation_ld50 = []
out_fun_ratio_vid_avian = []
out_fun_ratio_sid_avian = []
out_fun_ratio_vid_mammal = []
out_fun_ratio_sid_mammal = []
out_fun_loc_vid_avian = []
out_fun_loc_sid_avian = []
out_fun_loc_vid_mammal = []
out_fun_loc_sid_mammal = []

def set_globals(**kwargs):
    for argname in kwargs:
        globals()['%s_in' % argname] = kwargs[argname]

class TestCase_sat_air_conc(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testsat_air_conc_in(self):
        out_fun_sat_air_conc.append(self.stir_obj.sat_air_conc)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("sat_air_conc",self.stir_obj.sat_air_conc,fun)
        self.assertEqual(round(fun,3),round(self.sat_air_conc,3),testFailureMessage)

class TestCase_inh_rate_avian(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testinh_rate_avian_in(self):
        out_fun_inh_rate_avian.append(self.stir_obj.inh_rate_avian)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("inh_rate_avian",self.stir_obj.inh_rate_avian,fun)
        self.assertEqual(round(fun,3),round(self.inh_rate_avian,3),testFailureMessage)

class TestCase_vid_avian(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testvid_avian_in(self):
        out_fun_vid_avian.append(self.stir_obj.vid_avian)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("vid_avian",self.stir_obj.vid_avian,fun)
        self.assertEqual(round(fun,3),round(self.vid_avian,3),testFailureMessage)

class TestCase_inh_rate_mammal(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testinh_rate_mammal_in(self):
        out_fun_inh_rate_mammal.append(self.stir_obj.inh_rate_mammal)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("inh_rate_mammal",self.stir_obj.inh_rate_mammal,fun)
        self.assertEqual(round(fun,3),round(self.inh_rate_mammal,3),testFailureMessage)

class TestCase_vid_mammal(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testvid_mammal_in(self):
        out_fun_vid_mammal.append(self.stir_obj.vid_mammal)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("vid_mammal",self.stir_obj.vid_mammal,fun)
        self.assertEqual(round(fun,3),round(self.vid_mammal,3),testFailureMessage)

class TestCase_ar2(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testar2_in(self):
        out_fun_ar2.append(self.stir_obj.ar2)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("ar2",self.stir_obj.ar2,fun)
        self.assertEqual(round(fun,3),round(self.ar2,3),testFailureMessage)

class TestCase_air_conc(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testair_conc_in(self):
        out_fun_air_conc.append(self.stir_obj.air_conc)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("air_conc",self.stir_obj.air_conc,fun)
        self.assertEqual(round(fun,3),round(self.air_conc,3),testFailureMessage)

class TestCase_sid_avian(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testsid_avian_in(self):
        out_fun_sid_avian.append(self.stir_obj.sid_avian)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("sid_avian",self.stir_obj.sid_avian,fun)
        self.assertEqual(round(fun,3),round(self.sid_avian,3),testFailureMessage)

class TestCase_sid_mammal(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testsid_mammal_in(self):
        out_fun_sid_mammal.append(self.stir_obj.sid_mammal)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("sid_mammal",self.stir_obj.sid_mammal,fun)
        self.assertEqual(round(fun,3),round(self.sid_mammal,3),testFailureMessage)

class TestCase_cf(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testcf_in(self):
        out_fun_cf.append(self.stir_obj.cf)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("cf",self.stir_obj.cf,fun)
        self.assertEqual(round(fun,3),round(self.cf,3),testFailureMessage)

class TestCase_mammal_inhalation_ld50(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testmammal_inhalation_ld50_in(self):
        out_fun_mammal_inhalation_ld50.append(self.stir_obj.mammal_inhalation_ld50)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("mammal_inhalation_ld50",self.stir_obj.mammal_inhalation_ld50,fun)
        self.assertEqual(round(fun,3),round(self.mammal_inhalation_ld50,3),testFailureMessage)

class TestCase_adjusted_mammal_inhalation_ld50(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testadjusted_mammal_inhalation_ld50_in(self):
        out_fun_adjusted_mammal_inhalation_ld50.append(self.stir_obj.adjusted_mammal_inhalation_ld50)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("adjusted_mammal_inhalation_ld50",self.stir_obj.adjusted_mammal_inhalation_ld50,fun)
        self.assertEqual(round(fun,3),round(self.adjusted_mammal_inhalation_ld50,3),testFailureMessage)

class TestCase_estimated_avian_inhalation_ld50(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testestimated_avian_inhalation_ld50_in(self):
        out_fun_estimated_avian_inhalation_ld50.append(self.stir_obj.estimated_avian_inhalation_ld50)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("estimated_avian_inhalation_ld50",self.stir_obj.estimated_avian_inhalation_ld50,fun)
        self.assertEqual(round(fun,3),round(self.estimated_avian_inhalation_ld50,3),testFailureMessage)

class TestCase_adjusted_avian_inhalation_ld50(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testadjusted_avian_inhalation_ld50_in(self):
        out_fun_adjusted_avian_inhalation_ld50.append(self.stir_obj.adjusted_avian_inhalation_ld50)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("adjusted_avian_inhalation_ld50",self.stir_obj.adjusted_avian_inhalation_ld50,fun)
        self.assertEqual(round(fun,3),round(self.adjusted_avian_inhalation_ld50,3),testFailureMessage)

class TestCase_ratio_vid_avian(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testratio_vid_avian_in(self):
        out_fun_ratio_vid_avian.append(self.stir_obj.ratio_vid_avian)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("ratio_vid_avian",self.stir_obj.ratio_vid_avian,fun)
        self.assertEqual(round(fun,3),round(self.ratio_vid_avian,3),testFailureMessage)

class TestCase_ratio_sid_avian(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testratio_sid_avian_in(self):
        out_fun_ratio_sid_avian.append(self.stir_obj.ratio_sid_avian)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("ratio_sid_avian",self.stir_obj.ratio_sid_avian,fun)
        self.assertEqual(round(fun,3),round(self.ratio_sid_avian,3),testFailureMessage)

class TestCase_ratio_vid_mammal(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testratio_vid_mammal_in(self):
        out_fun_ratio_vid_mammal.append(self.stir_obj.ratio_vid_mammal)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("ratio_vid_mammal",self.stir_obj.ratio_vid_mammal,fun)
        self.assertEqual(round(fun,3),round(self.ratio_vid_mammal,3),testFailureMessage)

class TestCase_ratio_sid_mammal(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testratio_sid_mammal_in(self):
        out_fun_ratio_sid_mammal.append(self.stir_obj.ratio_sid_mammal)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("ratio_sid_mammal",self.stir_obj.ratio_sid_mammal,fun)
        self.assertEqual(round(fun,3),round(self.ratio_sid_mammal,3),testFailureMessage)

class TestCase_loc_vid_avian(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testloc_vid_avian_in(self):
        out_fun_loc_vid_avian.append(self.stir_obj.loc_vid_avian)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("loc_vid_avian",self.stir_obj.loc_vid_avian,fun)
        self.assertEqual(round(fun,3),round(self.loc_vid_avian,3),testFailureMessage)

class TestCase_loc_sid_avian(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testloc_sid_avian_in(self):
        out_fun_loc_sid_avian.append(self.stir_obj.loc_sid_avian)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("loc_sid_avian",self.stir_obj.loc_sid_avian,fun)
        self.assertEqual(round(fun,3),round(self.loc_sid_avian,3),testFailureMessage)

class TestCase_loc_vid_mammal(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testloc_vid_mammal_in(self):
        out_fun_loc_vid_mammal.append(self.stir_obj.loc_vid_mammal)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("loc_vid_mammal",self.stir_obj.loc_vid_mammal,fun)
        self.assertEqual(round(fun,3),round(self.loc_vid_mammal,3),testFailureMessage)

class TestCase_loc_sid_mammal(unittest.TestCase):
    def setUp(self):
        self.stir_obj = stir_object_in
    def testloc_sid_mammal_in(self):
        out_fun_loc_sid_mammal.append(self.stir_obj.loc_sid_mammal)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("loc_sid_mammal",self.stir_obj.loc_sid_mammal,fun)
        self.assertEqual(round(fun,3),round(self.loc_sid_mammal,3),testFailureMessage)

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

stir_obj = stir_model.StirModel(True,True,'',application_rate[0],column_height[0],spray_drift_fraction[0],direct_spray_duration[0],molecular_weight[0],vapor_pressure[0],avian_oral_ld50[0], body_weight_assessed_bird[0], body_weight_tested_bird[0],mineau_scaling_factor[0],mammal_inhalation_lc50[0],duration_mammal_inhalation_study[0],body_weight_assessed_mammal[0],body_weight_tested_mammal[0],mammal_oral_ld50[0])
stir_obj.set_unit_testing_variables()

stir_obj.chemical_name_expected = chemical_name[0]
stir_obj.sat_air_conc_expected = sat_air_conc[0]
stir_obj.inh_rate_avian_expected = inh_rate_avian[0]
stir_obj.vid_avian_expected = vid_avian[0]
stir_obj.inh_rate_mammal_expected = inh_rate_mammal[0]
stir_obj.vid_mammal_expected = vid_mammal[0]
stir_obj.ar2_expected = ar2[0]
stir_obj.air_conc_expected = air_conc[0]
stir_obj.sid_avian_expected = sid_avian[0]
stir_obj.sid_mammal_expected = sid_mammal[0]
stir_obj.cf_expected = cf[0]
stir_obj.mammal_inhalation_ld50_expected = mammal_inhalation_ld50[0]
stir_obj.adjusted_mammal_inhalation_ld50_expected = adjusted_mammal_inhalation_ld50[0]
stir_obj.estimated_avian_inhalation_ld50_expected = estimated_avian_inhalation_ld50[0]
stir_obj.adjusted_avian_inhalation_ld50_expected = adjusted_avian_inhalation_ld50[0]
stir_obj.ratio_vid_avian_expected = ratio_vid_avian[0]
stir_obj.ratio_sid_avian_expected = ratio_sid_avian[0]
stir_obj.ratio_vid_mammal_expected = ratio_vid_mammal[0]
stir_obj.ratio_sid_mammal_expected = ratio_sid_mammal[0]
stir_obj.loc_vid_avian_expected = loc_vid_avian[0]
stir_obj.loc_sid_avian_expected = loc_sid_avian[0]
stir_obj.loc_vid_mammal_expected = loc_vid_mammal[0]
stir_obj.loc_sid_mammal_expected = loc_sid_mammal[0]

test_suite_sat_air_conc = suite(TestCase_sat_air_conc, stir_obj=stir_obj)
test_suite_inh_rate_avian = suite(TestCase_inh_rate_avian, stir_obj=stir_obj)
test_suite_vid_avian = suite(TestCase_vid_avian, stir_obj=stir_obj)
test_suite_inh_rate_mammal = suite(TestCase_inh_rate_mammal, stir_obj=stir_obj)
test_suite_vid_mammal = suite(TestCase_vid_mammal, stir_obj=stir_obj)
test_suite_ar2 = suite(TestCase_ar2, stir_obj=stir_obj)
test_suite_air_conc = suite(TestCase_air_conc, stir_obj=stir_obj)
test_suite_sid_avian = suite(TestCase_sid_avian, stir_obj=stir_obj)
test_suite_sid_mammal = suite(TestCase_sid_mammal, stir_obj=stir_obj)
test_suite_cf = suite(TestCase_cf, stir_obj=stir_obj)
test_suite_mammal_inhalation_ld50 = suite(TestCase_mammal_inhalation_ld50, stir_obj=stir_obj)
test_suite_adjusted_mammal_inhalation_ld50 = suite(TestCase_adjusted_mammal_inhalation_ld50, stir_obj=stir_obj)
test_suite_estimated_avian_inhalation_ld50 = suite(TestCase_estimated_avian_inhalation_ld50, stir_obj=stir_obj)
test_suite_adjusted_avian_inhalation_ld50 = suite(TestCase_adjusted_avian_inhalation_ld50, stir_obj=stir_obj)
test_suite_ratio_vid_avian = suite(TestCase_ratio_vid_avian, stir_obj=stir_obj)
test_suite_ratio_sid_avian = suite(TestCase_ratio_sid_avian, stir_obj=stir_obj)
test_suite_ratio_vid_mammal = suite(TestCase_ratio_vid_mammal, stir_obj=stir_obj)
test_suite_ratio_sid_mammal = suite(TestCase_ratio_sid_mammal, stir_obj=stir_obj)
test_suite_loc_vid_avian = suite(TestCase_loc_vid_avian, stir_obj=stir_obj)
test_suite_loc_sid_avian = suite(TestCase_loc_sid_avian, stir_obj=stir_obj)
test_suite_loc_vid_mammal = suite(TestCase_loc_vid_mammal, stir_obj=stir_obj)
test_suite_loc_sid_mammal = suite(TestCase_loc_sid_mammal, stir_obj=stir_obj)


class stirQaqcPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "STIR QA/QC")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'stir','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'stir',
                'model_attributes':'STIR QAQC'})

        pvuheadings = stir_tables.getheaderpvu()
        pvuheadingsqaqc = stir_tables.getheaderpvuqaqc()
        pvrheadings = stir_tables.getheaderpvr()
        pvrheadingsqaqc = stir_tables.getheaderpvrqaqc()
        djtemplate = stir_tables.getdjtemplate()
        tmpl = Template(djtemplate)
        
        #instantiate stir model object
        # sm = stir_model.StirModel(True,True,chemical_name,application_rate,column_height,spray_drift_fraction,direct_spray_duration, 
        #     molecular_weight,vapor_pressure,avian_oral_ld50, body_weight_assessed_bird, body_weight_tested_bird, mineau_scaling_factor, 
        #     mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal, body_weight_tested_mammal, 
        #     mammal_oral_ld50)

        html = html + stir_tables.timestamp()
        html = html + stir_tables.table_1qaqc(pvuheadings,tmpl,stir_obj)
        html = html + stir_tables.table_2(pvuheadings,tmpl,stir_obj)
        html = html + stir_tables.table_3qaqc(pvuheadingsqaqc,tmpl,stir_obj)
        html = html + stir_tables.table_4qaqc(pvuheadingsqaqc,tmpl,stir_obj)
        html = html + stir_tables.table_5qaqc(pvrheadingsqaqc,tmpl,stir_obj)

        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', stirQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
