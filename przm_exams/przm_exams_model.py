import logging
import keys_Picloud_S3
import base64
import urllib
from google.appengine.api import urlfetch
import json
import os
import sys
from datetime import datetime, timedelta
import rest_funcs


############Provide the key and connect to EC2##############################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
url_part1 = os.environ['UBERTOOL_REST_SERVER']
###########################################################################  

Planting_pool={'NC Sweet Potato MLRA-133': '0805', 'ID Potato   MLRA-11B': '2505', 'NY Grape   MLRA-100/101': '2505', 'CA Citrus   MLRA-17': '2512', 'OR Hops   MLRA-2': '2503', 'FL Sugarcane   MLRA-156A': '2512', 'OR Mint   MLRA-2': '0804', 'FL Citrus   MLRA-156A': '2512', 'CA Almonds MLRA-17': '0901', 'ND Canola   MLRA-55A': '0905', 'MI Asparagus MLRA-96': '0906', 'PR Coffee MLRA-270': '2512', 'FL Avocado MLRA-156A': '2202', 'NC Tobacco   MLRA-133A': '0904', 'CA Grape  MLRA-17': '2501', 'FL Cucumber   MLRA-156A': '0910', 'OH Corn   MLRA-111': '2404', 'NC Apple   MLRA-130': '2503', 'CA Onions MLRA-17': '0901', 'PA Turf  MLRA-148': '2503', 'MI Beans MLRA-99': '2505', 'GA Onions MLRA-153A/133A': '0809', 'LA Sugarcane   MLRA-131': '2512', 'NC Corn - E   MLRA-153A': '0804', 'OR Christmas Trees  MLRA-2': '2512', 'MN Sugarbeet   MLRA-56': '0905', 'FL Turf  MLRA-155': '2501', 'MS Cotton   MLRA-134': '2404', 'MS Soybean   MLRA-134': '0904', 'GA Pecan   MLRA-133A': '0904', 'OR Filberts   MLRA-2': '2202', 'OR Grass Seed   MLRA-2': '0909', 'GA Peach   MLRA-133A': '2202', 'FL Carrots MLRA-156B': '0910', 'NC Cotton   MLRA-133A': '2505', 'CA Lettuce  MLRA-14': '0902', 'FL Tomato   MLRA-155': '2501', 'OR Apple   MLRA-2': '2503', 'ND Wheat   MLRA-56': '0905', 'CA Tomato MLRA-17': '2202', 'PA Corn   MLRA-148': '0904', 'FL Peppers MLRA-156A': '2508', 'MS Corn   MLRA-134': '0304', 'MI Cherry   MLRA-96': '2404', 'IL Corn   MLRA-108': '2404', 'ME Potato   MLRA-146': '2505', 'FL Strawberry   MLRA-155': '2409', 'KS Sorghum   MLRA-112': '1305', 'PA Apple   MLRA-148': '0904', 'CA Cotton   MLRA-17': '2404', 'NC Peanut   MLRA-153A': '0905', 'FL Cabbage   MLRA-155': '0910'}
EMergence_pool={'NC Sweet Potato MLRA-133': '1505', 'ID Potato   MLRA-11B': '0106', 'NY Grape   MLRA-100/101': '0106', 'CA Citrus   MLRA-17': '0101', 'OR Hops   MLRA-2': '0104', 'FL Sugarcane   MLRA-156A': '0101', 'OR Mint   MLRA-2': '1504', 'FL Citrus   MLRA-156A': '0101', 'CA Almonds MLRA-17': '1601', 'ND Canola   MLRA-55A': '1605', 'MI Asparagus MLRA-96': '1606', 'PR Coffee MLRA-270': '0101', 'FL Avocado MLRA-156A': '0103', 'NC Tobacco   MLRA-133A': '1604', 'CA Grape  MLRA-17': '0102', 'FL Cucumber   MLRA-156A': '1610', 'OH Corn   MLRA-111': '0105', 'NC Apple   MLRA-130': '0104', 'CA Onions MLRA-17': '1601', 'PA Turf  MLRA-148': '0104', 'MI Beans MLRA-99': '0106', 'GA Onions MLRA-153A/133A': '1509', 'LA Sugarcane   MLRA-131': '0101', 'NC Corn - E   MLRA-153A': '1504', 'OR Christmas Trees  MLRA-2': '0101', 'MN Sugarbeet   MLRA-56': '1605', 'FL Turf  MLRA-155': '0102', 'MS Cotton   MLRA-134': '0105', 'MS Soybean   MLRA-134': '1604', 'GA Pecan   MLRA-133A': '1604', 'OR Filberts   MLRA-2': '0103', 'OR Grass Seed   MLRA-2': '1609', 'GA Peach   MLRA-133A': '0103', 'FL Carrots MLRA-156B': '1610', 'NC Cotton   MLRA-133A': '0106', 'CA Lettuce  MLRA-14': '1602', 'FL Tomato   MLRA-155': '0102', 'OR Apple   MLRA-2': '0104', 'ND Wheat   MLRA-56': '1605', 'CA Tomato MLRA-17': '0103', 'PA Corn   MLRA-148': '1604', 'FL Peppers MLRA-156A': '0109', 'MS Corn   MLRA-134': '1004', 'MI Cherry   MLRA-96': '0105', 'IL Corn   MLRA-108': '0105', 'ME Potato   MLRA-146': '0106', 'FL Strawberry   MLRA-155': '0110', 'KS Sorghum   MLRA-112': '2005', 'PA Apple   MLRA-148': '1604', 'CA Cotton   MLRA-17': '0105', 'NC Peanut   MLRA-153A': '1605', 'FL Cabbage   MLRA-155': '1610'}
MAturation_pool={'NC Sweet Potato MLRA-133': '1509', 'ID Potato   MLRA-11B': '1508', 'NY Grape   MLRA-100/101': '0107', 'CA Citrus   MLRA-17': '0201', 'OR Hops   MLRA-2': '3007', 'FL Sugarcane   MLRA-156A': '0201', 'OR Mint   MLRA-2': '2507', 'FL Citrus   MLRA-156A': '0201', 'CA Almonds MLRA-17': '0208', 'ND Canola   MLRA-55A': '1508', 'MI Asparagus MLRA-96': '2508', 'PR Coffee MLRA-270': '0201', 'FL Avocado MLRA-156A': '1511', 'NC Tobacco   MLRA-133A': '0707', 'CA Grape  MLRA-17': '0103', 'FL Cucumber   MLRA-156A': '0512', 'OH Corn   MLRA-111': '2609', 'NC Apple   MLRA-130': '0305', 'CA Onions MLRA-17': '0106', 'PA Turf  MLRA-148': '1504', 'MI Beans MLRA-99': '2707', 'GA Onions MLRA-153A/133A': '0106', 'LA Sugarcane   MLRA-131': '0201', 'NC Corn - E   MLRA-153A': '2808', 'OR Christmas Trees  MLRA-2': '0201', 'MN Sugarbeet   MLRA-56': '0110', 'FL Turf  MLRA-155': '1502', 'MS Cotton   MLRA-134': '0709', 'MS Soybean   MLRA-134': '0109', 'GA Pecan   MLRA-133A': '2109', 'OR Filberts   MLRA-2': '1504', 'OR Grass Seed   MLRA-2': '1505', 'GA Peach   MLRA-133A': '1505', 'FL Carrots MLRA-156B': '1501', 'NC Cotton   MLRA-133A': '0108', 'CA Lettuce  MLRA-14': '0505', 'FL Tomato   MLRA-155': '2104', 'OR Apple   MLRA-2': '3004', 'ND Wheat   MLRA-56': '2507', 'CA Tomato MLRA-17': '0107', 'PA Corn   MLRA-148': '0407', 'FL Peppers MLRA-156A': '1511', 'MS Corn   MLRA-134': '2208', 'MI Cherry   MLRA-96': '0707', 'IL Corn   MLRA-108': '2109', 'ME Potato   MLRA-146': '0110', 'FL Strawberry   MLRA-155': '1011', 'KS Sorghum   MLRA-112': '2009', 'PA Apple   MLRA-148': '1005', 'CA Cotton   MLRA-17': '2009', 'NC Peanut   MLRA-153A': '0110', 'FL Cabbage   MLRA-155': '0802'}
HArvest_pool={'NC Sweet Potato MLRA-133': '2209', 'ID Potato   MLRA-11B': '1509', 'NY Grape   MLRA-100/101': '1510', 'CA Citrus   MLRA-17': '3112', 'OR Hops   MLRA-2': '0109', 'FL Sugarcane   MLRA-156A': '3112', 'OR Mint   MLRA-2': '0108', 'FL Citrus   MLRA-156A': '3112', 'CA Almonds MLRA-17': '1309', 'ND Canola   MLRA-55A': '2508', 'MI Asparagus MLRA-96': '1503', 'PR Coffee MLRA-270': '3112', 'FL Avocado MLRA-156A': '3011', 'NC Tobacco   MLRA-133A': '1607', 'CA Grape  MLRA-17': '3108', 'FL Cucumber   MLRA-156A': '1012', 'OH Corn   MLRA-111': '2510', 'NC Apple   MLRA-130': '2510', 'CA Onions MLRA-17': '1506', 'PA Turf  MLRA-148': '0111', 'MI Beans MLRA-99': '0409', 'GA Onions MLRA-153A/133A': '1506', 'LA Sugarcane   MLRA-131': '3112', 'NC Corn - E   MLRA-153A': '1209', 'OR Christmas Trees  MLRA-2': '3112', 'MN Sugarbeet   MLRA-56': '1510', 'FL Turf  MLRA-155': '1512', 'MS Cotton   MLRA-134': '2209', 'MS Soybean   MLRA-134': '1010', 'GA Pecan   MLRA-133A': '0110', 'OR Filberts   MLRA-2': '1011', 'OR Grass Seed   MLRA-2': '3006', 'GA Peach   MLRA-133A': '3108', 'FL Carrots MLRA-156B': '2201', 'NC Cotton   MLRA-133A': '0111', 'CA Lettuce  MLRA-14': '1205', 'FL Tomato   MLRA-155': '1505', 'OR Apple   MLRA-2': '3110', 'ND Wheat   MLRA-56': '0508', 'CA Tomato MLRA-17': '0109', 'PA Corn   MLRA-148': '0110', 'FL Peppers MLRA-156A': '0112', 'MS Corn   MLRA-134': '0209', 'MI Cherry   MLRA-96': '2107', 'IL Corn   MLRA-108': '2010', 'ME Potato   MLRA-146': '0510', 'FL Strawberry   MLRA-155': '1502', 'KS Sorghum   MLRA-112': '0110', 'PA Apple   MLRA-148': '1510', 'CA Cotton   MLRA-17': '1111', 'NC Peanut   MLRA-153A': '1010', 'FL Cabbage   MLRA-155': '1502'}


