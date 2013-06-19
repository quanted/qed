# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
import json
from przm_exams import przm_exams_model
from przm_exams import przm_exams_tables
import base64
import urllib
from google.appengine.api import urlfetch
import sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
import keys_Picloud_S3
from datetime import datetime, timedelta

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string}
###########################################################################               
station_pool={'NC Sweet Potato MLRA-133': 'Raleigh/Durham, NC', 'ID Potato   MLRA-11B': 'Pocatello, ID', 'NY Grape   MLRA-100/101': 'Binghamton, NY', 'CA Citrus   MLRA-17': 'Bakersfield, CA', 'OR Hops   MLRA-2': 'Salem, OR', 'FL Sugarcane   MLRA-156A': 'W Palm Beach, FL', 'OR Mint   MLRA-2': 'Salem, OR', 'FL Citrus   MLRA-156A': 'W Palm Beach, FL', 'CA Almonds MLRA-17': 'Sacramento, CA', 'ND Canola   MLRA-55A': 'Minot, ND', 'MI Asparagus MLRA-96': 'Muskegon, MI', 'PR Coffee MLRA-270': 'San Juan, PR', 'FL Avocado MLRA-156A': 'Miami, FL', 'NC Tobacco   MLRA-133A': 'Raleigh/Durham, NC', 'CA Grape  MLRA-17': 'Fresno, CA', 'FL Cucumber   MLRA-156A': 'W Palm Beach, FL', 'OH Corn   MLRA-111': 'Dayton, OH', 'NC Apple   MLRA-130': 'Asheville, NC', 'CA Onions MLRA-17': 'Bakersfield, CA', 'PA Turf  MLRA-148': 'Harrisburg, PA', 'MI Beans MLRA-99': 'Flint, MI', 'GA Onions MLRA-153A/133A': 'Savannah, GA', 'LA Sugarcane   MLRA-131': 'Baton Rouge, LA', 'NC Corn - E   MLRA-153A': 'Raleigh/Durham, NC', 'OR Christmas Trees  MLRA-2': 'Salem, OR', 'MN Sugarbeet   MLRA-56': 'Fargo, ND', 'FL Turf  MLRA-155': 'Daytona Beach, FL', 'MS Cotton   MLRA-134': 'Jackson, MS', 'MS Soybean   MLRA-134': 'Jackson, MS', 'GA Pecan   MLRA-133A': 'Tallahassee, FL', 'OR Filberts   MLRA-2': 'Salem, OR', 'OR Grass Seed   MLRA-2': 'Salem, OR', 'GA Peach   MLRA-133A': 'Macon, GA', 'FL Carrots MLRA-156B': 'W Palm Beach, FL', 'NC Cotton   MLRA-133A': 'Raleigh/Durham, NC', 'CA Lettuce  MLRA-14': 'Santa Maria, CA', 'FL Tomato   MLRA-155': 'W Palm Beach, FL', 'OR Apple   MLRA-2': 'Salem, OR', 'ND Wheat   MLRA-56': 'Fargo, ND', 'CA Tomato MLRA-17': 'Fresno, CA', 'PA Corn   MLRA-148': 'Harrisburg, PA', 'FL Peppers MLRA-156A': 'W Palm Beach, FL', 'MS Corn   MLRA-134': 'Jackson, MS', 'MI Cherry   MLRA-96': 'Traverse City, MI', 'IL Corn   MLRA-108': 'Peoria, IL', 'ME Potato   MLRA-146': 'Caribou, ME', 'FL Strawberry   MLRA-155': 'Tampa, FL', 'KS Sorghum   MLRA-112': 'Topeka, KS', 'PA Apple   MLRA-148': 'Harrisburg, PA', 'CA Cotton   MLRA-17': 'Fresno, CA', 'NC Peanut   MLRA-153A': 'Raleigh/Durham, NC', 'FL Cabbage   MLRA-155': 'Tampa, FL'}
met_pool={'NC Sweet Potato MLRA-133': 'W13722.DVF', 'ID Potato   MLRA-11B': 'W24156.DVF', 'NY Grape   MLRA-100/101': 'W04725.DVF', 'CA Citrus   MLRA-17': 'W23155.DVF', 'OR Hops   MLRA-2': 'W24232.DVF', 'FL Sugarcane   MLRA-156A': 'W12844.DVF', 'OR Mint   MLRA-2': 'W24232.DVF', 'FL Citrus   MLRA-156A': 'W12844.DVF', 'CA Almonds MLRA-17': 'W23232.DVF', 'ND Canola   MLRA-55A': 'W24013.DVF', 'MI Asparagus MLRA-96': 'w14840.DVF', 'PR Coffee MLRA-270': 'W11641.DVF', 'FL Avocado MLRA-156A': 'W12839.DVF', 'NC Tobacco   MLRA-133A': 'W13722.DVF', 'CA Grape  MLRA-17': 'W93193.DVF', 'FL Cucumber   MLRA-156A': 'W12844.DVF', 'OH Corn   MLRA-111': 'W93815.DVF', 'NC Apple   MLRA-130': 'W03812.DVF', 'CA Onions MLRA-17': 'W23155.DVF', 'PA Turf  MLRA-148': 'W14751.DVF', 'MI Beans MLRA-99': 'W14826.DVF', 'GA Onions MLRA-153A/133A': 'W03822.DVF', 'LA Sugarcane   MLRA-131': 'W13970.DVF', 'NC Corn - E   MLRA-153A': 'W13722.DVF', 'OR Christmas Trees  MLRA-2': 'W24232.DVF', 'MN Sugarbeet   MLRA-56': 'W14914.DVF', 'FL Turf  MLRA-155': 'W12834.DVF', 'MS Cotton   MLRA-134': 'W03940.DVF', 'MS Soybean   MLRA-134': 'W03940.DVF', 'GA Pecan   MLRA-133A': 'W93805.DVF', 'OR Filberts   MLRA-2': 'W24232.DVF', 'OR Grass Seed   MLRA-2': 'W24232.DVF', 'GA Peach   MLRA-133A': 'W03813.DVF', 'FL Carrots MLRA-156B': 'W12844.DVF', 'NC Cotton   MLRA-133A': 'W13722.DVF', 'CA Lettuce  MLRA-14': 'W93193.DVF', 'FL Tomato   MLRA-155': 'W12844.DVF', 'OR Apple   MLRA-2': 'W24232.DVF', 'ND Wheat   MLRA-56': 'W14914.DVF', 'CA Tomato MLRA-17': 'W93193.DVF', 'PA Corn   MLRA-148': 'W14751.DVF', 'FL Peppers MLRA-156A': 'W12844.DVF', 'MS Corn   MLRA-134': 'W03940.DVF', 'MI Cherry   MLRA-96': 'W14850.DVF', 'IL Corn   MLRA-108': 'W14842.DVF', 'ME Potato   MLRA-146': 'W14607.DVF', 'FL Strawberry   MLRA-155': 'W12842.DVF', 'KS Sorghum   MLRA-112': 'W13996.DVF', 'PA Apple   MLRA-148': 'W14751.DVF', 'CA Cotton   MLRA-17': 'W93193.DVF', 'NC Peanut   MLRA-153A': 'W13722.DVF', 'FL Cabbage   MLRA-155': 'W12842.DVF'}
inp_pool={'NC Sweet Potato MLRA-133': 'NC1SWE-P.INP', 'ID Potato   MLRA-11B': 'ID1Pot-P.INP', 'NY Grape   MLRA-100/101': 'NY2Gra-P.INP', 'CA Citrus   MLRA-17': 'CA1Cit-P.INP', 'OR Hops   MLRA-2': 'OR1Hop-P.INP', 'FL Sugarcane   MLRA-156A': 'FL1Sgc-P.INP', 'OR Mint   MLRA-2': 'OR1Min-P.INP', 'FL Citrus   MLRA-156A': 'FL1Cit-P.INP', 'CA Almonds MLRA-17': 'CA1Wal-P.INP', 'ND Canola   MLRA-55A': 'ND1Cno-P.INP', 'MI Asparagus MLRA-96': 'MI1Asp-P.INP', 'PR Coffee MLRA-270': 'PR1Cof-P.INP', 'FL Avocado MLRA-156A': 'FL1Avo-P.INP', 'NC Tobacco   MLRA-133A': 'NC1Tba-P.INP', 'CA Grape  MLRA-17': 'CA1Gra-P.INP', 'FL Cucumber   MLRA-156A': 'FL1Cuc-P.INP', 'OH Corn   MLRA-111': 'OH1Cor-P.INP', 'NC Apple   MLRA-130': 'NC1App-P.INP', 'CA Onions MLRA-17': 'CA1Oni-P.INP', 'PA Turf  MLRA-148': 'PA1Tur-P.INP', 'MI Beans MLRA-99': 'MI1Bea-P.INP', 'GA Onions MLRA-153A/133A': 'GA1Oni-P.INP', 'LA Sugarcane   MLRA-131': 'LA1Sgc-P.INP', 'NC Corn - E   MLRA-153A': 'NC1Cor-P.INP', 'OR Christmas Trees  MLRA-2': 'OR1Xma-P.INP', 'MN Sugarbeet   MLRA-56': 'MN1Sbe-P.INP', 'FL Turf  MLRA-155': 'FL1Tur-P.INP', 'MS Cotton   MLRA-134': 'MS1Ctt-P.INP', 'MS Soybean   MLRA-134': 'MS1Syb-P.INP', 'GA Pecan   MLRA-133A': 'GA1Pcn-P.INP', 'OR Filberts   MLRA-2': 'OR1Fil-P.INP', 'OR Grass Seed   MLRA-2': 'OR1Gra-P.INP', 'GA Peach   MLRA-133A': 'GA1Pch-P.INP', 'FL Carrots MLRA-156B': 'FL1Car-P.INP', 'NC Cotton   MLRA-133A': 'NC1Ctt-P.INP', 'CA Lettuce  MLRA-14': 'CA1Let-P.INP', 'FL Tomato   MLRA-155': 'FL1Tma-P.INP', 'OR Apple   MLRA-2': 'OR1App-P.INP', 'ND Wheat   MLRA-56': 'ND1Whe-P.INP', 'CA Tomato MLRA-17': 'CA1Tma-P.INP', 'PA Corn   MLRA-148': 'PA1Cor-P.INP', 'FL Peppers MLRA-156A': 'FL1Pep-P.INP', 'MS Corn   MLRA-134': 'MS1Cor-P.INP', 'MI Cherry   MLRA-96': 'MI1Che-P.INP', 'IL Corn   MLRA-108': 'IL1Cor-P.INP', 'ME Potato   MLRA-146': 'ME1Pot-P.INP', 'FL Strawberry   MLRA-155': 'FL1Str-P.INP', 'KS Sorghum   MLRA-112': 'KS2Srg-P.INP', 'PA Apple   MLRA-148': 'PA1App-P.INP', 'CA Cotton   MLRA-17': 'CA1Ctt-P.INP', 'NC Peanut   MLRA-153A': 'NC1Pnt-P.INP', 'FL Cabbage   MLRA-155': 'FL1Cbb-P.INP'}
run_pool={'NC Sweet Potato MLRA-133': 'NC1SWE-P.RUN', 'ID Potato   MLRA-11B': 'ID1Pot-P.RUN', 'NY Grape   MLRA-100/101': 'NY2Gra-P.RUN', 'CA Citrus   MLRA-17': 'CA1Cit-P.RUN', 'OR Hops   MLRA-2': 'OR1Hop-P.RUN', 'FL Sugarcane   MLRA-156A': 'FL1Sgc-P.RUN', 'OR Mint   MLRA-2': 'OR1Min-P.RUN', 'FL Citrus   MLRA-156A': 'FL1Cit-P.RUN', 'CA Almonds MLRA-17': 'CA1Wal-P.RUN', 'ND Canola   MLRA-55A': 'ND1Cno-P.RUN', 'MI Asparagus MLRA-96': 'MI1Asp-P.RUN', 'PR Coffee MLRA-270': 'PR1Cof-P.RUN', 'FL Avocado MLRA-156A': 'FL1Avo-P.RUN', 'NC Tobacco   MLRA-133A': 'NC1Tba-P.RUN', 'CA Grape  MLRA-17': 'CA1Gra-P.RUN', 'FL Cucumber   MLRA-156A': 'FL1Cuc-P.RUN', 'OH Corn   MLRA-111': 'OH1Cor-P.RUN', 'NC Apple   MLRA-130': 'NC1App-P.RUN', 'CA Onions MLRA-17': 'CA1Oni-P.RUN', 'PA Turf  MLRA-148': 'PA1Tur-P.RUN', 'MI Beans MLRA-99': 'MI1Bea-P.RUN', 'GA Onions MLRA-153A/133A': 'GA1Oni-P.RUN', 'LA Sugarcane   MLRA-131': 'LA1Sgc-P.RUN', 'NC Corn - E   MLRA-153A': 'NC1Cor-P.RUN', 'OR Christmas Trees  MLRA-2': 'OR1Xma-P.RUN', 'MN Sugarbeet   MLRA-56': 'MN1Sbe-P.RUN', 'FL Turf  MLRA-155': 'FL1Tur-P.RUN', 'MS Cotton   MLRA-134': 'MS1Ctt-P.RUN', 'MS Soybean   MLRA-134': 'MS1Syb-P.RUN', 'GA Pecan   MLRA-133A': 'GA1Pcn-P.RUN', 'OR Filberts   MLRA-2': 'OR1Fil-P.RUN', 'OR Grass Seed   MLRA-2': 'OR1Gra-P.RUN', 'GA Peach   MLRA-133A': 'GA1Pch-P.RUN', 'FL Carrots MLRA-156B': 'FL1Car-P.RUN', 'NC Cotton   MLRA-133A': 'NC1Ctt-P.RUN', 'CA Lettuce  MLRA-14': 'CA1Let-P.RUN', 'FL Tomato   MLRA-155': 'FL1Tma-P.RUN', 'OR Apple   MLRA-2': 'OR1App-P.RUN', 'ND Wheat   MLRA-56': 'ND1Whe-P.RUN', 'CA Tomato MLRA-17': 'CA1Tma-P.RUN', 'PA Corn   MLRA-148': 'PA1Cor-P.RUN', 'FL Peppers MLRA-156A': 'FL1Pep-P.RUN', 'MS Corn   MLRA-134': 'MS1Cor-P.RUN', 'MI Cherry   MLRA-96': 'MI1Che-P.RUN', 'IL Corn   MLRA-108': 'IL1Cor-P.RUN', 'ME Potato   MLRA-146': 'ME1Pot-P.RUN', 'FL Strawberry   MLRA-155': 'FL1Str-P.RUN', 'KS Sorghum   MLRA-112': 'KS2Srg-P.RUN', 'PA Apple   MLRA-148': 'PA1App-P.RUN', 'CA Cotton   MLRA-17': 'CA1Ctt-P.RUN', 'NC Peanut   MLRA-153A': 'NC1Pnt-P.RUN', 'FL Cabbage   MLRA-155': 'FL1Cbb-P.RUN'}
exam_pool={'NC Sweet Potato MLRA-133': 'NC1SWE-P.EXA', 'ID Potato   MLRA-11B': 'ID1Pot-P.EXA', 'NY Grape   MLRA-100/101': 'NY2Gra-P.EXA', 'CA Citrus   MLRA-17': 'CA1Cit-P.EXA', 'OR Hops   MLRA-2': 'OR1Hop-P.EXA', 'FL Sugarcane   MLRA-156A': 'FL1Sgc-P.EXA', 'OR Mint   MLRA-2': 'OR1Min-P.EXA', 'FL Citrus   MLRA-156A': 'FL1Cit-P.EXA', 'CA Almonds MLRA-17': 'CA1Wal-P.EXA', 'ND Canola   MLRA-55A': 'ND1Cno-P.EXA', 'MI Asparagus MLRA-96': 'MI1Asp-P.EXA', 'PR Coffee MLRA-270': 'PR1Cof-P.EXA', 'FL Avocado MLRA-156A': 'FL1Avo-P.EXA', 'NC Tobacco   MLRA-133A': 'NC1Tba-P.EXA', 'CA Grape  MLRA-17': 'CA1Gra-P.EXA', 'FL Cucumber   MLRA-156A': 'FL1Cuc-P.EXA', 'OH Corn   MLRA-111': 'OH1Cor-P.EXA', 'NC Apple   MLRA-130': 'NC1App-P.EXA', 'CA Onions MLRA-17': 'CA1Oni-P.EXA', 'PA Turf  MLRA-148': 'PA1Tur-P.EXA', 'MI Beans MLRA-99': 'MI1Bea-P.EXA', 'GA Onions MLRA-153A/133A': 'GA1Oni-P.EXA', 'LA Sugarcane   MLRA-131': 'LA1Sgc-P.EXA', 'NC Corn - E   MLRA-153A': 'NC1Cor-P.EXA', 'OR Christmas Trees  MLRA-2': 'OR1Xma-P.EXA', 'MN Sugarbeet   MLRA-56': 'MN1Sbe-P.EXA', 'FL Turf  MLRA-155': 'FL1Tur-P.EXA', 'MS Cotton   MLRA-134': 'MS1Ctt-P.EXA', 'MS Soybean   MLRA-134': 'MS1Syb-P.EXA', 'GA Pecan   MLRA-133A': 'GA1Pcn-P.EXA', 'OR Filberts   MLRA-2': 'OR1Fil-P.EXA', 'OR Grass Seed   MLRA-2': 'OR1Gra-P.EXA', 'GA Peach   MLRA-133A': 'GA1Pch-P.EXA', 'FL Carrots MLRA-156B': 'FL1Car-P.EXA', 'NC Cotton   MLRA-133A': 'NC1Ctt-P.EXA', 'CA Lettuce  MLRA-14': 'CA1Let-P.EXA', 'FL Tomato   MLRA-155': 'FL1Tma-P.EXA', 'OR Apple   MLRA-2': 'OR1App-P.EXA', 'ND Wheat   MLRA-56': 'ND1Whe-P.EXA', 'CA Tomato MLRA-17': 'CA1Tma-P.EXA', 'PA Corn   MLRA-148': 'PA1Cor-P.EXA', 'FL Peppers MLRA-156A': 'FL1Pep-P.EXA', 'MS Corn   MLRA-134': 'MS1Cor-P.EXA', 'MI Cherry   MLRA-96': 'MI1Che-P.EXA', 'IL Corn   MLRA-108': 'IL1Cor-P.EXA', 'ME Potato   MLRA-146': 'ME1Pot-P.EXA', 'FL Strawberry   MLRA-155': 'FL1Str-P.EXA', 'KS Sorghum   MLRA-112': 'KS2Srg-P.EXA', 'PA Apple   MLRA-148': 'PA1App-P.EXA', 'CA Cotton   MLRA-17': 'CA1Ctt-P.EXA', 'NC Peanut   MLRA-153A': 'NC1Pnt-P.EXA', 'FL Cabbage   MLRA-155': 'FL1Cbb-P.EXA'}

