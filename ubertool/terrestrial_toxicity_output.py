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
from ubertool.terrestrial_toxicity import TerrestrialToxicity
import logging


class UbertoolTerrestrialToxicityConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("UbertoolTerrestrialToxicityConfigurationPage")
        form = cgi.FieldStorage()
        config_name = str(form.getvalue('config_name'))
        user = users.get_current_user()
        q = db.Query(TerrestrialToxicity)
        q.filter('user =',user)
        q.filter("config_name =", config_name)        
        terr_tox = q.get()
        if terr_tox is None:
            terr_tox = TerrestrialToxicity()
        if user:
            logger.info(user.user_id())
            terr_tox.user = user
        terr_tox = TerrestrialToxicity()
        if user:
            logger.info(user.user_id())
            terr_tox.user = user
        terr_tox.config_name = config_name
        terr_tox.avian_ld50 = float(form.getvalue('avian_ld50'))
        terr_tox.low_bird_acute_oral_ld50 = float(form.getvalue('low_bird_acute_oral_ld50'))
        terr_tox.mamm_acute_derm_ld50 = float(form.getvalue('mamm_acute_derm_ld50'))
        terr_tox.bird_acute_oral_study = float(form.getvalue('bird_acute_oral_study'))
        terr_tox.mamm_acute_derm_study = float(form.getvalue('mamm_acute_derm_study'))
        terr_tox.bird_study_add_comm = float(form.getvalue('bird_study_add_comm'))
        terr_tox.Species_of_the_tested_bird = float(form.getvalue('Species_of_the_tested_bird'))
        terr_tox.Species_of_the_tested_bird_avian_LD50 = float(form.getvalue('Species_of_the_tested_bird_avian_LD50'))
        terr_tox.Species_of_the_tested_bird_avian_LC50 = float(form.getvalue('Species_of_the_tested_bird_avian_LC50'))
        terr_tox.Species_of_the_tested_bird_avian_NOAEC = float(form.getvalue('Species_of_the_tested_bird_avian_NOAEC'))
        terr_tox.Species_of_the_tested_bird_avian_NOAEL = float(form.getvalue('Species_of_the_tested_bird_avian_NOAEL'))
        terr_tox.mamm_study_add_comm = float(form.getvalue('mamm_study_add_comm'))
        terr_tox.avian_lc50 = float(form.getvalue('avian_lc50'))
        terr_tox.avian_NOAEC = float(form.getvalue('avian_NOAEC'))
        terr_tox.avian_NOAEL = float(form.getvalue('avian_NOAEL'))
        terr_tox.tested_bird_body_weight = float(form.getvalue('tested_bird_body_weight'))
        terr_tox.m_species = float(form.getvalue('m_species'))
        terr_tox.tested_mamm_body_weight = float(form.getvalue('tested_mamm_body_weight'))
        terr_tox.body_weight_of_the_assessed_bird = float(form.getvalue('body_weight_of_the_assessed_bird'))
        terr_tox.body_weight_of_the_assessed_bird_sm = float(form.getvalue('body_weight_of_the_assessed_bird_sm'))
        terr_tox.body_weight_of_the_assessed_bird_md = float(form.getvalue('body_weight_of_the_assessed_bird_md'))
        terr_tox.body_weight_of_the_assessed_bird_lg = float(form.getvalue('body_weight_of_the_assessed_bird_lg'))
        terr_tox.body_weight_of_the_assessed_mammal_sm = float(form.getvalue('body_weight_of_the_assessed_mammal_sm'))
        terr_tox.body_weight_of_the_assessed_mammal_md = float(form.getvalue('body_weight_of_the_assessed_mammal_md'))
        terr_tox.body_weight_of_the_assessed_mammal_lg = float(form.getvalue('body_weight_of_the_assessed_mammal_lg'))
        terr_tox.bw_quail = float(form.getvalue('bw_quail'))
        terr_tox.bw_duck = float(form.getvalue('bw_duck'))
        terr_tox.bwb_other = float(form.getvalue('bwb_other'))
        terr_tox.mineau_scaling_factor = float(form.getvalue('mineau_scaling_factor'))
        terr_tox.mammalian_ld50 = float(form.getvalue('mammalian_ld50'))
        terr_tox.mammalian_lc50 = float(form.getvalue('mammalian_lc50'))
        terr_tox.mammalian_inhalation_lc50 = float(form.getvalue('mammalian_inhalation_lc50'))
        terr_tox.duration_of_rat_study = float(form.getvalue('duration_of_rat_study'))
        terr_tox.mammalian_chronic_endpoint = float(form.getvalue('mammalian_chronic_endpoint'))
        terr_tox.mammalian_NOAEC = float(form.getvalue('mammalian_NOAEC'))
        terr_tox.mammalian_NOAEL = float(form.getvalue('mammalian_NOAEL'))
        terr_tox.amphibian_bw = float(form.getvalue('amphibian_bw'))
        terr_tox.terrestrial_phase_amphibian_ld50 = float(form.getvalue('terrestrial_phase_amphibian_ld50'))
        terr_tox.terrestrial_phase_amphibian_lc50 = float(form.getvalue('terrestrial_phase_amphibian_lc50'))
        terr_tox.terrestrial_phase_amphibian_NOAEC = float(form.getvalue('terrestrial_phase_amphibian_NOAEC'))
        terr_tox.terrestrial_phase_amphibian_NOAEL = float(form.getvalue('terrestrial_phase_amphibian_NOAEL'))
        terr_tox.reptile_bw = float(form.getvalue('reptile_bw'))
        terr_tox.terrestrial_phase_reptile_ld50 = float(form.getvalue('terrestrial_phase_reptile_ld50'))
        terr_tox.terrestrial_phase_reptile_lc50 = float(form.getvalue('terrestrial_phase_reptile_lc50'))
        terr_tox.terrestrial_phase_reptile_NOAEC = float(form.getvalue('terrestrial_phase_reptile_NOAEC'))
        terr_tox.terrestrial_phase_reptile_NOAEL = float(form.getvalue('terrestrial_phase_reptile_NOAEL'))
        terr_tox.EC25_for_nonlisted_seedling_emergence_monocot = float(form.getvalue('EC25_for_nonlisted_seedling_emergence_monocot'))
        terr_tox.EC25_for_nonlisted_seedling_emergence_dicot = float(form.getvalue('EC25_for_nonlisted_seedling_emergence_dicot'))
        terr_tox.NOAEC_for_listed_seedling_emergence_monocot = float(form.getvalue('NOAEC_for_listed_seedling_emergence_monocot'))
        terr_tox.NOAEC_for_listed_seedling_emergence_dicot = float(form.getvalue('NOAEC_for_listed_seedling_emergence_dicot'))
        terr_tox.EC25_for_nonlisted_vegetative_vigor_monocot = float(form.getvalue('EC25_for_nonlisted_vegetative_vigor_monocot'))
        terr_tox.EC25_for_nonlisted_vegetative_vigor_dicot = float(form.getvalue('EC25_for_nonlisted_vegetative_vigor_dicot'))
        terr_tox.NOAEC_for_listed_vegetative_vigor_monocot = float(form.getvalue('NOAEC_for_listed_vegetative_vigor_monocot'))
        terr_tox.NOAEC_for_listed_vegetative_vigor_dicot = float(form.getvalue('NOAEC_for_listed_vegetative_vigor_dicot'))
        terr_tox.Small_medium_and_large_BW_of_assessed_herptile_listed_species = float(form.getvalue('Small_medium_and_large_BW_of_assessed_herptile_listed_species'))
        terr_tox.percent_water_content_of_small_med_large_herptile_species_diet = float(form.getvalue('percent_water_content_of_small_med_large_herptile_species_diet'))    
        terr_tox.desired_threshold = float(form.getvalue('desired_threshold'))
        terr_tox.slope_of_dose_response = float(form.getvalue('slope_of_dose_response'))
        terr_tox.ld50_a = float(form.getvalue('ld50_a'))
        terr_tox.ld50_m = float(form.getvalue('ld50_m'))
        terr_tox.bw_rat = float(form.getvalue('bw_rat'))
        terr_tox.bwm_other = float(form.getvalue('bwm_other'))
        terr_tox.taxonomic_group = str(form.getvalue('taxonomic_group'))
        terr_tox.eat_mammals = str(form.getvalue('eat_mammals'))
        terr_tox.eat_amphibians_reptiles = str(form.getvalue('eat_amphibians_reptiles'))
        terr_tox.put()
        self.redirect("ecosystem_inputs.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolTerrestrialToxicityConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

