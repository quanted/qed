import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import csv
from fdadiet import fdadiet_model,fdadiet_tables


chemical_name=[]
trade_name=[]
run_use=[]
atuse_conc=[]
residue=[]
worst_case_est=[]
vol=[]
d=[]
h=[]
sa=[]
intake_avg=[]
intake_90th=[]

######Pre-defined outputs########
sa_cylinder=[]
conc_unit_conv=[]
edi=[]
edi_avg_vol=[]
edi_90th_vol=[]

def html_table(row_inp,iter):
    chemical_name.append(str(row_inp[0]))
    trade_name.append(str(row_inp[1]))
    atuse_conc.append(float(row_inp[2]))
    residue.append(float(row_inp[3]))
    worst_case_est.append(float(row_inp[4]))
    vol.append(float(row_inp[5]))
    d.append(float(row_inp[6]))
    h.append(float(row_inp[7]))
    intake_avg.append(float(row_inp[9]))
    intake_90th.append(float(row_inp[10]))


    # Setting the model to run Tank Residue (Volumetric) model
    run_use='1'
    sa=0

    fdadiet_obj = fdadiet_model.fdadiet(True,True,chemical_name[iter],trade_name[iter],run_use,atuse_conc[iter],residue[iter],worst_case_est[iter],vol[iter],d[iter],h[iter],sa,intake_avg[iter],intake_90th[iter])

    sa_cylinder.append(fdadiet_obj.sa_cylinder)
    conc_unit_conv.append(fdadiet_obj.conc_unit_conv)
    edi.append(fdadiet_obj.edi)
    edi_avg_vol.append(fdadiet_obj.edi_avg_vol)
    edi_90th_vol.append(fdadiet_obj.edi_90th_vol)

    batch_header = """
        <div class="out_">
            <br><H3>Batch Calculation of Iteration %s:</H3>
        </div>
        """%(iter + 1)

    html = batch_header + fdadiet_tables.table_all(fdadiet_obj)
    return html

def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    i=0
    iter_html=""
    for row in reader:
        iter_html = iter_html +html_table(row,i)
        i=i+1

    return iter_html              


class fdadietQaqcPageOut(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['upfile']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', 'title')
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'fdadiet','page':'qaqc'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'fdadiet',
                'model_attributes':'FDA Dietary Exposure Model QAQC'})
        html = html + fdadiet_tables.timestamp()
        html = html + iter_html
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', fdadietQaqcPageOut)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
