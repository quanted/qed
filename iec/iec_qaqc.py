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
from iec import iec_model
from pprint import pprint
import csv

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
           
class TestCase_Z_score_f(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.LC50_in=LC50_in
        self.threshold_in=threshold_in
        self.dose_response_in=dose_response_in
        #####Pre-defined outputs########
        self.z_score_f_out_in=z_score_f_out_in
    def testIec(self):
            fun = iec_output.z_score_f(self.dose_response_in,self.LC50_in,self.threshold_in)
            out_fun_z_score_f.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("Z_score_f",self.z_score_f_out_in,fun)
            self.assertEqual(round(fun,3),round(self.z_score_f_out_in,3),testFailureMessage)

class TestCase_F8_f(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.LC50_in=LC50_in
        self.threshold_in=threshold_in
        self.dose_response_in=dose_response_in
        #####Pre-defined outputs########
        self.F8_f_out_in=F8_f_out_in
    def testF8_f(self):
            fun = iec_output.F8_f(self.dose_response_in,self.LC50_in,self.threshold_in)
            out_fun_F8_f.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("F8_f",self.F8_f_out_in,fun)
            self.assertEqual(round(fun,3),round(self.F8_f_out_in,3),testFailureMessage)
            
class TestCase_chance_f(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.LC50_in=LC50_in
        self.threshold_in=threshold_in
        self.dose_response_in=dose_response_in
        #####Pre-defined outputs########
        self.chance_f_out_in=chance_f_out_in
    def testchance_f(self):
            fun = iec_output.chance_f(self.dose_response_in,self.LC50_in,self.threshold_in)
            out_fun_chance_f.append(fun)
            testFailureMessage = "Test of function name: %s expected: %s != calculated: %s" % ("Chance_f",self.chance_f_out_in,fun)
            self.assertEqual(round(fun,3),round(self.chance_f_out_in,3),testFailureMessage)
                        
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

test_suite_z_score_f_1 = suite(TestCase_Z_score_f, LC50=LC50[0], threshold=threshold[0], dose_response=dose_response[0], z_score_f_out=z_score_f_out[0])
test_suite_z_score_f_2 = suite(TestCase_Z_score_f, LC50=LC50[1], threshold=threshold[1], dose_response=dose_response[1], z_score_f_out=z_score_f_out[1])
test_suite_F8_f_1 = suite(TestCase_F8_f, LC50=LC50[0], threshold=threshold[0], dose_response=dose_response[0], F8_f_out=F8_f_out[0])
test_suite_F8_f_2 = suite(TestCase_F8_f, LC50=LC50[1], threshold=threshold[1], dose_response=dose_response[1], F8_f_out=F8_f_out[1])
test_suite_chance_f_1 = suite(TestCase_chance_f, LC50=LC50[0], threshold=threshold[0], dose_response=dose_response[0], chance_f_out=chance_f_out[0])
test_suite_chance_f_2 = suite(TestCase_chance_f, LC50=LC50[1], threshold=threshold[1], dose_response=dose_response[1], chance_f_out=chance_f_out[1])

                
class IecQaqcPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('iec/iec_description.txt','r')
        x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'iec','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'iec',
                'model_attributes':'IEC QAQC'})
        html = html + """
        <table border="1">
        <tr><H3>Model Validation Inputs</H3></tr><br>
        <tr>
        <td>Input Name</td>
        <td>Test value1</td>
        <td>Test value2</td>
        <td>Unit</td>
        </tr>      
        <tr>
        <td>LC<sub>50</sub>/LD<sub>50</sub></td>
        <td>%s</td>
        <td>%s</td>        
        <td>&nbsp</td>
        </tr>
        <tr>
        <td>Desired threshold</td>
        <td>%s</td>
        <td>%s</td>        
        <td>&nbsp</td>
        </tr>
        <tr>
        <td>Slope of does-response</td>
        <td>%s</td>
        <td>%s</td>        
        <td>&nbsp</td>
        </table>
        """  % (LC50[0], threshold[0], dose_response[0], LC50[1], threshold[1], dose_response[1])      
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
                <td>z_score_f</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>z_score_f</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>   
            <tr>
                <td>F8_f</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>        
            <tr>
                <td>F8_f</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>         
            <tr>
                <td>Chance_f</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>         
            <tr>
                <td>Chance_f</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>         
        </table>
        """ % (round(out_fun_z_score_f[0],3), round(z_score_f_out[0],3), test_suite_z_score_f_1, 
               round(out_fun_z_score_f[1],3), round(z_score_f_out[1],3), test_suite_z_score_f_2,
               round(out_fun_F8_f[0],3), round(F8_f_out[0],3), test_suite_F8_f_1, 
               round(out_fun_F8_f[1],3), round(F8_f_out[1],3), test_suite_F8_f_2,
               round(out_fun_chance_f[0],3), round(chance_f_out[0],3), test_suite_chance_f_1, 
               round(out_fun_chance_f[1],3), round(chance_f_out[1],3), test_suite_chance_f_2)
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', IecQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
