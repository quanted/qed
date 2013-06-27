import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
from google.appengine.api import users

class TerrestrialToxicity(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    low_bird_acute_oral_ld50 = db.FloatProperty()
    avian_ld50 = db.FloatProperty()
    avian_lc50 = db.FloatProperty()
    avian_NOAEC = db.FloatProperty()
    avian_NOAEL = db.FloatProperty()
    body_weight_of_the_assessed_bird = db.FloatProperty()
    mineau_scaling_factor = db.FloatProperty()
    mammalian_ld50 = db.FloatProperty()
    mammalian_lc50 = db.FloatProperty()
    mammalian_inhalation_lc50 = db.FloatProperty()
    duration_of_rat_study = db.FloatProperty()
    mammalian_NOAEC = db.FloatProperty()
    mammalian_NOAEL = db.FloatProperty()
    amphibian_bw = db.FloatProperty()    
    terrestrial_phase_amphibian_ld50 = db.FloatProperty()
    terrestrial_phase_amphibian_lc50 = db.FloatProperty()
    terrestrial_phase_amphibian_NOAEC = db.FloatProperty()
    terrestrial_phase_amphibian_NOAEL = db.FloatProperty()
    reptile_bw = db.FloatProperty()     
    terrestrial_phase_reptile_ld50 = db.FloatProperty()
    terrestrial_phase_reptile_lc50 = db.FloatProperty()
    terrestrial_phase_reptile_NOAEC = db.FloatProperty()
    terrestrial_phase_reptile_NOAEL = db.FloatProperty()
    EC25_for_nonlisted_seedling_emergence_monocot = db.FloatProperty()
    EC25_for_nonlisted_seedling_emergence_dicot = db.FloatProperty()
    NOAEC_for_listed_seedling_emergence_monocot = db.FloatProperty()
    NOAEC_for_listed_seedling_emergence_dicot = db.FloatProperty()
    EC25_for_nonlisted_vegetative_vigor_monocot = db.FloatProperty()
    EC25_for_nonlisted_vegetative_vigor_dicot = db.FloatProperty()
    NOAEC_for_listed_vegetative_vigor_monocot = db.FloatProperty()
    NOAEC_for_listed_vegetative_vigor_dicot = db.FloatProperty()
    Small_medium_and_large_BW_of_assessed_herptile_listed_species = db.FloatProperty()
    percent_water_content_of_small_med_large_herptile_species_diet = db.FloatProperty()    
    taxonomic_group = db.StringProperty()    
    eat_mammals = db.StringProperty()
    eat_amphibians_reptiles = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
