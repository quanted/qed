# -*- coding: utf-8 -*-
import keys_Picloud_S3
import base64
from google.appengine.api import urlfetch
import json
import os
import logging
import rest_funcs

############Provide the key and connect to EC2####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
url_part1 = os.environ['UBERTOOL_REST_SERVER']
###########################################################################

def get_jid(chem_name, scenarios, met, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out):
    all_dic = {"chem_name": chem_name,
               "scenarios": scenarios,
               "met": met,
               "farm": farm,
               "mw": mw,
               "sol": sol,
               "koc": koc,
               "vp": vp,
               "aem": aem,
               "anm": anm,
               "aqp": aqp,
               "tmper": tmper,
               "n_ph": n_ph,
               "ph_out": ph_out,
               "hl_out": hl_out}
    data = json.dumps(all_dic)
    jid=rest_funcs.gen_jid()
    url=url_part1 + '/exams/' + jid 
    response_val = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)
    output_val = json.loads(response_val.content)['result']
    return(jid, output_val)

class exams(object):
    # station_pool={'NC Sweet Potato MLRA-133': 'Raleigh/Durham, NC', 'ID Potato   MLRA-11B': 'Pocatello, ID', 'NY Grape   MLRA-100/101': 'Binghamton, NY', 'CA Citrus   MLRA-17': 'Bakersfield, CA', 'OR Hops   MLRA-2': 'Salem, OR', 'FL Sugarcane   MLRA-156A': 'W Palm Beach, FL', 'OR Mint   MLRA-2': 'Salem, OR', 'FL Citrus   MLRA-156A': 'W Palm Beach, FL', 'CA Almonds MLRA-17': 'Sacramento, CA', 'ND Canola   MLRA-55A': 'Minot, ND', 'MI Asparagus MLRA-96': 'Muskegon, MI', 'PR Coffee MLRA-270': 'San Juan, PR', 'FL Avocado MLRA-156A': 'Miami, FL', 'NC Tobacco   MLRA-133A': 'Raleigh/Durham, NC', 'CA Grape  MLRA-17': 'Fresno, CA', 'FL Cucumber   MLRA-156A': 'W Palm Beach, FL', 'OH Corn   MLRA-111': 'Dayton, OH', 'NC Apple   MLRA-130': 'Asheville, NC', 'CA Onions MLRA-17': 'Bakersfield, CA', 'PA Turf  MLRA-148': 'Harrisburg, PA', 'MI Beans MLRA-99': 'Flint, MI', 'GA Onions MLRA-153A/133A': 'Savannah, GA', 'LA Sugarcane   MLRA-131': 'Baton Rouge, LA', 'NC Corn - E   MLRA-153A': 'Raleigh/Durham, NC', 'OR Christmas Trees  MLRA-2': 'Salem, OR', 'MN Sugarbeet   MLRA-56': 'Fargo, ND', 'FL Turf  MLRA-155': 'Daytona Beach, FL', 'MS Cotton   MLRA-134': 'Jackson, MS', 'MS Soybean   MLRA-134': 'Jackson, MS', 'GA Pecan   MLRA-133A': 'Tallahassee, FL', 'OR Filberts   MLRA-2': 'Salem, OR', 'OR Grass Seed   MLRA-2': 'Salem, OR', 'GA Peach   MLRA-133A': 'Macon, GA', 'FL Carrots MLRA-156B': 'W Palm Beach, FL', 'NC Cotton   MLRA-133A': 'Raleigh/Durham, NC', 'CA Lettuce  MLRA-14': 'Santa Maria, CA', 'FL Tomato   MLRA-155': 'W Palm Beach, FL', 'OR Apple   MLRA-2': 'Salem, OR', 'ND Wheat   MLRA-56': 'Fargo, ND', 'CA Tomato MLRA-17': 'Fresno, CA', 'PA Corn   MLRA-148': 'Harrisburg, PA', 'FL Peppers MLRA-156A': 'W Palm Beach, FL', 'MS Corn   MLRA-134': 'Jackson, MS', 'MI Cherry   MLRA-96': 'Traverse City, MI', 'IL Corn   MLRA-108': 'Peoria, IL', 'ME Potato   MLRA-146': 'Caribou, ME', 'FL Strawberry   MLRA-155': 'Tampa, FL', 'KS Sorghum   MLRA-112': 'Topeka, KS', 'PA Apple   MLRA-148': 'Harrisburg, PA', 'CA Cotton   MLRA-17': 'Fresno, CA', 'NC Peanut   MLRA-153A': 'Raleigh/Durham, NC', 'FL Cabbage   MLRA-155': 'Tampa, FL'}
    def __init__(self, chem_name, scenarios, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out):
        met_pool={'NC Sweet Potato MLRA-133': 'W13722.DVF', 'ID Potato   MLRA-11B': 'W24156.DVF', 'NY Grape   MLRA-100/101': 'W04725.DVF', 'CA Citrus   MLRA-17': 'W23155.DVF', 'OR Hops   MLRA-2': 'W24232.DVF', 'FL Sugarcane   MLRA-156A': 'W12844.DVF', 'OR Mint   MLRA-2': 'W24232.DVF', 'FL Citrus   MLRA-156A': 'W12844.DVF', 'CA Almonds MLRA-17': 'W23232.DVF', 'ND Canola   MLRA-55A': 'W24013.DVF', 'MI Asparagus MLRA-96': 'w14840.DVF', 'PR Coffee MLRA-270': 'W11641.DVF', 'FL Avocado MLRA-156A': 'W12839.DVF', 'NC Tobacco   MLRA-133A': 'W13722.DVF', 'CA Grape  MLRA-17': 'W93193.DVF', 'FL Cucumber   MLRA-156A': 'W12844.DVF', 'OH Corn   MLRA-111': 'W93815.DVF', 'NC Apple   MLRA-130': 'W03812.DVF', 'CA Onions MLRA-17': 'W23155.DVF', 'PA Turf  MLRA-148': 'W14751.DVF', 'MI Beans MLRA-99': 'W14826.DVF', 'GA Onions MLRA-153A/133A': 'W03822.DVF', 'LA Sugarcane   MLRA-131': 'W13970.DVF', 'NC Corn - E   MLRA-153A': 'W13722.DVF', 'OR Christmas Trees  MLRA-2': 'W24232.DVF', 'MN Sugarbeet   MLRA-56': 'W14914.DVF', 'FL Turf  MLRA-155': 'W12834.DVF', 'MS Cotton   MLRA-134': 'W03940.DVF', 'MS Soybean   MLRA-134': 'W03940.DVF', 'GA Pecan   MLRA-133A': 'W93805.DVF', 'OR Filberts   MLRA-2': 'W24232.DVF', 'OR Grass Seed   MLRA-2': 'W24232.DVF', 'GA Peach   MLRA-133A': 'W03813.DVF', 'FL Carrots MLRA-156B': 'W12844.DVF', 'NC Cotton   MLRA-133A': 'W13722.DVF', 'CA Lettuce  MLRA-14': 'W93193.DVF', 'FL Tomato   MLRA-155': 'W12844.DVF', 'OR Apple   MLRA-2': 'W24232.DVF', 'ND Wheat   MLRA-56': 'W14914.DVF', 'CA Tomato MLRA-17': 'W93193.DVF', 'PA Corn   MLRA-148': 'W14751.DVF', 'FL Peppers MLRA-156A': 'W12844.DVF', 'MS Corn   MLRA-134': 'W03940.DVF', 'MI Cherry   MLRA-96': 'W14850.DVF', 'IL Corn   MLRA-108': 'W14842.DVF', 'ME Potato   MLRA-146': 'W14607.DVF', 'FL Strawberry   MLRA-155': 'W12842.DVF', 'KS Sorghum   MLRA-112': 'W13996.DVF', 'PA Apple   MLRA-148': 'W14751.DVF', 'CA Cotton   MLRA-17': 'W93193.DVF', 'NC Peanut   MLRA-153A': 'W13722.DVF', 'FL Cabbage   MLRA-155': 'W12842.DVF'}
        self.chem_name=chem_name
        self.scenarios=scenarios
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
        self.met = met_pool[scenarios] 
        self.final_res = get_jid(self.chem_name, self.scenarios, self.met, self.farm, self.mw, self.sol, self.koc, self.vp, self.aem, self.anm, self.aqp, self.tmper, self.n_ph, self.ph_out, self.hl_out)
        self.jid = self.final_res[0]
        self.link = self.final_res[1]
