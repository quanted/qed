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
sys.path.append("../earthworm")
from earthworm import earthworm_model,earthworm_tables
from uber import uber_lib
import csv
import numpy

######Pre-defined inputs########
Kow=[]
L=[]
Cs=[]
Kd=[]
Ps=[]
Cw=[]
MW=[]
Pe=[]

######Pre-defined outputs########
Ce_out=[]

logger = logging.getLogger("earthwormBatchOutput")

def html_table(row_inp,iter):
    Kow_temp=float(row_inp[0])
    Kow.append(Kow_temp)
    L_temp=float(row_inp[1])
    L.append(L_temp)
    Cs_temp=float(row_inp[2])
    Cs.append(Cs_temp)
    Kd_temp=float(row_inp[3])
    Kd.append(Kd_temp)
    Ps_temp=float(row_inp[4])
    Ps.append(Ps_temp)
    Cw_temp=float(row_inp[5])        
    Cw.append(Cw_temp)
    MW_temp=float(row_inp[6])   
    MW.append(MW_temp)
    Pe_temp=float(row_inp[7])
    Pe.append(Pe_temp)
    
    earth = earthworm_model.earthworm(True,True,Kow_temp,L_temp,Cs_temp,Kd_temp,Ps_temp,Cw_temp,MW_temp,Pe_temp)
    Ce_temp=earth.earthworm_fugacity_out
    Ce_out.append(Ce_temp)

    html = earthworm_tables.table_all_batch(earthworm_tables.pvuheadings,earthworm_tables.sumheadings,earthworm_tables.tmpl, earth)
    
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

    sum_html = earthworm_tables.table_all_sum(earthworm_tables.sumheadings, earthworm_tables.tmpl, Kow, L, Cs, Kd, Ps, Cw, MW, Pe, 
                    Ce_out)
    
    return sum_html + iter_html



class earthwormBatchOutputPage(webapp.RequestHandler):
    def post(self):
        text_file1 = open('earthworm/earthworm_description.txt','r')
        x = text_file1.read()
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['file-0']
        iter_html=loop_html(thefile)        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        # ChkCookie = self.request.cookies.get("ubercookie")
        # html = uber_lib.SkinChk(ChkCookie)
        # html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'earthworm','page':'batchinput'})
        # html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = template.render(templatepath + '04uberbatch_start.html', {
                'model':'earthworm',
                'model_attributes':'earthworm Batch Output'})
        html = html + earthworm_tables.timestamp()
        html = html + iter_html
        # html = html + template.render(templatepath + 'earthworm-batchoutput-jqplot.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        # html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', earthwormBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

