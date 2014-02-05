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
logger = logging.getLogger('PRZM5 Model')

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
url_part1 = os.environ['UBERTOOL_REST_SERVER']

###########################################################################

def get_jid(run_type, pfac, snowmelt, evapDepth, 
            uslek, uslels, uslep, fieldSize, ireg, slope, hydlength,
            canopyHoldup, rootDepth, canopyCover, canopyHeight,
            NumberOfFactors, useYears,
            USLE_day, USLE_mon, USLE_year, USLE_c, USLE_n, USLE_cn,
            firstyear, lastyear,
            dayEmerge_text, monthEmerge_text, dayMature_text, monthMature_text, dayHarvest_text, monthHarvest_text, addYearM, addYearH,
            irflag, tempflag,
            fleach, depletion, rateIrrig,
            albedo, bcTemp, Q10Box, soilTempBox1,
            numHoriz,
            SoilProperty_thick, SoilProperty_compartment, SoilProperty_bulkden, SoilProperty_maxcap, SoilProperty_mincap, SoilProperty_oc, SoilProperty_sand, SoilProperty_clay,
            rDepthBox, rDeclineBox, rBypassBox,
            eDepthBox, eDeclineBox,
            appNumber_year, totalApp,
            SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, Rela_a, app_date_type, DepthIncorp, PestAppyRate, localEff, localSpray,
            PestDispHarvest,
            nchem, convert_Foliar1, parentTo3, deg1To2, foliarHalfLifeBox,
            koc_check, Koc,
            soilHalfLifeBox,
            convertSoil1, convert1to3, convert2to3):


    all_dic = {"pfac": pfac, 
               "snowmelt": snowmelt, 
               "evapDepth": evapDepth,
               "uslek": uslek,
               "uslels": uslels,
               "uslep": uslep,
               "fieldSize": fieldSize,
               "ireg": ireg,
               "slope": slope,
               "hydlength": hydlength,
               "canopyHoldup": canopyHoldup,
               "rootDepth": rootDepth,
               "canopyCover": canopyCover,
               "canopyHeight": canopyHeight,
               "NumberOfFactors": NumberOfFactors,
               "useYears": useYears,
               "USLE_day": USLE_day,
               "USLE_mon": USLE_mon,
               "USLE_year": USLE_year,
               "USLE_c": USLE_c,
               "USLE_n": USLE_n,
               "USLE_cn": USLE_cn,
               "firstyear": firstyear,
               "lastyear": lastyear,
               "dayEmerge_text": dayEmerge_text,
               "monthEmerge_text": monthEmerge_text,
               "dayMature_text": dayMature_text,
               "monthMature_text": monthMature_text,
               "dayHarvest_text": dayHarvest_text,
               "monthHarvest_text": monthHarvest_text,
               "addYearM": addYearM,
               "addYearH": addYearH,
               "irflag": irflag,
               "tempflag": tempflag,
               "fleach": fleach,
               "depletion": depletion,
               "rateIrrig": rateIrrig,
               "albedo": albedo,
               "bcTemp": bcTemp,
               "Q10Box": Q10Box,
               "soilTempBox1": soilTempBox1,
               "numHoriz": numHoriz,
               "SoilProperty_thick": SoilProperty_thick,
               "SoilProperty_compartment": SoilProperty_compartment,
               "SoilProperty_bulkden": SoilProperty_bulkden,
               "SoilProperty_maxcap": SoilProperty_maxcap,
               "SoilProperty_mincap": SoilProperty_mincap,
               "SoilProperty_oc": SoilProperty_oc,
               "SoilProperty_sand": SoilProperty_sand,
               "SoilProperty_clay": SoilProperty_clay,
               "rDepthBox": rDepthBox,
               "rDeclineBox": rDeclineBox,
               "rBypassBox": rBypassBox,
               "eDepthBox": eDepthBox,
               "eDeclineBox": eDeclineBox,
               "appNumber_year": appNumber_year,
               "totalApp": totalApp,
               "SpecifyYears": SpecifyYears,
               "ApplicationTypes": ApplicationTypes,
               "PestAppyDay": PestAppyDay,
               "PestAppyMon": PestAppyMon,
               "Rela_a": Rela_a,
               "app_date_type": app_date_type,
               "DepthIncorp": DepthIncorp,
               "PestAppyRate": PestAppyRate,
               "localEff": localEff,
               "localSpray": localSpray,
               "PestDispHarvest": PestDispHarvest,
               "nchem": nchem,
               "convert_Foliar1": convert_Foliar1,
               "parentTo3": parentTo3,
               "deg1To2": deg1To2,
               "foliarHalfLifeBox": foliarHalfLifeBox,
               "koc_check": koc_check,
               "Koc": Koc,
               "soilHalfLifeBox": soilHalfLifeBox,
               "convertSoil1": convertSoil1,
               "convert1to3": convert1to3,
               "convert2to3": convert2to3}
    # logger.info(all_dic)
    data = json.dumps(all_dic)

    ts = datetime.now()
    if(time.daylight):
        ts1 = timedelta(hours=-4)+ts
    else:
        ts1 = timedelta(hours=-5)+ts
    jid = ts1.strftime('%Y%m%d%H%M%S%f')
    url=url_part1 + '/przm5/' + jid 


    if run_type == "single" or "qaqc":
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
        output_val = json.loads(response.content)['result']
        # jid= json.loads(response.content)['jid']
        # print "filepath=", output_val[4]
        # self.elapsed = (time.clock() - start)
        return(jid, output_val)

