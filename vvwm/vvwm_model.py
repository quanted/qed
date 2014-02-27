# -*- coding: utf-8 -*-
import keys_Picloud_S3
import base64
import urllib
from google.appengine.api import urlfetch
import json
from datetime import datetime, timedelta
import time
from collections import OrderedDict

import os
import logging
logger = logging.getLogger('vvwm Model')

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
url_part1 = os.environ['UBERTOOL_REST_SERVER']

###########################################################################

def get_jid(run_type, working_dir,
          koc_check, Koc, soilHalfLifeBox, soilTempBox1, foliarHalfLifeBox,
          wc_hl, w_temp, bm_hl, ben_temp, ap_hl, p_ref, h_hl, mwt, vp, sol, Q10Box,
          convertSoil, convert_Foliar, convertWC, convertBen, convertAP, convertH,
          deg_check, totalApp,
          SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, appNumber_year, app_date_type, DepthIncorp, PestAppyRate, localEff, localSpray,
          scenID,
          buried, D_over_dx, PRBEN, benthic_depth, porosity, bulk_density, FROC2, DOC2, BNMAS,
          DFAC, SUSED, CHL, FROC1, DOC1, PLMAS,
          firstYear, lastyear, vvwmSimType,
          afield, area, depth_0, depth_max,
          ReservoirFlowAvgDays):

    all_dic = {"working_dir": working_dir,
              "koc_check": koc_check,
              "Koc": Koc,
              "soilHalfLifeBox": soilHalfLifeBox,
              "soilTempBox1": soilTempBox1,
              "foliarHalfLifeBox": foliarHalfLifeBox,
              "wc_hl": wc_hl,
              "w_temp": w_temp,
              "bm_hl": bm_hl,
              "ben_temp": ben_temp,
              "ap_hl": ap_hl,
              "p_ref": p_ref,
              "h_hl": h_hl,
              "mwt": mwt,
              "vp": vp,
              "sol": sol,
              "Q10Box": Q10Box,
              "convertSoil":convertSoil,
              "convert_Foliar":convert_Foliar,
              "convertWC":convertWC,
              "convertBen":convertBen,
              "convertAP":convertAP,
              "convertH":convertH,
              "deg_check": deg_check,
              "totalApp": totalApp,
              "SpecifyYears": SpecifyYears,
              "ApplicationTypes": ApplicationTypes,
              "PestAppyDay": PestAppyDay,
              "PestAppyMon": PestAppyMon,
              "appNumber_year": appNumber_year,
              "app_date_type": app_date_type,
              "DepthIncorp": DepthIncorp,
              "PestAppyRate": PestAppyRate,
              "localEff": localEff,
              "localSpray": localSpray,
              "scenID": scenID,
              "buried": buried,
              "D_over_dx": D_over_dx,
              "PRBEN": PRBEN,
              "benthic_depth": benthic_depth,
              "porosity": porosity,
              "bulk_density": bulk_density,
              "FROC2": FROC2,
              "DOC2": DOC2,
              "BNMAS": BNMAS,
              "DFAC": DFAC,
              "SUSED": SUSED,
              "CHL": CHL,
              "FROC1": FROC1,
              "DOC1": DOC1,
              "PLMAS": PLMAS,
              "firstYear": firstYear,
              "lastyear": lastyear,
              "vvwmSimType": vvwmSimType,
              "afield": afield,
              "area": area,
              "depth_0": depth_0,
              "depth_max": depth_max,
              "ReservoirFlowAvgDays": ReservoirFlowAvgDays}
    logger.info(all_dic)
    data = json.dumps(all_dic)

    ts = datetime.now()
    if(time.daylight):
        ts1 = timedelta(hours=-4)+ts
    else:
        ts1 = timedelta(hours=-5)+ts
    jid = ts1.strftime('%Y%m%d%H%M%S%f')
    url=url_part1+'/vvwm/'+jid 


    if run_type == "single" or "qaqc":
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
        # logger.info(json.loads(response.content))
        output_val = json.loads(response.content)['result']
        # jid= json.loads(response.content)['jid']
        # print "filepath=", output_val[4]
        # self.elapsed = (time.clock() - start)
        return(jid, output_val)


