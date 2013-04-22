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
from dust import dust_tables
import csv
import numpy

chemical_name=[]
label_epa_reg_no=[]
ar_lb=[]
frac_pest_surface=[]
dislodge_fol_res=[]
bird_acute_oral_study=[]
bird_study_add_comm=[]
low_bird_acute_ld50=[]
test_bird_bw=[]
mineau=[]
mamm_acute_derm_study=[]
mamm_study_add_comm=[]
mam_acute_derm_ld50=[]
test_mam_bw=[]

######Pre-defined outputs########
mai1_out=[]
cw_out=[]

def html_table(row_inp,iter):
    chemical_name_temp=row_inp[0]
    chemical_name.append(chemical_name_temp)
    label_epa_reg_no_temp=row_inp[1]
    label_epa_reg_no.append(label_epa_reg_no_temp)  
    ar_lb_temp=float(row_inp[3])
    ar_lb.append(ar_lb_temp)
    frac_pest_surface_temp=float(row_inp[4])
    frac_pest_surface.append(frac_pest_surface_temp)
    dislodge_fol_res_temp=float(row_inp[5])
    dislodge_fol_res.append(dislodge_fol_res_temp)
    bird_acute_oral_study_temp=row_inp[6]
    bird_acute_oral_study.append(bird_acute_oral_study_temp)
    bird_study_add_comm_temp=row_inp[7]
    bird_study_add_comm.append(bird_study_add_comm_temp)
    low_bird_acute_ld50_temp=float(row_inp[8])   
    low_bird_acute_ld50.append(low_bird_acute_ld50_temp)
    test_bird_bw_temp=float(row_inp[9])   
    test_bird_bw.append(test_bird_bw_temp)
    mineau_temp=float(row_inp[10])   
    mineau.append(mineau_temp)
    mamm_acute_derm_study_temp=row_inp[11]
    mamm_acute_derm_study.append(mamm_acute_derm_study_temp)
    mamm_study_add_comm_temp=row_inp[12]
    mamm_study_add_comm.append(mamm_study_add_comm_temp)
    mam_acute_derm_ld50_temp=float(row_inp[13])   
    mam_acute_derm_ld50.append(mam_acute_derm_ld50_temp)
    test_mam_bw_temp=float(row_inp[14])   
    test_mam_bw.append(test_mam_bw_temp)

    Input_header="""<table border="1">
                        <tr><H3>Batch Calculation of Iteration %s</H3></tr><br>
                    </table>"""%(iter)

    html_table_temp = Input_header + dust_tables.table_all(dust_tables.pvuheadings, dust_tables.pvrheadings, dust_tables.tmpl, chemical_name_temp, label_epa_reg_no_temp, ar_lb_temp, frac_pest_surface_temp, 
                                            dislodge_fol_res_temp, bird_acute_oral_study_temp, bird_study_add_comm_temp, low_bird_acute_ld50_temp, test_bird_bw_temp, mineau_temp, 
                                            mamm_acute_derm_study_temp, mamm_study_add_comm_temp, mam_acute_derm_ld50_temp, test_mam_bw_temp)


    return html_table_temp  
                
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()

    i=1
    iter_html=""
    for row in reader:
        iter_html = iter_html +html_table(row,i)
        i=i+1

    sum_html = dust_tables.table_sum_input(dust_tables.sumheadings, dust_tables.tmpl, i, ar_lb, frac_pest_surface, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw)

    # sum_html ="""<table border="1">
    #                     <tr><H3>Summary Statistics (Iterations=%s)</H3></tr><br>
    #                     <tr>
    #                         <td><b>Input Name</b></td>
    #                         <td><b>Mean</b></td>
    #                         <td><b>Std.</b></td>
    #                         <td><b>Min</b></td>
    #                         <td><b>Max</b></td>                            
    #                         <td><b>Unit</b></td>
    #                     </tr>"""%(i-1)
                        
    # sum_html = sum_html + """<tr>
    #                 <td>Maximum Single Application Rate</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>
    #                 <td>%5.2f</td>                    
    #                 <td>lbs a.i./A</td>
    #             </tr>""" %(numpy.mean(ar_lb), numpy.std(ar_lb), numpy.min(ar_lb), numpy.max(ar_lb)) 













 
                
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
    # sum_output_cw="""<tr>
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
    return sum_html+iter_html



              
class DustBatchOutputPage(webapp.RequestHandler):
    def post(self):
        text_file1 = open('rice/rice_description.txt','r')
        x = text_file1.read()
        form = cgi.FieldStorage()
        thefile = form['upfile']

        iter_html=loop_html(thefile)        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'rice','page':'batchinput'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {})
        html = html + iter_html
        html = html + template.render(templatepath + 'rice-batchoutput-jqplot.html', {})                
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', DustBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

