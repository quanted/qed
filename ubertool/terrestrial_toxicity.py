import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
from google.appengine.api import users


class TerrestrialToxicityService(webapp.RequestHandler):
    def get(self, terr_tox):
        user = users.get_current_user()
        q = db.Query(TerrestrialToxicity)
        q.filter('user =',user)
        q.filter('config_name =',terr_tox)
        terrestrial = q.get()
        terrestrial_dict = {}
        terrestrial_dict['avian_lc50'] = None
        if terrestrial.avian_lc50 != None:
            terrestrial_dict['avian_lc50'] = terrestrial.avian_lc50
        terrestrial_dict['avian_ld50'] = None
        if terrestrial.avian_ld50 != None:
            terrestrial_dict['avian_ld50'] = terrestrial.avian_ld50
        terrestrial_dict['avian_NOAEC'] = None
        if terrestrial.avian_NOAEC != None:
            terrestrial_dict['avian_NOAEC'] = terrestrial.avian_NOAEC
        terrestrial_dict['avian_NOAEL'] = None
        if terrestrial.avian_NOAEL != None:
            terrestrial_dict['avian_NOAEL'] = terrestrial.avian_NOAEL
        terrestrial_dict['body_weight_of_the_assessed_bird'] = None
        if terrestrial.body_weight_of_the_assessed_bird != None:
            terrestrial_dict['body_weight_of_the_assessed_bird'] = terrestrial.body_weight_of_the_assessed_bird
        terrestrial_dict['mineau_scaling_factor'] = None
        if terrestrial.mineau_scaling_factor != None:
            terrestrial_dict['mineau_scaling_factor'] = terrestrial.mineau_scaling_factor
        terrestrial_dict['mammalian_ld50'] = None
        if terrestrial.mammalian_ld50 != None:
            terrestrial_dict['mammalian_ld50'] = terrestrial.mammalian_ld50
        terrestrial_dict['mammalian_lc50'] = None
        if terrestrial.mammalian_lc50 != None:
            terrestrial_dict['mammalian_lc50'] = terrestrial.mammalian_lc50
        terrestrial_dict['mammalian_inhalation_lc50'] = None
        if terrestrial.mammalian_inhalation_lc50 != None:
            terrestrial_dict['mammalian_inhalation_lc50'] = terrestrial.mammalian_inhalation_lc50
        terrestrial_dict['duration_of_rat_study'] = None
        if terrestrial.duration_of_rat_study != None:
            terrestrial_dict['duration_of_rat_study'] = terrestrial.duration_of_rat_study
        terrestrial_dict['mammalian_NOAEC'] = None
        if terrestrial.mammalian_NOAEC != None:
            terrestrial_dict['mammalian_NOAEC'] = terrestrial.mammalian_NOAEC
        terrestrial_dict['mammalian_NOAEL'] = None
        if terrestrial.mammalian_NOAEL != None:
            terrestrial_dict['mammalian_NOAEL'] = terrestrial.mammalian_NOAEL
        terrestrial_dict['amphibian_bw'] = None
        if terrestrial.amphibian_bw != None:
            terrestrial_dict['amphibian_bw'] = terrestrial.amphibian_bw
        terrestrial_dict['terrestrial_phase_amphibian_ld50'] = None
        if terrestrial.terrestrial_phase_amphibian_ld50 != None:
            terrestrial_dict['terrestrial_phase_amphibian_ld50'] = terrestrial.terrestrial_phase_amphibian_ld50
        terrestrial_dict['terrestrial_phase_amphibian_lc50'] = None
        if terrestrial.terrestrial_phase_amphibian_lc50 != None:
            terrestrial_dict['terrestrial_phase_amphibian_lc50'] = terrestrial.terrestrial_phase_amphibian_lc50
        terrestrial_dict['terrestrial_phase_amphibian_NOAEC'] = None
        if terrestrial.terrestrial_phase_amphibian_NOAEC != None:
            terrestrial_dict['terrestrial_phase_amphibian_NOAEC'] = terrestrial.terrestrial_phase_amphibian_NOAEC
        terrestrial_dict['terrestrial_phase_amphibian_NOAEL'] = None
        if terrestrial.terrestrial_phase_amphibian_NOAEL != None:
            terrestrial_dict['terrestrial_phase_amphibian_NOAEL'] = terrestrial.terrestrial_phase_amphibian_NOAEL
        terrestrial_dict['reptile_bw'] = None
        if terrestrial.reptile_bw != None:
            terrestrial_dict['reptile_bw'] = terrestrial.reptile_bw
        terrestrial_dict['terrestrial_phase_reptile_ld50'] = None
        if terrestrial.terrestrial_phase_reptile_ld50 != None:
            terrestrial_dict['terrestrial_phase_reptile_ld50'] = terrestrial.terrestrial_phase_reptile_ld50
        terrestrial_dict['terrestrial_phase_reptile_lc50'] = None
        if terrestrial.terrestrial_phase_reptile_lc50 != None:
            terrestrial_dict['terrestrial_phase_reptile_lc50'] = terrestrial.terrestrial_phase_reptile_lc50
        terrestrial_dict['terrestrial_phase_reptile_NOAEC'] = None
        if terrestrial.terrestrial_phase_reptile_NOAEC != None:
            terrestrial_dict['terrestrial_phase_reptile_NOAEC'] = terrestrial.terrestrial_phase_reptile_NOAEC
        terrestrial_dict['terrestrial_phase_reptile_NOAEL'] = None
        if terrestrial.terrestrial_phase_reptile_NOAEL != None:
            terrestrial_dict['terrestrial_phase_reptile_NOAEL'] = terrestrial.terrestrial_phase_reptile_NOAEL
        terrestrial_dict['EC25_for_nonlisted_seedling_emergence_monocot'] = None
        if terrestrial.EC25_for_nonlisted_seedling_emergence_monocot != None:
            terrestrial_dict['EC25_for_nonlisted_seedling_emergence_monocot'] = terrestrial.EC25_for_nonlisted_seedling_emergence_monocot
        terrestrial_dict['EC25_for_nonlisted_seedling_emergence_dicot'] = None
        if terrestrial.EC25_for_nonlisted_seedling_emergence_dicot != None:
            terrestrial_dict['EC25_for_nonlisted_seedling_emergence_dicot'] = terrestrial.EC25_for_nonlisted_seedling_emergence_dicot
        terrestrial_dict['NOAEC_for_listed_seedling_emergence_monocot'] = None
        if terrestrial.NOAEC_for_listed_seedling_emergence_monocot != None:
            terrestrial_dict['NOAEC_for_listed_seedling_emergence_monocot'] = terrestrial.NOAEC_for_listed_seedling_emergence_monocot
        terrestrial_dict['NOAEC_for_listed_seedling_emergence_dicot'] = None
        if terrestrial.NOAEC_for_listed_seedling_emergence_dicot != None:
            terrestrial_dict['NOAEC_for_listed_seedling_emergence_dicot'] = terrestrial.NOAEC_for_listed_seedling_emergence_dicot
        terrestrial_dict['EC25_for_nonlisted_vegetative_vigor_monocot'] = None
        if terrestrial.EC25_for_nonlisted_vegetative_vigor_monocot != None:
            terrestrial_dict['EC25_for_nonlisted_vegetative_vigor_monocot'] = terrestrial.EC25_for_nonlisted_vegetative_vigor_monocot
        terrestrial_dict['EC25_for_nonlisted_vegetative_vigor_dicot'] = None
        if terrestrial.EC25_for_nonlisted_vegetative_vigor_dicot != None:
            terrestrial_dict['EC25_for_nonlisted_vegetative_vigor_dicot'] = terrestrial.EC25_for_nonlisted_vegetative_vigor_dicot
        terrestrial_dict['NOAEC_for_listed_vegetative_vigor_monocot'] = None
        if terrestrial.NOAEC_for_listed_vegetative_vigor_monocot != None:
            terrestrial_dict['NOAEC_for_listed_vegetative_vigor_monocot'] = terrestrial.NOAEC_for_listed_vegetative_vigor_monocot
        terrestrial_dict['NOAEC_for_listed_vegetative_vigor_dicot'] = None
        if terrestrial.NOAEC_for_listed_vegetative_vigor_dicot != None:
            terrestrial_dict['NOAEC_for_listed_vegetative_vigor_dicot'] = terrestrial.NOAEC_for_listed_vegetative_vigor_dicot
        terrestrial_dict['Small_medium_and_large_BW_of_assessed_herptile_listed_species'] = None
        if terrestrial.Small_medium_and_large_BW_of_assessed_herptile_listed_species != None:
            terrestrial_dict['Small_medium_and_large_BW_of_assessed_herptile_listed_species'] = terrestrial.Small_medium_and_large_BW_of_assessed_herptile_listed_species
        terrestrial_dict['percent_water_content_of_small_med_large_herptile_species_diet'] = None
        if terrestrial.percent_water_content_of_small_med_large_herptile_species_diet != None:
            terrestrial_dict['percent_water_content_of_small_med_large_herptile_species_diet'] = terrestrial.percent_water_content_of_small_med_large_herptile_species_diet
        terrestrial_dict['taxonomic_group'] = None
        if terrestrial.taxonomic_group != None:
            terrestrial_dict['taxonomic_group'] = terrestrial.taxonomic_group
        terrestrial_dict['eat_mammals'] = None
        if terrestrial.eat_mammals != None:
            terrestrial_dict['eat_mammals'] = terrestrial.eat_mammals
        terrestrial_dict['eat_amphibians_reptiles'] = None
        if terrestrial.eat_amphibians_reptiles != None:
            terrestrial_dict['eat_amphibians_reptiles'] = terrestrial.eat_amphibians_reptiles

        use_json = simplejson.dumps(terrestrial_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(use_json)

class TerrestrialPropertiesRetrievalService(webapp.RequestHandler):
    
    def get(self, terrestrial_config_name):
        user = users.get_current_user()
        q = db.Query(TerrestrialToxicity)
        q.filter('user =',user)
        q.filter('config_name =',terrestrial_config_name)
        terrestrial = q.get()
        terrestrial_dict = {}
        terrestrial_dict['avian_lc50'] = terrestrial.avian_lc50
        terrestrial_dict['avian_ld50'] = terrestrial.avian_ld50
        terrestrial_dict['avian_NOAEC'] = terrestrial.avian_NOAEC
        terrestrial_dict['avian_NOAEL'] = terrestrial.avian_NOAEL
        terrestrial_dict['body_weight_of_the_assessed_bird'] = terrestrial.body_weight_of_the_assessed_bird
        terrestrial_dict['mineau_scaling_factor'] = terrestrial.mineau_scaling_factor
        terrestrial_dict['mammalian_ld50'] = terrestrial.mammalian_ld50
        terrestrial_dict['mammalian_lc50'] = terrestrial.mammalian_lc50
        terrestrial_dict['mammalian_inhalation_lc50'] = terrestrial.mammalian_inhalation_lc50
        terrestrial_dict['duration_of_rat_study'] = terrestrial.duration_of_rat_study
        terrestrial_dict['mammalian_NOAEC'] = terrestrial.mammalian_NOAEC
        terrestrial_dict['mammalian_NOAEL'] = terrestrial.mammalian_NOAEL
        terrestrial_dict['amphibian_bw'] = terrestrial.amphibian_bw
        terrestrial_dict['terrestrial_phase_amphibian_ld50'] = terrestrial.terrestrial_phase_amphibian_ld50
        terrestrial_dict['terrestrial_phase_amphibian_lc50'] = terrestrial.terrestrial_phase_amphibian_lc50
        terrestrial_dict['terrestrial_phase_amphibian_NOAEC'] = terrestrial.terrestrial_phase_amphibian_NOAEC
        terrestrial_dict['terrestrial_phase_amphibian_NOAEL'] = terrestrial.terrestrial_phase_amphibian_NOAEL
        terrestrial_dict['reptile_bw'] = terrestrial.reptile_bw
        terrestrial_dict['terrestrial_phase_reptile_ld50'] = terrestrial.terrestrial_phase_reptile_ld50
        terrestrial_dict['terrestrial_phase_reptile_lc50'] = terrestrial.terrestrial_phase_reptile_lc50
        terrestrial_dict['terrestrial_phase_reptile_NOAEL'] = terrestrial.terrestrial_phase_reptile_NOAEL
        terrestrial_dict['terrestrial_phase_reptile_NOAEC'] = terrestrial.terrestrial_phase_reptile_NOAEC
        terrestrial_dict['EC25_for_nonlisted_seedling_emergence_monocot'] = terrestrial.EC25_for_nonlisted_seedling_emergence_monocot
        terrestrial_dict['EC25_for_nonlisted_seedling_emergence_dicot'] = terrestrial.EC25_for_nonlisted_seedling_emergence_dicot
        terrestrial_dict['NOAEC_for_listed_seedling_emergence_monocot'] = terrestrial.NOAEC_for_listed_seedling_emergence_monocot
        terrestrial_dict['NOAEC_for_listed_seedling_emergence_monocot'] = terrestrial.NOAEC_for_listed_seedling_emergence_monocot
        terrestrial_dict['EC25_for_nonlisted_vegetative_vigor_monocot'] = terrestrial.EC25_for_nonlisted_vegetative_vigor_monocot
        terrestrial_dict['EC25_for_nonlisted_vegetative_vigor_dicot'] = terrestrial.EC25_for_nonlisted_vegetative_vigor_dicot
        terrestrial_dict['NOAEC_for_listed_vegetative_vigor_monocot'] = terrestrial.NOAEC_for_listed_vegetative_vigor_monocot
        terrestrial_dict['NOAEC_for_listed_vegetative_vigor_dicot'] = terrestrial.NOAEC_for_listed_vegetative_vigor_dicot
        terrestrial_dict['Small_medium_and_large_BW_of_assessed_herptile_listed_species'] = terrestrial.Small_medium_and_large_BW_of_assessed_herptile_listed_species
        terrestrial_dict['percent_water_content_of_small_med_large_herptile_species_diet'] = terrestrial.percent_water_content_of_small_med_large_herptile_species_diet
        terrestrial_dict['taxonomic_group'] = terrestrial.taxonomic_group
        terrestrial_dict['eat_mammals'] = terrestrial.eat_mammals
        terrestrial_dict['eat_amphibians_reptiles'] = terrestrial.eat_amphibians_reptiles
        return terrestrial_dict
    
class TerrestrialToxicityConfigNamesService(webapp.RequestHandler):
    
    def get(self):
        logger = logging.getLogger("TerrestrialToxicityConfigNamesService")
        user = users.get_current_user()
        q = db.Query(TerrestrialToxicity)
        q.filter('user =',user)
        terras = q.run()
        terra_config_names = []
        for terra in terras:
            terra_config_names.append(terra.config_name)
        terra_dict = {}
        terra_dict['config_names'] = terra_config_names
        terra_json = simplejson.dumps(terra_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(terra_json)

class TerrestrialToxicity(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
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
    
application = webapp.WSGIApplication([('/terrestrial/(.*)', TerrestrialToxicityService),
                                      ('/terra-config-names', TerrestrialToxicityConfigNamesService)],
                                      debug=True)

def main():
  	run_wsgi_app(application)

if __name__ == "__main__":
  	main()