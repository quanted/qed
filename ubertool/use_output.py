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
from ubertool.use import Use
import logging


class UbertoolUseConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("UbertoolUseConfigurationPage")
        form = cgi.FieldStorage()
        config_name = str(form.getvalue('config_name'))
        use = Use(key_name="config_name")
        user = users.get_current_user()
        if user:
            logger.info(user.user_id())
            use.user = user
        use.config_name = config_name
        use.cas_number = str(form.getvalue('cas_number'))
        use.formulated_product_name = form.getvalue('formulated_product_name')
        use.percent_ai = float(form.getvalue('percent_ai'))
        use.met_file = form.getvalue('metfile')
        use.przm_scenario = form.getvalue('PRZM_scenario')
        use.exams_environment_file = form.getvalue('EXAMS_environment_file')
        use.application_method = form.getvalue('application_mathod')
        use.application_type = form.getvalue('application_type')
        use.app_type = form.getvalue('app_type')
        use.weight_of_one_granule = float(form.getvalue('weight_of_one_granule'))
        use.wetted_in = bool(form.getvalue('wetted_in'))
        use.incorporation_depth = float(form.getvalue('incorporation_depth'))
        use.percent_incorporated = float(form.getvalue('percent_incorporated'))
        use.application_kg_rate = float(form.getvalue('application_kg_rate'))
        use.application_lbs_rate = float(form.getvalue('application_lbs_rate'))
        use.seed_treatment_formulation_name = form.getvalue('seed_treatment_formulation_name')
        use.density_of_product = float(form.getvalue('density_of_product'))
        use.maximum_seedling_rate_per_use = float(form.getvalue('maximum_seedling_rate_per_use'))
        use.application_rate_per_use = float(form.getvalue('application_rate_per_use'))
        logger.info(form.getvalue("application_date"))
        #TODO This is NASTY we should consider using Date Chooser or something with only one valid output
        app_data = form.getvalue('application_date')
        app_data_parts = app_data.split("-")
        use.application_date = datetime.date(int(app_data_parts[0]),int(app_data_parts[1]),int(app_data_parts[2]))
        use.number_of_applications = float(form.getvalue('number_of_applications'))
        use.interval_between_applications = float(form.getvalue('interval_between_applications'))
        use.application_efficiency = float(form.getvalue('application_efficiency'))
        use.percent_incorporated = float(form.getvalue('percent_incorporated'))
        use.spray_drift = float(form.getvalue('spray_drift'))
        use.runoff = float(form.getvalue('runoff'))
        use.put()
        self.redirect("pesticide_properties.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolUseConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

