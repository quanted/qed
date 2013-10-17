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
sys.path.append("../swim")
from swim import swim_model, swim_tables
import logging

logger = logging.getLogger('swimBatchPage')


#inputs
chemical_name = []
log_kow = []
mw = []
hlc = []
r = []
T = []
cw = []
noael = []

bw_aa = []
bw_fa = []
sa_a_c = []
sa_a_nc = []
et_a_c = []
et_a_nc = []
ir_a_c = []
ir_a_nc = []
igr_a_c = []
igr_a_nc = []

bw_c1 = []
sa_c1_c = []
sa_c1_nc = []
et_c1_c = []
et_c1_nc = []
ir_c1_c = []
ir_c1_nc = []
igr_c1_c = []
igr_c1_nc = []

bw_c2 = []
sa_c2_c = []
sa_c2_nc = []
et_c2_c = []
et_c2_nc = []
ir_c2_c = []
ir_c2_nc = []
igr_c2_c = []
igr_c2_nc = []


#outputs
inh_c_aa_out = []
inh_c_fa_out = []
inh_c_c1_out = []
inh_c_c2_out = []
inh_nc_aa_out = []
inh_nc_fa_out = []
inh_nc_c1_out = []
inh_nc_c2_out = []
inh_c_aa_moe_out = []
inh_c_fa_moe_out = []
inh_c_c1_moe_out = []
inh_c_c2_moe_out = []
inh_nc_aa_moe_out = []
inh_nc_fa_moe_out = []
inh_nc_c1_moe_out = []
inh_nc_c2_moe_out = []

ing_c_aa_out = []
ing_c_fa_out = []
ing_c_c1_out = []
ing_c_c2_out = []
ing_nc_aa_out = []
ing_nc_fa_out = []
ing_nc_c1_out = []
ing_nc_c2_out = []
ing_c_aa_moe_out = []
ing_c_fa_moe_out = []
ing_c_c1_moe_out = []
ing_c_c2_moe_out = []
ing_nc_aa_moe_out = []
ing_nc_fa_moe_out = []
ing_nc_c1_moe_out = []
ing_nc_c2_moe_out = []

der_c_aa_out = []
der_c_fa_out = []
der_c_c1_out = []
der_c_c2_out = []
der_nc_aa_out = []
der_nc_fa_out = []
der_nc_c1_out = []
der_nc_c2_out = []
der_c_aa_moe_out = []
der_c_fa_moe_out = []
der_c_c1_moe_out = []
der_c_c2_moe_out = []
der_nc_aa_moe_out = []
der_nc_fa_moe_out = []
der_nc_c1_moe_out = []
der_nc_c2_moe_out = []

