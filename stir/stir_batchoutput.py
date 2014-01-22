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
sys.path.append("../stir")
from stir import stir_model,stir_tables
from uber import uber_lib
import logging

logger = logging.getLogger('stirBatchPage')

cwd= os.getcwd()
data = csv.reader(open(cwd+'/stir/stir_qaqc.csv'))
#inputs
chemical_name = []
application_rate = []
column_height = []
spray_drift_fraction = []
direct_spray_duration = []
molecular_weight = []
vapor_pressure = []
avian_oral_ld50 = []
body_weight_assessed_bird = []
body_weight_tested_bird = []
mineau_scaling_factor = []
mammal_inhalation_lc50 = []
duration_mammal_inhalation_study = []
body_weight_assessed_mammal = []
body_weight_tested_mammal = []
mammal_oral_ld50 = []

#outputs
sat_air_conc_out = []
inh_rate_avian_out = []
vid_avian_out = []
inh_rate_mammal_out = []
vid_mammal_out = []
ar2_out = []
air_conc_out = []
sid_avian_out = []
sid_mammal_out = []
cf_out = []
mammal_inhalation_ld50_out = []
adjusted_mammal_inhalation_ld50_out = []
estimated_avian_inhalation_ld50_out = []
adjusted_avian_inhalation_ld50_out = []
ratio_vid_avian_out = []
ratio_sid_avian_out = []
ratio_vid_mammal_out = []
ratio_sid_mammal_out = []
loc_vid_avian_out = []
loc_sid_avian_out = []
loc_vid_mammal_out = []
loc_sid_mammal_out = []

data.next()

def html_table(row,iter):
    chemical_name.append(str(row[0]))
    application_rate.append(float(row[1]))
    column_height.append(float(row[2]))
    spray_drift_fraction.append(float(row[3]))
    direct_spray_duration.append(float(row[4]))
    molecular_weight.append(float(row[5]))
    vapor_pressure.append(float(row[6]))
    avian_oral_ld50.append(float(row[7]))
    body_weight_assessed_bird.append(float(row[8]))
    body_weight_tested_bird.append(float(row[9]))
    mineau_scaling_factor.append(float(row[10]))
    mammal_inhalation_lc50.append(float(row[11]))
    duration_mammal_inhalation_study.append(float(row[12]))
    body_weight_assessed_mammal.append(float(row[13]))
    body_weight_tested_mammal.append(float(row[14]))
    mammal_oral_ld50.append(float(row[15]))

    Input_header="""<div class="out_">
                        <br><H3>Batch Calculation of Iteration %s</H3>
                    </div>"""%(iter)

    stir_obj_temp = stir_model.StirModel(True,True,chemical_name[iter-1],application_rate[iter-1],column_height[iter-1],spray_drift_fraction[iter-1],direct_spray_duration[iter-1], 
            molecular_weight[iter-1],vapor_pressure[iter-1],avian_oral_ld50[iter-1], body_weight_assessed_bird[iter-1], body_weight_tested_bird[iter-1], mineau_scaling_factor[iter-1], 
            mammal_inhalation_lc50[iter-1],duration_mammal_inhalation_study[iter-1],body_weight_assessed_mammal[iter-1], body_weight_tested_mammal[iter-1], 
            mammal_oral_ld50[iter-1])

    sat_air_conc_out.append(stir_obj_temp.sat_air_conc)
    inh_rate_avian_out.append(stir_obj_temp.inh_rate_avian)
    vid_avian_out.append(stir_obj_temp.vid_avian)
    inh_rate_mammal_out.append(stir_obj_temp.inh_rate_mammal)
    vid_mammal_out.append(stir_obj_temp.vid_mammal)
    ar2_out.append(stir_obj_temp.ar2)
    air_conc_out.append(stir_obj_temp.air_conc)
    sid_avian_out.append(stir_obj_temp.sid_avian)
    sid_mammal_out.append(stir_obj_temp.sid_mammal)
    cf_out.append(stir_obj_temp.cf)
    mammal_inhalation_ld50_out.append(stir_obj_temp.mammal_inhalation_ld50)
    adjusted_mammal_inhalation_ld50_out.append(stir_obj_temp.adjusted_mammal_inhalation_ld50)
    estimated_avian_inhalation_ld50_out.append(stir_obj_temp.estimated_avian_inhalation_ld50)
    adjusted_avian_inhalation_ld50_out.append(stir_obj_temp.adjusted_avian_inhalation_ld50)
    ratio_vid_avian_out.append(stir_obj_temp.ratio_vid_avian)
    ratio_sid_avian_out.append(stir_obj_temp.ratio_sid_avian)
    ratio_vid_mammal_out.append(stir_obj_temp.ratio_vid_mammal)
    ratio_sid_mammal_out.append(stir_obj_temp.ratio_sid_mammal)
    loc_vid_avian_out.append(stir_obj_temp.loc_vid_avian)
    loc_sid_avian_out.append(stir_obj_temp.loc_sid_avian)
    loc_vid_mammal_out.append(stir_obj_temp.loc_vid_mammal)
    loc_sid_mammal_out.append(stir_obj_temp.loc_sid_mammal)

    table_all_out = stir_tables.table_all_batch(stir_obj_temp)
    
    html_table_temp = Input_header + table_all_out + "<br>"

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

    sum_1=stir_tables.table_sum_1(i,application_rate,column_height,spray_drift_fraction,direct_spray_duration,molecular_weight,vapor_pressure)
    sum_2=stir_tables.table_sum_2(avian_oral_ld50,body_weight_assessed_bird,body_weight_tested_bird,mineau_scaling_factor,mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal,body_weight_tested_mammal,mammal_oral_ld50)
    sum_3=stir_tables.table_sum_3(sat_air_conc_out,inh_rate_avian_out,vid_avian_out,estimated_avian_inhalation_ld50_out,adjusted_avian_inhalation_ld50_out,ratio_vid_avian_out,sid_avian_out,ratio_sid_avian_out)
    sum_4=stir_tables.table_sum_4(sat_air_conc_out,inh_rate_mammal_out,vid_mammal_out,mammal_inhalation_ld50_out,adjusted_mammal_inhalation_ld50_out,ratio_vid_mammal_out,sid_mammal_out,ratio_sid_mammal_out)
    sum_5=stir_tables.table_sum_5(ratio_vid_avian_out, ratio_sid_avian_out, ratio_vid_mammal_out, ratio_sid_mammal_out)   
    return sum_1+sum_2+sum_3+sum_4+sum_5+iter_html


              
class stirBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['file-0']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        # html = uber_lib.SkinChk(ChkCookie)
        # html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'stir','page':'batchinput'})
        # html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = template.render(templatepath + '04uberbatch_start.html', {
                'model':'stir',
                'model_attributes':'STIR Batch Output'})
        html = html + stir_tables.timestamp()
        html = html + iter_html
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        # html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', stirBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

