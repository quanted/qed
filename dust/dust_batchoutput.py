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
sys.path.append("../dust")
from dust import dust_tables,dust_model
from uber import uber_lib
import unittest
import cStringIO
import logging 
import Queue
from collections import OrderedDict
import rest_funcs
logger=logging.getLogger('dust batch')

chemical_name = []
label_epa_reg_no = []
ar_lb = []
frac_pest_surface = []
dislodge_fol_res = []
bird_acute_oral_study = []
bird_study_add_comm = []
low_bird_acute_ld50 = []
test_bird_bw = []
mamm_acute_derm_study = []
mamm_study_add_comm = []
mam_acute_derm_ld50 = []
mam_acute_oral_ld50 = []
test_mam_bw = []
mineau_scaling_factor = []


######Pre-defined outputs########
ar_mg_out=[]
bird_reptile_dermal_ld50_out=[]
gran_bird_ex_derm_dose_out=[]
gran_repamp_ex_derm_dose_out=[]
gran_mam_ex_derm_dose_out=[]
fol_bird_ex_derm_dose_out=[]
fol_repamp_ex_derm_dose_out=[]
fol_mam_ex_derm_dose_out=[]
bgs_bird_ex_derm_dose_out=[]
bgs_repamp_ex_derm_dose_out=[]
bgs_mam_ex_derm_dose_out=[]
amp_derm_ld50_out=[]
birdrep_derm_ld50_out=[]
mam_derm_ld50_out=[]
ratio_gran_bird_out=[]
LOC_gran_bird_out=[]
ratio_gran_rep_out=[]
LOC_gran_rep_out=[]
ratio_gran_amp_out=[]
LOC_gran_amp_out=[]
ratio_gran_mam_out=[]
LOC_gran_mam_out=[]
ratio_fol_bird_out=[]
LOC_fol_bird_out=[]
ratio_fol_rep_out=[]
LOC_fol_rep_out=[]
ratio_fol_amp_out=[]
LOC_fol_amp_out=[]
ratio_fol_mam_out=[]
LOC_fol_mam_out=[]
ratio_bgs_bird_out=[]
LOC_bgs_bird_out=[]
ratio_bgs_rep_out=[]
LOC_bgs_rep_out=[]
ratio_bgs_amp_out=[]
LOC_bgs_amp_out=[]
ratio_bgs_mam_out=[]
LOC_bgs_mam_out=[]
jid_all=[]
jid_batch=[]
dust_obj_all=[]
#data.next()

