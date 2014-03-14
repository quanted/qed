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
import rest_funcs

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


jid_all = []
jid_batch = []
stir_all = []
all_threads = []
out_html_all = {}
job_q = Queue.Queue()
thread_count = 10

data.next()


def html_table(row_inp_all):
    while True:
        row_inp_temp_all = row_inp_all.get()
        if row_inp_temp_all is None:
            break
        else:
            row_inp = row_inp_temp_all[0]
            iter = row_inp_temp_all[1]

            logger.info("iteration: " + str(iter))

            chemical_name_temp=str(row_inp[0])
            chemical_name.append(chemical_name_temp)
            application_rate_temp=float(row[1])
            application_rate.append(application_rate_temp)
            column_height_temp=float(row[2])
            column_height.append(column_height_temp)
            spray_drift_fraction_temp=float(row[3])
            spray_drift_fraction.append(spray_drift_fraction_temp)
            direct_spray_duration_temp=float(row[4])
            direct_spray_duration.append(direct_spray_duration_temp)
            molecular_weight_temp=float(row[5])
            molecular_weight.append(molecular_weight_temp)
            vapor_pressure_temp=float(row[6])
            vapor_pressure.append(vapor_pressure_temp)
            avian_oral_ld50_temp=float(row[7])
            avian_oral_ld50.append(avian_oral_ld50_temp)
            body_weight_assessed_bird_temp=float(row[8])
            body_weight_assessed_bird.append(body_weight_assessed_bird_temp)
            body_weight_tested_bird_temp=float(row[9])
            body_weight_tested_bird.append(body_weight_tested_bird_temp)
            mineau_scaling_factor_temp=float(row[10])
            mineau_scaling_factor.append(mineau_scaling_factor_temp)
            mammal_inhalation_lc50_temp=float(row[11])
            mammal_inhalation_lc50.append(mammal_inhalation_lc50_temp)
            duration_mammal_inhalation_study_temp=float(row[12])
            duration_mammal_inhalation_study.append(duration_mammal_inhalation_study_temp)
            body_weight_assessed_mammal_temp=float(row[13])
            body_weight_assessed_mammal.append(body_weight_assessed_mammal_temp)
            body_weight_tested_mammal_temp=float(row[14])
            body_weight_tested_mammal.append(body_weight_tested_mammal_temp)
            mammal_oral_ld50_temp=float(row[15])
            mammal_oral_ld50.append(mammal_oral_ld50_temp)


            Input_header="""<div class="out_">
                                <br><H3>Batch Calculation of Iteration %s</H3>
                            </div>"""%(iter)

            stir_obj_temp = stir_model.StirModel(True,True,chemical_name_temp,application_rate_temp,column_height_temp,spray_drift_fraction_temp,direct_spray_duration_temp, 
                    molecular_weight_temp,vapor_pressure_temp,avian_oral_ld50_temp, body_weight_assessed_bird_temp, body_weight_tested_bird_temp, mineau_scaling_factor_temp, 
                    mammal_inhalation_lc50_temp,duration_mammal_inhalation_study_temp,body_weight_assessed_mammal_temp, body_weight_tested_mammal_temp, 
                    mammal_oral_ld50_temp)
            
            logger.info("===============")

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

            jid_all.append(stir_obj_temp.jid)
            stir_all.append(stir_obj_temp)    
            if iter == 1:
                jid_batch.append(stir_obj_temp.jid)

            batch_header = """
                <div class="out_">
                    <br><H3>Batch Calculation of Iteration %s:</H3>
                </div>
                """%(iter)
                
            html_temp = stir_tables.table_all(stir_obj_temp)
            out_html_temp = batch_header + html_temp + "<br>"
            out_html_all[iter]=out_html_temp         
    
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    exclud_list = ['', " ", "  ", "   ", "    ", "     ", "      ", "       ", "        ", "         ", "          "]
    i=1

    for row in reader:
        job_q.put([row, i])
        i=i+1

    all_threads = [Thread(target=html_table, args=(job_q, )) for j in range(thread_count)]
    for x in all_threads:
        x.start()
    for x in all_threads:
        job_q.put(None)
    for x in all_threads:
        x.join()

    html_timestamp = stir_tables.timestamp("", jid_batch[0])
    out_html_all_sort = OrderedDict(sorted(out_html_all.items()))

    sum_1=stir_tables.table_sum_1(i,application_rate,column_height,spray_drift_fraction,direct_spray_duration,molecular_weight,vapor_pressure)
    sum_2=stir_tables.table_sum_2(avian_oral_ld50,body_weight_assessed_bird,body_weight_tested_bird,mineau_scaling_factor,mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal,body_weight_tested_mammal,mammal_oral_ld50)
    sum_3=stir_tables.table_sum_3(sat_air_conc_out,inh_rate_avian_out,vid_avian_out,estimated_avian_inhalation_ld50_out,adjusted_avian_inhalation_ld50_out,ratio_vid_avian_out,sid_avian_out,ratio_sid_avian_out)
    sum_4=stir_tables.table_sum_4(sat_air_conc_out,inh_rate_mammal_out,vid_mammal_out,mammal_inhalation_ld50_out,adjusted_mammal_inhalation_ld50_out,ratio_vid_mammal_out,sid_mammal_out,ratio_sid_mammal_out)
    sum_5=stir_tables.table_sum_5(ratio_vid_avian_out, ratio_sid_avian_out, ratio_vid_mammal_out, ratio_sid_mammal_out)   
    return html_timestamp + sum_1+sum_2+sum_3+sum_4+sum_5+"".join(out_html_all_sort.values())


              
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
        rest_funcs.batch_save_dic(html, [x.__dict__ for x in stir_all], 'stir', 'batch', jid_batch[0], ChkCookie, templatepath)
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', stirBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

