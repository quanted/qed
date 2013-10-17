# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
#import numpy as np
import cgi
#import math 
import cgitb
cgitb.enable()
from fdadiet import fdadiet_model,fdadiet_tables


class fdadietOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()

        chemical_name = form.getvalue('chemical_name')
        trade_name = form.getvalue('trade_name')
        run_use = form.getvalue('run_use')
        atuse_conc = float(form.getvalue('atuse_conc'))
        residue = float(form.getvalue('residue'))
        worst_case_est = float(form.getvalue('worst_case_est'))
        vol = float(form.getvalue('vol'))
        d = form.getvalue('d')
        h = form.getvalue('h')
        sa = form.getvalue('sa')
        intake_avg = float(form.getvalue('intake_avg'))
        intake_90th = float(form.getvalue('intake_90th'))

        fdadiet_obj = fdadiet_model.fdadiet(True,True,chemical_name,trade_name,run_use,atuse_conc,residue,worst_case_est,vol,d,h,sa,intake_avg,intake_90th)

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html',  {'model':'fdadiet','page':'output'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'fdadiet', 
                'model_attributes':'FDA Dietary Exposure Model Output'})
        html = html + fdadiet_tables.timestamp()
        html = html + fdadiet_tables.table_all(fdadiet_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', fdadietOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    