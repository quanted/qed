
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
from google.appengine.api import urlfetch
from django.utils import simplejson
import urllib
from ubertool import run_ubertool_db
from StringIO import StringIO
import cStringIO
import csv
import logging
import sys
import datetime
sys.path.append("utils")
from CSVTestParamsLoader import CSVTestParamsLoader

sys.path.append("ubertool")
import aquatic_toxicity_batch_output
import ecosystem_inputs_batch_output
import exposure_concentrations_batch_output
import pesticide_properties_batch_output
import terrestrial_toxicity_batch_output
import use_batch_output
    
logger = logging.getLogger("Run_Ubertool_Batch_Output")

ubertool_config_service_base_url = os.environ['UBERTOOL_MONGO_SERVER']

def loop_batch_file(thefile):
    params_matrix = get_params_matrix(thefile)
    logger.info("Params Matrix:")
    logger.info(params_matrix)
    batch_config_props = {}
    ubertools = []
    for batch_index in range(len(params_matrix.get('cas_number'))):
        batch_index = int(batch_index)
        ubertool_configuration_properties = {}
        ubertool_config_name = None
        if "ubertool_config_name" in params_matrix:
            ubertool_config_name = params_matrix.get("ubertool_config_name")[batch_index]
            ubertool_configuration_properties['config_name'] = ubertool_config_name
        ubertool_configuration_properties = aquatic_toxicity_batch_output.batchLoadAquaticToxicityConfigs(params_matrix,batch_index,ubertool_configuration_properties)
        ubertool_configuration_properties = ecosystem_inputs_batch_output.batchLoadEcosystemInputsConfigs(params_matrix,batch_index,ubertool_configuration_properties)
        ubertool_configuration_properties = exposure_concentrations_batch_output.batchLoadExposureConcentrationsConfigs(params_matrix,batch_index,ubertool_configuration_properties)
        ubertool_configuration_properties = pesticide_properties_batch_output.batchLoadPesticidePropertiesConfigs(params_matrix,batch_index,ubertool_configuration_properties)
        ubertool_configuration_properties = terrestrial_toxicity_batch_output.batchLoadTerrestrialToxicityConfigs(params_matrix,batch_index,ubertool_configuration_properties)
        ubertool_configuration_properties = use_batch_output.batchLoadUseConfigs(params_matrix,batch_index,ubertool_configuration_properties)
        ubertool_configuration_properties['created'] = str(datetime.datetime.now())

        #TODO: POST ubertool run data to mongodb server
        logger.info("Ubertool CSV-based data:")
        logger.info(ubertool_configuration_properties)
        form_data = simplejson.dumps(ubertool_configuration_properties)
        url = ubertool_config_service_base_url+"/ubertool/ubertool/"+ubertool_config_name
        result = urlfetch.fetch(url=url,
                            payload=form_data,
                            method=urlfetch.POST,
                            headers={'Content-Type': 'application/json'})
        ubertools.append(ubertool_configuration_properties)
        
    #TODO: POST batch data to mongodb server
    batch_config_props['ubertools'] = ubertools
    batchId = str(int(datetime.datetime.now().strftime("%s")) * 1000)
    batch_config_props['batchId']="batch-"+batchId
    batch_config_props['id']="batch-"+batchId
    batch_config_props['created'] = str(datetime.datetime.now())
    logger.info("Ubertool Batch CSV-based data:")
    logger.info(batch_config_props)
    form_data = simplejson.dumps(batch_config_props)
    url = ubertool_config_service_base_url+"/batch"
    result = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
    return result


def get_params_matrix(thefile):
    csvTestParamsLoader = CSVTestParamsLoader(thefile)
    csvTestParamsLoader.loadParamsMatrixFromUpFile(thefile)
    return csvTestParamsLoader.params_matrix

class RunUbertoolBatchPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['upfile1']
        loop_batch_file(thefile)
        self.redirect("user.html")
        

app = webapp.WSGIApplication([('/.*', RunUbertoolBatchPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()