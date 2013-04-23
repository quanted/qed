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
granbirdderm_out=[]
granherpderm_out=[]
granmammderm_out=[]
folbirdderm_out=[]
folherpderm_out=[]
folmammderm_out=[]
barebirdderm_out=[]
bareherpderm_out=[]
baremammderm_out=[]
granbirdrisk_out=[]
granreprisk_out=[]
granamphibrisk_out=[]
granmammrisk_out=[]
granbirdrisk_out=[]
granreprisk_out=[]
granamphibrisk_out=[]
granmammrisk_out=[]
folbirdrisk_out=[]
folreprisk_out=[]
folamphibrisk_out=[]
folmammrisk_out=[]
barebirdrisk_out=[]
barereprisk_out=[]
bareamphibrisk_out=[]
baremammrisk_out=[]


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

    table_all_out = dust_tables.table_all(dust_tables.pvuheadings, dust_tables.pvrheadings, dust_tables.tmpl, chemical_name_temp, label_epa_reg_no_temp, ar_lb_temp, frac_pest_surface_temp, 
                                            dislodge_fol_res_temp, bird_acute_oral_study_temp, bird_study_add_comm_temp, low_bird_acute_ld50_temp, test_bird_bw_temp, mineau_temp, 
                                            mamm_acute_derm_study_temp, mamm_study_add_comm_temp, mam_acute_derm_ld50_temp, test_mam_bw_temp)

    html_table_temp = Input_header + table_all_out[0]

######table 3#######
    granbirdderm_out_temp=table_all_out[1]['granbirdderm']
    granbirdderm_out.append(granbirdderm_out_temp)
    granherpderm_out_temp=table_all_out[1]['granherpderm']
    granherpderm_out.append(granherpderm_out_temp)
    granmammderm_out_temp=table_all_out[1]['granmammderm']
    granmammderm_out.append(granmammderm_out_temp)

######table 4#######
    folbirdderm_out_temp=table_all_out[2]['folbirdderm']
    folbirdderm_out.append(folbirdderm_out_temp)
    folherpderm_out_temp=table_all_out[2]['folherpderm']
    folherpderm_out.append(folherpderm_out_temp)
    folmammderm_out_temp=table_all_out[2]['folmammderm']
    folmammderm_out.append(folmammderm_out_temp)

######table 5#######
    barebirdderm_out_temp=table_all_out[3]['barebirdderm']
    barebirdderm_out.append(barebirdderm_out_temp)
    bareherpderm_out_temp=table_all_out[3]['bareherpderm']
    bareherpderm_out.append(bareherpderm_out_temp)
    baremammderm_out_temp=table_all_out[3]['baremammderm']
    baremammderm_out.append(baremammderm_out_temp)

######table 6#######
    granbirdrisk_out_temp=table_all_out[4]['granbirdrisk']
    granbirdrisk_out.append(granbirdrisk_out_temp)
    granreprisk_out_temp=table_all_out[4]['granreprisk']
    granreprisk_out.append(granreprisk_out_temp)
    granamphibrisk_out_temp=table_all_out[4]['granamphibrisk']
    granamphibrisk_out.append(granamphibrisk_out_temp)
    granmammrisk_out_temp=table_all_out[4]['granmammrisk']
    granmammrisk_out.append(granmammrisk_out_temp)

######table 7#######
    folbirdrisk_out_temp=table_all_out[5]['folbirdrisk']
    folbirdrisk_out.append(folbirdrisk_out_temp)
    folreprisk_out_temp=table_all_out[5]['folreprisk']
    folreprisk_out.append(folreprisk_out_temp)
    folamphibrisk_out_temp=table_all_out[5]['folamphibrisk']
    folamphibrisk_out.append(folamphibrisk_out_temp)
    folmammrisk_out_temp=table_all_out[5]['folmammrisk']
    folmammrisk_out.append(folmammrisk_out_temp)

######table 8#######
    barebirdrisk_out_temp=table_all_out[6]['barebirdrisk']
    barebirdrisk_out.append(barebirdrisk_out_temp)
    barereprisk_out_temp=table_all_out[6]['barereprisk']
    barereprisk_out.append(barereprisk_out_temp)
    bareamphibrisk_out_temp=table_all_out[6]['bareamphibrisk']
    bareamphibrisk_out.append(bareamphibrisk_out_temp)
    baremammrisk_out_temp=table_all_out[6]['baremammrisk']
    baremammrisk_out.append(baremammrisk_out_temp)

    return html_table_temp  


def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()

    i=1
    iter_html=""
    for row in reader:
        iter_html = iter_html +html_table(row,i)
        i=i+1

    sum_input_html = dust_tables.table_sum_input(dust_tables.sumheadings, dust_tables.tmpl, i, ar_lb, frac_pest_surface, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw)
    sum_output_html = dust_tables.table_sum_output(granbirdderm_out, granherpderm_out, granmammderm_out,
                    folbirdderm_out, folherpderm_out, folmammderm_out,
                    barebirdderm_out, bareherpderm_out, baremammderm_out,
                    granbirdrisk_out, granreprisk_out, granamphibrisk_out, granmammrisk_out,
                    folbirdrisk_out, folreprisk_out, folamphibrisk_out, folmammrisk_out,
                    barebirdrisk_out, barereprisk_out, bareamphibrisk_out, baremammrisk_out
                    )

    return sum_input_html+sum_output_html+iter_html



              
class DustBatchOutputPage(webapp.RequestHandler):
    def post(self):
        text_file1 = open('rice/rice_description.txt','r')
        x = text_file1.read()
        form = cgi.FieldStorage()
        thefile = form['upfile']

        iter_html=loop_html(thefile)        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', 'title')
        # print baremammrisk_out
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
    
    

