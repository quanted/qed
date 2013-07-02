import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import sys
sys.path.append("../utils")
sys.path.append('../CAS')
from CAS.CASGql import CASGql
import logging

class Use(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    gran_bird_ex_derm_dose = db.FloatProperty()
    gran_reamp_ex_derm_dose = db.FloatProperty()
    gran_mam_ex_derm_dose = db.FloatProperty()
    fol_bird_ex_derm_dose = db.FloatProperty()
    fol_repamp_ex_derm_dose = db.FloatProperty()
    fol_mam_ex_derm_dose = db.FloatProperty()
    bgs_bird_ex_derm_dose = db.FloatProperty()
    bgs_repamp_ex_derm_dose = db.FloatProperty()
    bgs_mam_ex_derm_dose = db.FloatProperty()
    ratio_gran_bird = db.FloatProperty()
    LOC_gran_bird = db.FloatProperty()
    ratio_gran_rep = db.FloatProperty()
    LOC_gran_rep = db.FloatProperty()
    ratio_gran_amp = db.FloatProperty()
    LOC_gran_amp = db.FloatProperty()
    ratio_gran_mam = db.FloatProperty()
    LOC_gran_mam = db.FloatProperty()
    ratio_fol_bird = db.FloatProperty()
    LOC_fol_bird = db.FloatProperty()
    ratio_fol_rep = db.FloatProperty()
    LOC_fol_rep = db.FloatProperty()
    ratio_fol_amp = db.FloatProperty()
    LOC_fol_amp = db.FloatProperty()
    ratio_fol_mam = db.FloatProperty()
    LOC_fol_mam = db.FloatProperty()
    ratio_bgs_bird = db.FloatProperty()
    LOC_bgs_bird = db.FloatProperty()
    ratio_bgs_rep = db.FloatProperty()
    LOC_bgs_rep = db.FloatProperty()
    ratio_bgs_amp = db.FloatProperty()
    LOC_bgs_amp = db.FloatProperty()
    ratio_bgs_mam = db.FloatProperty()
    LOC_bgs_mam = db.FloatProperty()


