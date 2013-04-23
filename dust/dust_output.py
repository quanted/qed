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
import logging
import sys
sys.path.append("../utils")
import utils.json_utils
sys.path.append("../dust")
from dust import dust_tables
from django.template import Context, Template


class DUSTExecutePage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        chemical_name = form.getvalue('chemical_name')
        label_epa_reg_no = form.getvalue('label_epa_reg_no')
        ar_lb = form.getvalue('application_rate')
        frac_pest_surface = form.getvalue('frac_pest_assumed_at_surface')
        dislodge_fol_res = form.getvalue('dislodgeable_foliar_residue')
        bird_acute_oral_study = form.getvalue('bird_acute_oral_study')
        bird_study_add_comm = form.getvalue('bird_study_add_comm')
        low_bird_acute_ld50 = form.getvalue('low_bird_acute_oral_ld50')
        test_bird_bw = form.getvalue('tested_bird_body_weight')
        mamm_acute_derm_study = form.getvalue('mamm_acute_derm_study')
        mamm_study_add_comm = form.getvalue('mamm_study_add_comm')
        mam_acute_derm_ld50 = form.getvalue('mamm_acute_derm_ld50')
        test_mam_bw = form.getvalue('tested_mamm_body_weight')
        mineau = form.getvalue('mineau')
        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'dust','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'dust', 
                'model_attributes':'DUST Output'})   

        html = html + dust_tables.table_all(dust_tables.pvuheadings, dust_tables.pvrheadings, dust_tables.tmpl, chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res, bird_acute_oral_study, bird_study_add_comm,
              low_bird_acute_ld50, test_bird_bw, mineau, mamm_acute_derm_study, mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw)[0]
        
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)


app = webapp.WSGIApplication([('/.*', DUSTExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()


    
