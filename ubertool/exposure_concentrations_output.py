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
from ubertool.exposure_concentrations import ExposureConcentrations
import logging


class UbertoolExposureConcentrationsConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("UbertoolExposureConcentrationsConfigurationPage")
        form = cgi.FieldStorage()
        config_name = str(form.getvalue('config_name'))
        user = users.get_current_user()
        q = db.Query(ExposureConcentrations)
        q.filter('user =',user)
        q.filter("config_name =", config_name)
        exposure_concentrations = q.get()
        if exposure_concentrations is None:
            exposure_concentrations = ExposureConcentrations()
        if user:
            logger.info(user.user_id())
            exposure_concentrations.user = user
        exposure_concentrations = ExposureConcentrations()
        exposure_concentrations.config_name = config_name
        exposure_concentrations.one_in_ten_peak_exposure_concentration = float(form.getvalue('one_in_ten_peak_exposure_concentration'))
        exposure_concentrations.one_in_ten_four_day_average_exposure_concentration = float(form.getvalue('one_in_ten_four_day_average_exposure_concentration'))
        exposure_concentrations.one_in_ten_twentyone_day_average_exposure_concentration = float(form.getvalue('one_in_ten_twentyone_day_average_exposure_concentration'))
        exposure_concentrations.one_in_ten_sixty_day_average_exposure_concentration = float(form.getvalue('one_in_ten_sixty_day_average_exposure_concentration'))
        exposure_concentrations.one_in_ten_ninety_day_average_exposure_concentration = float(form.getvalue('one_in_ten_ninety_day_average_exposure_concentration'))
        exposure_concentrations.maximum_peak_exposure_concentration = float(form.getvalue('maximum_peak_exposure_concentration'))
        exposure_concentrations.maximum_four_day_average_exposure_concentration = float(form.getvalue('maximum_four_day_average_exposure_concentration'))
        exposure_concentrations.maximum_twentyone_day_average_exposure_concentration = float(form.getvalue('maximum_twentyone_day_average_exposure_concentration'))
        exposure_concentrations.maximum_sixty_day_average_exposure_concentration = float(form.getvalue('maximum_sixty_day_average_exposure_concentration'))
        exposure_concentrations.maximum_ninety_day_average_exposure_concentration = float(form.getvalue('maximum_ninety_day_average_exposure_concentration'))
        exposure_concentrations.pore_water_peak_exposure_concentration = float(form.getvalue('pore_water_peak_exposure_concentration'))
        exposure_concentrations.pore_water_four_day_average_exposure_concentration = float(form.getvalue('pore_water_four_day_average_exposure_concentration'))
        exposure_concentrations.pore_water_twentyone_day_average_exposure_concentration = float(form.getvalue('pore_water_twentyone_day_average_exposure_concentration'))
        exposure_concentrations.pore_water_sixty_day_average_exposure_concentration = float(form.getvalue('pore_water_sixty_day_average_exposure_concentration'))
        exposure_concentrations.pore_water_ninety_day_average_exposure_concentration = float(form.getvalue('pore_water_ninety_day_average_exposure_concentration'))

        exposure_concentrations.put()
        self.redirect("aquatic_toxicity.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolExposureConcentrationsConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