def html_table(row,iter):
    chemical_name.append(str(row[0]))
    label_epa_reg_no.append(str(row[1]))
    ar_lb.append(float(row[2]))
    frac_pest_surface.append(float(row[3]))
    dislodge_fol_res.append(float(row[4]))
    bird_acute_oral_study.append(str(row[5]))
    bird_study_add_comm.append(str(row[6]))
    low_bird_acute_ld50.append(float(row[7]))
    test_bird_bw.append(float(row[8]))
    mineau_scaling_factor.append(float(row[9]))
    mamm_acute_derm_study.append(str(row[10]))
    mamm_study_add_comm.append(str(row[11]))
    mam_acute_derm_ld50.append(float(row[12]))
    mam_acute_oral_ld50.append(float(row[13]))
    test_mam_bw.append(float(row[14]))


    Input_header="""<div class="out_">
                        <br><H3>Batch Calculation of Iteration %s</H3>
                    </div>"""%(iter)

    dust_obj_temp = dust_model.dust(True,True, 'qaqc', chemical_name[iter-1],label_epa_reg_no[iter-1],ar_lb[iter-1],frac_pest_surface[iter-1],
    dislodge_fol_res[iter-1],bird_acute_oral_study[iter-1],bird_study_add_comm[iter-1],low_bird_acute_ld50[iter-1],test_bird_bw[iter-1],mineau_scaling_factor[iter-1],mamm_acute_derm_study[iter-1],mamm_study_add_comm[iter-1],mam_acute_derm_ld50[iter-1],mam_acute_oral_ld50[iter-1],test_mam_bw[iter-1],)

    ar_mg_out.append(dust_obj_temp.ar_mg)
    bird_reptile_dermal_ld50_out.append(dust_obj_temp.bird_reptile_dermal_ld50)
    gran_bird_ex_derm_dose_out.append(dust_obj_temp.gran_bird_ex_derm_dose)
    gran_repamp_ex_derm_dose_out.append(dust_obj_temp.gran_repamp_ex_derm_dose)
    gran_mam_ex_derm_dose_out.append(dust_obj_temp.gran_mam_ex_derm_dose)
    fol_bird_ex_derm_dose_out.append(dust_obj_temp.fol_bird_ex_derm_dose)
    fol_repamp_ex_derm_dose_out.append(dust_obj_temp.fol_repamp_ex_derm_dose)
    fol_mam_ex_derm_dose_out.append(dust_obj_temp.fol_mam_ex_derm_dose)
    bgs_bird_ex_derm_dose_out.append(dust_obj_temp.bgs_bird_ex_derm_dose)
    bgs_repamp_ex_derm_dose_out.append(dust_obj_temp.bgs_repamp_ex_derm_dose)
    bgs_mam_ex_derm_dose_out.append(dust_obj_temp.bgs_mam_ex_derm_dose)
    amp_derm_ld50_out.append(dust_obj_temp.amp_derm_ld50)
    birdrep_derm_ld50_out.append(dust_obj_temp.birdrep_derm_ld50)
    mam_derm_ld50_out.append(dust_obj_temp.mam_derm_ld50)
    ratio_gran_bird_out.append(dust_obj_temp.ratio_gran_bird)
    LOC_gran_bird_out.append(dust_obj_temp.LOC_gran_bird)
    ratio_gran_rep_out.append(dust_obj_temp.ratio_gran_rep)
    LOC_gran_rep_out.append(dust_obj_temp.LOC_gran_rep)
    ratio_gran_amp_out.append(dust_obj_temp.ratio_gran_amp)
    LOC_gran_amp_out.append(dust_obj_temp.LOC_gran_amp)
    ratio_gran_mam_out.append(dust_obj_temp.ratio_gran_mam)
    LOC_gran_mam_out.append(dust_obj_temp.LOC_gran_mam)
    ratio_fol_bird_out.append(dust_obj_temp.ratio_fol_bird)
    LOC_fol_bird_out.append(dust_obj_temp.LOC_fol_bird)
    ratio_fol_rep_out.append(dust_obj_temp.ratio_fol_rep)
    LOC_fol_rep_out.append(dust_obj_temp.LOC_fol_rep)
    ratio_fol_amp_out.append(dust_obj_temp.ratio_fol_amp)
    LOC_fol_amp_out.append(dust_obj_temp.LOC_fol_amp)
    ratio_fol_mam_out.append(dust_obj_temp.ratio_fol_mam)
    LOC_fol_mam_out.append(dust_obj_temp.LOC_fol_mam)
    ratio_bgs_bird_out.append(dust_obj_temp.ratio_bgs_bird)
    LOC_bgs_bird_out.append(dust_obj_temp.LOC_bgs_bird)
    ratio_bgs_rep_out.append(dust_obj_temp.ratio_bgs_rep)
    LOC_bgs_rep_out.append(dust_obj_temp.LOC_bgs_rep)
    ratio_bgs_amp_out.append(dust_obj_temp.ratio_bgs_amp)
    LOC_bgs_amp_out.append(dust_obj_temp.LOC_bgs_amp)
    ratio_bgs_mam_out.append(dust_obj_temp.ratio_bgs_mam)
    LOC_bgs_mam_out.append(dust_obj_temp.LOC_bgs_mam)

    jid_all.append(dust_obj_temp.jid)
    dust_obj_all.append(dust_obj_temp)    
    if iter == 1:
        jid_batch.append(dust_obj_temp.jid)

    table_all_out = dust_tables.table_all(dust_obj_temp)
        # html = html + dust_tables.table_all(dust_obj)[0]

    html_table_temp = Input_header + table_all_out[0] + "<br>"
    return html_table_temp
######table 3#######
#     granbirdderm_out_temp=table_all_out[1]['granbirdderm']
#     granbirdderm_out.append(granbirdderm_out_temp)
#     granherpderm_out_temp=table_all_out[1]['granherpderm']
#     granherpderm_out.append(granherpderm_out_temp)
#     granmammderm_out_temp=table_all_out[1]['granmammderm']
#     granmammderm_out.append(granmammderm_out_temp)

# ######table 4#######
#     folbirdderm_out_temp=table_all_out[2]['folbirdderm']
#     folbirdderm_out.append(folbirdderm_out_temp)
#     folherpderm_out_temp=table_all_out[2]['folherpderm']
#     folherpderm_out.append(folherpderm_out_temp)
#     folmammderm_out_temp=table_all_out[2]['folmammderm']
#     folmammderm_out.append(folmammderm_out_temp)

