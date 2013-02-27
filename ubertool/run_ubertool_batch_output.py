
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
from ubertool import run_ubertool_db
from StringIO import StringIO
import cStringIO
import csv
import logging
import sys
sys.path.append("utils")
sys.path.append("ubertool")
from CSVTestParamsLoader import CSVTestParamsLoader
from aquatic_toxicity_batch_output import AquaticToxicityBatchLoader
from ecosystem_inputs_batch_output import EcosystemInputsBatchLoader
from exposure_concentrations_batch_output import ExposureConcentrationsBatchLoader
from pesticide_properties_batch_output import PesticidePropertiesBatchLoader
from terrestrial_toxicity_batch_output import TerrestrialToxicityBatchLoader
from use_batch_output import UseBatchLoader
    
logger = logging.getLogger("Run_Ubertool_Batch_Output")


def loop_batch_file(thefile):
    params_matrix = get_params_matrix(thefile)
    aqua_toxicity = AquaticToxicityBatchLoader()
    params_matrix = aqua_toxicity.batchLoadAquaticToxicityConfigs(params_matrix)
    print params_matrix
    ecosystem_inputs = EcosystemInputsBatchLoader()
    params_matrix = ecosystem_inputs.batchLoadEcosystemInputsConfigs(params_matrix)
    print params_matrix
    exposure_concentrations = ExposureConcentrationsBatchLoader()
    params_matrix = exposure_concentrations.batchLoadExposureConcentrationsConfigs(params_matrix)
    print params_matrix
    pesticide_properties = PesticidePropertiesBatchLoader()
    params_matrix = pesticide_properties.batchLoadPesticidePropertiesConfigs(params_matrix)
    print params_matrix
    terrestrial_toxicity = TerrestrialToxicityBatchLoader()
    params_matrix = terrestrial_toxicity.batchLoadTerrestrialToxicityConfigs(params_matrix)
    print params_matrix
    use = UseBatchLoader()
    params_matrix = use.batchLoadUseConfigs(params_matrix)
    print params_matrix
    

def get_params_matrix(thefile):
    csvTestParamsLoader = CSVTestParamsLoader(thefile)
    csvTestParamsLoader.loadParamsMatrixFromUpFile(thefile)
    return csvTestParamsLoader.params_matrix

class RunUbertoolBatchPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['upfile1']
        loop_batch_file(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_nomodellinks.html', {'title2':'Ecosystem Inputs'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {'model':'run_ubertool'})
        html = html + str(run_ubertool_db.RunUbertoolInp())
        #html = html + template.render(templatepath + '04ubertext_checkbox.html', {})
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', RunUbertoolBatchPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()