import sys
sys.path.append("../ubertool")
from ubertool.ubertool import Ubertool
from ubertool.use import Use
from ubertool.aquatic_toxicity import AquaticToxicity
from ubertool.ecosystem_inputs import EcosystemInputs
from ubertool.exposure_concentrations import ExposureConcentrations
from ubertool.pesticide_properties import PesticideProperties
from ubertool.terrestrial_toxicity import TerrestrialToxicity

from google.appengine.api import users
from google.appengine.ext import db

class UbertoolUserPrefs(db.Expando):
    user_id=db.StringProperty()
    ubertool_configs = db.ListProperty(Ubertool)
    use_configs = db.ListProperty(Use)
    aqua_configs = db.ListProperty(AquaticToxicity)
    eco_configs = db.ListProperty(EcosystemInputs)
    expo_configs = db.ListProperty(ExposureConcentrations)
    pest_configs = db.ListProperty(PesticideProperties)
    terr_configs = db.ListProperty(TerrestrialToxicity)

    