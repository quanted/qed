# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from uber import uber_lib
import numpy as np
import cgi
import cgitb
from es_mapping import es_mapping_model, es_mapping_tables


import logging
logger = logging.getLogger('ES Model')

class ESOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()   

        # NSF = form.getvalue('NSF')
        # NSP = form.getvalue('NSP')
        # NSM = form.getvalue('NSM')
        # Crop = form.getvalue('Crop')
        # Pesticide = form.getvalue('Pesticide')

        # IUCN_Amphibians = form.getvalue('IUCN_Amphibians')
        # IUCN_Birds = form.getvalue('IUCN_Birds')
        # IUCN_Mammals = form.getvalue('IUCN_Mammals')
        # IUCN_Mammals_Marine = form.getvalue('IUCN_Mammals_Marine')
        # IUCN_Coral = form.getvalue('IUCN_Coral')
        # IUCN_Reptiles = form.getvalue('IUCN_Reptiles')
        # IUCN_Seagrasses = form.getvalue('IUCN_Seagrasses')
        # IUCN_SeaCucumbers = form.getvalue('IUCN_SeaCucumbers')        
        # IUCN_Mangrove = form.getvalue('IUCN_Mangrove')
        # IUCN_MarineFish = form.getvalue('IUCN_MarineFish')

        # USFWS_p = form.getvalue('USFWS_p')
        # USFWS_l = form.getvalue('USFWS_l')
        # print "USFWS_l=", USFWS_l

        args={}
        for key in form:
            args[key] = form.getvalue(key)
        es_obj = es_mapping_model.es_mapping(args)
        logger.info(vars(es_obj))


        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie)    
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'es_mapping','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
            'model':'es_mapping', 
            'model_attributes':'Endangered Species Mapper Output'})
        html = html + es_mapping_tables.table_all(es_obj)

        # html = html + template.render(templatepath+'ManykmlDropbox_test.html', {
        #        'NSF':NSF,
        #        'NSP':NSP,
        #        'NSM':NSM,
        #        'Crop':Crop,
        #        'Pesticide':Pesticide,
        #        'IUCN_Amphibians':IUCN_Amphibians,
        #        'IUCN_Birds':IUCN_Birds,
        #        'IUCN_Mammals':IUCN_Mammals,
        #        'IUCN_Mammals_Marine':IUCN_Mammals_Marine,
        #        'IUCN_Coral':IUCN_Coral,
        #        'IUCN_Reptiles':IUCN_Reptiles,
        #        'IUCN_Seagrasses':IUCN_Seagrasses,
        #        'IUCN_SeaCucumbers':IUCN_SeaCucumbers,
        #        'IUCN_Mangrove':IUCN_Mangrove,
        #        'IUCN_MarineFish':IUCN_MarineFish,
        #        'USFWS_p':USFWS_p,
        #        'USFWS_l':USFWS_l})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', ESOutputPage)], debug=True)
        

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()                                                                                                         




    

