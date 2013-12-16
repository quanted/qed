import keys_Picloud_S3
import base64
import urllib
from google.appengine.api import urlfetch
import json
import logging
logger = logging.getLogger('Geneec Model')

class geneec(object):
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
        api_key=keys_Picloud_S3.picloud_api_key
        api_secretkey=keys_Picloud_S3.picloud_api_secretkey
        base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
        http_headers = {'Authorization' : 'Basic %s' % base64string}
        ###########################################################################

        ########call the function################# 
        url='https://api.picloud.com/r/3303/geneec_fortran_s1' 

        APPRAT = self.application_rate
        APPNUM = self.number_of_applications
        APSPAC = self.interval_between_applications
        KOC = self.Koc
        METHAF = self.aerobic_soil_metabolism
        WETTED = json.dumps(self.wet_in)
        METHOD = json.dumps(self.application_method)
        AIRFLG = json.dumps(self.aerial_size_dist)
        YLOCEN = self.no_spray_drift
        GRNFLG = json.dumps(self.ground_spray_type)
        GRSIZE = json.dumps(self.spray_quality)
        ORCFLG = json.dumps(self.airblast_type)
        INCORP = self.incorporation_depth
        SOL = self.solubility
        METHAP = self.aerobic_aquatic_metabolism
        HYDHAP = self.hydrolysis
        FOTHAP = self.photolysis_aquatic_half_life

        data = urllib.urlencode({"APPRAT":APPRAT, "APPNUM":APPNUM, "APSPAC":APSPAC, "KOC":KOC, "METHAF":METHAF, "WETTED":WETTED,
                                 "METHOD":METHOD, "AIRFLG":AIRFLG, "YLOCEN":YLOCEN, "GRNFLG":GRNFLG, "GRSIZE":GRSIZE,
                                 "ORCFLG":ORCFLG, "INCORP":INCORP, "SOL":SOL, "METHAP":METHAP, "HYDHAP":HYDHAP, "FOTHAP":FOTHAP})
        
        logger.info({"APPRAT":APPRAT, "APPNUM":APPNUM, "APSPAC":APSPAC, "KOC":KOC, "METHAF":METHAF, "WETTED":WETTED,
                     "METHOD":METHOD, "AIRFLG":AIRFLG, "YLOCEN":YLOCEN, "GRNFLG":GRNFLG, "GRSIZE":GRSIZE,
                     "ORCFLG":ORCFLG, "INCORP":INCORP, "SOL":SOL, "METHAP":METHAP, "HYDHAP":HYDHAP, "FOTHAP":FOTHAP})
        
        if run_type == "individual":
            response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers)    
            self.jid= json.loads(response.content)['jid']
            self.output_st = ''
            
            while self.output_st!="done":
                self.response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %self.jid, headers=http_headers)
                self.output_st = json.loads(self.response_st.content)['info']['%s' %self.jid]['status']

            self.url_val = 'https://api.picloud.com/job/result/?jid='+str(self.jid)
            self.response_val = urlfetch.fetch(url=self.url_val, method=urlfetch.GET, headers=http_headers)
            self.output_val = json.loads(self.response_val.content)['result']

        if run_type == "batch":
            response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers)    
            self.jid= json.loads(response.content)['jid']
            self.output_st = ''
            
            # while self.output_st!="done":
            #     self.response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %self.jid, headers=http_headers)
            #     self.output_st = json.loads(self.response_st.content)['info']['%s' %self.jid]['status']

            # self.url_val = 'https://api.picloud.com/job/result/?jid='+str(self.jid)
            # self.response_val = urlfetch.fetch(url=self.url_val, method=urlfetch.GET, headers=http_headers)
            # self.output_val = json.loads(self.response_val.content)['result']

