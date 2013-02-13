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
from ubertool.pesticide_properties import PesticideProperties
import logging


class UbertoolPesticidePropertiesConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("UbertoolPesticidePropertiesConfigurationPage")
        form = cgi.FieldStorage()
        config_name = str(form.getvalue('config_name'))
        q = db.Query(PesticideProperties)
        q.filter("config_name =", config_name)
        pestProps = q.get()
        if pestProps is None:
            pestProps = PesticideProperties()
        user = users.get_current_user()
        if user:
            pestProps.user = user
        pestProps.config_name = config_name
        pestProps.molecular_weight = float(form.getvalue('molecular_weight'))
        pestProps.henrys_law_constant = float(form.getvalue('henrys_law_constant'))
        pestProps.vapor_pressure = float(form.getvalue('vapor_pressure'))                
        pestProps.solubility = float(form.getvalue('solubility'))
        pestProps.Kd = float(form.getvalue('Kd'))                
        pestProps.Koc = float(form.getvalue('Koc'))
        pestProps.photolysis = float(form.getvalue('photolysis'))                
        pestProps.aerobic_aquatic_metabolism = float(form.getvalue('aerobic_aquatic_metabolism'))
        pestProps.anaerobic_aquatic_metabolism = float(form.getvalue('anaerobic_aquatic_metabolism'))                
        pestProps.aerobic_soil_metabolism = float(form.getvalue('aerobic_soil_metabolism'))
        pestProps.hydrolysis_ph5 = float(form.getvalue('hydrolysis_ph5'))                
        pestProps.hydrolysis_ph7 = float(form.getvalue('hydrolysis_ph7'))
        pestProps.hydrolysis_ph9 = float(form.getvalue('hydrolysis_ph9'))                
        pestProps.foliar_extraction = float(form.getvalue('foliar_extraction'))
        pestProps.foliar_decay_rate = float(form.getvalue('foliar_decay_rate'))                
        pestProps.foliar_dissipation_half_life = float(form.getvalue('foliar_dissipation_half_life'))             
        pestProps.put()
        q = db.Query(PesticideProperties)
        for new_use in q:
            logger.info(new_use.to_xml())
        self.redirect("exposure_concentrations.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolPesticidePropertiesConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

