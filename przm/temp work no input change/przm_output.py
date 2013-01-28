# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from geneec import GENEECdb
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb

import json
import base64
import urllib
from google.appengine.api import urlfetch


############Provide the key and connect to the picloud####################
api_key='3355'
api_secretkey='212ed160e3f416fdac8a3b71c90f3016722856b9'
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string}
###########################################################################

station_pool={'OR Hops   MLRA-2': 'Salem, OR', 'NC Corn - W   MLRA-130 (OP)': 'Asheville, NC', 'GA Peach   MLRA-133A': 'Macon, GA', 'CA Citrus   MLRA-17': 'Bakersfield, CA', 'NC Sweet Potato MLRA-133': 'Raleigh/Durham, NC', 'CA Lettuce  MLRA-14': 'Santa Maria, CA', 'FL Peppers MLRA-156A': 'W Palm Beach, FL', 'ID Potato   MLRA-11B': 'Pocatello, ID', 'FL Sweet Corn   MLRA-156B (OP)': 'W Palm Beach, FL', 'OR Mint   MLRA-2': 'Salem, OR', 'FL Citrus   MLRA-156A': 'W Palm Beach, FL', 'OR Christmas Trees  MLRA-2': 'Salem, OR', 'OH Corn   MLRA-111': 'Dayton, OH', 'MI Asparagus MLRA-96': 'Muskegon, MI', 'PR Coffee MLRA-270': 'San Juan, PR', 'FL Avocado MLRA-156A': 'Miami, FL', 'TX Corn   MLRA-86/87 (OP)': 'Austin, TX', 'CA Almonds MLRA-17': 'Sacramento, CA', 'FL Sugarcane   MLRA-156A': 'W Palm Beach, FL', 'CA Grape  MLRA-17': 'Fresno, CA', 'FL Cucumber   MLRA-156A': 'W Palm Beach, FL', 'PA Turf  MLRA-148': 'Harrisburg, PA', 'TX Wheat   MLRA-86/87 (OP)': 'Austin, TX', 'CA Corn   MLRA-17 (OP)': 'Sacramento, CA', 'NC Apple   MLRA-130': 'Asheville, NC', 'OR Berries MLRA-2 (OP)': 'Salem, OR', 'CA Onions MLRA-17': 'Bakersfield, CA', 'MN Sugarbeet   MLRA-56': 'Fargo, ND', 'TX Cotton   MLRA-86/87 (OP)': 'Austin, TX', 'FL Turf  MLRA-155': 'Daytona Beach, FL', 'MI Beans MLRA-99': 'Flint, MI', 'OR Sweet Corn   MLRA-2 (OP)': 'Salem, OR', 'NC Tobacco   MLRA-133A': 'Raleigh/Durham, NC', 'GA Onions MLRA-153A/133A': 'Savannah, GA', 'LA Sugarcane   MLRA-131': 'Baton Rouge, LA', 'NC Corn - E   MLRA-153A': 'Raleigh/Durham, NC', 'CA Sugarbeet  MLRA-17  (OP)': 'Fresno, CA', 'TX Cotton   MLRA-83D (NMC)': 'Brownsville, TX', 'TX Alfalfa   MLRA-86/87 (OP)': 'Austin, TX', 'MS Cotton   MLRA-134': 'Jackson, MS', 'MS Soybean   MLRA-134': 'Jackson, MS', 'GA Pecan   MLRA-133A': 'Tallahassee, FL', 'MN Alfalfa MLRA-56 (OP)': 'Fargo, ND', 'NC Cotton   MLRA-133A': 'Raleigh/Durham, NC', 'OR Wheat   MLRA-2 (OP)': 'Salem, OR', 'NY Grape   MLRA-100/101': 'Binghamton, NY', 'ND Corn   MLRA-56 (OP)': 'Fargo, ND', 'FL Carrots MLRA-156B': 'W Palm Beach, FL', 'ND Canola   MLRA-55A': 'Minot, ND', 'OR Filberts   MLRA-2': 'Salem, OR', 'FL Cabbage   MLRA-155': 'Tampa, FL', 'TX Sorghum   MLRA-86/87 (OP)': 'Austin, TX', 'CA Alfalfa MLRA-17 (OP)': 'Fresno, CA', 'ND Wheat   MLRA-56': 'Fargo, ND', 'CA Tomato MLRA-17': 'Fresno, CA', 'PA Corn   MLRA-148': 'Harrisburg, PA', 'PA Alfalfa   MLRA-148 (OP)': 'Harrisburg, PA', 'OR Apple   MLRA-2': 'Salem, OR', 'MS Corn   MLRA-134': 'Jackson, MS', 'PA Tomato MLRA-148': 'Allentown, PA', 'MI Cherry   MLRA-96': 'Traverse City, MI', 'FL Tomato   MLRA-155': 'W Palm Beach, FL', 'FL Strawberry   MLRA-155': 'Tampa, FL', 'IL Corn   MLRA-108': 'Peoria, IL', 'ME Potato   MLRA-146': 'Caribou, ME', 'OR Grass Seed   MLRA-2': 'Salem, OR', 'KS Sorghum   MLRA-112': 'Topeka, KS', 'PA Apple   MLRA-148': 'Harrisburg, PA', 'CA Cotton   MLRA-17': 'Fresno, CA', 'NC Peanut   MLRA-153A': 'Raleigh/Durham, NC', 'NC Alfalfa   MLRA-136 (OP)': 'Asheville, NC'}
met_pool={'OR Hops   MLRA-2': 'W24232.dvf', 'NC Corn - W   MLRA-130 (OP)': 'W03812.dvf', 'GA Peach   MLRA-133A': 'W03813.dvf', 'CA Citrus   MLRA-17': 'W23155.dvf', 'NC Sweet Potato MLRA-133': 'W13722.dvf', 'CA Lettuce  MLRA-14': 'W93193.dvf', 'FL Peppers MLRA-156A': 'W12844.dvf', 'ID Potato   MLRA-11B': 'W24156.dvf', 'FL Sweet Corn   MLRA-156B (OP)': 'W12844.dvf', 'OR Mint   MLRA-2': 'W24232.dvf', 'FL Citrus   MLRA-156A': 'W12844.dvf', 'OR Christmas Trees  MLRA-2': 'W24232.dvf', 'OH Corn   MLRA-111': 'W93815.dvf', 'MI Asparagus MLRA-96': 'w14840.dvf', 'PR Coffee MLRA-270': 'W11641.dvf', 'FL Avocado MLRA-156A': 'W12839.dvf', 'TX Corn   MLRA-86/87 (OP)': 'W13958.dvf', 'CA Almonds MLRA-17': 'W23232.dvf', 'FL Sugarcane   MLRA-156A': 'W12844.dvf', 'CA Grape  MLRA-17': 'W93193.dvf', 'FL Cucumber   MLRA-156A': 'W12844.dvf', 'PA Turf  MLRA-148': 'W14751.dvf', 'TX Wheat   MLRA-86/87 (OP)': 'W13958.dvf', 'CA Corn   MLRA-17 (OP)': 'W23232.dvf', 'NC Apple   MLRA-130': 'W03812.dvf', 'OR Berries MLRA-2 (OP)': 'W24232.dvf', 'CA Onions MLRA-17': 'W23155.dvf', 'MN Sugarbeet   MLRA-56': 'W14914.dvf', 'TX Cotton   MLRA-86/87 (OP)': 'W13958.dvf', 'FL Turf  MLRA-155': 'W12834.dvf', 'MI Beans MLRA-99': 'W14826.dvf', 'OR Sweet Corn   MLRA-2 (OP)': 'W24232.dvf', 'NC Tobacco   MLRA-133A': 'W13722.dvf', 'GA Onions MLRA-153A/133A': 'W03822.dvf', 'LA Sugarcane   MLRA-131': 'W13970.dvf', 'NC Corn - E   MLRA-153A': 'W13722.dvf', 'CA Sugarbeet  MLRA-17  (OP)': 'W93193.dvf', 'TX Cotton   MLRA-83D (NMC)': 'W12919.dvf', 'TX Alfalfa   MLRA-86/87 (OP)': 'W13958.dvf', 'MS Cotton   MLRA-134': 'W03940.dvf', 'MS Soybean   MLRA-134': 'W03940.dvf', 'GA Pecan   MLRA-133A': 'W93805.dvf', 'MN Alfalfa MLRA-56 (OP)': 'W14914.dvf', 'NC Cotton   MLRA-133A': 'W13722.dvf', 'OR Wheat   MLRA-2 (OP)': 'W24232.dvf', 'NY Grape   MLRA-100/101': 'W14860.dvf', 'ND Corn   MLRA-56 (OP)': 'W14914.dvf', 'FL Carrots MLRA-156B': 'W12844.dvf', 'ND Canola   MLRA-55A': 'W24013.dvf', 'OR Filberts   MLRA-2': 'W24232.dvf', 'FL Cabbage   MLRA-155': 'W12842.dvf', 'TX Sorghum   MLRA-86/87 (OP)': 'W13958.dvf', 'CA Alfalfa MLRA-17 (OP)': 'W93193.dvf', 'ND Wheat   MLRA-56': 'W14914.dvf', 'CA Tomato MLRA-17': 'W93193.dvf', 'PA Corn   MLRA-148': 'W14751.dvf', 'PA Alfalfa   MLRA-148 (OP)': 'W14751.dvf', 'OR Apple   MLRA-2': 'W24232.dvf', 'MS Corn   MLRA-134': 'W03940.dvf', 'PA Tomato MLRA-148': 'W14751.dvf', 'MI Cherry   MLRA-96': 'W14850.dvf', 'FL Tomato   MLRA-155': 'W12844.dvf', 'FL Strawberry   MLRA-155': 'W12842.dvf', 'IL Corn   MLRA-108': 'W14842.dvf', 'ME Potato   MLRA-146': 'W14607.dvf', 'OR Grass Seed   MLRA-2': 'W24232.dvf', 'KS Sorghum   MLRA-112': 'W13996.dvf', 'PA Apple   MLRA-148': 'W14751.dvf', 'CA Cotton   MLRA-17': 'W93193.dvf', 'NC Peanut   MLRA-153A': 'W13722.dvf', 'NC Alfalfa   MLRA-136 (OP)': 'W03812.dvf'}
inp_pool={'OR Hops   MLRA-2': 'OR1Hop-R.INP', 'NC Corn - W   MLRA-130 (OP)': 'NC2Cor-R.INP', 'GA Peach   MLRA-133A': 'GA1Pch-R.INP', 'CA Citrus   MLRA-17': 'CA1Cit-R.INP', 'NC Sweet Potato MLRA-133': 'NC1SWE-R.INP', 'CA Lettuce  MLRA-14': 'CA1Let-R.INP', 'FL Peppers MLRA-156A': 'FL1Pep-R.INP', 'ID Potato   MLRA-11B': 'ID1Pot-R.INP', 'FL Sweet Corn   MLRA-156B (OP)': 'FL1Swc-R.INP', 'OR Mint   MLRA-2': 'OR1Min-R.INP', 'FL Citrus   MLRA-156A': 'FL1Cit-R.INP', 'OR Christmas Trees  MLRA-2': 'OR1Xma-R.INP', 'OH Corn   MLRA-111': 'OH1Cor-R.INP', 'MI Asparagus MLRA-96': 'MI1Asp-R.INP', 'PR Coffee MLRA-270': 'PR1Cof-R.INP', 'FL Avocado MLRA-156A': 'FL1Avo-R.INP', 'TX Corn   MLRA-86/87 (OP)': 'TX1Cor-R.INP', 'CA Almonds MLRA-17': 'CA1Wal-R.INP', 'FL Sugarcane   MLRA-156A': 'FL1Sgc-R.INP', 'CA Grape  MLRA-17': 'CA1Gra-R.INP', 'FL Cucumber   MLRA-156A': 'FL1Cuc-R.INP', 'PA Turf  MLRA-148': 'PA1Tur-R.INP', 'TX Wheat   MLRA-86/87 (OP)': 'TX2Whe-R.INP', 'CA Corn   MLRA-17 (OP)': 'CA1Cor-R.INP', 'NC Apple   MLRA-130': 'NC1App-R.INP', 'OR Berries MLRA-2 (OP)': 'OR1Ber-R.INP', 'CA Onions MLRA-17': 'CA1Oni-R.INP', 'MN Sugarbeet   MLRA-56': 'MN1Sbe-R.INP', 'TX Cotton   MLRA-86/87 (OP)': 'TX2Ctt-R.INP', 'FL Turf  MLRA-155': 'FL1Tur-R.INP', 'MI Beans MLRA-99': 'MI1Bea-R.INP', 'OR Sweet Corn   MLRA-2 (OP)': 'OR1Scr-R.INP', 'NC Tobacco   MLRA-133A': 'NC1Tba-R.INP', 'GA Onions MLRA-153A/133A': 'GA1Oni-R.INP', 'LA Sugarcane   MLRA-131': 'LA1Sgc-R.INP', 'NC Corn - E   MLRA-153A': 'NC1Cor-R.INP', 'CA Sugarbeet  MLRA-17  (OP)': 'CA1Sbe-R.INP', 'TX Cotton   MLRA-83D (NMC)': 'TX1Ctt-R.INP', 'TX Alfalfa   MLRA-86/87 (OP)': 'TX1Alf-R.INP', 'MS Cotton   MLRA-134': 'MS1Ctt-R.INP', 'MS Soybean   MLRA-134': 'MS1Syb-R.INP', 'GA Pecan   MLRA-133A': 'GA1Pcn-R.INP', 'MN Alfalfa MLRA-56 (OP)': 'MN2Alf-R.INP', 'NC Cotton   MLRA-133A': 'NC1Ctt-R.INP', 'OR Wheat   MLRA-2 (OP)': 'OR1Whe-R.INP', 'NY Grape   MLRA-100/101': 'NY2Gra-R.INP', 'ND Corn   MLRA-56 (OP)': 'ND1Cor-R.INP', 'FL Carrots MLRA-156B': 'FL1Car-R.INP', 'ND Canola   MLRA-55A': 'ND1Cno-R.INP', 'OR Filberts   MLRA-2': 'OR1Fil-R.INP', 'FL Cabbage   MLRA-155': 'FL1Cbb-R.INP', 'TX Sorghum   MLRA-86/87 (OP)': 'TX1Srg-R.INP', 'CA Alfalfa MLRA-17 (OP)': 'CA1Alf-R.INP', 'ND Wheat   MLRA-56': 'ND1Whe-R.INP', 'CA Tomato MLRA-17': 'CA1Tma-R.INP', 'PA Corn   MLRA-148': 'PA1Cor-R.INP', 'PA Alfalfa   MLRA-148 (OP)': 'PA1Alf-R.INP', 'OR Apple   MLRA-2': 'OR1App-R.INP', 'MS Corn   MLRA-134': 'MS1Cor-R.INP', 'PA Tomato MLRA-148': 'PA1Veg-R.INP', 'MI Cherry   MLRA-96': 'MI1Che-R.INP', 'FL Tomato   MLRA-155': 'FL1Tma-R.INP', 'FL Strawberry   MLRA-155': 'FL1Str-R.INP', 'IL Corn   MLRA-108': 'IL1Cor-R.INP', 'ME Potato   MLRA-146': 'ME1Pot-R.INP', 'OR Grass Seed   MLRA-2': 'OR1Gra-R.INP', 'KS Sorghum   MLRA-112': 'KS2Srg-R.INP', 'PA Apple   MLRA-148': 'PA1App-R.INP', 'CA Cotton   MLRA-17': 'CA1Ctt-R.INP', 'NC Peanut   MLRA-153A': 'NC1Pnt-R.INP', 'NC Alfalfa   MLRA-136 (OP)': 'NC1Alf-R.INP'}
run_pool={'OR Hops   MLRA-2': 'OR1Hop-R.RUN', 'NC Corn - W   MLRA-130 (OP)': 'NC2Cor-R.RUN', 'GA Peach   MLRA-133A': 'GA1Pch-R.RUN', 'CA Citrus   MLRA-17': 'CA1Cit-R.RUN', 'NC Sweet Potato MLRA-133': 'NC1SWE-R.RUN', 'CA Lettuce  MLRA-14': 'CA1Let-R.RUN', 'FL Peppers MLRA-156A': 'FL1Pep-R.RUN', 'ID Potato   MLRA-11B': 'ID1Pot-R.RUN', 'FL Sweet Corn   MLRA-156B (OP)': 'FL1Swc-R.RUN', 'OR Mint   MLRA-2': 'OR1Min-R.RUN', 'FL Citrus   MLRA-156A': 'FL1Cit-R.RUN', 'OR Christmas Trees  MLRA-2': 'OR1Xma-R.RUN', 'OH Corn   MLRA-111': 'OH1Cor-R.RUN', 'MI Asparagus MLRA-96': 'MI1Asp-R.RUN', 'PR Coffee MLRA-270': 'PR1Cof-R.RUN', 'FL Avocado MLRA-156A': 'FL1Avo-R.RUN', 'TX Corn   MLRA-86/87 (OP)': 'TX1Cor-R.RUN', 'CA Almonds MLRA-17': 'CA1Wal-R.RUN', 'FL Sugarcane   MLRA-156A': 'FL1Sgc-R.RUN', 'CA Grape  MLRA-17': 'CA1Gra-R.RUN', 'FL Cucumber   MLRA-156A': 'FL1Cuc-R.RUN', 'PA Turf  MLRA-148': 'PA1Tur-R.RUN', 'TX Wheat   MLRA-86/87 (OP)': 'TX2Whe-R.RUN', 'CA Corn   MLRA-17 (OP)': 'CA1Cor-R.RUN', 'NC Apple   MLRA-130': 'NC1App-R.RUN', 'OR Berries MLRA-2 (OP)': 'OR1Ber-R.RUN', 'CA Onions MLRA-17': 'CA1Oni-R.RUN', 'MN Sugarbeet   MLRA-56': 'MN1Sbe-R.RUN', 'TX Cotton   MLRA-86/87 (OP)': 'TX2Ctt-R.RUN', 'FL Turf  MLRA-155': 'FL1Tur-R.RUN', 'MI Beans MLRA-99': 'MI1Bea-R.RUN', 'OR Sweet Corn   MLRA-2 (OP)': 'OR1Scr-R.RUN', 'NC Tobacco   MLRA-133A': 'NC1Tba-R.RUN', 'GA Onions MLRA-153A/133A': 'GA1Oni-R.RUN', 'LA Sugarcane   MLRA-131': 'LA1Sgc-R.RUN', 'NC Corn - E   MLRA-153A': 'NC1Cor-R.RUN', 'CA Sugarbeet  MLRA-17  (OP)': 'CA1Sbe-R.RUN', 'TX Cotton   MLRA-83D (NMC)': 'TX1Ctt-R.RUN', 'TX Alfalfa   MLRA-86/87 (OP)': 'TX1Alf-R.RUN', 'MS Cotton   MLRA-134': 'MS1Ctt-R.RUN', 'MS Soybean   MLRA-134': 'MS1Syb-R.RUN', 'GA Pecan   MLRA-133A': 'GA1Pcn-R.RUN', 'MN Alfalfa MLRA-56 (OP)': 'MN2Alf-R.RUN', 'NC Cotton   MLRA-133A': 'NC1Ctt-R.RUN', 'OR Wheat   MLRA-2 (OP)': 'OR1Whe-R.RUN', 'NY Grape   MLRA-100/101': 'NY2Gra-R.RUN', 'ND Corn   MLRA-56 (OP)': 'ND1Cor-R.RUN', 'FL Carrots MLRA-156B': 'FL1Car-R.RUN', 'ND Canola   MLRA-55A': 'ND1Cno-R.RUN', 'OR Filberts   MLRA-2': 'OR1Fil-R.RUN', 'FL Cabbage   MLRA-155': 'FL1Cbb-R.RUN', 'TX Sorghum   MLRA-86/87 (OP)': 'TX1Srg-R.RUN', 'CA Alfalfa MLRA-17 (OP)': 'CA1Alf-R.RUN', 'ND Wheat   MLRA-56': 'ND1Whe-R.RUN', 'CA Tomato MLRA-17': 'CA1Tma-R.RUN', 'PA Corn   MLRA-148': 'PA1Cor-R.RUN', 'PA Alfalfa   MLRA-148 (OP)': 'PA1Alf-R.RUN', 'OR Apple   MLRA-2': 'OR1App-R.RUN', 'MS Corn   MLRA-134': 'MS1Cor-R.RUN', 'PA Tomato MLRA-148': 'PA1Veg-R.RUN', 'MI Cherry   MLRA-96': 'MI1Che-R.RUN', 'FL Tomato   MLRA-155': 'FL1Tma-R.RUN', 'FL Strawberry   MLRA-155': 'FL1Str-R.RUN', 'IL Corn   MLRA-108': 'IL1Cor-R.RUN', 'ME Potato   MLRA-146': 'ME1Pot-R.RUN', 'OR Grass Seed   MLRA-2': 'OR1Gra-R.RUN', 'KS Sorghum   MLRA-112': 'KS2Srg-R.RUN', 'PA Apple   MLRA-148': 'PA1App-R.RUN', 'CA Cotton   MLRA-17': 'CA1Ctt-R.RUN', 'NC Peanut   MLRA-153A': 'NC1Pnt-R.RUN', 'NC Alfalfa   MLRA-136 (OP)': 'NC1Alf-R.RUN'}