def html_table(row, iter):
    chemical_name_temp = str(row[0])
    chemical_name.append(chemical_name_temp)
    log_kow_temp = float(row[1])
    log_kow.append(log_kow_temp)
    mw_temp = float(row[2])
    mw.append(mw_temp)
    hlc_temp = float(row[3])
    hlc.append(hlc_temp)
    r_temp = float(row[4])
    r.append(r_temp)
    T_temp = float(row[5])
    T.append(T_temp)
    cw_temp = float(row[6])
    cw.append(cw_temp)
    noael_temp = float(row[7])
    noael.append(noael_temp)

    bw_aa_temp = float(row[8])
    bw_aa.append(bw_aa_temp)
    bw_fa_temp = float(row[9])
    bw_fa.append(bw_fa_temp)
    sa_a_c_temp = float(row[10])
    sa_a_c.append(sa_a_c_temp)
    sa_a_nc_temp = float(row[11])
    sa_a_nc.append(sa_a_nc_temp)
    et_a_c_temp = float(row[12])
    et_a_c.append(et_a_c_temp)
    et_a_nc_temp = float(row[13])
    et_a_nc.append(et_a_nc_temp)
    ir_a_c_temp = float(row[14])
    ir_a_c.append(ir_a_c_temp)
    ir_a_nc_temp = float(row[15])
    ir_a_nc.append(ir_a_nc_temp)
    igr_a_c_temp = float(row[16])
    igr_a_c.append(igr_a_c_temp)
    igr_a_nc_temp = float(row[17])
    igr_a_nc.append(igr_a_nc_temp)

    bw_c1_temp = float(row[18])
    bw_c1.append(bw_c1_temp)
    sa_c1_c_temp = float(row[19])
    sa_c1_c.append(sa_c1_c_temp)
    sa_c1_nc_temp = float(row[20])
    sa_c1_nc.append(sa_c1_nc_temp)
    et_c1_c_temp = float(row[21])
    et_c1_c.append(et_c1_c_temp)
    et_c1_nc_temp = float(row[22])
    et_c1_nc.append(et_c1_nc_temp)
    ir_c1_c_temp = float(row[23])
    ir_c1_c.append(ir_c1_c_temp)
    ir_c1_nc_temp = float(row[24])
    ir_c1_nc.append(ir_c1_nc_temp)
    igr_c1_c_temp = float(row[25])
    igr_c1_c.append(igr_c1_c_temp)
    igr_c1_nc_temp = float(row[26])
    igr_c1_nc.append(igr_c1_nc_temp)

    bw_c2_temp = float(row[27])
    bw_c2.append(bw_c2_temp)
    sa_c2_c_temp = float(row[28])
    sa_c2_c.append(sa_c2_c_temp)
    sa_c2_nc_temp = float(row[29])
    sa_c2_nc.append(sa_c2_nc_temp)
    et_c2_c_temp = float(row[30])
    et_c2_c.append(et_c2_c_temp)
    et_c2_nc_temp = float(row[31])
    et_c2_nc.append(et_c2_nc_temp)
    ir_c2_c_temp = float(row[32])
    ir_c2_c.append(ir_c2_c_temp)
    ir_c2_nc_temp = float(row[33])
    ir_c2_nc.append(ir_c2_nc_temp)
    igr_c2_c_temp = float(row[34])
    igr_c2_c.append(igr_c2_c_temp)
    igr_c2_nc_temp = float(row[35])
    igr_c2_nc.append(igr_c2_nc_temp)

    swim_obj_temp = swim_model.swim(chemical_name_temp, log_kow_temp, mw_temp, hlc_temp, r_temp, T_temp, cw_temp, noael_temp, 
                                     bw_aa_temp, bw_fa_temp, sa_a_c_temp, sa_a_nc_temp, et_a_c_temp, et_a_nc_temp, ir_a_c_temp, ir_a_nc_temp, igr_a_c_temp, igr_a_nc_temp, 
                                     bw_c1_temp, sa_c1_c_temp, sa_c1_nc_temp, et_c1_c_temp, et_c1_nc_temp, ir_c1_c_temp, ir_c1_nc_temp, igr_c1_c_temp, igr_c1_nc_temp, 
                                     bw_c2_temp, sa_c2_c_temp, sa_c2_nc_temp, et_c2_c_temp, et_c2_nc_temp, ir_c2_c_temp, ir_c2_nc_temp, igr_c2_c_temp, igr_c2_nc_temp)

    inh_c_aa_out.append(swim_obj_temp.inh_c_aa)
    inh_c_fa_out.append(swim_obj_temp.inh_c_fa)
    inh_c_c1_out.append(swim_obj_temp.inh_c_c1)
    inh_c_c2_out.append(swim_obj_temp.inh_c_c2)
    inh_nc_aa_out.append(swim_obj_temp.inh_nc_aa)
    inh_nc_fa_out.append(swim_obj_temp.inh_nc_fa)
    inh_nc_c1_out.append(swim_obj_temp.inh_nc_c1)
    inh_nc_c2_out.append(swim_obj_temp.inh_nc_c2)
    inh_c_aa_moe_out.append(swim_obj_temp.inh_c_aa_moe)
    inh_c_fa_moe_out.append(swim_obj_temp.inh_c_fa_moe)
    inh_c_c1_moe_out.append(swim_obj_temp.inh_c_c1_moe)
    inh_c_c2_moe_out.append(swim_obj_temp.inh_c_c2_moe)
    inh_nc_aa_moe_out.append(swim_obj_temp.inh_nc_aa_moe)
    inh_nc_fa_moe_out.append(swim_obj_temp.inh_nc_fa_moe)
    inh_nc_c1_moe_out.append(swim_obj_temp.inh_nc_c1_moe)
    inh_nc_c2_moe_out.append(swim_obj_temp.inh_nc_c2_moe)

    ing_c_aa_out.append(swim_obj_temp.ing_c_aa)
    ing_c_fa_out.append(swim_obj_temp.ing_c_fa)
    ing_c_c1_out.append(swim_obj_temp.ing_c_c1)
    ing_c_c2_out.append(swim_obj_temp.ing_c_c2)
    ing_nc_aa_out.append(swim_obj_temp.ing_nc_aa)
    ing_nc_fa_out.append(swim_obj_temp.ing_nc_fa)
    ing_nc_c1_out.append(swim_obj_temp.ing_nc_c1)
    ing_nc_c2_out.append(swim_obj_temp.ing_nc_c2)
    ing_c_aa_moe_out.append(swim_obj_temp.ing_c_aa_moe)
    ing_c_fa_moe_out.append(swim_obj_temp.ing_c_fa_moe)
    ing_c_c1_moe_out.append(swim_obj_temp.ing_c_c1_moe)
    ing_c_c2_moe_out.append(swim_obj_temp.ing_c_c2_moe)
    ing_nc_aa_moe_out.append(swim_obj_temp.ing_nc_aa_moe)
    ing_nc_fa_moe_out.append(swim_obj_temp.ing_nc_fa_moe)
    ing_nc_c1_moe_out.append(swim_obj_temp.ing_nc_c1_moe)
    ing_nc_c2_moe_out.append(swim_obj_temp.ing_nc_c2_moe)

    der_c_aa_out.append(swim_obj_temp.der_c_aa)
    der_c_fa_out.append(swim_obj_temp.der_c_fa)
    der_c_c1_out.append(swim_obj_temp.der_c_c1)
    der_c_c2_out.append(swim_obj_temp.der_c_c2)
    der_nc_aa_out.append(swim_obj_temp.der_nc_aa)
    der_nc_fa_out.append(swim_obj_temp.der_nc_fa)
    der_nc_c1_out.append(swim_obj_temp.der_nc_c1)
    der_nc_c2_out.append(swim_obj_temp.der_nc_c2)
    der_c_aa_moe_out.append(swim_obj_temp.der_c_aa_moe)
    der_c_fa_moe_out.append(swim_obj_temp.der_c_fa_moe)
    der_c_c1_moe_out.append(swim_obj_temp.der_c_c1_moe)
    der_c_c2_moe_out.append(swim_obj_temp.der_c_c2_moe)
    der_nc_aa_moe_out.append(swim_obj_temp.der_nc_aa_moe)
    der_nc_fa_moe_out.append(swim_obj_temp.der_nc_fa_moe)
    der_nc_c1_moe_out.append(swim_obj_temp.der_nc_c1_moe)
    der_nc_c2_moe_out.append(swim_obj_temp.der_nc_c2_moe)


    Input_header="""<H3 class="out_0 collapsible" id="section0"><span></span>Batch Calculation of Iteration %s</H3>
                    <div class="out_">
                    """%(iter)
    table_all_out = swim_tables.table_all(swim_obj_temp)
    html_table_temp = Input_header + table_all_out + "</div><br>"

    return html_table_temp           
    
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    reader.next()
    reader.next()
    header = reader.next()
    exclud_list = ['', " ", "  ", "   ", "    ", "     ", "      ", "       ", "        ", "         ", "          "]
    i=1

    iter_html=""
    for row in reader:
        if row[3] in exclud_list:
            break
        iter_html = iter_html +html_table(row,i)
        i=i+1
    sum_0 = """
                <H3 class="out_1 collapsible" id="section1"><span></span>Batch Summary Statistics (Iterations=%s)</H3>
                <div class="out_">
    """%(i-1)
    sum_1 = swim_tables.table_sum_1(i, log_kow, mw, hlc, r, T, cw, noael)
    sum_2 = swim_tables.table_sum_2(bw_aa, bw_fa, sa_a_c, sa_a_nc, et_a_c, et_a_nc, ir_a_c, ir_a_nc, igr_a_c, igr_a_nc)
    sum_3 = swim_tables.table_sum_3(bw_c1, sa_c1_c, sa_c1_nc, et_c1_c, et_c1_nc, ir_c1_c, ir_c1_nc, igr_c1_c, igr_c1_nc)
    sum_4 = swim_tables.table_sum_4(bw_c2, sa_c2_c, sa_c2_nc, et_c2_c, et_c2_nc, ir_c2_c, ir_c2_nc, igr_c2_c, igr_c2_nc)
    sum_5 = swim_tables.table_sum_5(inh_c_aa_out, inh_c_fa_out, inh_c_c1_out, inh_c_c2_out, inh_nc_aa_out, inh_nc_fa_out, 
                                    inh_nc_c1_out, inh_nc_c2_out, ing_c_aa_out, ing_c_fa_out, ing_c_c1_out, ing_c_c2_out, 
                                    ing_nc_aa_out, ing_nc_fa_out, ing_nc_c1_out, ing_nc_c2_out, der_c_aa_out, der_c_fa_out, 
                                    der_c_c1_out, der_c_c2_out, der_nc_aa_out, der_nc_fa_out, der_nc_c1_out, der_nc_c2_out)
    sum_6 = swim_tables.table_sum_6(inh_c_aa_moe_out, inh_c_fa_moe_out, inh_c_c1_moe_out, inh_c_c2_moe_out, inh_nc_aa_moe_out, inh_nc_fa_moe_out, 
                                    inh_nc_c1_moe_out, inh_nc_c2_moe_out, ing_c_aa_moe_out, ing_c_fa_moe_out, ing_c_c1_moe_out, ing_c_c2_moe_out, 
                                    ing_nc_aa_moe_out, ing_nc_fa_moe_out, ing_nc_c1_moe_out, ing_nc_c2_moe_out, der_c_aa_moe_out, der_c_fa_moe_out, 
                                    der_c_c1_moe_out, der_c_c2_moe_out, der_nc_aa_moe_out, der_nc_fa_moe_out, der_nc_c1_moe_out, der_nc_c2_moe_out)
    sum_7 = """</div><br>"""
    return sum_0+sum_1+sum_2+sum_3+sum_4+sum_5+sum_6+sum_7+iter_html


              
class swimBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['upfile']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', 'title')
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'swim','page':'batchinput'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {
                'model':'swim',
                'model_attributes':'SWIM Batch Output'})
        html = html + swim_tables.timestamp()
        html = html + iter_html
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', swimBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