def get_jid(chem_name, noa, scenarios, unit, met_o, inp_o, run_o, exam_o, 
            MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft, 
            Apt_p, DayRe, Ap_mp, Ar, CAM_f_p, EFF_p, Drft_p, DEPI_f,
            farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out):
    all_dic = {"chem_name" : chem_name,
               "noa" : noa,
               "scenarios" : scenarios,
               "unit" : unit,
               "met" : met_o,
               "inp" : inp_o,
               "run" : run_o,
               "exam" : exam_o,
               "MM" : MM,
               "DD" : DD,
               "YY" : YY,
               "CAM_f" : CAM_f,
               "DEPI" : DEPI_text,
               "Ar" : Ar_text,
               "EFF" : EFF,
               "Drft" : Drft,
               "farm" : farm,
               "mw" : mw,
               "sol" : sol,
               "koc" : koc,
               "vp" : vp,
               "aem" : aem,
               "anm" : anm,
               "aqp" : aqp,
               "tmper" : tmper,
               "n_ph" : n_ph,
               "ph_out" : ph_out,
               "hl_out" : hl_out}

    data=json.dumps(all_dic)
    jid=rest_funcs.gen_jid()
    logging.info(jid)
    url=url_part1 + '/przm_exams/' + jid
    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)
    output_val = json.loads(response.content)['result']
    return(jid, output_val)



