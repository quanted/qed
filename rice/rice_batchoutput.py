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
sys.path.append("../rice")
from rice import rice_model,rice_tables
import csv
from uber import uber_lib

logger = logging.getLogger("RiceBatchPage")

chemical_name=[]
mai=[]
a=[]
dsed=[]
pb=[]
dw=[]
osed=[]
kd=[]

######Pre-defined outputs########
msed=[]
vw=[]
mai1=[]
cw=[]

logger = logging.getLogger("RiceBatchOutput")


def html_table(row_inp,iter):
    logger.info("iteration: " + str(iter))
    chemical_name.append(str(row_inp[0]))
    mai.append(float(row_inp[1]))
    a.append(float(row_inp[2]))  
    dsed.append(float(row_inp[3]))
    pb.append(float(row_inp[4]))
    dw.append(float(row_inp[5]))
    osed.append(float(row_inp[6]))        
    kd.append(float(row_inp[7]))    
    # msed.append(float(row_inp[8]))
    # vw.append(float(row_inp[9]))
    # mai1.append(float(row_inp[10]))
    # cw.append(float(row_inp[11])) 
    
    logger.info(chemical_name)
    logger.info(mai)
    logger.info(a)
    logger.info(dsed)
    logger.info(pb)
    logger.info(dw)
    logger.info(osed)
    logger.info(kd)
    logger.info(msed)
    logger.info(vw)
    logger.info(mai1)
    logger.info(cw)

    rice_obj = rice_model.rice(True,True,chemical_name[iter], mai[iter], dsed[iter], a[iter], pb[iter], dw[iter], osed[iter], kd[iter])

    msed.append(rice_obj.msed)
    vw.append(rice_obj.vw)
    mai1.append(rice_obj.mai1)
    cw.append(rice_obj.cw)

    html = rice_tables.table_all(rice_obj)

    return html


    # Input_header="""<table border="1">
    #                     <tr><H3>Batch Calculation of Iteration %s</H3></tr><br>
    #                     <tr>
    #                         <td><b>Input Name</b></td>
    #                         <td><b>Input value</b></td>
    #                         <td><b>Unit</b></td>
    #                     </tr>"""%(iter)
    # Input_mai="""<tr>
    #                 <td>Mass of Applied Ingredient Applied to Paddy</td>
    #                 <td>%s</td>
    #                 <td>kg</td>
    #             </tr>""" %(mai_temp) 
    # Input_dsed="""<tr>
    #                 <td>Sediment Depth</td>
    #                 <td>%s</td>
    #                 <td>m</td>
    #             </tr>""" %(dsed_temp)                         
    # Input_a="""<tr>
    #                 <td>Area of the Rice Paddy</td>
    #                 <td>%s</td>
    #                 <td>m<sup>2</sup></td>
    #             </tr>""" %(a_temp)                          
    # Input_pb="""<tr>
    #                 <td>Bulk Density of Sediment</td>
    #                 <td>%s</td>
    #                 <td>kg/m<sup>3</sup></td>
    #             </tr>""" %(pb_temp)  
    # Input_dw="""<tr>
    #                 <td>Water Column Depth</td>
    #                 <td>%s</td>
    #                 <td>m</td>
    #             </tr>""" %(dw_temp) 
    # Input_osed="""<tr>
    #                 <td>Porosity of Sediment</td>
    #                 <td>%s</td>
    #                 <td>-</td>
    #             </tr>""" %(osed_temp)                        
    # Input_kd="""<tr>
    #                 <td>Water-Sediment Partitioning Coefficient</td>
    #                 <td>%s</td>
    #                 <td>L/kg</td>
    #             </tr></table><br>""" %(kd_temp)  

    # Output_header="""<table border="1">
    #                     <tr>
    #                         <td><b>Output Name</b></td>
    #                         <td><b>Output value</b></td>
    #                         <td><b>Unit</b></td>
    #                     </tr>"""
    # Output_mai1="""<tr>
    #                 <td>Application Rate</td>
    #                 <td>%0.2E</td>
    #                 <td>kg a.i./A</td>
    #             </tr>""" %(mai1_temp)
    # Output_cw="""<tr>
    #                 <td>Peak & Chronic EEC</td>
    #                 <td>%0.2E</td>
    #                 <td>&microg/L</td>
    #             </tr></table><br>""" %(cw_temp)
                                                                                  
    # Inout_table = Input_header+Input_mai+Input_dsed+Input_a+Input_pb+Input_dw+Input_osed+Input_kd+Output_header+Output_mai1+Output_cw  
               
    # return Inout_table  
                
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    logger.info(header)
    i=0
    iter_html=""
    for row in reader:
        iter_html = iter_html +html_table(row,i)
        i=i+1

    sum_output_cw="""<table border="1" style="display: none"><tr>
                    <td id="cw_out_raw" data-val='%s' style="display: none"></td>                                                                              
                    <td>&microg/L</td>
                </tr></table><br>""" %(cw)             
    sum_fig="""<H3>Historgram</H3><br>
               <div id="calculate">
                   <div class="block">
                        <label>How many buckets (Default is based on Sturgis rule):</label>
                        <input type="text" id="buckets" value=%s></div><br>
                        <button type="submit" id="calc">Calculate Historgram</button></div><br>
                <div id="chart1"></div><br>"""%(int(1+3.3*np.log10(len(cw)))) #number of bins coming from Sturgis rule         
                                     

    sum_html = rice_tables.table_sum_all(rice_tables.sumheadings, rice_tables.tmpl, mai, dsed, a, pb, dw, osed, kd, msed, vw, mai1, cw)

    return sum_html+sum_output_cw+sum_fig+iter_html

    # sum_header ="""<table border="1">
    #                     <tr><H3>Summary Statistics (Iterations=%s)</H3></tr><br>
    #                     <tr>
    #                         <td><b>Input Name</b></td>
    #                         <td><b>Mean</b></td>
    #                         <td><b>Std.</b></td>
    #                         <td><b>Min</b></td>
    #                         <td><b>Max</b></td>                            
    #                         <td><b>Unit</b></td>
    #                     </tr>"""%(i-1)
                        
    # sum_mai="""<tr>
    #                 <td>Mass of Applied Ingredient Applied to Paddy</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>                    
    #                 <td>kg</td>
    #             </tr>""" %(numpy.mean(mai), numpy.std(mai), numpy.min(mai), numpy.max(mai)) 
    # sum_dsed="""<tr>
    #                 <td>Sediment Depth</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>   
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>                                       
    #                 <td>m</td>
    #             </tr>""" %(numpy.mean(dsed), numpy.std(dsed), numpy.min(dsed), numpy.max(dsed))                         
    # sum_a="""<tr>
    #                 <td>Area of the Rice Paddy</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td> 
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>                                        
    #                 <td>m<sup>2</sup></td>
    #             </tr>""" %(numpy.mean(a), numpy.std(a), numpy.min(a), numpy.max(a))                          
    # sum_pb="""<tr>
    #                 <td>Bulk Density of Sediment</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>                                          
    #                 <td>kg/m<sup>3</sup></td>
    #             </tr>""" %(numpy.mean(pb), numpy.std(pb), numpy.min(pb), numpy.max(pb))  
    # sum_dw="""<tr>
    #                 <td>Water Column Depth</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td> 
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>                                     
    #                 <td>m</td>
    #             </tr>""" %(numpy.mean(dw), numpy.std(dw), numpy.min(dw), numpy.max(dw)) 
    # sum_osed="""<tr>
    #                 <td>Porosity of Sediment</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>  
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>                                        
    #                 <td>-</td>
    #             </tr>""" %(numpy.mean(osed), numpy.std(osed), numpy.min(osed), numpy.max(osed))                        
    # sum_kd="""<tr>
    #                 <td>Water-Sediment Partitioning Coefficient</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>                                          
    #                 <td>L/kg</td>
    #             </tr></table><br>""" %(numpy.mean(kd), numpy.std(kd), numpy.min(kd), numpy.max(kd))  
                
    # sum_output_header="""<table border="1">
    #                     <tr>
    #                         <td><b>Output Name</b></td>
    #                         <td><b>Mean</b></td>
    #                         <td><b>Std.</b></td>
    #                         <td><b>Min</b></td>
    #                         <td><b>Max</b></td>                             
    #                         <td><b>Unit</b></td>
    #                     </tr>"""
    # sum_output_mai1="""<tr>
    #                 <td>Application Rate</td>
    #                 <td>%0.2E</td>
    #                 <td>%0.2E</td>
    #                 <td>%0.2E</td>
    #                 <td>%0.2E</td>                      
    #                 <td>lbs a.i./A</td>
    #             </tr>""" %(numpy.mean(mai1_out), numpy.std(mai1_out), numpy.min(mai1_out), numpy.max(mai1_out))
    # sum_output_cw="""<table border="1" style="display: none"><tr>
    #                 <td>Peak & Chronic EEC</td>
    #                 <td>%0.2E</td>
    #                 <td>%0.2E</td> 
    #                 <td>%0.2E</td>
    #                 <td>%0.2E</td>                      
    #                 <td id="cw_out_raw" data-val='%s' style="display: none"></td>                                                                              
    #                 <td>&microg/L</td>
    #             </tr></table><br>""" %(numpy.mean(cw_out), numpy.std(cw_out), numpy.min(cw_out), numpy.max(cw_out), cw_out)             
    # sum_fig="""<H3>Historgram</H3><br>
    #            <div id="calculate">
    #                <div class="block">
    #                     <label>How many buckets (Default is based on Sturgis rule):</label>
    #                     <input type="text" id="buckets" value=%s></div><br>
    #                     <button type="submit" id="calc">Calculate Historgram</button></div><br>
    #             <div id="chart1"></div><br>"""%(int(1+3.3*np.log10(len(cw_out)))) #number of bins coming from Sturgis rule         
                                     
    # sum_html=sum_header+sum_mai+sum_dsed+sum_a+sum_pb+sum_dw+sum_osed+sum_kd+sum_output_header+sum_output_mai1+sum_output_cw+sum_fig    
    # return sum_html+iter_html



              
class RiceBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['file-0']
        iter_html=loop_html(thefile)        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        # html = uber_lib.SkinChk(ChkCookie)
        # html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'rice','page':'batchinput'})
        # html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = template.render(templatepath + '04uberbatch_start.html', {
                'model':'rice',
                'model_attributes':'Rice Model Batch Output'})
        html = html + rice_tables.timestamp()
        html = html + iter_html
        html = html + template.render(templatepath + 'rice-batchoutput-jqplot.html', {})
        html = html + template.render(templatepath + 'export.html', {})            
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        # html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', RiceBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

