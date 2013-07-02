import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db
import cgi
import cgitb
cgitb.enable()
import datetime
from ubertool.use import Use
import sys
sys.path.append("../")
import logging


class UbertoolUseConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("UbertoolUseConfigurationPage")
        form = cgi.FieldStorage()
        risk_output.gran_bird_ex_derm_dose = float(form.getvalue('gran_bird_ex_derm_dose'))
		risk_output.gran_repamp_ex_derm_dose = float(form.getvalue('gran_repamp_ex_derm_dose'))
		risk_output.gran_mam_ex_derm_dose = float(form.getvalue('gran_mam_ex_derm_dose'))
		risk_output.fol_bird_ex_derm_dose = float(form.getvalue('fol_bird_ex_derm_dose'))
		risk_output.fol_repamp_ex_derm_dose = float(form.getvalue('fol_repamp_ex_derm_dose'))
		risk_output.fol_mam_ex_derm_dose = float(form.getvalue('fol_mam_ex_derm_dose'))
		risk_output.bgs_bird_ex_derm_dose = float(form.getvalue('bgs_bird_ex_derm_dose'))
		risk_output.bgs_repamp_ex_derm_dose = float(form.getvalue('bgs_repamp_ex_derm_dose'))
		risk_output.bgs_mam_ex_derm_dose = float(form.getvalue('bgs_mam_ex_derm_dose'))
		risk_output.ratio_gran_bird = float(form.getvalue('ratio_gran_bird'))
		risk_output.LOC_gran_bird = float(form.getvalue('LOC_gran_bird'))
		risk_output.ratio_gran_rep = float(form.getvalue('ratio_gran_rep'))
		risk_output.LOC_gran_rep = float(form.getvalue('LOC_gran_rep'))
		risk_output.ratio_gran_amp = float(form.getvalue('ratio_gran_amp'))
		risk_output.LOC_gran_amp = float(form.getvalue('LOC_gran_amp'))
		risk_output.ratio_gran_mam = float(form.getvalue('ratio_gran_mam'))
		risk_output.LOC_gran_mam = float(form.getvalue('LOC_gran_mam'))
		risk_output.ratio_fol_bird = float(form.getvalue('ratio_fol_bird'))
		risk_output.LOC_fol_bird = float(form.getvalue('LOC_fol_bird'))
		risk_output.ratio_fol_rep = float(form.getvalue('ratio_fol_rep'))
		risk_output.LOC_fol_rep = float(form.getvalue('LOC_fol_rep'))
		risk_output.ratio_fol_amp = float(form.getvalue('ratio_fol_amp'))
		risk_output.LOC_fol_amp = float(form.getvalue('LOC_fol_amp'))
		risk_output.ratio_fol_mam = float(form.getvalue('ratio_fol_mam'))
		risk_output.LOC_fol_mam = float(form.getvalue('LOC_fol_mam'))
		risk_output.ratio_bgs_bird = float(form.getvalue('ratio_bgs_bird'))
		risk_output.LOC_bgs_bird = float(form.getvalue('LOC_bgs_bird'))
		risk_output.ratio_bgs_rep = float(form.getvalue('ratio_bgs_rep'))
		risk_output.LOC_bgs_rep = float(form.getvalue('LOC_bgs_rep'))
		risk_output.ratio_bgs_amp = float(form.getvalue('ratio_bgs_amp'))
		risk_output.LOC_bgs_amp = float(form.getvalue('LOC_bgs_amp'))
		risk_output.ratio_bgs_mam = float(form.getvalue('ratio_bgs_mam'))
		risk_output.LOC_bgs_mam = float(form.getvalue('LOC_bgs_mam'))




















        use.put()
        self.redirect("pesticide_properties.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolUseConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()