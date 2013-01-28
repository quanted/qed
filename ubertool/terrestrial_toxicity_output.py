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
        terr_tox = TerrestrialToxicity(key_name="config_name")
        user = users.get_current_user()
        if user:
            logger.info(user.user_id())
            terr_tox.user = user
        terr_tox.config_name = config_name
        terr_tox.avian_ld50 = float(form.getvalue('avian_ld50'))
        terr_tox.avian_lc50 = float(form.getvalue('avian_lc50'))
        terr_tox.avian_NOAEC = float(form.getvalue('avian_NOAEC'))
        terr_tox.avian_NOAEL = float(form.getvalue('avian_NOAEL'))
        terr_tox.body_weight_of_the_assessed_bird = float(form.getvalue('body_weight_of_the_assessed_bird'))
        terr_tox.body_weight_of_the_assessed_bird = float(form.getvalue('body_weight_of_the_assessed_bird'))
        terr_tox.mineau_scaling_factor = float(form.getvalue('mineau_scaling_factor'))
        terr_tox.mammalian_ld50 = float(form.getvalue('mammalian_ld50'))
        terr_tox.mammalian_lc50 = float(form.getvalue('mammalian_lc50'))
        terr_tox.mammalian_inhalation_lc50 = float(form.getvalue('mammalian_inhalation_lc50'))
        terr_tox.duration_of_rat_study = float(form.getvalue('duration_of_rat_study'))
        terr_tox.mammlian_NOAEC = float(form.getvalue('mammlian_NOAEC'))
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
        terr_tox.taxonomic_group = str(form.getvalue('taxonomic_group'))
        terr_tox.eat_mammals = str(form.getvalue('eat_mammals'))
        terr_tox.eat_amphibians_reptiles = str(form.getvalue('eat_amphibians_reptiles'))
        terr_tox.put()
        q = db.Query(TerrestrialToxicity)
        for new_use in q:
            logger.info(new_use.to_xml())
        self.redirect("ecosystem_inputs.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolTerrestrialToxicityConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

