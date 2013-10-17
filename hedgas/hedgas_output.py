# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import math 
import cgitb
cgitb.enable()
from hedgas import hedgas_model,hedgas_tables
  
 
class hedgasOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()

        run_acuteNonOcc = form.getvalue('run_acuteNonOcc')
        run_noaelunit_acuteNonOcc = form.getvalue('run_noaelunit_acuteNonOcc')
        if run_acuteNonOcc == '1':
            mw_acuteNonOcc = float(form.getvalue('mw_acuteNonOcc'))
            if run_noaelunit_acuteNonOcc == '1':
                noael_acuteNonOcc = float(form.getvalue('noael_acuteNonOcc'))
            else:
                noael_acuteNonOcc = float(form.getvalue('noael_acuteNonOcc')) * (mw_acuteNonOcc / 24.45)
            hrs_animal_acuteNonOcc = float(form.getvalue('hrs_animal_acuteNonOcc'))
            hrs_human_acuteNonOcc = float(form.getvalue('hrs_human_acuteNonOcc'))
            dow_animal_acuteNonOcc = float(form.getvalue('dow_animal_acuteNonOcc'))
            dow_human_acuteNonOcc = float(form.getvalue('dow_human_acuteNonOcc'))
            b0_acuteNonOcc = float(form.getvalue('b0_acuteNonOcc'))
            b1_acuteNonOcc = float(form.getvalue('b1_acuteNonOcc'))
            SAa_acuteNonOcc = float(form.getvalue('SAa_acuteNonOcc'))
            tb_acuteNonOcc = float(form.getvalue('tb_acuteNonOcc'))
            pu_acuteNonOcc = float(form.getvalue('pu_acuteNonOcc'))            
        else:
            mw_acuteNonOcc = -1
            run_noaelunit_acuteNonOcc = -1
            noael_acuteNonOcc = -1
            hrs_animal_acuteNonOcc = -1
            hrs_human_acuteNonOcc = -1
            dow_animal_acuteNonOcc = -1
            dow_human_acuteNonOcc = -1
            b0_acuteNonOcc = -1
            b1_acuteNonOcc = -1
            SAa_acuteNonOcc = -1
            tb_acuteNonOcc = -1
            pu_acuteNonOcc = -1

        run_stitNonOcc = form.getvalue('run_stitNonOcc')
        run_noaelunit_stitNonOcc = form.getvalue('run_noaelunit_stitNonOcc')
        if run_stitNonOcc == '1':
            mw_stitNonOcc = float(form.getvalue('mw_stitNonOcc'))
            if run_noaelunit_stitNonOcc == '1':
                noael_stitNonOcc = float(form.getvalue('noael_stitNonOcc'))
            else:
                noael_stitNonOcc = float(form.getvalue('noael_stitNonOcc')) * (mw_stitNonOcc / 24.45)
            hrs_animal_stitNonOcc = float(form.getvalue('hrs_animal_stitNonOcc'))
            hrs_human_stitNonOcc = float(form.getvalue('hrs_human_stitNonOcc'))
            BWa_stitNonOcc = float(form.getvalue('BWa_stitNonOcc'))
            dow_animal_stitNonOcc = float(form.getvalue('dow_animal_stitNonOcc'))
            dow_human_stitNonOcc = float(form.getvalue('dow_human_stitNonOcc'))
            b0_stitNonOcc = float(form.getvalue('b0_stitNonOcc'))
            b1_stitNonOcc = float(form.getvalue('b1_stitNonOcc'))
            SAa_stitNonOcc = float(form.getvalue('SAa_stitNonOcc'))
            tb_stitNonOcc = float(form.getvalue('tb_stitNonOcc'))
            pu_stitNonOcc = float(form.getvalue('pu_stitNonOcc'))           
        else:
            mw_stitNonOcc = -1
            run_noaelunit_stitNonOcc = -1
            noael_stitNonOcc = -1
            hrs_animal_stitNonOcc = -1
            hrs_human_stitNonOcc = -1
            BWa_stitNonOcc = -1
            dow_animal_stitNonOcc = -1
            dow_human_stitNonOcc = -1
            b0_stitNonOcc = -1
            b1_stitNonOcc = -1
            SAa_stitNonOcc = -1
            tb_stitNonOcc = -1
            pu_stitNonOcc = -1

        run_ltNonOcc = form.getvalue('run_ltNonOcc')
        run_noaelunit_ltNonOcc = form.getvalue('run_noaelunit_ltNonOcc')
        if run_ltNonOcc == '1':
            mw_ltNonOcc = float(form.getvalue('mw_ltNonOcc'))
            if run_noaelunit_ltNonOcc == '1':
                noael_ltNonOcc = float(form.getvalue('noael_ltNonOcc'))
            else:
                noael_ltNonOcc = float(form.getvalue('noael_ltNonOcc')) * (mw_ltNonOcc / 24.45)
            hrs_animal_ltNonOcc = float(form.getvalue('hrs_animal_ltNonOcc'))
            hrs_human_ltNonOcc = float(form.getvalue('hrs_human_ltNonOcc'))
            BWa_ltNonOcc = float(form.getvalue('BWa_ltNonOcc'))
            dow_animal_ltNonOcc = float(form.getvalue('dow_animal_ltNonOcc'))
            dow_human_ltNonOcc = float(form.getvalue('dow_human_ltNonOcc'))
            b0_ltNonOcc = float(form.getvalue('b0_ltNonOcc'))
            b1_ltNonOcc = float(form.getvalue('b1_ltNonOcc'))
            SAa_ltNonOcc = float(form.getvalue('SAa_ltNonOcc'))
            tb_ltNonOcc = float(form.getvalue('tb_ltNonOcc'))
            pu_ltNonOcc = float(form.getvalue('pu_ltNonOcc'))           
        else:
            mw_ltNonOcc = -1
            run_noaelunit_ltNonOcc = -1
            noael_ltNonOcc = -1
            hrs_animal_ltNonOcc = -1
            hrs_human_ltNonOcc = -1
            BWa_ltNonOcc = -1
            dow_animal_ltNonOcc = -1
            dow_human_ltNonOcc = -1
            b0_ltNonOcc = -1
            b1_ltNonOcc = -1
            SAa_ltNonOcc = -1
            tb_ltNonOcc = -1
            pu_ltNonOcc = -1

        run_acuteOcc = form.getvalue('run_acuteOcc')
        run_noaelunit_acuteOcc = form.getvalue('run_noaelunit_acuteOcc')
        if run_acuteOcc == '1':
            mw_acuteOcc = float(form.getvalue('mw_acuteOcc'))
            if run_noaelunit_acuteOcc == '1':
                noael_acuteOcc = float(form.getvalue('noael_acuteOcc'))
            else:
                noael_acuteOcc = float(form.getvalue('noael_acuteOcc')) * (mw_acuteOcc / 24.45)
            hrs_animal_acuteOcc = float(form.getvalue('hrs_animal_acuteOcc'))
            hrs_human_acuteOcc = float(form.getvalue('hrs_human_acuteOcc'))
            dow_animal_acuteOcc = float(form.getvalue('dow_animal_acuteOcc'))
            dow_human_acuteOcc = float(form.getvalue('dow_human_acuteOcc'))
            BWa_acuteOcc = float(form.getvalue('BWa_acuteOcc'))
            b0_acuteOcc = float(form.getvalue('b0_acuteOcc'))
            b1_acuteOcc = float(form.getvalue('b1_acuteOcc'))
            SAa_acuteOcc = float(form.getvalue('SAa_acuteOcc'))
            tb_acuteOcc = float(form.getvalue('tb_acuteOcc'))
            pu_acuteOcc = float(form.getvalue('pu_acuteOcc'))            
        else:
            mw_acuteOcc = -1
            noael_acuteOcc = -1
            run_noaelunit_acuteOcc = -1
            hrs_animal_acuteOcc = -1
            hrs_human_acuteOcc = -1
            BWa_acuteOcc = -1
            dow_animal_acuteOcc = -1
            dow_human_acuteOcc = -1
            b0_acuteOcc = -1
            b1_acuteOcc = -1
            SAa_acuteOcc = -1
            tb_acuteOcc = -1
            pu_acuteOcc = -1

        run_stitOcc = form.getvalue('run_stitOcc')
        run_noaelunit_stitOcc = form.getvalue('run_noaelunit_stitOcc')
        if run_stitOcc == '1':
            mw_stitOcc = float(form.getvalue('mw_stitOcc'))
            if run_noaelunit_stitOcc == '1':
                noael_stitOcc = float(form.getvalue('noael_stitOcc'))
            else:
                noael_stitOcc = float(form.getvalue('noael_stitOcc')) * (mw_stitOcc / 24.45)
            hrs_animal_stitOcc = float(form.getvalue('hrs_animal_stitOcc'))
            hrs_human_stitOcc = float(form.getvalue('hrs_human_stitOcc'))
            BWa_stitOcc = float(form.getvalue('BWa_stitOcc'))
            dow_animal_stitOcc = float(form.getvalue('dow_animal_stitOcc'))
            dow_human_stitOcc = float(form.getvalue('dow_human_stitOcc'))
            b0_stitOcc = float(form.getvalue('b0_stitOcc'))
            b1_stitOcc = float(form.getvalue('b1_stitOcc'))
            SAa_stitOcc = float(form.getvalue('SAa_stitOcc'))
            tb_stitOcc = float(form.getvalue('tb_stitOcc'))
            pu_stitOcc = float(form.getvalue('pu_stitOcc'))           
        else:
            mw_stitOcc = -1
            run_noaelunit_stitOcc = -1
            noael_stitOcc = -1
            hrs_animal_stitOcc = -1
            hrs_human_stitOcc = -1
            BWa_stitOcc = -1
            dow_animal_stitOcc = -1
            dow_human_stitOcc = -1
            b0_stitOcc = -1
            b1_stitOcc = -1
            SAa_stitOcc = -1
            tb_stitOcc = -1
            pu_stitOcc = -1

        run_ltOcc = form.getvalue('run_ltOcc')
        run_noaelunit_ltOcc = form.getvalue('run_noaelunit_ltOcc')
        if run_ltOcc == '1':
            mw_ltOcc = float(form.getvalue('mw_ltOcc'))
            if run_noaelunit_ltOcc == '1':
                noael_ltOcc = float(form.getvalue('noael_ltOcc'))
            else:
                noael_ltOcc = float(form.getvalue('noael_ltOcc')) * (mw_ltOcc / 24.45)
            hrs_animal_ltOcc = float(form.getvalue('hrs_animal_ltOcc'))
            hrs_human_ltOcc = float(form.getvalue('hrs_human_ltOcc'))
            BWa_ltOcc = float(form.getvalue('BWa_ltOcc'))
            dow_animal_ltOcc = float(form.getvalue('dow_animal_ltOcc'))
            dow_human_ltOcc = float(form.getvalue('dow_human_ltOcc'))
            b0_ltOcc = float(form.getvalue('b0_ltOcc'))
            b1_ltOcc = float(form.getvalue('b1_ltOcc'))
            SAa_ltOcc = float(form.getvalue('SAa_ltOcc'))
            tb_ltOcc = float(form.getvalue('tb_ltOcc'))
            pu_ltOcc = float(form.getvalue('pu_ltOcc'))           
        else:
            mw_ltOcc = -1
            run_noaelunit_ltOcc = -1
            noael_ltOcc = -1
            hrs_animal_ltOcc = -1
            hrs_human_ltOcc = -1
            BWa_ltOcc = -1
            dow_animal_ltOcc = -1
            dow_human_ltOcc = -1
            b0_ltOcc = -1
            b1_ltOcc = -1
            SAa_ltOcc = -1
            tb_ltOcc = -1
            pu_ltOcc = -1


        hedgas_obj = hedgas_model.hedgas(True,True,run_acuteNonOcc,mw_acuteNonOcc,noael_acuteNonOcc,hrs_animal_acuteNonOcc,hrs_human_acuteNonOcc,dow_animal_acuteNonOcc,dow_human_acuteNonOcc,b0_acuteNonOcc,b1_acuteNonOcc,SAa_acuteNonOcc,tb_acuteNonOcc,pu_acuteNonOcc,run_stitNonOcc,mw_stitNonOcc,noael_stitNonOcc,hrs_animal_stitNonOcc,hrs_human_stitNonOcc,BWa_stitNonOcc,dow_animal_stitNonOcc,dow_human_stitNonOcc,b0_stitNonOcc,b1_stitNonOcc,SAa_stitNonOcc,tb_stitNonOcc,pu_stitNonOcc,run_ltNonOcc,mw_ltNonOcc,noael_ltNonOcc,hrs_animal_ltNonOcc,hrs_human_ltNonOcc,BWa_ltNonOcc,dow_animal_ltNonOcc,dow_human_ltNonOcc,b0_ltNonOcc,b1_ltNonOcc,SAa_ltNonOcc,tb_ltNonOcc,pu_ltNonOcc,run_acuteOcc,mw_acuteOcc,noael_acuteOcc,hrs_animal_acuteOcc,hrs_human_acuteOcc,BWa_acuteOcc,dow_animal_acuteOcc,dow_human_acuteOcc,b0_acuteOcc,b1_acuteOcc,SAa_acuteOcc,tb_acuteOcc,pu_acuteOcc,run_stitOcc,mw_stitOcc,noael_stitOcc,hrs_animal_stitOcc,hrs_human_stitOcc,BWa_stitOcc,dow_animal_stitOcc,dow_human_stitOcc,b0_stitOcc,b1_stitOcc,SAa_stitOcc,tb_stitOcc,pu_stitOcc,run_ltOcc,mw_ltOcc,noael_ltOcc,hrs_animal_ltOcc,hrs_human_ltOcc,BWa_ltOcc,dow_animal_ltOcc,dow_human_ltOcc,b0_ltOcc,b1_ltOcc,SAa_ltOcc,tb_ltOcc,pu_ltOcc)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html',  {'model':'hedgas','page':'output'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'hedgas', 
                'model_attributes':'HED Gas Calculator Output'})
        html = html + hedgas_tables.timestamp()
        html = html + hedgas_tables.table_all(hedgas_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', hedgasOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()