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
		risk_output.EEC_diet_SG = float(form.getvalue('EEC_diet_SG'))
        risk_output.EEC_diet_TG = float(form.getvalue('EEC_diet_TG'))
        risk_output.EEC_diet_TG = float(form.getvalue('EEC_diet_BP'))
        risk_output.EEC_diet_TG = float(form.getvalue('EEC_diet_FR'))
        risk_output.EEC_diet_TG = float(form.getvalue('EEC_diet_AR'))
        risk_output.EEC_dose_bird_SG_sm = float(form.getvalue('EEC_dose_bird_SG_sm'))
        risk_output.EEC_dose_bird_SG_md = float(form.getvalue('EEC_dose_bird_SG_md'))
        risk_output.EEC_dose_bird_SG_lg = float(form.getvalue('EEC_dose_bird_SG_lg'))
        risk_output.EEC_dose_bird_TG_sm = float(form.getvalue('EEC_dose_bird_TG_sm'))
        risk_output.EEC_dose_bird_TG_md = float(form.getvalue('EEC_dose_bird_TG_md'))
        risk_output.EEC_dose_bird_TG_lg = float(form.getvalue('EEC_dose_bird_TG_lg'))
        risk_output.EEC_dose_bird_BP_sm = float(form.getvalue('EEC_dose_bird_BP_sm'))
        risk_output.EEC_dose_bird_BP_md = float(form.getvalue('EEC_dose_bird_BP_md'))
        risk_output.EEC_dose_bird_BP_lg = float(form.getvalue('EEC_dose_bird_BP_lg'))
        risk_output.EEC_dose_bird_FP_sm = float(form.getvalue('EEC_dose_bird_FP_sm'))
        risk_output.EEC_dose_bird_FP_md = float(form.getvalue('EEC_dose_bird_FP_md'))
        risk_output.EEC_dose_bird_FP_lg = float(form.getvalue('EEC_dose_bird_FP_lg'))
        risk_output.EEC_dose_bird_AR_sm = float(form.getvalue('EEC_dose_bird_AR_sm'))
        risk_output.EEC_dose_bird_AR_md = float(form.getvalue('EEC_dose_bird_AR_md'))
        risk_output.EEC_dose_bird_AR_lg = float(form.getvalue('EEC_dose_bird_AR_lg'))
        risk_output.EEC_dose_bird_SE_sm = float(form.getvalue('EEC_dose_bird_SE_sm'))
        risk_output.EEC_dose_bird_SE_md = float(form.getvalue('EEC_dose_bird_SE_md'))
        risk_output.EEC_dose_bird_SE_lg = float(form.getvalue('EEC_dose_bird_SE_lg'))
        risk_output.ARQ_diet_bird_SG_A = float(form.getvalue('ARQ_diet_bird_SG_A'))
        risk_output.ARQ_diet_bird_SG_C = float(form.getvalue('ARQ_diet_bird_SG_C'))
        risk_output.ARQ_diet_bird_TG_A = float(form.getvalue('ARQ_diet_bird_TG_A'))
        risk_output.ARQ_diet_bird_TG_C = float(form.getvalue('ARQ_diet_bird_TG_C'))
        risk_output.ARQ_diet_bird_BP_A = float(form.getvalue('ARQ_diet_bird_BP_A'))
        risk_output.ARQ_diet_bird_BP_C = float(form.getvalue('ARQ_diet_bird_BP_C'))
        risk_output.ARQ_diet_bird_FP_A = float(form.getvalue('ARQ_diet_bird_FP_A'))
        risk_output.ARQ_diet_bird_FP_C = float(form.getvalue('ARQ_diet_bird_FP_C'))
        risk_output.ARQ_diet_bird_AR_A = float(form.getvalue('ARQ_diet_bird_AR_A'))
        risk_output.ARQ_diet_bird_AR_C = float(form.getvalue('ARQ_diet_bird_AR_C'))
        risk_output.EEC_dose_mamm_SG_sm = float(form.getvalue('EEC_dose_mamm_SG_sm'))
        risk_output.EEC_dose_mamm_SG_md = float(form.getvalue('EEC_dose_mamm_SG_md'))
        risk_output.EEC_dose_mamm_SG_lg = float(form.getvalue('EEC_dose_mamm_SG_lg'))
        risk_output.EEC_dose_mamm_TG_sm = float(form.getvalue('EEC_dose_mamm_TG_sm'))
        risk_output.EEC_dose_mamm_TG_md = float(form.getvalue('EEC_dose_mamm_TG_md'))
        risk_output.EEC_dose_mamm_TG_lg = float(form.getvalue('EEC_dose_mamm_TG_lg'))
        risk_output.EEC_dose_mamm_BP_sm = float(form.getvalue('EEC_dose_mamm_BP_sm'))
        risk_output.EEC_dose_mamm_BP_md = float(form.getvalue('EEC_dose_mamm_BP_md'))
        risk_output.EEC_dose_mamm_BP_lg = float(form.getvalue('EEC_dose_mamm_BP_lg'))
        risk_output.EEC_dose_mamm_FP_sm = float(form.getvalue('EEC_dose_mamm_FP_sm'))
        risk_output.EEC_dose_mamm_FP_md = float(form.getvalue('EEC_dose_mamm_FP_md'))
        risk_output.EEC_dose_mamm_FP_lg = float(form.getvalue('EEC_dose_mamm_FP_lg'))
        risk_output.EEC_dose_mamm_AR_sm = float(form.getvalue('EEC_dose_mamm_AR_sm'))
        risk_output.EEC_dose_mamm_AR_md = float(form.getvalue('EEC_dose_mamm_AR_md'))
        risk_output.EEC_dose_mamm_AR_lg = float(form.getvalue('EEC_dose_mamm_AR_lg'))
        risk_output.EEC_dose_mamm_SE_sm = float(form.getvalue('EEC_dose_mamm_SE_sm'))
        risk_output.EEC_dose_mamm_SE_md = float(form.getvalue('EEC_dose_mamm_SE_md'))
        risk_output.EEC_dose_mamm_SE_lg = float(form.getvalue('EEC_dose_mamm_SE_lg'))
        risk_output.ARQ_dose_mamm_SG_sm = float(form.getvalue('ARQ_dose_mamm_SG_sm'))
        risk_output.CRQ_dose_mamm_SG_sm = float(form.getvalue('CRQ_dose_mamm_SG_sm'))
        risk_output.ARQ_dose_mamm_SG_md = float(form.getvalue('ARQ_dose_mamm_SG_md'))
        risk_output.CRQ_dose_mamm_SG_md = float(form.getvalue('CRQ_dose_mamm_SG_md'))
		risk_output.ARQ_dose_mamm_SG_lg = float(form.getvalue('ARQ_dose_mamm_SG_lg'))
        risk_output.CRQ_dose_mamm_SG_lg = float(form.getvalue('CRQ_dose_mamm_SG_lg'))
        risk_output.ARQ_dose_mamm_TG_sm = float(form.getvalue('ARQ_dose_mamm_TG_sm'))
        risk_output.CRQ_dose_mamm_TG_sm = float(form.getvalue('CRQ_dose_mamm_TG_sm'))
        risk_output.ARQ_dose_mamm_TG_md = float(form.getvalue('ARQ_dose_mamm_TG_md'))
        risk_output.CRQ_dose_mamm_TG_md = float(form.getvalue('CRQ_dose_mamm_TG_md'))
		risk_output.ARQ_dose_mamm_TG_lg = float(form.getvalue('ARQ_dose_mamm_TG_lg'))
        risk_output.CRQ_dose_mamm_TG_lg = float(form.getvalue('CRQ_dose_mamm_TG_lg'))
        risk_output.ARQ_dose_mamm_BP_sm = float(form.getvalue('ARQ_dose_mamm_BP_sm'))
        risk_output.CRQ_dose_mamm_BP_sm = float(form.getvalue('CRQ_dose_mamm_BP_sm'))
        risk_output.ARQ_dose_mamm_BP_md = float(form.getvalue('ARQ_dose_mamm_BP_md'))
        risk_output.CRQ_dose_mamm_BP_md = float(form.getvalue('CRQ_dose_mamm_BP_md'))
		risk_output.ARQ_dose_mamm_BP_lg = float(form.getvalue('ARQ_dose_mamm_BP_lg'))
        risk_output.CRQ_dose_mamm_BP_lg = float(form.getvalue('CRQ_dose_mamm_BP_lg'))
        risk_output.ARQ_dose_mamm_FP_sm = float(form.getvalue('ARQ_dose_mamm_FP_sm'))
        risk_output.CRQ_dose_mamm_FP_sm = float(form.getvalue('CRQ_dose_mamm_FP_sm'))
        risk_output.ARQ_dose_mamm_FP_md = float(form.getvalue('ARQ_dose_mamm_FP_md'))
        risk_output.CRQ_dose_mamm_FP_md = float(form.getvalue('CRQ_dose_mamm_FP_md'))
		risk_output.ARQ_dose_mamm_FP_lg = float(form.getvalue('ARQ_dose_mamm_FP_lg'))
        risk_output.CRQ_dose_mamm_FP_lg = float(form.getvalue('CRQ_dose_mamm_FP_lg'))
        risk_output.ARQ_dose_mamm_AR_sm = float(form.getvalue('ARQ_dose_mamm_AR_sm'))
        risk_output.CRQ_dose_mamm_AR_sm = float(form.getvalue('CRQ_dose_mamm_AR_sm'))
        risk_output.ARQ_dose_mamm_AR_md = float(form.getvalue('ARQ_dose_mamm_AR_md'))
        risk_output.CRQ_dose_mamm_AR_md = float(form.getvalue('CRQ_dose_mamm_AR_md'))
		risk_output.ARQ_dose_mamm_AR_lg = float(form.getvalue('ARQ_dose_mamm_AR_lg'))
        risk_output.CRQ_dose_mamm_AR_lg = float(form.getvalue('CRQ_dose_mamm_AR_lg'))
        risk_output.ARQ_dose_mamm_SE_sm = float(form.getvalue('ARQ_dose_mamm_AR_sm'))
        risk_output.CRQ_dose_mamm_SE_sm = float(form.getvalue('CRQ_dose_mamm_AR_sm'))
        risk_output.ARQ_dose_mamm_SE_md = float(form.getvalue('ARQ_dose_mamm_AR_md'))
        risk_output.CRQ_dose_mamm_SE_md = float(form.getvalue('CRQ_dose_mamm_AR_md'))
		risk_output.ARQ_dose_mamm_SE_lg = float(form.getvalue('ARQ_dose_mamm_AR_lg'))
        risk_output.CRQ_dose_mamm_SE_lg = float(form.getvalue('CRQ_dose_mamm_AR_lg'))
        risk_output.ARQ_diet_mamm_SG = float(form.getvalue('ARQ_diet_mamm_SG'))
        risk_output.CRQ_diet_mamm_SG = float(form.getvalue('CRQ_diet_mamm_SG'))
        risk_output.ARQ_diet_mamm_TG = float(form.getvalue('ARQ_diet_mamm_TG'))
        risk_output.CRQ_diet_mamm_TG = float(form.getvalue('CRQ_diet_mamm_TG'))
        risk_output.ARQ_diet_mamm_BP = float(form.getvalue('ARQ_diet_mamm_BP'))
        risk_output.CRQ_diet_mamm_BP = float(form.getvalue('CRQ_diet_mamm_BP'))
        risk_output.ARQ_diet_mamm_FP = float(form.getvalue('ARQ_diet_mamm_FP'))
        risk_output.CRQ_diet_mamm_FP = float(form.getvalue('CRQ_diet_mamm_FP'))
        risk_output.ARQ_diet_mamm_AR = float(form.getvalue('ARQ_diet_mamm_AR'))
        risk_output.CRQ_diet_mamm_AR = float(form.getvalue('CRQ_diet_mamm_AR'))
        risk_output.LD50_rg_bird_sm = float(form.getvalue('LD50_rg_bird_sm'))
        risk_output.LD50_rg_bird_md = float(form.getvalue('LD50_rg_bird_md'))
        risk_output.LD50_rg_bird_lg = float(form.getvalue('LD50_rg_bird_lg'))
        risk_output.LD50_rg_mamm_sm = float(form.getvalue('LD50_rg_mamm_sm'))
        risk_output.LD50_rg_mamm_md = float(form.getvalue('LD50_rg_mamm_md'))
        risk_output.LD50_rg_mamm_lg = float(form.getvalue('LD50_rg_mamm_lg'))
        risk_output.LD50_rl_bird_sm = float(form.getvalue('LD50_rl_bird_sm'))
        risk_output.LD50_rl_bird_md = float(form.getvalue('LD50_rl_bird_md'))
        risk_output.LD50_rl_bird_lg = float(form.getvalue('LD50_rl_bird_lg'))
        risk_output.LD50_rl_mamm_sm = float(form.getvalue('LD50_rl_mamm_sm'))
        risk_output.LD50_rl_mamm_md = float(form.getvalue('LD50_rl_mamm_md'))
        risk_output.LD50_rl_mamm_lg = float(form.getvalue('LD50_rl_mamm_lg'))
        risk_output.LD50_bg_bird_sm = float(form.getvalue('LD50_bg_bird_sm'))
        risk_output.LD50_bg_bird_md = float(form.getvalue('LD50_bg_bird_md'))
        risk_output.LD50_bg_bird_lg = float(form.getvalue('LD50_bg_bird_lg'))
        risk_output.LD50_bg_mamm_sm = float(form.getvalue('LD50_bg_mamm_sm'))
        risk_output.LD50_bg_mamm_md = float(form.getvalue('LD50_bg_mamm_md'))
        risk_output.LD50_bg_mamm_lg = float(form.getvalue('LD50_bg_mamm_lg'))
        risk_output.LD50_bl_bird_sm = float(form.getvalue('LD50_bl_bird_sm'))
        risk_output.LD50_bl_bird_md = float(form.getvalue('LD50_bl_bird_md'))
        risk_output.LD50_bl_bird_lg = float(form.getvalue('LD50_bl_bird_lg'))
        risk_output.LD50_bl_mamm_sm = float(form.getvalue('LD50_bl_mamm_sm'))
        risk_output.LD50_bl_mamm_md = float(form.getvalue('LD50_bl_mamm_md'))
        risk_output.LD50_bl_mamm_lg = float(form.getvalue('LD50_bl_mamm_lg'))
        use.put()
        self.redirect("pesticide_properties.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolUseConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()