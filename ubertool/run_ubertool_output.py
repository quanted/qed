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
sys.path.append("../batch")
from batch.batch import Batch
from batch.batch_processor import BatchService
import logging
import urllib,httplib
#import urllib, httplib2
#batch_conn = httplib.HTTPConnection('http://localhost:8888')
#h = httplib2.Http(".cache")
from django.utils import simplejson
import pickle

batchProcessor = BatchService()
usePropService = UsePropertiesRetrievalService()
pestPropService = PestPropertiesRetrievalService()
aquaPropService = AquaticToxicityPropertiesRetrievalService()
ecoPropService = EcosystemInputsPropertiesRetrievalService()
expoPropService = ExposureConcentrationsRetrievalService()
terrePropService = TerrestrialPropertiesRetrievalService()
logger = logging.getLogger("RunUbertoolBatch")

def retrieveUbertoolConfigFromForm(data,ubertool_config_key,use_config_key,pest_config_key,aquatic_config_key,ecosystems_config_key,expo_config_key,terra_config_key):
    user = users.get_current_user()
    ubertool_dict = {}
    config_name = data[ubertool_config_key]
    ubertool = Ubertool()
    ubertool.config_name = config_name
    ubertool_dict['config_name'] = config_name
    if user:
        logger.info(user.user_id())
        ubertool.user = user
    use_tuple = retrieveUseConfigFromForm(data, use_config_key)
    logger.info(use_tuple)
    ubertool.use = use_tuple[0]
    ubertool_dict['use'] = use_tuple[1]
    pest_tuple = retrievePestConfigFromForm(data, pest_config_key)
    ubertool.pest = pest_tuple[0]
    ubertool_dict['pest'] = pest_tuple[1]
    aqua_tuple = retrieveAquaConfigFromForm(data, aquatic_config_key)
    ubertool.aqua = aqua_tuple[0]
    ubertool_dict['aqua'] = aqua_tuple[1]
    eco_tuple = retrieveEcoConfigFromForm(data, ecosystems_config_key)
    ubertool.eco = eco_tuple[0]
    ubertool_dict['eco'] = eco_tuple[1]
    expo_tuple = retrieveExpoConfigFromForm(data, expo_config_key)
    ubertool.expo = expo_tuple[0]
    ubertool_dict['expo'] = expo_tuple[1]
    terra_tuple = retrieveTerraConfigFromForm(data, terra_config_key)
    ubertool.terra = terra_tuple[0]
    ubertool_dict['terra'] = terra_tuple[1]
    ubertool.put()
    return (ubertool,ubertool_dict)

def retrieveUseConfigFromForm(data, use_config_key):
    use_config_name = str(data[use_config_key])
    q = db.Query(Use)
    q.filter("config_name =", use_config_name)
    use = q.get()
    use_dict = usePropService.get(use_config_name)
    logger.info(use_dict)
    return (use,use_dict)

def retrievePestConfigFromForm(data, pest_config_key):
    pesticide_properties_config_name = str(data[pest_config_key])
    q = db.Query(PesticideProperties)
    q.filter("config_name =", pesticide_properties_config_name)
    pest = q.get()
    pest_dict = pestPropService.get(pesticide_properties_config_name)
    return (pest, pest_dict)
    
def retrieveAquaConfigFromForm(data, aquatic_config_key):
    aquatic_toxicity_config_name = str(data[aquatic_config_key])
    q = db.Query(AquaticToxicity)
    q.filter("config_name =", aquatic_toxicity_config_name)
    aqua = q.get()
    aqua_dict = aquaPropService.get(aquatic_toxicity_config_name)
    return (aqua, aqua_dict)

def retrieveEcoConfigFromForm(data, ecosystems_config_key):
    ecosystem_inputs_config_name = str(data[ecosystems_config_key])
    q = db.Query(EcosystemInputs)
    q.filter("config_name =", ecosystem_inputs_config_name)
    eco = q.get()
    eco_dict = ecoPropService.get(ecosystem_inputs_config_name)
    return (eco, eco_dict)

def retrieveExpoConfigFromForm(data, expo_config_key):
    exposure_concentrations_config_name = str(data[expo_config_key])
    q = db.Query(ExposureConcentrations)
    q.filter("config_name =", exposure_concentrations_config_name)
    expo = q.get()
    expo_dict = expoPropService.get(exposure_concentrations_config_name)
    return (expo, expo_dict)

