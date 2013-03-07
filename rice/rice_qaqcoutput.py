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
from rice import rice_output
from pprint import pprint
import csv

dsed=[]
a=[]
pb=[]
dw=[]
osed=[]
mai=[]
kd=[]
######Pre-defined outputs########
msed_out=[]
vw_out=[]
mai1_out=[]
cw_out=[]

form = cgi.FieldStorage() 
thefile = form['upfile']
reader = csv.reader(thefile.file)
header = reader.next()

for row in reader:
    dsed.append(float(row[0]))
    a.append(float(row[1]))  
    pb.append(float(row[2]))
    dw.append(float(row[3]))
    osed.append(float(row[4]))        
    mai.append(float(row[5]))    
    kd.append(float(row[6]))    
    msed_out.append(float(row[7]))
    vw_out.append(float(row[8]))
    mai1_out.append(float(row[9]))
    cw_out.append(float(row[10]))
    
out_fun_Msed=[]
out_fun_Vw=[]
out_fun_Mai1=[]            
out_fun_Cw=[]      


def set_globals(**kwargs):
    for argname in kwargs:
        globals()['%s_in' % argname] = kwargs[argname]
           
class TestCase_Msed(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.dsed_in=dsed_in
        self.a_in=a_in
        self.pb_in=pb_in
        #####Pre-defined outputs########
        self.msed_out_in=msed_out_in
    def testMsed(self):
            fun = rice_output.msed(self.dsed_in,self.a_in,self.pb_in)
            out_fun_Msed.append(fun)
            testFailureMessage = "Test of function name: %s expected: %i != calculated: %i" % ("msed",self.msed_out_in,fun)
            self.assertEqual(round(fun,3),round(self.msed_out_in,3),testFailureMessage)

class TestCase_Vw(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.dw_in=dw_in       
        self.a_in=a_in
        self.dsed_in=dsed_in
        self.osed_in=osed_in       
        #####Pre-defined outputs########
        self.vw_out_in=vw_out_in
    def testVw(self):
            fun = rice_output.vw(self.dw_in,self.a_in,self.dsed_in,self.osed_in)
            out_fun_Vw.append(fun)
            testFailureMessage = "Test of function name: %s expected: %i != calculated: %i" % ("vw",self.vw_out_in,fun)
            self.assertEqual(round(fun,3),round(self.vw_out_in,3),testFailureMessage)
            
class TestCase_Mai1(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.mai_in=mai_in       
        self.a_in=a_in     
        #####Pre-defined outputs########
        self.mai1_out_in=mai1_out_in
    def testMai1(self):
            fun = rice_output.mai1(self.mai_in,self.a_in)
            out_fun_Mai1.append(fun)
            testFailureMessage = "Test of function name: %s expected: %i != calculated: %i" % ("mai1",self.mai1_out_in,fun)
            self.assertEqual(round(fun,3),round(self.mai1_out_in,3),testFailureMessage)

class TestCase_Cw(unittest.TestCase):
    def setUp(self):
        #####Pre-defined inputs########
        self.dsed_in=dsed_in
        self.pb_in=pb_in
        self.dw_in=dw_in
        self.osed_in=osed_in
        self.mai_in=mai_in
        self.kd_in=kd_in
        self.a_in=a_in
        #####Pre-defined outputs########
        self.cw_out_in=cw_out_in
    def testCw(self):
            fun = rice_output.cw(rice_output.mai1(self.mai_in,self.a_in),self.dw_in,self.dsed_in,self.osed_in,self.pb_in,self.kd_in)
            out_fun_Cw.append(fun)
            testFailureMessage = "Test of function name: %s expected: %d != calculated: %d" % ("cw",self.cw_out_in,fun)
            self.assertEqual(round(fun,3),round(self.cw_out_in,3),testFailureMessage)
                        
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

test_suite_msed_1 = suite(TestCase_Msed, dsed=dsed[0], a=a[0], pb=pb[0], msed_out=msed_out[0])
test_suite_msed_2 = suite(TestCase_Msed, dsed=dsed[1], a=a[1], pb=pb[1], msed_out=msed_out[1])
test_suite_vw_1 = suite(TestCase_Vw, dw=dw[0], a=a[0], dsed=dsed[0], osed=osed[0], vw_out=vw_out[0])
test_suite_vw_2 = suite(TestCase_Vw, dw=dw[1], a=a[1], dsed=dsed[1], osed=osed[1], vw_out=vw_out[1])
test_suite_mai1_1 = suite(TestCase_Mai1, mai=mai[0], a=a[0], mai1_out=mai1_out[0])
test_suite_mai1_2 = suite(TestCase_Mai1, mai=mai[1], a=a[1], mai1_out=mai1_out[1])
test_suite_cw_1 = suite(TestCase_Cw, mai=mai[0], a=a[0], dw=dw[0], dsed=dsed[0], osed=osed[0], pb=pb[0], kd=kd[0], cw_out=cw_out[0])
test_suite_cw_2 = suite(TestCase_Cw, mai=mai[1], a=a[1], dw=dw[1], dsed=dsed[1], osed=osed[1], pb=pb[1], kd=kd[1], cw_out=cw_out[1])


                
class RiceQaqcOutputPage(webapp.RequestHandler):
    def post(self):
        text_file1 = open('rice/rice_description.txt','r')
        x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'rice','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {'model':'rice'})
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
        <td>Mass of Applied Ingredient Applied to Paddy</td>
        <td>%s</td>
        <td>%s</td>        
        <td>kg</td>
        </tr>
        <tr>
        <td>Sediment Depth</td>
        <td>%s</td>
        <td>%s</td>        
        <td>m</td>
        </tr>
        <tr>
        <td>Area of the Rice Paddy</td>
        <td>%s</td>
        <td>%s</td>        
        <td>m<sup>2</sup></td>
        </tr>
        <tr>
        <td>Bulk Density of Sediment</td>
        <td>%s</td>
        <td>%s</td>        
        <td>kg/m<sup>3</sup></td>
        </tr>
        <tr>
        <td>Water Column Depth</td>
        <td>%s</td>
        <td>%s</td>        
        <td>m</td>
        </tr>
        <tr>
        <td>Porosity of Sediment</td>
        <td>%s</td>
        <td>%s</td>        
        <td>-</td>
        </tr>
        <tr>
        <td>Water-Sediment Partitioning Coefficient</td>
        <td>%s</td>
        <td>%s</td>        
        <td>L/kg</td>
        </table>
        """  % (mai[0], mai[1], dsed[0], dsed[1], a[0], a[1], 
               pb[0], pb[1], dw[0], dw[1], osed[0], osed[1], kd[0], kd[1])      
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
                <td>Msed</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>
            <tr>
                <td>Msed</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>   
            <tr>
                <td>Vw</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>        
            <tr>
                <td>Vw</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>         
            <tr>
                <td>Mai1</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>         
            <tr>
                <td>Mai1</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>         
            <tr>
                <td>Cw</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>         
            <tr>
                <td>Cw</td>
                <td>%s</td>        
                <td>%s</td>
                <td><div style="word-wrap: break-word; width:40em">%s</div></td> 
            </tr>         
        </table>
        """ % (out_fun_Msed[0],msed_out[0],test_suite_msed_1,out_fun_Msed[1],msed_out[1],test_suite_msed_2,
               out_fun_Vw[0],vw_out[0],test_suite_vw_1,out_fun_Vw[1],vw_out[1],test_suite_vw_2,
               out_fun_Mai1[0],mai1_out[0],test_suite_mai1_1,out_fun_Mai1[1],mai1_out[1],test_suite_mai1_2,
               out_fun_Cw[0],cw_out[0],test_suite_cw_1,out_fun_Cw[1],cw_out[1],test_suite_cw_2)
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', RiceQaqcOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

