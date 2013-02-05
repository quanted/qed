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
from ubertool.ecosystem_inputs import EcosystemInputs
import logging


class UbertoolEcosystemInputsConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("UbertoolUseConfigurationPage")
        form = cgi.FieldStorage()
        config_name = str(form.getvalue('config_name'))
        eco_inputs = EcosystemInputs()
        user = users.get_current_user()
        if user:
            logger.info(user.user_id())
            eco_inputs.user = user
        eco_inputs.config_name = config_name
        eco_inputs.concentration_of_particulate_organic_carbon = float(form.getvalue('concentration_of_particulate_organic_carbon'))
        eco_inputs.concentration_of_dissolved_organic_carbon = float(form.getvalue('concentration_of_dissolved_organic_carbon'))
        eco_inputs.concentration_of_dissolved_oxygen = float(form.getvalue('concentration_of_dissolved_oxygen'))
        eco_inputs.water_temperature = float(form.getvalue('water_temperature'))
        eco_inputs.concentration_of_suspended_solids = float(form.getvalue('concentration_of_suspended_solids'))
        eco_inputs.sediment_organic_carbon = float(form.getvalue('sediment_organic_carbon'))
        eco_inputs.put()
        q = db.Query(EcosystemInputs)
        for new_use in q:
            logger.info(new_use.to_xml())
        self.redirect("run_ubertool.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolEcosystemInputsConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

