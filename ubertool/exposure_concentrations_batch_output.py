import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgi
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db
from ubertool import run_ubertool_db
from StringIO import StringIO
import cStringIO
import csv
import sys
sys.path.append("utils")
sys.path.append("./")
sys.path.append("ubertool")
from ubertool.ubertool import Ubertool
from ubertool.run_ubertool_config import UbertoolConfiguration
from CSVTestParamsLoader import CSVTestParamsLoader
from exposure_concentrations import ExposureConcentrations

class ExposureConcentrationsBatchLoader:
    
    def batchLoadExposureConcentrationsConfigs(self,params_matrix,exposure_concentrations_config_index,ubertool):
        runUbertoolConfigPage = UbertoolConfiguration()
        exposure_concentrations_config_name = None
        if "exposure_concentrations_config_name" in params_matrix:
            exposure_concentrations_config_name = params_matrix.get("exposure_concentrations_config_name")[exposure_concentrations_config_index]
        one_in_ten_peak_exposure_concentration = None
        if "one_in_ten_peak_exposure_concentration" in params_matrix:
            one_in_ten_peak_exposure_concentration = params_matrix.get("one_in_ten_peak_exposure_concentration")[exposure_concentrations_config_index]            
        one_in_ten_four_day_average_exposure_concentration = None
        if "one_in_ten_four_day_average_exposure_concentration" in params_matrix:
            one_in_ten_four_day_average_exposure_concentration = params_matrix.get("one_in_ten_four_day_average_exposure_concentration")[exposure_concentrations_config_index]            
        one_in_ten_twentyone_day_average_exposure_concentration = None
        if "one_in_ten_twentyone_day_average_exposure_concentration" in params_matrix:
            one_in_ten_twentyone_day_average_exposure_concentration = params_matrix.get("one_in_ten_twentyone_day_average_exposure_concentration")[exposure_concentrations_config_index]            
        one_in_ten_sixty_day_average_exposure_concentration = None
        if "one_in_ten_sixty_day_average_exposure_concentration" in params_matrix:
            one_in_ten_sixty_day_average_exposure_concentration = params_matrix.get("one_in_ten_sixty_day_average_exposure_concentration")[exposure_concentrations_config_index]  
        one_in_ten_ninety_day_average_exposure_concentration = None
        if "one_in_ten_ninety_day_average_exposure_concentration" in params_matrix:
            one_in_ten_ninety_day_average_exposure_concentration = params_matrix.get("one_in_ten_ninety_day_average_exposure_concentration")[exposure_concentrations_config_index]  
        maximum_peak_exposure_concentration = None
        if "maximum_peak_exposure_concentration" in params_matrix:
            maximum_peak_exposure_concentration = params_matrix.get("maximum_peak_exposure_concentration")[exposure_concentrations_config_index]  
        maximum_four_day_average_exposure_concentration = None
        if "maximum_four_day_average_exposure_concentration" in params_matrix:
            maximum_four_day_average_exposure_concentration = params_matrix.get("maximum_four_day_average_exposure_concentration")[exposure_concentrations_config_index]
        maximum_twentyone_day_average_exposure_concentration = None
        if "maximum_twentyone_day_average_exposure_concentration" in params_matrix:
            maximum_twentyone_day_average_exposure_concentration = params_matrix.get("maximum_twentyone_day_average_exposure_concentration")[exposure_concentrations_config_index]            
        maximum_sixty_day_average_exposure_concentration = None
        if "maximum_sixty_day_average_exposure_concentration" in params_matrix:
            maximum_sixty_day_average_exposure_concentration = params_matrix.get("maximum_sixty_day_average_exposure_concentration")[exposure_concentrations_config_index]            
        maximum_ninety_day_average_exposure_concentration = None
        if "maximum_ninety_day_average_exposure_concentration" in params_matrix:
            maximum_ninety_day_average_exposure_concentration = params_matrix.get("maximum_ninety_day_average_exposure_concentration")[exposure_concentrations_config_index]
        pore_water_peak_exposure_concentration = None
        if "pore_water_peak_exposure_concentration" in params_matrix:
            pore_water_peak_exposure_concentration = params_matrix.get("pore_water_peak_exposure_concentration")[exposure_concentrations_config_index]            
        pore_water_four_day_average_exposure_concentration = None
        if "pore_water_four_day_average_exposure_concentration" in params_matrix:
            pore_water_four_day_average_exposure_concentration = params_matrix.get("pore_water_four_day_average_exposure_concentration")[exposure_concentrations_config_index]            
        pore_water_twentyone_day_average_exposure_concentration = None
        if "pore_water_twentyone_day_average_exposure_concentration" in params_matrix:
            pore_water_twentyone_day_average_exposure_concentration = params_matrix.get("pore_water_twentyone_day_average_exposure_concentration")[exposure_concentrations_config_index]
        pore_water_sixty_day_average_exposure_concentration = None
        if "pore_water_sixty_day_average_exposure_concentration" in params_matrix:
            pore_water_sixty_day_average_exposure_concentration = params_matrix.get("pore_water_sixty_day_average_exposure_concentration")[exposure_concentrations_config_index]            
        pore_water_ninety_day_average_exposure_concentration = None
        if "pore_water_ninety_day_average_exposure_concentration" in params_matrix:
            pore_water_ninety_day_average_exposure_concentration = params_matrix.get("pore_water_ninety_day_average_exposure_concentration")[exposure_concentrations_config_index]            
        user = users.get_current_user()
        q = db.Query(ExposureConcentrations)
        if user:
            q.filter('user =',user)
        if exposure_concentrations_config_name:
            q.filter("config_name =", exposure_concentrations_config_name)
        exposure = q.get()
        if exposure is None:
            exposure = ExposureConcentrations()
        if user:
            exposure.user = user
        exposure.config_name = exposure_concentrations_config_name
        exposure.one_in_ten_peak_exposure_concentration = one_in_ten_peak_exposure_concentration
        exposure.one_in_ten_four_day_average_exposure_concentration = one_in_ten_four_day_average_exposure_concentration
        exposure.one_in_ten_twentyone_day_average_exposure_concentration = one_in_ten_twentyone_day_average_exposure_concentration
        exposure.one_in_ten_sixty_day_average_exposure_concentration = one_in_ten_sixty_day_average_exposure_concentration   
        exposure.one_in_ten_ninety_day_average_exposure_concentration = one_in_ten_ninety_day_average_exposure_concentration
        exposure.maximum_peak_exposure_concentration = maximum_peak_exposure_concentration
        exposure.maximum_four_day_average_exposure_concentration = maximum_four_day_average_exposure_concentration
        exposure.maximum_twentyone_day_average_exposure_concentration = maximum_twentyone_day_average_exposure_concentration
        exposure.maximum_sixty_day_average_exposure_concentration = maximum_sixty_day_average_exposure_concentration
        exposure.maximum_ninety_day_average_exposure_concentration = maximum_ninety_day_average_exposure_concentration
        exposure.pore_water_peak_exposure_concentration = pore_water_peak_exposure_concentration
        exposure.pore_water_four_day_average_exposure_concentration = pore_water_four_day_average_exposure_concentration
        exposure.pore_water_twentyone_day_average_exposure_concentration = pore_water_twentyone_day_average_exposure_concentration
        exposure.pore_water_sixty_day_average_exposure_concentration = pore_water_sixty_day_average_exposure_concentration
        exposure.pore_water_ninety_day_average_exposure_concentration = pore_water_ninety_day_average_exposure_concentration
        exposure.put()
        return runUbertoolConfigPage.addExposureConcentrationsToUbertool(ubertool,exposure_concentrations_config_name)
                      