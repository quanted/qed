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

class Use_metadata(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    percent_ai = db.FloatProperty()
    seed_treatment_formulation_name = forms.CharField(label="Seed Treatment Formulation Name", initial="")
    density_of_product = db.FloatProperty()
    maximum_seedling_rate_per_use = db.FloatProperty()
    use = forms.CharField(label="Use", initial="")
    seed_crop = forms.CharField(label="Crop Use")
    application_type = forms.CharField(label="Application Type", initial="")
    n_a = db.FloatProperty()
    ar_lb = db.FloatProperty()
    row_sp = db.FloatProperty()
    bandwidth = db.FloatProperty()
    foliar_dissipation_half_life = db.FloatProperty()
    frac_pest_surface = db.FloatProperty()
    day_out = db.FloatProperty()
    aerobic_aquatic_metabolism = db.FloatProperty()
    anaerobic_aquatic_metabolism = db.FloatProperty()
    aerobic_soil_metabolism = db.FloatProperty()
    foliar_extraction = db.FloatProperty()
    foliar_decay_rate = db.FloatProperty()
    foliar_dissipation_half_life = db.FloatProperty()
    application_method = db.StringProperty()
    application_form = db.StringProperty()
