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
import sys
sys.path.append("../ubertool")
from ubertool.use import Use, UsePropertiesRetrievalService
from ubertool.pesticide_properties import PesticideProperties, PestPropertiesRetrievalService
from ubertool.aquatic_toxicity import AquaticToxicity, AquaticToxicityPropertiesRetrievalService
from ubertool.ecosystem_inputs import EcosystemInputs, EcosystemInputsPropertiesRetrievalService
from ubertool.exposure_concentrations import ExposureConcentrations, ExposureConcentrationsRetrievalService
from ubertool.terrestrial_toxicity import TerrestrialToxicity, TerrestrialPropertiesRetrievalService
from ubertool.ubertool import Ubertool
import logging
from gae_restful_lib import GAE_Connection as Connection

batch_conn = Connection('http://localhost/batch')
usePropService = UsePropertiesRetrievalService()
pestPropService = PestPropertiesRetrievalService()
aquaPropService = AquaticToxicityPropertiesRetrievalService()
ecoPropService = EcosystemInputsPropertiesRetrievalService()
expoPropService = ExposureConcentrationsRetrievalService()
terrePropService = TerrestrialPropertiesRetrievalService()

def retrieveUbertoolConfigFromForm(form,ubertool_config_key,use_config_key,pest_config_key,aquatic_config_key,ecosystems_config_key,expo_config_key,terra_config_key):
    ubertool_dict = {}
    config_name = str(form.getvalue(ubertool_config_key))
    ubertool = Ubertool()
    ubertool.config_name = config_name
    ubertool_dict['config_name'] = config_name
    user = users.get_current_user()
    if user:
        logger.info(user.user_id())
        ubertool.user = user
    use_tuple = retrieveUseConfigFromForm(form, use_config_key)
    ubertool.use - use_tuple[0]
    ubertool_dict['use'] = use_tuple[1]
    pest_tuple = retrievePestConfigFromForm(form, pest_config_key)
    ubertool.pest - pest_tuple[0]
    ubertool_dict['pest'] = pest_tuple[1]
    aqua_tuple = retrieveAquaConfigFromForm(form, aquatic_config_key)
    ubertool.aqua = aqua_tuple[0]
    ubertool_dict['aqua'] = aqua_tuple[1]
    eco_tuple = retrieveEcoConfigFromForm(form, ecosystems_config_key)
    ubertool.eco = eco_tuple[0]
    ubertool_dict['eco'] = eco_tuple[1]
    expo_tuple = retrieveExpoConfigFromForm(form, expo_config_key)
    ubertool.expo = expo_tuple[0]
    ubertool_dict['expo'] - expo_tuple[1]
    terra_tuple = retrieveTerraConfigFromForm(form, terra_config_key)
    ubertool.terra = terra_tuple[0]
    ubertool_dict['terra'] = terra_tuple[1]
    ubertool.put()
    return (ubertool,ubertool_dict)

def retrieveUseConfigFromForm(form, use_config_key):
    use_config_name = str(form.getvalue(use_config_key))
    q = db.Query(Use)
    q.filter("config_name =", use_config_name)
    use = q.get()
    use_dict = usePropService.get()
    return (use,use_dict)

def retrievePestConfigFromForm(form, pest_config_key):
    pesticide_properties_config_name = str(form.getvalue(pest_config_key))
    q = db.Query(PesticideProperties)
    q.filter("config_name =", pesticide_properties_config_name)
    pest = q.get()
    pest_dict = pestPropService.get()
    return (pest, pest_dict)
    
def retrieveAquaConfigFromForm(form, aquatic_config_key):
    aquatic_toxicity_config_name = str(form.getvalue(aquatic_config_key))
    q = db.Query(AquaticToxicity)
    q.filter("config_name =", aquatic_toxicity_config_name)
    aqua = q.get()
    aqua_dict = aquaPropService.get()
    return (aqua. aqua_dict)

def retrieveEcoConfigFromForm(form, ecosystems_config_key):
    ecosystem_inputs_config_name = str(form.getvalue(ecosystems_config_key))
    q = db.Query(EcosystemInputs)
    q.filter("config_name =", ecosystem_inputs_config_name)
    eco = q.get()
    eco_dict = ecoPropService.get()
    return (eco, eco_dict)

def retrieveExpoConfigFromForm(form, expo_config_key):
    exposure_concentrations_config_name = str(form.getvalue(expo_config_key))
    q = db.Query(ExposureConcentrations)
    q.filter("config_name =", exposure_concentrations_config_name)
    expo = q.get()
    expo_dict = expoPropService.get()
    return (expo, expo_dict)

def retrieveTerraConfigFromForm(form, terra_config_key):
    terrestrial_toxicity_config_name = str(form.getvalue(terra_config_key))
    q = db.Query(TerrestrialToxicity)
    q.filter("config_name =", terrestrial_toxicity_config_name)
    terra = q.get()
    terra_dict = terrePropService.get()
    return (terra, terra_dict)

class RunUbertoolConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("RunUbertoolConfigurationPage")
        form = cgi.FieldStorage()
        keys = form.keys()
        logger.info(form)
        ubertool_tuple = retrieveUbertoolConfigFromForm(form,'config_name','use_configuration','pest_configuration','aquatic_configuration','ecosystems_configuration','exposures_configuration','terrestrial_configuration')
        ubertool = ubertool_tuple[0]
        uber_dict = ubertool_tuple[1]
        ubertools_dict = []
        ubertool_config_name = uber_dict['config_name']
        ubertools_dict[ubertool_config_name] = uber_dict
        current_config_number = 1
        ubertool_config_name_prefix = "config_name_"
        use_config_name_prefix = "use_config_name_"
        pest_config_name_prefix = "pest_configuration_"
        aqua_config_name_prefix = "aquatic_configuration_"
        eco_config_name_prefix = "ecosystems_configuration_"
        expo_config_name_prefix = "exposures_configuration_"
        terra_config_name_prefix = "terrestrial_configuration_"
        current_ubertool_config_name = ubertool_config_name_prefix + current_config_number
        batch = None
        if current_ubertool_config_name in keys:
            while current_ubertool_config_name in keys:
                current_use_config_name = use_config_name_prefix + current_config_number
                current_pest_config_name = pest_config_name_prefix + current_config_number
                current_aqua_config_name = aqua_config_name_prefix + current_config_number
                current_eco_config_name = eco_config_name_prefix + current_config_number
                current_expo_config_name = expo_config_name_prefix + current_config_number
                current_terra_config_name = terre_config_name_prefix + current_config_number
                ubertool_tuple = retrieveUbertoolConfigFromForm(form,current_ubertool_config_name,current_use_config_name,current_pest_config_name,current_aqua_config_name,current_eco_config_name,current_expo_config_name,current_terra_config_name)
                ubertool = ubertool_tuple[0]
                uber_dict = ubertool_tuple[1]
                ubertool_config_name = uber_dict['config_name']
                ubertools_dict[ubertool_config_name] = uber_dict
                current_config_number += 1
                current_ubertool_config_name = config_name_prefix + current_config_number
            #create Batch object
            batch = Batch(user=user,
                          completed=False,
                          ubertools=ubertools_dict)
        #test if only partial configs were passed
        else:
            current_config_number = 1
            use_configs = []
            current_use_config_name = use_config_name_prefix + current_config_number
            while current_use_config_name in keys:
                use = retrieveUseConfigFromForm(form, current_use_config_name)
                use_configs.append(use)
                current_config_number += 1
                current_use_config_name = use_config_name_prefix + current_config_number
            current_config_number = 1
            pest_configs = []
            current_pest_config_name = pest_config_name_prefix + current_config_number
            while current_pest_config_name in keys:
                pest = retrievePestConfigFromForm(form, current_pest_config_name)
                pest_configs.append(pest)
                current_config_number += 1
                current_pest_config_name = pest_config_name_prefix + current_config_number
            current_config_number = 1
            aqua_configs = []
            current_aqua_config_name = aqua_config_name_prefix + current_config_number
            while current_aqua_config_name in keys:
                aqua = retrieveAquaConfigFromForm(form, current_aqua_config_name)
                aqua_configs.append(aqua)
                current_config_number += 1
                current_aqua_config_name = aqua_config_name_prefix + current_config_number
            current_config_number = 1
            eco_configs = []
            current_eco_config_name = eco_config_name_prefix + current_config_number
            while current_eco_config_name in keys:
                eco = retrieveEcoConfigFromForm(form, current_eco_config_name)
                eco_configs.append(eco)
                current_config_number += 1
                current_eco_config_name = eco_config_name_prefix + current_config_number
            current_config_number = 1
            expo_configs = []
            current_expo_config_name = expo_config_name_prefix + current_config_number
            while current_expo_config_name in keys:
                expo = retrieveExpoConfigFromForm(form, current_expo_config_name)
                expo_configs.append(expo)
                current_config_number += 1
                current_expo_config_name = expo_config_name_prefix + current_config_number
            current_config_number = 1
            terra_configs = []
            current_terra_config_name = terra_config_name_prefix + current_config_number
            while current_terra_config_name in keys:
                terra = retrieveTerraConfigFromForm(form, current_terra_config_name)
                terra_configs.append(terra)
                current_config_number += 1
                current_terraa_config_name = terra_config_name_prefix + current_config_number
            #create Batch object
            batch = Batch(user=user,
                          completed=False,
                          uses=use_configs,
                          pests=pest_configs,
                          aquas=aqua_configs,
                          ecos=eco_configs,
                          expos=expo_configs,
                          terras=terra_configs
                          )
            batch.put()
            logger.info(batch.to_xml())
        #Pass batch id to cookie so user page will be able to periodically check back to see progress of batch
        self.redirect("user.html")
        
        
app = webapp.WSGIApplication([('/.*', RunUbertoolConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()