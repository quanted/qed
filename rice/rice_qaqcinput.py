import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from StringIO import StringIO
import csv

cwd= os.getcwd()
data = csv.reader(open(cwd+'/rice/rice_unittest_inputs.csv'))
dsed=[]
a=[]
pb=[]
dw=[]
osed=[]
mai=[]
kd=[]
#####Pre-defined outputs########
msed_out=[]
vw_out=[]
mai1_out=[]
cw_out=[]

data.next()
for row in data:
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
    
               
class RiceQaqcInputPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('rice/rice_description.txt','r')
        x = text_file1.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'rice','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberqaqcinput.html', {'model':'rice'})   
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', RiceQaqcInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    









