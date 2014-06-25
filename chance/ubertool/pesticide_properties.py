import google.appengine.ext.db as db
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import sys
import logging

class PesticideProperties(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    chemical_name = db.StringProperty()
    Formulated_product_name = db.StringProperty()
    seed_treatment_formulation_name = db.StringProperty()
    label_epa_reg_no = db.StringProperty()
    molecular_weight = db.FloatProperty()
    percent_ai = db.FloatProperty() 
    henrys_law_constant = db.FloatProperty()
    vapor_pressure = db.FloatProperty()
    solubility = db.FloatProperty()
    Kd = db.FloatProperty()
    photolysis = db.FloatProperty()
    aerobic_aquatic_metabolism = db.FloatProperty()
    anaerobic_aquatic_metabolism = db.FloatProperty()
    aerobic_soil_metabolism = db.FloatProperty() 
    hydrolysis_ph5 = db.FloatProperty()
    hydrolysis_ph7 = db.FloatProperty()
    hydrolysis_ph9 = db.FloatProperty()
    foliar_extraction = db.FloatProperty()
    foliar_decay_rate = db.FloatProperty()
    Foliar_dissipation_half_life = db.FloatProperty()
    density_of_product = db.FloatProperty()
    row_sp = db.FloatProperty()
    maximum_seedling_rate_per_use = db.FloatProperty()
    bandwith = db.FloatProperty()
    day_out = db.FloatProperty()
    use = db.FloatProperty()
    seed_crop = db.FloatProperty()
    Application_type = db.FloatProperty()
    n_a = db.FloatProperty()
    ar_lb = db.FloatProperty()
    percent_incorporated = db.FloatProperty()
    l_kow = db.FloatProperty()
    k_oc = db.FloatProperty()
    c_wdp = db.FloatProperty()
    water_column_EEC = db.FloatProperty()
    created = db.DateTimeProperty(auto_now_add=True)
