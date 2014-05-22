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
from dust import dust_tables,dust_model
from uber import uber_lib
from django.template import Context, Template
from django.utils import simplejson
import rest_funcs

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
        #aviandermaltype = form.getvalue('aviandermaltype')
        mam_acute_derm_ld50 = form.getvalue('mamm_acute_derm_ld50')
        mam_acute_oral_ld50 = form.getvalue('mam_acute_oral_ld50')
        test_mam_bw = form.getvalue('tested_mamm_body_weight')
        mineau_scaling_factor = float(form.getvalue('mineau_scaling_factor'))
        dust_obj = dust_model.dust(True, False, 'single',chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res, bird_acute_oral_study, bird_study_add_comm,
              low_bird_acute_ld50, test_bird_bw, mineau_scaling_factor, mamm_acute_derm_study, mamm_study_add_comm, mam_acute_derm_ld50, mam_acute_oral_ld50, test_mam_bw, None)
        #print vars(dust_obj)

        # client = pymongo.MongoClient()
        # # print client

        # db = client.test_database
        # posts = db.posts
        # user_names={"user":"tao"}
        # dust_save = dict(dust_obj.__dict__,**user_names)
        # posts.insert(dust_save)
        # print db
        # print posts
        # print posts.find_one({"user":"tao"})

        # for post in posts.find({"user":"tao"}):
        #     print post
            
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "DUST Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'dust','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'dust', 
                'model_attributes':'DUST Output'})
        html = html + dust_tables.timestamp(dust_obj)
        html = html + dust_tables.table_all(dust_obj)[0]
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, dust_obj.__dict__, "dust", "single")
        self.response.out.write(html)


app = webapp.WSGIApplication([('/.*', DUSTExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()


    
