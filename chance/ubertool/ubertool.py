import google.appengine.ext.db as db
from google.appengine.api import users
import datetime
import time
import sys
sys.path.append("ubertool")
from use_metadata import Use_metadata
from pesticide_properties import PesticideProperties
from aquatic_toxicity import AquaticToxicity
from ecosystem_inputs import EcosystemInputs
from exposure import Exposure
from terrestrial_toxicity import TerrestrialToxicity
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import logging
from utils import json_utils

logger = logging.getLogger("Ubertool")
               
class Ubertool(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    use = db.ReferenceProperty(Use_metadata)
    pest = db.ReferenceProperty(PesticideProperties)
    aqua = db.ReferenceProperty(AquaticToxicity)
    eco = db.ReferenceProperty(EcosystemInputs)
    expo = db.ReferenceProperty(Exposure)
    terra = db.ReferenceProperty(TerrestrialToxicity)
    created = db.DateTimeProperty(auto_now_add=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()