
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

@author: jharston
"""

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
import logging
import sys
sys.path.append("utils")
sys.path.append("ubertool")
from CSVTestParamsLoader import CSVTestParamsLoader
import json_utils
from aquatic_toxicity_batch_output import AquaticToxicityBatchLoader
from ecosystem_inputs_batch_output import EcosystemInputsBatchLoader
from exposure_concentrations_batch_output import ExposureConcentrationsBatchLoader
from pesticide_properties_batch_output import PesticidePropertiesBatchLoader
from terrestrial_toxicity_batch_output import TerrestrialToxicityBatchLoader
from use_batch_output import UseBatchLoader
from use import Use, UsePropertiesRetrievalService
from pesticide_properties import PesticideProperties, PestPropertiesRetrievalService
from aquatic_toxicity import AquaticToxicity, AquaticToxicityPropertiesRetrievalService
from ecosystem_inputs import EcosystemInputs, EcosystemInputsPropertiesRetrievalService
from exposure_concentrations import ExposureConcentrations, ExposureConcentrationsRetrievalService
from terrestrial_toxicity import TerrestrialToxicity, TerrestrialPropertiesRetrievalService
from ubertool.ubertool import Ubertool
sys.path.append("../batch")
from batch.batch import Batch
from batch.batch_processor import BatchService
from django.utils import simplejson
import pickle
from run_ubertool_input import UbertoolInputPage
    
logger = logging.getLogger("Run_Ubertool_Batch_Output")

batchProcessor = BatchService()
usePropService = UsePropertiesRetrievalService()
pestPropService = PestPropertiesRetrievalService()
aquaPropService = AquaticToxicityPropertiesRetrievalService()
ecoPropService = EcosystemInputsPropertiesRetrievalService()
expoPropService = ExposureConcentrationsRetrievalService()
terrePropService = TerrestrialPropertiesRetrievalService()

def loop_batch_file(thefile):
    params_matrix = get_params_matrix(thefile)
    user = users.get_current_user()
    batch_ubertools = []
    batch_ubertools_list = []
    for batch_index in range(len(params_matrix.get('cas_number'))):
        ubertool_dict = {}
        ubertool_config_name = None
        if "ubertool_config_name" in params_matrix:
            ubertool_config_name = params_matrix.get("ubertool_config_name")[batch_index]
        q = db.Query(Ubertool)
        if user:
            q.filter('user =',user)
        if ubertool_config_name:
            q.filter("config_name =", ubertool_config_name)
        ubertool = q.get()
        if ubertool is None:
            ubertool = Ubertool()
            ubertool.config_name = ubertool_config_name
        if user:
            ubertool.user = user
        aqua_toxicity = AquaticToxicityBatchLoader()
        ubertool.aqua = aqua_toxicity.batchLoadAquaticToxicityConfigs(params_matrix,batch_index,ubertool)
        ubertool_dict['aqua'] = aquaPropService.get(ubertool.aqua.config_name)
        ecosystem_inputs = EcosystemInputsBatchLoader()
        ubertool.eco = ecosystem_inputs.batchLoadEcosystemInputsConfigs(params_matrix,batch_index,ubertool)
        ubertool_dict['eco'] = ecoPropService.get(ubertool.eco.config_name)
        exposure_concentrations = ExposureConcentrationsBatchLoader()
        ubertool.expo = exposure_concentrations.batchLoadExposureConcentrationsConfigs(params_matrix,batch_index,ubertool)
        ubertool_dict['expo'] = expoPropService.get(ubertool.expo.config_name)
        pesticide_properties = PesticidePropertiesBatchLoader()
        ubertool.pest = pesticide_properties.batchLoadPesticidePropertiesConfigs(params_matrix,batch_index,ubertool)
        ubertool_dict['pest'] = pestPropService.get(ubertool.pest.config_name)
        terrestrial_toxicity = TerrestrialToxicityBatchLoader()
        ubertool.terra = terrestrial_toxicity.batchLoadTerrestrialToxicityConfigs(params_matrix,batch_index,ubertool)
        ubertool_dict['terra'] = terrePropService.get(ubertool.terra.config_name)
        use = UseBatchLoader()
        ubertool.use = use.batchLoadUseConfigs(params_matrix,batch_index,ubertool)
        ubertool_dict['use'] = usePropService.get(ubertool.use.config_name)
        logger.info(ubertool.to_xml())
        ubertool.put()
        ubertool_dict['config_name'] = ubertool_config_name
        batch_ubertools_list.append(ubertool_dict)
        batch_ubertools.append(ubertool)
    return (batch_ubertools, batch_ubertools_list)

def get_params_matrix(thefile):
    csvTestParamsLoader = CSVTestParamsLoader(thefile)
    csvTestParamsLoader.loadParamsMatrixFromUpFile(thefile)
    return csvTestParamsLoader.params_matrix

class RunUbertoolBatchPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['upfile1']
        loop_batch_file(thefile)

app = webapp.WSGIApplication([('/.*', RunUbertoolBatchPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()