# ######table 5#######
#     barebirdderm_out_temp=table_all_out[3]['barebirdderm']
#     barebirdderm_out.append(barebirdderm_out_temp)
#     bareherpderm_out_temp=table_all_out[3]['bareherpderm']
#     bareherpderm_out.append(bareherpderm_out_temp)
#     baremammderm_out_temp=table_all_out[3]['baremammderm']
#     baremammderm_out.append(baremammderm_out_temp)

# ######table 6#######
#     granbirdrisk_out_temp=table_all_out[4]['granbirdrisk']
#     granbirdrisk_out.append(granbirdrisk_out_temp)
#     granreprisk_out_temp=table_all_out[4]['granreprisk']
#     granreprisk_out.append(granreprisk_out_temp)
#     granamphibrisk_out_temp=table_all_out[4]['granamphibrisk']
#     granamphibrisk_out.append(granamphibrisk_out_temp)
#     granmammrisk_out_temp=table_all_out[4]['granmammrisk']
#     granmammrisk_out.append(granmammrisk_out_temp)

# ######table 7#######
#     folbirdrisk_out_temp=table_all_out[5]['folbirdrisk']
#     folbirdrisk_out.append(folbirdrisk_out_temp)
#     folreprisk_out_temp=table_all_out[5]['folreprisk']
#     folreprisk_out.append(folreprisk_out_temp)
#     folamphibrisk_out_temp=table_all_out[5]['folamphibrisk']
#     folamphibrisk_out.append(folamphibrisk_out_temp)
#     folmammrisk_out_temp=table_all_out[5]['folmammrisk']
#     folmammrisk_out.append(folmammrisk_out_temp)

# ######table 8#######
#     barebirdrisk_out_temp=table_all_out[6]['barebirdrisk']
#     barebirdrisk_out.append(barebirdrisk_out_temp)
#     barereprisk_out_temp=table_all_out[6]['barereprisk']
#     barereprisk_out.append(barereprisk_out_temp)
#     bareamphibrisk_out_temp=table_all_out[6]['bareamphibrisk']
#     bareamphibrisk_out.append(bareamphibrisk_out_temp)
#     baremammrisk_out_temp=table_all_out[6]['baremammrisk']
#     baremammrisk_out.append(baremammrisk_out_temp)

#     return html_table_temp  


def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()

    i=1
    iter_html=""
    for row in reader:
        logger.info(row)
        iter_html = iter_html +html_table(row,i)
        i=i+1

    sum_input_html = dust_tables.table_sum_input(i, ar_lb,frac_pest_surface,dislodge_fol_res,low_bird_acute_ld50,test_bird_bw,mam_acute_derm_ld50, mam_acute_oral_ld50,test_mam_bw,mineau_scaling_factor)
    sum_output_html = dust_tables.table_sum_output(gran_bird_ex_derm_dose_out,gran_repamp_ex_derm_dose_out,gran_mam_ex_derm_dose_out,fol_bird_ex_derm_dose_out,fol_repamp_ex_derm_dose_out,fol_mam_ex_derm_dose_out,bgs_bird_ex_derm_dose_out,bgs_repamp_ex_derm_dose_out,bgs_mam_ex_derm_dose_out,ratio_gran_bird_out,ratio_gran_rep_out,ratio_gran_amp_out,ratio_gran_mam_out,ratio_fol_bird_out,ratio_fol_rep_out,ratio_fol_amp_out,ratio_fol_mam_out,ratio_bgs_bird_out,ratio_bgs_rep_out,ratio_bgs_amp_out,ratio_bgs_mam_out)
    return sum_input_html + sum_output_html + iter_html 


class DustBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['file-0']
        iter_html=loop_html(thefile)        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        # html = uber_lib.SkinChk(ChkCookie)
        # html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'dust','page':'batchinput'})
        # html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = template.render(templatepath + '04uberbatch_start.html', {
                'model':'dust',
                'model_attributes':'DUST Batch Output'})
        html = html + dust_tables.timestamp("",jid_batch[0])
        html = html + iter_html
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        # html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.batch_save_dic(html, [x.__dict__ for x in dust_obj_all], 'dust', 'batch', jid_batch[0], ChkCookie, templatepath)
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', DustBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