#########################################################    
##########Estimate relevant apply date###################
#########################################################
def es_date(NOA, Scenarios, Apt, DayRe, Date_inp):
    NOA=int(NOA)
    YY=[None]*NOA
    MM=[None]*NOA
    DD=[None]*NOA
    for i in range(NOA):
        Apt_t=Apt[i]
        DayRe_t=DayRe[i]
        Date_inp_t=Date_inp[i]
        if Apt_t=='1':
            YY_t=1961
            MM_t=Planting_pool[Scenarios][2:4]
            DD_t=Planting_pool[Scenarios][0:2]
        elif Apt_t=='2':
            YY_t=1961
            MM_t=EMergence_pool[Scenarios][2:4]
            DD_t=EMergence_pool[Scenarios][0:2]
        elif Apt_t=='3':
            YY_t=1961
            MM_t=MAturation_pool[Scenarios][2:4]
            DD_t=MAturation_pool[Scenarios][0:2]
        elif Apt_t=='4':
            YY_t=1961
            MM_t=HArvest_pool[Scenarios][2:4]
            DD_t=HArvest_pool[Scenarios][0:2]
        elif Apt_t=='5':
            YY_t=1961
            MM_t=Date_inp_t[0:2]
            DD_t=Date_inp_t[3:5]
                          
        DayRe_t=float(DayRe_t)             
        now = datetime(YY_t,int(MM_t),int(DD_t))
        Later = now + timedelta(days=DayRe_t)
        Later=str(Later)
        YY[i]=(Later[2:4])
        MM[i]=(Later[5:7])
        DD[i]=(Later[8:10])  
    return MM,DD 


