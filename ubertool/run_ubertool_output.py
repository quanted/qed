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
import sys
sys.path.append("../ubertool")
from ubertool.use import Use
from ubertool.pesticide_properties import PesticideProperties
from ubertool.aquatic_toxicity import AquaticToxicity
from ubertool.ecosystem_inputs import EcosystemInputs
from ubertool.exposure_concentrations import ExposureConcentrations
from ubertool.terrestrial_toxicity import TerrestrialToxicity
from ubertool.ubertool import Ubertool
import logging


class RunUbertoolConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("RunUbertoolConfigurationPage")
        form = cgi.FieldStorage()
        config_name = str(form.getvalue('config_name'))
        ubertool = Ubertool()
        ubertool.config_name = config_name
        user = users.get_current_user()
        if user:
            logger.info(user.user_id())
            ubertool.user = user
        use_config_name = str(form.getvalue('use_configuration'))
        q = db.Query(Use)
        q.filter("config_name =", use_config_name)
        use = q.get()
        ubertool.use = use
        pesticide_properties_config_name = str(form.getvalue('pest_configuration'))
        q = db.Query(PesticideProperties)
        q.filter("config_name =", pesticide_properties_config_name)
        pest = q.get()
        ubertool.pest = pest
        aquatic_toxicity_config_name = str(form.getvalue('aquatic_configuration'))
        q = db.Query(AquaticToxicity)
        q.filter("config_name =", aquatic_toxicity_config_name)
        aqua = q.get()
        ubertool.aqua = aqua
        ecosystem_inputs_config_name = str(form.getvalue('ecosystems_configuration'))
        q = db.Query(EcosystemInputs)
        q.filter("config_name =", ecosystem_inputs_config_name)
        eco = q.get()
        ubertool.eco = eco
        exposure_concentrations_config_name = str(form.getvalue('exposures_configuration'))
        q = db.Query(ExposureConcentrations)
        q.filter("config_name =", exposure_concentrations_config_name)
        expo = q.get()
        ubertool.expo = expo
        terrestrial_toxicity_config_name = str(form.getvalue('terrestrial_configuration'))
        q = db.Query(TerrestrialToxicity)
        q.filter("config_name =", terrestrial_toxicity_config_name)
        terra = q.get()
        ubertool.terra = terra
        ubertool.put()
        q = db.Query(Ubertool)
        for new_use in q:
            logger.info(new_use.to_xml())
        
        
        
app = webapp.WSGIApplication([('/.*', RunUbertoolConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()