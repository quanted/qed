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
        pestProps.chemical_name = float(form.getvalue('chemical_name'))
        pestProps.Formulated_product_name = float(form.getvalue('Formulated_product_name'))
        pestProps.seed_treatment_formulation_name = float(form.getvalue('seed_treatment_formulation_name'))
        pestProps.label_epa_reg_no = float(form.getvalue('label_epa_reg_no'))
        pestProps.molecular_weight = float(form.getvalue('molecular_weight'))
        pestProps.percent_ai = float(form.getvalue('percent_ai'))
        pestProps.henrys_law_constant = float(form.getvalue('henrys_law_constant'))
        pestProps.vapor_pressure = float(form.getvalue('vapor_pressure'))                
        pestProps.solubility = float(form.getvalue('solubility'))
        pestProps.Kd = float(form.getvalue('Kd'))                
        pestProps.photolysis = float(form.getvalue('photolysis'))                
        pestProps.aerobic_aquatic_metabolism = float(form.getvalue('aerobic_aquatic_metabolism'))
        pestProps.anaerobic_aquatic_metabolism = float(form.getvalue('anaerobic_aquatic_metabolism'))                
        pestProps.aerobic_soil_metabolism = float(form.getvalue('aerobic_soil_metabolism'))
        pestProps.hydrolysis_ph5 = float(form.getvalue('hydrolysis_ph5'))                
        pestProps.hydrolysis_ph7 = float(form.getvalue('hydrolysis_ph7'))
        pestProps.hydrolysis_ph9 = float(form.getvalue('hydrolysis_ph9'))                
        pestProps.foliar_extraction = float(form.getvalue('foliar_extraction'))
        pestProps.foliar_decay_rate = float(form.getvalue('foliar_decay_rate'))                
        pestProps.Foliar_dissipation_half_life = float(form.getvalue('Foliar_dissipation_half_life'))  
        pestProps.density_of_product = float(form.getvalue('density_of_product'))   
        pestProps.maximum_seedling_rate_per_use = float(form.getvalue('maximum_seedling_rate_per_use'))
        pestProps.row_sp = float(form.getvalue('row_sp'))
        pestProps.bandwidth = float(form.getvalue('bandwidth'))
        pestProps.day_out = float(form.getvalue('day_out'))
        pestProps.use = float(form.getvalue('use'))
        pestProps.seed_crop = float(form.getvalue('seed_crop'))
        pestProps.Application_type = float(form.getvalue('Application_type'))
        pestProps.n_a = float(form.getvalue('n_a'))
        pestProps.ar_lb = float(form.getvalue('ar_lb'))
        pestProps.percent_incorporated = float(form.getvalue('percent_incorporated'))
        pestProps.l_kow = float(form.getvalue('l_kow'))
        pestProps.k_oc = float(form.getvalue('k_oc'))
        pestProps.c_wdp = float(form.getvalue('c_wdp'))
        pestProps.water_column_EEC = float(form.getvalue('water_column_EEC'))
        
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

