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
from StringIO import StringIO
from pprint import pprint
import csv
import sys
sys.path.append("../agdrift")
from agdrift import agdrift_tables,agdrift_model
from uber import uber_lib
import unittest
import cStringIO
import logging 
import Queue
from collections import OrderedDict
import rest_funcs
logger=logging.getLogger('agdrift batch')

drop_size = []
ecosystem_type = [] 
application_method = []
boom_height = []
orchard_type = []
application_rate = []
distance = []
aquatic_type = []
calculation_input = []
#predefined outputs
init_avg_dep_foa_out = []
avg_depo_lbac_out = []
avg_depo_gha_out  = []
deposition_ngL_out = []
deposition_mgcm_out = []
nasae_out = []
y_out = []
x_out = []
express_y_out = []
jid_all = []
jid_batch = []
agdrift_obj_all = []
#data.next()

def html_table(row,iter):
    drop_size.append(str(row[0]))
    ecosystem_type.append(str(row[1])) 
    application_method.append(str(row[2]))
    boom_height.append(str(row[3]))
    orchard_type.append(str(row[4]))
    application_rate.append(float(row[5]))
    distance.append(float(row[6]))
    aquatic_type.append(str(row[7]))
    calculation_input.append(str(row[8]))

    Input_header="""<div class="out_">
                        <br><H3>Batch Calculation of Iteration %s</H3>
                    </div>"""%(iter)

    agdrift_obj_temp = agdrift_model.agdrift(True,True,'batch',drop_size[iter-1],ecosystem_type[iter-1], application_method[iter-1],boom_height[iter-1],orchard_type[iter-1],application_rate[iter-1],distance[iter-1],aquatic_type[iter-1],calculation_input[iter-1],)
    agdrift_obj_temp.loop_indx = str(iter)

    init_avg_dep_foa_out.append(agdrift_obj_temp.init_avg_dep_foa)
    avg_depo_lbac_out.append(agdrift_obj_temp.avg_depo_lbac)
    avg_depo_gha_out.append(agdrift_obj_temp.avg_depo_gha)
    deposition_ngL_out.append(agdrift_obj_temp.deposition_ngL)
    deposition_mgcm_out.append(agdrift_obj_temp.deposition_mgcm)
    nasae_out.append(agdrift_obj_temp.nasae)
    y_out.append(agdrift_obj_temp.y)
    x_out.append(agdrift_obj_temp.x)
    express_y_out.append(agdrift_obj_temp.express_y)

    jid_all.append(agdrift_obj_temp.jid)
    agdrift_obj_all.append(agdrift_obj_temp)    
    if iter == 1:
        jid_batch.append(agdrift_obj_temp.jid)
    
    table_all_out = agdrift_tables.table_all(agdrift_obj_temp)

    html_table_temp = Input_header + table_all_out + "<br>"
    return html_table_temp

def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()

    i=1
    iter_html_temp=""
    for row in reader:
        iter_html_temp = iter_html_temp +html_table(row,i)
        logger.info(iter_html_temp)
        i=i+1

    sum_input_html = agdrift_tables.table_sum_input(i,application_rate,distance)
    sum_output_html = agdrift_tables.table_sum_output(init_avg_dep_foa_out,avg_depo_lbac_out,avg_depo_gha_out,deposition_ngL_out,deposition_mgcm_out,nasae_out,y_out,x_out,express_y_out)
    return sum_input_html + sum_output_html + iter_html_temp


class AgdriftBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['file-0']
        iter_html=loop_html(thefile)        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        # html = uber_lib.SkinChk(ChkCookie)
        # html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'agdrift','page':'batchinput'})
        # html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = template.render(templatepath + '04uberbatch_start.html', {
                'model':'agdrift',
                'model_attributes':'Agdrift Batch Output'})
        html = html + agdrift_tables.timestamp("",jid_batch[0])
        html = html + iter_html
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + 'agdrift-output-jqplot_header.html', {})

        # html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.batch_save_dic(html, [x.__dict__ for x in agdrift_obj_all], 'agdrift', 'batch', jid_batch[0], ChkCookie, templatepath)
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', AgdriftBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

