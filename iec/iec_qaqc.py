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
sys.path.append("../iec")
from iec import iec_model,iec_tables
from uber import uber_lib
import rest_funcs
import logging

logger = logging.getLogger('IECQaqcPage')

cwd= os.getcwd()
data = csv.reader(open(cwd+'/iec/iec_unittest_inputs.csv'))
LC50=[]
threshold=[]
dose_response=[]

#####Pre-defined outputs########
z_score_f_out=[]
F8_f_out=[]
chance_f_out=[]

data.next()
for row in data:
    LC50.append(float(row[0]))
    threshold.append(float(row[1]))  
    dose_response.append(float(row[2]))
    z_score_f_out.append(float(row[3])) 
    F8_f_out.append(float(row[4]))
    chance_f_out.append(float(row[5]))
    
out_fun_z_score_f=[]
out_fun_F8_f=[]
out_fun_chance_f=[]

def set_globals(**kwargs):
    for argname in kwargs:
        globals()['%s_in' % argname] = kwargs[argname]
           
class TestCase_z_score_f_out(unittest.TestCase):
    def setUp(self):
        self.iec_obj = iec_object_in
    def testz_score_f_out_in(self):
        out_fun_z_score_f.append(self.iec_obj.z_score_f_out)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("Z_score_f",self.iec_obj.z_score_f_out,fun)
        self.assertEqual(round(fun,3),round(self.z_score_f_out,3),testFailureMessage)

class TestCase_F8_f_out(unittest.TestCase):
    def setUp(self):
        self.iec_obj = iec_object_in
    def testF8_f_out_in(self):
        out_fun_F8_f.append(self.iec_obj.F8_f_out)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("F8_f",self.iec_obj.F8_f_out,fun)
        self.assertEqual(round(fun,3),round(self.F8_f_out,3),testFailureMessage)
            
class TestCase_chance_f_out(unittest.TestCase):
    def setUp(self):
        self.iec_obj = iec_object_in
    def testchance_f_out_in(self):
        out_fun_chance_f.append(self.iec_obj.chance_f_out)
        testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("Chance_f",self.iec_obj.chance_f_out,fun)
        self.assertEqual(round(fun,3),round(self.chance_f_out,3),testFailureMessage)
                        
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

iec_obj = iec_model.iec(True,True,dose_response[0],LC50[0],threshold[0])
iec_obj.set_unit_testing_variables()

iec_obj.z_score_f_out_expected = z_score_f_out[0]
iec_obj.F8_f_out_expected = F8_f_out[0]
iec_obj.chance_f_out_expected = chance_f_out[0]

test_suite_z_score_f_out = suite(TestCase_z_score_f_out, iec_obj=iec_obj)
test_suite_F8_f_out = suite(TestCase_F8_f_out, iec_obj=iec_obj)
test_suite_chance_f_out = suite(TestCase_chance_f_out, iec_obj=iec_obj)

                
class IecQaqcPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('iec/iec_description.txt','r')
        x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "IEC QA/QC")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'iec','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'iec',
                'model_attributes':'IEC QAQC'})
       # html = html + iec_tables.timestamp()
        html = html + iec_tables.table_all_qaqc(iec_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', IecQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
