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
import csv
import sys
sys.path.append("../idream")
from idream import idream_model, idream_tables
import logging

logger = logging.getLogger('idreamBatchPage')


#inputs
tire = [] 
ai_name = []
prod_re = []
ai = []
liq_rte = []
fruit_rte = []
bread_rte = []
cheese_rte = []
veg_rte = []
meat_rte = []
pure_rte = []
piec_rte = []
powd_rte = []

#outputs
exp_child_c_1_out = []
exp_child_c_2_out = []
exp_adult_c_out = []
exp_fe_c_out = []
exp_child_a_1_out = []
exp_child_a_2_out = []
exp_adult_a_out = []
exp_fe_a_out = []


def html_table(row, iter):
    tire_temp = str(row[0])
    ai_name_temp = str(row[1])
    ai_name.append(ai_name_temp)
    prod_re_temp = float(row[2])
    prod_re.append(prod_re_temp)
    ai_temp = float(row[3])/100
    ai.append(ai_temp)

    if tire_temp == 'Tier 2':
        idream_obj_temp = idream_model.idream(tire_temp, ai_name_temp, prod_re_temp, ai_temp)
        liq_rte.append(1)
        fruit_rte.append(0.7)
        bread_rte.append(0.2)
        cheese_rte.append(0.55)
        veg_rte.append(0.7)
        meat_rte.append(0.8)
        pure_rte.append(1)
        piec_rte.append(0.55)
        powd_rte.append(0.2)

        exp_child_c_1_out.append(idream_obj_temp.exp_child_c_1)
        exp_child_c_2_out.append(idream_obj_temp.exp_child_c_2)
        exp_adult_c_out.append(idream_obj_temp.exp_adult_c)
        exp_fe_c_out.append(idream_obj_temp.exp_fe_c)
        exp_child_a_1_out.append(idream_obj_temp.exp_child_a_1)
        exp_child_a_2_out.append(idream_obj_temp.exp_child_a_2)
        exp_adult_a_out.append(idream_obj_temp.exp_adult_a)
        exp_fe_a_out.append(idream_obj_temp.exp_fe_a)

    else:
        liq_rte_temp = float(row[4])/100
        fruit_rte_temp = float(row[5])/100
        bread_rte_temp = float(row[6])/100
        cheese_rte_temp = float(row[7])/100
        veg_rte_temp = float(row[8])/100
        meat_rte_temp = float(row[9])/100
        pure_rte_temp = float(row[10])/100
        piec_rte_temp = float(row[11])/100
        powd_rte_temp = float(row[12])/100
        liq_rte.append(liq_rte_temp)
        fruit_rte.append(fruit_rte_temp)
        bread_rte.append(bread_rte_temp)
        cheese_rte.append(cheese_rte_temp)
        veg_rte.append(veg_rte_temp)
        meat_rte.append(meat_rte_temp)
        pure_rte.append(pure_rte_temp)
        piec_rte.append(piec_rte_temp)
        powd_rte.append(powd_rte_temp)
        
        idream_obj_temp = idream_model.idream3(tire_temp, ai_name_temp, prod_re_temp, ai_temp, liq_rte_temp, fruit_rte_temp, bread_rte_temp, cheese_rte_temp, veg_rte_temp, meat_rte_temp, pure_rte_temp, piec_rte_temp, powd_rte_temp)

        exp_child_c_1_out.append(idream_obj_temp.exp_child_c_1[0])
        exp_child_c_2_out.append(idream_obj_temp.exp_child_c_2[0])
        exp_adult_c_out.append(idream_obj_temp.exp_adult_c[0])
        exp_fe_c_out.append(idream_obj_temp.exp_fe_c[0])
        exp_child_a_1_out.append(idream_obj_temp.exp_child_a_1)
        exp_child_a_2_out.append(idream_obj_temp.exp_child_a_2)
        exp_adult_a_out.append(idream_obj_temp.exp_adult_a)
        exp_fe_a_out.append(idream_obj_temp.exp_fe_a)


    Input_header="""<br><H3 class="out_0 collapsible" id="section0"><span></span>Batch Calculation of Iteration %s</H3>
                        <div class="out_">
                 """%(iter)

    table_all_out = idream_tables.table_all(idream_obj_temp)
    html_table_temp = Input_header + table_all_out + "</div><br>"

    return html_table_temp           
    
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    exclud_list = ['', " ", "  ", "   ", "    ", "     ", "      ", "       ", "        ", "         ", "          "]
    i=1

    iter_html=""
    for row in reader:
        if row[3] in exclud_list:
            break
        iter_html = iter_html +html_table(row,i)
        i=i+1


    sum_0="""
        <H3 class="out_1 collapsible" id="section1"><span></span>Batch Summary Statistics (Iterations=%s)</H3>
        <div class="out_">"""%(i-1)
    sum_1=idream_tables.table_sum_1(i, prod_re, ai, liq_rte, fruit_rte, bread_rte, cheese_rte, veg_rte, meat_rte, pure_rte, piec_rte, powd_rte)
    sum_2=idream_tables.table_sum_2(exp_child_c_1_out, exp_child_c_2_out, exp_adult_c_out, exp_fe_c_out)
    sum_3=idream_tables.table_sum_3(exp_child_a_1_out, exp_child_a_2_out, exp_adult_a_out, exp_fe_a_out)
    sum_4="""</div>"""
    return sum_0+sum_1+sum_2+sum_3+sum_4+iter_html


              
class idreamBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['upfile']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', 'title')
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'idream','page':'batchinput'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {
                'model':'idream',
                'model_attributes':'IDREAM Batch Output'})
        html = html + idream_tables.timestamp()
        html = html + iter_html
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', idreamBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

