import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class TerrestrialToxicityService(webapp.RequestHandler):
    def get(self, terr_tox):
        user = users.get_current_user()
        q = db.Query(TerrestrialToxicity)
        q.filter('user =',user)
        q.filter('config_name =',terr_tox)
        terr = q.get()
        use_dict = {}
        use_dict['avian_ld50']=terr.avian_ld50
        use_dict['avian_lc50']=terr.avian_lc50
        use_dict['avian_NOAEC']=terr.avian_NOAEC
        use_dict['avian_NOAEL']=terr.avian_NOAEL
        use_dict['body_weight_of_the_assessed_bird']=terr.body_weight_of_the_assessed_bird
        use_dict['mineau_scaling_factor']=terr.mineau_scaling_factor
        use_dict['mammalian_ld50']=terr.mammalian_ld50
        use_dict['mammalian_lc50']=terr.mammalian_lc50
        use_dict['mammalian_inhalation_lc50']=terr.mammalian_inhalation_lc50
        use_dict['duration_of_rat_study']=terr.duration_of_rat_study
        use_dict['mammlian_NOAEC']=terr.mammlian_NOAEC
        use_dict['mammalian_NOAEL']=terr.mammalian_NOAEL
        use_dict['amphibian_bw']=terr.amphibian_bw
        use_dict['terrestrial_phase_amphibian_ld50']=terr.terrestrial_phase_amphibian_ld50
        use_dict['terrestrial_phase_amphibian_lc50']=terr.terrestrial_phase_amphibian_lc50
        use_dict['terrestrial_phase_amphibian_NOAEC']=terr.terrestrial_phase_amphibian_NOAEC
        use_dict['terrestrial_phase_amphibian_NOAEL']=terr.terrestrial_phase_amphibian_NOAEL
        use_dict['reptile_bw']=terr.reptile_bw
        use_dict['terrestrial_phase_reptile_ld50']=terr.terrestrial_phase_reptile_ld50
        use_dict['terrestrial_phase_reptile_lc50']=terr.terrestrial_phase_reptile_lc50
        use_dict['terrestrial_phase_reptile_NOAEC']=terr.terrestrial_phase_reptile_NOAEC
        use_dict['terrestrial_phase_reptile_NOAEL']=terr.terrestrial_phase_reptile_NOAEL
        use_dict['EC25_for_nonlisted_seedling_emergence_monocot']=terr.EC25_for_nonlisted_seedling_emergence_monocot
        use_dict['EC25_for_nonlisted_seedling_emergence_dicot']=terr.EC25_for_nonlisted_seedling_emergence_dicot
        use_dict['NOAEC_for_listed_seedling_emergence_monocot']=terr.NOAEC_for_listed_seedling_emergence_monocot
        use_dict['NOAEC_for_listed_seedling_emergence_dicot']=terr.NOAEC_for_listed_seedling_emergence_dicot
        use_dict['EC25_for_nonlisted_vegetative_vigor_monocot']=terr.EC25_for_nonlisted_vegetative_vigor_monocot
        use_dict['EC25_for_nonlisted_vegetative_vigor_dicot']=terr.EC25_for_nonlisted_vegetative_vigor_dicot
        use_dict['NOAEC_for_listed_vegetative_vigor_monocot']=terr.NOAEC_for_listed_vegetative_vigor_monocot
        use_dict['NOAEC_for_listed_vegetative_vigor_dicot']=terr.NOAEC_for_listed_vegetative_vigor_dicot
        use_dict['Small_medium_and_large_BW_of_assessed_herptile_listed_species']=terr.Small_medium_and_large_BW_of_assessed_herptile_listed_species
        use_dict['percent_water_content_of_small_med_large_herptile_species_diet']=terr.percent_water_content_of_small_med_large_herptile_species_diet
        use_dict['taxonomic_group']=terr.taxonomic_group
        use_dict['eat_mammals']=terr.eat_mammals
        use_dict['eat_amphibians_reptiles']=terr.eat_amphibians_reptiles

        use_json = simplejson.dumps(use_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(use_json)

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
    mammlian_NOAEC = db.FloatProperty()
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

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()