def get_jid():

    url='https://api.picloud.com/r/3303/przm_s1_old' 
    data = urllib.urlencode({})

    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers) 
    jid= json.loads(response.content)['jid']
    output_st = ''
        
    while output_st!="done":
        response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid, headers=http_headers)
        output_st = json.loads(response_st.content)['info']['%s' %jid]['status']

    url_val = 'https://api.picloud.com/job/result/?jid='+str(jid)
    response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
    output_val = json.loads(response_val.content)['result']
    return(jid, output_st, output_val)

########call the function################# 
#def get_jid(met, inp, run):
#
#    url='https://api.picloud.com/r/3303/przm_s1' 
#    met=json.dumps(met)
#    inp=json.dumps(inp)
#    run=json.dumps(run)
#    data = urllib.urlencode({"met":met,"inp":inp,"run":run})
##    print(data)
##    print(type(met))
##    print(met)
#    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers) 
##    print(response)   
#    jid= json.loads(response.content)['jid']
#    output_st = ''
#        
#    while output_st!="done":
#        response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid, headers=http_headers)
#        output_st = json.loads(response_st.content)['info']['%s' %jid]['status']
#
#    url_val = 'https://api.picloud.com/job/result/?jid='+str(jid)
#    response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
#    output_val = json.loads(response_val.content)['result']
#    return(jid, output_st, output_val)



                                   
class PRZMOutputPage(webapp.RequestHandler):
    def get(self):
        #text_file1 = open('geneec/geneec_description.txt','r')
        #x = text_file1.read()        
        form = cgi.FieldStorage() 
        chem_name = form.getvalue('chemical_name')
        Scenarios =form.getvalue('Scenarios')
        station = station_pool[Scenarios]
        met_o = met_pool[Scenarios]
        inp_o = inp_pool[Scenarios]
        run_o = run_pool[Scenarios]               
        met_o=str(met_o)
        inp_o=str(inp_o)
        run_o=str(run_o)
                    
        Modeled_Start = form.getvalue('Modeled_Start')
        Modeled_end = form.getvalue('Modeled_end')
        Modeled_zones = form.getvalue('Modeled_zones')
        Number_crop = form.getvalue('Number_crop')
           
        final_res=get_jid()

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock.html', {'title2':'PRZM Output Page', 'title3':''})
        html = html + template.render(templatepath + '02modellinkblock.html', {'model':'przm'})
        html = html + template.render (templatepath + '03cubertext_links_left.html', {})                
        html = html + template.render(templatepath + '03euberinput_start.html', {'model':'przm'})
        html = html + """<table width="500" border="1">
                          <tr>
                            <th scope="col" width="200">Inputs</div></th>
                            <th scope="col" width="150">Unit</div></th>                            
                            <th scope="col" width="150">Value</div></th>
                          <tr>
                            <td>Chemical name</td>
                            <td>&nbsp</td>                            
                            <td>%s</td>
                          </tr>                            
                          <tr>
                            <td>Standard OPP/EFED Scenarios</td>
                            <td>&nbsp</td>                            
                            <td>%s</td>
                          </tr>
                          <tr>
                            <td>Weather station</td>
                            <td>&nbsp</td>                            
                            <td>%s</td>
                          </tr>
                          <tr>
                            <td>Met filename</td>
                            <td>&nbsp</td>                            
                            <td>%s</td>
                          </tr>
                          <tr>
                            <td>INP filename</td>
                            <td>&nbsp</td>                            
                            <td>%s</td>
                          </tr>
                          <tr>
                            <td>RUN filename</td>
                            <td>&nbsp</td>                            
                            <td>%s</td>
                          </tr>                                                    
                          <tr>
                            <td>Simulation Start Year</td>
                            <td>Year</td>                            
                            <td>%s</td>
                          </tr>
                          <tr>
                            <td>Simulation End Year</td>
                            <td>Year</td>                            
                            <td>%s</td>
                          </tr>
                          <tr>
                            <td>Modeled zones</td>
                            <td>&nbsp</td>                            
                            <td>%s</td>
                          </tr>
                          <tr>
                            <td>Number of simulated crops</td>
                            <td>&nbsp</td>                            
                            <td>%s</td>
                          </tr>                                                                                                                                                    
                          </table>
                          <p>&nbsp;</p>"""%(chem_name, Scenarios, station, met_o, inp_o, run_o, Modeled_Start, Modeled_end, Modeled_zones, Number_crop) 
                          
        html = html +  """<table width="700" border="1">
                          <tr>
                            <th scope="col">Outputs</div></th>
                            <th scope="col">Value</div></th>                            
                          </tr>
                          <tr>
                            <td>Simulation is finished. Please download your file from here</td>
                            <td><a href=%s>Link</a></td>
                          </tr>
                           """ %(final_res[2])
        html = html + """ <style type="text/css">img {margin-left: 50px;}</style> <img src="../stylesheets/images/PRZM.png" width="600" height="400" />"""

        html = html + template.render(templatepath + '03duberinput_end1.html', {})
        html = html + template.render(templatepath + '03cubertext_links.html', {})
        html = html + template.render(templatepath + '04uberform_end.html', {})
        html = html + template.render(templatepath + '05uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', PRZMOutputPage)], debug=True)
        

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()                                                                                                         




    