import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from google.appengine.api import users
from google.appengine.ext import db
import cgi
import cgitb
cgitb.enable()
import datetime
import sys
sys.path.append("./")
from use import Use
from pesticide_properties import PesticideProperties
from aquatic_toxicity import AquaticToxicity
from ecosystem_inputs import EcosystemInputs
from exposure_concentrations import ExposureConcentrations
from terrestrial_toxicity import TerrestrialToxicity
from ubertool import Ubertool
sys.path.append("ubertool")
import logging


class UbertoolConfiguration():
        
    def addAquaticToxicityToUbertool(self,ubertool,aquatic_toxicity_config_name):
        q = db.Query(AquaticToxicity)
        q.filter("config_name =", aquatic_toxicity_config_name)
        aqua = q.get()
        return aqua
        
    def addUseToUbertool(self,ubertool,use_config_name):
        q = db.Query(Use)
        q.filter("config_name =", use_config_name)
        use = q.get()
        return use
    
    def addPesticidePropertiesToUbertool(self,ubertool,pesticide_properties_config_name):
        q = db.Query(PesticideProperties)
        q.filter("config_name =", pesticide_properties_config_name)
        pest = q.get()
        return pest
    
    def addEcosystemInputsToUbertool(self,ubertool,ecosystem_inputs_config_name):
        q = db.Query(EcosystemInputs)
        q.filter("config_name =", ecosystem_inputs_config_name)
        eco = q.get()
        return eco
        
    def addExposureConcentrationsToUbertool(self,ubertool,exposure_concentrations_config_name):
        q = db.Query(ExposureConcentrations)
        q.filter("config_name =", exposure_concentrations_config_name)
        expo = q.get()
        return expo
    
    def addTerrestrialToxicityToUbertool(self,ubertool,terrestrial_toxicity_config_name):
        q = db.Query(TerrestrialToxicity)
        q.filter("config_name =", terrestrial_toxicity_config_name)
        terra = q.get()
        return terra