# Commented out at end of this file - What does this do?
def get_upload(src1, name1):
    all_dic = {"src1": src1, "name1": name1, "model_name":"vvwm"}
    data = json.dumps(all_dic)
    url=url_part1+'/file_upload'
    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   

def convert_dict_key(key):
    try:
        return int(key.split('_')[2])
    except:
        return key

class vvwm(object):
  def __init__(self, dictionary):
    logger.info('===================')
    logger.info('===================')
    # logger.info(os.getcwd())
    # cwd=os.getcwd()+'/vvwm/'

    alphanum_key = lambda (key, value): convert_dict_key(key)
    dictionary_1 = sorted(dictionary.items(), key=alphanum_key)
    self.dictionary = OrderedDict(dictionary_1)
    logger.info(self.dictionary)
    # Model input variables not on input page:
    self.working_dir = "/"
    self.dvf_file = "test.dvf"         # TEMPORARILY FIXED VALUE
    self.firstYear = 1961              # TEMPORARILY FIXED VALUE (from above *.dvf file)
    self.lastYear = 1990               # TEMPORARILY FIXED VALUE (from above *.dvf file)
    self.totalApp = '1'                # Remove when Number of Apps is enabled
    self.SpecifyYears = ""             # Remove when Specify Years is enabled
    self.app_date_type = ""            # Remove when Relative Dates is enabled
    self.ReservoirFlowAvgDays = "0"
    # Create empty lists for variables below that need to be lists
    # Lists = ['','',''] are setup that way bc those inputs could potential be left blank
    self.ApplicationTypes = []
    self.DepthIncorp = []
    self.PestAppyDay = []
    self.PestAppyMon = []
    self.appNumber_year = []
    # Year will be added here when "Specify Years" for Applications is enabled
    self.PestAppyRate = []
    self.tempEffPondList = []
    self.tempSprayPondList = []
    self.tempEffResList = []
    self.tempSprayResList = []
    self.tempEffCustomList = []
    self.tempSprayCustomList = []
    self.localEff = []
    self.localSpray = []
    self.Koc = []
    self.soilHalfLifeBox = []
    self.soilTempBox1 = []
    self.foliarHalfLifeBox = []
    self.wc_hl = []
    self.w_temp = []
    self.bm_hl = []
    self.ben_temp = []
    self.ap_hl = []
    self.p_ref = []
    self.h_hl = []
    self.mwt = []
    self.vp = []
    self.sol = []
    # Molar Conversion Factors
    self.convertSoil = []
    self.convert_Foliar = []
    self.convertWC = []
    self.convertBen = []
    self.convertAP = []
    self.convertH = []
    # Watershed and Water Body Dimensions
    self.afield = []
    self.area = []
    self.depth_0 = []
    self.depth_max = []
    # Run function to fill above lists from input page
    self.fillData()

  def fillData(self):
    for k, v in self.dictionary.items():
        setattr(self, k, v)
        if k.startswith('sp_year'):
            self.useYears = 1
        elif k.startswith('deg_check'):
            self.deg_check = int(v) + 1
        elif k.startswith('cam_a_'):
            self.ApplicationTypes.append(int(v))
        elif k.startswith('depth_a_'):
            self.DepthIncorp.append(v)
        elif k.startswith('day_a_'):
            self.PestAppyDay.append(v)
        elif k.startswith('mon_a_'):
            self.PestAppyMon.append(v)
        elif k.startswith('rate_a_'):
            self.PestAppyRate.append(v)
        elif k.startswith('eff_pond_a_'):
            self.tempEffPondList.append(v)
        elif k.startswith('drift_pond_a_'):
            self.tempSprayPondList.append(v)
        elif k.startswith('eff_res_a_'):
            self.tempEffResList.append(v)
        elif k.startswith('drift_res_a_'):
            self.tempSprayResList.append(v)
        elif k.startswith('eff_custom_a_'):
            self.tempEffCustomList.append(v)
        elif k.startswith('drift_custom_a_'):
            self.tempSprayCustomList.append(v)
        elif k.startswith('foliarHalfLife_'):
            self.foliarHalfLifeBox.append(float(v))
        elif k.startswith('Koc_'):
            self.Koc.append(float(v))
        elif k.startswith('soilHalfLife_'):
            self.soilHalfLifeBox.append(float(v))
        elif k.startswith('soilHalfLifeRef'):
            self.soilTempBox1.append(float(v))
        elif k.startswith('wc_hl_'):
            self.wc_hl.append(float(v))
        elif k.startswith('w_temp_'):
            self.w_temp.append(float(v))
        elif k.startswith('bm_hl_'):
            self.bm_hl.append(float(v))
        elif k.startswith('ben_temp_'):
            self.ben_temp.append(float(v))
        elif k.startswith('ap_hl_'):
            self.ap_hl.append(float(v))
        elif k.startswith('p_ref_'):
            self.p_ref.append(float(v))
        elif k.startswith('h_hl_'):
            self.h_hl.append(float(v))
        elif k.startswith('mwt_'):
            self.mwt.append(float(v))
        elif k.startswith('vp_'):
            self.vp.append(float(v))
        elif k.startswith('sol_'):
            self.sol.append(float(v))
        elif k.startswith('QT'):
            self.Q10Box = v
        elif k.startswith('noa'):
            self.totalApp = v
        elif k.startswith('specifyYears'):
            self.SpecifyYears = v
        elif k.startswith('app_date_type'):
            self.app_date_type = v
        elif k.startswith('BurialFlag'):
            self.buried = v
        elif k.startswith('SimTypeFlag'):
            self.vvwmSimType = v
        # Molar Conversion Factors
        elif k.startswith('convertSoil'):
            self.convertSoil.append(v)
        elif k.startswith('convert_Foliar'):
            self.convert_Foliar.append(v)
        elif k.startswith('convertWC'):
            self.convertWC.append(v)
        elif k.startswith('convertBen'):
            self.convertBen.append(v)
        elif k.startswith('convertAP'):
            self.convertAP.append(v)
        elif k.startswith('convertH'):
            self.convertH.append(v)
    # Fill localEff & localSpray Lists:
    self.localEff.append(self.tempEffPondList)
    self.localEff.append(self.tempEffResList)
    self.localEff.append(self.tempEffCustomList)
    self.localSpray.append(self.tempSprayPondList)
    self.localSpray.append(self.tempSprayResList)
    self.localSpray.append(self.tempSprayCustomList)
    # Define based on SimTypeFlag:
    if self.vvwmSimType == '5': #EPA Pond Only
        self.afield.append(self.dictionary['fieldArea_Pond'])
        self.area.append(self.dictionary['wbArea_Pond'])
        self.depth_0.append(self.dictionary['depth_0_Pond'])
        self.depth_max.append(self.dictionary['depth_max_Pond'])
    if self.vvwmSimType == '4': #EPA Reservoir Only
        self.afield.append(self.dictionary['fieldArea_Reservoir'])
        self.area.append(self.dictionary['wbArea_Reservoir'])
        self.depth_0.append(self.dictionary['depth_0_Reservoir'])
        self.depth_max.append(self.dictionary['depth_max_Reservoir'])
    if self.vvwmSimType == '6' or self.vvwmSimType == '1' or self.vvwmSimType == '2' or self.vvwmSimType == '3': #Reservoir w/ User Avg, Varying Volume, Constant Volume (w/o Flowthrough), OR Constant Volume (w/ Flowthrough)
        self.afield.append(self.dictionary['fieldArea_Custom'])
        self.area.append(self.dictionary['wbArea_Custom'])
        self.depth_0.append(self.dictionary['depth_0_Custom'])
        self.depth_max.append(self.dictionary['depth_max_Custom'])
    if self.vvwmSimType == '6': #Reservoir w/ User Avg (only)
        self.ReservoirFlowAvgDays = self.dictionary['resAvgBox_Custom']
    if self.vvwmSimType == '0': #EPA Reservoir & Pond (this will run the model twice, w/ two separate transfer files)
        self.afield.append(self.dictionary['fieldArea_Pond'])
        self.area.append(self.dictionary['wbArea_Pond'])
        self.depth_0.append(self.dictionary['depth_0_Pond'])
        self.depth_max.append(self.dictionary['depth_max_Pond'])
        self.afield.append(self.dictionary['fieldArea_Reservoir'])
        self.area.append(self.dictionary['wbArea_Reservoir'])
        self.depth_0.append(self.dictionary['depth_0_Reservoir'])
        self.depth_max.append(self.dictionary['depth_max_Reservoir'])

    self.final_res=get_jid(self.run_type, self.working_dir,
          self.koc_check, self.Koc, self.soilHalfLifeBox, self.soilTempBox1, self.foliarHalfLifeBox,
          self.wc_hl, self.w_temp, self.bm_hl, self.ben_temp, self.ap_hl, self.p_ref, self.h_hl, self.mwt, self.vp, self.sol, self.Q10Box,
          self.convertSoil, self.convert_Foliar, self.convertWC, self.convertBen, self.convertAP, self.convertH,
          self.deg_check, self.totalApp,
          self.SpecifyYears, self.ApplicationTypes, self.PestAppyDay, self.PestAppyMon, self.appNumber_year, self.app_date_type, self.DepthIncorp, self.PestAppyRate, self.localEff, self.localSpray,
          self.scenID,
          self.buried, self.D_over_dx, self.PRBEN, self.benthic_depth, self.porosity, self.bulk_density, self.FROC2, self.DOC2, self.BNMAS,
          self.DFAC, self.SUSED, self.CHL, self.FROC1, self.DOC1, self.PLMAS,
          self.firstYear, self.lastYear, self.vvwmSimType,
          self.afield, self.area, self.depth_0, self.depth_max,
          self.ReservoirFlowAvgDays)
    # logger.info(self.final_res)

    # Assign output variables to the vvwm_obj:
    self.WC_peak = self.final_res[1][1]
    self.WC_chronic = self.final_res[1][2]
    self.WC_simavg = self.final_res[1][3]
    self.WC_4dayavg = self.final_res[1][4]
    self.WC_21dayavg = self.final_res[1][5]
    self.WC_60dayavg = self.final_res[1][6]
    self.WC_90dayavg = self.final_res[1][7]
    self.Ben_peak = self.final_res[1][8]
    self.Ben_21dayavg = self.final_res[1][9]
    self.Ben_convfact = self.final_res[1][10]
    self.Ben_massfract = self.final_res[1][11]
    self.EWCH_washout = self.final_res[1][12]
    self.EWCH_metabolism = self.final_res[1][13]
    self.EWCH_hydrolysis = self.final_res[1][14]
    self.EWCH_photolysis = self.final_res[1][15]
    self.EWCH_volatilization = self.final_res[1][16]
    self.EWCH_total = self.final_res[1][17]
    self.EBH_burial = self.final_res[1][18]
    self.EBH_metabolism = self.final_res[1][19]
    self.EBH_hydrolysis = self.final_res[1][20]
    self.EBH_total = self.final_res[1][21]
    self.RT_runoff = self.final_res[1][22]
    self.RT_erosion = self.final_res[1][23]
    self.RT_drift = self.final_res[1][24]
    self.peak_li1 = self.final_res[1][25]
    self.ben_peak_li1 = self.final_res[1][26]
    self.peak_li2 = self.final_res[1][27]
    self.ben_peak_li2 = self.final_res[1][28]
    self.link = self.final_res[1][0]
    self.jid = self.final_res[0]
    self.src1 = self.final_res[1][29]
    self.name1 = self.final_res[1][30]

    get_upload(self.src1, self.name1)