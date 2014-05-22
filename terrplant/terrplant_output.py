# terrplant Version 1.2.2
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import sys
sys.path.append("../utils")
import utils.json_utils
sys.path.append("../terrplant")
from terrplant import terrplant_model,terrplant_parameters,terrplant_tables
from uber import uber_lib
import logging
logger = logging.getLogger('terrplant out')
import rest_funcs


class terrplantExecutePage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        #Get variables needed to construct terrplant object
        version_terrplant = form.getvalue('version_terrplant')
        I = form.getvalue('incorporation')
        A = form.getvalue('application_rate')
        D = form.getvalue('drift_fraction')
        R = form.getvalue('runoff_fraction')
        nms = form.getvalue('EC25_for_nonlisted_seedling_emergence_monocot')
        nds = form.getvalue('EC25_for_nonlisted_seedling_emergence_dicot')
        lms = form.getvalue('NOAEC_for_listed_seedling_emergence_monocot')
        lds = form.getvalue('NOAEC_for_listed_seedling_emergence_dicot')
        #fill out terrplant object with yet to be used data
        chemical_name = form.getvalue('chemical_name')
        # terr.chemical_name = chemical_name
        pc_code = form.getvalue('pc_code')
        # terr.pc_code = pc_code
        use = form.getvalue('use')
        # terr.use = use
        application_method = form.getvalue('application_method')
        # terr.application_method = application_method
        application_form = form.getvalue('application_form')
        # terr.application_form = application_form
        solubility = form.getvalue('solubility')
        # terr.sol = sol
        terr = terrplant_model.terrplant(True,True,version_terrplant,"single",A,I,R,D,nms,lms,nds,lds,chemical_name,pc_code,use,application_method,application_form,solubility)
        nmv = form.getvalue('EC25_for_nonlisted_vegetative_vigor_monocot')
        terr.nmv = nmv
        ndv = form.getvalue('EC25_for_nonlisted_vegetative_vigor_dicot')
        terr.ndv = ndv
        lmv = form.getvalue('NOAEC_for_listed_vegetative_vigor_monocot')
        terr.lmv = lmv
        ldv = form.getvalue('NOAEC_for_listed_vegetative_vigor_dicot')
        terr.ldv = ldv
        logger.info(terr.__dict__)

        text_file = open('terrplant/terrplant_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "TerrPlant Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'terrplant','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                                
        html = html + template.render(templatepath + '04uberoutput_start.html',{
                'model':'terrplant',
                'model_attributes':'TerrPlant Output'})
        html = html + terrplant_tables.timestamp(terr)
        html = html + terrplant_tables.table_all(terrplant_tables.pvheadings, terrplant_tables.pvuheadings,terrplant_tables.deheadings,
                                        terrplant_tables.plantec25noaecheadings,terrplant_tables.plantecdrysemisprayheadings, 
                                        terrplant_tables.sumheadings, terrplant_tables.tmpl, terr)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, terr.__dict__, "terrplant", "single")
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', terrplantExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