Planting_pool={'NC Sweet Potato MLRA-133': '0805', 'ID Potato   MLRA-11B': '2505', 'NY Grape   MLRA-100/101': '2505', 'CA Citrus   MLRA-17': '2512', 'OR Hops   MLRA-2': '2503', 'FL Sugarcane   MLRA-156A': '2512', 'OR Mint   MLRA-2': '0804', 'FL Citrus   MLRA-156A': '2512', 'CA Almonds MLRA-17': '0901', 'ND Canola   MLRA-55A': '0905', 'MI Asparagus MLRA-96': '0906', 'PR Coffee MLRA-270': '2512', 'FL Avocado MLRA-156A': '2202', 'NC Tobacco   MLRA-133A': '0904', 'CA Grape  MLRA-17': '2501', 'FL Cucumber   MLRA-156A': '0910', 'OH Corn   MLRA-111': '2404', 'NC Apple   MLRA-130': '2503', 'CA Onions MLRA-17': '0901', 'PA Turf  MLRA-148': '2503', 'MI Beans MLRA-99': '2505', 'GA Onions MLRA-153A/133A': '0809', 'LA Sugarcane   MLRA-131': '2512', 'NC Corn - E   MLRA-153A': '0804', 'OR Christmas Trees  MLRA-2': '2512', 'MN Sugarbeet   MLRA-56': '0905', 'FL Turf  MLRA-155': '2501', 'MS Cotton   MLRA-134': '2404', 'MS Soybean   MLRA-134': '0904', 'GA Pecan   MLRA-133A': '0904', 'OR Filberts   MLRA-2': '2202', 'OR Grass Seed   MLRA-2': '0909', 'GA Peach   MLRA-133A': '2202', 'FL Carrots MLRA-156B': '0910', 'NC Cotton   MLRA-133A': '2505', 'CA Lettuce  MLRA-14': '0902', 'FL Tomato   MLRA-155': '2501', 'OR Apple   MLRA-2': '2503', 'ND Wheat   MLRA-56': '0905', 'CA Tomato MLRA-17': '2202', 'PA Corn   MLRA-148': '0904', 'FL Peppers MLRA-156A': '2508', 'MS Corn   MLRA-134': '0304', 'MI Cherry   MLRA-96': '2404', 'IL Corn   MLRA-108': '2404', 'ME Potato   MLRA-146': '2505', 'FL Strawberry   MLRA-155': '2409', 'KS Sorghum   MLRA-112': '1305', 'PA Apple   MLRA-148': '0904', 'CA Cotton   MLRA-17': '2404', 'NC Peanut   MLRA-153A': '0905', 'FL Cabbage   MLRA-155': '0910'}
EMergence_pool={'NC Sweet Potato MLRA-133': '1505', 'ID Potato   MLRA-11B': '0106', 'NY Grape   MLRA-100/101': '0106', 'CA Citrus   MLRA-17': '0101', 'OR Hops   MLRA-2': '0104', 'FL Sugarcane   MLRA-156A': '0101', 'OR Mint   MLRA-2': '1504', 'FL Citrus   MLRA-156A': '0101', 'CA Almonds MLRA-17': '1601', 'ND Canola   MLRA-55A': '1605', 'MI Asparagus MLRA-96': '1606', 'PR Coffee MLRA-270': '0101', 'FL Avocado MLRA-156A': '0103', 'NC Tobacco   MLRA-133A': '1604', 'CA Grape  MLRA-17': '0102', 'FL Cucumber   MLRA-156A': '1610', 'OH Corn   MLRA-111': '0105', 'NC Apple   MLRA-130': '0104', 'CA Onions MLRA-17': '1601', 'PA Turf  MLRA-148': '0104', 'MI Beans MLRA-99': '0106', 'GA Onions MLRA-153A/133A': '1509', 'LA Sugarcane   MLRA-131': '0101', 'NC Corn - E   MLRA-153A': '1504', 'OR Christmas Trees  MLRA-2': '0101', 'MN Sugarbeet   MLRA-56': '1605', 'FL Turf  MLRA-155': '0102', 'MS Cotton   MLRA-134': '0105', 'MS Soybean   MLRA-134': '1604', 'GA Pecan   MLRA-133A': '1604', 'OR Filberts   MLRA-2': '0103', 'OR Grass Seed   MLRA-2': '1609', 'GA Peach   MLRA-133A': '0103', 'FL Carrots MLRA-156B': '1610', 'NC Cotton   MLRA-133A': '0106', 'CA Lettuce  MLRA-14': '1602', 'FL Tomato   MLRA-155': '0102', 'OR Apple   MLRA-2': '0104', 'ND Wheat   MLRA-56': '1605', 'CA Tomato MLRA-17': '0103', 'PA Corn   MLRA-148': '1604', 'FL Peppers MLRA-156A': '0109', 'MS Corn   MLRA-134': '1004', 'MI Cherry   MLRA-96': '0105', 'IL Corn   MLRA-108': '0105', 'ME Potato   MLRA-146': '0106', 'FL Strawberry   MLRA-155': '0110', 'KS Sorghum   MLRA-112': '2005', 'PA Apple   MLRA-148': '1604', 'CA Cotton   MLRA-17': '0105', 'NC Peanut   MLRA-153A': '1605', 'FL Cabbage   MLRA-155': '1610'}
MAturation_pool={'NC Sweet Potato MLRA-133': '1509', 'ID Potato   MLRA-11B': '1508', 'NY Grape   MLRA-100/101': '0107', 'CA Citrus   MLRA-17': '0201', 'OR Hops   MLRA-2': '3007', 'FL Sugarcane   MLRA-156A': '0201', 'OR Mint   MLRA-2': '2507', 'FL Citrus   MLRA-156A': '0201', 'CA Almonds MLRA-17': '0208', 'ND Canola   MLRA-55A': '1508', 'MI Asparagus MLRA-96': '2508', 'PR Coffee MLRA-270': '0201', 'FL Avocado MLRA-156A': '1511', 'NC Tobacco   MLRA-133A': '0707', 'CA Grape  MLRA-17': '0103', 'FL Cucumber   MLRA-156A': '0512', 'OH Corn   MLRA-111': '2609', 'NC Apple   MLRA-130': '0305', 'CA Onions MLRA-17': '0106', 'PA Turf  MLRA-148': '1504', 'MI Beans MLRA-99': '2707', 'GA Onions MLRA-153A/133A': '0106', 'LA Sugarcane   MLRA-131': '0201', 'NC Corn - E   MLRA-153A': '2808', 'OR Christmas Trees  MLRA-2': '0201', 'MN Sugarbeet   MLRA-56': '0110', 'FL Turf  MLRA-155': '1502', 'MS Cotton   MLRA-134': '0709', 'MS Soybean   MLRA-134': '0109', 'GA Pecan   MLRA-133A': '2109', 'OR Filberts   MLRA-2': '1504', 'OR Grass Seed   MLRA-2': '1505', 'GA Peach   MLRA-133A': '1505', 'FL Carrots MLRA-156B': '1501', 'NC Cotton   MLRA-133A': '0108', 'CA Lettuce  MLRA-14': '0505', 'FL Tomato   MLRA-155': '2104', 'OR Apple   MLRA-2': '3004', 'ND Wheat   MLRA-56': '2507', 'CA Tomato MLRA-17': '0107', 'PA Corn   MLRA-148': '0407', 'FL Peppers MLRA-156A': '1511', 'MS Corn   MLRA-134': '2208', 'MI Cherry   MLRA-96': '0707', 'IL Corn   MLRA-108': '2109', 'ME Potato   MLRA-146': '0110', 'FL Strawberry   MLRA-155': '1011', 'KS Sorghum   MLRA-112': '2009', 'PA Apple   MLRA-148': '1005', 'CA Cotton   MLRA-17': '2009', 'NC Peanut   MLRA-153A': '0110', 'FL Cabbage   MLRA-155': '0802'}
HArvest_pool={'NC Sweet Potato MLRA-133': '2209', 'ID Potato   MLRA-11B': '1509', 'NY Grape   MLRA-100/101': '1510', 'CA Citrus   MLRA-17': '3112', 'OR Hops   MLRA-2': '0109', 'FL Sugarcane   MLRA-156A': '3112', 'OR Mint   MLRA-2': '0108', 'FL Citrus   MLRA-156A': '3112', 'CA Almonds MLRA-17': '1309', 'ND Canola   MLRA-55A': '2508', 'MI Asparagus MLRA-96': '1503', 'PR Coffee MLRA-270': '3112', 'FL Avocado MLRA-156A': '3011', 'NC Tobacco   MLRA-133A': '1607', 'CA Grape  MLRA-17': '3108', 'FL Cucumber   MLRA-156A': '1012', 'OH Corn   MLRA-111': '2510', 'NC Apple   MLRA-130': '2510', 'CA Onions MLRA-17': '1506', 'PA Turf  MLRA-148': '0111', 'MI Beans MLRA-99': '0409', 'GA Onions MLRA-153A/133A': '1506', 'LA Sugarcane   MLRA-131': '3112', 'NC Corn - E   MLRA-153A': '1209', 'OR Christmas Trees  MLRA-2': '3112', 'MN Sugarbeet   MLRA-56': '1510', 'FL Turf  MLRA-155': '1512', 'MS Cotton   MLRA-134': '2209', 'MS Soybean   MLRA-134': '1010', 'GA Pecan   MLRA-133A': '0110', 'OR Filberts   MLRA-2': '1011', 'OR Grass Seed   MLRA-2': '3006', 'GA Peach   MLRA-133A': '3108', 'FL Carrots MLRA-156B': '2201', 'NC Cotton   MLRA-133A': '0111', 'CA Lettuce  MLRA-14': '1205', 'FL Tomato   MLRA-155': '1505', 'OR Apple   MLRA-2': '3110', 'ND Wheat   MLRA-56': '0508', 'CA Tomato MLRA-17': '0109', 'PA Corn   MLRA-148': '0110', 'FL Peppers MLRA-156A': '0112', 'MS Corn   MLRA-134': '0209', 'MI Cherry   MLRA-96': '2107', 'IL Corn   MLRA-108': '2010', 'ME Potato   MLRA-146': '0510', 'FL Strawberry   MLRA-155': '1502', 'KS Sorghum   MLRA-112': '0110', 'PA Apple   MLRA-148': '1510', 'CA Cotton   MLRA-17': '1111', 'NC Peanut   MLRA-153A': '1010', 'FL Cabbage   MLRA-155': '1502'}

