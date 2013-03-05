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
from ubertool.aquatic_toxicity import AquaticToxicity
import logging


class UbertoolAquaticToxicityConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("UbertoolAquaticToxicityConfigurationPage")
        form = cgi.FieldStorage()
        config_name = str(form.getvalue('config_name'))
        user = users.get_current_user()
        q = db.Query(ExposureConcentrations)
        q.filter('user =',user)
        q.filter("config_name =", config_name)
        aquatic_toxicity = q.get()
        if aquatic_toxicity is None:
            aquatic_toxicity = AquaticToxicity()
        if user:
            logger.info(user.user_id())
            aquatic_toxicity.user = user
        aquatic_toxicity = AquaticToxicity()
        aquatic_toxicity.config_name = config_name
        aquatic_toxicity.acute_toxicity_target_concentration_for_freshwater_fish = float(form.getvalue('acute_toxicity_target_concentration_for_freshwater_fish'))
        aquatic_toxicity.chronic_toxicity_target_concentration_for_freshwater_fish = float(form.getvalue('chronic_toxicity_target_concentration_for_freshwater_fish'))
        aquatic_toxicity.acute_toxicity_target_concentration_for_freshwater_invertebrates = float(form.getvalue('acute_toxicity_target_concentration_for_freshwater_invertebrates'))
        aquatic_toxicity.chronic_toxicity_target_concentration_for_freshwater_invertebrates = float(form.getvalue('chronic_toxicity_target_concentration_for_freshwater_invertebrates'))   
        aquatic_toxicity.toxicity_target_concentration_for_nonlisted_vascular_plants = float(form.getvalue('toxicity_target_concentration_for_nonlisted_vascular_plants'))
        aquatic_toxicity.toxicity_target_concentration_for_listed_vascular_plants = float(form.getvalue('toxicity_target_concentration_for_listed_vascular_plants'))
        aquatic_toxicity.toxicity_target_concentration_for_duckweed = float(form.getvalue('toxicity_target_concentration_for_duckweed'))

        aquatic_toxicity.put()
        self.redirect("terrestrial_toxicity.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolAquaticToxicityConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

