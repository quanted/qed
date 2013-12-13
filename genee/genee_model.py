import keys_Picloud_S3
import base64
import urllib
from google.appengine.api import urlfetch
import json
import logging
logger = logging.getLogger('Geneec Model')

class genee(object):
    def __init__(self, run_type, chem_name, application_target, application_rate, number_of_applications, interval_between_applications, Koc, aerobic_soil_metabolism, wet_in, application_method, application_method_label, aerial_size_dist, ground_spray_type, airblast_type, spray_quality, no_spray_drift, incorporation_depth, solubility, aerobic_aquatic_metabolism, hydrolysis, photolysis_aquatic_half_life):
        self.run_type = run_type
        self.chem_name = chem_name
        self.application_target = application_target
        self.application_rate = application_rate
        self.number_of_applications = number_of_applications
        self.interval_between_applications = interval_between_applications
        self.Koc = Koc
        self.aerobic_soil_metabolism = aerobic_soil_metabolism
        self.wet_in = wet_in
        self.application_method = application_method
        if application_method == 'a':
            self.application_method_label = 'Aerial Spray'
        if application_method == 'b':
            self.application_method_label = 'Ground Spray'
        if application_method == 'c':
            self.application_method_label = 'Airblast Spray (Orchard & Vineyard)'
        if application_method == 'd':
            self.application_method_label = 'Granular (Non-spray)'

        self.aerial_size_dist = aerial_size_dist
        self.ground_spray_type = ground_spray_type
        self.airblast_type = airblast_type
        self.spray_quality = spray_quality
        self.no_spray_drift = no_spray_drift
        self.incorporation_depth = incorporation_depth
        self.solubility = solubility
        self.aerobic_aquatic_metabolism = aerobic_aquatic_metabolism
        self.hydrolysis = hydrolysis
        self.photolysis_aquatic_half_life = photolysis_aquatic_half_life

        ############Provide the key and connect to the picloud####################

        ########call the function################# 

        APPRAT = self.application_rate
        APPNUM = self.number_of_applications
        APSPAC = self.interval_between_applications
        KOC = self.Koc
        METHAF = self.aerobic_soil_metabolism
        WETTED = self.wet_in
        METHOD = self.application_method
        AIRFLG = self.aerial_size_dist
        YLOCEN = self.no_spray_drift
        GRNFLG = self.ground_spray_type
        GRSIZE = self.spray_quality
        ORCFLG = self.airblast_type
        INCORP = self.incorporation_depth
        SOL = self.solubility
        METHAP = self.aerobic_aquatic_metabolism
        HYDHAP = self.hydrolysis
        FOTHAP = self.photolysis_aquatic_half_life


        all_dic = {"APPRAT":APPRAT, "APPNUM":APPNUM, "APSPAC":APSPAC, "KOC":KOC, "METHAF":METHAF, "WETTED":WETTED,
                   "METHOD":METHOD, "AIRFLG":AIRFLG, "YLOCEN":YLOCEN, "GRNFLG":GRNFLG, "GRSIZE":GRSIZE,
                   "ORCFLG":ORCFLG, "INCORP":INCORP, "SOL":SOL, "METHAP":METHAP, "HYDHAP":HYDHAP, "FOTHAP":FOTHAP}
        logger.info(all_dic)

        data = json.dumps(all_dic)
        # url='http://localhost:7777/myroute/' 
        url='http://54.204.192.91:7777/myroute/' 


        http_headers = {'Content-Type' : 'application/json'}
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers)   
        self.data_a= json.loads(response.content)["ff"]
        # self.data_a= response

        logger.info(self.data_a)


        # if run_type == "individual":
        #     response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers)    
        #     self.jid= json.loads(response.content)['jid']
        #     self.output_st = ''