def get_jid(przm_exams_obj):
    url='https://api.picloud.com/r/3303/przm_exams_s1'
    chem_name = przm_exams_obj.chem_name
    noa = przm_exams_obj.noa
    scenarios = przm_exams_obj.scenarios
    unit = przm_exams_obj.unit
    met = przm_exams_obj.met_o
    inp = przm_exams_obj.inp_o
    run = przm_exams_obj.run_o
    exam = przm_exams_obj.exam_o
    MM = przm_exams_obj.MM
    DD = przm_exams_obj.DD
    YY = przm_exams_obj.YY
    CAM_f = przm_exams_obj.CAM_f
    DEPI = przm_exams_obj.DEPI_text
    Ar = przm_exams_obj.Ar_text
    EFF = przm_exams_obj.EFF
    Drft = przm_exams_obj.Drft

    farm = przm_exams_obj.farm
    mw = przm_exams_obj.mw
    sol = przm_exams_obj.sol
    koc = przm_exams_obj.koc
    vp = przm_exams_obj.vp
    aem = przm_exams_obj.aem
    anm = przm_exams_obj.anm
    aqp = przm_exams_obj.aqp
    tmper = przm_exams_obj.tmper
    n_ph = przm_exams_obj.n_ph
    ph_out = przm_exams_obj.ph_out
    hl_out = przm_exams_obj.hl_out

    input_list=[chem_name, noa, scenarios, unit, met, inp, run, exam, MM, DD, YY, CAM_f, DEPI, Ar, EFF, Drft, 
                farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out]

    input_list=json.dumps(input_list)
    data = urllib.urlencode({"input_list":input_list})
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

class PRZMEXAMSOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()

        scenarios =form.getvalue('Scenarios')
        chem_name = form.getvalue('chemical_name')
        noa = int(form.getvalue('NOA'))
        unit = form.getvalue('Unit')

        station = station_pool[scenarios]
        met_o = met_pool[scenarios]
        inp_o = inp_pool[scenarios]
        run_o = run_pool[scenarios]
        exam_o = exam_pool[scenarios]

        met_o=str(met_o)
        inp_o=str(inp_o)
        run_o=str(run_o)
        exam_o=str(exam_o)


####################################################        
######inputs related to different applications#####
####################################################
        Apt = []        #Application timings (indicators)
        Apt_p = []      #Application timings (words)
        DayRe = []      #Days relevant to the application
        Ap_mp = []      #Application methods (words)
        Ar = []         #Application rates
        CAM_f_p = []    #Chemical application Methods (words)
        CAM_f = []      #Chemical application Methods (indicators)
        EFF_p = []      #EFF (words)
        EFF = []        #EFF (numbers)
        Drft_p = []     #Drft (words)
        Drft = []       #Drft (numbers)
        DEPI_p = []     #DEPI (numbers)
        Date_inp = []   #Date 
        
        for i in range(noa):

            if i<1:    
                Apt_temp = form.getvalue('Apt')
                Apt.append(Apt_temp)
                Date_inp_temp=form.getvalue('Date_apt')
                Date_inp.append(Date_inp_temp)
                DayRe_temp = form.getvalue('DayRe')
                DayRe.append(DayRe_temp)
                
                CAM_1 = form.getvalue('CAM_1')
                CAM_2 = form.getvalue('CAM_2')
                CAM_3 = form.getvalue('CAM_3')
                CAM_4 = form.getvalue('CAM_4')  
                DEPI = form.getvalue('DEPI')
                
                Ap_m_temp = form.getvalue('Ap_m')
                Ap_mp.append(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[0])
                Ar_temp = form.getvalue('Ar')
                Ar.append(float(Ar_temp))
              
                CAM_f_p.append(CAM_select(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[0])   #CAM_f_p
                DEPI_p.append(CAM_select(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[1])   #DEPI                
                CAM_f.append(CAM_select(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[2])   #CAM_f
                EFF_p.append(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[2])
                Drft_p.append(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[3])
                EFF.append(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[4])
                Drft.append(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[5])

                if Apt_temp=='1':
                    Apt_p.append('Relative to planting')
                elif Apt_temp=='2':
                    Apt_p.append('Relative to emergence')
                elif Apt_temp=='3':
                    Apt_p.append('Relative to maturity')             
                elif Apt_temp=='4':
                    Apt_p.append('Relative to harvest')
                elif Apt_temp=='5':
                    Apt_p.append('Enter your own dates')                    
                    
            else:
                j=i+1
                Apt_temp = form.getvalue('Apt'+str(j))
                Apt.append(Apt_temp)
                Date_inp_temp=form.getvalue('Date_apt'+str(j))
                Date_inp.append(Date_inp_temp)             
                DayRe_temp = form.getvalue('DayRe'+str(j))
                DayRe.append(DayRe_temp)
                
                CAM_1 = form.getvalue('CAM_1_'+str(j))
                CAM_2 = form.getvalue('CAM_2_'+str(j))
                CAM_3 = form.getvalue('CAM_3_'+str(j))
                CAM_4 = form.getvalue('CAM_4_'+str(j)) 
                DEPI = form.getvalue('DEPI_'+str(j))
                
                Ap_m_temp = form.getvalue('Ap_m'+str(j))
                Ap_mp.append(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[0])
                Ar_temp = form.getvalue('Ar'+str(j))
                Ar.append(float(Ar_temp))
                
                CAM_f_p.append(CAM_select(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[0])   #CAM_f_p
                DEPI_p.append(CAM_select(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[1])   #DEPI                
                CAM_f.append(CAM_select(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[2])   #CAM_f
                EFF_p.append(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[2])
                Drft_p.append(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[3])
                EFF.append(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[4])
                Drft.append(Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[5])
                
                if Apt_temp=='1':
                    Apt_p.append('Relative to planting')
                elif Apt_temp=='2':
                    Apt_p.append('Relative to emergence')
                elif Apt_temp=='3':
                    Apt_p.append('Relative to maturity')             
                elif Apt_temp=='4':
                    Apt_p.append('Relative to harvest') 
                elif Apt_temp=='5':
                    Apt_p.append('Enter your own dates') 
                                                        
        MM=es_date(noa, scenarios, Apt, DayRe, Date_inp)[0]
        DD=es_date(noa, scenarios, Apt, DayRe, Date_inp)[1]
        YY='61'
        
        Ar_text=['%.4f' %i for i in Ar]
        CAM_f_f = [float(i) for i in CAM_f]
        CAM_text=['%.2f' %i for i in CAM_f_f]
        DEPI_f = [float(i) for i in DEPI_p]
        DEPI_text=['%.2f' %i for i in DEPI_f]

###################################################
#################EXAMS Inputs######################
###################################################

        farm =form.getvalue('farm_pond')
        mw = form.getvalue('molecular_weight')
        sol = form.getvalue('solubility')
        koc = form.getvalue('Koc')
        vp = form.getvalue('vapor_pressure')
        aem = form.getvalue('aerobic_aquatic_metabolism')
        anm = form.getvalue('anaerobic_aquatic_metabolism')
        aqp = form.getvalue('aquatic_direct_photolysis')
        tmper = form.getvalue('temperature')

        n_ph = float(form.getvalue('n_ph'))
        ph_out = []
        hl_out = []
        for i in range(int(n_ph)):
            j=i+1
            ph_temp = form.getvalue('ph'+str(j))
            ph_out.append(float(ph_temp))
            hl_temp = float(form.getvalue('hl'+str(j)))
            hl_out.append(hl_temp)  

        #PRZM_obj=(NOA, met_o, inp_o, run_o, MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft)
        przm_exams_obj = przm_exams_model.przm_exams(chem_name, noa, scenarios, unit, met_o, inp_o, run_o, exam_o, 
                                                     MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft, 
                                                     Apt_p, DayRe, Ap_mp, Ar, CAM_f_p, EFF_p, Drft_p, DEPI_f,
                                                     farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out)

        final_res=get_jid(przm_exams_obj)
        # express_obj.link = final_res[2]
        # print przm_exams_obj.__dict__.items()
        # print vars(przm_exams_obj)
        # print final_res
        przm_exams_obj.link = final_res[2][0]

###############PRZM plots#############################
        x_precip=[float(i) for i in final_res[2][1]]
        x_runoff=[float(i) for i in final_res[2][2]]
        x_et=[float(i) for i in final_res[2][3]]
        x_irr=[float(i) for i in final_res[2][4]]
        x_leachate=[float(i) for i in final_res[2][5]]
        x_pre_irr=[i+j for i,j in zip(x_precip,x_irr)]
        x_leachate=[i/100000 for i in x_leachate]

        Lim_inst=[float(i)*1000 for i in final_res[2][6]]
        Lim_24h=[float(i)*1000 for i in final_res[2][7]]
        Lim_96h=[float(i)*1000 for i in final_res[2][8]]
        Lim_21d=[float(i)*1000 for i in final_res[2][9]]
        Lim_60d=[float(i)*1000 for i in final_res[2][10]]
        Lim_90d=[float(i)*1000 for i in final_res[2][11]]
        Lim_y=[float(i)*1000 for i in final_res[2][12]]

        Ben_inst=[float(i)*1000 for i in final_res[2][13]]
        Ben_24h=[float(i)*1000 for i in final_res[2][14]]
        Ben_96h=[float(i)*1000 for i in final_res[2][15]]
        Ben_21d=[float(i)*1000 for i in final_res[2][16]]
        Ben_60d=[float(i)*1000 for i in final_res[2][17]]
        Ben_90d=[float(i)*1000 for i in final_res[2][18]]
        Ben_y=[float(i)*1000 for i in final_res[2][19]]

        # print form
        # print 'chem_name=', chem_name
        # print 'Apt=', Apt
        # print 'Apt_p=', Apt_p
        # print 'Ap_mp=', Ap_mp
        # print 'DayRe=', DayRe
        # print 'Ar=', Ar
        # print 'Ar_text=', Ar_text

        # print 'CAM_f_p=', CAM_f_p
        # print 'CAM_f=', CAM_f
        # print 'CAM_f_f=', CAM_f_f
        # print 'CAM_text=', CAM_text
        # print 'EFF_p=', EFF_p
        # print 'EFF=', EFF
        # print 'Drft_p=', Drft_p
        # print 'Drft=', Drft
        # print 'DEPI_p=', DEPI_p
        # print 'DEPI_f=', DEPI_f
        # print 'DEPI_text=', DEPI_text
        # print 'Date_inp=', Date_inp
        # print 'YY=', YY
        # print 'MM=', MM
        # print 'DD=', DD
        # print 'met_o=', met_o
        # print 'inp_o=', inp_o
        # print 'run_o=', run_o
        # print 'exam_o=', exam_o

        # print 'farm=', farm
        # print 'mw=', mw
        # print 'sol=', sol
        # print 'koc=', koc
        # print 'vp=', vp
        # print 'aem=', aem
        # print 'anm=', anm
        # print 'aqp=', aqp
        # print 'tmper=', tmper
        # print 'n_ph=', n_ph
        # print 'ph_out=', ph_out
        # print 'hl_out=', hl_out


        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'przm_exams','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'express', 
                'model_attributes':'PRZM-EXAMS Output'})

        html = html + przm_exams_tables.table_all(przm_exams_obj)

        html = html + """
        <br><div><table class="results" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">PRZM-EXAMS Results</div></th>
                          </tr>
                          <tr>
                            <th scope="col"><div align="center">Outputs</div></th>
                            <th scope="col"><div align="center">Value</div></th>                            
                          </tr>
                          <tr>
                            <td><div align="center">Simulation is finished. Please download your file from here</div></td>
                            <td><div align="center"><a href=%s>Link</a></div></td>
                          </tr>
                          <tr>          
                            <td id="x_pre_irr_val" data-val='%s' style="display: none"></td>  
                            <td id="x_leachate_val" data-val='%s' style="display: none"></td>  
                            <td id="x_et_val" data-val='%s' style="display: none"></td>  
                            <td id="x_runoff_val" data-val='%s' style="display: none"></td>
                            <td id="Lim_inst_val" data-val='%s' style="display: none"></td>  
                            <td id="Lim_24h_val" data-val='%s' style="display: none"></td>  
                            <td id="Lim_96h_val" data-val='%s' style="display: none"></td>  
                            <td id="Lim_21d_val" data-val='%s' style="display: none"></td>
                            <td id="Lim_60d_val" data-val='%s' style="display: none"></td>  
                            <td id="Lim_90d_val" data-val='%s' style="display: none"></td>  
                            <td id="Lim_y_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_inst_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_24h_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_96h_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_21d_val" data-val='%s' style="display: none"></td>
                            <td id="Ben_60d_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_90d_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_y_val" data-val='%s' style="display: none"></td>  
                          </tr>                               
        </table><br></div>"""%(przm_exams_obj.link, x_pre_irr, x_leachate, x_et, x_runoff,
                               Lim_inst, Lim_24h, Lim_96h, Lim_21d, Lim_60d, Lim_90d, Lim_y,  
                               Ben_inst, Ben_24h, Ben_96h, Ben_21d, Ben_60d, Ben_90d, Ben_y)

        html = html + template.render(templatepath + 'przm_exams_jqplot.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', PRZMEXAMSOutputPage)], debug=True)
 
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
