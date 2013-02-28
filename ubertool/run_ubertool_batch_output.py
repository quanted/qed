
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
from aquatic_toxicity_batch_output import AquaticToxicityBatchLoader
from ecosystem_inputs_batch_output import EcosystemInputsBatchLoader
from exposure_concentrations_batch_output import ExposureConcentrationsBatchLoader
from pesticide_properties_batch_output import PesticidePropertiesBatchLoader
from terrestrial_toxicity_batch_output import TerrestrialToxicityBatchLoader
from use_batch_output import UseBatchLoader
from use import Use
from ubertool.ubertool import Ubertool
    
logger = logging.getLogger("Run_Ubertool_Batch_Output")


def loop_batch_file(thefile):
    params_matrix = get_params_matrix(thefile)
    user = users.get_current_user()
    for batch_index in range(len(params_matrix.get('cas_number'))):
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
        ecosystem_inputs = EcosystemInputsBatchLoader()
        ubertool.eco = ecosystem_inputs.batchLoadEcosystemInputsConfigs(params_matrix,batch_index,ubertool)
        exposure_concentrations = ExposureConcentrationsBatchLoader()
        ubertool.expo = exposure_concentrations.batchLoadExposureConcentrationsConfigs(params_matrix,batch_index,ubertool)
        pesticide_properties = PesticidePropertiesBatchLoader()
        ubertool.pest = pesticide_properties.batchLoadPesticidePropertiesConfigs(params_matrix,batch_index,ubertool)
        terrestrial_toxicity = TerrestrialToxicityBatchLoader()
        ubertool.terra = terrestrial_toxicity.batchLoadTerrestrialToxicityConfigs(params_matrix,batch_index,ubertool)
        use = UseBatchLoader()
        ubertool.use = use.batchLoadUseConfigs(params_matrix,batch_index,ubertool)
        logger.info(ubertool.to_xml())
        ubertool.put()


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