#########################################################    
##########Select application method######################
#########################################################
def Ap_m_select(Ap_m, CAM_1, CAM_2, CAM_3, CAM_4):
    if Ap_m=='1':
        CAM_f=CAM_1
        Ap_mp='Aerial'
        EFF='.9500'
        EFF_p='0.95'
        Drft='.0500'
        Drft_p='0.05'
            
    elif Ap_m=='2':
        CAM_f=CAM_2
        Ap_mp='Ground Sprayer'
        EFF='.9900'
        EFF_p='0.99'
        Drft='.0100'
        Drft_p='0.0100'
        
    elif Ap_m=='3':
        CAM_f=CAM_3
        Ap_mp='Airblast'
        EFF='.9900'
        EFF_p='0.99'
        Drft='.0500'
        Drft_p='0.05'
                                        
    elif Ap_m=='4':
        CAM_f=CAM_4
        Ap_mp='Other equipment'
        EFF='1.000'
        EFF_p='1.00'
        Drft='.0000'                    
        Drft_p='0.00'
    return Ap_mp, CAM_f, EFF_p, Drft_p, EFF, Drft

def CAM_select(CAM_f, DEPI):
    if CAM_f=='1':
        CAM_f_p='1-Soil applied (4cm incorporation, linearly decreasing with depth)'
        DEPI='4'
    elif CAM_f=='2':
        CAM_f_p='2-Interception based on crop canopy'
        DEPI='4'
    elif CAM_f=='4':
        CAM_f_p='4-Soil applied (user-defined incorporation, uniform with depth)'
        DEPI=DEPI        
    elif CAM_f=='5':
        CAM_f_p='5-Soil applied (user-defined incorporation, linearly increasing with depth)'
        DEPI=DEPI 
    elif CAM_f=='6':
        CAM_f_p='6-Soil applied (user-defined incorporation, linearly decreasing with depth)'
        DEPI=DEPI 
    elif CAM_f=='7':
        CAM_f_p='7-Soil applied, T-Band granular application'
        DEPI=DEPI 
    elif CAM_f=='8':
        CAM_f_p='8-Soil applied, chemical incorporated depth specified by user'            
        DEPI=DEPI 
    elif CAM_f=='9':
        CAM_f_p='9-Linear foliar based on crop canop'
        DEPI=DEPI 
    return CAM_f_p, DEPI, CAM_f