def get_upload(src1, name1):
    all_dic = {"src1": src1, "name1": name1, "model_name":"przm5"}
    data = json.dumps(all_dic)
    url=url_part1+'/file_upload'
    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   

def convert_dict_key(key):
    try:
        return int(key.split('_')[2])
    except:
        return key

class przm5(object):
     def __init__(self, dictionary):
        logger.info('===================')
        # logger.info(os.getcwd())
        # cwd=os.getcwd()+'/PRZM5/'


        alphanum_key = lambda (key, value): convert_dict_key(key)
        dictionary_1 = sorted(dictionary.items(), key=alphanum_key)
        dictionary = OrderedDict(dictionary_1)

        self.hydlength = 356.8  #for pond
        self.useYears = 0
        self.tempflag = 0
        self.Q10Box = 2.0
        self.soilTempBox1 = 25.0
        self.SpecifyYears = 0
        self.parentTo3 = 0
        self.deg1To2 = 0
        self.convert1to3 = 0
        self.convert2to3 = 0


        self.Rela_a = []
        self.USLE_day = []
        self.USLE_mon = []
        self.USLE_year = []
        self.USLE_c = []
        self.USLE_n = []
        self.USLE_cn = []
        self.SoilProperty_thick = []
        self.SoilProperty_compartment = []
        self.SoilProperty_bulkden = []
        self.SoilProperty_maxcap = []
        self.SoilProperty_mincap = []
        self.SoilProperty_oc = []
        self.SoilProperty_sand = []
        self.SoilProperty_clay = []
        self.ApplicationTypes = []
        self.DepthIncorp = []
        self.PestAppyDay = []
        self.PestAppyMon = []
        self.PestAppyRate = []
        self.localEff = []
        self.localSpray = []
        self.foliarHalfLifeBox = []
        self.Koc = []
        self.soilHalfLifeBox = []


        for k, v in dictionary.items():
            setattr(self, k, v)
            if k.startswith('sp_year'):
                self.useYears = 1
            elif k.startswith('tempflag_check'):
                self.tempflag = 1
            elif k.startswith('day_t_'):
                self.USLE_day.append(v)
            elif k.startswith('mon_t_'):
                self.USLE_mon.append(v)
            elif k.startswith('year_t_'):
                self.USLE_year.append(v)
            elif k.startswith('c_t_'):
                self.USLE_c.append(v)
            elif k.startswith('n_t_'):
                self.USLE_n.append(v)
            elif k.startswith('cn_t_'):
                self.USLE_cn.append(v)
            elif k.startswith('cn_t_'):
                self.USLE_cn.append(v)
            elif k.startswith('thick_h_'):
                self.SoilProperty_thick.append(v)
            elif k.startswith('n_h_'):
                self.SoilProperty_compartment.append(int(v))
            elif k.startswith('rho_h_'):
                self.SoilProperty_bulkden.append(float(v))
            elif k.startswith('max_h_'):
                self.SoilProperty_maxcap.append(float(v))
            elif k.startswith('min_h_'):
                self.SoilProperty_mincap.append(float(v))
            elif k.startswith('oc_h_'):
                self.SoilProperty_oc.append(float(v))
            elif k.startswith('sand_h_'):
                self.SoilProperty_sand.append(float(v))
            elif k.startswith('clay_h_'):
                self.SoilProperty_clay.append(float(v))
            elif k.startswith('deg_check'):
                self.nchem = int(v) + 1
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
            elif k.startswith('eff_a_'):
                self.localEff.append(v)
            elif k.startswith('drift_a_'):
                self.localSpray.append(v)
            elif k.startswith('foliarHalfLife_'):
                self.foliarHalfLifeBox.append(float(v))
            elif k.startswith('Koc_'):
                self.Koc.append(float(v))
            elif k.startswith('soilHalfLife_'):
                self.soilHalfLifeBox.append(float(v))
            elif k.startswith('rela_a_'):
                self.Rela_a.append(v)


        self.NumberOfFactors = int(self.nott)
        # dvf_file_read = open(cwd+self.dvf_file,'r')
        # content = dvf_file_read.readlines()
        # self.firstyear = int(content[0][5:7])
        # self.lastyear = int(content[-1][5:7])

        self.firstyear = 61
        self.lastyear = 90

        #Record 12
        self.dayEmerge_text=int(self.Emerge_text[0:2])
        self.monthEmerge_text=int(self.Emerge_text[3:5])
        self.dateEmerge_text = datetime.strptime(str(self.dayEmerge_text)+str(self.monthEmerge_text), "%d%m") 
        self.dayMature_text=int(self.Mature_text[0:2])
        self.monthMature_text=int(self.Mature_text[3:5])
        self.dateMature_text = datetime.strptime(str(self.dayMature_text)+str(self.monthMature_text), "%d%m") 
        self.dayHarvest_text=int(self.Harvest_text[0:2])
        self.monthHarvest_text=int(self.Harvest_text[3:5])
        self.dateHarvest_text = datetime.strptime(str(self.dayHarvest_text)+str(self.monthHarvest_text), "%d%m") 
        if self.dateEmerge_text.date()>self.dateMature_text.date():
            self.addYearM = 1
        else:
            self.addYearM = 0

        if self.dateMature_text.date()>self.dateHarvest_text.date():
            self.addYearH = 1
        else:
            self.addYearH = 0

        #Record 13-14
        # if int(self.irflag) == 1:
        #     self.irtype = 3
        # elif int(self.irflag) == 2:
        #     self.irtype = 4

        #Record 18
        self.numHoriz = int(self.noh)

        #Record C1
        self.appNumber_year = int(self.noa)
        self.totalApp = (self.lastyear - self.firstyear + 1)*self.appNumber_year

        #Record C3
        self.PestDispHarvest = int(self.PestDispHarvest)

        #Record C5, C9
        if int(self.deg2_source) == 0:
            self.deg1To2 = 1
            self.convert1to3 = self.convertSoil2
        else:
            self.parentTo3 = 1
            self.convert2to3 = self.convertSoil2

        self.dateEmerge_text = str(self.dateEmerge_text)
        self.dateMature_text = str(self.dateMature_text)
        self.dateHarvest_text = str(self.dateHarvest_text)

        self.final_res=get_jid(self.run_type, self.pfac, self.snowmelt, self.evapDepth, 
                               self.uslek, self.uslels, self.uslep, self.fieldSize, self.ireg, self.slope, self.hydlength,
                               self.canopyHoldup, self.rootDepth, self.canopyCover, self.canopyHeight,
                               self.NumberOfFactors, self.useYears,
                               self.USLE_day, self.USLE_mon, self.USLE_year, self.USLE_c, self.USLE_n, self.USLE_cn,
                               self.firstyear, self.lastyear,
                               self.dayEmerge_text, self.monthEmerge_text, self.dayMature_text, self.monthMature_text, self.dayHarvest_text, self.monthHarvest_text, self.addYearM, self.addYearH,
                               self.irflag, self.tempflag,
                               self.fleach, self.depletion, self.rateIrrig,
                               self.albedo, self.bcTemp, self.Q10Box, self.soilTempBox1,
                               self.numHoriz,
                               self.SoilProperty_thick, self.SoilProperty_compartment, self.SoilProperty_bulkden, self.SoilProperty_maxcap, self.SoilProperty_mincap, self.SoilProperty_oc, self.SoilProperty_sand, self.SoilProperty_clay,
                               self.rDepthBox, self.rDeclineBox, self.rBypassBox,
                               self.eDepthBox, self.eDeclineBox,
                               self.appNumber_year, self.totalApp,
                               self.SpecifyYears, self.ApplicationTypes, self.PestAppyDay, self.PestAppyMon, self.Rela_a, self.app_date_type, self.DepthIncorp, self.PestAppyRate, self.localEff, self.localSpray,
                               self.PestDispHarvest,
                               self.nchem, self.convert_Foliar1, self.parentTo3, self.deg1To2, self.foliarHalfLifeBox,
                               self.koc_check, self.Koc,
                               self.soilHalfLifeBox,
                               self.convertSoil1, self.convert1to3, self.convert2to3)
        # self.info = self.final_res

        self.jid = self.final_res[0]
        self.link = self.final_res[1][0]
        self.PRCP_IRRG_sum = self.final_res[1][1]
        self.RUNF_sum = self.final_res[1][2]
        self.CEVP_TETD_sum = self.final_res[1][3]
        self.src1 = self.final_res[1][4]
        self.name1 = self.final_res[1][5]
        logger.info("++++++++++++++++++")
        logger.info(self.src1)
        logger.info(self.name1)
        logger.info("++++++++++++++++++")
        get_upload(self.src1, self.name1)
