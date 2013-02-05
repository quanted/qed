import google.appengine.ext.db as db
from google.appengine.api import users
import datetime
import time
from use import Use
from pesticide_properties import PesticideProperties
from aquatic_toxicity import AquaticToxicity
from ecosystem_inputs import EcosystemInputs
from exposure_concentrations import ExposureConcentrations
from terrestrial_toxicity import TerrestrialToxicity

class Ubertool(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    use = db.ReferenceProperty(Use)
    pest = db.ReferenceProperty(PesticideProperties)
    aqua = db.ReferenceProperty(AquaticToxicity)
    eco = db.ReferenceProperty(EcosystemInputs)
    expo = db.ReferenceProperty(ExposureConcentrations)
    terra = db.ReferenceProperty(TerrestrialToxicity)
    created = db.DateTimeProperty(auto_now_add=True)