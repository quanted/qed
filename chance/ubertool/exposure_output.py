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
from ubertool.exposure import Exposure
import logging


class UbertoolExposureConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("UbertoolExposureConfigurationPage")
        form = cgi.FieldStorage()
        config_name = str(form.getvalue('config_name'))
        user = users.get_current_user()
        q = db.Query(Exposure)
        q.filter('user =',user)
        q.filter("config_name =", config_name)
        exposure = q.get()
        if exposure is None:
            exposure = Exposure()
        if user:
            logger.info(user.user_id())
            exposure.user = user
        exposure.config_name = config_name
        exposure.cas_number = str(form.getvalue('cas_number'))
        exposure.formulated_product_name = form.getvalue('formulated_product_name')
        exposure.met_file = form.getvalue('metfile')
        exposure.przm_scenario = form.getvalue('PRZM_scenario')
        exposure.exams_environment_file = form.getvalue('EXAMS_environment_file')
        exposure.application_method = form.getvalue('application_mathod')
        exposure.app_type = form.getvalue('app_type')
        exposure.weight_of_one_granule = float(form.getvalue('weight_of_one_granule'))
        exposure.wetted_in = bool(form.getvalue('wetted_in'))
        exposure.incorporation_depth = float(form.getvalue('incorporation_depth'))
        exposure.application_kg_rate = float(form.getvalue('application_kg_rate'))
        exposure.application_lbs_rate = float(form.getvalue('application_lbs_rate'))
        exposure.application_rate_per_use = float(form.getvalue('application_rate_per_use'))
        logger.info(form.getvalue("application_date"))
        #TODO This is NASTY we should consider using Date Chooser or something with only one valid output
        app_data = form.getvalue('application_date')
        app_data_parts = app_data.split("-")
        exposure.application_date = datetime.date(int(app_data_parts[0]),int(app_data_parts[1]),int(app_data_parts[2]))
        exposure.interval_between_applications = float(form.getvalue('interval_between_applications'))
        exposure.application_efficiency = float(form.getvalue('application_efficiency'))
        exposure.percent_incorporated = float(form.getvalue('percent_incorporated'))
        exposure.spray_drift = float(form.getvalue('spray_drift'))
        exposure.runoff = float(form.getvalue('runoff'))
        exposure.one_in_ten_peak_exposure_concentration = float(form.getvalue('one_in_ten_peak_exposure_concentration'))
        exposure.one_in_ten_four_day_average_exposure_concentration = float(form.getvalue('one_in_ten_four_day_average_exposure_concentration'))
        exposure.one_in_ten_twentyone_day_average_exposure_concentration = float(form.getvalue('one_in_ten_twentyone_day_average_exposure_concentration'))
        exposure.one_in_ten_sixty_day_average_exposure_concentration = float(form.getvalue('one_in_ten_sixty_day_average_exposure_concentration'))
        exposure.one_in_ten_ninety_day_average_exposure_concentration = float(form.getvalue('one_in_ten_ninety_day_average_exposure_concentration'))
        exposure.maximum_peak_exposure_concentration = float(form.getvalue('maximum_peak_exposure_concentration'))
        exposure.maximum_four_day_average_exposure_concentration = float(form.getvalue('maximum_four_day_average_exposure_concentration'))
        exposure.maximum_twentyone_day_average_exposure_concentration = float(form.getvalue('maximum_twentyone_day_average_exposure_concentration'))
        exposure.maximum_sixty_day_average_exposure_concentration = float(form.getvalue('maximum_sixty_day_average_exposure_concentration'))
        exposure.maximum_ninety_day_average_exposure_concentration = float(form.getvalue('maximum_ninety_day_average_exposure_concentration'))
        exposure.pore_water_peak_exposure_concentration = float(form.getvalue('pore_water_peak_exposure_concentration'))
        exposure.pore_water_four_day_average_exposure_concentration = float(form.getvalue('pore_water_four_day_average_exposure_concentration'))
        exposure.pore_water_twentyone_day_average_exposure_concentration = float(form.getvalue('pore_water_twentyone_day_average_exposure_concentration'))
        exposure.pore_water_sixty_day_average_exposure_concentration = float(form.getvalue('pore_water_sixty_day_average_exposure_concentration'))
        exposure.pore_water_ninety_day_average_exposure_concentration = float(form.getvalue('pore_water_ninety_day_average_exposure_concentration'))
        exposure.frac_pest_surface = float(form.getvalue('frac_pest_surface'))
        exposure.put()
        self.redirect("aquatic_toxicity.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolExposureConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