def retrieveTerraConfigFromForm(data, terra_config_key):
    terrestrial_toxicity_config_name = str(data[terra_config_key])
    q = db.Query(TerrestrialToxicity)
    q.filter("config_name =", terrestrial_toxicity_config_name)
    terra = q.get()
    terra_dict = terrePropService.get(terrestrial_toxicity_config_name)
    return (terra, terra_dict)

def retrieveBatchUbertoolConfiguration(data):
    keys = data.keys()
    user = users.get_current_user()
    batch = Batch()
    batch.user = user
    logger.info(batch.to_xml())
    ubertool_tuple = retrieveUbertoolConfigFromForm(data,"config_name","use_configuration","pest_configuration","aquatic_configuration","ecosystems_configuration","exposures_configuration","terrestrial_configuration")
    ubertool = ubertool_tuple[0]
    uber_dict = ubertool_tuple[1]
    ubertools = []
    batch_dict = {}
    ubertool_config_name = uber_dict['config_name']
    ubertools.append(uber_dict)
    current_config_number = 1
    ubertool_config_name_prefix = "config_name_"
    use_config_name_prefix = "use_configuration_"
    pest_config_name_prefix = "pest_configuration_"
    aqua_config_name_prefix = "aquatic_configuration_"
    eco_config_name_prefix = "ecosystems_configuration_"
    expo_config_name_prefix = "exposures_configuration_"
    terra_config_name_prefix = "terrestrial_configuration_"
    current_use_config_name = use_config_name_prefix + str(current_config_number)
    current_pest_config_name = pest_config_name_prefix + str(current_config_number)
    current_aqua_config_name = aqua_config_name_prefix + str(current_config_number)
    current_eco_config_name = eco_config_name_prefix + str(current_config_number)
    current_expo_config_name = expo_config_name_prefix + str(current_config_number)
    current_terra_config_name = terra_config_name_prefix + str(current_config_number)
    current_ubertool_config_name = ubertool_config_name_prefix + str(current_config_number)
    batch_ubertool_config_names = []
    batch_use_config_names = []
    batch_pest_config_names = []
    batch_aqua_config_names = []
    batch_eco_config_names = []
    batch_expo_config_names = []
    batch_terra_config_names = []
    batch_ubertool_config_names.append(ubertool_config_name)
    if current_ubertool_config_name in keys:
        while current_ubertool_config_name in keys:
            ubertool_tuple = retrieveUbertoolConfigFromForm(data,current_ubertool_config_name,current_use_config_name,current_pest_config_name,current_aqua_config_name,current_eco_config_name,current_expo_config_name,current_terra_config_name)
            ubertool = ubertool_tuple[0]
            uber_dict = ubertool_tuple[1]
            ubertool_config_name = uber_dict['config_name']
            ubertools.append(uber_dict)
            current_config_number += 1
            current_use_config_name = use_config_name_prefix + str(current_config_number)
            current_pest_config_name = pest_config_name_prefix + str(current_config_number)
            current_aqua_config_name = aqua_config_name_prefix + str(current_config_number)
            current_eco_config_name = eco_config_name_prefix + str(current_config_number)
            current_expo_config_name = expo_config_name_prefix + str(current_config_number)
            current_terra_config_name = terra_config_name_prefix + str(current_config_number)
            current_ubertool_config_name = ubertool_config_name_prefix + str(current_config_number)
            batch_ubertool_config_names.append(current_ubertool_config_name)
        #create Batch object
        uber_pickle = pickle.dumps(ubertools)
        batch.ubertools=uber_pickle
        batch.put()
        batch_dict['id'] = str(batch.key())
        batch_dict['ubertools'] = ubertools
    #test if only partial configs were passed
    elif current_use_config_name in keys or current_pest_config_name in keys or current_aqua_config_name in keys or current_eco_config_name in keys or current_expo_config_name in keys or current_terra_config_name in keys:
        batch_use_config_names.append(current_use_config_name)
        batch_pest_config_names.append(current_pest_config_name)
        batch_aqua_config_names.append(current_aqua_config_name)
        batch_eco_config_names.append(current_eco_config_name)
        batch_expo_config_names.append(current_expo_config_name)
        batch_terra_config_names.append(current_terra_config_name)
        current_config_number = 1
        use_configs = []
        current_use_config_name = use_config_name_prefix + str(current_config_number)
        while current_use_config_name in keys:
            use_tuple = retrieveUseConfigFromForm(data, current_use_config_name)
            use_configs.append(use_tuple[1])
            current_config_number += 1
            current_use_config_name = use_config_name_prefix + str(current_config_number)
        batch_dict["uses"] = use_configs
        current_config_number = 1
        pest_configs = []
        current_pest_config_name = pest_config_name_prefix + str(current_config_number)
        while current_pest_config_name in keys:
            pest_tuple = retrievePestConfigFromForm(data, current_pest_config_name)
            pest_configs.append(pest_tuple[1])
            current_config_number += 1
            current_pest_config_name = pest_config_name_prefix + str(current_config_number)
        batch_dict["pests"] = pest_configs
        current_config_number = 1
        aqua_configs = []
        current_aqua_config_name = aqua_config_name_prefix + str(current_config_number)
        while current_aqua_config_name in keys:
            aqua_tuple = retrieveAquaConfigFromForm(data, current_aqua_config_name)
            aqua_configs.append(aqua_tuple[1])
            current_config_number += 1
            current_aqua_config_name = aqua_config_name_prefix + str(current_config_number)
        batch_dict["aquas"] = aqua_configs
        current_config_number = 1
        eco_configs = []
        current_eco_config_name = eco_config_name_prefix + str(current_config_number)
        while current_eco_config_name in keys:
            eco_tuple = retrieveEcoConfigFromForm(data, current_eco_config_name)
            eco_configs.append(eco_tuple[1])
            current_config_number += 1
            current_eco_config_name = eco_config_name_prefix + str(current_config_number)
        batch_dict["ecos"] = eco_configs
        current_config_number = 1
        expo_configs = []
        current_expo_config_name = expo_config_name_prefix + str(current_config_number)
        while current_expo_config_name in keys:
            expo_tuple = retrieveExpoConfigFromForm(data, current_expo_config_name)
            expo_configs.append(expo_tuple[1])
            current_config_number += 1
            current_expo_config_name = expo_config_name_prefix + str(current_config_number)
        batch_dict["expos"] = expo_configs
        current_config_number = 1
        terra_configs = []
        current_terra_config_name = terra_config_name_prefix + str(current_config_number)
        while current_terra_config_name in keys:
            terra_tuple = retrieveTerraConfigFromForm(data, current_terra_config_name)
            terra_configs.append(terra_tuple[1])
            current_config_number += 1
            current_terraa_config_name = terra_config_name_prefix + str(current_config_number)
        batch_dict["terras"] = terra_configs
        #create Batch object
        if 'uses' in batch_dict:
            uses_pickle = pickle.dumps(batch_ubertool_config_names)
            batch.uses = uses_pickle
        if 'pests' in batch_dict:
            pests_pickle = pickle.dumps(batch_pest_config_names)
            batch.pests = pests_pickle
        if 'aquas' in batch_dict:
            aquas_pickle = pickle.dumps(batch_aqua_config_names)
            batch.aquas = aquas_pickle
        if 'ecos' in batch_dict:
            ecos_pickle = pickle.dumps(batch_eco_config_names)
            batch.ecos = ecos_pickle
        if 'expos' in batch_dict:
            expos_pickle = pickle.dumps(batch_expo_config_names)
            batch.expos = expos_pickle
        if 'terras' in batch_dict:
            terras_pickle = pickle.dumps(batch_terra_config_names)
            batch.terras = terras_pickle
        batch.put()
        batch_dict['id'] = str(batch.key())
        logger.info(batch.to_xml())
    else:
        uber_pickle = pickle.dumps(batch_ubertool_config_names)
        batch.ubertools=uber_pickle
        batch.put()
        logger.info(batch.to_xml())
        batch_dict['id'] = str(batch.key())
        batch_dict["ubertools"] = ubertools
    return batch_dict
        
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class UbertoolBatchConfigurationService(webapp.RequestHandler):
    
    def post(self):
        logger = logging.getLogger("RunUbertoolConfigurationPage")
        data = simplejson.loads(self.request.body)
        data = convert(data)
        logger.info(data)
        batch_dict = retrieveBatchUbertoolConfiguration(data)
        batch_json = simplejson.dumps(batch_dict)
        logger.info(batch_json)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(batch_json)
        
        
app = webapp.WSGIApplication([('/ubertool-batch-configuration', UbertoolBatchConfigurationService)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()