class przm_exams(object):
    def __init__(self, chem_name, noa, scenarios, unit, met_o, inp_o, run_o, exam_o, 
                 MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft, 
                 Apt_p, DayRe, Ap_mp, Ar, CAM_f_p, EFF_p, Drft_p, DEPI_f,
                 farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out):

        self.chem_name=chem_name
        self.noa=int(noa)
        self.scenarios=scenarios
        self.unit=unit

        self.met_o=met_o
        self.inp_o=inp_o
        self.run_o=run_o
        self.exam_o=exam_o

        self.MM=MM
        self.DD=DD
        self.YY=YY
        self.CAM_f=CAM_f
        self.DEPI_text=DEPI_text
        self.Ar_text=Ar_text
        self.EFF=EFF
        self.Drft=Drft

        self.Apt_p=Apt_p
        self.DayRe=DayRe
        self.Ap_mp=Ap_mp
        self.Ar=Ar
        self.CAM_f_p=CAM_f_p
        self.EFF_p=EFF_p
        self.Drft_p=Drft_p
        self.DEPI_f=DEPI_f

        if self.unit=='1':
            self.unit_p='kg/ha'
        elif self.unit=='2':
            self.unit_p='lb/acre'

        self.farm=farm
        self.mw=mw
        self.sol=sol
        self.koc=koc
        self.vp=vp
        self.aem=aem
        self.anm=anm
        self.aqp=aqp
        self.tmper=tmper
        self.n_ph=n_ph
        self.ph_out=ph_out
        self.hl_out=hl_out
        self.final_res=get_jid(chem_name, noa, scenarios, unit, met_o, inp_o, run_o, exam_o, 
                               MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft, 
                               Apt_p, DayRe, Ap_mp, Ar, CAM_f_p, EFF_p, Drft_p, DEPI_f,
                               farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out)
        self.jid = self.final_res[0]
        self.link = self.final_res[1][0]


###############PRZM plots#############################
        self.x_precip=[float(i) for i in self.final_res[1][1]]
        self.x_runoff=[float(i) for i in self.final_res[1][2]]
        self.x_et=[float(i) for i in self.final_res[1][3]]
        self.x_irr=[float(i) for i in self.final_res[1][4]]
        self.x_leachate=[float(i) for i in self.final_res[1][5]]
        self.x_pre_irr=[i+j for i,j in zip(self.x_precip, self.x_irr)]
        self.x_leachate=[i/100000 for i in self.x_leachate]

        self.Lim_inst=[float(i)*1000 for i in self.final_res[1][6]]
        self.Lim_24h=[float(i)*1000 for i in self.final_res[1][7]]
        self.Lim_96h=[float(i)*1000 for i in self.final_res[1][8]]
        self.Lim_21d=[float(i)*1000 for i in self.final_res[1][9]]
        self.Lim_60d=[float(i)*1000 for i in self.final_res[1][10]]
        self.Lim_90d=[float(i)*1000 for i in self.final_res[1][11]]
        self.Lim_y=[float(i)*1000 for i in self.final_res[1][12]]

        self.Ben_inst=[float(i)*1000 for i in self.final_res[1][13]]
        self.Ben_24h=[float(i)*1000 for i in self.final_res[1][14]]
        self.Ben_96h=[float(i)*1000 for i in self.final_res[1][15]]
        self.Ben_21d=[float(i)*1000 for i in self.final_res[1][16]]
        self.Ben_60d=[float(i)*1000 for i in self.final_res[1][17]]
        self.Ben_90d=[float(i)*1000 for i in self.final_res[1][18]]
        self.Ben_y=[float(i)*1000 for i in self.final_res[1][19]]

